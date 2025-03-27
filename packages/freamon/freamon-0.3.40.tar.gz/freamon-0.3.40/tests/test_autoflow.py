"""
Unit tests for AutoModelFlow's automatic train-test splitting functionality.
"""
import pandas as pd
import numpy as np
import pytest
from sklearn.datasets import make_classification, make_regression

from freamon.modeling.autoflow import auto_model, AutoModelFlow

class TestAutoModelFlow:
    """Tests for AutoModelFlow's automatic train-test splitting functionality."""
    
    def test_auto_split_classification(self):
        """Test automatic train-test splitting for classification."""
        # Generate synthetic classification data
        X, y = make_classification(
            n_samples=100,
            n_features=5,
            n_informative=3,
            n_redundant=1,
            n_classes=2,
            random_state=42
        )
        
        # Create a dataframe
        df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(X.shape[1])])
        df['target'] = y
        
        # Use auto_model with automatic train-test splitting
        results = auto_model(
            df=df,
            target_column='target',
            model_type='lgbm_classifier',
            problem_type='classification',
            cv_folds=2,  # Use fewer folds for faster tests
            test_size=0.2,
            auto_split=True,
            random_state=42,
            tuning=False  # For faster tests
        )
        
        # Check if required components are in results
        assert 'model' in results
        assert 'test_metrics' in results
        assert 'test_df' in results
        assert 'autoflow' in results
        
        # Verify metrics
        assert 'accuracy' in results['test_metrics']
        assert 'precision' in results['test_metrics']
        assert 'recall' in results['test_metrics']
        assert 'f1' in results['test_metrics']
        
        # Verify feature importance
        assert 'feature_importance' in results
        assert isinstance(results['feature_importance'], pd.DataFrame)
        assert len(results['feature_importance']) > 0
    
    def test_auto_split_time_series(self):
        """Test automatic train-test splitting for time series data."""
        # Create synthetic time series data
        np.random.seed(42)
        dates = pd.date_range(start='2020-01-01', periods=100, freq='D')
        
        # Generate regression data
        X, y = make_regression(
            n_samples=100,
            n_features=5,
            n_informative=3,
            random_state=42
        )
        
        # Create a dataframe
        df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(X.shape[1])])
        df['date'] = dates
        df['target'] = y
        
        # Use auto_model with automatic time-based splitting
        results = auto_model(
            df=df,
            target_column='target',
            date_column='date',
            model_type='lgbm_regressor',
            problem_type='regression',
            cv_folds=2,  # Use fewer folds for faster tests
            metrics=['rmse', 'mae', 'r2'],
            time_options={
                'create_target_lags': True,
                'lag_periods': [1, 7],
                'rolling_windows': [7]
            },
            test_size=0.2,
            auto_split=True,
            random_state=42,
            tuning=False,  # For faster tests
            verbose=False
        )
        
        # Check if required components are in results
        assert 'model' in results
        assert 'test_metrics' in results
        assert 'test_df' in results
        assert 'autoflow' in results
        
        # Verify metrics
        assert 'rmse' in results['test_metrics']
        assert 'mae' in results['test_metrics']
        assert 'r2' in results['test_metrics']
        
        # Verify feature importance
        assert 'feature_importance' in results
        assert isinstance(results['feature_importance'], pd.DataFrame)
        assert len(results['feature_importance']) > 0
        
        # Test predictions on test data
        test_df = results['test_df']
        preds = results['autoflow'].predict(test_df)
        assert len(preds) == len(test_df)
    
    def test_model_type_shortcuts(self):
        """Test that shorthand model types like lgbm_classifier work properly."""
        # Generate synthetic classification data
        X, y = make_classification(
            n_samples=50, 
            n_features=5,
            n_informative=2,
            n_redundant=1,
            n_classes=2,
            random_state=42
        )
        
        df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(X.shape[1])])
        df['target'] = y
        
        # Test different shorthand model types
        model_types = ['lgbm_classifier', 'lgbm_regressor']
        
        for model_type in model_types:
            problem_type = 'classification' if 'classifier' in model_type else 'regression'
            
            # Create model
            autoflow = AutoModelFlow(
                model_type=model_type,
                problem_type=problem_type,
                verbose=False
            )
            
            # Should not raise any exceptions
            autoflow.analyze_dataset(df, target_column='target')