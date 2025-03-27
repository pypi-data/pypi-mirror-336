"""
Automatic parameter selection for deduplication.

This module provides intelligent parameter selection for deduplication tasks,
based on dataset characteristics, memory constraints, and desired accuracy.
"""

import numpy as np
import pandas as pd
import psutil
import math
import logging
from typing import Dict, List, Any, Tuple, Optional, Union, Set
import sys

logger = logging.getLogger(__name__)

# Constants for parameter selection
DEFAULT_MEMORY_LIMIT_GB = 4.0  # Default memory limit for deduplication in GB
MIN_LSH_DATASET_SIZE = 5000    # Minimum dataset size for using LSH
MIN_BLOCKING_DATASET_SIZE = 1000  # Minimum dataset size for using blocking
MAX_MEMORY_PERCENTAGE = 0.75   # Max percentage of available memory to use


def estimate_memory_usage(
    df_size: int, 
    comparison_count: int,
    feature_count: int
) -> float:
    """
    Estimate memory usage for deduplication in GB.
    
    Parameters
    ----------
    df_size : int
        Number of rows in the dataframe
    comparison_count : int
        Estimated number of pairwise comparisons
    feature_count : int
        Number of features/columns used for comparison
        
    Returns
    -------
    float
        Estimated memory usage in GB
    """
    # Base memory for the dataframe and overhead
    base_memory_mb = df_size * feature_count * 8 / 1024
    
    # Memory for graph structures and comparison results
    # Each edge takes ~16 bytes, we assume ~10% of comparisons will create edges
    edge_memory_mb = (comparison_count * 0.1 * 16) / (1024 * 1024)
    
    # Memory for intermediate data structures
    aux_memory_mb = df_size * 64 / 1024
    
    total_memory_gb = (base_memory_mb + edge_memory_mb + aux_memory_mb) / 1024
    
    # Add 20% buffer
    return total_memory_gb * 1.2


def get_available_memory_gb() -> float:
    """
    Get available system memory in GB.
    
    Returns
    -------
    float
        Available memory in GB
    """
    try:
        return psutil.virtual_memory().available / (1024**3)
    except Exception as e:
        logger.warning(f"Error getting system memory: {e}. Using default value.")
        return DEFAULT_MEMORY_LIMIT_GB


def calculate_optimal_chunk_size(df_size: int, feature_count: int) -> int:
    """
    Calculate optimal chunk size based on dataset size and available memory.
    
    Parameters
    ----------
    df_size : int
        Number of rows in the dataframe
    feature_count : int
        Number of features/columns used for comparison
        
    Returns
    -------
    int
        Optimal chunk size
    """
    available_memory_gb = get_available_memory_gb() * MAX_MEMORY_PERCENTAGE
    
    # Calculate the maximum chunk size that would use the available memory
    # We use a simple quadratic model because the memory usage grows quadratically
    # with chunk size due to pairwise comparisons
    
    # Start with a default guess based on data size
    if df_size < 10000:
        chunk_size = 2000
    elif df_size < 50000:
        chunk_size = 1000
    elif df_size < 100000:
        chunk_size = 500
    else:
        chunk_size = 200
    
    # Refine based on available memory
    # Each comparison requires ~100 bytes including overhead
    comparisons_per_memory_gb = 10000000  # 10M comparisons per GB
    max_comparisons = comparisons_per_memory_gb * available_memory_gb
    
    # Solve for chunk_size where chunk_size^2 <= max_comparisons
    max_chunk_size = int(math.sqrt(max_comparisons))
    
    # Use the smaller of our default or memory-based size
    return min(chunk_size, max_chunk_size)


