"""
Advanced Locality-Sensitive Hashing (LSH) implementations for efficient similarity search.

This module extends the core LSH functionality with additional algorithms:
1. SimHash: For efficient text similarity based on term frequency
2. TLSH: (Trend Micro Locality Sensitive Hash) for fuzzy matching of documents
3. BKTree: For edit distance similarity search
4. SuperMinHash: For more efficient MinHash signatures
"""

import numpy as np
from typing import List, Dict, Any, Callable, Tuple, Set, Union, Optional
import pandas as pd
import logging
from collections import defaultdict
import re
import math
import networkx as nx
import mmh3  # MurmurHash for SimHash implementation

logger = logging.getLogger(__name__)


class SimHash:
    """
    SimHash implementation for text similarity.
    
    SimHash is a locality-sensitive hashing algorithm that creates
    fingerprints of documents based on term frequency. It's particularly
    effective for finding near-duplicate documents.
    
    References
    ----------
    Charikar, M. S. (2002). Similarity estimation techniques from rounding algorithms.
    In Proceedings of the 34th Annual ACM Symposium on Theory of Computing (pp. 380-388).
    """
    
    def __init__(self, hash_bits: int = 64, tokenizer: Optional[Callable] = None):
        """
        Initialize SimHash with specified hash size.
        
        Parameters
        ----------
        hash_bits : int, default=64
            Number of bits in the hash (fingerprint size)
        tokenizer : Optional[Callable], default=None
            Function to convert text to tokens. If None, uses simple
            whitespace/punctuation tokenization
        """
        self.hash_bits = hash_bits
        self.tokenizer = tokenizer or self._default_tokenizer
    
    @staticmethod
    def _default_tokenizer(text: str) -> List[str]:
        """
        Default tokenization function that splits text into words.
        
        Parameters
        ----------
        text : str
            Input text to tokenize
            
        Returns
        -------
        List[str]
            List of tokens
        """
        # Convert to lowercase and remove punctuation
        text = text.lower()
        # Split into words
        return re.findall(r'\w+', text)
    
    def compute_hash(self, text: str) -> int:
        """
        Compute the SimHash of a text document.
        
        Parameters
        ----------
        text : str
            Input text document
            
        Returns
        -------
        int
            SimHash fingerprint
        """
        if not text or not isinstance(text, str):
            return 0
            
        # Tokenize the text
        tokens = self.tokenizer(text)
        
        if not tokens:
            return 0
            
        # Initialize vector for feature weighing
        v = [0] * self.hash_bits
        
        # For each token
        for token in tokens:
            # Compute a hash
            token_hash = mmh3.hash64(token.encode('utf-8'))[0]
            
            # For each bit in the hash
            for i in range(self.hash_bits):
                bit = (token_hash >> i) & 1
                if bit == 1:
                    v[i] += 1
                else:
                    v[i] -= 1
        
        # Convert weighted features to fingerprint
        fingerprint = 0
        for i in range(self.hash_bits):
            if v[i] > 0:
                fingerprint |= (1 << i)
        
        return fingerprint
    
    @staticmethod
    def hamming_distance(hash1: int, hash2: int) -> int:
        """
        Calculate the Hamming distance between two hashes.
        
        Parameters
        ----------
        hash1 : int
            First hash value
        hash2 : int
            Second hash value
            
        Returns
        -------
        int
            Hamming distance (number of differing bits)
        """
        # XOR the hashes, then count the number of 1 bits
        xor = hash1 ^ hash2
        distance = bin(xor).count('1')
        return distance
    
    @staticmethod
    def similarity(hash1: int, hash2: int, hash_bits: int = 64) -> float:
        """
        Calculate similarity between two SimHash fingerprints.
        
        Parameters
        ----------
        hash1 : int
            First hash value
        hash2 : int
            Second hash value
        hash_bits : int, default=64
            Number of bits in the hash
            
        Returns
        -------
        float
            Similarity between 0.0 and 1.0
        """
        distance = SimHash.hamming_distance(hash1, hash2)
        return 1.0 - (distance / hash_bits)


