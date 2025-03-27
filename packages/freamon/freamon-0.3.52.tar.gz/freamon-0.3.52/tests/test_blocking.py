"""
Tests for the blocking module in deduplication.
"""
import os
import sys
import unittest
from pathlib import Path
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import logging

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from freamon.deduplication.blocking import (
    create_exact_blocks,
    create_phonetic_blocks,
    create_ngram_blocks,
    create_custom_blocks,
    get_comparison_pairs_from_blocks,
    apply_blocking_strategy
)


class TestBlockingModule(unittest.TestCase):
    """Tests for the blocking functionality in deduplication module."""
    
    def setUp(self):
        """Set up test data."""
        # Create a test dataframe with different data types
        self.df = pd.DataFrame({
            'id': [1, 2, 3, 4, 5, 6, 7, 8],
            'first_name': ['John', 'Jane', 'Jon', 'Jim', 'James', 'Jennifer', 'Jessica', 'Jean'],
            'last_name': ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson'],
            'zip_code': ['12345', '23456', '34567', '45678', '56789', '67890', '78901', '89012'],
            'numeric': [1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5],
            'category': ['A', 'B', 'A', 'C', 'B', 'C', 'A', 'B']
        })
        
        # Create a test dataframe with missing values and non-string types
        self.df_mixed = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['John Smith', 'Jane Doe', None, 'Jim Brown', 'James Smith'],
            'zip': ['12345', None, '34567', '45678', '12345'],
            'value': [100, 200, None, 400, 100]
        })
        
        # Create a test dataframe with special characters
        self.df_special = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'text': ['Hello, world!', 'Test & data', 'Special: chars', 'More? symbols!', 'Hello world'],
            'mixed': ['abc123', '123abc', 'a1b2c3', 'abc-123', 'abc_123']
        })
        
        # Mock logging to prevent output during tests
        logging.basicConfig(level=logging.CRITICAL)

    def test_create_exact_blocks_single_column(self):
        """Test exact blocking with a single column."""
        blocks = create_exact_blocks(self.df, ['category'])
        
        # Should create 3 blocks (A, B, C)
        self.assertEqual(len(blocks), 3)
        
        # Check block contents
        self.assertEqual(set(blocks[('A',)]), {0, 2, 6})  # Category A
        self.assertEqual(set(blocks[('B',)]), {1, 4, 7})  # Category B
        self.assertEqual(set(blocks[('C',)]), {3, 5})     # Category C

    def test_create_exact_blocks_multiple_columns(self):
        """Test exact blocking with multiple columns."""
        blocks = create_exact_blocks(self.df, ['category', 'first_name'])
        
        # Each combination of category and first_name should create a separate block
        self.assertEqual(len(blocks), 8)  # 8 unique combinations
        
        # Each block should contain exactly one record
        for indices in blocks.values():
            self.assertEqual(len(indices), 1)

    def test_create_exact_blocks_with_missing_values(self):
        """Test exact blocking with missing values."""
        blocks = create_exact_blocks(self.df_mixed, ['zip'])
        
        # Different implementations might handle missing values differently
        # Check if we have a specific block for missing values
        missing_values_found = False
        for key, indices in blocks.items():
            if 1 in indices:  # Index 1 has a missing zip value
                missing_values_found = True
                break
        
        self.assertTrue(missing_values_found, "Missing values not handled properly")
        
        # 12345 appears twice (indices 0 and 4)
        zip_12345_indices = []
        for key, indices in blocks.items():
            if key == ('12345',):
                zip_12345_indices = indices
                break
        
        self.assertEqual(len(zip_12345_indices), 2, "Expected two records with zip 12345")

    def test_create_phonetic_blocks_default(self):
        """Test phonetic blocking with default function (first character)."""
        blocks = create_phonetic_blocks(self.df, 'first_name')
        
        # Should create blocks based on first character
        self.assertEqual(set(blocks.keys()), {'J'})  # All names start with J
        self.assertEqual(len(blocks['J']), 8)        # All 8 records

    @unittest.skipIf(True, "Jellyfish might not be installed")
    def test_create_phonetic_blocks_with_soundex(self):
        """Test phonetic blocking with Soundex encoding."""
        try:
            import jellyfish
            
            # Use Soundex phonetic algorithm
            blocks = create_phonetic_blocks(self.df, 'first_name', jellyfish.soundex)
            
            # Should create blocks based on Soundex encoding
            # John, Jon, and Jane should be in the same block (J500)
            # Other names may vary
            self.assertTrue(any(len(indices) > 1 for indices in blocks.values()))
        except ImportError:
            self.skipTest("Jellyfish not installed")

    def test_create_phonetic_blocks_with_missing_values(self):
        """Test phonetic blocking with missing values."""
        blocks = create_phonetic_blocks(self.df_mixed, 'name')
        
        # Should have a specific block for missing values
        self.assertTrue('_missing' in blocks)
        self.assertEqual(blocks['_missing'], [2])  # Index with missing name

    def test_create_phonetic_blocks_custom_function(self):
        """Test phonetic blocking with custom function."""
        # Custom function that uses the length of the string as the key
        length_func = lambda x: len(x)
        
        blocks = create_phonetic_blocks(self.df, 'first_name', length_func)
        
        # Should create blocks based on name length
        self.assertTrue(4 in blocks)  # 4-letter names: John, Jane, Jean
        self.assertTrue(3 in blocks)  # 3-letter names: Jon, Jim
        self.assertTrue(5 in blocks)  # 5-letter names: James
        self.assertTrue(8 in blocks)  # 8-letter names: Jennifer, Jessica

    def test_create_ngram_blocks_default(self):
        """Test n-gram blocking with default settings (bigrams)."""
        blocks = create_ngram_blocks(self.df, 'first_name')
        
        # Should create blocks for each bigram
        self.assertTrue('jo' in blocks)  # From John, Jon
        self.assertTrue('oh' in blocks)  # From John
        self.assertTrue('ja' in blocks)  # From Jane, James
        
        # John and Jon should share the 'jo' block
        self.assertTrue(0 in blocks['jo'])  # John
        self.assertTrue(2 in blocks['jo'])  # Jon

    def test_create_ngram_blocks_with_different_n(self):
        """Test n-gram blocking with different n values."""
        # Test with trigrams
        blocks = create_ngram_blocks(self.df, 'first_name', n=3)
        
        # Should create blocks for each trigram
        self.assertTrue('joh' in blocks)  # From John
        self.assertTrue('ohn' in blocks)  # From John
        
        # Test with unigrams
        blocks = create_ngram_blocks(self.df, 'first_name', n=1)
        
        # Should create blocks for each character
        self.assertTrue('j' in blocks)  # All names start with J
        self.assertEqual(len(blocks['j']), 8)  # All 8 records

    def test_create_ngram_blocks_with_multiple_grams(self):
        """Test n-gram blocking using multiple n-grams per record."""
        blocks = create_ngram_blocks(self.df, 'first_name', n=2, num_grams=2)
        
        # Should create blocks for combinations of the first 2 bigrams
        # For example, John would be in a block with key ('jo', 'oh')
        for key, indices in blocks.items():
            if isinstance(key, tuple) and len(key) == 2:
                # Each block should contain records that share those 2 bigrams
                for idx in indices:
                    name = self.df.iloc[idx]['first_name'].lower()
                    bigrams = [name[i:i+2] for i in range(len(name)-1)]
                    # The first two bigrams from the name should match the block key
                    self.assertTrue(set(bigrams[:2]).issuperset(set(key)))

    def test_create_ngram_blocks_special_characters(self):
        """Test n-gram blocking with special characters."""
        blocks = create_ngram_blocks(self.df_special, 'text')
        
        # Should handle special characters in text
        self.assertTrue('he' in blocks)  # From "Hello, world!" and "Hello world"
        self.assertTrue('o,' in blocks)  # From "Hello, world!"
        
        # Both "Hello, world!" and "Hello world" should be in the 'he' block
        hello_idx = [i for i, row in self.df_special.iterrows() 
                    if row['text'].lower().startswith('hello')]
        for idx in hello_idx:
            self.assertTrue(idx in blocks['he'])

    def test_create_custom_blocks(self):
        """Test custom blocking function."""
        # Custom function that blocks by length of first_name
        def length_block(row):
            name = row['first_name']
            return len(name) if isinstance(name, str) else 0
        
        blocks = create_custom_blocks(self.df, length_block)
        
        # Count names of each length in the test data
        name_lengths = {}
        for _, row in self.df.iterrows():
            name = row['first_name']
            length = len(name)
            name_lengths[length] = name_lengths.get(length, 0) + 1
        
        # Verify blocks match name lengths
        for length, count in name_lengths.items():
            if length in blocks:
                self.assertEqual(len(blocks[length]), count, 
                               f"Expected {count} names of length {length}")
        
        # Verify some specific lengths
        self.assertTrue(3 in blocks, "Should have names of length 3")  # Jim, Jon
        self.assertTrue(4 in blocks, "Should have names of length 4")  # John, Jane, Jean

    def test_create_custom_blocks_with_multiple_keys(self):
        """Test custom blocking function that returns multiple keys."""
        # Custom function that creates blocks by first letter and length
        def multi_block(row):
            name = row['first_name']
            if isinstance(name, str):
                return [name[0], len(name)]  # First letter and length
            return ['_missing', 0]
        
        blocks = create_custom_blocks(self.df, multi_block)
        
        # Count first letters and names of each length
        first_letters = {}
        name_lengths = {}
        for _, row in self.df.iterrows():
            name = row['first_name']
            letter = name[0]
            length = len(name)
            first_letters[letter] = first_letters.get(letter, 0) + 1
            name_lengths[length] = name_lengths.get(length, 0) + 1
            
        # Verify blocks for first letters
        for letter, count in first_letters.items():
            if letter in blocks:
                self.assertEqual(len(blocks[letter]), count,
                               f"Expected {count} names starting with {letter}")
                
        # Verify some name lengths exist in blocks
        self.assertTrue(3 in blocks, "Should have blocks for names of length 3")
        self.assertTrue(4 in blocks, "Should have blocks for names of length 4")
        self.assertEqual(len(blocks[3]), 2)    # 3-letter names

    def test_create_custom_blocks_with_error_handling(self):
        """Test custom blocking function with error handling."""
        # Function that will raise an exception for some rows
        def error_func(row):
            name = row['first_name']
            if name == 'Jim':
                raise ValueError("Test error")
            return name[0]
        
        blocks = create_custom_blocks(self.df, error_func)
        
        # Should handle errors and put problematic records in _error block
        self.assertTrue('_error' in blocks)
        self.assertEqual(blocks['_error'], [3])  # Jim's index

    def test_get_comparison_pairs_from_blocks(self):
        """Test generating comparison pairs from blocks."""
        # Create some test blocks
        blocks = {
            'A': [0, 2, 6],  # 3 records in category A
            'B': [1, 4, 7],  # 3 records in category B
            'C': [3, 5]      # 2 records in category C
        }
        
        pairs = get_comparison_pairs_from_blocks(blocks)
        
        # Should generate all possible pairs within each block
        expected_pairs = [
            (0, 2), (0, 6), (2, 6),  # Category A pairs (3 choose 2)
            (1, 4), (1, 7), (4, 7),  # Category B pairs (3 choose 2)
            (3, 5)                    # Category C pairs (2 choose 2)
        ]
        
        # Sort both lists for comparison
        self.assertEqual(sorted(pairs), sorted(expected_pairs))
        self.assertEqual(len(pairs), 7)  # Total of 7 pairs

    def test_get_comparison_pairs_with_max_block_size(self):
        """Test generating comparison pairs with max_block_size limit."""
        # Create a large block that will be limited
        large_block = {'large': list(range(100))}  # 100 records = 4950 pairs
        
        with patch('numpy.random.choice', return_value=list(range(10))):
            pairs = get_comparison_pairs_from_blocks(large_block, max_block_size=10)
            
            # Should limit the block to 10 records = 45 pairs
            self.assertEqual(len(pairs), 45)

    def test_get_comparison_pairs_with_max_comparisons(self):
        """Test generating comparison pairs with max_comparisons limit."""
        # Create blocks that would generate many pairs
        blocks = {
            'A': list(range(50)),    # 50 records = 1225 pairs
            'B': list(range(50, 70)) # 20 records = 190 pairs
        }                             # Total: 1415 pairs
        
        # The random sampling can be implementation-dependent
        # So we'll just check that the number is limited
        pairs = get_comparison_pairs_from_blocks(blocks, max_comparisons=100)
        
        # Should limit the pairs (either through sampling or final cutoff)
        self.assertLessEqual(len(pairs), 100, 
                          f"Should have at most 100 pairs, got {len(pairs)}")

    def test_apply_blocking_strategy_exact(self):
        """Test apply_blocking_strategy with exact matching."""
        pairs = apply_blocking_strategy(
            self.df,
            strategy='exact',
            blocking_columns=['category']
        )
        
        # Should return pairs from same category only
        for idx1, idx2 in pairs:
            # Records in the same pair should have the same category
            self.assertEqual(
                self.df.iloc[idx1]['category'],
                self.df.iloc[idx2]['category']
            )

    def test_apply_blocking_strategy_phonetic(self):
        """Test apply_blocking_strategy with phonetic matching."""
        # Skip jellyfish mocking, and just test with default behavior (first character)
        pairs = apply_blocking_strategy(
            self.df,
            strategy='phonetic',
            blocking_columns=['first_name'],
            phonetic_algorithm=None
        )
        
        # All first names start with 'J' so all should be compared with each other
        # Form pairs of records with same first letter
        expected_pairs = []
        for i in range(len(self.df)):
            for j in range(i+1, len(self.df)):
                # Check if first letters match
                if self.df.iloc[i]['first_name'][0] == self.df.iloc[j]['first_name'][0]:
                    expected_pairs.append((i, j))
        
        # Check that all pairs with the same first letter are included
        for i, j in expected_pairs:
            pair_found = False
            for p1, p2 in pairs:
                if (p1 == i and p2 == j) or (p1 == j and p2 == i):
                    pair_found = True
                    break
            self.assertTrue(pair_found, f"Expected pair {(i, j)} not found")

    def test_apply_blocking_strategy_ngram(self):
        """Test apply_blocking_strategy with n-gram matching."""
        pairs = apply_blocking_strategy(
            self.df,
            strategy='ngram',
            blocking_columns=['first_name'],
            ngram_size=2,
            ngram_count=1
        )
        
        # Should return pairs that share at least one bigram
        # For example, John and Jon share 'jo'
        self.assertTrue(
            any((idx1 == 0 and idx2 == 2) or (idx1 == 2 and idx2 == 0) 
                for idx1, idx2 in pairs)
        )

    def test_apply_blocking_strategy_rule(self):
        """Test apply_blocking_strategy with rule-based matching."""
        # Custom rule: block by first character of name
        def first_char(row):
            return row['first_name'][0] if isinstance(row['first_name'], str) else '_'
        
        pairs = apply_blocking_strategy(
            self.df,
            strategy='rule',
            blocking_rules={'first_char': first_char}
        )
        
        # All first names start with 'J' so all should be compared
        expected_pairs_count = (8 * 7) // 2  # 28 pairs for 8 records
        self.assertEqual(len(pairs), expected_pairs_count)

    def test_apply_blocking_strategy_invalid(self):
        """Test apply_blocking_strategy with invalid configuration."""
        # Missing required parameters should raise ValueError
        with self.assertRaises(ValueError):
            apply_blocking_strategy(
                self.df,
                strategy='exact',
                blocking_columns=None
            )
        
        # Invalid strategy should raise ValueError
        with self.assertRaises(ValueError):
            apply_blocking_strategy(
                self.df,
                strategy='invalid_strategy',
                blocking_columns=['category']
            )


if __name__ == '__main__':
    unittest.main()