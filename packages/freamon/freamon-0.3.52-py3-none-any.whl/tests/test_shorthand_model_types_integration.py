"""
Unit tests for shorthand model type support across the entire library.

These tests verify that shorthand model types like 'lgbm_classifier' and 'lgbm_regressor'
are properly supported throughout different components including:
- HyperparameterTuningStep
- AutoModelFlow
- Pipeline
- ModelTrainingStep
"""
import pytest
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification, make_regression

from freamon.modeling.autoflow import AutoModelFlow
from freamon.pipeline.steps import HyperparameterTuningStep, ModelTrainingStep
from freamon.pipeline.pipeline import Pipeline
from freamon.modeling.factory import create_model

class TestShorthandModelTypeIntegration:
    """Tests for shorthand model type support throughout the library."""
    
    def setup_method(self):
        """Set up test data for classification and regression."""
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
    
    def test_factory_shorthand_support(self):
        """Test that model factory supports shorthand model types."""
        # Test classification shorthand
        cls_model = create_model('lgbm_classifier', 'classification', random_state=42)
        assert cls_model is not None
        assert hasattr(cls_model, 'fit')
        assert hasattr(cls_model, 'predict')
        
        # Test regression shorthand
        reg_model = create_model('lgbm_regressor', 'regression', random_state=42)
        assert reg_model is not None
        assert hasattr(reg_model, 'fit')
        assert hasattr(reg_model, 'predict')
    
    def test_model_training_step_shorthand(self):
        """Test that ModelTrainingStep supports shorthand model types."""
        # Classification model
        cls_step = ModelTrainingStep(
            name="cls_training",
            model_type="lgbm_classifier",
            problem_type="classification",
            random_state=42
        )
        
        X_train = self.train_cls.drop('target', axis=1)
        y_train = self.train_cls['target']
        
        # Should not raise exception
        cls_step.fit(X_train, y=y_train)
        assert cls_step.trainer is not None
        
        # Regression model
        reg_step = ModelTrainingStep(
            name="reg_training",
            model_type="lgbm_regressor",
            problem_type="regression",
            random_state=42
        )
        
        X_train_reg = self.train_reg.drop('target', axis=1)
        y_train_reg = self.train_reg['target']
        
        # Should not raise exception
        reg_step.fit(X_train_reg, y=y_train_reg)
        assert reg_step.trainer is not None
    
    def test_automodelflow_shorthand(self):
        """Test that AutoModelFlow supports shorthand model types."""
        # Classification
        cls_flow = AutoModelFlow(
            model_type="lgbm_classifier",
            problem_type="classification",
            random_state=42,
            verbose=False
        )
        
        # This should not raise an exception
        cls_flow.analyze_dataset(self.df_cls, target_column="target")
        
        # Regression
        reg_flow = AutoModelFlow(
            model_type="lgbm_regressor",
            problem_type="regression",
            random_state=42,
            verbose=False
        )
        
        # This should not raise an exception
        reg_flow.analyze_dataset(self.df_reg, target_column="target")
    
    def test_hyperparameter_tuning_step_validation(self):
        """Test that HyperparameterTuningStep validates shorthand model types."""
        # Check step creation for classification
        tuning_cls = HyperparameterTuningStep(
            name="tuning_cls",
            model_type="lgbm_classifier",
            problem_type="classification",
            n_trials=1,  # Minimal trials for test speed
            random_state=42
        )
        
        assert tuning_cls is not None
        assert tuning_cls.model_type == "lgbm_classifier"
        
        # Check step creation for regression
        tuning_reg = HyperparameterTuningStep(
            name="tuning_reg",
            model_type="lgbm_regressor",
            problem_type="regression",
            n_trials=1,  # Minimal trials for test speed
            random_state=42
        )
        
        assert tuning_reg is not None
        assert tuning_reg.model_type == "lgbm_regressor"
    
    def test_pipeline_with_shorthand_types(self):
        """Test Pipeline integration with shorthand model types."""
        # Create a simple pipeline with steps using shorthand model types
        # Pipeline expects a list of PipelineStep objects, not tuples
        train_step = ModelTrainingStep(
            name="train",
            model_type="lgbm_classifier",
            problem_type="classification",
            random_state=42
        )
        cls_pipeline = Pipeline([train_step])
        
        # Need to extract X and y separately since the pipeline's ModelTrainingStep 
        # expects y as a separate parameter
        X_train = self.train_cls.drop('target', axis=1)
        y_train = self.train_cls['target']
        # This should not raise an exception
        cls_pipeline.fit(X_train, y=y_train)
        
        # Make sure we can predict (need to exclude target column for prediction)
        X_test = self.test_cls.drop('target', axis=1)
        preds = cls_pipeline.predict(X_test)
        assert len(preds) == len(X_test)
        
        # Same test for regression
        reg_train_step = ModelTrainingStep(
            name="train",
            model_type="lgbm_regressor",
            problem_type="regression",
            random_state=42
        )
        reg_pipeline = Pipeline([reg_train_step])
        
        # Extract X and y for regression
        X_train_reg = self.train_reg.drop('target', axis=1)
        y_train_reg = self.train_reg['target']
        # This should not raise an exception
        reg_pipeline.fit(X_train_reg, y=y_train_reg)
        
        # Make sure we can predict (need to exclude target column for prediction)
        X_test_reg = self.test_reg.drop('target', axis=1)
        preds = reg_pipeline.predict(X_test_reg)
        assert len(preds) == len(X_test_reg)