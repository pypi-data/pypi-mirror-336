"""
Feature selection methods for categorical variables.

This module provides specialized methods for selecting the most informative
categorical features using methods such as Chi-Square, ANOVA F-value, and
mutual information criteria.
"""
from typing import Any, Dict, List, Optional, Union, Tuple, Literal, Set
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import (
    chi2,
    f_classif, 
    f_regression, 
    mutual_info_classif, 
    mutual_info_regression,
    SelectKBest,
    SelectPercentile
)
import scipy.stats as stats

from freamon.utils import check_dataframe_type, convert_dataframe


class CategoricalFeatureSelector:
    """
    Feature selector for categorical variables using statistical tests.
    
    This selector uses statistical tests like Chi-square, ANOVA F-test, and 
    mutual information to identify the most informative categorical features 
    for a target variable.
    
    Attributes
    ----------
    method : str
        The statistical method used for feature selection.
    k : int or float
        Number or proportion of top features to select.
    scoring_func : callable
        The function used to score features.
    selector : SelectKBest or SelectPercentile
        The underlying scikit-learn selector.
    feature_names_ : List[str]
        Names of categorical features.
    scores_ : np.ndarray
        Feature scores after fitting.
    pvalues_ : np.ndarray
        Feature p-values after fitting (if applicable).
    selected_features_ : List[str]
        Names of selected features after fitting.
    """
    
    def __init__(
        self, 
        method: Literal['chi2', 'anova_f', 'mutual_info'] = 'chi2',
        k: Union[int, float] = 10,
        target_type: Optional[Literal['classification', 'regression']] = None
    ):
        """
        Initialize the categorical feature selector.
        
        Parameters
        ----------
        method : {'chi2', 'anova_f', 'mutual_info'}, default='chi2'
            The statistical method to use for feature selection:
            - 'chi2': Chi-square test (for classification)
            - 'anova_f': ANOVA F-test (for regression or classification)
            - 'mutual_info': Mutual information (for regression or classification)
        k : int or float, default=10
            Number of top features to select if int, or proportion of features 
            to select if float between 0 and 1.
        target_type : {'classification', 'regression'}, default=None
            Type of target variable. If None, will be inferred from data.
        """
        self.method = method
        self.k = k
        self.target_type = target_type
        
        self.scoring_func = None
        self.selector = None
        self.feature_names_ = None
        self.scores_ = None
        self.pvalues_ = None
        self.selected_features_ = None
        self.effect_sizes_ = None
    
    def fit(
        self,
        X: pd.DataFrame,
        y: Union[pd.Series, np.ndarray],
        categorical_features: Optional[List[str]] = None
    ):
        """
        Fit the selector to the data.
        
        Parameters
        ----------
        X : pd.DataFrame
            Input features.
        y : pd.Series or np.ndarray
            Target variable.
        categorical_features : List[str], optional
            List of categorical column names. If None, all object and category
            columns are considered categorical, plus numeric columns with <=20
            unique values.
            
        Returns
        -------
        self : CategoricalFeatureSelector
            The fitted selector.
        """
        # Check dataframe type and convert to pandas if needed
        X_type = check_dataframe_type(X)
        if X_type != 'pandas':
            X_pandas = convert_dataframe(X, 'pandas')
        else:
            X_pandas = X
            
        # Identify categorical features if not provided
        if categorical_features is None:
            # Start with object and category columns
            categorical_features = list(
                X_pandas.select_dtypes(include=['object', 'category']).columns
            )
            
            # Add low-cardinality numeric columns
            for col in X_pandas.select_dtypes(include=['number']).columns:
                if X_pandas[col].nunique() <= 20:  # Arbitrary threshold
                    categorical_features.append(col)
        
        if not categorical_features:
            raise ValueError("No categorical features found in data")
            
        self.feature_names_ = categorical_features
        
        # Infer target type if not provided
        if self.target_type is None:
            # Check if target is categorical
            if hasattr(y, 'nunique'):
                if y.nunique() <= 20:  # Arbitrary threshold
                    self.target_type = 'classification'
                else:
                    self.target_type = 'regression'
            else:
                y_array = np.array(y)
                if np.issubdtype(y_array.dtype, np.integer) and len(np.unique(y_array)) <= 20:
                    self.target_type = 'classification'
                else:
                    self.target_type = 'regression'
        
        # Create encoder mapping for categorical features
        X_encoded = pd.DataFrame()
        self.encoders_ = {}
        
        for feature in categorical_features:
            # Get feature values
            feature_values = X_pandas[feature].astype(str)
            
            # Create one-hot encoding
            dummies = pd.get_dummies(feature_values, prefix=feature, drop_first=False)
            
            # Store in encoded dataframe
            X_encoded = pd.concat([X_encoded, dummies], axis=1)
            
            # Store encoder mapping
            value_columns = dummies.columns.tolist()
            self.encoders_[feature] = value_columns
            
        # Set scoring function based on method and target type
        if self.method == 'chi2':
            if self.target_type != 'classification':
                raise ValueError("Chi-square test only applicable for classification problems")
            self.scoring_func = chi2
        elif self.method == 'anova_f':
            if self.target_type == 'classification':
                self.scoring_func = f_classif
            else:
                self.scoring_func = f_regression
        elif self.method == 'mutual_info':
            if self.target_type == 'classification':
                self.scoring_func = mutual_info_classif
            else:
                self.scoring_func = mutual_info_regression
        else:
            raise ValueError(f"Unknown method: {self.method}")
        
        # Create selector based on k type
        if isinstance(self.k, int):
            # Select top k features
            self.selector = SelectKBest(score_func=self.scoring_func, k=min(self.k, len(categorical_features)))
        else:
            # Select top k% features
            self.selector = SelectPercentile(score_func=self.scoring_func, percentile=self.k * 100)
        
        # Fit selector
        self.selector.fit(X_encoded, y)
        
        # Get scores and p-values (if available)
        self.scores_ = self.selector.scores_
        if hasattr(self.selector, 'pvalues_'):
            self.pvalues_ = self.selector.pvalues_
        
        # Calculate effect sizes if applicable
        self.effect_sizes_ = {}
        if self.method == 'chi2' and self.target_type == 'classification':
            # Calculate Cramer's V for each feature
            for feature in categorical_features:
                # Create contingency table
                contingency = pd.crosstab(X_pandas[feature], y)
                
                # Calculate Cramer's V
                chi2_val, _, _, _ = stats.chi2_contingency(contingency)
                n = contingency.sum().sum()
                phi2 = chi2_val / n
                r, k = contingency.shape
                cramers_v = np.sqrt(phi2 / min(k-1, r-1))
                
                self.effect_sizes_[feature] = cramers_v
        elif self.method == 'anova_f' and self.target_type == 'regression':
            # Calculate Eta-squared for each feature
            for feature in categorical_features:
                groups = []
                
                # Group target values by feature categories
                for category, group in X_pandas.groupby(feature):
                    target_values = y.iloc[group.index] if hasattr(y, 'iloc') else y[group.index]
                    if len(target_values) > 0:
                        groups.append(target_values)
                
                if len(groups) >= 2:
                    # Calculate eta-squared
                    # Sum of squares between groups
                    grand_mean = np.mean(y)
                    ss_between = sum(len(group) * (np.mean(group) - grand_mean)**2 for group in groups)
                    
                    # Total sum of squares
                    ss_total = sum((val - grand_mean)**2 for val in y)
                    
                    # Calculate eta-squared
                    eta_squared = ss_between / ss_total if ss_total > 0 else 0
                    
                    self.effect_sizes_[feature] = eta_squared
        
        # Aggregate scores for each feature (from one-hot encoded columns)
        feature_scores = {}
        feature_pvalues = {}
        
        for feature, value_columns in self.encoders_.items():
            # Get indices for this feature's columns
            indices = [i for i, col in enumerate(X_encoded.columns) if col in value_columns]
            
            if indices:
                # Aggregate scores - use mean
                feature_scores[feature] = np.mean(self.scores_[indices])
                
                # Aggregate p-values if available - use minimum (most significant)
                if hasattr(self, 'pvalues_') and self.pvalues_ is not None:
                    feature_pvalues[feature] = np.min(self.pvalues_[indices])
        
        # Create feature importance dataframe
        importance_data = []
        for feature in categorical_features:
            importance_data.append({
                'Feature': feature,
                'Score': feature_scores.get(feature, 0),
                'P-Value': feature_pvalues.get(feature, 1) if feature_pvalues else None,
                'Effect Size': self.effect_sizes_.get(feature, None)
            })
        
        self.feature_importance_ = pd.DataFrame(importance_data)
        
        # Sort by score descending
        self.feature_importance_ = self.feature_importance_.sort_values('Score', ascending=False)
        
        # Determine selected features
        k = self.k if isinstance(self.k, int) else int(len(categorical_features) * self.k)
        self.selected_features_ = self.feature_importance_['Feature'].head(k).tolist()
        
        return self
    
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Transform the data to include only selected features.
        
        Parameters
        ----------
        X : pd.DataFrame
            Input features.
            
        Returns
        -------
        pd.DataFrame
            Transformed dataframe with only the selected features.
        """
        if self.selected_features_ is None:
            raise ValueError("Selector not fitted. Call fit first.")
        
        # Check dataframe type and convert to pandas if needed
        X_type = check_dataframe_type(X)
        if X_type != 'pandas':
            X_pandas = convert_dataframe(X, 'pandas')
        else:
            X_pandas = X
        
        # Return only selected columns
        return X_pandas[self.selected_features_]
    
    def fit_transform(
        self,
        X: pd.DataFrame,
        y: Union[pd.Series, np.ndarray],
        categorical_features: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Fit the selector and transform the data.
        
        Parameters
        ----------
        X : pd.DataFrame
            Input features.
        y : pd.Series or np.ndarray
            Target variable.
        categorical_features : List[str], optional
            List of categorical column names.
            
        Returns
        -------
        pd.DataFrame
            Transformed dataframe with only the selected features.
        """
        self.fit(X, y, categorical_features)
        return self.transform(X)
    
    def plot_feature_importance(self, top_n: int = 10, figsize: Tuple[int, int] = (10, 6)):
        """
        Plot feature importance scores.
        
        Parameters
        ----------
        top_n : int, default=10
            Number of top features to show.
        figsize : tuple, default=(10, 6)
            Figure size.
            
        Returns
        -------
        matplotlib.figure.Figure
            The generated figure.
        """
        if self.feature_importance_ is None:
            raise ValueError("Selector not fitted. Call fit first.")
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Get top n features
        top_features = self.feature_importance_.head(top_n)
        
        # Create plot
        sns.barplot(
            y='Feature',
            x='Score',
            data=top_features,
            ax=ax
        )
        
        # Add title and labels
        if self.method == 'chi2':
            ax.set_title('Top Features by Chi-Square Score')
            ax.set_xlabel('Chi-Square Score')
        elif self.method == 'anova_f':
            ax.set_title('Top Features by F-Score (ANOVA)')
            ax.set_xlabel('F-Score')
        elif self.method == 'mutual_info':
            ax.set_title('Top Features by Mutual Information')
            ax.set_xlabel('Mutual Information Score')
        
        ax.set_ylabel('Feature')
        
        plt.tight_layout()
        return fig
    
    def plot_effect_sizes(self, top_n: int = 10, figsize: Tuple[int, int] = (10, 6)):
        """
        Plot effect sizes for features.
        
        Parameters
        ----------
        top_n : int, default=10
            Number of top features to show.
        figsize : tuple, default=(10, 6)
            Figure size.
            
        Returns
        -------
        matplotlib.figure.Figure
            The generated figure.
        """
        if self.effect_sizes_ is None or len(self.effect_sizes_) == 0:
            raise ValueError("Effect sizes not available. Either not calculated or not applicable.")
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create dataframe from effect sizes
        effect_df = pd.DataFrame([
            {'Feature': feature, 'Effect Size': effect_size}
            for feature, effect_size in self.effect_sizes_.items()
        ]).sort_values('Effect Size', ascending=False)
        
        # Get top n features
        top_effects = effect_df.head(top_n)
        
        # Create plot
        sns.barplot(
            y='Feature',
            x='Effect Size',
            data=top_effects,
            ax=ax
        )
        
        # Add title and labels
        if self.method == 'chi2':
            ax.set_title("Top Features by Cramer's V (Effect Size)")
            ax.set_xlabel("Cramer's V")
        elif self.method == 'anova_f':
            ax.set_title('Top Features by Eta-Squared (Effect Size)')
            ax.set_xlabel('Eta-Squared')
        
        ax.set_ylabel('Feature')
        
        plt.tight_layout()
        return fig