class BKTree:
    """
    Burkhard-Keller Tree for efficient edit distance matching.
    
    A BK-Tree is a tree data structure specialized for finding strings that
    are within a certain edit distance of a query string. It's particularly
    efficient for fuzzy matching and spell checking.
    
    References
    ----------
    Burkhard, W. A., & Keller, R. M. (1973). Some approaches to best-match
    file searching. Communications of the ACM, 16(4), 230-236.
    """
    
    def __init__(self, distance_func: Optional[Callable] = None):
        """
        Initialize BK-Tree with specified distance function.
        
        Parameters
        ----------
        distance_func : Optional[Callable], default=None
            Function to compute distance between two strings.
            If None, uses Levenshtein distance.
        """
        self.root = None
        self.distance_func = distance_func or self._levenshtein_distance
    
    @staticmethod
    def _levenshtein_distance(s1: str, s2: str) -> int:
        """
        Calculate Levenshtein (edit) distance between two strings.
        
        Parameters
        ----------
        s1 : str
            First string
        s2 : str
            Second string
            
        Returns
        -------
        int
            Edit distance
        """
        if len(s1) < len(s2):
            return BKTree._levenshtein_distance(s2, s1)
            
        if len(s2) == 0:
            return len(s1)
            
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
            
        return previous_row[-1]
    
    def add(self, word: str, data: Any = None) -> None:
        """
        Add a word to the BK-Tree.
        
        Parameters
        ----------
        word : str
            Word to add
        data : Any, default=None
            Associated data to store with the word
        """
        node = {'word': word, 'data': data, 'children': {}}
        
        if self.root is None:
            self.root = node
            return
            
        current = self.root
        while True:
            distance = self.distance_func(word, current['word'])
            
            # If the word is already in the tree, update data
            if distance == 0:
                current['data'] = data
                return
                
            # If there's already a child at this distance, go deeper
            if distance in current['children']:
                current = current['children'][distance]
            else:
                # Otherwise, add a new child at this distance
                current['children'][distance] = node
                return
    
    def find(self, word: str, max_distance: int) -> List[Tuple[str, Any, int]]:
        """
        Find all words within max_distance of the query word.
        
        Parameters
        ----------
        word : str
            Query word
        max_distance : int
            Maximum edit distance
            
        Returns
        -------
        List[Tuple[str, Any, int]]
            List of (word, data, distance) tuples
        """
        if self.root is None:
            return []
            
        results = []
        
        def search(node):
            distance = self.distance_func(word, node['word'])
            
            if distance <= max_distance:
                results.append((node['word'], node['data'], distance))
                
            # Search in children that could have matches
            for i in range(max(0, distance - max_distance), distance + max_distance + 1):
                if i in node['children']:
                    search(node['children'][i])
                    
        search(self.root)
        return sorted(results, key=lambda x: x[2])  # Sort by distance
    
    def find_most_similar(self, word: str, threshold: float = 0.8) -> Optional[Tuple[str, Any, float]]:
        """
        Find the most similar word with similarity above threshold.
        
        Parameters
        ----------
        word : str
            Query word
        threshold : float, default=0.8
            Minimum similarity threshold (0.0 to 1.0)
            
        Returns
        -------
        Optional[Tuple[str, Any, float]]
            (word, data, similarity) of most similar match, or None if no match found
        """
        max_distance = len(word)  # Maximum possible edit distance
        
        # Search with decreasing similarity threshold
        while max_distance > 0:
            matches = self.find(word, max_distance)
            
            if matches:
                # Calculate similarity (1.0 - distance/max(len(s1),len(s2)))
                best_match = min(matches, key=lambda x: x[2])
                best_word, best_data, best_distance = best_match
                
                max_len = max(len(word), len(best_word))
                if max_len == 0:
                    similarity = 1.0
                else:
                    similarity = 1.0 - (best_distance / max_len)
                    
                if similarity >= threshold:
                    return (best_word, best_data, similarity)
                    
            # Reduce max_distance to increase similarity threshold
            max_distance -= 1
            
        return None


