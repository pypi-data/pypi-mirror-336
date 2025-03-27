"""
Tests for the supervised deduplication module.
"""
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from freamon.deduplication.supervised_deduplication import SupervisedDeduplicationModel


class TestSupervisedDeduplication:
    """Test class for supervised deduplication functionality."""
    
    @pytest.fixture
    def sample_data(self):
        """Create a sample dataset with known duplicates for testing."""
        np.random.seed(42)
        
        # Create base dataframe
        df = pd.DataFrame({
            'id': [f"ID_{i:06d}" for i in range(50)],
            'name': [f"Customer {i}" for i in range(50)],
            'email': [f"customer{i}@example.com" for i in range(50)],
            'amount': np.random.uniform(10, 1000, 50).round(2),
            'date': [(datetime.now() - timedelta(days=np.random.randint(1, 30))) for _ in range(50)],
            'category': np.random.choice(['A', 'B', 'C'], 50),
        })
        
        # Create duplicates
        duplicates = []
        duplicate_pairs = []
        
        # Create 10 duplicates with slight modifications
        for i in range(10):
            idx = np.random.randint(0, 50)
            original = df.iloc[idx].copy()
            
            duplicate = original.copy()
            # Modify some fields
            if i % 3 == 0:
                duplicate['name'] = duplicate['name'] + ' Jr'
            if i % 2 == 0:
                duplicate['amount'] = round(duplicate['amount'] * 1.05, 2)
            
            duplicates.append(duplicate)
            duplicate_pairs.append((idx, 50 + i))
        
        # Combine original dataframe and duplicates
        full_df = pd.concat([df, pd.DataFrame(duplicates)], ignore_index=True)
        
        return full_df, duplicate_pairs
    
    def test_init(self):
        """Test initialization of the model."""
        model = SupervisedDeduplicationModel(
            model_type='lightgbm',
            date_features=['date'],
            key_features=['name', 'email']
        )
        
        assert model.model_type == 'lightgbm'
        assert model.date_features == ['date']
        assert model.key_features == ['name', 'email']
        assert model.model is None
        assert not model.trained
    
    def test_fit_and_predict(self, sample_data):
        """Test fitting the model and making predictions."""
        df, duplicate_pairs = sample_data
        
        # Split into train and test sets
        train_size = 40
        test_size = len(df) - train_size
        
        train_df = df.iloc[:train_size].copy().reset_index(drop=True)
        test_df = df.iloc[train_size:].copy().reset_index(drop=True)
        
        # Adjust duplicate pairs for train set
        train_duplicate_pairs = []
        for i, j in duplicate_pairs:
            if i < train_size and j < train_size:
                train_duplicate_pairs.append((i, j))
        
        # Initialize and train model
        model = SupervisedDeduplicationModel(
            model_type='lightgbm',
            date_features=['date'],
            key_features=['name', 'email', 'amount', 'category']
        )
        
        # Should have no duplicates at this point
        assert len(train_duplicate_pairs) == 0
        
        # Create some synthetic duplicate pairs for training
        train_duplicate_pairs = []
        for i in range(5):
            # Create duplicated records with modifications
            idx = i
            dup_idx = i + 20
            
            # Manually modify a record to be similar to another
            train_df.loc[dup_idx, 'name'] = train_df.loc[idx, 'name'] + ' Jr'
            train_df.loc[dup_idx, 'email'] = train_df.loc[idx, 'email']
            
            train_duplicate_pairs.append((idx, dup_idx))
        
        # Train the model
        model.fit(train_df, train_duplicate_pairs)
        
        # Model should be trained now
        assert model.trained
        assert model.model is not None
        
        # Test prediction on same data
        predictions = model.predict_duplicate_probability(df=train_df)
        
        # Should return a dataframe with probabilities
        assert isinstance(predictions, pd.DataFrame)
        assert 'duplicate_probability' in predictions.columns
        assert 'idx1' in predictions.columns
        assert 'idx2' in predictions.columns
        
        # Find duplicates
        detected_duplicates = model.find_duplicates(
            train_df, 
            threshold=0.5,
            return_probabilities=False
        )
        
        # Should find some duplicates
        assert isinstance(detected_duplicates, list)
        assert all(isinstance(pair, tuple) for pair in detected_duplicates)
    
    def test_feature_generation(self, sample_data):
        """Test feature generation for record pairs."""
        df, _ = sample_data
        
        model = SupervisedDeduplicationModel(
            model_type='random_forest',
            date_features=['date'],
            key_features=['name', 'email', 'amount', 'category']
        )
        
        # Create two small test dataframes
        df1 = df.iloc[[0, 1, 2]].copy()
        df2 = df.iloc[[3, 4, 5]].copy()
        
        # Generate features
        features = model._generate_pair_features(df1, df2)
        
        # Should have generated features for each key feature
        assert 'name_text_sim' in features.columns
        assert 'email_text_sim' in features.columns
        assert 'amount_abs_diff' in features.columns
        assert 'category_exact_match' in features.columns
        
        # Should have generated features for date
        assert 'date_days_diff' in features.columns
        
        # Check shapes
        assert len(features) == 3  # 3 pairs
    
    def test_training_pair_creation(self, sample_data):
        """Test creation of training pairs."""
        df, duplicate_pairs = sample_data
        
        model = SupervisedDeduplicationModel(
            model_type='gradient_boosting',
            key_features=['name', 'email']
        )
        
        # Create training pairs
        df1, df2, labels = model._create_training_pairs(df, duplicate_pairs[:5])
        
        # Verify sizes
        assert len(df1) > 5  # Should have positive and negative examples
        assert len(df1) == len(df2)
        assert len(df1) == len(labels)
        
        # Verify label distribution
        assert (labels == 1).sum() == 5  # 5 positive examples
        assert (labels == 0).sum() > 0  # Some negative examples
    
    def test_model_evaluation(self, sample_data):
        """Test model evaluation metrics."""
        df, duplicate_pairs = sample_data
        
        # Create more synthetic duplicates for testing
        for i in range(5):
            idx = i
            dup_idx = i + 25
            
            # Make records more similar
            df.loc[dup_idx, 'name'] = df.loc[idx, 'name']
            df.loc[dup_idx, 'email'] = df.loc[idx, 'email']
            
            duplicate_pairs.append((idx, dup_idx))
        
        # Train model on part of the data
        train_size = 40
        train_df = df.iloc[:train_size].copy().reset_index(drop=True)
        test_df = df.iloc[train_size:].copy().reset_index(drop=True)
        
        # Adjust duplicate pairs for train/test
        train_pairs = []
        for i, j in duplicate_pairs:
            if i < train_size and j < train_size:
                train_pairs.append((i, j))
        
        test_pairs = []
        for i, j in duplicate_pairs:
            if i >= train_size and j >= train_size:
                test_pairs.append((i-train_size, j-train_size))
        
        # Initialize and train model
        model = SupervisedDeduplicationModel(
            model_type='lightgbm',
            key_features=['name', 'email', 'amount', 'category']
        )
        
        # Need to create some synthetic pairs if we don't have any
        if len(train_pairs) == 0:
            for i in range(3):
                idx1 = i
                idx2 = i + 10
                train_df.loc[idx2, 'name'] = train_df.loc[idx1, 'name']
                train_df.loc[idx2, 'email'] = train_df.loc[idx1, 'email']
                train_pairs.append((idx1, idx2))
        
        if len(test_pairs) == 0:
            for i in range(2):
                idx1 = i
                idx2 = i + 5
                test_df.loc[idx2, 'name'] = test_df.loc[idx1, 'name']
                test_df.loc[idx2, 'email'] = test_df.loc[idx1, 'email']
                test_pairs.append((idx1, idx2))
        
        model.fit(train_df, train_pairs)
        
        # Evaluate model
        metrics = model.evaluate(test_df, test_pairs)
        
        # Check that we have all expected metrics
        assert 'precision' in metrics
        assert 'recall' in metrics
        assert 'f1' in metrics
        assert 'auc' in metrics
        
        # Metrics should be between 0 and 1
        for metric, value in metrics.items():
            assert 0 <= value <= 1
    
    def test_feature_importances(self, sample_data):
        """Test getting feature importances."""
        df, duplicate_pairs = sample_data
        
        # Create synthetic duplicates for training
        for i in range(5):
            idx = i
            dup_idx = i + 30
            
            # Make records more similar
            df.loc[dup_idx, 'name'] = df.loc[idx, 'name']
            df.loc[dup_idx, 'email'] = df.loc[idx, 'email']
            
            duplicate_pairs.append((idx, dup_idx))
        
        model = SupervisedDeduplicationModel(
            model_type='random_forest',
            key_features=['name', 'email', 'amount', 'category']
        )
        
        # Train model
        model.fit(df, duplicate_pairs)
        
        # Get feature importances
        importances = model.get_feature_importances()
        
        # Check that we have importances
        assert importances is not None
        assert len(importances) > 0
        
        # Importances should sum to approximately 1
        assert 0.95 <= sum(importances.values()) <= 1.05
        
        # Each importance should be between 0 and 1
        for feature, importance in importances.items():
            assert 0 <= importance <= 1