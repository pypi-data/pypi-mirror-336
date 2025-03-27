"""
Unit tests for early stopping parameter handling across the library.

These tests verify that early_stopping_rounds is properly handled in:
- LightGBM model fitting
- HyperparameterTuningStep
- auto_model function
- ModelTrainingStep
"""
import pytest
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification

from freamon.modeling.factory import create_model
from freamon.modeling.autoflow import AutoModelFlow
from freamon.pipeline.steps import ModelTrainingStep, HyperparameterTuningStep
from freamon.modeling.model import Model

class TestEarlyStoppingParameter:
    """Tests for early stopping parameter handling."""
    
    def setup_method(self):
        """Set up test data."""
        # Create small classification dataset
        X, y = make_classification(
            n_samples=100,
            n_features=3,
            n_informative=2,
            n_redundant=0,
            n_classes=2,
            random_state=42
        )
        
        self.X = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(X.shape[1])])
        self.y = pd.Series(y, name="target")
        
        # Create small train/val/test split
        self.X_train = self.X.iloc[:70]
        self.y_train = self.y.iloc[:70]
        self.X_val = self.X.iloc[70:85]
        self.y_val = self.y.iloc[70:85]
        self.X_test = self.X.iloc[85:]
        self.y_test = self.y.iloc[85:]

    def test_model_early_stopping(self):
        """Test that early_stopping_rounds is properly handled in Model.fit()."""
        # Create model
        model = create_model('lgbm_classifier', 'classification', random_state=42)
        
        # Wrap in Model class
        model_wrapper = Model(model, 'classification')
        
        # Should not raise exception when early_stopping_rounds is provided
        model_wrapper.fit(
            self.X_train, 
            self.y_train, 
            val_X=self.X_val,
            val_y=self.y_val,
            early_stopping_rounds=5
        )
        
        # Predict
        preds = model_wrapper.predict(self.X_test)
        assert len(preds) == len(self.X_test)
    
    def test_early_stopping_in_model_training_step(self):
        """Test that early_stopping_rounds is properly handled in ModelTrainingStep."""
        # Create step
        step = ModelTrainingStep(
            name="training",
            model_type="lgbm_classifier",
            problem_type="classification",
            early_stopping_rounds=5,
            random_state=42
        )
        
        # Fit without validation data (should work without error)
        step.fit(self.X_train, y=self.y_train)
        
        # Fit with validation data
        step.fit(self.X_train, y=self.y_train, val_X=self.X_val, val_y=self.y_val)
        
        # Predict
        preds = step.predict(self.X_test)
        assert len(preds) == len(self.X_test)
    
    def test_early_stopping_in_hyperparameter_tuning(self):
        """Test that early_stopping_rounds is properly handled in HyperparameterTuningStep."""
        # Create step with minimal trials for speed
        step = HyperparameterTuningStep(
            name="tuning",
            model_type="lgbm_classifier",
            problem_type="classification",
            n_trials=2,  # Minimal for test speed
            early_stopping_rounds=5,
            random_state=42
        )
        
        # Should not raise exception 
        step.fit(self.X_train, y=self.y_train)
        
        # Predict
        preds = step.predict(self.X_test)
        assert len(preds) == len(self.X_test)
    
    def test_early_stopping_in_automodelflow(self):
        """Test that early_stopping_rounds is properly handled in AutoModelFlow."""
        # Create flow with minimal tuning
        flow = AutoModelFlow(
            model_type="lgbm_classifier",
            problem_type="classification",
            tuning_options={
                "n_trials": 2,  # Minimal for test speed
                "early_stopping_rounds": 5  # This should be properly extracted
            },
            random_state=42,
            verbose=False
        )
        
        # This should not raise an exception
        flow.analyze_dataset(pd.concat([self.X_train, self.y_train], axis=1), target_column="target")
        
        # Fit with train/val data
        flow.fit(self.X_train, self.y_train, val_X=self.X_val, val_y=self.y_val)
        
        # Predict
        preds = flow.predict(self.X_test)
        assert len(preds) == len(self.X_test)