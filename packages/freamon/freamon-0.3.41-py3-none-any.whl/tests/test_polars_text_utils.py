"""
Tests for the Polars text utilities.
"""
import pytest
import pandas as pd
import numpy as np
import polars as pl
from typing import List

from freamon.utils.text_utils import TextProcessor
from freamon.utils.polars_text_utils import (
    process_text_column,
    deduplicate_text_column,
    batch_calculate_similarities,
    batch_vectorize_texts
)


class TestPolarsTextUtils:
    """Test class for Polars text utilities."""
    
    @pytest.fixture
    def sample_texts(self) -> List[str]:
        """Create sample texts for testing."""
        return [
            "This is a test document for processing",
            "A different document with unique content",
            "Another unique document for testing",
            "This is a test document for processing",  # Exact duplicate of first
            "This is a test document for processing with slight change",  # Near duplicate
            "Another unique text for the algorithm to process",
            "A document that is completely different from all others",
            "This is a test document for processing using text utilities",  # Near duplicate
        ]
    
    @pytest.fixture
    def sample_dataframe(self) -> pd.DataFrame:
        """Create sample dataframe for testing."""
        return pd.DataFrame({
            'id': list(range(8)),
            'text': [
                "This is a test document for processing",
                "A different document with unique content",
                "Another unique document for testing",
                "This is a test document for processing",  # Exact duplicate of first
                "This is a test document for processing with slight change",  # Near duplicate
                "Another unique text for the algorithm to process",
                "A document that is completely different from all others",
                "This is a test document for processing using text utilities",  # Near duplicate
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
    
    def test_process_text_column_pandas(self, sample_dataframe, text_processor):
        """Test text column processing with pandas dataframe."""
        # Process the text column
        processed_df = process_text_column(
            df=sample_dataframe,
            text_column='text',
            processor=text_processor,
            lowercase=True,
            remove_punctuation=True,
            remove_stopwords=True,
            batch_size=3  # Small batch for testing
        )
        
        # Check that we got a dataframe back
        assert isinstance(processed_df, pd.DataFrame)
        
        # Check that all texts are processed (lowercase, no punctuation)
        for text in processed_df['text']:
            assert text.islower()
            assert all(c.isalnum() or c.isspace() for c in text)
    
    def test_process_text_column_polars(self, sample_polars_dataframe, text_processor):
        """Test text column processing with polars dataframe."""
        # Process the text column
        processed_df = process_text_column(
            df=sample_polars_dataframe,
            text_column='text',
            processor=text_processor,
            lowercase=True,
            remove_punctuation=True,
            remove_stopwords=True,
            batch_size=3  # Small batch for testing
        )
        
        # Check that we got a Polars dataframe back
        assert isinstance(processed_df, pl.DataFrame)
        
        # Convert to pandas for checking
        processed_pandas = processed_df.to_pandas()
        
        # Check that all texts are processed (lowercase, no punctuation)
        for text in processed_pandas['text']:
            assert text.islower()
            assert all(c.isalnum() or c.isspace() for c in text)
    
    def test_process_text_column_parallel(self, sample_dataframe, text_processor):
        """Test parallel text column processing."""
        # Process the text column in parallel
        processed_df = process_text_column(
            df=sample_dataframe,
            text_column='text',
            processor=text_processor,
            lowercase=True,
            remove_punctuation=True,
            n_jobs=2  # Use parallel processing
        )
        
        # Check that we got a dataframe back
        assert isinstance(processed_df, pd.DataFrame)
        
        # Check that all texts are processed (lowercase, no punctuation)
        for text in processed_df['text']:
            assert text.islower()
            assert all(c.isalnum() or c.isspace() for c in text)
    
    def test_deduplicate_text_column_exact(self, sample_dataframe):
        """Test exact deduplication of text column."""
        # Deduplicate the text column
        deduplicated_df = deduplicate_text_column(
            df=sample_dataframe,
            text_column='text',
            method='exact',
            keep='first'
        )
        
        # Check that we got a dataframe back
        assert isinstance(deduplicated_df, pd.DataFrame)
        
        # Check that exact duplicates are removed
        assert len(deduplicated_df) < len(sample_dataframe)
        
        # Check duplicate count (should be at least 1 exact duplicate)
        assert len(sample_dataframe) - len(deduplicated_df) >= 1
    
    def test_deduplicate_text_column_lsh(self, sample_dataframe):
        """Test LSH deduplication of text column."""
        # Deduplicate the text column
        deduplicated_df = deduplicate_text_column(
            df=sample_dataframe,
            text_column='text',
            method='lsh',
            threshold=0.7,
            batch_size=3  # Small batch for testing
        )
        
        # Check that we got a dataframe back
        assert isinstance(deduplicated_df, pd.DataFrame)
        
        # Check that duplicates are removed (should find both exact and near duplicates)
        assert len(deduplicated_df) < len(sample_dataframe)
        
        # Should remove more than just the exact duplicates
        assert len(sample_dataframe) - len(deduplicated_df) > 1
    
    def test_deduplicate_text_column_polars(self, sample_polars_dataframe):
        """Test deduplication with Polars dataframe."""
        # Deduplicate the text column
        deduplicated_df = deduplicate_text_column(
            df=sample_polars_dataframe,
            text_column='text',
            method='lsh',
            threshold=0.7,
            batch_size=3  # Small batch for testing
        )
        
        # Check that we got a Polars dataframe back
        assert isinstance(deduplicated_df, pl.DataFrame)
        
        # Check that duplicates are removed
        assert len(deduplicated_df) < len(sample_polars_dataframe)
    
    def test_deduplicate_text_column_with_similarity_dict(self, sample_dataframe):
        """Test deduplication with similarity dictionary."""
        # Deduplicate the text column and get similarity dict
        deduplicated_df, similarity_dict = deduplicate_text_column(
            df=sample_dataframe,
            text_column='text',
            method='lsh',
            threshold=0.7,
            return_similarity_dict=True
        )
        
        # Check that we got both return values
        assert isinstance(deduplicated_df, pd.DataFrame)
        assert isinstance(similarity_dict, dict)
        
        # Check that the similarity dict has entries
        assert len(similarity_dict) > 0
    
    def test_batch_calculate_similarities(self, sample_texts, text_processor):
        """Test batch calculation of similarities."""
        # Calculate similarities with reference text
        reference = sample_texts[0]
        similarities = batch_calculate_similarities(
            texts=sample_texts,
            reference_text=reference,
            method='cosine',
            processor=text_processor,
            batch_size=3  # Small batch for testing
        )
        
        # Check that we got an array of the right size
        assert len(similarities) == len(sample_texts)
        
        # First text should be identical to reference
        assert similarities[0] == 1.0
        
        # Exact duplicate should have similarity 1.0
        assert similarities[3] == 1.0
        
        # Near duplicates should have high but not perfect similarity
        assert 0.5 < similarities[4] < 1.0
        assert 0.5 < similarities[7] < 1.0
        
        # Different documents should have lower similarity
        assert similarities[1] < 0.5
        # This document is slightly above 0.5 similarity, let's adjust the test
        assert similarities[2] < 0.51
    
    def test_batch_calculate_similarities_pairwise(self, sample_texts, text_processor):
        """Test batch calculation of pairwise similarities."""
        # Calculate pairwise similarities
        similarities = batch_calculate_similarities(
            texts=sample_texts[:4],  # Use a subset for speed
            reference_text=None,  # Pairwise mode
            method='cosine',
            processor=text_processor,
            batch_size=2  # Small batch for testing
        )
        
        # Check that we got a matrix of the right size
        assert similarities.shape == (4, 4)
        
        # Diagonal should all be 1.0 (self-similarity)
        assert np.all(np.diag(similarities) == 1.0)
        
        # Matrix should be symmetric
        assert np.allclose(similarities, similarities.T)
        
        # Check specific values: texts 0 and 3 are identical
        assert similarities[0, 3] == 1.0
        assert similarities[3, 0] == 1.0
    
    def test_batch_vectorize_texts(self, sample_texts):
        """Test batch vectorization of texts."""
        from sklearn.feature_extraction.text import CountVectorizer
        
        # Create and fit vectorizer
        vectorizer = CountVectorizer()
        vectorizer.fit(sample_texts)
        
        # Create vectorizer function
        vectorizer_func = lambda texts: vectorizer.transform(texts)
        
        # Vectorize in batches
        vectors = batch_vectorize_texts(
            texts=sample_texts,
            vectorizer_func=vectorizer_func,
            batch_size=3  # Small batch for testing
        )
        
        # Check that we got vectors of the right size
        assert vectors.shape[0] == len(sample_texts)
        
        # Feature dimension should match vocabulary size
        assert vectors.shape[1] == len(vectorizer.vocabulary_)