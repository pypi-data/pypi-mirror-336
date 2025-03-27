"""
Module for generating simplified EDA reports with enhanced text analysis,
category visualization, and target relationships.

This module provides a streamlined approach to exploratory data analysis
with a focus on producing clean, information-dense reports suitable for
Jupyter notebooks and data scientists who want quick insights.
"""
import base64
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Any, Dict, List, Optional, Union, Tuple
from datetime import datetime
from scipy import stats
from freamon.utils.datatype_detector import DataTypeDetector
from freamon.utils.matplotlib_fixes import configure_matplotlib_for_currency
from freamon.utils.text_utils import TextProcessor, create_topic_model_optimized
from freamon.eda.export import export_to_excel, export_to_powerpoint

# Configure matplotlib for better display
configure_matplotlib_for_currency()
plt.style.use('seaborn-v0_8-whitegrid')


def generate_simple_eda_report(
    df: pd.DataFrame,
    target_column: Optional[str] = None,
    text_columns: Optional[List[str]] = None,
    categorical_columns: Optional[List[str]] = None,
    numeric_columns: Optional[List[str]] = None,
    datetime_columns: Optional[List[str]] = None,
    max_categories: int = 10,
    max_correlations: int = 15,
    sampling_threshold: int = 10000,
    sampling_size: int = 5000,
    figsize: Tuple[int, int] = (10, 6),
    return_html: bool = True,
    export_format: Optional[str] = None,
    output_path: Optional[str] = None,
    include_topic_modeling: bool = False,
    topic_modeling_params: Optional[Dict[str, Any]] = None
) -> str:
    """
    Generate a simplified EDA report with enhanced text visualization and target relationships.
    
    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to analyze
    target_column : Optional[str], default=None
        The target column for supervised analyses
    text_columns : Optional[List[str]], default=None
        List of text columns to analyze; if None, will attempt to detect
    categorical_columns : Optional[List[str]], default=None
        List of categorical columns to analyze; if None, will attempt to detect
    numeric_columns : Optional[List[str]], default=None
        List of numeric columns to analyze; if None, will attempt to detect
    datetime_columns : Optional[List[str]], default=None
        List of datetime columns to analyze; if None, will attempt to detect
    max_categories : int, default=10
        Maximum number of categories to display in categorical analysis
    max_correlations : int, default=15
        Maximum number of correlations to display
    sampling_threshold : int, default=10000
        Threshold for applying sampling to large datasets
    sampling_size : int, default=5000
        Number of samples to use if sampling is applied
    figsize : Tuple[int, int], default=(10, 6)
        Default figure size for plots
    return_html : bool, default=True
        Whether to return HTML (True) or Markdown (False)
    export_format : Optional[str], default=None
        Format to export the report to. Options: 'xlsx', 'pptx'. 
        If None, no export is performed.
    output_path : Optional[str], default=None
        Path to save the exported report. Required if export_format is provided.
    include_topic_modeling : bool, default=False
        Whether to include topic modeling analysis for text columns
    topic_modeling_params : Optional[Dict[str, Any]], default=None
        Parameters for topic modeling. If None, default parameters are used.
        
    Returns
    -------
    str
        HTML or Markdown report
    """
    # Apply sampling if needed
    sampling_applied = False
    if len(df) > sampling_threshold:
        df_sample = df.sample(sampling_size, random_state=42)
        sampling_applied = True
    else:
        df_sample = df
    
    # Auto-detect column types if not provided
    detector = DataTypeDetector(df)
    detected_types = detector.detect_all_types()
    
    if numeric_columns is None:
        numeric_columns = [col for col, info in detected_types.items()
                          if info.get('logical_type') in 
                          ['integer', 'float', 'continuous_integer', 'continuous_float']]
    
    if categorical_columns is None:
        categorical_columns = [col for col, info in detected_types.items()
                            if info.get('logical_type') in 
                            ['categorical', 'categorical_integer', 'boolean', 'string']]
    
    if datetime_columns is None:
        datetime_columns = [col for col, info in detected_types.items()
                          if info.get('logical_type') in ['datetime']]
    
    # Detect text columns if not provided
    if text_columns is None:
        text_columns = []
        for col in df.columns:
            if col in categorical_columns and df[col].dtype == 'object':
                # Check if column contains longer text by checking mean length
                if df[col].astype(str).str.len().mean() > 20:
                    text_columns.append(col)
    
    # Start building the report
    report_parts = []
    
    # Title section
    report_parts.append("# Exploratory Data Analysis Report")
    report_parts.append(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_parts.append("")
    
    # Info alert for sampling
    if sampling_applied:
        report_parts.append(f"> **Note:** Analysis performed on {sampling_size:,} sampled rows from a total of {len(df):,} rows")
    report_parts.append("")
    
    # Dataset overview section
    report_parts.append("## Dataset Overview")
    report_parts.append("")
    
    # Basic statistics table
    report_parts.append("### Basic Statistics")
    report_parts.append("")
    report_parts.append("| Metric | Value |")
    report_parts.append("|--------|-------|")
    report_parts.append(f"| Rows | {len(df):,} |")
    report_parts.append(f"| Columns | {len(df.columns):,} |")
    report_parts.append(f"| Numeric Columns | {len(numeric_columns):,} |")
    report_parts.append(f"| Categorical Columns | {len(categorical_columns):,} |")
    report_parts.append(f"| Text Columns | {len(text_columns):,} |")
    report_parts.append(f"| Datetime Columns | {len(datetime_columns):,} |")
    report_parts.append(f"| Missing Values | {df.isna().sum().sum():,} ({df.isna().sum().sum() / (df.shape[0] * df.shape[1]) * 100:.2f}%) |")
    report_parts.append("")
    
    # Missing values visualization
    if df.isna().sum().sum() > 0:
        report_parts.append("### Missing Values")
        report_parts.append("")
        
        # Create missing values heatmap
        plt.figure(figsize=(figsize[0], min(figsize[1], max(3, len(df.columns) * 0.3))))
        cols_with_missing = df.columns[df.isna().any()].tolist()
        missing_data = df[cols_with_missing].isna()
        
        # Only show if there are not too many columns with missing values
        if len(cols_with_missing) <= 30:
            sns.heatmap(missing_data, cmap='viridis', cbar=False, yticklabels=False)
            plt.title('Missing Values Heatmap')
            plt.tight_layout()
            
            # Convert plot to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            img_str = base64.b64encode(buffer.read()).decode('utf-8')
            plt.close()
            
            report_parts.append(f"![Missing Values Heatmap](data:image/png;base64,{img_str})")
            report_parts.append("")
        
        # Missing values by column
        cols_with_missing_pct = df.isna().mean().sort_values(ascending=False)
        cols_with_missing_pct = cols_with_missing_pct[cols_with_missing_pct > 0]
        
        report_parts.append("#### Columns with Missing Values")
        report_parts.append("")
        report_parts.append("| Column | Missing Count | Missing % |")
        report_parts.append("|--------|--------------|-----------|")
        
        for col, pct in cols_with_missing_pct.items():
            count = df[col].isna().sum()
            report_parts.append(f"| {col} | {count:,} | {pct*100:.2f}% |")
        
        report_parts.append("")
        
        # Missingness correlation analysis - identify patterns in missing values
        if len(cols_with_missing) >= 2:
            report_parts.append("#### Missing Value Correlation")
            report_parts.append("")
            report_parts.append("This analysis shows which columns tend to have missing values in the same rows:")
            report_parts.append("")
            
            # Calculate correlation matrix of missing indicators
            missing_corr = missing_data.corr()
            
            # Create a heatmap for missingness correlation
            plt.figure(figsize=figsize)
            mask = np.triu(np.ones_like(missing_corr, dtype=bool))
            sns.heatmap(missing_corr, mask=mask, annot=len(cols_with_missing) < 10, 
                      fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, cbar=True,
                      linewidths=0.5)
            plt.title('Missing Value Correlation')
            plt.tight_layout()
            
            # Convert plot to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            img_str = base64.b64encode(buffer.read()).decode('utf-8')
            plt.close()
            
            report_parts.append(f"![Missing Value Correlation](data:image/png;base64,{img_str})")
            report_parts.append("")
            
            # Show top missing value correlations
            missing_corr_pairs = []
            for i in range(len(cols_with_missing)):
                for j in range(i+1, len(cols_with_missing)):
                    col1 = cols_with_missing[i]
                    col2 = cols_with_missing[j]
                    corr = missing_corr.loc[col1, col2]
                    if not np.isnan(corr):
                        missing_corr_pairs.append((col1, col2, corr))
            
            # Only show if there are meaningful correlations
            if missing_corr_pairs:
                # Sort by absolute correlation value
                missing_corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
                
                report_parts.append("Top correlated missing values (columns that tend to be missing together):")
                report_parts.append("")
                report_parts.append("| Column 1 | Column 2 | Correlation |")
                report_parts.append("|----------|----------|-------------|")
                
                # Show top 10 or fewer, focusing on meaningful correlations
                for col1, col2, corr in missing_corr_pairs[:min(10, len(missing_corr_pairs))]:
                    if abs(corr) > 0.1:  # Only show meaningful correlations
                        report_parts.append(f"| {col1} | {col2} | {corr:.3f} |")
                        
                        # Add interpretation for strong correlations
                        if abs(corr) > 0.7:
                            if corr > 0:
                                report_parts.append(f"> **Strong positive correlation**: When {col1} is missing, {col2} is very likely to be missing too")
                            else:
                                report_parts.append(f"> **Strong negative correlation**: When {col1} is missing, {col2} is very likely to be present")
                
                report_parts.append("")
    
    # Sample data preview
    report_parts.append("### Sample Data")
    report_parts.append("")
    
    # Convert sample of DataFrame to markdown table
    sample_df = df.head(5)
    header = "| |"
    for col in sample_df.columns:
        header += f" {col} |"
    report_parts.append(header)
    
    separator = "|---|"
    for _ in range(len(sample_df.columns)):
        separator += "---|"
    report_parts.append(separator)
    
    for idx, row in sample_df.iterrows():
        row_str = f"| {idx} |"
        for val in row:
            # Format different data types appropriately
            if pd.isna(val):
                cell = " NaN |"
            elif isinstance(val, (int, np.integer)):
                cell = f" {val:,} |"
            elif isinstance(val, (float, np.floating)):
                cell = f" {val:.4f} |"
            elif isinstance(val, str) and len(val) > 50:
                cell = f" {val[:47]}... |"
            else:
                cell = f" {val} |"
            row_str += cell
        report_parts.append(row_str)
    
    report_parts.append("")
    
    # Datatype overview visualization
    report_parts.append("### Data Type Distribution")
    report_parts.append("")
    
    # Create data type distribution chart
    dtype_counts = {
        'Numeric': len(numeric_columns),
        'Categorical': len([c for c in categorical_columns if c not in text_columns]),
        'Text': len(text_columns),
        'Datetime': len(datetime_columns)
    }
    
    # Filter out zero counts
    dtype_counts = {k: v for k, v in dtype_counts.items() if v > 0}
    
    plt.figure(figsize=figsize)
    bars = plt.bar(dtype_counts.keys(), dtype_counts.values(), color=sns.color_palette("viridis", len(dtype_counts)))
    plt.title('Column Data Type Distribution')
    plt.ylabel('Count')
    
    # Add count labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height:,}', ha='center')
    
    plt.tight_layout()
    
    # Convert plot to base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()
    
    report_parts.append(f"![Data Type Distribution](data:image/png;base64,{img_str})")
    report_parts.append("")
    
    # Text Column Analysis
    if text_columns:
        report_parts.append("## Text Analysis")
        report_parts.append("")
        report_parts.append("Analysis of text columns including statistics, word counts, and common terms.")
        report_parts.append("")
        
        # Initialize text processor
        text_processor = TextProcessor()
        
        for col in text_columns:
            report_parts.append(f"### {col}")
            report_parts.append("")
            
            # Filter out null values
            text_data = df_sample[col].dropna().astype(str)
            
            # Calculate basic text statistics
            char_count = text_data.str.len()
            word_count = text_data.str.split().str.len()
            
            report_parts.append("#### Text Statistics")
            report_parts.append("")
            report_parts.append("| Metric | Value |")
            report_parts.append("|--------|-------|")
            report_parts.append(f"| Non-null Count | {df[col].count():,} ({df[col].count() / len(df) * 100:.1f}%) |")
            report_parts.append(f"| Unique Values | {df[col].nunique():,} |")
            report_parts.append(f"| Mean Character Length | {char_count.mean():.1f} |")
            report_parts.append(f"| Mean Word Count | {word_count.mean():.1f} |")
            report_parts.append(f"| Min Length | {char_count.min()} |")
            report_parts.append(f"| Max Length | {char_count.max()} |")
            report_parts.append("")
            
            # Extract and display top keywords
            all_text = ' '.join(text_data.tolist())
            keywords = text_processor.extract_keywords_rake(all_text, max_keywords=10)
            
            if keywords:
                report_parts.append("#### Top Keywords")
                report_parts.append("")
                report_parts.append("| Keyword | Score |")
                report_parts.append("|---------|-------|")
                
                for keyword, score in keywords:
                    report_parts.append(f"| {keyword} | {score:.3f} |")
                
                report_parts.append("")
            
            # Length distribution visualization
            plt.figure(figsize=figsize)
            sns.histplot(word_count, kde=True)
            plt.title(f'Word Count Distribution for {col}')
            plt.xlabel('Word Count')
            plt.ylabel('Frequency')
            plt.tight_layout()
            
            # Convert plot to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            img_str = base64.b64encode(buffer.read()).decode('utf-8')
            plt.close()
            
            report_parts.append("#### Word Count Distribution")
            report_parts.append("")
            report_parts.append(f"![Word Count Distribution](data:image/png;base64,{img_str})")
            report_parts.append("")
            
            # If target column is provided, analyze relationship with text column
            if target_column and target_column != col:
                report_parts.append(f"#### Relationship with {target_column}")
                report_parts.append("")
                
                if target_column in categorical_columns:
                    # For categorical target, show word count by category
                    plt.figure(figsize=figsize)
                    target_groups = df_sample.groupby(target_column)[col].apply(
                        lambda x: x.str.split().str.len().mean()).sort_values(ascending=False)
                    
                    sns.barplot(x=target_groups.index, y=target_groups.values)
                    plt.title(f'Average Word Count by {target_column}')
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    
                    # Convert plot to base64
                    buffer = io.BytesIO()
                    plt.savefig(buffer, format='png')
                    buffer.seek(0)
                    img_str = base64.b64encode(buffer.read()).decode('utf-8')
                    plt.close()
                    
                    report_parts.append(f"![Word Count by Target](data:image/png;base64,{img_str})")
                    report_parts.append("")
                
                elif target_column in numeric_columns:
                    # For numeric target, show correlation with word count
                    word_counts = df_sample[col].fillna('').astype(str).str.split().str.len()
                    corr = word_counts.corr(df_sample[target_column])
                    
                    report_parts.append(f"Correlation between word count and {target_column}: **{corr:.3f}**")
                    report_parts.append("")
                    
                    # Create scatter plot
                    plt.figure(figsize=figsize)
                    plt.scatter(word_counts, df_sample[target_column], alpha=0.5)
                    plt.title(f'Word Count vs {target_column}')
                    plt.xlabel('Word Count')
                    plt.ylabel(target_column)
                    plt.tight_layout()
                    
                    # Convert plot to base64
                    buffer = io.BytesIO()
                    plt.savefig(buffer, format='png')
                    buffer.seek(0)
                    img_str = base64.b64encode(buffer.read()).decode('utf-8')
                    plt.close()
                    
                    report_parts.append(f"![Word Count vs Target](data:image/png;base64,{img_str})")
                    report_parts.append("")
    
    # Categorical Analysis
    if categorical_columns:
        report_parts.append("## Categorical Analysis")
        report_parts.append("")
        report_parts.append("Analysis of categorical variables including frequency distribution and target relationships.")
        report_parts.append("")
        
        # Analyze each categorical column
        for col in categorical_columns:
            # Skip if it's already analyzed as text
            if col in text_columns:
                continue
                
            report_parts.append(f"### {col}")
            report_parts.append("")
            
            # Calculate value counts
            val_counts = df[col].value_counts()
            val_pcts = df[col].value_counts(normalize=True)
            
            # Basic statistics
            report_parts.append("#### Statistics")
            report_parts.append("")
            report_parts.append("| Metric | Value |")
            report_parts.append("|--------|-------|")
            report_parts.append(f"| Non-null Count | {df[col].count():,} ({df[col].count() / len(df) * 100:.1f}%) |")
            report_parts.append(f"| Unique Values | {df[col].nunique():,} |")
            report_parts.append(f"| Mode | {df[col].mode().iloc[0] if not df[col].mode().empty else 'N/A'} |")
            report_parts.append(f"| Most Common Value | {val_counts.index[0] if not val_counts.empty else 'N/A'} ({val_pcts.iloc[0]*100:.1f}%) |")
            report_parts.append("")
            
            # Show top N categories visualization
            plt.figure(figsize=figsize)
            
            # If too many categories, limit to top N
            if val_counts.shape[0] > max_categories:
                top_n = val_counts.head(max_categories)
                other_count = val_counts.iloc[max_categories:].sum()
                
                # Create a new series with 'Other' category
                plot_data = pd.concat([top_n, pd.Series({'Other': other_count})])
                
                # Note about grouping
                report_parts.append(f"> Showing top {max_categories} categories. Other {val_counts.shape[0] - max_categories:,} categories grouped as 'Other'.")
                report_parts.append("")
            else:
                plot_data = val_counts
            
            # Plot categories
            sns.barplot(x=plot_data.index, y=plot_data.values)
            plt.title(f'Value Distribution for {col}')
            plt.xticks(rotation=45, ha='right')
            plt.ylabel('Count')
            plt.tight_layout()
            
            # Convert plot to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            img_str = base64.b64encode(buffer.read()).decode('utf-8')
            plt.close()
            
            report_parts.append("#### Value Distribution")
            report_parts.append("")
            report_parts.append(f"![Value Distribution](data:image/png;base64,{img_str})")
            report_parts.append("")
            
            # If target column is provided, analyze relationship
            if target_column and target_column != col:
                report_parts.append(f"#### Relationship with {target_column}")
                report_parts.append("")
                
                if target_column in categorical_columns:
                    # For categorical vs categorical, calculate chi-squared
                    contingency = pd.crosstab(df_sample[col], df_sample[target_column])
                    chi2, p, dof, expected = stats.chi2_contingency(contingency)
                    
                    report_parts.append(f"Chi-squared test p-value: **{p:.3f}**")
                    if p < 0.05:
                        report_parts.append("> Statistically significant relationship detected (p < 0.05)")
                    else:
                        report_parts.append("> No statistically significant relationship detected (p >= 0.05)")
                    report_parts.append("")
                    
                    # Stacked bar chart for relationship visualization
                    plt.figure(figsize=figsize)
                    contingency_pct = contingency.div(contingency.sum(axis=1), axis=0)
                    contingency_pct.plot(kind='bar', stacked=True)
                    plt.title(f'Relationship between {col} and {target_column}')
                    plt.xlabel(col)
                    plt.ylabel('Proportion')
                    plt.legend(title=target_column)
                    plt.tight_layout()
                    
                    # Convert plot to base64
                    buffer = io.BytesIO()
                    plt.savefig(buffer, format='png')
                    buffer.seek(0)
                    img_str = base64.b64encode(buffer.read()).decode('utf-8')
                    plt.close()
                    
                    report_parts.append(f"![Category Relationship](data:image/png;base64,{img_str})")
                    report_parts.append("")
                    
                elif target_column in numeric_columns:
                    # For categorical vs numeric, calculate ANOVA
                    groups = df_sample.groupby(col)[target_column].apply(list)
                    
                    # Try ANOVA if there are at least two non-empty groups
                    valid_groups = [g for g in groups if len(g) > 0]
                    if len(valid_groups) >= 2:
                        try:
                            f_val, p_val = stats.f_oneway(*valid_groups)
                            report_parts.append(f"ANOVA test p-value: **{p_val:.3f}**")
                            if p_val < 0.05:
                                report_parts.append("> Statistically significant relationship detected (p < 0.05)")
                            else:
                                report_parts.append("> No statistically significant relationship detected (p >= 0.05)")
                        except:
                            report_parts.append("> Could not perform ANOVA test (possibly due to data constraints)")
                    else:
                        report_parts.append("> Insufficient data for ANOVA test")
                    
                    report_parts.append("")
                    
                    # Boxplot for relationship visualization
                    plt.figure(figsize=figsize)
                    sns.boxplot(x=col, y=target_column, data=df_sample)
                    plt.title(f'{col} vs {target_column}')
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    
                    # Convert plot to base64
                    buffer = io.BytesIO()
                    plt.savefig(buffer, format='png')
                    buffer.seek(0)
                    img_str = base64.b64encode(buffer.read()).decode('utf-8')
                    plt.close()
                    
                    report_parts.append(f"![Category vs Numeric](data:image/png;base64,{img_str})")
                    report_parts.append("")
    
    # Numeric Analysis
    if numeric_columns:
        report_parts.append("## Numeric Analysis")
        report_parts.append("")
        report_parts.append("Analysis of numeric variables including distribution, statistics, and correlations.")
        report_parts.append("")
        
        # Compute correlation matrix for all numeric columns
        numeric_df = df_sample[numeric_columns].copy()
        correlation = numeric_df.corr()
        
        # Correlation heatmap
        if len(numeric_columns) > 1:
            plt.figure(figsize=figsize)
            mask = np.triu(np.ones_like(correlation, dtype=bool))
            
            # Use a diverging colormap to better visualize negative and positive correlations
            sns.heatmap(correlation, mask=mask, annot=len(numeric_columns) < 10, 
                       fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, cbar=True,
                       linewidths=0.5)
            plt.title('Correlation Heatmap')
            plt.tight_layout()
            
            # Convert plot to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            img_str = base64.b64encode(buffer.read()).decode('utf-8')
            plt.close()
            
            report_parts.append("### Correlation Heatmap")
            report_parts.append("")
            report_parts.append(f"![Correlation Heatmap](data:image/png;base64,{img_str})")
            report_parts.append("")
            
            # Find highly correlated features
            high_corr_threshold = 0.7
            high_corr_features = []
            multi_collinear_groups = {}
            
            # Get upper triangle of correlation matrix
            corr_mat = correlation.where(~mask)
            corr_pairs = []
            
            for col1 in corr_mat.columns:
                for col2 in corr_mat.columns:
                    if col1 != col2:
                        corr_value = corr_mat.loc[col1, col2]
                        if not np.isnan(corr_value):
                            corr_pairs.append((col1, col2, corr_value))
                            
                            # Track highly correlated pairs
                            if abs(corr_value) >= high_corr_threshold:
                                pair = tuple(sorted([col1, col2]))
                                if pair not in high_corr_features:
                                    high_corr_features.append(pair)
                                
                                # Track groups of collinear features
                                found = False
                                for group_id, group in multi_collinear_groups.items():
                                    if col1 in group or col2 in group:
                                        group.update([col1, col2])
                                        found = True
                                        break
                                
                                if not found:
                                    group_id = len(multi_collinear_groups) + 1
                                    multi_collinear_groups[group_id] = {col1, col2}
            
            # Sort by absolute correlation (descending)
            corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
            
            # Display top correlations
            report_parts.append("### Top Correlations")
            report_parts.append("")
            report_parts.append("| Variable 1 | Variable 2 | Correlation | Interpretation |")
            report_parts.append("|-----------|-----------|-------------|----------------|")
            
            for col1, col2, corr_value in corr_pairs[:min(max_correlations, len(corr_pairs))]:
                # Add interpretation column
                if abs(corr_value) >= 0.8:
                    interp = "Very strong"
                elif abs(corr_value) >= 0.6:
                    interp = "Strong"
                elif abs(corr_value) >= 0.4:
                    interp = "Moderate"
                elif abs(corr_value) >= 0.2:
                    interp = "Weak"
                else:
                    interp = "Very weak"
                
                # Add direction
                if corr_value > 0:
                    interp += " positive"
                else:
                    interp += " negative"
                
                report_parts.append(f"| {col1} | {col2} | {corr_value:.3f} | {interp} |")
            
            report_parts.append("")
            
            # If multicollinearity is detected, add a special section
            if high_corr_features:
                report_parts.append("### Multicollinearity Analysis")
                report_parts.append("")
                report_parts.append("> **Multicollinearity detected**: The following feature groups are highly correlated (|correlation| ≥ 0.7)")
                report_parts.append("This may affect model stability and interpretation. Consider dimensionality reduction or feature selection.")
                report_parts.append("")
                
                # Display collinear groups if they exist
                if multi_collinear_groups:
                    for group_id, group in multi_collinear_groups.items():
                        if len(group) > 2:  # Only show actual groups, not just pairs
                            report_parts.append(f"**Group {group_id}**: {', '.join(sorted(group))}")
                    report_parts.append("")
                
                # Create a network visualization of highly correlated features
                if len(high_corr_features) > 0:
                    try:
                        import networkx as nx
                        
                        # Create graph
                        G = nx.Graph()
                        
                        # Add nodes
                        nodes = set()
                        for col1, col2 in high_corr_features:
                            nodes.add(col1)
                            nodes.add(col2)
                        
                        for node in nodes:
                            G.add_node(node)
                        
                        # Add edges with correlation as weight
                        for col1, col2 in high_corr_features:
                            corr = abs(correlation.loc[col1, col2])
                            G.add_edge(col1, col2, weight=corr)
                        
                        # Create visualization
                        plt.figure(figsize=figsize)
                        pos = nx.spring_layout(G, seed=42)
                        
                        # Draw the graph
                        nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
                        
                        # Draw edges with width based on correlation
                        edge_weights = [G[u][v]['weight'] * 3 for u, v in G.edges()]
                        nx.draw_networkx_edges(G, pos, width=edge_weights, alpha=0.7, edge_color='darkblue')
                        
                        # Draw labels
                        nx.draw_networkx_labels(G, pos, font_size=10)
                        
                        plt.title('Highly Correlated Features Network')
                        plt.axis('off')
                        plt.tight_layout()
                        
                        # Convert plot to base64
                        buffer = io.BytesIO()
                        plt.savefig(buffer, format='png')
                        buffer.seek(0)
                        img_str = base64.b64encode(buffer.read()).decode('utf-8')
                        plt.close()
                        
                        report_parts.append(f"![Correlation Network](data:image/png;base64,{img_str})")
                        report_parts.append("")
                    except ImportError:
                        # If networkx is not available, show a simple list of correlated pairs
                        report_parts.append("**Highly correlated pairs:**")
                        report_parts.append("")
                        for col1, col2 in high_corr_features:
                            corr = correlation.loc[col1, col2]
                            report_parts.append(f"- {col1} and {col2}: {corr:.3f}")
                        report_parts.append("")
            
            report_parts.append("")
        
        # Analyze each numeric column
        for col in numeric_columns:
            report_parts.append(f"### {col}")
            report_parts.append("")
            
            # Calculate statistics
            stats_dict = df[col].describe()
            
            report_parts.append("#### Statistics")
            report_parts.append("")
            report_parts.append("| Metric | Value |")
            report_parts.append("|--------|-------|")
            report_parts.append(f"| Count | {stats_dict['count']:,} |")
            report_parts.append(f"| Mean | {stats_dict['mean']:.4f} |")
            report_parts.append(f"| Std. Dev. | {stats_dict['std']:.4f} |")
            report_parts.append(f"| Min | {stats_dict['min']:.4f} |")
            report_parts.append(f"| 25% | {stats_dict['25%']:.4f} |")
            report_parts.append(f"| Median | {stats_dict['50%']:.4f} |")
            report_parts.append(f"| 75% | {stats_dict['75%']:.4f} |")
            report_parts.append(f"| Max | {stats_dict['max']:.4f} |")
            report_parts.append(f"| Range | {stats_dict['max'] - stats_dict['min']:.4f} |")
            
            # Calculate skewness and kurtosis if data allows
            if df[col].count() > 2:
                skewness = df[col].skew()
                kurtosis = df[col].kurtosis()
                report_parts.append(f"| Skewness | {skewness:.4f} |")
                report_parts.append(f"| Kurtosis | {kurtosis:.4f} |")
            
            report_parts.append("")
            
            # Distribution plot
            plt.figure(figsize=figsize)
            sns.histplot(df_sample[col], kde=True)
            plt.title(f'Distribution of {col}')
            plt.xlabel(col)
            plt.ylabel('Frequency')
            plt.tight_layout()
            
            # Convert plot to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            img_str = base64.b64encode(buffer.read()).decode('utf-8')
            plt.close()
            
            report_parts.append("#### Distribution")
            report_parts.append("")
            report_parts.append(f"![Distribution](data:image/png;base64,{img_str})")
            report_parts.append("")
            
            # If target column is provided, analyze relationship
            if target_column and target_column != col:
                report_parts.append(f"#### Relationship with {target_column}")
                report_parts.append("")
                
                if target_column in numeric_columns:
                    # For numeric vs numeric, calculate correlation
                    corr_value = df_sample[col].corr(df_sample[target_column])
                    report_parts.append(f"Pearson correlation: **{corr_value:.3f}**")
                    
                    # Classify the strength of correlation
                    if abs(corr_value) > 0.7:
                        report_parts.append("> Strong correlation")
                    elif abs(corr_value) > 0.3:
                        report_parts.append("> Moderate correlation")
                    else:
                        report_parts.append("> Weak correlation")
                    
                    report_parts.append("")
                    
                    # Scatter plot
                    plt.figure(figsize=figsize)
                    sns.regplot(x=col, y=target_column, data=df_sample, line_kws={"color":"red"})
                    plt.title(f'{col} vs {target_column}')
                    plt.tight_layout()
                    
                    # Convert plot to base64
                    buffer = io.BytesIO()
                    plt.savefig(buffer, format='png')
                    buffer.seek(0)
                    img_str = base64.b64encode(buffer.read()).decode('utf-8')
                    plt.close()
                    
                    report_parts.append(f"![Scatter Plot](data:image/png;base64,{img_str})")
                    report_parts.append("")
                    
                elif target_column in categorical_columns:
                    # Calculate R-squared or ANOVA
                    categories = df_sample[target_column].dropna().unique()
                    
                    if len(categories) > 1:
                        groups = df_sample.groupby(target_column)[col].apply(list)
                        valid_groups = [g for g in groups if len(g) > 0]
                        
                        if len(valid_groups) >= 2:
                            try:
                                f_val, p_val = stats.f_oneway(*valid_groups)
                                report_parts.append(f"ANOVA test p-value: **{p_val:.3f}**")
                                
                                # Calculate eta-squared (effect size)
                                dfb = len(categories) - 1  # degrees of freedom between groups
                                dfw = df_sample[col].count() - len(categories)  # degrees of freedom within groups
                                eta_sq = (dfb * f_val) / (dfb * f_val + dfw)
                                
                                report_parts.append(f"Eta-squared (effect size): **{eta_sq:.3f}**")
                                
                                if p_val < 0.05:
                                    report_parts.append("> Statistically significant relationship detected (p < 0.05)")
                                    
                                    # Interpret effect size
                                    if eta_sq > 0.14:
                                        report_parts.append("> Large effect size")
                                    elif eta_sq > 0.06:
                                        report_parts.append("> Medium effect size") 
                                    else:
                                        report_parts.append("> Small effect size")
                                else:
                                    report_parts.append("> No statistically significant relationship detected (p >= 0.05)")
                            except:
                                report_parts.append("> Could not perform ANOVA test (possibly due to data constraints)")
                        else:
                            report_parts.append("> Insufficient data for ANOVA test")
                    
                    report_parts.append("")
                    
                    # Boxplot for relationship visualization
                    plt.figure(figsize=figsize)
                    sns.boxplot(x=target_column, y=col, data=df_sample)
                    plt.title(f'{target_column} vs {col}')
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    
                    # Convert plot to base64
                    buffer = io.BytesIO()
                    plt.savefig(buffer, format='png')
                    buffer.seek(0)
                    img_str = base64.b64encode(buffer.read()).decode('utf-8')
                    plt.close()
                    
                    report_parts.append(f"![Boxplot](data:image/png;base64,{img_str})")
                    report_parts.append("")
    
    # Datetime Analysis
    if datetime_columns:
        report_parts.append("## Datetime Analysis")
        report_parts.append("")
        report_parts.append("Analysis of datetime variables including temporal patterns and distributions.")
        report_parts.append("")
        
        for col in datetime_columns:
            report_parts.append(f"### {col}")
            report_parts.append("")
            
            # Ensure column is datetime type
            try:
                df[col] = pd.to_datetime(df[col])
                date_series = df[col].dropna()
            except:
                report_parts.append(f"> Error converting {col} to datetime format")
                report_parts.append("")
                continue
            
            # Calculate basic statistics
            report_parts.append("#### Statistics")
            report_parts.append("")
            report_parts.append("| Metric | Value |")
            report_parts.append("|--------|-------|")
            report_parts.append(f"| Count | {date_series.count():,} |")
            report_parts.append(f"| Earliest Date | {date_series.min()} |")
            report_parts.append(f"| Latest Date | {date_series.max()} |")
            report_parts.append(f"| Range | {(date_series.max() - date_series.min()).days} days |")
            report_parts.append("")
            
            # Temporal distribution visualization
            plt.figure(figsize=figsize)
            
            # Group by month for visualization
            date_sample = df_sample[col].dropna()
            if not date_sample.empty:
                date_counts = date_sample.groupby(date_sample.dt.to_period('M')).count()
                date_counts.index = date_counts.index.astype(str)
                
                # Plot temporal distribution
                sns.lineplot(x=date_counts.index, y=date_counts.values)
                plt.title(f'Temporal Distribution of {col}')
                plt.xticks(rotation=45, ha='right')
                plt.ylabel('Count')
                plt.tight_layout()
                
                # Convert plot to base64
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                img_str = base64.b64encode(buffer.read()).decode('utf-8')
                plt.close()
                
                report_parts.append("#### Temporal Distribution")
                report_parts.append("")
                report_parts.append(f"![Temporal Distribution](data:image/png;base64,{img_str})")
                report_parts.append("")
            
            # If target column is provided, analyze relationship
            if target_column and target_column != col and target_column in numeric_columns:
                report_parts.append(f"#### Relationship with {target_column}")
                report_parts.append("")
                
                # Create time series plot
                plt.figure(figsize=figsize)
                valid_data = df_sample[[col, target_column]].dropna()
                
                if len(valid_data) > 0:
                    # Group by week and calculate mean target value
                    valid_data['week'] = valid_data[col].dt.to_period('W')
                    weekly_means = valid_data.groupby('week')[target_column].mean()
                    weekly_means.index = weekly_means.index.astype(str)
                    
                    # Plot the trend
                    sns.lineplot(x=weekly_means.index, y=weekly_means.values)
                    plt.title(f'{target_column} Over Time')
                    plt.xticks(rotation=45, ha='right')
                    plt.ylabel(target_column)
                    plt.tight_layout()
                    
                    # Convert plot to base64
                    buffer = io.BytesIO()
                    plt.savefig(buffer, format='png')
                    buffer.seek(0)
                    img_str = base64.b64encode(buffer.read()).decode('utf-8')
                    plt.close()
                    
                    report_parts.append(f"![Time Series](data:image/png;base64,{img_str})")
                    report_parts.append("")
    
    # Add topic modeling section if requested
    if include_topic_modeling and text_columns:
        report_parts.append("## Topic Modeling Analysis")
        report_parts.append("")
        
        # Set default topic modeling parameters if not provided
        if topic_modeling_params is None:
            topic_modeling_params = {
                'n_topics': 5,
                'method': 'nmf',
                'preprocessing_options': {
                    'enabled': True,
                    'use_lemmatization': True,
                    'remove_stopwords': True,
                },
                'max_docs': 500,  # Limit documents for performance
                'use_multiprocessing': True
            }
        
        # Run topic modeling on specified text columns
        topic_results = {}
        for col in text_columns:
            report_parts.append(f"### Topic Modeling for {col}")
            report_parts.append("")
            
            # Run optimized topic modeling
            try:
                topic_result = create_topic_model_optimized(
                    df=df_sample,
                    text_column=col,
                    **topic_modeling_params
                )
                
                # Store result for potential export
                topic_results[col] = topic_result
                
                # Add topics
                report_parts.append("#### Topics")
                report_parts.append("")
                for topic_idx, terms in topic_result['topics']:
                    term_str = ", ".join([f"{t[0]} ({t[1]:.3f})" for t in terms[:10]])
                    report_parts.append(f"**Topic {topic_idx + 1}**: {term_str}")
                report_parts.append("")
                
                # Add document-topic distribution visualization
                doc_topics = topic_result['document_topics']
                plt.figure(figsize=figsize)
                mean_topic_dist = doc_topics.mean()
                plt.bar(range(len(mean_topic_dist)), mean_topic_dist, color=sns.color_palette("viridis", len(mean_topic_dist)))
                plt.xticks(range(len(mean_topic_dist)), [f"Topic {i+1}" for i in range(len(mean_topic_dist))])
                plt.title(f'Average Topic Distribution for {col}')
                plt.ylabel('Average Weight')
                plt.tight_layout()
                
                # Convert plot to base64
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                img_str = base64.b64encode(buffer.read()).decode('utf-8')
                plt.close()
                
                report_parts.append("#### Topic Distribution")
                report_parts.append("")
                report_parts.append(f"![Topic Distribution](data:image/png;base64,{img_str})")
                report_parts.append("")
                
                # Add interactive visualization if available and HTML format
                if return_html and 'visualizer' in topic_result['topic_model']:
                    report_parts.append("#### Interactive Topic Visualization")
                    report_parts.append("")
                    report_parts.append('<div class="topic-vis">')
                    report_parts.append(topic_result['topic_model']['visualizer'])
                    report_parts.append('</div>')
                    report_parts.append("")
                    
            except Exception as e:
                report_parts.append(f"> Error in topic modeling: {str(e)}")
                report_parts.append("")
    
    # Convert to HTML if requested
    markdown_report = "\n".join(report_parts)
    
    # Create export data dictionary
    export_data = {
        'df': df,
        'numeric_columns': numeric_columns,
        'categorical_columns': categorical_columns,
        'text_columns': text_columns,
        'datetime_columns': datetime_columns
    }
    
    # Add multicollinearity data if available
    high_corr_features = []
    if len(numeric_columns) > 1:
        correlation = df_sample[numeric_columns].corr()
        mask = np.triu(np.ones_like(correlation, dtype=bool))
        corr_mat = correlation.where(~mask)
        
        for col1 in corr_mat.columns:
            for col2 in corr_mat.columns:
                if col1 != col2:
                    corr_value = corr_mat.loc[col1, col2]
                    if not np.isnan(corr_value) and abs(corr_value) >= 0.7:
                        high_corr_features.append((col1, col2, corr_value))
    
    if high_corr_features:
        export_data['multicollinearity'] = {(col1, col2): corr for col1, col2, corr in high_corr_features}
    
    # Add topic modeling results if available
    if include_topic_modeling and text_columns and 'topic_results' in locals():
        export_data['topic_results'] = topic_results
    
    # Handle export if requested
    if export_format and output_path:
        if export_format.lower() == 'xlsx':
            export_to_excel(export_data, output_path, report_type="eda")
            print(f"Excel report exported to {output_path}")
        elif export_format.lower() == 'pptx':
            export_to_powerpoint(export_data, output_path, report_type="eda")
            print(f"PowerPoint report exported to {output_path}")
        else:
            print(f"Unsupported export format: {export_format}")
    
    if return_html:
        try:
            import markdown as markdown_module
            from markdown.extensions.tables import TableExtension
            from markdown.extensions.fenced_code import FencedCodeExtension
        except ImportError:
            import subprocess
            subprocess.check_call(["pip", "install", "markdown"])
            import markdown as markdown_module
            from markdown.extensions.tables import TableExtension
            from markdown.extensions.fenced_code import FencedCodeExtension
        
        # Convert markdown to HTML
        html_body = markdown_module.markdown(markdown_report, extensions=[
            TableExtension(),
            FencedCodeExtension(),
            'nl2br',  # Convert new lines to <br>
            'sane_lists',  # Better handling of lists
        ])
        
        # Create HTML document with proper styling
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Exploratory Data Analysis Report</title>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
            <style>
                body {{ padding-top: 20px; padding-bottom: 40px; }}
                .container {{ max-width: 1200px; }}
                .section {{ margin-bottom: 40px; }}
                img {{ max-width: 100%; height: auto; margin: 10px 0; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 1em; }}
                table, th, td {{ border: 1px solid #ddd; }}
                th, td {{ padding: 8px; text-align: left; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                th {{ background-color: #f9f9f9; color: #333; }}
                blockquote {{ padding: 10px 20px; background-color: #f8f9fa; border-left: 4px solid #007bff; }}
                .topic-vis {{ overflow: auto; max-width: 100%; }}
            </style>
        </head>
        <body>
            <div class="container">
                {html_body}
            </div>
            <script>
            // Code to enable image display in Jupyter
            if (typeof require !== 'undefined') {{
                if (document.querySelector('div.jp-OutputArea-output')) {{
                    document.querySelectorAll('img').forEach(img => {{
                        img.style.maxWidth = '100%';
                    }});
                }}
            }}
            </script>
        </body>
        </html>
        """
        
        return html
    else:
        return markdown_report