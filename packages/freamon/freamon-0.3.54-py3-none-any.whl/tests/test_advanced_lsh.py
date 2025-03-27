"""
Tests for advanced LSH algorithms in the deduplication module.
"""

import unittest
import pandas as pd
import numpy as np
from freamon.deduplication.advanced_lsh import (
    SimHash,
    BKTree,
    SuperMinHash,
    flag_similar_records_advanced_lsh,
    create_simhash_signatures,
    find_similar_pairs_simhash,
    create_superminhash_signatures,
    find_similar_pairs_superminhash
)


class TestSimHash(unittest.TestCase):
    """Test the SimHash implementation."""
    
    def setUp(self):
        """Set up test data."""
        self.simhash = SimHash(hash_bits=64)
        self.text1 = "The quick brown fox jumps over the lazy dog"
        self.text2 = "The quick brown fox jumps over the lazy dog."
        self.text3 = "A completely different sentence with no similarity"
    
    def test_compute_hash(self):
        """Test SimHash hash computation."""
        hash1 = self.simhash.compute_hash(self.text1)
        self.assertIsInstance(hash1, int)
        self.assertTrue(0 <= hash1 <= 2**64)
        
        # Empty text should return 0
        hash_empty = self.simhash.compute_hash("")
        self.assertEqual(hash_empty, 0)
        
        # None should return 0
        hash_none = self.simhash.compute_hash(None)
        self.assertEqual(hash_none, 0)
    
    def test_similarity(self):
        """Test SimHash similarity calculation."""
        hash1 = self.simhash.compute_hash(self.text1)
        hash2 = self.simhash.compute_hash(self.text2)
        hash3 = self.simhash.compute_hash(self.text3)
        
        # Similar texts should have high similarity
        sim12 = SimHash.similarity(hash1, hash2)
        self.assertGreater(sim12, 0.9)
        
        # Different texts should have low similarity
        sim13 = SimHash.similarity(hash1, hash3)
        self.assertLess(sim13, 0.7)
        
        # Identical hashes should have similarity 1.0
        self.assertEqual(SimHash.similarity(hash1, hash1), 1.0)
    
    def test_hamming_distance(self):
        """Test hamming distance calculation."""
        # Test with simple bit patterns
        self.assertEqual(SimHash.hamming_distance(0, 0), 0)
        self.assertEqual(SimHash.hamming_distance(0, 1), 1)
        self.assertEqual(SimHash.hamming_distance(3, 7), 1)  # 011 vs 111
        self.assertEqual(SimHash.hamming_distance(15, 0), 4)  # 1111 vs 0000


class TestBKTree(unittest.TestCase):
    """Test the BK-Tree implementation."""
    
    def setUp(self):
        """Set up test data."""
        self.bktree = BKTree()
        self.words = ["hello", "hallo", "hell", "held", "help", "world"]
    
    def test_levenshtein_distance(self):
        """Test the Levenshtein distance implementation."""
        self.assertEqual(self.bktree._levenshtein_distance("hello", "hello"), 0)
        self.assertEqual(self.bktree._levenshtein_distance("hello", "hallo"), 1)
        self.assertEqual(self.bktree._levenshtein_distance("hello", "hell"), 1)
        self.assertEqual(self.bktree._levenshtein_distance("hello", "world"), 4)
        self.assertEqual(self.bktree._levenshtein_distance("", "hello"), 5)
        self.assertEqual(self.bktree._levenshtein_distance("hello", ""), 5)
    
    def test_add_and_find(self):
        """Test adding words and finding similar ones."""
        # Add words to the tree
        for i, word in enumerate(self.words):
            self.bktree.add(word, i)
        
        # Find words within distance 1
        results = self.bktree.find("hello", 1)
        self.assertEqual(len(results), 3)  # hello, hallo, hell
        
        # Check exact match
        exact_match = [r for r in results if r[0] == "hello"]
        self.assertEqual(len(exact_match), 1)
        self.assertEqual(exact_match[0][2], 0)  # Distance 0
        
        # Find words within distance 2
        results = self.bktree.find("hello", 2)
        self.assertEqual(len(results), 5)  # hello, hallo, hell, held, help
        
        # No matches should return empty list
        results = self.bktree.find("xyzzy", 0)
        self.assertEqual(len(results), 0)
    
    def test_find_most_similar(self):
        """Test finding the most similar word."""
        # Add words to the tree
        for i, word in enumerate(self.words):
            self.bktree.add(word, i)
        
        # Find the most similar to "helo"
        result = self.bktree.find_most_similar("helo", threshold=0.5)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "hello")  # Most similar word
        
        # Test with high threshold (no match)
        result = self.bktree.find_most_similar("xyz", threshold=0.9)
        self.assertIsNone(result)


