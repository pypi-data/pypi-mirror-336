"""
Tests for the evaluation module in the deduplication package.
"""

import unittest
import pandas as pd
import numpy as np
import os
from freamon.deduplication.evaluation import (
    calculate_deduplication_metrics,
    plot_confusion_matrix,
    evaluate_threshold_sensitivity,
    generate_evaluation_report,
    flag_and_evaluate
)


class TestDeduplicationEvaluation(unittest.TestCase):
    """Test the deduplication evaluation functionality."""
    
    def setUp(self):
        """Set up test data with known duplicates."""
        # Create a small dataframe with known duplicate flags
        self.df = pd.DataFrame({
            'id': [1, 2, 3, 4, 5, 6, 7, 8],
            'text': [
                "The quick brown fox jumps over the lazy dog",
                "The quick brown fox jumps over the sleeping dog",
                "A completely different sentence with no similarity",
                "Another unique sentence with no duplicates",
                "The quick brown fox jumps over the lazy dog.",
                "The fast brown fox leaps over the lazy dog",
                "A sentence with unique content",
                "The speedy brown fox jumps over the lazy canine"
            ],
            'is_known_duplicate': [False, False, False, False, True, True, False, True],
            'is_predicted_duplicate': [False, False, False, False, True, False, False, True]
        })
    
    def test_calculate_deduplication_metrics(self):
        """Test calculation of deduplication metrics."""
        metrics = calculate_deduplication_metrics(
            df=self.df,
            prediction_column='is_predicted_duplicate',
            truth_column='is_known_duplicate'
        )
        
        # Check that all expected metrics are present
        expected_metrics = ['precision', 'recall', 'f1', 'accuracy', 
                           'true_positives', 'false_positives', 
                           'true_negatives', 'false_negatives']
        for metric in expected_metrics:
            self.assertIn(metric, metrics)
        
        # Check metric values
        self.assertEqual(metrics['true_positives'], 2)  # Records 5 and 8
        self.assertEqual(metrics['false_negatives'], 1)  # Record 6
        self.assertEqual(metrics['false_positives'], 0)
        self.assertEqual(metrics['true_negatives'], 5)  # Records 1, 2, 3, 4, 7
        
        # Verify precision, recall, and F1 based on the confusion matrix
        self.assertEqual(metrics['precision'], 1.0)  # 2 / (2 + 0)
        self.assertAlmostEqual(metrics['recall'], 2/3)  # 2 / (2 + 1)
        self.assertAlmostEqual(metrics['f1'], 0.8)  # 2 * (1.0 * 0.667) / (1.0 + 0.667)
    
    def test_plot_confusion_matrix(self):
        """Test confusion matrix visualization."""
        # Test as_base64 return value
        cm_base64 = plot_confusion_matrix(
            df=self.df,
            prediction_column='is_predicted_duplicate',
            truth_column='is_known_duplicate',
            as_base64=True
        )
        
        self.assertIsInstance(cm_base64, str)
        self.assertTrue(len(cm_base64) > 0)
        self.assertTrue(cm_base64.startswith('iVBOR') or cm_base64.startswith('R0lGOD'))
    
    def test_evaluate_threshold_sensitivity(self):
        """Test evaluation of threshold sensitivity."""
        # Create a function for flag_similar_records to avoid importing the actual one
        def mock_flag_similar_records(df, **kwargs):
            # Just return the dataframe with a mock flag based on threshold
            threshold = kwargs.get('threshold', 0.8)
            mock_df = df.copy()
            
            # Simulate different thresholds producing different results
            if threshold <= 0.5:
                mock_df['_predicted_duplicate'] = [False, False, False, False, True, True, False, True]
            elif threshold <= 0.7:
                mock_df['_predicted_duplicate'] = [False, False, False, False, True, True, False, False]
            else:
                mock_df['_predicted_duplicate'] = [False, False, False, False, True, False, False, False]
                
            return mock_df
        
        # Patch the import to use our mock
        import sys
        import types
        mock_module = types.ModuleType('freamon.deduplication')
        mock_module.flag_similar_records = mock_flag_similar_records
        sys.modules['freamon.deduplication'] = mock_module
        
        # Run the test
        results = evaluate_threshold_sensitivity(
            df=self.df,
            columns=['text'],
            truth_column='is_known_duplicate',
            thresholds=[0.5, 0.7, 0.9],
            show_plot=False
        )
        
        # Verify results
        self.assertIn('thresholds', results)
        self.assertIn('metrics', results)
        self.assertIn('optimal_threshold', results)
        self.assertIn('optimal_metrics', results)
        
        # Check if all thresholds have metrics
        self.assertEqual(len(results['metrics']), 3)
        
        # Cleanup
        del sys.modules['freamon.deduplication']
    
    def test_generate_evaluation_report(self):
        """Test generation of evaluation reports in different formats."""
        # Test text format
        text_report = generate_evaluation_report(
            df=self.df,
            prediction_column='is_predicted_duplicate',
            truth_column='is_known_duplicate',
            format='text',
            include_plots=False
        )
        
        self.assertIsInstance(text_report, str)
        self.assertIn('DEDUPLICATION EVALUATION REPORT', text_report)
        
        # Test markdown format
        md_report = generate_evaluation_report(
            df=self.df,
            prediction_column='is_predicted_duplicate',
            truth_column='is_known_duplicate',
            format='markdown',
            include_plots=False
        )
        
        self.assertIsInstance(md_report, str)
        self.assertIn('# Deduplication Evaluation Report', md_report)
        
        # Test HTML format
        html_report = generate_evaluation_report(
            df=self.df,
            prediction_column='is_predicted_duplicate',
            truth_column='is_known_duplicate',
            format='html',
            include_plots=False
        )
        
        self.assertIsInstance(html_report, str)
        self.assertIn('<div class="deduplication-report">', html_report)
        
        # Test invalid format
        with self.assertRaises(ValueError):
            generate_evaluation_report(
                df=self.df,
                prediction_column='is_predicted_duplicate',
                truth_column='is_known_duplicate',
                format='invalid'
            )
    
    def test_flag_and_evaluate(self):
        """Test the flag_and_evaluate function."""
        # Create a mock flag_similar_records function again
        def mock_flag_similar_records(df, **kwargs):
            # Return df with duplicates matching known duplicates but with one mistake
            mock_df = df.copy()
            mock_df['is_duplicate'] = [False, False, False, False, True, False, False, True]
            return mock_df
        
        # Patch the import
        import sys
        import types
        mock_module = types.ModuleType('freamon.deduplication')
        mock_module.flag_similar_records = mock_flag_similar_records
        sys.modules['freamon.deduplication'] = mock_module
        
        # Run the function
        result = flag_and_evaluate(
            df=self.df,
            columns=['text'],
            known_duplicate_column='is_known_duplicate',
            flag_column='is_duplicate',
            generate_report=True,
            report_format='text'
        )
        
        # Check results
        self.assertIn('dataframe', result)
        self.assertIn('metrics', result)
        self.assertIn('report', result)
        self.assertIn('confusion_matrix_base64', result)
        
        # Verify metrics
        metrics = result['metrics']
        self.assertEqual(metrics['true_positives'], 2)  # Records 5 and 8
        self.assertEqual(metrics['false_negatives'], 1)  # Record 6
        self.assertEqual(metrics['false_positives'], 0)
        
        # Cleanup
        del sys.modules['freamon.deduplication']


if __name__ == '__main__':
    unittest.main()