class SuperMinHash:
    """
    SuperMinHash implementation for more efficient MinHash signatures.
    
    SuperMinHash is a more efficient variant of MinHash that requires fewer
    hash functions while maintaining accuracy. It's useful for large-scale 
    similarity search applications.
    
    References
    ----------
    Ertl, O. (2019). SuperMinHash - A New Minwise Hashing Algorithm for Jaccard
    Similarity Estimation. arXiv preprint arXiv:1909.07424.
    """
    
    def __init__(self, num_perm: int = 128, seed: int = 42):
        """
        Initialize SuperMinHash with specified parameters.
        
        Parameters
        ----------
        num_perm : int, default=128
            Number of permutations
        seed : int, default=42
            Random seed for initialization
        """
        self.num_perm = num_perm
        self.seed = seed
        self._init_hash_functions()
    
    def _init_hash_functions(self) -> None:
        """
        Initialize hash functions and random state variables.
        """
        # Set random seed for reproducibility
        np.random.seed(self.seed)
        
        # Generate random a and b for (ax + b) % p hash functions
        self.p = (1 << 31) - 1  # Prime number for hash function
        self.a = np.random.randint(1, self.p, self.num_perm, dtype=np.int64)
        self.b = np.random.randint(0, self.p, self.num_perm, dtype=np.int64)
        
        # Random permutation values for SuperMinHash
        self.pi = np.zeros((self.num_perm, self.num_perm), dtype=np.int32)
        for i in range(self.num_perm):
            self.pi[i] = np.random.permutation(self.num_perm)
        
        # Random offset values for SuperMinHash
        self.beta = np.random.random(self.num_perm)
    
    def compute_signature(self, tokens: List[str]) -> np.ndarray:
        """
        Compute SuperMinHash signature for a set of tokens.
        
        Parameters
        ----------
        tokens : List[str]
            List of tokens representing the set
            
        Returns
        -------
        np.ndarray
            SuperMinHash signature
        """
        if not tokens:
            return np.zeros(self.num_perm, dtype=np.float64)
            
        # Initialize hashes array with infinity
        hashes = np.full(self.num_perm, np.inf, dtype=np.float64)
        
        # Process each token
        for token in tokens:
            # Hash the token using MurmurHash
            hash_val = mmh3.hash64(token.encode('utf-8'))[0] & 0x7FFFFFFF
            
            # Apply SuperMinHash algorithm
            for i in range(self.num_perm):
                # Compute hash for this permutation
                h = (self.a[i] * hash_val + self.b[i]) % self.p
                r = (h / self.p) + self.beta[i]
                while r >= 1:
                    r -= 1
                
                # Get permutation index
                k = int(r * self.num_perm)
                
                # Check if we have a new minimum
                if r < hashes[self.pi[i][k]]:
                    hashes[self.pi[i][k]] = r
        
        return hashes
    
    @staticmethod
    def jaccard_similarity(sig1: np.ndarray, sig2: np.ndarray) -> float:
        """
        Calculate Jaccard similarity between two SuperMinHash signatures.
        
        Parameters
        ----------
        sig1 : np.ndarray
            First signature
        sig2 : np.ndarray
            Second signature
            
        Returns
        -------
        float
            Estimated Jaccard similarity
        """
        if sig1.shape != sig2.shape:
            raise ValueError("Signatures must have the same shape")
            
        # Calculate element-wise equality
        equal_count = np.sum(np.isclose(sig1, sig2))
        
        # Return similarity estimate
        return equal_count / len(sig1)


def create_simhash_signatures(
    df: Any,
    columns: List[str],
    weights: Optional[Dict[str, float]] = None,
    hash_bits: int = 64
) -> Dict[int, int]:
    """
    Create SimHash signatures for texts in a dataframe.
    
    Parameters
    ----------
    df : Any
        Input dataframe
    columns : List[str]
        Columns to use for creating signatures
    weights : Optional[Dict[str, float]], default=None
        Weights for each column
    hash_bits : int, default=64
        Size of hash fingerprints in bits
        
    Returns
    -------
    Dict[int, int]
        Dictionary mapping row indices to SimHash signatures
    """
    # Initialize SimHash
    simhash = SimHash(hash_bits=hash_bits)
    
    # Set default weights if not provided
    if weights is None:
        weights = {col: 1.0 / len(columns) for col in columns}
    
    # Normalize weights to sum to 1
    total_weight = sum(weights.values())
    norm_weights = {col: weights.get(col, 0) / total_weight for col in columns}
    
    # Generate signatures for each row
    signatures = {}
    for idx, row in df.iterrows():
        # Compute weighted SimHash for all columns
        combined_hash = 0
        total_col_weight = 0
        
        for col in columns:
            if col not in row or pd.isna(row[col]):
                continue
                
            try:
                # Convert to string if necessary
                val = str(row[col]) if not isinstance(row[col], str) else row[col]
                
                # Compute hash for this column
                col_hash = simhash.compute_hash(val)
                
                # Apply weight
                weight = norm_weights.get(col, 0)
                if weight > 0:
                    # Use bitwise OR with precedence based on weight
                    if combined_hash == 0:
                        combined_hash = col_hash
                    else:
                        # XOR the bits where they differ, weighted by column importance
                        diff_bits = combined_hash ^ col_hash
                        for bit_pos in range(hash_bits):
                            bit_mask = 1 << bit_pos
                            if diff_bits & bit_mask:
                                # If bits differ, use weighted decision
                                if np.random.random() < weight:
                                    # Take bit from column hash
                                    if col_hash & bit_mask:
                                        combined_hash |= bit_mask
                                    else:
                                        combined_hash &= ~bit_mask
                    
                    total_col_weight += weight
            except Exception as e:
                logger.debug(f"Error computing SimHash for {col}: {e}")
                continue
        
        # Store the combined hash
        signatures[idx] = combined_hash
    
    return signatures