class TestSuperMinHash(unittest.TestCase):
    """Test the SuperMinHash implementation."""
    
    def setUp(self):
        """Set up test data."""
        self.hasher = SuperMinHash(num_perm=128, seed=42)
        self.tokens1 = ["the", "quick", "brown", "fox", "jumps", "over", "lazy", "dog"]
        self.tokens2 = ["the", "quick", "brown", "fox", "jumps", "over", "sleepy", "dog"]
        self.tokens3 = ["completely", "different", "set", "of", "tokens"]
    
    def test_compute_signature(self):
        """Test signature computation."""
        sig1 = self.hasher.compute_signature(self.tokens1)
        self.assertIsInstance(sig1, np.ndarray)
        self.assertEqual(len(sig1), 128)
        
        # Empty tokens should return zeros
        sig_empty = self.hasher.compute_signature([])
        self.assertEqual(np.sum(sig_empty), 0)
    
    def test_jaccard_similarity(self):
        """Test Jaccard similarity calculation."""
        sig1 = self.hasher.compute_signature(self.tokens1)
        sig2 = self.hasher.compute_signature(self.tokens2)
        sig3 = self.hasher.compute_signature(self.tokens3)
        
        # Similar signatures should have high similarity
        sim12 = SuperMinHash.jaccard_similarity(sig1, sig2)
        self.assertGreater(sim12, 0.7)
        
        # Different signatures should have low similarity
        sim13 = SuperMinHash.jaccard_similarity(sig1, sig3)
        self.assertLess(sim13, 0.3)
        
        # Identical signatures should have similarity 1.0
        self.assertEqual(SuperMinHash.jaccard_similarity(sig1, sig1), 1.0)
        
        # Test with different shapes
        with self.assertRaises(ValueError):
            SuperMinHash.jaccard_similarity(sig1, sig1[:64])


class TestAdvancedLSHFunctions(unittest.TestCase):
    """Test the advanced LSH utility functions."""
    
    def setUp(self):
        """Set up test data."""
        # Create a small dataframe with text data
        self.df = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'text': [
                "The quick brown fox jumps over the lazy dog",
                "The quick brown fox jumps over the sleeping dog",
                "The fast brown fox leaps over the lazy dog",
                "A completely different sentence with no similarity",
                "The quick brown fox jumps over the lazy dog."
            ],
            'category': ['A', 'A', 'A', 'B', 'A']
        })
    
    def test_create_simhash_signatures(self):
        """Test creating SimHash signatures."""
        signatures = create_simhash_signatures(
            df=self.df,
            columns=['text'],
            hash_bits=64
        )
        
        self.assertEqual(len(signatures), 5)
        for idx, sig in signatures.items():
            self.assertIsInstance(sig, int)
    
    def test_find_similar_pairs_simhash(self):
        """Test finding similar pairs with SimHash."""
        signatures = create_simhash_signatures(
            df=self.df,
            columns=['text']
        )
        
        similar_pairs = find_similar_pairs_simhash(
            signatures=signatures,
            threshold=0.8
        )
        
        self.assertIsInstance(similar_pairs, set)
        # We expect texts 0, 1, 2, and 4 to be similar
        self.assertGreaterEqual(len(similar_pairs), 3)
    
    def test_create_superminhash_signatures(self):
        """Test creating SuperMinHash signatures."""
        signatures = create_superminhash_signatures(
            df=self.df,
            columns=['text'],
            num_perm=64
        )
        
        self.assertEqual(len(signatures), 5)
        for idx, sig in signatures.items():
            self.assertIsInstance(sig, np.ndarray)
            self.assertEqual(len(sig), 64)
    
    def test_find_similar_pairs_superminhash(self):
        """Test finding similar pairs with SuperMinHash."""
        signatures = create_superminhash_signatures(
            df=self.df,
            columns=['text'],
            num_perm=64
        )
        
        similar_pairs = find_similar_pairs_superminhash(
            signatures=signatures,
            threshold=0.7
        )
        
        self.assertIsInstance(similar_pairs, set)
        # We expect some similar pairs
        self.assertGreater(len(similar_pairs), 0)