def select_categorical_features(
    df: pd.DataFrame,
    target: Union[pd.Series, np.ndarray, str],
    method: Literal['chi2', 'anova_f', 'mutual_info'] = 'chi2',
    k: Union[int, float] = 10,
    categorical_features: Optional[List[str]] = None,
    problem_type: Optional[Literal['classification', 'regression']] = None,
    return_names_only: bool = True,
    return_scores: bool = False
) -> Union[List[str], pd.DataFrame, Tuple[List[str], pd.DataFrame]]:
    """
    Select the most informative categorical features using statistical tests.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    target : pd.Series, np.ndarray, or str
        Target variable or name of target column in df.
    method : {'chi2', 'anova_f', 'mutual_info'}, default='chi2'
        The statistical method to use for feature selection.
    k : int or float, default=10
        Number of top features to select if int, or proportion of features to
        select if float between 0 and 1.
    categorical_features : List[str], optional
        List of categorical column names. If None, all object and category
        columns are considered categorical, plus numeric columns with <=20
        unique values.
    problem_type : {'classification', 'regression'}, optional
        Type of problem. If None, inferred from target data.
    return_names_only : bool, default=True
        If True, return only the names of selected features.
        If False, return a dataframe with only the selected features.
    return_scores : bool, default=False
        If True, also return feature importance scores.
        
    Returns
    -------
    Union[List[str], pd.DataFrame, Tuple[List[str], pd.DataFrame]]
        Depending on return_names_only and return_scores:
        - List of selected feature names if return_names_only=True and return_scores=False
        - DataFrame with only selected features if return_names_only=False and return_scores=False
        - Tuple of (selected feature names, scores dataframe) if return_scores=True
    """
    # Check dataframe type and convert to pandas if needed
    df_type = check_dataframe_type(df)
    if df_type != 'pandas':
        df_pandas = convert_dataframe(df, 'pandas')
    else:
        df_pandas = df
    
    # Get target
    if isinstance(target, str):
        if target not in df_pandas.columns:
            raise ValueError(f"Target column '{target}' not found in dataframe")
        y = df_pandas[target]
    else:
        y = target
    
    # Identify categorical features if not provided
    if categorical_features is None:
        # Start with object and category columns
        categorical_features = list(
            df_pandas.select_dtypes(include=['object', 'category']).columns
        )
        
        # Add low-cardinality numeric columns
        for col in df_pandas.select_dtypes(include=['number']).columns:
            if col != target and df_pandas[col].nunique() <= 20:  # Arbitrary threshold
                categorical_features.append(col)
    
    if not categorical_features:
        raise ValueError("No categorical features found in data")
    
    # Create selector
    selector = CategoricalFeatureSelector(
        method=method,
        k=k,
        target_type=problem_type
    )
    
    # Fit selector
    selector.fit(df_pandas, y, categorical_features)
    
    # Return results
    if return_scores:
        return selector.selected_features_, selector.feature_importance_
    elif return_names_only:
        return selector.selected_features_
    else:
        return df_pandas[selector.selected_features_]


