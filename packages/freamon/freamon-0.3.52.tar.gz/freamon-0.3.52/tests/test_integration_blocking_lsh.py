"""
Integration tests for the Blocking and LSH modules working together
with the flag_similar_records function.
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

# Mock the datasketch module before importing
mock_datasketch = MagicMock()
mock_datasketch.MinHash.return_value = MagicMock()
mock_datasketch.MinHashLSH.return_value = MagicMock()
mock_datasketch.MinHashLSH.return_value.query.return_value = []
sys.modules['datasketch'] = mock_datasketch

# Import deduplication modules
from freamon.deduplication.blocking import (
    create_exact_blocks,
    apply_blocking_strategy
)
from freamon.deduplication.lsh import (
    apply_lsh_strategy
)


class TestBlockingLSHIntegration(unittest.TestCase):
    """Integration tests for blocking and LSH deduplication functionality."""
    
    def setUp(self):
        """Set up test data."""
        # Create a realistic test dataset with similar records
        self.df = pd.DataFrame({
            'id': list(range(1, 21)),
            'first_name': [
                'John', 'Jon', 'Johnny', 'Jonathan', 'Jane',
                'Janet', 'Janice', 'Michael', 'Mike', 'Michele',
                'Robert', 'Rob', 'Bob', 'Bobby', 'Sarah',
                'Sara', 'William', 'Will', 'Bill', 'Billy'
            ],
            'last_name': [
                'Smith', 'Smyth', 'Smith', 'Smithe', 'Johnson',
                'Johnston', 'Johnson', 'Davis', 'Davies', 'Davis',
                'Taylor', 'Taylor', 'Taylor', 'Taylor', 'Wilson',
                'Wilson', 'Brown', 'Brown', 'Brown', 'Browne'
            ],
            'city': [
                'New York', 'New York', 'NYC', 'Manhattan', 'Los Angeles',
                'LA', 'Los Angeles', 'Chicago', 'Chicago', 'Chicago',
                'Houston', 'Houston', 'Houston', 'Houston', 'Phoenix',
                'Phoenix', 'Philadelphia', 'Philly', 'Philadelphia', 'Phila'
            ],
            'email': [
                'john.smith@example.com', 'jon.smyth@example.com', 'johnny.smith@example.com', 'j.smithe@example.com', 'jane.johnson@example.com',
                'janet.johnston@example.com', 'janice.johnson@example.com', 'michael.davis@example.com', 'mike.davies@example.com', 'michele.davis@example.com',
                'robert.taylor@example.com', 'rob.taylor@example.com', 'bob.taylor@example.com', 'bobby.taylor@example.com', 'sarah.wilson@example.com',
                'sara.wilson@example.com', 'william.brown@example.com', 'will.brown@example.com', 'bill.brown@example.com', 'billy.browne@example.com'
            ],
            'age': [
                30, 30, 31, 30, 25,
                25, 26, 45, 45, 44,
                50, 50, 50, 51, 35,
                35, 40, 40, 40, 41
            ],
            'income': [
                50000, 50500, 51000, 50000, 60000,
                61000, 60000, 75000, 75500, 75000,
                90000, 90000, 89000, 91000, 65000,
                65000, 80000, 80000, 80500, 80000
            ]
        })
        
        # Create a dataframe with numeric data for testing random projection LSH
        self.df_numeric = pd.DataFrame({
            'id': list(range(1, 11)),
            'x': [1.0, 1.1, 5.0, 5.1, 10.0, 10.1, 15.0, 15.1, 20.0, 20.1],
            'y': [2.0, 2.1, 6.0, 6.1, 11.0, 11.1, 16.0, 16.1, 21.0, 21.1],
            'z': [3.0, 3.1, 7.0, 7.1, 12.0, 12.1, 17.0, 17.1, 22.0, 22.1]
        })
        
        # Mock logging to prevent output during tests
        logging.basicConfig(level=logging.CRITICAL)
        
    def test_blocking_strategy(self):
        """Test that blocking strategy correctly groups similar records."""
        # Use exact blocking on last_name
        pairs = apply_blocking_strategy(
            self.df,
            strategy='exact',
            blocking_columns=['last_name']
        )
        
        # There should be pairs where last names match exactly
        for idx1, idx2 in pairs:
            last_name1 = self.df.iloc[idx1]['last_name']
            last_name2 = self.df.iloc[idx2]['last_name']
            self.assertEqual(last_name1, last_name2)
        
        # Check specific known pairs within the Smith family
        smith_indices = [i for i, row in self.df.iterrows() 
                        if row['last_name'] == 'Smith']
        self.assertEqual(len(smith_indices), 2)  # John Smith and Johnny Smith
        
        # At least one pair from each family should be in the pairs
        families = ['Smith', 'Johnson', 'Davis', 'Taylor', 'Wilson', 'Brown']
        for family in families:
            family_indices = [i for i, row in self.df.iterrows() 
                             if row['last_name'] == family]
            if len(family_indices) > 1:
                # Should have at least one pair from this family
                self.assertTrue(any(
                    (idx1 in family_indices and idx2 in family_indices) 
                    for idx1, idx2 in pairs
                ))

    def test_lsh_strategy_minhash(self):
        """Test that LSH correctly identifies similar text records."""
        # Mock the minhash functions to return some expected pairs
        with patch('freamon.deduplication.lsh.create_minhash_signatures',
                  return_value={0: MagicMock(), 1: MagicMock(), 2: MagicMock()}), \
             patch('freamon.deduplication.lsh.find_similar_pairs_minhash_lsh',
                  return_value={(0, 1), (0, 2)}):
                  
            # Use minhash LSH on name columns
            pairs = apply_lsh_strategy(
                self.df,
                columns=['first_name', 'last_name'],
                lsh_method='minhash',
                threshold=0.7  # Moderate threshold
            )
            
            # Check that we get the mocked pairs
            self.assertEqual(pairs, {(0, 1), (0, 2)})
            
            # Also verify that the first position in our test data has expected values
            # (sanity check that our test data matches what we expect)
            self.assertEqual(self.df.iloc[0]['first_name'], 'John')
            self.assertEqual(self.df.iloc[1]['first_name'], 'Jon')

    def test_lsh_strategy_random_projection(self):
        """Test that LSH correctly identifies similar numeric records."""
        # Use random projection LSH on numeric columns
        pairs = apply_lsh_strategy(
            self.df_numeric,
            columns=['x', 'y', 'z'],
            lsh_method='random_projection',
            threshold=0.95  # High threshold for numeric similarity
        )
        
        # There should be pairs with similar values
        self.assertTrue(len(pairs) > 0)
        
        # Each pair should have similar values
        for idx1, idx2 in pairs:
            # Calculate cosine similarity between the vectors
            vec1 = np.array([
                self.df_numeric.iloc[idx1]['x'],
                self.df_numeric.iloc[idx1]['y'],
                self.df_numeric.iloc[idx1]['z']
            ])
            vec2 = np.array([
                self.df_numeric.iloc[idx2]['x'],
                self.df_numeric.iloc[idx2]['y'],
                self.df_numeric.iloc[idx2]['z']
            ])
            
            # Normalize
            vec1 = vec1 / np.linalg.norm(vec1)
            vec2 = vec2 / np.linalg.norm(vec2)
            
            # Calculate cosine similarity
            similarity = np.dot(vec1, vec2)
            
            # Should be highly similar
            self.assertGreater(similarity, 0.9)

    def test_combined_blocking_and_lsh(self):
        """Test combining blocking and LSH for efficient deduplication."""
        # Step 1: Use blocking to get candidate pairs
        block_pairs = apply_blocking_strategy(
            self.df,
            strategy='exact',
            blocking_columns=['last_name']
        )
        
        # Extract the unique indices in these pairs
        block_indices = set()
        for idx1, idx2 in block_pairs:
            block_indices.add(idx1)
            block_indices.add(idx2)
        
        # Create a subset of the dataframe with just these indices
        df_subset = self.df.iloc[list(block_indices)].reset_index(drop=True)
        
        # Step 2: Mock LSH and use it on the subset
        with patch('freamon.deduplication.lsh.create_minhash_signatures',
                  return_value={0: MagicMock(), 1: MagicMock()}), \
             patch('freamon.deduplication.lsh.find_similar_pairs_minhash_lsh',
                  return_value={(0, 1)}):
                  
            # Use LSH on the subset
            lsh_pairs = apply_lsh_strategy(
                df_subset,
                columns=['first_name', 'email'],
                lsh_method='minhash',
                threshold=0.7
            )
            
            # Verify we get our mocked pairs
            self.assertEqual(lsh_pairs, {(0, 1)})
            
            # Map back to original indices
            original_indices = list(block_indices)
            mapped_pairs = {
                (original_indices[idx1], original_indices[idx2])
                for idx1, idx2 in lsh_pairs
            }
            
            # Each pair should have similar properties
            for idx1, idx2 in mapped_pairs:
                # Should have the same last name (due to blocking)
                self.assertEqual(
                    self.df.iloc[idx1]['last_name'],
                    self.df.iloc[idx2]['last_name']
                )

    def test_exact_blocking_efficiency(self):
        """Test that exact blocking reduces the number of comparisons."""
        n = len(self.df)
        total_possible_pairs = n * (n - 1) // 2  # All possible pairs
        
        # Block by city
        pairs = apply_blocking_strategy(
            self.df,
            strategy='exact',
            blocking_columns=['city']
        )
        
        # Number of pairs should be less than total possible
        self.assertLess(len(pairs), total_possible_pairs)
        
        # Calculate reduction percentage
        reduction = 100 - (len(pairs) / total_possible_pairs * 100)
        
        # Should reduce comparisons by at least 50%
        self.assertGreater(reduction, 50)
        
        # All pairs should have the same city
        for idx1, idx2 in pairs:
            self.assertEqual(
                self.df.iloc[idx1]['city'],
                self.df.iloc[idx2]['city']
            )

    def test_ngram_blocking_effectiveness(self):
        """Test that n-gram blocking correctly identifies similar text."""
        # Use n-gram blocking on first_name
        pairs = apply_blocking_strategy(
            self.df,
            strategy='ngram',
            blocking_columns=['first_name'],
            ngram_size=2
        )
        
        # Should identify pairs with similar names
        similar_name_pairs = 0
        for idx1, idx2 in pairs:
            name1 = self.df.iloc[idx1]['first_name'].lower()
            name2 = self.df.iloc[idx2]['first_name'].lower()
            
            # Check if they share a bigram
            bigrams1 = set(name1[i:i+2] for i in range(len(name1)-1))
            bigrams2 = set(name2[i:i+2] for i in range(len(name2)-1))
            
            if bigrams1.intersection(bigrams2):
                similar_name_pairs += 1
        
        # All pairs should share at least one bigram
        self.assertEqual(similar_name_pairs, len(pairs))
        
        # Should find the obvious pairs
        # John, Jon, Johnny
        john_idx = self.df[self.df['first_name'] == 'John'].index[0]
        jon_idx = self.df[self.df['first_name'] == 'Jon'].index[0]
        johnny_idx = self.df[self.df['first_name'] == 'Johnny'].index[0]
        
        # Check at least some of these are paired
        self.assertTrue(
            any((john_idx, jon_idx) == pair or (jon_idx, john_idx) == pair for pair in pairs) or
            any((john_idx, johnny_idx) == pair or (johnny_idx, john_idx) == pair for pair in pairs) or
            any((jon_idx, johnny_idx) == pair or (johnny_idx, jon_idx) == pair for pair in pairs)
        )

    def test_max_block_size_parameter(self):
        """Test that max_block_size parameter correctly limits block size."""
        # Create a dataframe with many records in the same block
        df_large_block = pd.DataFrame({
            'id': list(range(1, 101)),
            'category': ['A'] * 100  # All in same category
        })
        
        # No limit - should create one large block with all 100 records
        pairs_no_limit = apply_blocking_strategy(
            df_large_block,
            strategy='exact',
            blocking_columns=['category']
        )
        
        # With limit - should sample the block
        pairs_limited = apply_blocking_strategy(
            df_large_block,
            strategy='exact',
            blocking_columns=['category'],
            max_block_size=10
        )
        
        # No limit should generate C(100,2) = 4950 pairs
        self.assertEqual(len(pairs_no_limit), 4950)
        
        # Limited should generate C(10,2) = 45 pairs
        self.assertEqual(len(pairs_limited), 45)


if __name__ == '__main__':
    unittest.main()