class TestFlagSimilarRecordsAdvancedLSH(unittest.TestCase):
    """Test the flag_similar_records_advanced_lsh function."""
    
    def setUp(self):
        """Set up test data."""
        # Create a dataframe with known duplicates
        np.random.seed(42)
        self.df = pd.DataFrame({
            'id': range(1, 11),
            'text': [
                "The quick brown fox jumps over the lazy dog",
                "The quick brown fox jumps over the sleeping dog",
                "The fast brown fox leaps over the lazy dog",
                "A completely different sentence with no similarity",
                "The quick brown fox jumps over the lazy dog.",
                "Another unique sentence that has no duplicates",
                "The quick brown fox jumps over the lazy canine",
                "A sentence with unique content and no similarity",
                "The speedy brown fox jumps over the lazy dog",
                "This has nothing in common with other sentences"
            ],
            'category': ['A', 'A', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'C']
        })
        
        # Mark known duplicates
        self.df['is_known_duplicate'] = [False, False, False, False, True, 
                                         False, True, False, True, False]
    
    def test_simhash_method(self):
        """Test deduplication with SimHash method."""
        result = flag_similar_records_advanced_lsh(
            df=self.df,
            columns=['text'],
            method='simhash',
            threshold=0.8,
            flag_column='is_duplicate',
            group_column='group_id'
        )
        
        # Check that duplicates were found
        self.assertIn('is_duplicate', result.columns)
        self.assertIn('group_id', result.columns)
        self.assertGreater(result['is_duplicate'].sum(), 0)
        self.assertGreater(result['group_id'].max(), 0)
    
    def test_bktree_method(self):
        """Test deduplication with BKTree method."""
        result = flag_similar_records_advanced_lsh(
            df=self.df,
            columns=['text'],
            method='bktree',
            threshold=0.7,
            flag_column='is_duplicate',
            similarity_column='similarity'
        )
        
        # Check that duplicates were found
        self.assertIn('is_duplicate', result.columns)
        self.assertIn('similarity', result.columns)
        self.assertGreater(result['is_duplicate'].sum(), 0)
    
    def test_superminhash_method(self):
        """Test deduplication with SuperMinHash method."""
        result = flag_similar_records_advanced_lsh(
            df=self.df,
            columns=['text'],
            method='superminhash',
            threshold=0.7,
            flag_column='is_duplicate'
        )
        
        # Check that duplicates were found
        self.assertIn('is_duplicate', result.columns)
        self.assertGreater(result['is_duplicate'].sum(), 0)
    
    def test_invalid_method(self):
        """Test with invalid method."""
        with self.assertRaises(ValueError):
            flag_similar_records_advanced_lsh(
                df=self.df,
                columns=['text'],
                method='invalid_method'
            )


if __name__ == '__main__':
    unittest.main()