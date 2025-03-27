"""
Unit tests for error recovery and fallback mechanisms in topic modeling.

These tests verify that the topic modeling functionality can recover from various error
conditions and apply appropriate fallback strategies.
"""
import pandas as pd
import numpy as np
import pytest
from scipy.sparse import csr_matrix

from freamon.modeling.autoflow import auto_model, AutoModelFlow
from freamon.utils.text_utils import create_topic_model_optimized, create_topic_model_optimized_from_matrix

class TestTopicModelingRecovery:
    """Tests for error recovery mechanisms in topic modeling."""
    
    def setup_method(self):
        """Set up test data including various challenging text datasets."""
        np.random.seed(42)
        
        # Standard text dataset
        standard_texts = [
            "This is a sample text document for testing",
            "Another document with different words",
            "Text analytics can be used for many applications",
            "Machine learning models need good text features",
            "Topic modeling helps find patterns in text data",
            "Vectors represent documents in semantic space",
            "Word embeddings capture semantic relationships",
            "Different dimensions represent different topics",
            "Natural language processing uses text data",
            "Document clustering groups similar texts together"
        ]
        
        self.df_standard = pd.DataFrame({
            'feature_0': np.random.randn(10),
            'text_column': standard_texts,
            'target': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
        })
        
        # Very short texts (challenging for vectorization)
        short_texts = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
        self.df_short = pd.DataFrame({
            'feature_0': np.random.randn(10),
            'text_column': short_texts,
            'target': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
        })
        
        # Empty texts (should trigger fallbacks)
        empty_texts = ["", "", "", "", "", "", "", "", "", ""]
        self.df_empty = pd.DataFrame({
            'feature_0': np.random.randn(10),
            'text_column': empty_texts,
            'target': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
        })
        
        # Duplicate texts (challenging for topic diversity)
        duplicate_texts = ["same text"] * 10
        self.df_duplicate = pd.DataFrame({
            'feature_0': np.random.randn(10),
            'text_column': duplicate_texts,
            'target': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
        })
        
        # Mixed texts with some normal and some problematic
        mixed_texts = standard_texts[:5] + empty_texts[:5]
        self.df_mixed = pd.DataFrame({
            'feature_0': np.random.randn(10),
            'text_column': mixed_texts,
            'target': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
        })
        
        # Multiple text columns
        self.df_multi_text = pd.DataFrame({
            'feature_0': np.random.randn(10),
            'text_column1': standard_texts,
            'text_column2': [t.upper() for t in standard_texts],
            'target': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
        })
    
    def test_standard_text_processing(self):
        """Test topic modeling with standard text data."""
        results = auto_model(
            df=self.df_standard,
            target_column='target',
            model_type='lgbm_classifier',
            problem_type='classification',
            cv_folds=2,
            test_size=0.2,
            auto_split=True,
            random_state=42,
            tuning=False,
            text_columns=['text_column'],
            text_options={
                'n_topics': 2,
                'min_df': 1,
                'max_df': 0.9
            }
        )
        
        # Verify text features were created
        assert 'autoflow' in results
        feature_cols = results['autoflow'].feature_columns
        assert any('topic' in col for col in feature_cols)
    
    def test_short_text_recovery(self):
        """Test recovery with very short texts."""
        results = auto_model(
            df=self.df_short,
            target_column='target',
            model_type='lgbm_classifier',
            problem_type='classification',
            cv_folds=2,
            test_size=0.2,
            auto_split=True,
            random_state=42,
            tuning=False,
            text_columns=['text_column'],
            text_options={
                'n_topics': 2,
                'min_df': 1,
                'max_df': 0.9
            }
        )
        
        # Verify the model was created despite challenging text
        assert 'model' in results
        assert 'test_metrics' in results
    
    def test_empty_text_recovery(self):
        """Test recovery with empty texts."""
        results = auto_model(
            df=self.df_empty,
            target_column='target',
            model_type='lgbm_classifier',
            problem_type='classification',
            cv_folds=2,
            test_size=0.2,
            auto_split=True,
            random_state=42,
            tuning=False,
            text_columns=['text_column'],
            text_options={
                'n_topics': 2,
                'min_df': 1,
                'max_df': 0.9
            }
        )
        
        # Verify the model was created despite empty text
        assert 'model' in results
        assert 'test_metrics' in results
    
    def test_duplicate_text_recovery(self):
        """Test recovery with duplicate texts."""
        results = auto_model(
            df=self.df_duplicate,
            target_column='target',
            model_type='lgbm_classifier',
            problem_type='classification',
            cv_folds=2,
            test_size=0.2,
            auto_split=True,
            random_state=42,
            tuning=False,
            text_columns=['text_column'],
            text_options={
                'n_topics': 2,
                'min_df': 1,
                'max_df': 0.9
            }
        )
        
        # Verify the model was created despite duplicate text
        assert 'model' in results
        assert 'test_metrics' in results
    
    def test_mixed_text_recovery(self):
        """Test recovery with mixed normal and problematic texts."""
        results = auto_model(
            df=self.df_mixed,
            target_column='target',
            model_type='lgbm_classifier',
            problem_type='classification',
            cv_folds=2,
            test_size=0.2,
            auto_split=True,
            random_state=42,
            tuning=False,
            text_columns=['text_column'],
            text_options={
                'n_topics': 2,
                'min_df': 1,
                'max_df': 0.9
            }
        )
        
        # Verify the model was created despite mixed text quality
        assert 'model' in results
        assert 'test_metrics' in results
    
    def test_multiple_text_columns(self):
        """Test processing multiple text columns."""
        results = auto_model(
            df=self.df_multi_text,
            target_column='target',
            model_type='lgbm_classifier',
            problem_type='classification',
            cv_folds=2,
            test_size=0.2,
            auto_split=True,
            random_state=42,
            tuning=False,
            text_columns=['text_column1', 'text_column2'],
            text_options={
                'n_topics': 2,
                'min_df': 1,
                'max_df': 0.9
            }
        )
        
        # Verify text features were created for both columns
        assert 'autoflow' in results
        feature_cols = results['autoflow'].feature_columns
        assert any('text_column1_topic' in col for col in feature_cols)
        assert any('text_column2_topic' in col for col in feature_cols)
    
    def test_direct_topic_model_fallbacks(self):
        """Test direct fallback mechanisms in create_topic_model_optimized_from_matrix."""
        from sklearn.feature_extraction.text import TfidfVectorizer
        
        # Test with empty TF-IDF matrix (should trigger fallbacks)
        empty_matrix = csr_matrix((10, 1))
        feature_names = ['feature']
        
        # This should not raise exceptions due to fallbacks
        topics_df, topic_terms, doc_topics = create_topic_model_optimized_from_matrix(
            tfidf_matrix=empty_matrix,
            feature_names=feature_names,
            n_topics=2,
            random_state=42
        )
        
        # Check that fallback created reasonable outputs
        assert isinstance(topics_df, pd.DataFrame)
        assert doc_topics.shape[0] == empty_matrix.shape[0]
        
    def test_text_options_filtering(self):
        """Test the filtering of text options parameters."""
        # Create a simplified test of text options filtering logic
        
        # Standard case - valid parameters only
        standard_options = {
            'n_topics': 2,
            'min_df': 1,
            'max_df': 0.9
        }
        
        supported_options = {'n_topics', 'min_df', 'max_df', 'method'}
        
        filtered_standard = {k: v for k, v in standard_options.items() 
                            if k in supported_options}
        
        assert filtered_standard == standard_options
        
        # Case with invalid parameters
        invalid_options = {
            'n_topics': 2,
            'invalid_param': 'value',
            'sampling_ratio': 0.8,  # Should be filtered
            'min_df': 1
        }
        
        filtered_invalid = {k: v for k, v in invalid_options.items() 
                           if k in supported_options}
        
        assert 'invalid_param' not in filtered_invalid
        assert 'sampling_ratio' not in filtered_invalid
        assert 'n_topics' in filtered_invalid
        assert 'min_df' in filtered_invalid