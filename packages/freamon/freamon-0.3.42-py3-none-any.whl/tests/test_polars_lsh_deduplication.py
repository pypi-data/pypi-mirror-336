"""
Tests for the Polars-optimized LSH deduplication module.
"""
import pytest
import pandas as pd
import numpy as np
import polars as pl
from typing import List, Tuple

from freamon.deduplication.polars_lsh_deduplication import (
    polars_lsh_deduplication,
    batch_process_texts,
    batch_create_minhash_signatures,
    create_hash_tables,
    verify_candidate_pairs,
    find_clusters,
    choose_representatives,
    streaming_lsh_deduplication
)
from freamon.utils.text_utils import TextProcessor


class TestPolarsLSHDeduplication:
    """Test class for Polars-optimized LSH deduplication functionality."""
    
    @pytest.fixture
    def sample_texts(self) -> List[str]:
        """Create sample texts for testing."""
        return [
            "This is a test document for LSH deduplication",
            "A different document with unique content",
            "Another unique document for testing",
            "This is a test document for LSH deduplication",  # Exact duplicate of first
            "This is a test document for LSH deduplication with slight change",  # Near duplicate
            "Another unique text for the algorithm to process",
            "A document that is completely different from all others",
            "This is a test document for deduplication using LSH",  # Near duplicate
        ]
    
    @pytest.fixture
    def sample_dataframe(self) -> pd.DataFrame:
        """Create sample dataframe for testing."""
        return pd.DataFrame({
            'id': list(range(8)),
            'text': [
                "This is a test document for LSH deduplication",
                "A different document with unique content",
                "Another unique document for testing",
                "This is a test document for LSH deduplication",  # Exact duplicate of first
                "This is a test document for LSH deduplication with slight change",  # Near duplicate
                "Another unique text for the algorithm to process",
                "A document that is completely different from all others",
                "This is a test document for deduplication using LSH",  # Near duplicate
            ],
            'value': np.random.rand(8)
        })
    
    @pytest.fixture
    def sample_polars_dataframe(self, sample_dataframe) -> pl.DataFrame:
        """Create sample Polars dataframe for testing."""
        return pl.from_pandas(sample_dataframe)
    
    @pytest.fixture
    def text_processor(self) -> TextProcessor:
        """Create text processor for testing."""
        return TextProcessor()
    
    def test_batch_process_texts(self, sample_texts, text_processor):
        """Test batch processing of texts."""
        # Test with default parameters
        processed_texts = batch_process_texts(
            texts=sample_texts,
            text_processor=text_processor,
            preprocess=True,
            batch_size=3  # Small batch size for testing
        )
        
        # Should return same number of texts
        assert len(processed_texts) == len(sample_texts)
        
        # Test without preprocessing
        no_preprocess = batch_process_texts(
            texts=sample_texts,
            text_processor=text_processor,
            preprocess=False
        )
        
        # Should return original texts
        assert no_preprocess == sample_texts
    
    def test_batch_create_minhash_signatures(self, sample_texts):
        """Test batch creation of MinHash signatures."""
        signatures = batch_create_minhash_signatures(
            texts=sample_texts,
            shingle_size=3,
            num_permutations=50,
            batch_size=2  # Small batch size for testing
        )
        
        # Should return same number of signatures as texts
        assert len(signatures) == len(sample_texts)
        
        # Each signature should have the specified number of permutations
        for signature in signatures:
            if signature:  # Empty texts will have empty signatures
                assert len(signature) == 50
        
        # Identical texts should have identical signatures
        assert signatures[0] == signatures[3]
    
    def test_create_hash_tables(self, sample_texts):
        """Test creation of LSH hash tables."""
        # Create signatures
        signatures = batch_create_minhash_signatures(
            texts=sample_texts,
            shingle_size=3,
            num_permutations=50
        )
        
        # Create hash tables
        hash_tables, candidate_pairs = create_hash_tables(
            signatures=signatures,
            num_bands=10
        )
        
        # Should have 10 hash tables (one per band)
        assert len(hash_tables) == 10
        
        # Should find candidate pairs
        assert len(candidate_pairs) > 0
        
        # Identical documents should be candidates
        assert 3 in candidate_pairs.get(0, []) or 0 in candidate_pairs.get(3, [])
    
    def test_verify_candidate_pairs(self, sample_texts):
        """Test verification of candidate pairs."""
        # Create signatures
        signatures = batch_create_minhash_signatures(
            texts=sample_texts,
            shingle_size=3,
            num_permutations=100
        )
        
        # Create hash tables and find candidate pairs
        _, candidate_pairs = create_hash_tables(
            signatures=signatures,
            num_bands=20
        )
        
        # Verify candidate pairs
        similar_pairs = verify_candidate_pairs(
            signatures=signatures,
            candidate_pairs=candidate_pairs,
            threshold=0.7,
            num_minhash_permutations=100
        )
        
        # Should find some similar pairs
        assert len(similar_pairs) > 0
        
        # High threshold should find fewer pairs
        high_threshold_pairs = verify_candidate_pairs(
            signatures=signatures,
            candidate_pairs=candidate_pairs,
            threshold=0.9,
            num_minhash_permutations=100
        )
        
        assert len(high_threshold_pairs) <= len(similar_pairs)
    
    def test_find_clusters(self, sample_texts):
        """Test finding clusters of similar texts."""
        # Create signatures
        signatures = batch_create_minhash_signatures(
            texts=sample_texts,
            shingle_size=3,
            num_permutations=100
        )
        
        # Create hash tables and find candidate pairs
        _, candidate_pairs = create_hash_tables(
            signatures=signatures,
            num_bands=20
        )
        
        # Verify candidate pairs
        similar_pairs = verify_candidate_pairs(
            signatures=signatures,
            candidate_pairs=candidate_pairs,
            threshold=0.7,
            num_minhash_permutations=100
        )
        
        # Find clusters
        clusters = find_clusters(
            similar_pairs=similar_pairs,
            num_texts=len(sample_texts)
        )
        
        # Should find at least one cluster (at least the duplicate documents)
        assert len(clusters) > 0
        
        # Each cluster should have at least 2 documents
        for cluster in clusters:
            assert len(cluster) >= 2
            
        # Identical documents should be in the same cluster
        for cluster in clusters:
            if 0 in cluster:
                assert 3 in cluster
    
    def test_choose_representatives(self, sample_texts):
        """Test choosing representative texts from clusters."""
        # Create a simple cluster
        clusters = [{0, 3, 4, 7}]  # Cluster containing similar documents
        
        # Test keep='first' strategy
        representatives = choose_representatives(
            clusters=clusters,
            texts=sample_texts,
            keep='first'
        )
        
        # Should keep index 0 and all unclustered texts
        assert 0 in representatives
        assert 1 in representatives
        assert 2 in representatives
        assert 3 not in representatives
        assert 4 not in representatives
        assert 5 in representatives
        assert 6 in representatives
        assert 7 not in representatives
        
        # Test keep='longest' strategy
        representatives = choose_representatives(
            clusters=clusters,
            texts=sample_texts,
            keep='longest'
        )
        
        # Should keep the longest text in the cluster (index 4)
        assert 4 in representatives
        assert 0 not in representatives
        assert 3 not in representatives
        assert 7 not in representatives
    
    def test_polars_lsh_deduplication_with_list(self, sample_texts):
        """Test full LSH deduplication with list input."""
        # Test with default parameters
        unique_indices = polars_lsh_deduplication(
            texts=sample_texts,
            threshold=0.7,
            num_minhash_permutations=100,
            num_bands=20,
            show_progress=False
        )
        
        # Should find duplicates and remove them
        assert len(unique_indices) < len(sample_texts)
        
        # Test with different keep strategy
        unique_indices_last = polars_lsh_deduplication(
            texts=sample_texts,
            threshold=0.7,
            keep='last',
            show_progress=False
        )
        
        # Should have same number of unique texts but different indices
        assert len(unique_indices_last) == len(unique_indices)
        assert unique_indices != unique_indices_last
        
        # Test with return_similarity_dict
        unique_indices, similarity_dict = polars_lsh_deduplication(
            texts=sample_texts,
            return_similarity_dict=True,
            show_progress=False
        )
        
        # Should return similarity dictionary
        assert isinstance(similarity_dict, dict)
        assert len(similarity_dict) > 0
    
    def test_polars_lsh_deduplication_with_pandas(self, sample_dataframe):
        """Test full LSH deduplication with pandas input."""
        # Test with pandas Series
        unique_indices = polars_lsh_deduplication(
            texts=sample_dataframe['text'],
            threshold=0.7,
            show_progress=False
        )
        
        # Should find duplicates and remove them
        assert len(unique_indices) < len(sample_dataframe)
        
        # Result should be a list of indices
        assert isinstance(unique_indices, list)
        assert all(isinstance(idx, int) for idx in unique_indices)
    
    def test_polars_lsh_deduplication_with_polars(self, sample_polars_dataframe):
        """Test full LSH deduplication with polars input."""
        # Test with polars Series
        unique_indices = polars_lsh_deduplication(
            texts=sample_polars_dataframe['text'],
            threshold=0.7,
            show_progress=False
        )
        
        # Should find duplicates and remove them
        assert len(unique_indices) < len(sample_polars_dataframe)
        
        # Result should be a list of indices
        assert isinstance(unique_indices, list)
        assert all(isinstance(idx, int) for idx in unique_indices)
    
    def test_streaming_lsh_deduplication(self, sample_texts):
        """Test streaming LSH deduplication."""
        # Create an iterator that yields batches of texts
        def text_iterator():
            for i in range(0, len(sample_texts), 2):
                yield sample_texts[i:min(i+2, len(sample_texts))]
        
        # Test streaming deduplication
        unique_indices = streaming_lsh_deduplication(
            texts_iterator=text_iterator(),
            threshold=0.7,
            batch_size=2,
            show_progress=False
        )
        
        # Should find duplicates and remove them
        assert len(unique_indices) < len(sample_texts)
        
        # Result should be a list of indices
        assert isinstance(unique_indices, list)
        assert all(isinstance(idx, int) for idx in unique_indices)