def find_similar_pairs_simhash(
    signatures: Dict[int, int],
    threshold: float = 0.8,
    hash_bits: int = 64
) -> Set[Tuple[int, int]]:
    """
    Find similar pairs using SimHash signatures.
    
    Parameters
    ----------
    signatures : Dict[int, int]
        Dictionary mapping indices to SimHash signatures
    threshold : float, default=0.8
        Similarity threshold
    hash_bits : int, default=64
        Size of hash fingerprints in bits
        
    Returns
    -------
    Set[Tuple[int, int]]
        Set of similar pairs (idx1, idx2)
    """
    # Convert threshold to maximum Hamming distance
    max_distance = int((1 - threshold) * hash_bits)
    
    # Find similar pairs by comparing hashes
    similar_pairs = set()
    indices = list(signatures.keys())
    
    # For each pair of indices
    for i in range(len(indices)):
        idx1 = indices[i]
        hash1 = signatures[idx1]
        
        for j in range(i + 1, len(indices)):
            idx2 = indices[j]
            hash2 = signatures[idx2]
            
            # Calculate Hamming distance
            distance = SimHash.hamming_distance(hash1, hash2)
            
            # If distance is within threshold, add to similar pairs
            if distance <= max_distance:
                # Ensure consistent ordering of pairs
                similar_pairs.add((min(idx1, idx2), max(idx1, idx2)))
    
    return similar_pairs


def build_bktree_index(
    df: Any,
    column: str,
    preprocess: bool = True
) -> BKTree:
    """
    Build a BK-Tree index for a text column in a dataframe.
    
    Parameters
    ----------
    df : Any
        Input dataframe
    column : str
        Column to index
    preprocess : bool, default=True
        Whether to preprocess text (lowercase, remove punctuation)
        
    Returns
    -------
    BKTree
        BK-Tree index
    """
    # Initialize BK-Tree
    bktree = BKTree()
    
    # Add each value to the tree
    for idx, row in df.iterrows():
        if column not in row or pd.isna(row[column]):
            continue
            
        try:
            # Convert to string if necessary
            val = str(row[column]) if not isinstance(row[column], str) else row[column]
            
            # Preprocess if required
            if preprocess:
                val = val.lower()
                val = re.sub(r'[^\w\s]', '', val)
            
            # Add to tree with row index as data
            bktree.add(val, idx)
        except Exception as e:
            logger.debug(f"Error adding {val} to BK-Tree: {e}")
            continue
    
    return bktree


