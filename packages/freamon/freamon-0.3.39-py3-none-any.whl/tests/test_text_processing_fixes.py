"""
Tests for the text processing fixes, specifically addressing index mismatch errors.
"""
import pandas as pd
import numpy as np
import pytest

from freamon.utils.text_utils import create_topic_model_optimized, TextProcessor


class TestTextProcessingFixes:
    """Test class for text processing fixes addressing index mismatch errors."""
    
    @pytest.fixture
    def sample_texts_with_gaps(self):
        """Create a dataframe with text data and non-contiguous indices."""
        texts = [
            "Machine learning is a field of artificial intelligence.",
            "Natural language processing involves computational linguistics.",
            "Computer vision enables machines to interpret visual information.",
            "Reinforcement learning focuses on decision making processes.",
            "Neural networks are computing systems inspired by biological networks.",
            "Deep learning uses multi-layered neural networks for analysis.",
            "Supervised learning uses labeled datasets for training models.",
            "Unsupervised learning identifies patterns in unlabeled data.",
            "Semi-supervised learning combines labeled and unlabeled data.",
            "Transfer learning applies knowledge from one task to another."
        ]
        
        # Create a dataframe with non-contiguous index
        df = pd.DataFrame({"text": texts})
        
        # Set non-contiguous indices
        df.index = [0, 2, 5, 7, 10, 15, 20, 25, 30, 35]
        
        return df
    
    @pytest.fixture
    def duplicate_texts_df(self):
        """Create a dataframe with duplicate text entries."""
        texts = [
            "Machine learning is a field of artificial intelligence.",
            "Natural language processing involves computational linguistics.",
            "Machine learning is a field of artificial intelligence.",  # Duplicate
            "Computer vision enables machines to interpret visual information.",
            "Reinforcement learning focuses on decision making processes.",
            "Natural language processing involves computational linguistics.",  # Duplicate
            "Deep learning uses multi-layered neural networks for analysis.",
            "Computer vision enables machines to interpret visual information.",  # Duplicate
            "Unsupervised learning identifies patterns in unlabeled data.",
            "Reinforcement learning focuses on decision making processes."  # Duplicate
        ]
        
        # Create a dataframe with standard sequential index
        df = pd.DataFrame({"text": texts})
        
        return df
    
    def test_aligning_document_topics(self, sample_texts_with_gaps):
        """Test that document topics can be aligned with non-contiguous indices."""
        df = sample_texts_with_gaps
        
        # Run topic modeling
        result = create_topic_model_optimized(
            df,
            'text',
            n_topics=2,
            method='nmf',
            preprocessing_options={
                'enabled': True,
                'remove_stopwords': True
            }
        )
        
        # Check that document topic distributions were created successfully
        assert 'document_topics' in result
        assert len(result['document_topics']) == len(df)
        
        # Verify that document topics have the same index as the original dataframe
        assert result['document_topics'].index.equals(df.index)
    
    def test_handling_duplicates(self, duplicate_texts_df):
        """Test that the code can handle datasets with duplicate text entries."""
        df = duplicate_texts_df
        
        # Count original duplicates
        duplicate_count = df['text'].duplicated().sum()
        assert duplicate_count > 0, "Test data should contain duplicates"
        
        # Run topic modeling with deduplication
        result = create_topic_model_optimized(
            df,
            'text',
            n_topics=2,
            method='nmf',
            deduplication_options={
                'enabled': True,
                'method': 'exact'
            },
            preprocessing_options={
                'enabled': True,
                'remove_stopwords': True
            }
        )
        
        # Check that document topics were created successfully
        assert 'document_topics' in result
        assert len(result['document_topics']) == len(df)
        
        # Check processing info includes deduplication info
        assert 'deduplication_method' in result['processing_info']
        assert 'deduplication_mapping_size' in result['processing_info']
        assert result['processing_info']['deduplication_method'] == 'exact'
    
    def test_processing_large_datasets(self):
        """Test that the code can handle large datasets."""
        # Create a dataset of moderate size
        np.random.seed(42)
        texts = []
        for i in range(200):
            words = ["sample", "text", "words", "testing", "data", "machine", "learning"]
            # Create random sentences of 5-10 words
            sentence_len = np.random.randint(5, 10)
            text = " ".join(np.random.choice(words, size=sentence_len))
            texts.append(text)
            
        df = pd.DataFrame({"text": texts})
        
        # Run topic modeling
        result = create_topic_model_optimized(
            df,
            'text',
            n_topics=2,
            method='nmf',
            max_docs=100,  # Limit for performance
            preprocessing_options={
                'enabled': True,
                'remove_stopwords': True
            }
        )
        
        # Check that document topics were created successfully
        assert 'document_topics' in result
        
        # The length of document_topics should match the input dataframe
        # This verifies that topics are generated for all documents
        # even if sampling was used internally
        assert len(result['document_topics']) == len(df)
        
        # Verify some basic info is present in processing_info
        assert len(result['processing_info']) > 0
    
    def test_preprocessing_options(self, sample_texts_with_gaps):
        """Test that all preprocessing options work correctly."""
        df = sample_texts_with_gaps
        
        # Run with comprehensive preprocessing options
        preprocessing_options = {
            'enabled': True,
            'use_lemmatization': True,
            'remove_stopwords': True,
            'remove_punctuation': True,
            'min_token_length': 3,
            'custom_stopwords': ['artificial', 'field']
        }
        
        result = create_topic_model_optimized(
            df,
            'text',
            n_topics=2,
            method='nmf',
            preprocessing_options=preprocessing_options
        )
        
        # Check that preprocessing was performed by looking at relevant keys
        processing_info = result['processing_info']
        # Verify some preprocessing occurred by checking the time
        assert 'preprocessing_time' in processing_info
        assert processing_info['preprocessing_time'] > 0
        
        # Check that topic model was created successfully
        assert 'topic_model' in result
        assert result['topic_model']['n_topics'] == 2
    
    def test_error_handling_with_very_small_corpus(self):
        """Test error handling with a very small corpus that might cause issues."""
        # Create a tiny dataset with meaningful text (not just single words)
        df = pd.DataFrame({
            "text": [
                "Machine learning algorithms are used to analyze data.",
                "Deep learning uses neural networks for complex tasks.",
                "Natural language processing helps computers understand human language."
            ]
        })
        
        # This should not raise exceptions even with such a small corpus
        result = create_topic_model_optimized(
            df,
            'text',
            n_topics=2,  # More topics than might be reasonable for 3 documents
            method='nmf',
            preprocessing_options={
                'enabled': True,
                'remove_stopwords': True
            }
        )
        
        # Check if the function gracefully handled the small corpus
        assert 'topic_model' in result
        assert 'document_topics' in result
        assert 'processing_info' in result