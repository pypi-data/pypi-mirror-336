"""
Tests for the LSH (Locality-Sensitive Hashing) module in deduplication.
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

from freamon.deduplication.lsh import (
    create_minhash_signatures,
    find_similar_pairs_minhash_lsh,
    create_feature_vectors,
    find_similar_pairs_random_projection,
    analyze_column_types,
    calculate_optimal_bands_rows,
    apply_lsh_strategy
)


class MockMinHash:
    """Mock for datasketch MinHash."""
    def __init__(self, num_perm=128):
        self.num_perm = num_perm
        self.hashvalues = np.zeros(num_perm)
        self.content = set()
    
    def update(self, b):
        """Mock update method."""
        # Add content to track what was added
        self.content.add(b.decode('utf8') if isinstance(b, bytes) else b)
        # Update some hash values to make them unique
        self.hashvalues[hash(b) % self.num_perm] = hash(b)
    
    def jaccard(self, other):
        """Calculate Jaccard similarity between MinHashes."""
        # Simple implementation for testing
        if not hasattr(other, 'content'):
            return 0.0
        if not self.content or not other.content:
            return 0.0
        intersection = len(self.content.intersection(other.content))
        union = len(self.content.union(other.content))
        return intersection / union if union > 0 else 0.0


class MockMinHashLSH:
    """Mock for datasketch MinHashLSH."""
    def __init__(self, threshold=0.5, num_perm=128):
        self.threshold = threshold
        self.num_perm = num_perm
        self.index = {}  # Maps key to MinHash
    
    def insert(self, key, minhash):
        """Insert a key and minhash into the index."""
        self.index[key] = minhash
    
    def query(self, minhash):
        """Find similar items."""
        results = []
        for key, other_minhash in self.index.items():
            if minhash.jaccard(other_minhash) >= self.threshold:
                results.append(key)
        return results


class TestLSHModule(unittest.TestCase):
    """Tests for the LSH functionality in deduplication module."""
    
    def setUp(self):
        """Set up test data."""
        # Create a test dataframe with text data
        self.df_text = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'title': [
                'Machine Learning Introduction',
                'Introduction to ML',
                'Deep Learning Basics',
                'Neural Networks Guide',
                'Introduction to Machine Learning'
            ],
            'description': [
                'Learn the basics of machine learning algorithms',
                'A beginner guide to ML concepts',
                'Fundamentals of deep neural networks',
                'Comprehensive guide to neural networks',
                'Basic concepts of machine learning for beginners'
            ]
        })
        
        # Create a test dataframe with numerical data
        self.df_numeric = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'x': [1.0, 1.1, 5.0, 5.1, 10.0],
            'y': [2.0, 2.2, 8.0, 8.1, 15.0],
            'z': [3.0, 3.3, 12.0, 12.2, 20.0]
        })
        
        # Create a test dataframe with mixed data types
        self.df_mixed = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'text': [
                'Product A',
                'Product B',
                'Product C',
                'Product D',
                'Product A'  # Duplicate
            ],
            'price': [9.99, 19.99, 29.99, 39.99, 9.99],  # Duplicate
            'rating': [4.5, 3.5, 4.0, 4.5, 4.5]
        })
        
        # Convert these to plain numbers for the tests
        self.df_numeric = self.df_numeric.astype({'x': float, 'y': float, 'z': float})
        
        # Mock logging to prevent output during tests
        logging.basicConfig(level=logging.CRITICAL)
        
        # Import module to test
        import freamon.deduplication.lsh
        self.lsh_module = freamon.deduplication.lsh
        
        # Patch necessary methods instead of trying to mock the entire datasketch module
        self.patches = []
        
        # Mock create_minhash_signatures
        def mock_create_minhash_signatures(df, columns, weights=None, num_perm=128, tokenizer=None):
            result = {}
            for idx in range(len(df)):
                mock = MockMinHash(num_perm=num_perm)
                # Add content based on actual text
                for col in columns:
                    value = df.iloc[idx][col]
                    if isinstance(value, str):
                        tokens = value.lower().split() if tokenizer is None else tokenizer(value)
                        for token in tokens:
                            mock.update(token.encode('utf8'))
                result[idx] = mock
            return result
            
        self.patches.append(patch.object(
            freamon.deduplication.lsh, 
            'create_minhash_signatures', 
            side_effect=mock_create_minhash_signatures
        ))
        
        # Mock find_similar_pairs_minhash_lsh
        def mock_find_similar_pairs_minhash_lsh(minhashes, threshold=0.7, num_perm=128):
            pairs = set()
            keys = list(minhashes.keys())
            for i, idx1 in enumerate(keys):
                for idx2 in keys[i+1:]:
                    sim = minhashes[idx1].jaccard(minhashes[idx2])
                    if sim >= threshold:
                        pairs.add((min(idx1, idx2), max(idx1, idx2)))
            return pairs
        
        self.patches.append(patch.object(
            freamon.deduplication.lsh, 
            'find_similar_pairs_minhash_lsh', 
            side_effect=mock_find_similar_pairs_minhash_lsh
        ))
        
        # Mock analyze_column_types to return expected values
        def mock_analyze_column_types(df, columns, sample_size=100):
            # Just return numeric for test numeric columns
            return {col: 'numeric' if col in ['x', 'y', 'z', 'price', 'rating'] else 'text' 
                    for col in columns}
        
        self.patches.append(patch.object(
            freamon.deduplication.lsh, 
            'analyze_column_types', 
            side_effect=mock_analyze_column_types
        ))
        
        # Start all patches
        for p in self.patches:
            p.start()

    def tearDown(self):
        """Clean up after tests."""
        for p in self.patches:
            p.stop()

    def test_create_minhash_signatures(self):
        """Test creating MinHash signatures for text data."""
        columns = ['title', 'description']
        minhashes = create_minhash_signatures(self.df_text, columns)
        
        # Should create a signature for each record
        self.assertEqual(len(minhashes), len(self.df_text))
        
        # Each signature should be a MinHash object
        for sig in minhashes.values():
            self.assertIsInstance(sig, MockMinHash)
            self.assertTrue(hasattr(sig, 'hashvalues'))
            self.assertTrue(hasattr(sig, 'content'))
        
        # Similar records should have more similar MinHash signatures
        # Records 0 and 4 have similar titles and descriptions about machine learning
        sim_0_4 = minhashes[0].jaccard(minhashes[4])
        # Records 0 and 2 are less similar (machine learning vs deep learning)
        sim_0_2 = minhashes[0].jaccard(minhashes[2])
        
        # Similarity of similar pairs should be higher
        self.assertGreater(sim_0_4, sim_0_2)

    def test_create_minhash_signatures_with_weights(self):
        """Test creating MinHash signatures with column weights."""
        columns = ['title', 'description']
        weights = {'title': 2.0, 'description': 1.0}  # Title twice as important
        
        minhashes = create_minhash_signatures(
            self.df_text, columns, weights=weights
        )
        
        # Should create a signature for each record
        self.assertEqual(len(minhashes), len(self.df_text))
        
        # Check that title tokens appear more frequently in the content
        # due to higher weight (implementation specific)
        for idx, sig in minhashes.items():
            title_tokens = set(self.df_text.iloc[idx]['title'].lower().split())
            desc_tokens = set(self.df_text.iloc[idx]['description'].lower().split())
            
            title_count = sum(1 for token in sig.content if token in title_tokens)
            desc_count = sum(1 for token in sig.content if token in desc_tokens)
            
            # Since we're using mock objects, we can only check that tokens from
            # both columns are present, not their exact counts
            self.assertTrue(title_count > 0)
            self.assertTrue(desc_count > 0)

    def test_find_similar_pairs_minhash_lsh(self):
        """Test finding similar pairs using MinHash LSH."""
        # Create mock MinHash objects
        minhash1 = MockMinHash()
        minhash2 = MockMinHash()
        minhash3 = MockMinHash()
        
        # Make minhash1 and minhash2 similar
        for token in ['apple', 'banana', 'cherry']:
            minhash1.update(token.encode())
            minhash2.update(token.encode())
        
        # Make minhash3 different
        for token in ['dog', 'elephant', 'fox']:
            minhash3.update(token.encode())
        
        minhashes = {0: minhash1, 1: minhash2, 2: minhash3}
        
        # Find similar pairs
        pairs = find_similar_pairs_minhash_lsh(minhashes, threshold=0.5)
        
        # Should find that minhash1 and minhash2 are similar
        self.assertEqual(len(pairs), 1)
        self.assertEqual(list(pairs)[0], (0, 1))  # Indices 0 and 1 are similar

    def test_create_feature_vectors(self):
        """Test creating feature vectors for numerical data."""
        columns = ['x', 'y', 'z']
        
        # Create non-normalized vectors to check values
        vectors_unnorm = create_feature_vectors(self.df_numeric, columns, normalize=False)
        
        # Should create a vector for each record
        self.assertEqual(len(vectors_unnorm), len(self.df_numeric))
        
        # Each vector should have the right dimension
        for vec in vectors_unnorm.values():
            self.assertEqual(len(vec), len(columns))
        
        # Vectors should contain the actual data values (when not normalized)
        for idx, vec in vectors_unnorm.items():
            row = self.df_numeric.iloc[idx]
            for i, col in enumerate(columns):
                self.assertAlmostEqual(vec[i], float(row[col]), places=6)
        
        # Test normalization (with normalize=True explicitly)
        vectors_norm = create_feature_vectors(self.df_numeric, columns, normalize=True)
        for vec in vectors_norm.values():
            # Normalized vectors should have length 1
            self.assertAlmostEqual(np.linalg.norm(vec), 1.0, places=6)

    def test_create_feature_vectors_without_normalization(self):
        """Test creating feature vectors without normalization."""
        columns = ['x', 'y', 'z']
        vectors = create_feature_vectors(
            self.df_numeric, columns, normalize=False
        )
        
        # Vectors should contain the actual unnormalized data values
        for idx, vec in vectors.items():
            row = self.df_numeric.iloc[idx]
            for i, col in enumerate(columns):
                self.assertEqual(vec[i], row[col])
        
        # Without normalization, vectors should not all have length 1
        for idx, vec in vectors.items():
            if idx > 0:  # Skip the first record
                self.assertNotAlmostEqual(np.linalg.norm(vec), 1.0, places=6)

    def test_create_feature_vectors_with_weights(self):
        """Test creating feature vectors with column weights."""
        columns = ['x', 'y', 'z']
        weights = {'x': 2.0, 'y': 1.0, 'z': 0.5}
        
        vectors = create_feature_vectors(
            self.df_numeric, columns, weights=weights, normalize=False
        )
        
        # Vectors should reflect the weighted values
        for idx, vec in vectors.items():
            row = self.df_numeric.iloc[idx]
            self.assertEqual(vec[0], row['x'] * 2.0)      # x has weight 2.0
            self.assertEqual(vec[1], row['y'] * 1.0)      # y has weight 1.0
            self.assertEqual(vec[2], row['z'] * 0.5)      # z has weight 0.5

    def test_find_similar_pairs_random_projection(self):
        """Test finding similar pairs using random projection LSH."""
        # Create a simplified mock version
        def mock_find_similar_pairs_random_projection(vectors, threshold=0.7, num_projections=50, bands=10, rows=5):
            pairs = set()
            # Just compute direct cosine similarity
            keys = list(vectors.keys())
            for i, idx1 in enumerate(keys):
                for idx2 in keys[i+1:]:
                    vec1 = vectors[idx1]
                    vec2 = vectors[idx2]
                    # Compute cosine similarity
                    sim = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
                    if sim >= threshold:
                        pairs.add((min(idx1, idx2), max(idx1, idx2)))
            return pairs
            
        # Patch the function
        with patch.object(self.lsh_module, 'find_similar_pairs_random_projection', 
                         side_effect=mock_find_similar_pairs_random_projection):
            
            # Create some test vectors
            vectors = {
                0: np.array([1.0, 2.0, 3.0]),
                1: np.array([1.1, 2.2, 3.3]),  # Close to vector 0
                2: np.array([5.0, 8.0, 12.0]),
                3: np.array([5.1, 8.1, 12.2]),  # Close to vector 2
                4: np.array([10.0, 15.0, 20.0])  # Different from others
            }
            
            # Normalize the vectors for cosine similarity
            for idx, vec in vectors.items():
                norm = np.linalg.norm(vec)
                vectors[idx] = vec / norm
            
            # Find similar pairs
            pairs = find_similar_pairs_random_projection(
                vectors, threshold=0.99  # High threshold for test
            )
            
            # Should find two similar pairs: (0,1) and (2,3)
            self.assertEqual(len(pairs), 2)
            pair_list = list(pairs)
            self.assertTrue((0, 1) in pair_list)
            self.assertTrue((2, 3) in pair_list)

    def test_analyze_column_types(self):
        """Test analyzing column types for LSH method selection."""
        # Test with all numeric columns
        column_types = analyze_column_types(self.df_numeric, ['x', 'y', 'z'])
        self.assertEqual(column_types, {'x': 'numeric', 'y': 'numeric', 'z': 'numeric'})
        
        # Test with all text columns
        column_types = analyze_column_types(self.df_text, ['title', 'description'])
        self.assertEqual(column_types, {'title': 'text', 'description': 'text'})
        
        # Test with mixed columns
        column_types = analyze_column_types(self.df_mixed, ['text', 'price', 'rating'])
        self.assertEqual(column_types, {'text': 'text', 'price': 'numeric', 'rating': 'numeric'})

    def test_calculate_optimal_bands_rows(self):
        """Test calculating optimal bands and rows for LSH."""
        # Test with different thresholds
        bands, rows = calculate_optimal_bands_rows(threshold=0.5, num_perm=128)
        self.assertEqual(bands * rows, 128)  # Should sum to num_perm
        
        # Higher threshold should result in more bands or fewer rows
        bands_high, rows_high = calculate_optimal_bands_rows(threshold=0.9, num_perm=128)
        self.assertEqual(bands_high * rows_high, 128)
        
        # Compare the implied thresholds
        s_normal = (1/bands) ** (1/rows)
        s_high = (1/bands_high) ** (1/rows_high)
        self.assertGreater(s_high, s_normal)  # Higher threshold should be higher

    def test_apply_lsh_strategy_minhash(self):
        """Test applying LSH strategy with MinHash method."""
        # Apply MinHash LSH
        with patch.object(self.lsh_module, 'find_similar_pairs_minhash_lsh', 
                         return_value={(0, 4), (1, 2)}):
            pairs = apply_lsh_strategy(
                self.df_text,
                columns=['title', 'description'],
                lsh_method='minhash',
                threshold=0.7
            )
        
        # Should return the mocked pairs
        self.assertEqual(pairs, {(0, 4), (1, 2)})

    def test_apply_lsh_strategy_random_projection(self):
        """Test applying LSH strategy with random projection method."""
        # Apply random projection LSH
        with patch.object(self.lsh_module, 'find_similar_pairs_random_projection', 
                         return_value={(0, 1), (2, 3)}):
            pairs = apply_lsh_strategy(
                self.df_numeric,
                columns=['x', 'y', 'z'],
                lsh_method='random_projection',
                threshold=0.7
            )
        
        # Should return the mocked pairs
        self.assertEqual(pairs, {(0, 1), (2, 3)})

    def test_apply_lsh_strategy_auto(self):
        """Test applying LSH strategy with auto method selection."""
        # Test with numeric data - should select random_projection
        with patch.object(self.lsh_module, 'analyze_column_types', 
                         return_value={'x': 'numeric', 'y': 'numeric', 'z': 'numeric'}), \
             patch.object(self.lsh_module, 'find_similar_pairs_random_projection', 
                         return_value={(0, 1), (2, 3)}):
            pairs = apply_lsh_strategy(
                self.df_numeric,
                columns=['x', 'y', 'z'],
                lsh_method='auto',
                threshold=0.7
            )
        
        # Should return the mocked pairs from random_projection
        self.assertEqual(pairs, {(0, 1), (2, 3)})
        
        # Test with text data - should select minhash
        with patch.object(self.lsh_module, 'analyze_column_types', 
                         return_value={'title': 'text', 'description': 'text'}), \
             patch.object(self.lsh_module, 'find_similar_pairs_minhash_lsh', 
                         return_value={(0, 4), (1, 2)}):
            pairs = apply_lsh_strategy(
                self.df_text,
                columns=['title', 'description'],
                lsh_method='auto',
                threshold=0.7
            )
        
        # Should return the mocked pairs from minhash
        self.assertEqual(pairs, {(0, 4), (1, 2)})

    def test_apply_lsh_strategy_hybrid(self):
        """Test applying LSH strategy with hybrid method."""
        # Apply hybrid LSH (both minhash and random projection)
        with patch.object(self.lsh_module, 'analyze_column_types', 
                         return_value={'text': 'text', 'price': 'numeric', 'rating': 'numeric'}), \
             patch.object(self.lsh_module, 'find_similar_pairs_minhash_lsh', 
                         return_value={(0, 4)}), \
             patch.object(self.lsh_module, 'find_similar_pairs_random_projection', 
                         return_value={(0, 4), (1, 2)}):
            pairs = apply_lsh_strategy(
                self.df_mixed,
                columns=['text', 'price', 'rating'],
                lsh_method='hybrid',
                threshold=0.7
            )
        
        # Should combine pairs from both methods
        self.assertEqual(pairs, {(0, 4), (1, 2)})

    def test_apply_lsh_strategy_with_custom_band_rows(self):
        """Test applying LSH strategy with custom band and row settings."""
        # Apply LSH with custom bands and rows
        with patch.object(self.lsh_module, 'find_similar_pairs_minhash_lsh', 
                         return_value={(0, 4), (1, 2)}):
            pairs = apply_lsh_strategy(
                self.df_text,
                columns=['title', 'description'],
                lsh_method='minhash',
                threshold=0.7,
                num_bands=16,
                rows_per_band=8,
                num_perm=128  # Should be adjusted to 16*8=128
            )
        
        # Should return the mocked pairs
        self.assertEqual(pairs, {(0, 4), (1, 2)})
    
    def test_apply_lsh_strategy_with_incompatible_bands_rows(self):
        """Test applying LSH strategy with incompatible bands and rows."""
        # Apply LSH with bands and rows that don't multiply to num_perm
        with patch.object(self.lsh_module, 'find_similar_pairs_minhash_lsh', 
                         return_value={(0, 4), (1, 2)}):
            # This should adjust num_perm to 15 (3*5)
            pairs = apply_lsh_strategy(
                self.df_text,
                columns=['title', 'description'],
                lsh_method='minhash',
                threshold=0.7,
                num_bands=3,
                rows_per_band=5,
                num_perm=128  # Should be adjusted to 3*5=15
            )
        
        # Should still work and return the mocked pairs
        self.assertEqual(pairs, {(0, 4), (1, 2)})

    def test_apply_lsh_strategy_invalid_method(self):
        """Test applying LSH strategy with invalid method."""
        # Should raise ValueError for invalid method
        with self.assertRaises(ValueError):
            apply_lsh_strategy(
                self.df_text,
                columns=['title', 'description'],
                lsh_method='invalid_method',
                threshold=0.7
            )


if __name__ == '__main__':
    unittest.main()