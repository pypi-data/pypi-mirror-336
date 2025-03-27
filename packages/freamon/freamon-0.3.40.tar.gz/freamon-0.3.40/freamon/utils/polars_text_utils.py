"""
Polars-optimized utility functions for text processing.

This module provides Polars-optimized versions of common text processing functions,
which can significantly improve performance for large datasets.
"""
import re
import time
import warnings
import numpy as np
import pandas as pd
import polars as pl
from typing import List, Dict, Tuple, Union, Optional, Any, Callable, Iterator
from collections import Counter
import multiprocessing
from functools import partial

# Check if we have access to the deduplication functions
try:
    from freamon.deduplication.polars_lsh_deduplication import (
        polars_lsh_deduplication,
        batch_process_texts,
        streaming_lsh_deduplication
    )
    HAS_POLARS_DEDUPLICATION = True
except ImportError:
    HAS_POLARS_DEDUPLICATION = False
    warnings.warn("Polars LSH deduplication not available")

from freamon.utils.text_utils import TextProcessor
from freamon.utils.dataframe_utils import check_dataframe_type, convert_dataframe


def batch_vectorize_texts(
    texts: List[str],
    vectorizer_func: Callable,
    batch_size: int = 10000,
    show_progress: bool = False
) -> Any:
    """
    Vectorize a large collection of texts in batches to avoid memory issues.
    
    Parameters
    ----------
    texts : List[str]
        The texts to vectorize.
    vectorizer_func : Callable
        A function that takes a list of texts and returns a vectorized representation.
    batch_size : int, default=10000
        The number of texts to process in each batch.
    show_progress : bool, default=False
        Whether to show progress information.
        
    Returns
    -------
    Any
        The combined vectorized representation of all texts.
        
    Examples
    --------
    >>> from sklearn.feature_extraction.text import CountVectorizer
    >>> texts = ["First document", "Second document", "Third one"]
    >>> vectorizer = CountVectorizer().fit(texts)
    >>> vectorizer_func = lambda t: vectorizer.transform(t)
    >>> vectors = batch_vectorize_texts(texts, vectorizer_func, batch_size=2)
    >>> vectors.shape[0] == len(texts)
    True
    """
    import scipy.sparse as sp
    
    # Initialize batches
    n_texts = len(texts)
    n_batches = (n_texts + batch_size - 1) // batch_size
    
    if show_progress:
        print(f"Vectorizing {n_texts} texts in {n_batches} batches")
    
    # Process the first batch to get the dimensionality
    end_idx = min(batch_size, n_texts)
    first_batch = vectorizer_func(texts[:end_idx])
    
    # If it's already a numpy array or we only have one batch, return it
    if n_batches == 1:
        return first_batch
    
    # For sparse matrices, process in batches
    if sp.issparse(first_batch):
        results = [first_batch]
        
        for i in range(1, n_batches):
            start_idx = i * batch_size
            end_idx = min((i + 1) * batch_size, n_texts)
            
            if show_progress:
                print(f"Processing batch {i+1}/{n_batches}")
                
            batch = vectorizer_func(texts[start_idx:end_idx])
            results.append(batch)
        
        # Combine the sparse matrices
        return sp.vstack(results)
    else:
        # For dense arrays
        results = [first_batch]
        
        for i in range(1, n_batches):
            start_idx = i * batch_size
            end_idx = min((i + 1) * batch_size, n_texts)
            
            if show_progress:
                print(f"Processing batch {i+1}/{n_batches}")
                
            batch = vectorizer_func(texts[start_idx:end_idx])
            results.append(batch)
        
        # Combine the dense arrays
        return np.vstack(results)