def anova_f_selection(
    df: pd.DataFrame,
    target: Union[pd.Series, np.ndarray, str],
    k: Union[int, float] = 10,
    categorical_features: Optional[List[str]] = None,
    return_names_only: bool = True,
    return_scores: bool = False
) -> Union[List[str], pd.DataFrame, Tuple[List[str], pd.DataFrame]]:
    """
    Select categorical features using ANOVA F-test.
    
    This function uses ANOVA F-test to select the most informative categorical
    features for a target variable.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    target : pd.Series, np.ndarray, or str
        Target variable or name of target column in df.
    k : int or float, default=10
        Number of top features to select if int, or proportion of features to
        select if float between 0 and 1.
    categorical_features : List[str], optional
        List of categorical column names. If None, all object and category
        columns are considered categorical, plus numeric columns with <=20
        unique values.
    return_names_only : bool, default=True
        If True, return only the names of selected features.
        If False, return a dataframe with only the selected features.
    return_scores : bool, default=False
        If True, also return feature importance scores.
        
    Returns
    -------
    Union[List[str], pd.DataFrame, Tuple[List[str], pd.DataFrame]]
        Selected features based on return options.
    """
    return select_categorical_features(
        df=df,
        target=target,
        method='anova_f',
        k=k,
        categorical_features=categorical_features,
        return_names_only=return_names_only,
        return_scores=return_scores
    )


