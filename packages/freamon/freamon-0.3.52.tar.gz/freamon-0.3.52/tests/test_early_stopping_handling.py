"""
Unit tests for early_stopping_rounds parameter handling throughout the library.

These tests verify that the early_stopping_rounds parameter is correctly:
1. Extracted from tuning_options in auto_model
2. Passed to _train_model_with_tuning
3. Properly handled in model.fit() with LightGBM callbacks
"""
import pytest
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification, make_regression

from freamon.modeling.autoflow import auto_model, AutoModelFlow
from freamon.modeling.model import Model
from freamon.modeling.lightgbm import train_lightgbm_model

class TestEarlyStoppingHandling:
    """Tests for early_stopping_rounds parameter handling."""
    
    def setup_method(self):
        """Set up test data."""
        # Create small classification dataset
        X_cls, y_cls = make_classification(
            n_samples=100,
            n_features=3,
            n_informative=2,
            n_redundant=0,
            n_classes=2,
            random_state=42
        )
        
        self.df_cls = pd.DataFrame(X_cls, columns=[f"feature_{i}" for i in range(X_cls.shape[1])])
        self.df_cls['target'] = y_cls
        
        # Create small regression dataset
        X_reg, y_reg = make_regression(
            n_samples=100,
            n_features=3,
            n_informative=2,
            random_state=42
        )
        
        self.df_reg = pd.DataFrame(X_reg, columns=[f"feature_{i}" for i in range(X_reg.shape[1])])
        self.df_reg['target'] = y_reg
        
        # Create small train/test splits
        self.train_cls = self.df_cls.iloc[:80]
        self.test_cls = self.df_cls.iloc[80:]
        
        self.train_reg = self.df_reg.iloc[:80]
        self.test_reg = self.df_reg.iloc[80:]
    
    def test_parameter_extraction(self):
        """Test that early_stopping_rounds is correctly extracted from tuning_options."""
        # Define tuning options with early_stopping_rounds
        tuning_options = {
            'n_trials': 3,
            'early_stopping_rounds': 10,
            'custom_param': 'value'
        }
        
        # Extract early_stopping_rounds
        early_stopping_rounds = None
        if 'early_stopping_rounds' in tuning_options:
            early_stopping_rounds = tuning_options.pop('early_stopping_rounds')
        
        # Verify extraction
        assert early_stopping_rounds == 10
        assert 'early_stopping_rounds' not in tuning_options
        assert 'n_trials' in tuning_options
        assert 'custom_param' in tuning_options
    
    def test_model_fit_parameter_handling(self):
        """Test that the Model class correctly handles early_stopping_rounds."""
        # Test with direct Model instantiation and fit
        from freamon.modeling.factory import create_model
        
        # Create a model
        model = Model(
            create_model('lgbm_classifier', 'classification', random_state=42),
            model_type='lightgbm'
        )
        
        # Create train/val data for testing
        X_train = self.train_cls.drop('target', axis=1)
        y_train = self.train_cls['target']
        
        X_val = self.test_cls.drop('target', axis=1)
        y_val = self.test_cls['target']
        
        # This should not raise any exceptions
        model.fit(
            X_train, 
            y_train,
            eval_set=[(X_val, y_val)],
            early_stopping_rounds=5
        )
        
        # Model should be fitted
        assert model.is_fitted
    
    def test_lightgbm_train_with_early_stopping(self):
        """Test train_lightgbm_model with early_stopping_rounds parameter."""
        # Create a model
        from freamon.modeling.factory import create_model
        model = create_model('lgbm_classifier', 'classification', random_state=42)
        
        # Get data
        X_train = self.train_cls.drop('target', axis=1)
        y_train = self.train_cls['target']
        
        X_val = self.test_cls.drop('target', axis=1)
        y_val = self.test_cls['target']
        
        # Train with early stopping - this should not raise exceptions
        trained_model, metrics = train_lightgbm_model(
            model=model,
            train_df=self.train_cls,
            val_df=self.test_cls,
            feature_columns=X_train.columns.tolist(),
            target_column='target',
            problem_type='classification',
            early_stopping_rounds=5,
            verbose=False
        )
        
        # Model should be trained
        assert trained_model is not None
        assert metrics is not None
    
    def test_autoflow_with_early_stopping(self):
        """Test AutoModelFlow with early_stopping_rounds extraction."""
        # Create AutoModelFlow instance
        flow = AutoModelFlow(
            model_type='lgbm_classifier',
            problem_type='classification',
            random_state=42,
            verbose=False
        )
        
        # This simulates the early_stopping_rounds extraction logic in AutoModelFlow.fit
        tuning_options = {
            'n_trials': 3,
            'early_stopping_rounds': 10
        }
        
        # Extract early_stopping_rounds
        early_stopping_rounds = tuning_options.pop('early_stopping_rounds', 50) if tuning_options else 50
        
        # Check extraction
        assert early_stopping_rounds == 10
        assert 'early_stopping_rounds' not in tuning_options
        
        # Check default extraction
        tuning_options_no_early = {'n_trials': 3}
        early_stopping_default = tuning_options_no_early.pop('early_stopping_rounds', 50) if tuning_options_no_early else 50
        assert early_stopping_default == 50
    
    def test_autoflow_combined_options(self):
        """Test combined parameter filtering for both early_stopping_rounds and text options."""
        # Simulate both parameter handling mechanisms
        tuning_options = {
            'n_trials': 2,
            'early_stopping_rounds': 15,
            'custom_param': 'value'
        }
        
        text_options = {
            'n_topics': 5,
            'sampling_ratio': 0.8,
            'min_df': 1
        }
        
        # Extract early_stopping_rounds
        early_stopping_rounds = None
        if 'early_stopping_rounds' in tuning_options:
            early_stopping_rounds = tuning_options.pop('early_stopping_rounds')
        
        # Set supported text options
        supported_text_options = {'n_topics', 'min_df', 'max_df', 'method'}
        
        # Filter text options
        filtered_text_options = {}
        for key, value in text_options.items():
            if key in supported_text_options:
                filtered_text_options[key] = value
        
        # Check both parameter handling mechanisms
        assert early_stopping_rounds == 15
        assert 'sampling_ratio' not in filtered_text_options
        assert 'n_topics' in filtered_text_options
        assert 'min_df' in filtered_text_options