def find_similar_text_bktree(
    df: Any,
    query_column: str,
    index_column: str,
    threshold: float = 0.8,
    preprocess: bool = True,
    max_results: int = 10
) -> Dict[Any, List[Tuple[Any, float]]]:
    """
    Find similar texts using BK-Tree for efficient edit distance matching.
    
    Parameters
    ----------
    df : Any
        Input dataframe
    query_column : str
        Column with query texts
    index_column : str
        Column to build the index on (can be the same as query_column)
    threshold : float, default=0.8
        Similarity threshold (0.0 to 1.0)
    preprocess : bool, default=True
        Whether to preprocess text
    max_results : int, default=10
        Maximum number of results to return per query
        
    Returns
    -------
    Dict[Any, List[Tuple[Any, float]]]
        Dictionary mapping row indices to lists of (similar_idx, similarity) pairs
    """
    # Build BK-Tree index on index_column
    bktree = build_bktree_index(df, index_column, preprocess=preprocess)
    
    # Find similar texts for each query
    results = {}
    
    for idx, row in df.iterrows():
        if query_column not in row or pd.isna(row[query_column]):
            continue
            
        try:
            # Convert to string if necessary
            query = str(row[query_column]) if not isinstance(row[query_column], str) else row[query_column]
            
            # Preprocess if required
            if preprocess:
                query = query.lower()
                query = re.sub(r'[^\w\s]', '', query)
            
            # Calculate maximum edit distance based on threshold
            # Use a more forgiving max_distance formula to catch more candidates
            max_distance = len(query) + 1 - int(len(query) * threshold)
            
            # Find similar texts
            similar = bktree.find(query, max_distance)
            
            # Filter by similarity threshold and convert to (idx, similarity)
            similar_texts = []
            for match_text, match_idx, distance in similar:
                # Skip self-matches
                if match_idx == idx:
                    continue
                    
                # Calculate similarity
                max_len = max(len(query), len(match_text))
                if max_len == 0:
                    similarity = 1.0
                else:
                    similarity = 1.0 - (distance / max_len)
                    
                if similarity >= threshold:
                    similar_texts.append((match_idx, similarity))
            
            # Sort by similarity (descending) and limit to max_results
            similar_texts.sort(key=lambda x: x[1], reverse=True)
            results[idx] = similar_texts[:max_results]
        except Exception as e:
            logger.debug(f"Error finding similar texts: {e}")
            continue
    
    return results


def create_superminhash_signatures(
    df: Any,
    columns: List[str],
    weights: Optional[Dict[str, float]] = None,
    num_perm: int = 128,
    tokenizer: Optional[Callable] = None
) -> Dict[int, np.ndarray]:
    """
    Create SuperMinHash signatures for texts in a dataframe.
    
    Parameters
    ----------
    df : Any
        Input dataframe
    columns : List[str]
        Columns to use for creating signatures
    weights : Optional[Dict[str, float]], default=None
        Weights for each column
    num_perm : int, default=128
        Number of permutations for SuperMinHash
    tokenizer : Optional[Callable], default=None
        Function to convert text to tokens
        
    Returns
    -------
    Dict[int, np.ndarray]
        Dictionary mapping row indices to SuperMinHash signatures
    """
    # Initialize SuperMinHash
    hasher = SuperMinHash(num_perm=num_perm)
    
    # Default tokenizer if none provided
    if tokenizer is None:
        tokenizer = lambda x: re.findall(r'\w+', x.lower())
    
    # Set default weights if not provided
    if weights is None:
        weights = {col: 1.0 / len(columns) for col in columns}
    
    # Normalize weights to sum to 1
    total_weight = sum(weights.values())
    norm_weights = {col: weights.get(col, 0) / total_weight for col in columns}
    
    # Generate signatures for each row
    signatures = {}
    
    for idx, row in df.iterrows():
        # Tokenize text from all columns with weights
        all_tokens = []
        
        for col in columns:
            if col not in row or pd.isna(row[col]):
                continue
                
            try:
                # Convert to string if necessary
                val = str(row[col]) if not isinstance(row[col], str) else row[col]
                
                # Tokenize
                tokens = tokenizer(val)
                
                # Apply weight by duplicating tokens
                weight = norm_weights.get(col, 0)
                if weight > 0:
                    # Repeat tokens based on weight (minimum 1 time)
                    repetitions = max(1, int(10 * weight))
                    weighted_tokens = tokens * repetitions
                    all_tokens.extend(weighted_tokens)
            except Exception as e:
                logger.debug(f"Error tokenizing {col}: {e}")
                continue
        
        # Compute signature for all tokens
        signature = hasher.compute_signature(all_tokens)
        signatures[idx] = signature
    
    return signatures