def chi2_selection(
    df: pd.DataFrame,
    target: Union[pd.Series, np.ndarray, str],
    k: Union[int, float] = 10,
    categorical_features: Optional[List[str]] = None,
    return_names_only: bool = True,
    return_scores: bool = False
) -> Union[List[str], pd.DataFrame, Tuple[List[str], pd.DataFrame]]:
    """
    Select categorical features using Chi-square test.
    
    This function uses Chi-square test to select the most informative categorical
    features for a categorical target variable.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    target : pd.Series, np.ndarray, or str
        Target variable or name of target column in df.
    k : int or float, default=10
        Number of top features to select if int, or proportion of features to
        select if float between 0 and 1.
    categorical_features : List[str], optional
        List of categorical column names. If None, all object and category
        columns are considered categorical, plus numeric columns with <=20
        unique values.
    return_names_only : bool, default=True
        If True, return only the names of selected features.
        If False, return a dataframe with only the selected features.
    return_scores : bool, default=False
        If True, also return feature importance scores.
        
    Returns
    -------
    Union[List[str], pd.DataFrame, Tuple[List[str], pd.DataFrame]]
        Selected features based on return options.
    """
    return select_categorical_features(
        df=df,
        target=target,
        method='chi2',
        k=k,
        categorical_features=categorical_features,
        problem_type='classification',  # Chi-square only works for classification
        return_names_only=return_names_only,
        return_scores=return_scores
    )