def calculate_max_comparisons(df_size: int, feature_count: int) -> Optional[int]:
    """
    Calculate the maximum number of comparisons based on dataset size and memory constraints.
    
    Parameters
    ----------
    df_size : int
        Number of rows in the dataframe
    feature_count : int
        Number of features/columns used for comparison
        
    Returns
    -------
    Optional[int]
        Maximum number of comparisons to perform, or None if no limit is needed
    """
    # For small datasets, no need to limit comparisons
    if df_size < 5000:
        return None
    
    available_memory_gb = get_available_memory_gb() * MAX_MEMORY_PERCENTAGE
    
    # Each comparison requires ~100 bytes including overhead
    comparisons_per_memory_gb = 10000000  # 10M comparisons per GB
    max_comparisons = int(comparisons_per_memory_gb * available_memory_gb)
    
    # Calculate total possible comparisons
    total_comparisons = (df_size * (df_size - 1)) // 2
    
    # If we can do all comparisons, return None (no limit)
    if total_comparisons <= max_comparisons:
        return None
    
    # Otherwise, return the maximum we can handle
    # We set a minimum to ensure reasonable results
    return max(10000, max_comparisons)


def should_use_lsh(df_size: int, columns: List[str]) -> bool:
    """
    Determine if LSH should be used based on dataset size and column types.
    
    Parameters
    ----------
    df_size : int
        Number of rows in the dataframe
    columns : List[str]
        Columns used for deduplication
        
    Returns
    -------
    bool
        Whether to use LSH
    """
    # For very small datasets, LSH overhead isn't worth it
    if df_size < MIN_LSH_DATASET_SIZE:
        return False
    
    # For medium datasets, use LSH
    if df_size >= MIN_LSH_DATASET_SIZE:
        return True
    
    return False


def should_use_blocking(df_size: int, columns: List[str]) -> bool:
    """
    Determine if blocking should be used based on dataset size.
    
    Parameters
    ----------
    df_size : int
        Number of rows in the dataframe
    columns : List[str]
        Columns used for deduplication
        
    Returns
    -------
    bool
        Whether to use blocking
    """
    # For very small datasets, blocking overhead isn't worth it
    if df_size < MIN_BLOCKING_DATASET_SIZE:
        return False
    
    # For larger datasets, use blocking
    return True


