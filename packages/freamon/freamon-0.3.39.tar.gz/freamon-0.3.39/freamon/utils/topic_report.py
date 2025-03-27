"""
Topic modeling reporting module.

This module provides functions for generating comprehensive reports
about topic modeling results, including topic-term matrices,
document-topic distributions, interactive visualizations, and
topic coherence metrics.
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


def generate_topic_modeling_report(
    topic_model_results: Dict[str, Any],
    text_data: Optional[pd.DataFrame] = None,
    category_column: Optional[str] = None,
    export_format: Optional[str] = None,
    output_path: Optional[str] = None,
    include_pyldavis: bool = True,
) -> Dict[str, Any]:
    """
    Generate a comprehensive topic modeling report.
    
    Parameters
    ----------
    topic_model_results : Dict[str, Any]
        Dictionary containing topic modeling results, typically from
        create_topic_model or create_topic_model_optimized functions.
        Should include:
        - topics: List of topic terms and weights
        - document_topics: DataFrame of document-topic distribution
        - topic_model: Dict with model details 
    text_data : Optional[pd.DataFrame], default=None
        DataFrame containing the original text data
    category_column : Optional[str], default=None
        Name of category/label column in text_data, if available
    export_format : Optional[str], default=None
        Format to export the report to. Options: 'xlsx', 'pptx'. 
        If None, no export is performed.
    output_path : Optional[str], default=None
        Path to save the exported report. Required if export_format is provided.
    include_pyldavis : bool, default=True
        Whether to include pyLDAvis visualization in HTML exports.
        
    Returns
    -------
    Dict[str, Any]
        Dictionary containing the report data
    """
    # Create report data dictionary
    report_data = {
        'model_type': topic_model_results.get('topic_model', {}).get('model_type', 'Unknown'),
        'n_topics': len(topic_model_results.get('topics', [])),
        'topics': topic_model_results.get('topics', []),
        'document_topics': topic_model_results.get('document_topics', None),
        'n_documents': len(topic_model_results.get('document_topics', [])),
        'preprocessing': topic_model_results.get('processing_info', {}).get('preprocessing', 'Unknown')
    }
    
    # Extract vocabulary size if available
    topic_model = topic_model_results.get('topic_model', {})
    if 'model' in topic_model:
        model = topic_model['model']
        if hasattr(model, 'components_'):
            report_data['vocab_size'] = model.components_.shape[1]
        elif isinstance(model, dict) and 'components' in model:
            report_data['vocab_size'] = model['components'].shape[1]
    
    # Add coherence scores if available
    if 'coherence' in topic_model_results:
        report_data['coherence'] = topic_model_results['coherence']
    
    # Calculate topic similarity
    doc_topics = report_data['document_topics']
    if isinstance(doc_topics, pd.DataFrame):
        topic_similarity = doc_topics.corr().values
        report_data['topic_similarity'] = topic_similarity
    
    # Add category information if available
    if text_data is not None and category_column is not None and category_column in text_data.columns:
        # Map document topics to categories
        category_topics = {}
        
        if isinstance(doc_topics, pd.DataFrame):
            # Join doc_topics with categories
            doc_categories = text_data[category_column].reset_index(drop=True)
            if len(doc_topics) == len(doc_categories):
                doc_topics_with_cat = doc_topics.copy()
                doc_topics_with_cat['category'] = doc_categories
                
                # Calculate average topic distribution by category
                category_topics = doc_topics_with_cat.groupby('category').mean()
                report_data['category_topics'] = category_topics
    
    # Generate visualizations
    visualizations = {}
    
    # Topic term visualizations
    topics = report_data['topics']
    for topic_idx, terms in enumerate(topics[:min(5, len(topics))]):  # Limit to top 5 topics
        # Extract term data
        if isinstance(terms[0], tuple):
            term_words = [term[0] for term in terms[:15]]
            term_weights = [term[1] for term in terms[:15]]
        else:
            term_words = terms[:15]
            term_weights = [1.0] * len(term_words)  # Default weights
        
        plt.figure(figsize=(12, 8))
        y_pos = range(len(term_words))
        plt.barh(y_pos, term_weights, align='center')
        plt.yticks(y_pos, term_words)
        plt.xlabel('Weight')
        plt.title(f'Top Terms for Topic {topic_idx + 1}')
        plt.tight_layout()
        
        # Save visualization
        img_path = f"topic_{topic_idx + 1}_terms.png"
        if output_path:
            base_path = os.path.splitext(output_path)[0]
            img_path = f"{base_path}_topic_{topic_idx + 1}_terms.png"
        plt.savefig(img_path)
        plt.close()
        
        visualizations[f'topic_{topic_idx + 1}_terms'] = img_path
    
    # Topic distribution visualization
    if isinstance(doc_topics, pd.DataFrame):
        mean_topic_dist = doc_topics.mean()
        
        plt.figure(figsize=(12, 8))
        plt.bar(range(len(mean_topic_dist)), mean_topic_dist, color=sns.color_palette("viridis", len(mean_topic_dist)))
        plt.xticks(range(len(mean_topic_dist)), [f"Topic {i+1}" for i in range(len(mean_topic_dist))])
        plt.xlabel('Topic')
        plt.ylabel('Average Weight')
        plt.title('Average Topic Distribution Across Documents')
        plt.tight_layout()
        
        # Save visualization
        img_path = "topic_distribution.png"
        if output_path:
            base_path = os.path.splitext(output_path)[0]
            img_path = f"{base_path}_topic_distribution.png"
        plt.savefig(img_path)
        plt.close()
        
        visualizations['topic_distribution'] = img_path
    
    # Topic similarity visualization
    if 'topic_similarity' in report_data:
        topic_similarity = report_data['topic_similarity']
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(topic_similarity, cmap='coolwarm', annot=True, fmt=".2f",
                    xticklabels=[f'T{i+1}' for i in range(len(topic_similarity))],
                    yticklabels=[f'T{i+1}' for i in range(len(topic_similarity))])
        plt.title('Topic Similarity Matrix')
        plt.tight_layout()
        
        # Save visualization
        img_path = "topic_similarity.png"
        if output_path:
            base_path = os.path.splitext(output_path)[0]
            img_path = f"{base_path}_topic_similarity.png"
        plt.savefig(img_path)
        plt.close()
        
        visualizations['topic_similarity'] = img_path
    
    # Category-topic visualization if available
    if 'category_topics' in report_data:
        category_topics = report_data['category_topics']
        
        plt.figure(figsize=(14, 10))
        sns.heatmap(category_topics, cmap='viridis', annot=False, cbar=True)
        plt.xlabel('Topics')
        plt.ylabel('Categories')
        plt.title('Topic Distribution by Category')
        plt.tight_layout()
        
        # Save visualization
        img_path = "category_topics.png"
        if output_path:
            base_path = os.path.splitext(output_path)[0]
            img_path = f"{base_path}_category_topics.png"
        plt.savefig(img_path)
        plt.close()
        
        visualizations['category_topics'] = img_path
    
    # Add pyLDAvis HTML if available and requested
    if include_pyldavis and 'visualizer' in topic_model:
        visualizations['pyldavis_html'] = topic_model['visualizer']
    
    # Add visualizations to report data
    report_data['visualizations'] = visualizations
    
    # Handle export if requested
    if export_format and output_path:
        if export_format.lower() == 'xlsx':
            export_to_excel(report_data, output_path, report_type="topic")
            print(f"Excel report exported to {output_path}")
        elif export_format.lower() == 'pptx':
            export_to_powerpoint(report_data, output_path, report_type="topic")
            print(f"PowerPoint report exported to {output_path}")
        else:
            print(f"Unsupported export format: {export_format}")
    
    return report_data