def process_text_column(
    df: Union[pd.DataFrame, pl.DataFrame],
    text_column: str,
    processor: Optional[TextProcessor] = None,
    lowercase: bool = True,
    remove_punctuation: bool = True,
    remove_stopwords: bool = True,
    lemmatize: bool = False,
    batch_size: int = 10000,
    n_jobs: int = 1,
    show_progress: bool = False
) -> Union[pd.DataFrame, pl.DataFrame]:
    """
    Process a text column in a dataframe using Polars optimizations when available.
    
    Parameters
    ----------
    df : Union[pd.DataFrame, pl.DataFrame]
        The dataframe containing the text column.
    text_column : str
        The name of the column containing texts to process.
    processor : Optional[TextProcessor], default=None
        Instance of TextProcessor for text preprocessing. If None, a new one will be created.
    lowercase : bool, default=True
        Whether to convert texts to lowercase.
    remove_punctuation : bool, default=True
        Whether to remove punctuation.
    remove_stopwords : bool, default=True
        Whether to remove stopwords.
    lemmatize : bool, default=False
        Whether to lemmatize words.
    batch_size : int, default=10000
        The number of texts to process in each batch.
    n_jobs : int, default=1
        Number of parallel jobs to run. If -1, use all available cores.
    show_progress : bool, default=False
        Whether to show progress information.
        
    Returns
    -------
    Union[pd.DataFrame, pl.DataFrame]
        Dataframe with processed text column. Returns same type as input.
        
    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({'text': ["First document!", "Second, document.", "THIRD ONE!"]})
    >>> processed_df = process_text_column(df, 'text')
    >>> processed_df['text'].tolist()
    ['first document', 'second document', 'third one']
    """
    # Check dataframe type
    df_type = check_dataframe_type(df)
    
    # Create text processor if not provided
    if processor is None:
        processor = TextProcessor()
    
    # Convert to pandas for processing if necessary
    if df_type == "polars":
        df_pandas = convert_dataframe(df, "pandas")
    else:
        df_pandas = df
    
    # Get the texts
    texts = df_pandas[text_column].tolist()
    
    # Process texts in parallel
    if n_jobs != 1:
        # Determine number of jobs
        if n_jobs == -1:
            n_jobs = multiprocessing.cpu_count()
        
        # Split texts into n_jobs chunks
        chunk_size = (len(texts) + n_jobs - 1) // n_jobs
        chunks = [texts[i:i+chunk_size] for i in range(0, len(texts), chunk_size)]
        
        # Process each chunk in parallel
        process_func = partial(
            _process_texts_batch,
            processor=processor,
            lowercase=lowercase,
            remove_punctuation=remove_punctuation,
            remove_stopwords=remove_stopwords,
            lemmatize=lemmatize
        )
        
        with multiprocessing.Pool(n_jobs) as pool:
            processed_chunks = pool.map(process_func, chunks)
        
        # Combine results
        processed_texts = [item for sublist in processed_chunks for item in sublist]
    else:
        # Process in batches
        processed_texts = []
        n_batches = (len(texts) + batch_size - 1) // batch_size
        
        for i in range(n_batches):
            start_idx = i * batch_size
            end_idx = min((i + 1) * batch_size, len(texts))
            
            if show_progress and n_batches > 1:
                print(f"Processing batch {i+1}/{n_batches}")
                
            batch = texts[start_idx:end_idx]
            processed_batch = _process_texts_batch(
                batch,
                processor=processor,
                lowercase=lowercase,
                remove_punctuation=remove_punctuation,
                remove_stopwords=remove_stopwords,
                lemmatize=lemmatize
            )
            processed_texts.extend(processed_batch)
    
    # Create a new dataframe with processed texts
    result = df_pandas.copy()
    result[text_column] = processed_texts
    
    # Convert back to original type if necessary
    if df_type == "polars":
        return convert_dataframe(result, "polars")
    
    return result


def _process_texts_batch(
    texts: List[str],
    processor: TextProcessor,
    lowercase: bool = True,
    remove_punctuation: bool = True,
    remove_stopwords: bool = True,
    lemmatize: bool = False
) -> List[str]:
    """Process a batch of texts using the TextProcessor."""
    return [
        processor.preprocess_text(
            text,
            lowercase=lowercase,
            remove_punctuation=remove_punctuation,
            remove_stopwords=remove_stopwords,
            lemmatize=lemmatize
        )
        for text in texts
    ]