def get_optimal_blocking_columns(
    df: Any, 
    columns: List[str],
    blocking_columns: Optional[List[str]] = None
) -> List[str]:
    """
    Identify optimal columns for blocking based on cardinality and data types.
    
    Parameters
    ----------
    df : Any
        Input dataframe
    columns : List[str]
        Columns used for deduplication
    blocking_columns : Optional[List[str]], default=None
        User-provided blocking columns to consider
        
    Returns
    -------
    List[str]
        Optimal columns to use for blocking
    """
    # If user specified blocking columns, use them
    if blocking_columns:
        return blocking_columns
    
    # Find categorical columns with reasonable cardinality for blocking
    categorical_cols = []
    numerical_cols = []
    
    for col in df.columns:
        # Skip columns not in the original comparison set
        if col not in columns:
            continue
        
        # Check if column is categorical or numerical
        try:
            dtype = df[col].dtype
            if pd.api.types.is_categorical_dtype(dtype) or pd.api.types.is_object_dtype(dtype):
                # Check cardinality (not too high, not too low)
                cardinality = df[col].nunique()
                
                # Aim for columns that split the data into reasonable-sized chunks
                if 10 <= cardinality <= df.shape[0] // 10:
                    categorical_cols.append((col, cardinality))
            elif pd.api.types.is_numeric_dtype(dtype):
                numerical_cols.append(col)
        except Exception:
            # Skip columns that can't be analyzed
            continue
    
    # Sort categorical columns by cardinality (moderate cardinality is better for blocking)
    sorted_categorical = sorted(categorical_cols, key=lambda x: abs(x[1] - df.shape[0] // 100))
    
    # If we have good categorical columns, use them
    if sorted_categorical:
        # Use the best 1-2 categorical columns
        return [col for col, _ in sorted_categorical[:2]]
    
    # If no good categorical columns, use numerical columns with binning
    if numerical_cols:
        return [numerical_cols[0]]
    
    # If no suitable columns, return an empty list
    return []


def get_optimal_lsh_parameters(
    df_size: int, 
    threshold: float,
    text_dominant: bool = True
) -> Dict[str, Any]:
    """
    Calculate optimal LSH parameters based on dataset size and threshold.
    
    Parameters
    ----------
    df_size : int
        Number of rows in the dataframe
    threshold : float
        Similarity threshold for deduplication
    text_dominant : bool, default=True
        Whether text columns dominate the similarity calculation
        
    Returns
    -------
    Dict[str, Any]
        Dictionary of optimal LSH parameters
    """
    if text_dominant:
        # MinHash LSH parameter optimization
        
        # Higher thresholds need more permutations for accuracy
        if threshold > 0.9:
            num_perm = 256
        elif threshold > 0.8:
            num_perm = 192
        elif threshold > 0.7:
            num_perm = 128
        else:
            num_perm = 96
            
        # For very large datasets, use fewer permutations to save memory
        if df_size > 100000:
            num_perm = max(64, num_perm // 2)
            
        # Calculate optimal bands and rows
        # Following the rule: threshold ≈ (1/b)^(1/r)
        # where b = number of bands, r = rows per band
        
        # Initial estimate of rows per band
        rows_per_band = int(math.log(1 / threshold) * 10)
        rows_per_band = max(2, min(8, rows_per_band))
        
        # Calculate bands
        num_bands = num_perm // rows_per_band
        
        return {
            'lsh_method': 'minhash',
            'num_perm': num_perm,
            'num_bands': num_bands,
            'rows_per_band': rows_per_band,
            'lsh_threshold': threshold * 0.9  # Slightly lower threshold for LSH to catch more candidates
        }
    else:
        # Random Projection LSH parameters for numerical data
        return {
            'lsh_method': 'random_projection',
            'num_perm': 16,
            'lsh_threshold': threshold * 0.9
        }


def analyze_column_types(df: Any, columns: List[str]) -> bool:
    """
    Analyze columns to determine if text or numerical data dominates.
    
    Parameters
    ----------
    df : Any
        Input dataframe
    columns : List[str]
        Columns to analyze
        
    Returns
    -------
    bool
        True if text data dominates, False if numerical data dominates
    """
    text_cols = 0
    num_cols = 0
    
    for col in columns:
        if col not in df.columns:
            continue
        
        dtype = df[col].dtype
        if pd.api.types.is_string_dtype(dtype) or pd.api.types.is_object_dtype(dtype):
            # Sample some values to confirm these are actually text fields
            sample = df[col].dropna().sample(min(10, len(df[col].dropna()))).astype(str)
            text_cols += 1
        elif pd.api.types.is_numeric_dtype(dtype):
            num_cols += 1
    
    # If text columns are dominant or equal, prefer text-based methods
    return text_cols >= num_cols


def recommend_deduplication_parameters(
    df: Any, 
    columns: List[str],
    threshold: float = 0.8,
    weights: Optional[Dict[str, float]] = None,
    blocking_columns: Optional[List[str]] = None,
    memory_limit_gb: Optional[float] = None
) -> Dict[str, Any]:
    """
    Recommend optimal deduplication parameters based on dataset characteristics.
    
    Parameters
    ----------
    df : Any
        Input dataframe
    columns : List[str]
        Columns to use for deduplication
    threshold : float, default=0.8
        Similarity threshold
    weights : Optional[Dict[str, float]], default=None
        Weight for each column in similarity calculation
    blocking_columns : Optional[List[str]], default=None
        User-suggested columns for blocking
    memory_limit_gb : Optional[float], default=None
        Memory limit for deduplication in GB
        
    Returns
    -------
    Dict[str, Any]
        Dictionary of recommended parameters
    """
    df_size = len(df)
    feature_count = len(columns)
    
    # Set memory limit
    if memory_limit_gb is None:
        memory_limit_gb = get_available_memory_gb() * MAX_MEMORY_PERCENTAGE
    
    # Determine if we should use LSH
    use_lsh = should_use_lsh(df_size, columns)
    
    # Determine if we should use blocking
    use_blocking = should_use_blocking(df_size, columns)
    
    # Calculate optimal chunk size if needed
    if df_size > MIN_BLOCKING_DATASET_SIZE:
        chunk_size = calculate_optimal_chunk_size(df_size, feature_count)
    else:
        chunk_size = None
    
    # Calculate max comparisons if needed
    max_comparisons = calculate_max_comparisons(df_size, feature_count)
    
    # Determine optimal blocking columns if using blocking
    if use_blocking:
        blocking_cols = get_optimal_blocking_columns(df, columns, blocking_columns)
        blocking_method = 'exact'  # Default to exact blocking for simplicity
    else:
        blocking_cols = None
        blocking_method = None
    
    # Determine LSH parameters if using LSH
    if use_lsh:
        text_dominant = analyze_column_types(df, columns)
        lsh_params = get_optimal_lsh_parameters(df_size, threshold, text_dominant)
    else:
        lsh_params = {}
    
    # Calculate max block size if using blocking
    max_block_size = None
    if use_blocking and blocking_cols:
        # Max block size should be reasonable for memory but still large enough for useful comparisons
        # For large datasets, use smaller blocks
        if df_size > 100000:
            max_block_size = 1000
        elif df_size > 50000:
            max_block_size = 2000
        elif df_size > 10000:
            max_block_size = 5000
        else:
            max_block_size = 10000
    
    # Build final recommendation
    recommendation = {
        'use_lsh': use_lsh,
        'use_blocking': use_blocking,
        'chunk_size': chunk_size,
        'max_comparisons': max_comparisons,
        'n_jobs': min(psutil.cpu_count() or 1, 4)  # Use up to 4 cores by default
    }
    
    # Add blocking parameters if using blocking
    if use_blocking:
        recommendation.update({
            'blocking_columns': blocking_cols,
            'blocking_method': blocking_method,
            'max_block_size': max_block_size
        })
    
    # Add LSH parameters if using LSH
    if use_lsh:
        recommendation.update(lsh_params)
    
    return recommendation


def apply_auto_params(
    df: Any,
    columns: List[str],
    **kwargs
) -> Dict[str, Any]:
    """
    Apply automatic parameter selection to the deduplication parameters.
    
    This function integrates with flag_similar_records to provide automatic
    parameter selection based on dataset characteristics.
    
    Parameters
    ----------
    df : Any
        Input dataframe
    columns : List[str]
        Columns to use for deduplication
    **kwargs : dict
        Additional parameters passed to flag_similar_records
        
    Returns
    -------
    Dict[str, Any]
        Combined parameters for flag_similar_records
    """
    # Extract parameters that affect optimization
    threshold = kwargs.get('threshold', 0.8)
    weights = kwargs.get('weights', None)
    blocking_columns = kwargs.get('blocking_columns', None)
    memory_limit_gb = kwargs.get('memory_limit_gb', None)
    
    # Get recommended parameters
    recommended = recommend_deduplication_parameters(
        df=df,
        columns=columns,
        threshold=threshold,
        weights=weights,
        blocking_columns=blocking_columns,
        memory_limit_gb=memory_limit_gb
    )
    
    # Log recommended parameters
    logger.info(f"Auto-selected deduplication parameters: {recommended}")
    if 'show_progress' in kwargs and kwargs['show_progress']:
        print(f"Auto-selected deduplication parameters: {recommended}")
    
    # Combine recommended parameters with user-provided parameters
    # User-provided parameters take precedence
    combined_params = {}
    combined_params.update(recommended)
    combined_params.update({k: v for k, v in kwargs.items() if v is not None})
    
    return combined_params