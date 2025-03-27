"""
Tests for the Polars-optimized supervised deduplication module.
"""
import pytest
import pandas as pd
import numpy as np
import polars as pl
from datetime import datetime, timedelta

from freamon.deduplication.polars_supervised_deduplication import PolarsSupervisedDeduplicationModel


class TestPolarsSupervisedDeduplication:
    """Test class for Polars-optimized supervised deduplication functionality."""
    
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
    
    @pytest.fixture
    def sample_polars_data(self, sample_data):
        """Convert sample data to Polars DataFrame."""
        df, duplicate_pairs = sample_data
        return pl.from_pandas(df), duplicate_pairs
    
    def test_init(self):
        """Test initialization of the model."""
        model = PolarsSupervisedDeduplicationModel(
            model_type='lightgbm',
            date_features=['date'],
            key_features=['name', 'email'],
            use_polars=True
        )
        
        assert model.model_type == 'lightgbm'
        assert model.date_features == ['date']
        assert model.key_features == ['name', 'email']
        assert model.model is None
        assert not model.trained
        assert model.use_polars is True
    
    def test_generate_pair_features_polars(self, sample_polars_data):
        """Test feature generation with Polars."""
        df, _ = sample_polars_data
        
        # Create model with Polars enabled
        model = PolarsSupervisedDeduplicationModel(
            model_type='lightgbm',
            date_features=['date'],
            key_features=['name', 'email', 'amount', 'category'],
            use_polars=True
        )
        
        # Create two small test dataframes
        df1 = df.slice(0, 3)
        df2 = df.slice(3, 3)
        
        # Generate features
        features = model._generate_pair_features_polars(df1, df2)
        
        # Should have generated features
        assert isinstance(features, pd.DataFrame)
        assert len(features) > 0
        
        # Should have numeric features for amount
        assert 'amount_abs_diff' in features.columns
        
        # Should have date features
        assert 'date_days_diff' in features.columns
    
    def test_generate_pair_features(self, sample_data):
        """Test feature generation with both Polars and pandas."""
        df, _ = sample_data
        
        # Create model with Polars enabled
        model = PolarsSupervisedDeduplicationModel(
            key_features=['name', 'email', 'amount', 'category'],
            date_features=['date'],
            use_polars=True
        )
        
        # Create two small test dataframes
        df1 = df.iloc[:3].copy()
        df2 = df.iloc[3:6].copy()
        
        # Generate features - should use Polars
        features = model._generate_pair_features(df1, df2)
        
        # Should have generated features for each key feature
        assert 'name_text_sim' in features.columns
        assert 'email_text_sim' in features.columns
        assert 'amount_abs_diff' in features.columns
        assert 'category_exact_match' in features.columns
        
        # Should have generated features for date
        assert 'date_days_diff' in features.columns
        
        # Now disable Polars and test the pandas fallback
        model.use_polars = False
        features_pandas = model._generate_pair_features(df1, df2)
        
        # Should have similar structure
        assert set(features.columns).issubset(features_pandas.columns) or \
               set(features_pandas.columns).issubset(features.columns)
    
    def test_create_training_pairs_polars(self, sample_polars_data):
        """Test creation of training pairs with Polars."""
        df, duplicate_pairs = sample_polars_data
        
        model = PolarsSupervisedDeduplicationModel(
            key_features=['name', 'email'],
            use_polars=True
        )
        
        # Create training pairs
        df1, df2, labels = model._create_training_pairs_polars(df, duplicate_pairs[:5])
        
        # Verify output types
        assert isinstance(df1, pl.DataFrame)
        assert isinstance(df2, pl.DataFrame)
        assert isinstance(labels, pd.Series)
        
        # Verify sizes
        assert len(df1) > 5  # Should have positive and negative examples
        assert len(df1) == len(df2)
        assert len(df1) == len(labels)
        
        # Verify label distribution
        assert (labels == 1).sum() == 5  # 5 positive examples
        assert (labels == 0).sum() > 0  # Some negative examples
    
    def test_create_training_pairs(self, sample_data):
        """Test creation of training pairs with both Polars and pandas."""
        df, duplicate_pairs = sample_data
        
        # First test with Polars
        model = PolarsSupervisedDeduplicationModel(
            key_features=['name', 'email'],
            use_polars=True
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
        
        # Now test with pandas fallback
        model.use_polars = False
        df1_pd, df2_pd, labels_pd = model._create_training_pairs(df, duplicate_pairs[:5])
        
        # Results should be similar in structure
        assert len(df1_pd) > 5
        assert len(df1_pd) == len(df2_pd)
        assert len(df1_pd) == len(labels_pd)
    
    def test_fit_and_predict(self, sample_data):
        """Test fitting the model and making predictions."""
        df, duplicate_pairs = sample_data
        
        # Split into train and test sets
        train_size = 40
        train_df = df.iloc[:train_size].copy().reset_index(drop=True)
        test_df = df.iloc[train_size:].copy().reset_index(drop=True)
        
        # Create some synthetic duplicate pairs for training
        train_duplicate_pairs = []
        for i in range(5):
            idx1 = i
            idx2 = i + 20
            
            # Manually modify a record to be similar to another
            train_df.loc[idx2, 'name'] = train_df.loc[idx1, 'name'] + ' Jr'
            train_df.loc[idx2, 'email'] = train_df.loc[idx1, 'email']
            
            train_duplicate_pairs.append((idx1, idx2))
        
        # Initialize and train model with Polars
        model = PolarsSupervisedDeduplicationModel(
            model_type='lightgbm',
            key_features=['name', 'email', 'amount', 'category'],
            date_features=['date'],
            use_polars=True
        )
        
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
    
    def test_predict_duplicate_probability_chunked(self, sample_data):
        """Test chunked prediction for large datasets."""
        df, duplicate_pairs = sample_data
        
        # Create synthetic duplicates for training
        for i in range(5):
            idx1 = i
            idx2 = i + 30
            
            # Make records more similar
            df.loc[idx2, 'name'] = df.loc[idx1, 'name']
            df.loc[idx2, 'email'] = df.loc[idx1, 'email']
            
            duplicate_pairs.append((idx1, idx2))
        
        # Initialize and train model
        model = PolarsSupervisedDeduplicationModel(
            model_type='lightgbm',
            key_features=['name', 'email', 'amount'],
            use_polars=True
        )
        
        # Train the model
        model.fit(df, duplicate_pairs)
        
        # Test chunked prediction
        result = model.predict_duplicate_probability_chunked(
            df=df,
            chunk_size=20,  # Small chunk size for testing
            max_pairs=1000,
            threshold=0.5
        )
        
        # Should return a dataframe with probabilities
        assert isinstance(result, pd.DataFrame)
        assert 'duplicate_probability' in result.columns
        assert len(result) > 0
    
    def test_evaluate(self, sample_data):
        """Test model evaluation metrics."""
        df, duplicate_pairs = sample_data
        
        # Create more synthetic duplicates for testing
        for i in range(5):
            idx1 = i
            idx2 = i + 25
            
            # Make records more similar
            df.loc[idx2, 'name'] = df.loc[idx1, 'name']
            df.loc[idx2, 'email'] = df.loc[idx1, 'email']
            
            duplicate_pairs.append((idx1, idx2))
        
        # Initialize and train model
        model = PolarsSupervisedDeduplicationModel(
            model_type='lightgbm',
            key_features=['name', 'email', 'amount'],
            use_polars=True
        )
        
        # Train the model
        model.fit(df, duplicate_pairs)
        
        # Evaluate model on same data
        metrics = model.evaluate(df, duplicate_pairs)
        
        # Check that we have all expected metrics
        assert 'precision' in metrics
        assert 'recall' in metrics
        assert 'f1' in metrics
        assert 'auc' in metrics
        
        # Metrics should be between 0 and 1
        for metric, value in metrics.items():
            assert 0 <= value <= 1
    
    def test_auto_tune_threshold(self, sample_data):
        """Test automatic threshold tuning."""
        df, duplicate_pairs = sample_data
        
        # Create synthetic duplicates for training
        for i in range(5):
            idx1 = i
            idx2 = i + 30
            
            # Make records more similar
            df.loc[idx2, 'name'] = df.loc[idx1, 'name']
            df.loc[idx2, 'email'] = df.loc[idx1, 'email']
            
            duplicate_pairs.append((idx1, idx2))
        
        # Initialize and train model
        model = PolarsSupervisedDeduplicationModel(
            model_type='lightgbm',
            key_features=['name', 'email', 'amount'],
            use_polars=True
        )
        
        # Train the model
        model.fit(df, duplicate_pairs)
        
        # Auto-tune threshold
        results = model.auto_tune_threshold(
            df=df,
            true_duplicate_pairs=duplicate_pairs,
            threshold_range=[0.3, 0.5, 0.7, 0.9],
            optimize_for='f1'
        )
        
        # Should return results dict
        assert isinstance(results, dict)
        assert 'best_threshold' in results
        assert 'best_metrics' in results
        assert 'all_results' in results
        
        # Should have updated optimal threshold
        assert model.optimal_threshold > 0
        assert model.auto_tuning_performed is True
    
    def test_ensemble_methods(self, sample_data):
        """Test ensemble methods for deduplication."""
        df, duplicate_pairs = sample_data
        
        # Create synthetic duplicates for training
        for i in range(5):
            idx1 = i
            idx2 = i + 30
            
            # Make records more similar
            df.loc[idx2, 'name'] = df.loc[idx1, 'name']
            df.loc[idx2, 'email'] = df.loc[idx1, 'email']
            
            duplicate_pairs.append((idx1, idx2))
        
        # Initialize model
        model = PolarsSupervisedDeduplicationModel(
            key_features=['name', 'email', 'amount'],
            use_polars=True
        )
        
        # Train ensemble
        model.fit_ensemble(
            df=df,
            duplicate_pairs=duplicate_pairs,
            model_types=['lightgbm', 'random_forest'],
            model_weights=[0.7, 0.3]
        )
        
        # Should have ensemble models
        assert len(model.ensemble_models) == 2
        assert len(model.ensemble_weights) == 2
        assert model.trained is True
        
        # Test prediction with ensemble
        predictions = model.predict_duplicate_probability(df=df)
        
        # Should return predictions
        assert isinstance(predictions, pd.DataFrame)
        assert len(predictions) > 0
    
    def test_explainability(self, sample_data):
        """Test explainability features."""
        df, duplicate_pairs = sample_data
        
        # Create synthetic duplicates
        idx1, idx2 = 0, 30
        df.loc[idx2, 'name'] = df.loc[idx1, 'name']
        df.loc[idx2, 'email'] = df.loc[idx1, 'email']
        duplicate_pairs.append((idx1, idx2))
        
        # Initialize and train model
        model = PolarsSupervisedDeduplicationModel(
            model_type='random_forest',  # Model with feature importances
            key_features=['name', 'email', 'amount', 'category'],
            use_polars=True
        )
        
        # Train the model
        model.fit(df, duplicate_pairs)
        
        # Make prediction to populate feature contributions
        model.predict_duplicate_probability(df=df)
        
        # Get feature contributions
        contributions = model.get_feature_contributions(top_n=5)
        
        # Should return contributions
        assert isinstance(contributions, dict)
        assert len(contributions) <= 5  # At most top_n features
        
        # Get explanation for a pair
        record1 = df.iloc[idx1].to_dict()
        record2 = df.iloc[idx2].to_dict()
        
        explanation = model.get_explanation_for_pair(record1, record2)
        
        # Should return explanation
        assert isinstance(explanation, dict)
        assert 'probability' in explanation
        assert 'key_similarities' in explanation
        assert 'key_differences' in explanation
    
    def test_process_large_dataset(self, sample_data):
        """Test processing of large datasets in chunks."""
        df, duplicate_pairs = sample_data
        
        # Make sure we have enough duplicates
        for i in range(5):
            idx1 = i
            idx2 = i + 40
            df.loc[idx2, 'name'] = df.loc[idx1, 'name']
            df.loc[idx2, 'email'] = df.loc[idx1, 'email']
            duplicate_pairs.append((idx1, idx2))
        
        # Initialize and train model
        model = PolarsSupervisedDeduplicationModel(
            model_type='lightgbm',
            key_features=['name', 'email'],
            use_polars=True
        )
        
        # Train the model
        model.fit(df, duplicate_pairs)
        
        # Process large dataset
        detected_duplicates = model.process_large_dataset(
            df=df,
            chunk_size=20,  # Small chunk size for testing
            threshold=0.5,
            show_progress=False
        )
        
        # Should find duplicates
        assert isinstance(detected_duplicates, list)
        assert len(detected_duplicates) > 0
        assert all(isinstance(pair, tuple) for pair in detected_duplicates)
    
    def test_active_learning(self, sample_data):
        """Test active learning functionality."""
        df, duplicate_pairs = sample_data
        
        # Initialize and train model
        model = PolarsSupervisedDeduplicationModel(
            model_type='lightgbm',
            key_features=['name', 'email', 'amount'],
            use_polars=True
        )
        
        # Set uncertainty threshold
        model.uncertainty_threshold = 0.4  # More uncertain samples
        
        # Train the model
        model.fit(df, duplicate_pairs)
        
        # Make predictions to identify uncertain samples
        model.predict_duplicate_probability(df=df)
        
        # Request active learning samples
        samples = model.request_active_learning_samples(n_samples=3)
        
        # Should return samples to label
        assert isinstance(samples, list)
        
        # If we have uncertain samples, test the labeling flow
        if samples:
            # Label a sample
            labeled_samples = [{
                'idx1': samples[0]['idx1'],
                'idx2': samples[0]['idx2'],
                'is_duplicate': True
            }]
            
            # Add labeled samples
            model.add_labeled_samples(labeled_samples)
            
            # Update model with active learning
            model.update_model_with_active_learning(df)
            
            # Should have incorporated labeled samples
            assert not model.labeled_samples
    
    def test_incremental_learning(self, sample_data):
        """Test incremental learning functionality."""
        df, duplicate_pairs = sample_data
        
        # Split data
        train_size = 40
        train_df = df.iloc[:train_size].copy().reset_index(drop=True)
        new_df = df.iloc[train_size:].copy().reset_index(drop=True)
        
        # Adjust duplicate pairs
        train_pairs = []
        new_pairs = []
        
        for i, j in duplicate_pairs:
            if i < train_size and j < train_size:
                train_pairs.append((i, j))
            elif i >= train_size and j >= train_size:
                new_pairs.append((i - train_size, j - train_size))
        
        # Create synthetic pairs if needed
        if not train_pairs:
            for i in range(3):
                train_df.loc[i+10, 'name'] = train_df.loc[i, 'name']
                train_df.loc[i+10, 'email'] = train_df.loc[i, 'email']
                train_pairs.append((i, i+10))
        
        if not new_pairs:
            for i in range(2):
                new_df.loc[i+5, 'name'] = new_df.loc[i, 'name']
                new_df.loc[i+5, 'email'] = new_df.loc[i, 'email']
                new_pairs.append((i, i+5))
        
        # Initialize and train model
        model = PolarsSupervisedDeduplicationModel(
            model_type='lightgbm',
            key_features=['name', 'email'],
            use_polars=True
        )
        
        # Train on initial data
        model.fit(train_df, train_pairs)
        
        # Enable incremental mode
        model.incremental_mode = True
        
        # Update model incrementally
        model.incremental_fit(new_df, new_pairs, learning_rate=0.3)
        
        # Model should still be trained
        assert model.trained
        
        # Test predictions on new data
        predictions = model.predict_duplicate_probability(df=new_df)
        
        # Should return predictions
        assert isinstance(predictions, pd.DataFrame)
        assert len(predictions) > 0