def find_similar_pairs_superminhash(
    signatures: Dict[int, np.ndarray],
    threshold: float = 0.8
) -> Set[Tuple[int, int]]:
    """
    Find similar pairs using SuperMinHash signatures.
    
    Parameters
    ----------
    signatures : Dict[int, np.ndarray]
        Dictionary mapping indices to SuperMinHash signatures
    threshold : float, default=0.8
        Similarity threshold
        
    Returns
    -------
    Set[Tuple[int, int]]
        Set of similar pairs (idx1, idx2)
    """
    # Find similar pairs by comparing signatures
    similar_pairs = set()
    indices = list(signatures.keys())
    
    # For each pair of indices
    for i in range(len(indices)):
        idx1 = indices[i]
        sig1 = signatures[idx1]
        
        for j in range(i + 1, len(indices)):
            idx2 = indices[j]
            sig2 = signatures[idx2]
            
            # Calculate Jaccard similarity
            similarity = SuperMinHash.jaccard_similarity(sig1, sig2)
            
            # If similarity is above threshold, add to similar pairs
            if similarity >= threshold:
                # Ensure consistent ordering of pairs
                similar_pairs.add((min(idx1, idx2), max(idx1, idx2)))
    
    return similar_pairs


def flag_similar_records_advanced_lsh(
    df: Any,
    columns: List[str],
    weights: Optional[Dict[str, float]] = None,
    threshold: float = 0.8,
    method: str = 'simhash',
    flag_column: str = 'is_similar',
    inplace: bool = False,
    group_column: Optional[str] = None,
    similarity_column: Optional[str] = None
) -> Any:
    """
    Flag similar records using advanced LSH algorithms.
    
    Parameters
    ----------
    df : Any
        The dataframe to process
    columns : List[str]
        Columns to consider when calculating similarity
    weights : Optional[Dict[str, float]], default=None
        Dictionary mapping column names to their weights
    threshold : float, default=0.8
        Similarity threshold
    method : str, default='simhash'
        LSH method to use: 'simhash', 'bktree', 'superminhash'
    flag_column : str, default='is_similar'
        Name of the column to add for flagging similar records
    inplace : bool, default=False
        If True, modify the dataframe in-place
    group_column : Optional[str], default=None
        If provided, add a column with this name containing group IDs
    similarity_column : Optional[str], default=None
        If provided, add a column with similarity scores
        
    Returns
    -------
    Any
        DataFrame with similar records flagged
    """
    # Start with pandas DataFrame for consistent processing
    df_type = None
    try:
        import pandas as pd
        
        # Check if df is already a pandas DataFrame
        if isinstance(df, pd.DataFrame):
            pandas_df = df.copy() if not inplace else df
        else:
            # Try to convert from other types (polars, dask, etc.)
            try:
                # For Polars DataFrame
                import polars as pl
                if hasattr(df, 'to_pandas'):
                    pandas_df = df.to_pandas()
                    df_type = 'polars'
                else:
                    pandas_df = pd.DataFrame(df)
            except ImportError:
                # Fall back to direct conversion
                pandas_df = pd.DataFrame(df)
    except ImportError:
        raise ImportError("Pandas is required for advanced LSH functionality")
    
    n_rows = len(pandas_df)
    
    # Initialize result columns
    duplicate_flags = np.zeros(n_rows, dtype=bool)
    group_ids = np.zeros(n_rows, dtype=int)
    similarity_scores = np.zeros(n_rows, dtype=float)
    
    # Create graph for tracking similar record pairs
    G = nx.Graph()
    for i in range(n_rows):
        G.add_node(i)
    
    # Use different LSH methods based on parameter
    if method == 'simhash':
        # Create SimHash signatures
        signatures = create_simhash_signatures(
            df=pandas_df,
            columns=columns,
            weights=weights
        )
        
        # Find similar pairs
        similar_pairs = find_similar_pairs_simhash(
            signatures=signatures,
            threshold=threshold
        )
        
        # Add edges to graph
        G.add_edges_from(similar_pairs)
        
    elif method == 'bktree':
        if len(columns) > 1:
            print("BKTree method works best with a single text column. Using the first column.")
        
        # Use the first column for BKTree
        primary_column = columns[0]
        
        # Find similar texts
        similar_texts = find_similar_text_bktree(
            df=pandas_df,
            query_column=primary_column,
            index_column=primary_column,
            threshold=threshold
        )
        
        # Add edges to graph
        for idx, matches in similar_texts.items():
            for match_idx, similarity in matches:
                G.add_edge(idx, match_idx)
                
                # Store similarity scores
                if similarity_column:
                    similarity_scores[idx] = max(similarity_scores[idx], similarity)
                    similarity_scores[match_idx] = max(similarity_scores[match_idx], similarity)
        
    elif method == 'superminhash':
        # Create SuperMinHash signatures
        signatures = create_superminhash_signatures(
            df=pandas_df,
            columns=columns,
            weights=weights
        )
        
        # Find similar pairs
        similar_pairs = find_similar_pairs_superminhash(
            signatures=signatures,
            threshold=threshold
        )
        
        # Add edges to graph
        G.add_edges_from(similar_pairs)
        
    else:
        raise ValueError(f"Unknown LSH method: {method}. Supported methods are 'simhash', 'bktree', and 'superminhash'.")
    
    # Find connected components (clusters of similar records)
    clusters = list(nx.connected_components(G))
    
    # Mark similar records and assign group IDs
    for group_id, cluster in enumerate(clusters, 1):
        if len(cluster) > 1:  # Only process actual similar groups
            for idx in cluster:
                duplicate_flags[idx] = True
                if group_column:
                    group_ids[idx] = group_id
    
    # For first occurrence in each group, set duplicate flag to False
    for cluster in clusters:
        if len(cluster) > 1:
            min_idx = min(cluster)
            duplicate_flags[min_idx] = False
    
    # Add columns to dataframe
    result_df = pandas_df.copy() if not inplace else pandas_df
    result_df[flag_column] = duplicate_flags
    
    if group_column:
        result_df[group_column] = group_ids
        
    if similarity_column:
        result_df[similarity_column] = similarity_scores
    
    # Convert back to original type if needed
    if df_type == 'polars' and not inplace:
        import polars as pl
        return pl.from_pandas(result_df)
    else:
        return result_df


