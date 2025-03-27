"""
Advanced multivariate analysis for EDA with PCA visualization, correlation networks, 
and target-oriented analysis.

This module provides functions for visualizing high-dimensional data using PCA,
correlation networks, and target-oriented multivariate analysis.
"""
from typing import Any, Dict, List, Optional, Union, Tuple, Literal
import logging
import io
import base64
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import mutual_info_regression, mutual_info_classif
from sklearn.metrics import pairwise_distances
import scipy.stats as stats

# Set up logging
logger = logging.getLogger(__name__)

# Configure matplotlib
plt.rcParams['text.usetex'] = False


def visualize_pca(
    df: pd.DataFrame,
    target_column: Optional[str] = None,
    n_components: int = 2,
    scale: bool = True,
    plot_loading: bool = True,
    figsize: Tuple[int, int] = (12, 10),
    return_dict: bool = False,
) -> Union[Dict[str, Any], Tuple[plt.Figure, Dict[str, Any]]]:
    """
    Visualize data using Principal Component Analysis (PCA).
    
    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to analyze.
    target_column : Optional[str], default=None
        The target column for coloring the scatter plot. If None, no coloring is applied.
    n_components : int, default=2
        Number of principal components to compute. Must be 2 or 3 for visualization.
    scale : bool, default=True
        Whether to standardize the features before PCA.
    plot_loading : bool, default=True
        Whether to plot feature loadings (contribution to principal components).
    figsize : Tuple[int, int], default=(12, 10)
        Figure size for the plots.
    return_dict : bool, default=False
        If True, return a dictionary with PCA results.
        
    Returns
    -------
    Union[Dict[str, Any], Tuple[plt.Figure, Dict[str, Any]]]
        If return_dict is True, returns a dictionary with PCA results.
        Otherwise, returns the figure and the results dictionary.
    """
    if n_components not in (2, 3):
        raise ValueError("n_components must be 2 or 3 for visualization")
    
    # Extract numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if target_column and target_column in numeric_cols:
        numeric_cols.remove(target_column)
    
    if len(numeric_cols) < 2:
        raise ValueError("Need at least 2 numeric columns for PCA")
    
    # Prepare the data
    X = df[numeric_cols].copy()
    
    # Handle missing values
    X = X.fillna(X.mean())
    
    # Scale the data if requested
    if scale:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
    else:
        X_scaled = X.values
    
    # Perform PCA
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(X_scaled)
    
    # Create a dataframe with the principal components
    pc_cols = [f'PC{i+1}' for i in range(n_components)]
    pc_df = pd.DataFrame(data=principal_components, columns=pc_cols)
    
    # Add target column if provided
    if target_column and target_column in df.columns:
        pc_df[target_column] = df[target_column].values
    
    # Prepare for plotting
    if n_components == 2:
        fig = plt.figure(figsize=figsize)
        
        # Create a subplot for PCA scatter plot
        if plot_loading:
            ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=2)
            ax2 = plt.subplot2grid((2, 2), (1, 0), colspan=2)
        else:
            ax1 = plt.subplot()
        
        # Create scatter plot
        if target_column and target_column in df.columns:
            target = df[target_column]
            
            # Check if target is categorical
            if target.dtype == 'object' or target.nunique() < 10:
                # Categorical target - use discrete colors
                scatter = ax1.scatter(
                    pc_df['PC1'], 
                    pc_df['PC2'], 
                    c=pd.factorize(target)[0], 
                    alpha=0.7,
                    cmap='viridis',
                    s=50,
                    edgecolor='w'
                )
                # Add legend
                legend_elements = [
                    plt.Line2D([0], [0], marker='o', color='w', 
                                markerfacecolor=scatter.cmap(scatter.norm(i)), 
                                markersize=10, label=val)
                    for i, val in enumerate(target.unique())
                ]
                ax1.legend(handles=legend_elements, title=target_column, 
                          bbox_to_anchor=(1.05, 1), loc='upper left')
            else:
                # Numeric target - use color gradient
                scatter = ax1.scatter(
                    pc_df['PC1'], 
                    pc_df['PC2'], 
                    c=target, 
                    alpha=0.7,
                    cmap='viridis',
                    s=50,
                    edgecolor='w'
                )
                plt.colorbar(scatter, ax=ax1, label=target_column)
        else:
            ax1.scatter(
                pc_df['PC1'], 
                pc_df['PC2'], 
                alpha=0.7,
                s=50,
                edgecolor='w'
            )
        
        # Label and title
        ax1.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)')
        ax1.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)')
        ax1.set_title('PCA: Principal Component Analysis', fontsize=14)
        ax1.grid(True, alpha=0.3)
        
        # Add loading plot if requested
        if plot_loading:
            # Calculate loadings
            loadings = pd.DataFrame(
                pca.components_.T,
                columns=pc_cols,
                index=numeric_cols
            )
            
            # Plot loadings
            for i, feature in enumerate(loadings.index):
                ax2.arrow(
                    0, 0,  # Start at origin
                    loadings.iloc[i, 0],  # PC1 loading
                    loadings.iloc[i, 1],  # PC2 loading
                    head_width=0.02,
                    head_length=0.03,
                    fc='blue',
                    ec='blue'
                )
                ax2.text(
                    loadings.iloc[i, 0] * 1.15,
                    loadings.iloc[i, 1] * 1.15,
                    feature,
                    color='black',
                    ha='center',
                    va='center'
                )
            
            # Set limits and labels
            ax2.set_xlim(-1, 1)
            ax2.set_ylim(-1, 1)
            ax2.set_xlabel('PC1')
            ax2.set_ylabel('PC2')
            ax2.set_title('Feature Contributions to Principal Components')
            ax2.grid(True, alpha=0.3)
            
            # Add a unit circle
            circle = plt.Circle((0, 0), 1, fc='none', ec='gray', ls='--')
            ax2.add_patch(circle)
            ax2.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
            ax2.axvline(x=0, color='gray', linestyle='-', alpha=0.3)
        
        plt.tight_layout()
    else:  # 3D plot
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')
        
        # Create 3D scatter plot
        if target_column and target_column in df.columns:
            target = df[target_column]
            
            # Check if target is categorical
            if target.dtype == 'object' or target.nunique() < 10:
                # Categorical target - use discrete colors
                scatter = ax.scatter(
                    pc_df['PC1'], 
                    pc_df['PC2'],
                    pc_df['PC3'],
                    c=pd.factorize(target)[0], 
                    alpha=0.7,
                    cmap='viridis',
                    s=50,
                    edgecolor='w'
                )
                # Add legend
                legend_elements = [
                    plt.Line2D([0], [0], marker='o', color='w', 
                                markerfacecolor=scatter.cmap(scatter.norm(i)), 
                                markersize=10, label=val)
                    for i, val in enumerate(target.unique())
                ]
                ax.legend(handles=legend_elements, title=target_column, 
                         bbox_to_anchor=(1.05, 1), loc='upper left')
            else:
                # Numeric target - use color gradient
                scatter = ax.scatter(
                    pc_df['PC1'], 
                    pc_df['PC2'],
                    pc_df['PC3'],
                    c=target, 
                    alpha=0.7,
                    cmap='viridis',
                    s=50,
                    edgecolor='w'
                )
                plt.colorbar(scatter, ax=ax, label=target_column)
        else:
            ax.scatter(
                pc_df['PC1'], 
                pc_df['PC2'],
                pc_df['PC3'],
                alpha=0.7,
                s=50,
                edgecolor='w'
            )
        
        # Label and title
        ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})')
        ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})')
        ax.set_zlabel(f'PC3 ({pca.explained_variance_ratio_[2]:.2%})')
        ax.set_title('PCA: 3D Principal Component Analysis', fontsize=14)
        
        plt.tight_layout()
    
    # Prepare return values
    results = {
        'pca': pca,
        'components': pc_df,
        'explained_variance_ratio': pca.explained_variance_ratio_,
        'loadings': pd.DataFrame(
            pca.components_.T,
            columns=pc_cols,
            index=numeric_cols
        )
    }
    
    if return_dict:
        # Save figure to buffer
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        
        # Convert to base64 for HTML embedding
        img_str = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close(fig)
        
        results['plot'] = f"data:image/png;base64,{img_str}"
        return results
    else:
        return fig, results