def deduplicate_text_column(
    df: Union[pd.DataFrame, pl.DataFrame],
    text_column: str,
    method: str = 'lsh',
    threshold: float = 0.8,
    keep: str = 'first',
    num_minhash_permutations: int = 100,
    num_bands: int = 20,
    preprocess: bool = True,
    processor: Optional[TextProcessor] = None,
    batch_size: int = 10000,
    return_similarity_dict: bool = False,
    show_progress: bool = False
) -> Union[pd.DataFrame, Union[Tuple[pd.DataFrame, Dict], Tuple[pl.DataFrame, Dict]]]:
    """
    Deduplicate a dataframe based on text similarity using Polars optimizations.
    
    Parameters
    ----------
    df : Union[pd.DataFrame, pl.DataFrame]
        The dataframe to deduplicate.
    text_column : str
        The name of the column containing texts to compare.
    method : str, default='lsh'
        The deduplication method: 'exact', 'lsh', or 'fuzzy'.
    threshold : float, default=0.8
        Similarity threshold for fuzzy deduplication.
    keep : str, default='first'
        Which instance to keep: 'first', 'last', or 'longest'.
    num_minhash_permutations : int, default=100
        Number of permutations for MinHash algorithm (only for 'lsh' method).
    num_bands : int, default=20
        Number of bands for LSH (only for 'lsh' method).
    preprocess : bool, default=True
        Whether to preprocess texts before comparison.
    processor : Optional[TextProcessor], default=None
        Instance of TextProcessor for text preprocessing. If None, a new one will be created.
    batch_size : int, default=10000
        The number of texts to process in each batch.
    return_similarity_dict : bool, default=False
        Whether to return the similarity dictionary along with the deduplicated dataframe.
    show_progress : bool, default=False
        Whether to show progress information.
        
    Returns
    -------
    Union[pd.DataFrame, Union[Tuple[pd.DataFrame, Dict], Tuple[pl.DataFrame, Dict]]]
        Deduplicated dataframe. If return_similarity_dict=True, also returns the similarity dictionary.
        Returns same type as input.
        
    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     'id': [1, 2, 3, 4],
    ...     'text': [
    ...         "This is a test document",
    ...         "A different document",
    ...         "This is a test document", # Exact duplicate
    ...         "This is a test document with slight difference"
    ...     ]
    ... })
    >>> deduplicated_df = deduplicate_text_column(df, 'text', method='exact')
    >>> len(deduplicated_df)
    3
    """
    # Check dataframe type
    df_type = check_dataframe_type(df)
    
    # Convert to pandas for processing if necessary
    if df_type == "polars":
        df_pandas = convert_dataframe(df, "pandas")
    else:
        df_pandas = df
    
    # Get the texts
    texts = df_pandas[text_column].tolist()
    
    # Create text processor if not provided
    if processor is None:
        processor = TextProcessor()
    
    # Deduplicate based on method
    if method == 'exact':
        # Use exact deduplication
        from freamon.deduplication.exact_deduplication import hash_deduplication
        
        if return_similarity_dict:
            unique_indices, similarity_dict = hash_deduplication(
                texts,
                keep=keep,
                return_duplicate_groups=True
            )
            result = df_pandas.iloc[unique_indices].copy()
            
            # Convert back to original type if necessary
            if df_type == "polars":
                return convert_dataframe(result, "polars"), similarity_dict
            return result, similarity_dict
        else:
            unique_indices = hash_deduplication(
                texts,
                keep=keep
            )
            result = df_pandas.iloc[unique_indices].copy()
            
            # Convert back to original type if necessary
            if df_type == "polars":
                return convert_dataframe(result, "polars")
            return result
        
    elif method == 'lsh':
        # Use LSH deduplication
        if HAS_POLARS_DEDUPLICATION:
            # Use optimized Polars implementation
            if return_similarity_dict:
                unique_indices, similarity_dict = polars_lsh_deduplication(
                    texts=texts,
                    threshold=threshold,
                    num_minhash_permutations=num_minhash_permutations,
                    num_bands=num_bands,
                    preprocess=preprocess,
                    text_processor=processor,
                    batch_size=batch_size,
                    keep=keep,
                    return_similarity_dict=True,
                    show_progress=show_progress
                )
                result = df_pandas.iloc[unique_indices].copy()
                
                # Convert back to original type if necessary
                if df_type == "polars":
                    return convert_dataframe(result, "polars"), similarity_dict
                return result, similarity_dict
            else:
                unique_indices = polars_lsh_deduplication(
                    texts=texts,
                    threshold=threshold,
                    num_minhash_permutations=num_minhash_permutations,
                    num_bands=num_bands,
                    preprocess=preprocess,
                    text_processor=processor,
                    batch_size=batch_size,
                    keep=keep,
                    show_progress=show_progress
                )
                result = df_pandas.iloc[unique_indices].copy()
                
                # Convert back to original type if necessary
                if df_type == "polars":
                    return convert_dataframe(result, "polars")
                return result
        else:
            # Fall back to standard implementation
            from freamon.deduplication.lsh_deduplication import lsh_deduplication
            
            if return_similarity_dict:
                unique_indices, similarity_dict = lsh_deduplication(
                    texts=texts,
                    threshold=threshold,
                    num_minhash_permutations=num_minhash_permutations,
                    num_bands=num_bands,
                    preprocess=preprocess,
                    keep=keep,
                    return_similarity_dict=True
                )
                result = df_pandas.iloc[unique_indices].copy()
                
                # Convert back to original type if necessary
                if df_type == "polars":
                    return convert_dataframe(result, "polars"), similarity_dict
                return result, similarity_dict
            else:
                unique_indices = lsh_deduplication(
                    texts=texts,
                    threshold=threshold,
                    num_minhash_permutations=num_minhash_permutations,
                    num_bands=num_bands,
                    preprocess=preprocess,
                    keep=keep
                )
                result = df_pandas.iloc[unique_indices].copy()
                
                # Convert back to original type if necessary
                if df_type == "polars":
                    return convert_dataframe(result, "polars")
                return result
    
    elif method == 'fuzzy':
        # Use fuzzy deduplication
        from freamon.deduplication.fuzzy_deduplication import deduplicate_texts
        
        unique_indices = deduplicate_texts(
            texts=texts,
            threshold=threshold,
            preprocess=preprocess,
            keep=keep
        )
        result = df_pandas.iloc[unique_indices].copy()
        
        # For fuzzy deduplication, we don't have a similarity dict
        if return_similarity_dict:
            # Create a simple mapping
            similarity_dict = {}
            for i, idx in enumerate(unique_indices):
                similarity_dict[i] = [idx]
            
            # Convert back to original type if necessary
            if df_type == "polars":
                return convert_dataframe(result, "polars"), similarity_dict
            return result, similarity_dict
        else:
            # Convert back to original type if necessary
            if df_type == "polars":
                return convert_dataframe(result, "polars")
            return result
    
    else:
        raise ValueError(f"Unknown deduplication method: {method}. Use 'exact', 'lsh', or 'fuzzy'.")


