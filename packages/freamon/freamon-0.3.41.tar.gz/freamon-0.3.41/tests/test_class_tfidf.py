"""
Tests for Class-based TF-IDF implementation in text_utils.py.
"""
import pytest
import pandas as pd
import numpy as np
from freamon.utils.text_utils import TextProcessor

class TestClassTFIDF:
    """Test the class-based TF-IDF implementation."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        return pd.DataFrame({
            'text': [
                'Document about sports and games',
                'Another sports document with details about athletes',
                'Financial report with economic data',
                'Banking information and financial metrics'
            ],
            'category': ['Sports', 'Sports', 'Finance', 'Finance']
        })
    
    @pytest.fixture
    def processor(self):
        """Create a TextProcessor instance."""
        return TextProcessor(use_spacy=False)
    
    def test_create_class_tfidf_model(self, sample_data, processor):
        """Test creation of class-based TF-IDF model."""
        model = processor.create_class_tfidf_model(
            df=sample_data,
            text_column='text',
            class_column='category'
        )
        
        # Check model structure
        assert 'vectorizer' in model
        assert 'class_tfidf_matrix' in model
        assert 'feature_names' in model
        assert 'class_labels' in model
        assert 'top_terms_per_class' in model
        assert 'class_sizes' in model
        
        # Check class labels
        assert set(model['class_labels']) == {'Sports', 'Finance'}
        
        # Check class sizes
        assert model['class_sizes'] == {'Sports': 2, 'Finance': 2}
        
        # Check feature names are strings
        assert all(isinstance(name, str) for name in model['feature_names'])
        
        # Check top terms
        assert 'Sports' in model['top_terms_per_class']
        assert 'Finance' in model['top_terms_per_class']
        
        # Check top terms format
        for class_label, terms in model['top_terms_per_class'].items():
            assert isinstance(terms, list)
            for term in terms:
                assert isinstance(term, tuple)
                assert isinstance(term[0], str)  # term name
                assert isinstance(term[1], (float, np.float64))  # term score
    
    def test_classify_with_ctfidf(self, sample_data, processor):
        """Test document classification using class-based TF-IDF."""
        # Create model
        model = processor.create_class_tfidf_model(
            df=sample_data,
            text_column='text',
            class_column='category'
        )
        
        # Test texts to classify
        test_texts = [
            'A document about football and athletics',
            'Economic indicators and banking sector analysis'
        ]
        
        # Test classification
        predictions = processor.classify_with_ctfidf(
            model=model,
            texts=test_texts
        )
        
        # Check predictions
        assert len(predictions) == 2
        assert predictions[0] == 'Sports'
        assert predictions[1] == 'Finance'
        
        # Test with return_scores=True
        scores = processor.classify_with_ctfidf(
            model=model,
            texts=test_texts,
            return_scores=True
        )
        
        # Check scores
        assert isinstance(scores, pd.DataFrame)
        assert scores.shape == (2, 2)
        assert list(scores.columns) == ['Sports', 'Finance']
        
        # Verify first text has higher score for Sports
        assert scores.iloc[0]['Sports'] > scores.iloc[0]['Finance']
        
        # Verify second text has higher score for Finance
        assert scores.iloc[1]['Finance'] > scores.iloc[1]['Sports']
    
    def test_class_tfidf_normalization(self, processor):
        """Test that class-based TF-IDF properly normalizes by class size."""
        # Create imbalanced dataset
        imbalanced_data = pd.DataFrame({
            'text': [
                'Sports document 1',
                'Sports document 2',
                'Sports document 3',
                'Sports document 4',
                'Sports document 5',
                'Finance document 1',
                'Finance document 2'
            ],
            'category': ['Sports', 'Sports', 'Sports', 'Sports', 'Sports', 'Finance', 'Finance']
        })
        
        # Create model
        model = processor.create_class_tfidf_model(
            df=imbalanced_data,
            text_column='text',
            class_column='category'
        )
        
        # Verify class sizes
        assert model['class_sizes'] == {'Sports': 5, 'Finance': 2}
        
        # Test classification on ambiguous text
        test_text = ['Document with both sports and finance']
        
        # Get scores
        scores = processor.classify_with_ctfidf(
            model=model,
            texts=test_text,
            return_scores=True
        )
        
        # Without normalization, the Sports class would dominate due to more documents
        # With proper normalization, scores should be more balanced
        sports_score = scores.iloc[0]['Sports']
        finance_score = scores.iloc[0]['Finance']
        
        # Check that scores sum close to 1
        assert abs(sports_score + finance_score - 1.0) < 1e-6
        
        # The specific outcome depends on the vectorization and normalization details,
        # but we want to ensure the minority class (Finance) isn't completely overwhelmed
        assert finance_score > 0.2