def plot_categorical_importance(
    feature_scores: pd.DataFrame,
    method: str = 'chi2',
    top_n: int = 10,
    figsize: Tuple[int, int] = (10, 6),
    show_effect_size: bool = True
) -> plt.Figure:
    """
    Plot importance scores for categorical features.
    
    Parameters
    ----------
    feature_scores : pd.DataFrame
        Dataframe with feature importance scores, as returned by 
        select_categorical_features with return_scores=True.
    method : str, default='chi2'
        The method used for feature selection.
    top_n : int, default=10
        Number of top features to show.
    figsize : tuple, default=(10, 6)
        Figure size.
    show_effect_size : bool, default=True
        Whether to show effect sizes in a separate plot.
        
    Returns
    -------
    plt.Figure or Tuple[plt.Figure, plt.Figure]
        The generated figure(s).
    """
    if not isinstance(feature_scores, pd.DataFrame):
        raise ValueError("feature_scores must be a DataFrame")
    
    # Sort by score if not already sorted
    scores_df = feature_scores.sort_values('Score', ascending=False).head(top_n)
    
    # Create figure for scores
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot scores
    sns.barplot(
        y='Feature',
        x='Score',
        data=scores_df,
        ax=ax
    )
    
    # Add title and labels
    if method == 'chi2':
        ax.set_title('Top Features by Chi-Square Score')
        ax.set_xlabel('Chi-Square Score')
    elif method == 'anova_f':
        ax.set_title('Top Features by F-Score (ANOVA)')
        ax.set_xlabel('F-Score')
    elif method == 'mutual_info':
        ax.set_title('Top Features by Mutual Information')
        ax.set_xlabel('Mutual Information Score')
    
    ax.set_ylabel('Feature')
    
    plt.tight_layout()
    
    # Create figure for effect sizes if requested
    if show_effect_size and 'Effect Size' in feature_scores.columns:
        has_effect_sizes = feature_scores['Effect Size'].notna().any()
        
        if has_effect_sizes:
            # Sort by effect size
            effect_df = feature_scores.sort_values('Effect Size', ascending=False).head(top_n)
            
            # Create figure
            fig_effect, ax_effect = plt.subplots(figsize=figsize)
            
            # Plot effect sizes
            sns.barplot(
                y='Feature',
                x='Effect Size',
                data=effect_df,
                ax=ax_effect
            )
            
            # Add title and labels
            if method == 'chi2':
                ax_effect.set_title("Top Features by Cramer's V (Effect Size)")
                ax_effect.set_xlabel("Cramer's V")
            elif method == 'anova_f':
                ax_effect.set_title('Top Features by Eta-Squared (Effect Size)')
                ax_effect.set_xlabel('Eta-Squared')
            
            ax_effect.set_ylabel('Feature')
            
            plt.tight_layout()
            
            return fig, fig_effect
    
    return fig