def batch_calculate_similarities(
    texts: List[str],
    reference_text: Optional[str] = None,
    method: str = 'cosine',
    processor: Optional[TextProcessor] = None,
    preprocess: bool = True,
    batch_size: int = 1000,
    show_progress: bool = False
) -> np.ndarray:
    """
    Calculate similarities between texts in batches using Polars optimizations.
    
    Parameters
    ----------
    texts : List[str]
        The texts to calculate similarities for.
    reference_text : Optional[str], default=None
        Reference text to compare against. If None, calculate pairwise similarities.
    method : str, default='cosine'
        Similarity method: 'cosine', 'jaccard', or 'levenshtein'.
    processor : Optional[TextProcessor], default=None
        Instance of TextProcessor for text preprocessing. If None, a new one will be created.
    preprocess : bool, default=True
        Whether to preprocess texts before comparison.
    batch_size : int, default=1000
        The number of texts to process in each batch.
    show_progress : bool, default=False
        Whether to show progress information.
        
    Returns
    -------
    np.ndarray
        Array of similarities. If reference_text is provided, shape is (len(texts),).
        Otherwise, shape is (len(texts), len(texts)).
        
    Examples
    --------
    >>> texts = ["First document", "Second document", "Completely different text"]
    >>> batch_calculate_similarities(texts, "First document")
    array([1.        , 0.33333333, 0.        ])
    """
    # Create text processor if not provided
    if processor is None:
        processor = TextProcessor()
    
    # Preprocess texts if needed
    if preprocess:
        processed_texts = []
        n_batches = (len(texts) + batch_size - 1) // batch_size
        
        for i in range(n_batches):
            start_idx = i * batch_size
            end_idx = min((i + 1) * batch_size, len(texts))
            
            if show_progress and n_batches > 1:
                print(f"Preprocessing batch {i+1}/{n_batches}")
                
            batch = texts[start_idx:end_idx]
            processed_batch = [
                processor.preprocess_text(
                    text, 
                    lowercase=True, 
                    remove_punctuation=True
                ) for text in batch
            ]
            processed_texts.extend(processed_batch)
    else:
        processed_texts = texts
    
    # If reference text is provided, calculate similarities against it
    if reference_text is not None:
        if preprocess:
            processed_reference = processor.preprocess_text(
                reference_text,
                lowercase=True,
                remove_punctuation=True
            )
        else:
            processed_reference = reference_text
        
        similarities = np.zeros(len(processed_texts))
        n_batches = (len(processed_texts) + batch_size - 1) // batch_size
        
        for i in range(n_batches):
            start_idx = i * batch_size
            end_idx = min((i + 1) * batch_size, len(processed_texts))
            
            if show_progress and n_batches > 1:
                print(f"Processing batch {i+1}/{n_batches}")
                
            batch = processed_texts[start_idx:end_idx]
            
            for j, text in enumerate(batch):
                if method == 'cosine':
                    similarities[start_idx + j] = processor.calculate_document_similarity(
                        processed_reference, text, method='cosine'
                    )
                elif method == 'jaccard':
                    from freamon.deduplication.fuzzy_deduplication import calculate_jaccard_similarity
                    similarities[start_idx + j] = calculate_jaccard_similarity(
                        processed_reference, text
                    )
                elif method == 'levenshtein':
                    from freamon.deduplication.fuzzy_deduplication import calculate_levenshtein_similarity
                    similarities[start_idx + j] = calculate_levenshtein_similarity(
                        processed_reference, text
                    )
                else:
                    raise ValueError(f"Unknown similarity method: {method}")
        
        return similarities
    
    # Otherwise, calculate pairwise similarities
    n_texts = len(processed_texts)
    similarities = np.zeros((n_texts, n_texts))
    
    # Fill diagonal with 1s (self-similarity)
    np.fill_diagonal(similarities, 1.0)
    
    # Calculate similarities for upper triangle only
    for i in range(n_texts):
        for j in range(i + 1, n_texts):
            if method == 'cosine':
                sim = processor.calculate_document_similarity(
                    processed_texts[i], processed_texts[j], method='cosine'
                )
            elif method == 'jaccard':
                from freamon.deduplication.fuzzy_deduplication import calculate_jaccard_similarity
                sim = calculate_jaccard_similarity(
                    processed_texts[i], processed_texts[j]
                )
            elif method == 'levenshtein':
                from freamon.deduplication.fuzzy_deduplication import calculate_levenshtein_similarity
                sim = calculate_levenshtein_similarity(
                    processed_texts[i], processed_texts[j]
                )
            else:
                raise ValueError(f"Unknown similarity method: {method}")
            
            # Fill both upper and lower triangle (symmetric matrix)
            similarities[i, j] = sim
            similarities[j, i] = sim
    
    return similarities