def analyze_target_relationships(
    df: pd.DataFrame,
    target_column: str,
    max_features: int = 10,
    figsize: Tuple[int, int] = (12, 8),
    return_dict: bool = False,
) -> Union[Dict[str, Any], Tuple[List[plt.Figure], Dict[str, Any]]]:
    """
    Analyze relationships between features and a target variable.
    
    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to analyze.
    target_column : str
        The target column to analyze relationships with.
    max_features : int, default=10
        Maximum number of top features to show in visualizations.
    figsize : Tuple[int, int], default=(12, 8)
        Figure size for the plots.
    return_dict : bool, default=False
        If True, return a dictionary with results.
        
    Returns
    -------
    Union[Dict[str, Any], Tuple[List[plt.Figure], Dict[str, Any]]]
        If return_dict is True, returns a dictionary with results.
        Otherwise, returns a list of figures and the results dictionary.
    """
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataframe")
    
    target = df[target_column]
    
    # Determine if target is categorical or continuous
    is_categorical = False
    if target.dtype == 'object' or target.nunique() < 10:
        is_categorical = True
    
    # Extract numeric features
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if target_column in numeric_cols:
        numeric_cols.remove(target_column)
    
    # Extract categorical features
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    if target_column in categorical_cols:
        categorical_cols.remove(target_column)
    
    # Add low-cardinality numeric columns as categorical
    for col in numeric_cols[:]:
        if df[col].nunique() < 10:
            categorical_cols.append(col)
            numeric_cols.remove(col)
    
    results = {
        'target_column': target_column,
        'is_categorical_target': is_categorical,
        'feature_scores': {},
        'numerical_features': numeric_cols,
        'categorical_features': categorical_cols
    }
    
    figures = []
    
    # Analyze relationship with numeric features
    if numeric_cols and len(numeric_cols) > 0:
        # Calculate mutual information scores
        if is_categorical:
            mi_func = mutual_info_classif
        else:
            mi_func = mutual_info_regression
        
        # Fill NA with mean for MI calculation
        X_numeric = df[numeric_cols].fillna(df[numeric_cols].mean())
        mi_scores = mi_func(X_numeric, target, random_state=42)
        
        # Create a dataframe of scores
        mi_df = pd.DataFrame({
            'Feature': numeric_cols,
            'Mutual Information': mi_scores
        }).sort_values('Mutual Information', ascending=False)
        
        # Store in results
        results['feature_scores']['mutual_information'] = mi_df.set_index('Feature')['Mutual Information'].to_dict()
        
        # Calculate Pearson correlation if target is numeric
        if not is_categorical:
            correlations = {}
            p_values = {}
            
            for col in numeric_cols:
                # Skip if all values are the same
                if df[col].nunique() <= 1:
                    continue
                    
                mask = ~(df[col].isna() | df[target_column].isna())
                if mask.sum() < 2:
                    continue
                    
                r, p = stats.pearsonr(df.loc[mask, col], df.loc[mask, target_column])
                correlations[col] = r
                p_values[col] = p
            
            # Create correlation dataframe
            if correlations:
                corr_df = pd.DataFrame({
                    'Feature': list(correlations.keys()),
                    'Correlation': list(correlations.values()),
                    'P-Value': list(p_values.values())
                }).sort_values(by='Correlation', key=abs, ascending=False)
                
                # Store in results
                results['feature_scores']['correlation'] = corr_df.set_index('Feature')['Correlation'].to_dict()
                results['feature_scores']['p_values'] = corr_df.set_index('Feature')['P-Value'].to_dict()
        
        # Create visualization of top features by mutual information
        fig_mi, ax_mi = plt.subplots(figsize=figsize)
        
        top_mi = mi_df.head(min(max_features, len(mi_df)))
        sns.barplot(
            x='Mutual Information',
            y='Feature',
            data=top_mi,
            ax=ax_mi
        )
        ax_mi.set_title(f'Top Features by Mutual Information with {target_column}')
        ax_mi.set_xlabel('Mutual Information Score')
        plt.tight_layout()
        figures.append(fig_mi)
        
        # Calculate Predictive Power Score if possible
        try:
            import ppscore as pps
            has_pps = True
        except ImportError:
            has_pps = False
            
        if has_pps:
            # Calculate PPS for each feature with target
            pps_scores = {}
            for col in numeric_cols:
                pps_scores[col] = pps.score(df, col, target_column)['ppscore']
                
            # Create PPS dataframe
            pps_df = pd.DataFrame({
                'Feature': list(pps_scores.keys()),
                'PPS': list(pps_scores.values())
            }).sort_values('PPS', ascending=False)
            
            # Store in results
            results['feature_scores']['pps'] = pps_df.set_index('Feature')['PPS'].to_dict()
            
            # Create visualization of top features by PPS
            fig_pps, ax_pps = plt.subplots(figsize=figsize)
            
            top_pps = pps_df.head(min(max_features, len(pps_df)))
            sns.barplot(
                x='PPS',
                y='Feature',
                data=top_pps,
                ax=ax_pps
            )
            ax_pps.set_title(f'Top Features by Predictive Power Score with {target_column}')
            ax_pps.set_xlabel('Predictive Power Score')
            plt.tight_layout()
            figures.append(fig_pps)
    
    # Analyze relationship with categorical features using ANOVA/Chi-squared
    if categorical_cols and len(categorical_cols) > 0:
        if is_categorical:
            # Use Chi-squared test for categorical target and categorical features
            chi2_results = {}
            cramers_v = {}
            
            for col in categorical_cols:
                # Create contingency table
                contingency = pd.crosstab(df[col], df[target_column])
                
                # Perform chi-squared test
                chi2, p, dof, expected = stats.chi2_contingency(contingency)
                
                # Calculate Cramer's V (normalized effect size for chi-squared)
                n = contingency.sum().sum()
                phi2 = chi2 / n
                r, k = contingency.shape
                cramers_v_value = np.sqrt(phi2 / min(k-1, r-1))
                
                chi2_results[col] = {
                    'chi2': chi2,
                    'p_value': p,
                    'dof': dof
                }
                cramers_v[col] = cramers_v_value
            
            # Create chi-squared dataframe
            if chi2_results:
                chi2_df = pd.DataFrame({
                    'Feature': list(chi2_results.keys()),
                    'Chi-Squared': [chi2_results[f]['chi2'] for f in chi2_results.keys()],
                    'P-Value': [chi2_results[f]['p_value'] for f in chi2_results.keys()],
                    "Cramer's V": [cramers_v[f] for f in chi2_results.keys()]
                }).sort_values("Cramer's V", ascending=False)
                
                # Store in results
                results['feature_scores']['chi_squared'] = {
                    f: {'chi2': chi2_results[f]['chi2'], 'p_value': chi2_results[f]['p_value']}
                    for f in chi2_results.keys()
                }
                results['feature_scores']['cramers_v'] = {f: cramers_v[f] for f in cramers_v.keys()}
                
                # Create visualization of top categorical features by Cramer's V
                fig_cv, ax_cv = plt.subplots(figsize=figsize)
                
                top_cv = chi2_df.head(min(max_features, len(chi2_df)))
                sns.barplot(
                    x="Cramer's V",
                    y='Feature',
                    data=top_cv,
                    ax=ax_cv
                )
                ax_cv.set_title(f"Top Categorical Features by Cramer's V with {target_column}")
                ax_cv.set_xlabel("Cramer's V (Effect Size)")
                plt.tight_layout()
                figures.append(fig_cv)
                
        else:
            # Use ANOVA for numeric target and categorical features
            anova_results = {}
            eta_squared = {}
            
            for col in categorical_cols:
                groups = []
                labels = []
                
                # Collect data for each group
                for group_label, group_data in df.groupby(col)[target_column]:
                    if len(group_data) > 0:
                        groups.append(group_data)
                        labels.append(group_label)
                
                # Only perform ANOVA if we have at least 2 groups
                if len(groups) >= 2:
                    try:
                        # Perform one-way ANOVA
                        f_stat, p_value = stats.f_oneway(*groups)
                        
                        # Calculate eta-squared (effect size for ANOVA)
                        # Sum of squares between groups
                        ss_between = sum(len(group) * (group.mean() - df[target_column].mean())**2 
                                        for group in groups)
                        # Total sum of squares
                        ss_total = sum((x - df[target_column].mean())**2 
                                      for x in df[target_column].dropna())
                        # Calculate eta-squared
                        eta_sq = ss_between / ss_total if ss_total > 0 else 0
                        
                        anova_results[col] = {
                            'f_statistic': f_stat,
                            'p_value': p_value
                        }
                        eta_squared[col] = eta_sq
                    except Exception as e:
                        logger.warning(f"Error in ANOVA for {col}: {str(e)}")
            
            # Create ANOVA dataframe
            if anova_results:
                anova_df = pd.DataFrame({
                    'Feature': list(anova_results.keys()),
                    'F-Statistic': [anova_results[f]['f_statistic'] for f in anova_results.keys()],
                    'P-Value': [anova_results[f]['p_value'] for f in anova_results.keys()],
                    'Eta-Squared': [eta_squared[f] for f in anova_results.keys()]
                }).sort_values('Eta-Squared', ascending=False)
                
                # Store in results
                results['feature_scores']['anova'] = {
                    f: {'f_statistic': anova_results[f]['f_statistic'], 
                        'p_value': anova_results[f]['p_value']}
                    for f in anova_results.keys()
                }
                results['feature_scores']['eta_squared'] = {f: eta_squared[f] for f in eta_squared.keys()}
                
                # Create visualization of top categorical features by eta-squared
                fig_eta, ax_eta = plt.subplots(figsize=figsize)
                
                top_eta = anova_df.head(min(max_features, len(anova_df)))
                sns.barplot(
                    x='Eta-Squared',
                    y='Feature',
                    data=top_eta,
                    ax=ax_eta
                )
                ax_eta.set_title(f'Top Categorical Features by Eta-Squared with {target_column}')
                ax_eta.set_xlabel('Eta-Squared (Effect Size)')
                plt.tight_layout()
                figures.append(fig_eta)
    
    # Combine all feature scores into a unified ranking
    all_scores = {}
    score_types = results['feature_scores'].keys()
    
    for score_type in score_types:
        if score_type in ['mutual_information', 'pps', 'cramers_v', 'eta_squared']:
            # These are direct scores where higher is better
            for feature, score in results['feature_scores'][score_type].items():
                if feature not in all_scores:
                    all_scores[feature] = {'scores': {}, 'avg_rank': 0}
                all_scores[feature]['scores'][score_type] = score
    
    # Calculate average normalized score for each feature
    for feature in all_scores:
        scores = all_scores[feature]['scores']
        if len(scores) > 0:
            # Normalize each score type to [0, 1] range and average
            normalized_scores = []
            for score_type, score in scores.items():
                all_scores_of_type = [all_scores[f]['scores'].get(score_type, 0) 
                                     for f in all_scores if score_type in all_scores[f]['scores']]
                max_score = max(all_scores_of_type)
                if max_score > 0:
                    normalized_scores.append(score / max_score)
                else:
                    normalized_scores.append(0)
            
            all_scores[feature]['avg_score'] = sum(normalized_scores) / len(normalized_scores)
    
    # Sort features by average score
    sorted_features = sorted(all_scores.keys(), 
                             key=lambda f: all_scores[f].get('avg_score', 0), 
                             reverse=True)
    
    # Store combined ranking
    results['feature_ranking'] = {
        f: {
            'rank': i + 1,
            'avg_score': all_scores[f].get('avg_score', 0),
            'scores': all_scores[f]['scores']
        }
        for i, f in enumerate(sorted_features)
    }
    
    # Create visualization of top features by combined score
    if sorted_features:
        fig_combined, ax_combined = plt.subplots(figsize=figsize)
        
        top_combined = pd.DataFrame({
            'Feature': sorted_features[:min(max_features, len(sorted_features))],
            'Score': [all_scores[f].get('avg_score', 0) 
                     for f in sorted_features[:min(max_features, len(sorted_features))]]
        })
        
        sns.barplot(
            x='Score',
            y='Feature',
            data=top_combined,
            ax=ax_combined
        )
        ax_combined.set_title(f'Top Features by Combined Relevance Score for {target_column}')
        ax_combined.set_xlabel('Normalized Relevance Score')
        plt.tight_layout()
        figures.append(fig_combined)
    
    if return_dict:
        # Convert figures to base64 for HTML embedding
        plots = {}
        for i, fig in enumerate(figures):
            buffer = io.BytesIO()
            fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            img_str = base64.b64encode(buffer.read()).decode('utf-8')
            plots[f'plot_{i}'] = f"data:image/png;base64,{img_str}"
            plt.close(fig)
        
        results['plots'] = plots
        return results
    else:
        return figures, results


