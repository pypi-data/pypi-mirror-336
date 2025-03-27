"""
Unit tests for parameter handling in topic modeling functions.

These tests verify that:
- Unsupported parameters are properly filtered out
- create_topic_model_optimized handles sampling_ratio parameter correctly
- create_topic_model_optimized_from_matrix handles parameters properly
"""
import pytest
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from freamon.utils.text_utils import (
    create_topic_model_optimized,
    create_topic_model_optimized_from_matrix
)

class TestTopicModelingParameters:
    """Tests for topic modeling parameter handling."""
    
    def setup_method(self):
        """Set up test data."""
        self.text_data = pd.Series([
            "machine learning algorithms help computers learn from data",
            "neural networks are inspired by human brain structure",
            "deep learning models can recognize patterns in data",
            "reinforcement learning trains agents through rewards",
            "natural language processing helps computers understand text",
            "computer vision allows machines to interpret visual information",
            "unsupervised learning finds patterns without labeled data",
            "supervised learning uses labeled examples to train models",
            "decision trees split data based on feature values",
            "random forests combine multiple decision trees"
        ])
    
    def test_unsupported_parameters_filtering(self):
        """Test that unsupported parameters are filtered out."""
        # Try with an unsupported parameter (sampling_ratio)
        result = create_topic_model_optimized(
            self.text_data,
            n_topics=2,  # Small for test speed
            sampling_ratio=0.5,  # This should be filtered out without error
            random_state=42
        )
        
        # Check that the result contains expected fields
        assert 'topic_model' in result
        assert 'document_topics' in result
        assert 'feature_names' in result
        assert 'topic_terms' in result
        
        # Check shape of document topics
        assert result['document_topics'].shape[0] == len(self.text_data)
        assert result['document_topics'].shape[1] == 2  # 2 topics
    
    def test_create_topic_model_from_matrix(self):
        """Test that create_topic_model_optimized_from_matrix handles parameters correctly."""
        # Create TF-IDF matrix directly
        vectorizer = TfidfVectorizer(
            min_df=1, 
            max_df=0.9,
            stop_words='english'
        )
        tfidf_matrix = vectorizer.fit_transform(self.text_data)
        feature_names = vectorizer.get_feature_names_out()
        
        # Try with mixed supported and unsupported parameters
        result = create_topic_model_optimized_from_matrix(
            tfidf_matrix=tfidf_matrix,
            feature_names=feature_names,
            n_topics=2,  # Small for test speed
            sampling_ratio=0.5,  # This should be filtered out
            init='random',  # Supported
            alpha=0.1,  # Supported
            random_state=42
        )
        
        # Check that the result contains expected fields
        assert 'topic_model' in result
        assert 'document_topics' in result
        assert 'feature_names' in result
        assert 'topic_terms' in result
        
        # Check shape of document topics
        assert result['document_topics'].shape[0] == tfidf_matrix.shape[0]
        assert result['document_topics'].shape[1] == 2  # 2 topics
    
    def test_fallback_on_error(self):
        """Test that topic modeling falls back to simpler parameters on error."""
        # Create a dataset that might cause issues
        problematic_data = pd.Series([
            "very short text",
            "",  # Empty string
            "another short text",
            " ",  # Just whitespace
            "final text example"
        ])
        
        # Should not raise exception despite problematic input
        result = create_topic_model_optimized(
            problematic_data,
            n_topics=2,
            random_state=42
        )
        
        # Check that the result contains expected fields
        assert 'topic_model' in result
        assert 'document_topics' in result
        assert 'feature_names' in result
        assert 'topic_terms' in result