def compare_lsh_methods(
    df: Any,
    columns: List[str],
    weights: Optional[Dict[str, float]] = None,
    threshold: float = 0.8,
    sample_size: Optional[int] = None
) -> Dict[str, Any]:
    """
    Compare different LSH methods on the same dataset.
    
    Parameters
    ----------
    df : Any
        Input dataframe
    columns : List[str]
        Columns to use for comparison
    weights : Optional[Dict[str, float]], default=None
        Weights for each column
    threshold : float, default=0.8
        Similarity threshold
    sample_size : Optional[int], default=None
        Number of rows to sample for comparison (for large datasets)
        
    Returns
    -------
    Dict[str, Any]
        Dictionary with comparison results
    """
    import time
    import pandas as pd
    
    # Sample if requested
    if sample_size is not None and len(df) > sample_size:
        df_sample = df.sample(sample_size, random_state=42)
    else:
        df_sample = df
    
    # Convert to pandas if needed
    if not isinstance(df_sample, pd.DataFrame):
        try:
            pandas_df = pd.DataFrame(df_sample)
        except:
            # Try to convert from polars
            try:
                import polars as pl
                if hasattr(df_sample, 'to_pandas'):
                    pandas_df = df_sample.to_pandas()
                else:
                    raise ValueError("Could not convert dataframe to pandas")
            except ImportError:
                raise ValueError("Could not convert dataframe to pandas")
    else:
        pandas_df = df_sample
    
    # Methods to compare
    methods = ['simhash', 'bktree', 'superminhash', 'standard']
    results = {}
    
    # Standard method (baseline)
    from freamon.deduplication.flag_duplicates import flag_similar_records
    
    for method in methods:
        print(f"Testing method: {method}")
        start_time = time.time()
        
        if method == 'standard':
            # Use the standard flag_similar_records function as baseline
            result_df = flag_similar_records(
                df=pandas_df,
                columns=columns,
                weights=weights,
                threshold=threshold,
                flag_column='is_similar',
                group_column='group_id',
                similarity_column='similarity'
            )
        else:
            # Use the advanced LSH methods
            result_df = flag_similar_records_advanced_lsh(
                df=pandas_df,
                columns=columns,
                weights=weights,
                threshold=threshold,
                method=method,
                flag_column='is_similar',
                group_column='group_id',
                similarity_column='similarity'
            )
        
        # Record time
        elapsed_time = time.time() - start_time
        
        # Record statistics
        duplicate_count = result_df['is_similar'].sum()
        group_count = result_df['group_id'].max() if 'group_id' in result_df.columns else 0
        
        results[method] = {
            'time': elapsed_time,
            'duplicate_count': duplicate_count,
            'group_count': group_count,
            'sample_results': result_df.head(5).to_dict() if isinstance(result_df, pd.DataFrame) else None
        }
    
    return results