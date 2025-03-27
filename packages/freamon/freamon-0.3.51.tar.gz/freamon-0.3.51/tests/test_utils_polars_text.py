"""
Tests for Polars optimizations in text utilities.
"""
import pytest
import pandas as pd
import numpy as np
import polars as pl
from typing import List

from freamon.utils.text_utils import TextProcessor
from freamon.utils.dataframe_utils import check_dataframe_type, convert_dataframe


class TestPolarsTextUtils:
    """Test class for Polars-optimized text utilities."""
    
    @pytest.fixture
    def sample_texts(self) -> List[str]:
        """Create sample texts for testing."""
        return [
            "This is a test document for text processing",
            "A different document with unique content",
            "Another unique document for testing",
            "This is a test document for text processing",  # Exact duplicate of first
            "This is a test document for text processing with slight change",  # Near duplicate
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
                "This is a test document for text processing",
                "A different document with unique content",
                "Another unique document for testing",
                "This is a test document for text processing",  # Exact duplicate of first
                "This is a test document for text processing with slight change",  # Near duplicate
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
    
    def test_dataframe_type_detection(self, sample_dataframe, sample_polars_dataframe):
        """Test detection of dataframe types."""
        # Test pandas detection
        assert check_dataframe_type(sample_dataframe) == "pandas"
        
        # Test polars detection
        assert check_dataframe_type(sample_polars_dataframe) == "polars"
        
        # Test other objects
        assert check_dataframe_type("not a dataframe") == "unknown"
    
    def test_dataframe_conversion(self, sample_dataframe, sample_polars_dataframe):
        """Test conversion between dataframe types."""
        # Convert pandas to polars
        converted_to_polars = convert_dataframe(sample_dataframe, "polars")
        assert check_dataframe_type(converted_to_polars) == "polars"
        assert len(converted_to_polars) == len(sample_dataframe)
        
        # Convert polars to pandas
        converted_to_pandas = convert_dataframe(sample_polars_dataframe, "pandas")
        assert check_dataframe_type(converted_to_pandas) == "pandas"
        assert len(converted_to_pandas) == len(sample_polars_dataframe)
        
        # Convert to same type (no-op)
        same_type = convert_dataframe(sample_dataframe, "pandas")
        assert same_type is sample_dataframe
    
    def test_text_processor_with_polars(self, sample_polars_dataframe, text_processor):
        """Test text processor with Polars dataframes."""
        # Convert Polars to pandas for processing
        df_pandas = convert_dataframe(sample_polars_dataframe, "pandas")
        
        # Process text column
        processed_texts = []
        for text in df_pandas['text']:
            processed_texts.append(text_processor.preprocess_text(
                text,
                lowercase=True,
                remove_punctuation=True,
                remove_stopwords=True
            ))
        
        # Check that we get expected number of processed texts
        assert len(processed_texts) == len(sample_polars_dataframe)
        
        # Check that preprocessing had the expected effect
        assert all(t.islower() for t in processed_texts if t)
    
    def test_batch_text_processing_with_polars(self, sample_polars_dataframe, text_processor):
        """Test batch processing of text with Polars."""
        # Get the text column from Polars DataFrame
        texts = sample_polars_dataframe['text'].to_list()
        
        # Define a batch processor function
        def process_batch(batch_texts, processor=text_processor):
            return [
                processor.preprocess_text(
                    text,
                    lowercase=True,
                    remove_punctuation=True,
                    remove_stopwords=True
                ) 
                for text in batch_texts
            ]
        
        # Process in a batch
        batch_size = 3
        all_processed = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:min(i+batch_size, len(texts))]
            processed_batch = process_batch(batch)
            all_processed.extend(processed_batch)
        
        # Check that we processed all texts
        assert len(all_processed) == len(texts)
        
        # Check that preprocessing had the expected effect
        assert all(t.islower() for t in all_processed if t)
    
    def test_text_vectorization_with_polars(self, sample_polars_dataframe):
        """Test text vectorization with Polars."""
        from sklearn.feature_extraction.text import CountVectorizer
        
        # Get text column from Polars DataFrame
        texts = sample_polars_dataframe['text'].to_list()
        
        # Vectorize the texts
        vectorizer = CountVectorizer(max_features=100)
        vectors = vectorizer.fit_transform(texts)
        
        # Check that we get expected shape
        assert vectors.shape[0] == len(texts)
        assert vectors.shape[1] <= 100
    
    def test_text_similarity_with_polars(self, sample_polars_dataframe, text_processor):
        """Test text similarity calculation with Polars."""
        # Get text column from Polars DataFrame
        texts = sample_polars_dataframe['text'].to_list()
        
        # Calculate similarity between first and each document
        reference = texts[0]
        similarities = []
        
        for text in texts:
            similarity = text_processor.calculate_document_similarity(
                reference, text, method='cosine'
            )
            similarities.append(similarity)
        
        # Check that identical documents have similarity 1.0
        assert similarities[0] == 1.0  # Self-similarity
        assert similarities[3] == 1.0  # Exact duplicate
        
        # Similar documents should have high but not perfect similarity
        assert 0.5 < similarities[4] < 1.0
        assert 0.5 < similarities[7] < 1.0
        
        # Different documents should have lower similarity
        assert similarities[1] < 0.5
        assert similarities[2] < 0.5
        assert similarities[5] < 0.5
        assert similarities[6] < 0.5