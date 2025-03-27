"""
Tests for the simplified EDA report generation module.
"""
import pytest
import pandas as pd
import numpy as np
from freamon.eda.simple_report import generate_simple_eda_report

class TestSimpleEDAReport:
    """Test case for the simplified EDA report generator."""
    
    @pytest.fixture
    def sample_data(self):
        """Create a sample dataset for testing."""
        np.random.seed(42)
        df = pd.DataFrame({
            'numeric_1': np.random.normal(0, 1, 100),
            'numeric_2': np.random.uniform(0, 100, 100),
            'categorical_1': np.random.choice(['A', 'B', 'C'], 100),
            'categorical_2': np.random.choice(['X', 'Y', 'Z', 'W'], 100),
            'text': [
                "This is a longer text example that contains multiple words and should be analyzed as text." 
                + " It might contain keywords like data, science, and analysis " * np.random.randint(1, 5)
                for _ in range(100)
            ],
            'date': pd.date_range(start='2023-01-01', periods=100, freq='D'),
            'target_numeric': np.random.normal(50, 10, 100),
            'target_categorical': np.random.choice(['Low', 'Medium', 'High'], 100)
        })
        return df
    
    def test_report_generation_numeric_target(self, sample_data):
        """Test report generation with numeric target."""
        report = generate_simple_eda_report(
            df=sample_data,
            target_column='target_numeric',
            return_html=False
        )
        
        # Check that the report is a string
        assert isinstance(report, str)
        
        # Check that the report contains expected sections
        assert "# Exploratory Data Analysis Report" in report
        assert "## Dataset Overview" in report
        assert "## Numeric Analysis" in report
        assert "## Text Analysis" in report
        assert "## Categorical Analysis" in report
        assert "## Datetime Analysis" in report
        
        # Check that target relationship analysis is included
        assert "Relationship with target_numeric" in report
    
    def test_report_generation_categorical_target(self, sample_data):
        """Test report generation with categorical target."""
        report = generate_simple_eda_report(
            df=sample_data,
            target_column='target_categorical',
            return_html=False
        )
        
        # Check that the report contains categorical target analysis
        assert "Relationship with target_categorical" in report
    
    def test_html_report_generation(self, sample_data):
        """Test HTML report generation."""
        html_report = generate_simple_eda_report(
            df=sample_data,
            target_column='target_numeric',
            return_html=True
        )
        
        # Check that HTML report is a string
        assert isinstance(html_report, str)
        
        # Check that it contains HTML elements
        assert "<!DOCTYPE html>" in html_report
        assert "<html>" in html_report
        assert "<head>" in html_report
        assert "<body>" in html_report
    
    def test_custom_column_selection(self, sample_data):
        """Test report generation with custom column selections."""
        report = generate_simple_eda_report(
            df=sample_data,
            target_column='target_numeric',
            text_columns=['text'],
            categorical_columns=['categorical_1'],
            numeric_columns=['numeric_1'],
            datetime_columns=['date'],
            return_html=False
        )
        
        # Check that only specified columns are analyzed
        assert "numeric_1" in report
        assert "numeric_2" not in report
        assert "categorical_1" in report
        assert "categorical_2" not in report
    
    def test_sampling_parameter(self, sample_data):
        """Test sampling parameter."""
        # Create a large dataframe that should trigger sampling
        large_df = pd.concat([sample_data] * 20, ignore_index=True)
        
        report = generate_simple_eda_report(
            df=large_df,
            sampling_threshold=100,  # Set low to trigger sampling
            sampling_size=50,
            return_html=False
        )
        
        # Check that sampling note is included
        assert "sampled rows" in report.lower()
    
    def test_max_categories_parameter(self, sample_data):
        """Test max_categories parameter."""
        # Create a dataset with many categories
        many_cats = pd.DataFrame({
            'many_categories': np.random.choice(list('ABCDEFGHIJKLMNOPQRST'), 100),
            'numeric': np.random.normal(0, 1, 100)
        })
        
        report = generate_simple_eda_report(
            df=many_cats,
            max_categories=5,
            return_html=False
        )
        
        # Check that the report mentions showing only top categories
        assert "top 5 categories" in report.lower()
    
    def test_fig_size_parameter(self, sample_data):
        """Test figure size parameter working (not a visual test)."""
        # This just tests that the parameter is accepted and doesn't cause errors
        report = generate_simple_eda_report(
            df=sample_data,
            figsize=(8, 4),
            return_html=False
        )
        
        assert isinstance(report, str)