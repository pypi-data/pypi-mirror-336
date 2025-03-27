"""
Model performance reporting module.

This module provides functions for generating comprehensive reports 
about model performance, including metrics, cross-validation results,
feature importance, and visualizations.
"""
from typing import Any, Dict, List, Optional, Union, Tuple
import os
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

from freamon.eda.export import export_to_excel, export_to_powerpoint


def generate_model_performance_report(
    model_results: Dict[str, Any],
    cv_results: Optional[Dict[str, List]] = None,
    feature_importance: Optional[Dict[str, Any]] = None,
    export_format: Optional[str] = None,
    output_path: Optional[str] = None,
    include_visualizations: bool = True,
) -> Dict[str, Any]:
    """
    Generate a comprehensive model performance report.
    
    Parameters
    ----------
    model_results : Dict[str, Any]
        Dictionary containing model results, should include:
        - model_type: str, type of model (classification, regression)
        - model_library: str, library used (lightgbm, sklearn, etc.)
        - metrics: Dict[str, float], performance metrics
        - predictions: Array-like, model predictions
        - actuals: Array-like, actual values
        - confusion_matrix: Optional np.ndarray, confusion matrix (for classification)
        - class_labels: Optional List[str], class labels (for classification)
    cv_results : Optional[Dict[str, List]], default=None
        Cross-validation results with metrics for each fold
    feature_importance : Optional[Dict[str, Any]], default=None
        Feature importance information, can be:
        - Dict mapping feature names to importance values
        - Dict with 'importances_mean', 'importances_std', 'feature_names' (scikit-learn format)
    export_format : Optional[str], default=None
        Format to export the report to. Options: 'xlsx', 'pptx'. 
        If None, no export is performed.
    output_path : Optional[str], default=None
        Path to save the exported report. Required if export_format is provided.
    include_visualizations : bool, default=True
        Whether to include visualizations in the report.
        
    Returns
    -------
    Dict[str, Any]
        Dictionary containing the report data
    """
    # Create report data dictionary
    report_data = {
        'model_type': model_results.get('model_type', 'Unknown'),
        'model_library': model_results.get('model_library', 'Unknown'),
        'training_date': model_results.get('training_date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        'metrics': model_results.get('metrics', {}),
        'predictions': model_results.get('predictions', None),
        'actuals': model_results.get('actuals', None),
        'confusion_matrix': model_results.get('confusion_matrix', None),
        'class_labels': model_results.get('class_labels', None)
    }
    
    # Add CV results if provided
    if cv_results:
        report_data['cv_results'] = cv_results
    
    # Add feature importance if provided
    if feature_importance:
        report_data['feature_importance'] = feature_importance
    
    # Generate visualizations if requested
    if include_visualizations:
        # Store visualization paths
        visualizations = {}
        
        # Determine if it's a classification or regression model
        is_classification = ('model_type' in model_results and 
                            'class' in model_results['model_type'].lower())
        
        # Create appropriate visualizations based on model type
        if is_classification:
            # Confusion matrix visualization
            if report_data['confusion_matrix'] is not None:
                confusion_matrix = report_data['confusion_matrix']
                class_labels = report_data['class_labels'] or [
                    f'Class {i}' for i in range(confusion_matrix.shape[0])
                ]
                
                plt.figure(figsize=(10, 8))
                sns.heatmap(confusion_matrix, annot=True, fmt='d', cmap='Blues',
                           xticklabels=class_labels, yticklabels=class_labels)
                plt.xlabel('Predicted')
                plt.ylabel('Actual')
                plt.title('Confusion Matrix')
                
                # Save visualization
                img_path = "confusion_matrix.png" if not output_path else f"{os.path.splitext(output_path)[0]}_confusion_matrix.png"
                plt.savefig(img_path)
                plt.close()
                
                visualizations['confusion_matrix'] = img_path
        else:  # Regression model
            # Actual vs Predicted scatter plot
            if report_data['predictions'] is not None and report_data['actuals'] is not None:
                predictions = report_data['predictions']
                actuals = report_data['actuals']
                
                plt.figure(figsize=(10, 8))
                plt.scatter(actuals, predictions, alpha=0.5)
                
                # Add perfect prediction line
                min_val = min(min(actuals), min(predictions))
                max_val = max(max(actuals), max(predictions))
                plt.plot([min_val, max_val], [min_val, max_val], 'r--')
                
                plt.xlabel('Actual')
                plt.ylabel('Predicted')
                plt.title('Actual vs Predicted Values')
                plt.axis('equal')
                
                # Save visualization
                img_path = "actual_vs_predicted.png" if not output_path else f"{os.path.splitext(output_path)[0]}_actual_vs_predicted.png"
                plt.savefig(img_path)
                plt.close()
                
                visualizations['actual_vs_predicted'] = img_path
                
                # Prediction error histogram
                errors = np.array(actuals) - np.array(predictions)
                
                plt.figure(figsize=(10, 6))
                plt.hist(errors, bins=30, alpha=0.7)
                plt.axvline(x=0, color='r', linestyle='--')
                plt.xlabel('Prediction Error')
                plt.ylabel('Frequency')
                plt.title('Distribution of Prediction Errors')
                
                # Save visualization
                img_path = "error_distribution.png" if not output_path else f"{os.path.splitext(output_path)[0]}_error_distribution.png"
                plt.savefig(img_path)
                plt.close()
                
                visualizations['error_distribution'] = img_path
        
        # Feature importance visualization
        if feature_importance:
            # Handle different types of feature importance
            if 'importances_mean' in feature_importance:
                # Handle scikit-learn style importance
                features = feature_importance.get('feature_names', [])
                importances = feature_importance.get('importances_mean', [])
            elif isinstance(feature_importance, dict) and len(feature_importance) > 0:
                # Handle simple dict of feature->importance mappings
                features = list(feature_importance.keys())
                importances = list(feature_importance.values())
            else:
                features = []
                importances = []
            
            if features and importances:
                # Sort features by importance
                sorted_idx = np.argsort(importances)
                top_features = [features[i] for i in sorted_idx[-20:]]  # Top 20 features
                top_importances = [importances[i] for i in sorted_idx[-20:]]
                
                plt.figure(figsize=(12, 10))
                plt.barh(range(len(top_features)), top_importances, align='center')
                plt.yticks(range(len(top_features)), top_features)
                plt.xlabel('Importance')
                plt.title('Feature Importance')
                
                # Save visualization
                img_path = "feature_importance.png" if not output_path else f"{os.path.splitext(output_path)[0]}_feature_importance.png"
                plt.savefig(img_path)
                plt.close()
                
                visualizations['feature_importance'] = img_path
        
        # Cross-validation results visualization
        if cv_results:
            # Extract metrics (skip non-metric fields)
            metrics = {}
            non_metrics = ['fold', 'train_size', 'test_size', 'train_start_date', 
                          'train_end_date', 'test_start_date', 'test_end_date',
                          'predictions', 'test_targets', 'test_dates']
            
            for metric, values in cv_results.items():
                if metric not in non_metrics and isinstance(values[0], (int, float)):
                    metrics[metric] = values
            
            if metrics:
                # Calculate mean and std for each metric
                means = {k: np.mean(v) for k, v in metrics.items()}
                stds = {k: np.std(v) for k, v in metrics.items()}
                
                plt.figure(figsize=(12, 8))
                x = list(means.keys())
                y = list(means.values())
                error = list(stds.values())
                
                plt.bar(x, y, yerr=error, capsize=5, color=sns.color_palette("viridis", len(x)))
                plt.title('Cross-Validation Metrics')
                plt.xticks(rotation=45, ha='right')
                plt.ylabel('Value')
                plt.tight_layout()
                
                # Save visualization
                img_path = "cv_metrics.png" if not output_path else f"{os.path.splitext(output_path)[0]}_cv_metrics.png"
                plt.savefig(img_path)
                plt.close()
                
                visualizations['cv_metrics'] = img_path
        
        # Add visualizations to report data
        report_data['visualizations'] = visualizations
    
    # Handle export if requested
    if export_format and output_path:
        if export_format.lower() == 'xlsx':
            export_to_excel(report_data, output_path, report_type="model")
            print(f"Excel report exported to {output_path}")
        elif export_format.lower() == 'pptx':
            export_to_powerpoint(report_data, output_path, report_type="model")
            print(f"PowerPoint report exported to {output_path}")
        else:
            print(f"Unsupported export format: {export_format}")
    
    return report_data


def generate_hyperparameter_tuning_report(
    tuning_results: Dict[str, Any],
    parameter_importance: Optional[Dict[str, float]] = None,
    trial_history: Optional[List[Dict[str, Any]]] = None,
    export_format: Optional[str] = None,
    output_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate a comprehensive hyperparameter tuning report.
    
    Parameters
    ----------
    tuning_results : Dict[str, Any]
        Dictionary containing tuning results, should include:
        - model_type: str, type of model
        - optimization_algorithm: str, optimizer used
        - n_trials: int, number of trials run
        - best_score: float, best score achieved
        - best_params: Dict[str, Any], best parameters found
        - metric: str, optimization metric
    parameter_importance : Optional[Dict[str, float]], default=None
        Dictionary mapping parameter names to importance values
    trial_history : Optional[List[Dict[str, Any]]], default=None
        List of trials with parameters and scores
    export_format : Optional[str], default=None
        Format to export the report to. Options: 'xlsx', 'pptx'. 
        If None, no export is performed.
    output_path : Optional[str], default=None
        Path to save the exported report. Required if export_format is provided.
        
    Returns
    -------
    Dict[str, Any]
        Dictionary containing the report data
    """
    # Create report data dictionary
    report_data = {
        'model_type': tuning_results.get('model_type', 'Unknown'),
        'optimization_algorithm': tuning_results.get('optimization_algorithm', 'Unknown'),
        'n_trials': tuning_results.get('n_trials', 0),
        'best_score': tuning_results.get('best_score', 0),
        'best_params': tuning_results.get('best_params', {}),
        'metric': tuning_results.get('metric', 'Unknown'),
        'metric_direction': tuning_results.get('metric_direction', 'minimize'),
        'tuning_date': tuning_results.get('tuning_date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        'param_ranges': tuning_results.get('param_ranges', {})
    }
    
    # Add parameter importance if provided
    if parameter_importance:
        report_data['param_importance'] = parameter_importance
    
    # Add trial history if provided
    if trial_history:
        report_data['trials'] = trial_history
    
    # Generate visualizations
    visualizations = {}
    
    # Parameter importance visualization
    if parameter_importance:
        # Convert to lists and sort by importance
        params = list(parameter_importance.keys())
        importances = list(parameter_importance.values())
        
        # Sort parameters by importance
        sorted_idx = np.argsort(importances)
        top_params = [params[i] for i in sorted_idx[-10:]]  # Top 10 parameters
        top_importances = [importances[i] for i in sorted_idx[-10:]]
        
        plt.figure(figsize=(12, 8))
        plt.barh(range(len(top_params)), top_importances, align='center')
        plt.yticks(range(len(top_params)), top_params)
        plt.xlabel('Importance')
        plt.title('Parameter Importance')
        
        # Save visualization
        img_path = "param_importance.png" if not output_path else f"{os.path.splitext(output_path)[0]}_param_importance.png"
        plt.savefig(img_path)
        plt.close()
        
        visualizations['param_importance'] = img_path
    
    # Trial history visualization
    if trial_history:
        # Extract trial scores and parameters
        trial_numbers = list(range(1, len(trial_history) + 1))
        trial_scores = [trial.get('value', None) for trial in trial_history]
        
        if None not in trial_scores:
            plt.figure(figsize=(12, 6))
            plt.plot(trial_numbers, trial_scores, 'o-')
            
            # Add best score as horizontal line
            best_score = min(trial_scores) if report_data['metric_direction'] == 'minimize' else max(trial_scores)
            plt.axhline(y=best_score, color='r', linestyle='--', label=f'Best Score: {best_score:.4f}')
            
            plt.xlabel('Trial Number')
            plt.ylabel(report_data['metric'])
            plt.title('Optimization Progress')
            plt.legend()
            plt.grid(True)
            
            # Save visualization
            img_path = "optimization_progress.png" if not output_path else f"{os.path.splitext(output_path)[0]}_optimization_progress.png"
            plt.savefig(img_path)
            plt.close()
            
            visualizations['optimization_progress'] = img_path
    
    # Add visualizations to report data
    report_data['visualizations'] = visualizations
    
    # Handle export if requested
    if export_format and output_path:
        if export_format.lower() == 'xlsx':
            export_to_excel(report_data, output_path, report_type="hyperparameter")
            print(f"Excel report exported to {output_path}")
        elif export_format.lower() == 'pptx':
            export_to_powerpoint(report_data, output_path, report_type="hyperparameter")
            print(f"PowerPoint report exported to {output_path}")
        else:
            print(f"Unsupported export format: {export_format}")
    
    return report_data