def create_correlation_network(
    df: pd.DataFrame,
    threshold: float = 0.7,
    method: str = 'pearson',
    figsize: Tuple[int, int] = (12, 10),
    return_dict: bool = False,
) -> Union[Dict[str, Any], Tuple[plt.Figure, Dict[str, Any]]]:
    """
    Create a network visualization of feature correlations.
    
    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to analyze.
    threshold : float, default=0.7
        Correlation threshold for including edges in the network.
    method : str, default='pearson'
        Correlation method ('pearson', 'spearman', or 'kendall').
    figsize : Tuple[int, int], default=(12, 10)
        Figure size for the plot.
    return_dict : bool, default=False
        If True, return a dictionary with results.
        
    Returns
    -------
    Union[Dict[str, Any], Tuple[plt.Figure, Dict[str, Any]]]
        If return_dict is True, returns a dictionary with results.
        Otherwise, returns the figure and the results dictionary.
    """
    # Check for networkx
    try:
        import networkx as nx
    except ImportError:
        raise ImportError("networkx is required for correlation networks. "
                         "Install it with: pip install networkx")
    
    # Extract numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if len(numeric_cols) < 2:
        raise ValueError("Need at least 2 numeric columns for correlation network")
    
    # Calculate correlation matrix
    corr_matrix = df[numeric_cols].corr(method=method)
    
    # Create network graph
    G = nx.Graph()
    
    # Add nodes (features)
    for col in numeric_cols:
        G.add_node(col)
    
    # Add edges (correlations above threshold)
    for i, col1 in enumerate(numeric_cols):
        for j, col2 in enumerate(numeric_cols):
            if i < j:  # Only look at upper triangle
                corr = abs(corr_matrix.loc[col1, col2])
                if corr >= threshold:
                    G.add_edge(col1, col2, weight=corr)
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Calculate node positions using spring layout
    pos = nx.spring_layout(G, seed=42)
    
    # Get node sizes based on degree
    node_sizes = [300 + 100 * G.degree(node) for node in G.nodes()]
    
    # Get edge weights for width
    edge_weights = [G[u][v]['weight'] * 3 for u, v in G.edges()]
    
    # Calculate node colors based on clustering coefficient
    clustering = nx.clustering(G)
    node_colors = [clustering.get(node, 0) for node in G.nodes()]
    
    # Draw the network
    nx.draw_networkx_nodes(
        G, pos, 
        node_size=node_sizes,
        node_color=node_colors,
        cmap='viridis',
        alpha=0.8,
        ax=ax
    )
    
    # Draw edges with width proportional to correlation strength
    nx.draw_networkx_edges(
        G, pos,
        width=edge_weights,
        alpha=0.6,
        edge_color='gray',
        ax=ax
    )
    
    # Draw labels with appropriate font size
    nx.draw_networkx_labels(
        G, pos,
        font_size=10,
        font_family='sans-serif',
        ax=ax
    )
    
    plt.title('Feature Correlation Network', fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    
    # Prepare results
    results = {
        'graph': G,
        'correlations': corr_matrix.to_dict(),
        'nodes': list(G.nodes()),
        'edges': list(G.edges()),
        'clustering': clustering
    }
    
    if return_dict:
        # Convert figure to base64 for HTML embedding
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        img_str = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close(fig)
        
        results['plot'] = f"data:image/png;base64,{img_str}"
        return results
    else:
        return fig, results