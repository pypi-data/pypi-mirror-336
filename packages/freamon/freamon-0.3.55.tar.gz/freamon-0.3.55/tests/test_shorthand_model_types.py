"""
Unit tests for shorthand model type support across the pipeline.

These tests verify that shorthand model types like 'lgbm_classifier' and 'lgbm_regressor'
are correctly supported throughout the modeling pipeline, including in hyperparameter tuning.
"""
import pandas as pd
import numpy as np
import pytest
from sklearn.datasets import make_classification, make_regression

from freamon.modeling.autoflow import auto_model, AutoModelFlow
from freamon.pipeline.steps import HyperparameterTuningStep, ModelTrainingStep
from freamon.pipeline.pipeline import Pipeline
from freamon.modeling.factory import create_model

class TestShorthandModelTypes:
    """Tests for shorthand model type support across the system."""
    
    def setup_method(self):
        """Set up test data for classification and regression."""
        # Classification data
        X_cls, y_cls = make_classification(
            n_samples=100,
            n_features=5,
            n_informative=3,
            n_redundant=1,
            n_classes=2,
            random_state=42
        )
        
        self.df_cls = pd.DataFrame(X_cls, columns=[f"feature_{i}" for i in range(X_cls.shape[1])])
        self.df_cls['target'] = y_cls
        
        # Regression data
        X_reg, y_reg = make_regression(
            n_samples=100,
            n_features=5,
            n_informative=3,
            random_state=42
        )
        
        self.df_reg = pd.DataFrame(X_reg, columns=[f"feature_{i}" for i in range(X_reg.shape[1])])
        self.df_reg['target'] = y_reg
        
        # List of shorthand model types to test
        self.shorthand_models = [
            ('lgbm_classifier', 'classification'),
            ('lgbm_regressor', 'regression'),
        ]
    
    def test_model_factory_shorthand_support(self):
        """Test that create_model supports shorthand model types."""
        for model_type, problem_type in self.shorthand_models:
            # This should not raise an exception
            model = create_model(
                model_type=model_type,
                problem_type=problem_type,
                random_state=42
            )
            
            # Check the model is created correctly
            assert model is not None
            
            # Verify model type
            if problem_type == 'classification':
                assert hasattr(model, 'predict_proba')
            else:
                assert hasattr(model, 'predict')
    
    def test_autoflow_shorthand_support(self):
        """Test that AutoModelFlow supports shorthand model types."""
        for model_type, problem_type in self.shorthand_models:
            # Create AutoModelFlow instance with shorthand model type
            autoflow = AutoModelFlow(
                model_type=model_type,
                problem_type=problem_type,
                random_state=42,
                verbose=False
            )
            
            # Get appropriate dataset
            df = self.df_cls if problem_type == 'classification' else self.df_reg
            
            # Analyze dataset
            autoflow.analyze_dataset(df, target_column='target')
            
            # Fit model
            autoflow.fit(df)
            
            # Predict
            predictions = autoflow.predict(df)
            assert len(predictions) == len(df)
    
    def test_tuning_step_shorthand_support(self):
        """Test that HyperparameterTuningStep supports shorthand model types."""
        for model_type, problem_type in self.shorthand_models:
            # Create tuning step with shorthand model type
            tuning_step = HyperparameterTuningStep(
                model_type=model_type,
                problem_type=problem_type,
                target_column='target',
                n_trials=2,  # Small number for faster tests
                random_state=42
            )
            
            # Get appropriate dataset
            df = self.df_cls if problem_type == 'classification' else self.df_reg
            
            # This should not raise an exception
            tuning_step.fit(df)
            transformed_df = tuning_step.transform(df)
            
            # Verify tuning completed successfully
            assert tuning_step.best_params is not None
            assert tuning_step.best_score is not None
    
    def test_model_training_step_shorthand_support(self):
        """Test that ModelTrainingStep supports shorthand model types."""
        for model_type, problem_type in self.shorthand_models:
            # Create training step with shorthand model type
            training_step = ModelTrainingStep(
                model_type=model_type,
                problem_type=problem_type,
                target_column='target',
                random_state=42
            )
            
            # Get appropriate dataset
            df = self.df_cls if problem_type == 'classification' else self.df_reg
            
            # This should not raise an exception
            training_step.fit(df)
            predictions = training_step.predict(df)
            
            # Verify training completed successfully
            assert training_step.model is not None
            assert len(predictions) == len(df)
    
    def test_pipeline_shorthand_support(self):
        """Test that Pipeline supports shorthand model types in its steps."""
        for model_type, problem_type in self.shorthand_models:
            # Create a pipeline with tuning and training steps using shorthand model types
            pipeline = Pipeline([
                ('tuning', HyperparameterTuningStep(
                    model_type=model_type,
                    problem_type=problem_type,
                    target_column='target',
                    n_trials=2,
                    random_state=42
                )),
                ('training', ModelTrainingStep(
                    model_type=model_type,
                    problem_type=problem_type,
                    target_column='target',
                    random_state=42
                ))
            ])
            
            # Get appropriate dataset
            df = self.df_cls if problem_type == 'classification' else self.df_reg
            
            # This should not raise an exception
            pipeline.fit(df)
            predictions = pipeline.predict(df)
            
            # Verify pipeline completed successfully
            assert pipeline.steps[-1][1].model is not None
            assert len(predictions) == len(df)
    
    def test_auto_model_with_tuning_shorthand_support(self):
        """Test auto_model with shorthand model types and tuning enabled."""
        for model_type, problem_type in self.shorthand_models:
            # Get appropriate dataset
            df = self.df_cls if problem_type == 'classification' else self.df_reg
            
            # Use auto_model with shorthand model type and tuning
            results = auto_model(
                df=df,
                target_column='target',
                model_type=model_type,
                problem_type=problem_type,
                cv_folds=2,  # Use fewer folds for faster tests
                test_size=0.2,
                auto_split=True,
                random_state=42,
                tuning=True,
                tuning_options={
                    'n_trials': 2,  # Small number for faster tests
                    'early_stopping_rounds': 5  # Testing our fix
                }
            )
            
            # Verify results
            assert 'model' in results
            assert 'test_metrics' in results
            assert 'autoflow' in results
            assert 'feature_importance' in results