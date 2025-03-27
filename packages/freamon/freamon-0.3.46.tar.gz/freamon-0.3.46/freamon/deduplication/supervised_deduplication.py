"""Supervised learning approach for duplicate detection in datasets."""

from typing import Dict, List, Tuple, Union, Optional, Any, Set, Callable
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import precision_recall_fscore_support, roc_auc_score
import lightgbm as lgb
from collections import defaultdict

from freamon.utils.text_utils import TextProcessor
from freamon.modeling.model import Model
from freamon.features.engineer import FeatureEngineer


class SupervisedDeduplicationModel:
    """
    A supervised learning model for detecting duplicate records in datasets.
    
    This model can be trained on labeled data (known duplicates) and then
    used to detect duplicates in new datasets by predicting the probability
    of two records being duplicates of each other.
    
    Parameters
    ----------
    model_type : str, default='lightgbm'
        The type of model to use: 'lightgbm', 'random_forest', or 'gradient_boosting'.
    text_processor : Optional[TextProcessor], default=None
        Instance of TextProcessor for text feature processing.
    date_features : Optional[List[str]], default=None
        List of column names containing date/time features.
    key_features : Optional[List[str]], default=None
        List of column names for features that are important for duplicate detection.
    model_params : Optional[Dict[str, Any]], default=None
        Parameters for the underlying model.
    """
    
    def __init__(
        self,
        model_type: str = 'lightgbm',
        text_processor: Optional[TextProcessor] = None,
        date_features: Optional[List[str]] = None,
        key_features: Optional[List[str]] = None,
        model_params: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the supervised deduplication model."""
        self.model_type = model_type
        self.text_processor = text_processor if text_processor else TextProcessor()
        self.date_features = date_features or []
        self.key_features = key_features or []
        self.model_params = model_params or {}
        self.model = None
        self.feature_importances_ = None
        self.feature_names_ = None
        self.trained = False
        
        # Initialize feature engineer
        self.feature_engineer = FeatureEngineer()
        
        # For active learning
        self.uncertainty_threshold = 0.3
        self.active_learning_samples = []
        self.labeled_samples = []
        
        # For incremental learning
        self.incremental_mode = False
        self.previous_data_fingerprint = None
        self.previous_data_size = 0
        self.previous_features = None
        
        # For ensemble methods
        self.ensemble_models = []
        self.ensemble_weights = []
        
        # For auto-tuning
        self.auto_tuning_performed = False
        self.auto_tuning_results = {}
        self.optimal_threshold = 0.5
        
        # For explainability
        self.feature_contributions = defaultdict(list)
    
    def _create_model(self) -> Any:
        """Create the underlying model based on model_type."""
        if self.model_type == 'lightgbm':
            params = {
                'objective': 'binary',
                'metric': 'auc',
                'boosting_type': 'gbdt',
                'num_leaves': 31,
                'learning_rate': 0.05,
                'feature_fraction': 0.9,
                'bagging_fraction': 0.8,
                'bagging_freq': 5,
                'verbose': -1,
                **self.model_params
            }
            return lgb.LGBMClassifier(**params)
        
        elif self.model_type == 'random_forest':
            params = {
                'n_estimators': 100,
                'max_depth': 10,
                'min_samples_split': 2,
                'min_samples_leaf': 1,
                'random_state': 42,
                **self.model_params
            }
            return RandomForestClassifier(**params)
        
        elif self.model_type == 'gradient_boosting':
            params = {
                'n_estimators': 100,
                'learning_rate': 0.1,
                'max_depth': 3,
                'random_state': 42,
                **self.model_params
            }
            return GradientBoostingClassifier(**params)
        
        else:
            raise ValueError(f"Unknown model type: {self.model_type}. Use 'lightgbm', 'random_forest', or 'gradient_boosting'.")
    
    def _generate_pair_features(self, df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        """
        Generate features for pairs of records that describe their similarity.
        
        Parameters
        ----------
        df1 : pd.DataFrame
            First dataframe containing records.
        df2 : pd.DataFrame
            Second dataframe containing records to compare with.
            
        Returns
        -------
        pd.DataFrame
            Dataframe with features describing similarity between record pairs.
        """
        feature_df = pd.DataFrame()
        
        # Process each key feature
        for feature in self.key_features:
            if feature not in df1.columns or feature not in df2.columns:
                continue
                
            # Handle different data types differently
            if pd.api.types.is_numeric_dtype(df1[feature]):
                # For numeric features, calculate absolute difference and ratio
                feature_df[f'{feature}_abs_diff'] = abs(df1[feature].values - df2[feature].values)
                
                # Calculate ratio where possible (avoid division by zero)
                with np.errstate(divide='ignore', invalid='ignore'):
                    ratio = df1[feature].values / df2[feature].values
                    ratio = np.where(np.isfinite(ratio), ratio, 0)
                    feature_df[f'{feature}_ratio'] = ratio
                    
            elif pd.api.types.is_string_dtype(df1[feature]):
                # For string features, calculate text similarity
                text_similarities = []
                for text1, text2 in zip(df1[feature].fillna(''), df2[feature].fillna('')):
                    if not isinstance(text1, str):
                        text1 = str(text1)
                    if not isinstance(text2, str):
                        text2 = str(text2)
                        
                    # Calculate cosine similarity
                    similarity = self.text_processor.calculate_document_similarity(
                        text1, text2, method='cosine')
                    text_similarities.append(similarity)
                    
                feature_df[f'{feature}_text_sim'] = text_similarities
                
                # Also add Levenshtein similarity for shorter strings
                if df1[feature].str.len().mean() < 100 and df2[feature].str.len().mean() < 100:
                    levenshtein_similarities = []
                    for text1, text2 in zip(df1[feature].fillna(''), df2[feature].fillna('')):
                        if not isinstance(text1, str):
                            text1 = str(text1)
                        if not isinstance(text2, str):
                            text2 = str(text2)
                            
                        # Import is inside loop to avoid circular imports
                        from freamon.deduplication.fuzzy_deduplication import calculate_levenshtein_similarity
                        similarity = calculate_levenshtein_similarity(text1, text2)
                        levenshtein_similarities.append(similarity)
                        
                    feature_df[f'{feature}_lev_sim'] = levenshtein_similarities
            
            elif pd.api.types.is_categorical_dtype(df1[feature]):
                # For categorical features, exact match (1) or not (0)
                feature_df[f'{feature}_exact_match'] = (df1[feature] == df2[feature]).astype(int)
            
            else:
                # Default case - exact match
                feature_df[f'{feature}_exact_match'] = (df1[feature] == df2[feature]).astype(int)
        
        # Process date features with special handling
        for date_feat in self.date_features:
            if date_feat not in df1.columns or date_feat not in df2.columns:
                continue
                
            # Convert to datetime if not already
            df1_dates = pd.to_datetime(df1[date_feat], errors='coerce')
            df2_dates = pd.to_datetime(df2[date_feat], errors='coerce')
            
            # Calculate time differences in days
            time_diffs = abs((df1_dates - df2_dates).dt.total_seconds() / (60 * 60 * 24))
            feature_df[f'{date_feat}_days_diff'] = time_diffs.fillna(999)  # Fill NaN with large value
            
            # Add exact date match feature
            feature_df[f'{date_feat}_exact_match'] = (df1_dates == df2_dates).astype(int)
        
        return feature_df
    
    def _create_training_pairs(
        self, 
        df: pd.DataFrame, 
        duplicate_pairs: List[Tuple[int, int]]
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
        """
        Create training data with positive and negative examples of duplicate pairs.
        
        Parameters
        ----------
        df : pd.DataFrame
            The dataset containing records.
        duplicate_pairs : List[Tuple[int, int]]
            List of tuples containing index pairs of known duplicates.
            
        Returns
        -------
        Tuple[pd.DataFrame, pd.DataFrame, pd.Series]
            Tuple of (df1, df2, labels) where df1 and df2 contain record pairs
            and labels indicates whether they are duplicates.
        """
        # Convert duplicate pairs to set for faster lookup
        duplicate_set = set((min(a, b), max(a, b)) for a, b in duplicate_pairs)
        
        # Create positive examples (known duplicates)
        df1_pos = pd.DataFrame([df.iloc[i].copy() for i, j in duplicate_set])
        df2_pos = pd.DataFrame([df.iloc[j].copy() for i, j in duplicate_set])
        y_pos = pd.Series([1] * len(duplicate_set))
        
        # Create negative examples (non-duplicates)
        # For negative examples, randomly select pairs that are not in duplicate_set
        n_pos = len(duplicate_set)
        n_neg = min(n_pos * 3, 10000)  # Cap the number of negative examples
        
        negative_pairs = set()
        max_attempts = n_neg * 10  # Avoid infinite loop
        attempts = 0
        
        while len(negative_pairs) < n_neg and attempts < max_attempts:
            i, j = np.random.choice(len(df), 2, replace=False)
            pair = (min(i, j), max(i, j))
            if pair not in duplicate_set:
                negative_pairs.add(pair)
            attempts += 1
        
        if not negative_pairs:
            raise ValueError("Could not generate any negative examples")
        
        df1_neg = pd.DataFrame([df.iloc[i].copy() for i, j in negative_pairs])
        df2_neg = pd.DataFrame([df.iloc[j].copy() for i, j in negative_pairs])
        y_neg = pd.Series([0] * len(negative_pairs))
        
        # Combine positive and negative examples
        df1 = pd.concat([df1_pos, df1_neg], ignore_index=True)
        df2 = pd.concat([df2_pos, df2_neg], ignore_index=True)
        y = pd.concat([y_pos, y_neg], ignore_index=True)
        
        return df1, df2, y
    
    def fit(
        self,
        df: pd.DataFrame,
        duplicate_pairs: List[Tuple[int, int]],
        validation_pairs: Optional[List[Tuple[int, int]]] = None,
        validation_fraction: float = 0.2,
        **kwargs
    ) -> 'SupervisedDeduplicationModel':
        """
        Train the deduplication model on labeled duplicate data.
        
        Parameters
        ----------
        df : pd.DataFrame
            The dataset containing records.
        duplicate_pairs : List[Tuple[int, int]]
            List of tuples containing index pairs of known duplicates.
        validation_pairs : Optional[List[Tuple[int, int]]], default=None
            Optional list of validation duplicate pairs. If None, a portion of
            duplicate_pairs will be used for validation based on validation_fraction.
        validation_fraction : float, default=0.2
            Fraction of data to use for validation if validation_pairs is None.
        **kwargs
            Additional parameters passed to the underlying model's fit method.
            
        Returns
        -------
        SupervisedDeduplicationModel
            The fitted model.
        """
        # Create model if not already initialized
        if self.model is None:
            self.model = self._create_model()
        
        # Split into train and validation if validation_pairs is None
        if validation_pairs is None and validation_fraction > 0:
            n_val = int(len(duplicate_pairs) * validation_fraction)
            if n_val > 0:
                np.random.shuffle(duplicate_pairs)
                train_pairs = duplicate_pairs[n_val:]
                validation_pairs = duplicate_pairs[:n_val]
            else:
                train_pairs = duplicate_pairs
                validation_pairs = []
        else:
            train_pairs = duplicate_pairs
        
        # Create training pairs
        df1_train, df2_train, y_train = self._create_training_pairs(df, train_pairs)
        
        # Generate features for training pairs
        X_train = self._generate_pair_features(df1_train, df2_train)
        
        # Save feature names
        self.feature_names_ = X_train.columns.tolist()
        
        # Create validation data if available
        eval_set = None
        if validation_pairs and len(validation_pairs) > 0:
            df1_val, df2_val, y_val = self._create_training_pairs(df, validation_pairs)
            X_val = self._generate_pair_features(df1_val, df2_val)
            eval_set = [(X_val, y_val)]
        
        # Fit the model
        if eval_set:
            self.model.fit(X_train, y_train, eval_set=eval_set, **kwargs)
        else:
            self.model.fit(X_train, y_train, **kwargs)
        
        # Store feature importances if available
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importances_ = dict(zip(self.feature_names_, self.model.feature_importances_))
        
        self.trained = True
        
        # Store previous data fingerprint for incremental learning
        if self.incremental_mode:
            self.previous_data_size = len(df)
            self.previous_features = self.feature_names_
        
        return self
    
    def fit_ensemble(
        self,
        df: pd.DataFrame,
        duplicate_pairs: List[Tuple[int, int]],
        model_types: List[str] = ['lightgbm', 'random_forest', 'gradient_boosting'],
        model_weights: Optional[List[float]] = None,
        **kwargs
    ) -> 'SupervisedDeduplicationModel':
        """
        Train multiple models and combine them as an ensemble.
        
        Parameters
        ----------
        df : pd.DataFrame
            The dataset containing records.
        duplicate_pairs : List[Tuple[int, int]]
            List of tuples containing index pairs of known duplicates.
        model_types : List[str], default=['lightgbm', 'random_forest', 'gradient_boosting']
            Types of models to include in the ensemble.
        model_weights : Optional[List[float]], default=None
            Weights for each model in the ensemble. If None, equal weights are assigned.
        **kwargs
            Additional parameters passed to each model's fit method.
            
        Returns
        -------
        SupervisedDeduplicationModel
            The fitted ensemble model.
        """
        self.ensemble_models = []
        
        # Train each model in the ensemble
        for model_type in model_types:
            # Create a model of this type
            sub_model = SupervisedDeduplicationModel(
                model_type=model_type,
                text_processor=self.text_processor,
                date_features=self.date_features,
                key_features=self.key_features,
                model_params=self.model_params
            )
            
            # Train the model
            sub_model.fit(df, duplicate_pairs, **kwargs)
            
            # Add to ensemble
            self.ensemble_models.append(sub_model)
        
        # Set weights
        if model_weights is None:
            # Equal weights by default
            self.ensemble_weights = [1.0 / len(model_types)] * len(model_types)
        else:
            # Normalize weights to sum to 1
            total = sum(model_weights)
            self.ensemble_weights = [w / total for w in model_weights]
        
        self.trained = True
        return self
    
    def predict_duplicate_probability(
        self,
        df1: Optional[pd.DataFrame] = None,
        df2: Optional[pd.DataFrame] = None,
        df: Optional[pd.DataFrame] = None,
        max_pairs: int = 1000000,
        return_features: bool = False,
    ) -> Union[pd.DataFrame, Tuple[pd.DataFrame, pd.DataFrame]]:
        """
        Predict the probability of record pairs being duplicates.
        
        Parameters
        ----------
        df1 : Optional[pd.DataFrame], default=None
            First dataframe containing records. If None, df must be provided.
        df2 : Optional[pd.DataFrame], default=None
            Second dataframe containing records. If None, df must be provided.
        df : Optional[pd.DataFrame], default=None
            Single dataframe to compare with itself. Used when df1 and df2 are None.
        max_pairs : int, default=1000000
            Maximum number of pairs to evaluate (to prevent memory issues).
        return_features : bool, default=False
            Whether to return the feature dataframe along with predictions.
            
        Returns
        -------
        Union[pd.DataFrame, Tuple[pd.DataFrame, pd.DataFrame]]
            Dataframe with record indices and duplicate probabilities.
            If return_features=True, also returns the feature dataframe.
        """
        if not self.trained:
            raise RuntimeError("Model must be trained before making predictions")
        
        # Handle different input scenarios
        if df is not None:
            # Single dataframe - compare rows pairwise
            n = len(df)
            pairs = []
            
            # Limit number of pairs to avoid memory issues
            for i in range(n):
                for j in range(i+1, n):
                    pairs.append((i, j))
                    if len(pairs) >= max_pairs:
                        break
                if len(pairs) >= max_pairs:
                    break
            
            # Create temporary dataframes for pairs
            df1 = pd.DataFrame([df.iloc[i].copy() for i, j in pairs])
            df2 = pd.DataFrame([df.iloc[j].copy() for i, j in pairs])
            
            # Store original indices
            idx1 = [i for i, j in pairs]
            idx2 = [j for i, j in pairs]
            
        elif df1 is not None and df2 is not None:
            # Two dataframes - compare rows between them
            n1, n2 = len(df1), len(df2)
            pairs = []
            
            # Limit number of pairs to avoid memory issues
            for i in range(n1):
                for j in range(n2):
                    pairs.append((i, j))
                    if len(pairs) >= max_pairs:
                        break
                if len(pairs) >= max_pairs:
                    break
            
            # Create temporary dataframes for pairs
            df1_temp = pd.DataFrame([df1.iloc[i].copy() for i, j in pairs])
            df2_temp = pd.DataFrame([df2.iloc[j].copy() for i, j in pairs])
            
            # Store original indices
            idx1 = [i for i, j in pairs]
            idx2 = [j for i, j in pairs]
            
            # Reassign
            df1, df2 = df1_temp, df2_temp
            
        else:
            raise ValueError("Either df or both df1 and df2 must be provided")
        
        # Generate features for pairs
        X = self._generate_pair_features(df1, df2)
        
        # Ensure all expected features are present
        for feature in self.feature_names_:
            if feature not in X:
                X[feature] = 0  # Default value for missing features
        
        # Keep only the features used during training
        X = X[self.feature_names_]
        
        # Predict probabilities using the appropriate method
        if self.ensemble_models:
            # Use ensemble prediction
            probabilities = self._predict_ensemble_proba(X)
        else:
            # Use single model prediction
            probabilities = self.model.predict_proba(X)[:, 1]
        
        # Create result dataframe
        result = pd.DataFrame({
            'idx1': idx1,
            'idx2': idx2,
            'duplicate_probability': probabilities
        })
        
        # Sort by probability (highest first)
        result = result.sort_values('duplicate_probability', ascending=False).reset_index(drop=True)
        
        # Store feature contributions for explainability if using a compatible model
        if hasattr(self.model, 'feature_importances_'):
            self._calculate_feature_contributions(X, probabilities)
        
        # Identify uncertain samples for active learning
        self._identify_uncertain_samples(result, df1, df2, idx1, idx2)
        
        if return_features:
            return result, X
        return result
    
    def _predict_ensemble_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict probabilities using the ensemble of models.
        
        Parameters
        ----------
        X : pd.DataFrame
            Feature matrix.
            
        Returns
        -------
        np.ndarray
            Weighted average of probabilities from all models.
        """
        # Get predictions from each model
        all_probas = []
        for model, weight in zip(self.ensemble_models, self.ensemble_weights):
            probas = model.model.predict_proba(X)[:, 1]
            all_probas.append(probas * weight)
        
        # Combine predictions with weights
        return np.sum(all_probas, axis=0)
    
    def _calculate_feature_contributions(self, X: pd.DataFrame, probabilities: np.ndarray) -> None:
        """
        Calculate feature contributions for explainability.
        
        Parameters
        ----------
        X : pd.DataFrame
            Feature matrix.
        probabilities : np.ndarray
            Predicted probabilities.
        """
        # Reset contributions
        self.feature_contributions = defaultdict(list)
        
        # Calculate simple correlation-based feature contributions
        for feature in X.columns:
            correlation = np.corrcoef(X[feature], probabilities)[0, 1]
            self.feature_contributions[feature] = correlation
    
    def _identify_uncertain_samples(
        self, 
        result: pd.DataFrame, 
        df1: pd.DataFrame, 
        df2: pd.DataFrame, 
        idx1: List[int], 
        idx2: List[int]
    ) -> None:
        """
        Identify samples with uncertain predictions for active learning.
        
        Parameters
        ----------
        result : pd.DataFrame
            Dataframe with predictions.
        df1, df2 : pd.DataFrame
            Record pairs.
        idx1, idx2 : List[int]
            Original indices of records.
        """
        # Find predictions close to decision boundary
        uncertain_mask = np.abs(result['duplicate_probability'] - 0.5) < self.uncertainty_threshold
        uncertain_indices = result[uncertain_mask].index.tolist()
        
        # Limit to a manageable number of samples
        np.random.shuffle(uncertain_indices)
        uncertain_indices = uncertain_indices[:min(len(uncertain_indices), 100)]
        
        # Store uncertain samples
        self.active_learning_samples = []
        for idx in uncertain_indices:
            i, j = result.iloc[idx]['idx1'], result.iloc[idx]['idx2']
            prob = result.iloc[idx]['duplicate_probability']
            record1 = df1.iloc[idx].to_dict()
            record2 = df2.iloc[idx].to_dict()
            self.active_learning_samples.append({
                'idx1': int(i),
                'idx2': int(j),
                'probability': prob,
                'record1': record1,
                'record2': record2
            })
    
    def find_duplicates(
        self,
        df: pd.DataFrame,
        threshold: float = 0.5,
        max_comparisons: int = 1000000,
        return_probabilities: bool = False
    ) -> Union[List[Tuple[int, int]], pd.DataFrame]:
        """
        Find duplicate records in a dataframe.
        
        Parameters
        ----------
        df : pd.DataFrame
            The dataset to check for duplicates.
        threshold : float, default=0.5
            Probability threshold above which pairs are considered duplicates.
        max_comparisons : int, default=1000000
            Maximum number of pair comparisons to evaluate.
        return_probabilities : bool, default=False
            Whether to return a dataframe with probabilities instead of just pairs.
            
        Returns
        -------
        Union[List[Tuple[int, int]], pd.DataFrame]
            If return_probabilities=False: List of tuples containing index pairs of detected duplicates.
            If return_probabilities=True: Dataframe with record indices and duplicate probabilities.
        """
        # Use auto-tuned threshold if available
        if self.auto_tuning_performed:
            threshold = self.optimal_threshold
        
        # Predict duplicate probabilities
        result = self.predict_duplicate_probability(df=df, max_pairs=max_comparisons)
        
        # Filter pairs by threshold
        duplicates = result[result['duplicate_probability'] >= threshold]
        
        if return_probabilities:
            return duplicates
        else:
            return [(int(row['idx1']), int(row['idx2'])) for _, row in duplicates.iterrows()]
    
    def evaluate(
        self,
        df: pd.DataFrame,
        true_duplicate_pairs: List[Tuple[int, int]],
        threshold: float = 0.5,
        max_comparisons: int = 100000
    ) -> Dict[str, float]:
        """
        Evaluate the model's performance on a test dataset with known duplicates.
        
        Parameters
        ----------
        df : pd.DataFrame
            The dataset containing records.
        true_duplicate_pairs : List[Tuple[int, int]]
            List of tuples containing index pairs of actual duplicates (ground truth).
        threshold : float, default=0.5
            Probability threshold above which pairs are considered duplicates.
        max_comparisons : int, default=100000
            Maximum number of pair comparisons to evaluate.
            
        Returns
        -------
        Dict[str, float]
            Dictionary with evaluation metrics (precision, recall, f1, auc).
        """
        # Convert true pairs to standard form (smaller index first)
        true_pairs_set = set((min(i, j), max(i, j)) for i, j in true_duplicate_pairs)
        
        # Get all pairs and predictions
        result = self.predict_duplicate_probability(df=df, max_pairs=max_comparisons)
        
        # Convert to standard form for comparison
        all_pairs = [(min(int(row['idx1']), int(row['idx2'])), max(int(row['idx1']), int(row['idx2']))) 
                     for _, row in result.iterrows()]
        all_probs = result['duplicate_probability'].values
        
        # Create true labels for the pairs we've evaluated
        y_true = np.array([1 if pair in true_pairs_set else 0 for pair in all_pairs])
        
        # Calculate AUC if there are both positive and negative examples
        auc = 0.0
        if len(set(y_true)) > 1:
            auc = roc_auc_score(y_true, all_probs)
        
        # Apply threshold to get predicted duplicates
        y_pred = (all_probs >= threshold).astype(int)
        
        # Calculate precision, recall, and F1 score
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_true, y_pred, average='binary', zero_division=0)
        
        # Return evaluation metrics
        return {
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'auc': auc
        }
    
    def get_feature_importances(self) -> Dict[str, float]:
        """
        Get the feature importances from the trained model.
        
        Returns
        -------
        Dict[str, float]
            Dictionary mapping feature names to importance scores.
        """
        if not self.trained:
            raise RuntimeError("Model must be trained before getting feature importances")
        
        if self.feature_importances_ is None:
            raise ValueError("Feature importances not available for this model")
        
        return dict(sorted(self.feature_importances_.items(), key=lambda x: x[1], reverse=True))
    
    def request_active_learning_samples(self, n_samples: int = 10) -> List[Dict[str, Any]]:
        """
        Get samples that would be most valuable for labeling.
        
        Parameters
        ----------
        n_samples : int, default=10
            Number of samples to request.
            
        Returns
        -------
        List[Dict[str, Any]]
            List of sample pairs most valuable for labeling.
        """
        if not self.active_learning_samples:
            return []
        
        # Return top n uncertain samples
        return self.active_learning_samples[:min(n_samples, len(self.active_learning_samples))]
    
    def add_labeled_samples(self, samples: List[Dict[str, Any]]) -> 'SupervisedDeduplicationModel':
        """
        Add manually labeled samples to improve the model.
        
        Parameters
        ----------
        samples : List[Dict[str, Any]]
            List of dictionaries with labeled samples. Each dictionary should contain:
            - 'idx1', 'idx2': Indices of the record pair
            - 'is_duplicate': Boolean indicating if the pair is a duplicate
            
        Returns
        -------
        SupervisedDeduplicationModel
            The updated model.
        """
        # Store labeled samples
        self.labeled_samples.extend(samples)
        
        # Return self for method chaining
        return self
    
    def update_model_with_active_learning(self, df: pd.DataFrame) -> 'SupervisedDeduplicationModel':
        """
        Update the model with actively labeled samples.
        
        Parameters
        ----------
        df : pd.DataFrame
            The dataset containing records.
            
        Returns
        -------
        SupervisedDeduplicationModel
            The updated model.
        """
        if not self.labeled_samples:
            return self
        
        # Extract labeled duplicate pairs
        new_duplicate_pairs = [
            (sample['idx1'], sample['idx2']) 
            for sample in self.labeled_samples 
            if sample.get('is_duplicate', False)
        ]
        
        if not new_duplicate_pairs:
            return self
        
        # Update model with new labeled data
        self.fit(df, new_duplicate_pairs, validation_fraction=0.0)
        
        # Clear labeled samples since they're now incorporated
        self.labeled_samples = []
        
        return self
    
    def auto_tune_threshold(
        self, 
        df: pd.DataFrame, 
        true_duplicate_pairs: List[Tuple[int, int]],
        threshold_range: Optional[List[float]] = None,
        optimize_for: str = 'f1'
    ) -> Dict[str, Any]:
        """
        Automatically find the optimal threshold value.
        
        Parameters
        ----------
        df : pd.DataFrame
            The dataset containing records.
        true_duplicate_pairs : List[Tuple[int, int]]
            List of known duplicate pairs for evaluation.
        threshold_range : Optional[List[float]], default=None
            Range of thresholds to evaluate. If None, uses np.arange(0.1, 1.0, 0.1).
        optimize_for : str, default='f1'
            Metric to optimize: 'precision', 'recall', 'f1', or 'balanced'.
            
        Returns
        -------
        Dict[str, Any]
            Results of threshold optimization.
        """
        if threshold_range is None:
            threshold_range = np.arange(0.1, 1.0, 0.1)
        
        results = []
        for threshold in threshold_range:
            metrics = self.evaluate(
                df=df,
                true_duplicate_pairs=true_duplicate_pairs,
                threshold=threshold
            )
            
            # Calculate balanced score if requested
            if optimize_for == 'balanced':
                balanced_score = (metrics['precision'] + metrics['recall']) / 2
                metrics['balanced_score'] = balanced_score
                
            results.append({
                'threshold': threshold,
                **metrics
            })
        
        # Find optimal threshold based on chosen metric
        if optimize_for == 'balanced':
            best_result = max(results, key=lambda x: x['balanced_score'])
        else:
            best_result = max(results, key=lambda x: x[optimize_for])
            
        # Store results
        self.auto_tuning_results = {
            'all_results': results,
            'best_threshold': best_result['threshold'],
            'best_metrics': {k: v for k, v in best_result.items() if k != 'threshold'}
        }
        
        # Set optimal threshold
        self.optimal_threshold = best_result['threshold']
        self.auto_tuning_performed = True
        
        return self.auto_tuning_results
    
    def get_feature_contributions(self, top_n: int = 10) -> Dict[str, float]:
        """
        Get the contribution of each feature to duplicate detection.
        
        Parameters
        ----------
        top_n : int, default=10
            Number of top features to return.
            
        Returns
        -------
        Dict[str, float]
            Dictionary of feature contributions.
        """
        if not self.feature_contributions:
            return {}
        
        # Sort by absolute contribution and return top n
        sorted_contribs = sorted(
            self.feature_contributions.items(), 
            key=lambda x: abs(x[1]), 
            reverse=True
        )
        
        return dict(sorted_contribs[:top_n])
    
    def get_explanation_for_pair(
        self, 
        record1: Dict[str, Any], 
        record2: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Get explanation for why a pair is predicted as duplicate or not.
        
        Parameters
        ----------
        record1 : Dict[str, Any]
            First record.
        record2 : Dict[str, Any]
            Second record.
            
        Returns
        -------
        Dict[str, Any]
            Explanation with key features and their contributions.
        """
        if not self.trained:
            raise RuntimeError("Model must be trained before getting explanations")
        
        # Convert records to dataframes
        df1 = pd.DataFrame([record1])
        df2 = pd.DataFrame([record2])
        
        # Generate features
        X = self._generate_pair_features(df1, df2)
        
        # Ensure all expected features are present
        for feature in self.feature_names_:
            if feature not in X:
                X[feature] = 0
        
        # Keep only features used during training
        X = X[self.feature_names_]
        
        # Get prediction
        if self.ensemble_models:
            probability = self._predict_ensemble_proba(X)[0]
        else:
            probability = self.model.predict_proba(X)[0, 1]
        
        # For tree-based models, get feature contributions if available
        feature_contributions = {}
        explanation = {
            'probability': probability,
            'is_duplicate': probability >= self.optimal_threshold,
            'threshold': self.optimal_threshold,
            'key_differences': [],
            'key_similarities': []
        }
        
        # Generate simpler explanation based on data
        for feature in self.key_features:
            if feature in record1 and feature in record2:
                val1, val2 = record1[feature], record2[feature]
                
                if pd.api.types.is_numeric_dtype(pd.Series([val1, val2])):
                    # Numeric features
                    diff = abs(val1 - val2)
                    if diff < 0.001:
                        explanation['key_similarities'].append(f"{feature}: Exact match ({val1})")
                    else:
                        explanation['key_differences'].append(f"{feature}: {val1} vs {val2}")
                elif isinstance(val1, str) and isinstance(val2, str):
                    # String features
                    if val1.lower() == val2.lower():
                        explanation['key_similarities'].append(f"{feature}: Exact match ({val1})")
                    elif val1.lower() in val2.lower() or val2.lower() in val1.lower():
                        explanation['key_similarities'].append(f"{feature}: Partial match ({val1} / {val2})")
                    else:
                        # Get Levenshtein distance
                        from freamon.deduplication.fuzzy_deduplication import calculate_levenshtein_similarity
                        similarity = calculate_levenshtein_similarity(val1, val2)
                        if similarity > 0.8:
                            explanation['key_similarities'].append(f"{feature}: Similar values ({val1} / {val2})")
                        else:
                            explanation['key_differences'].append(f"{feature}: Different values ({val1} vs {val2})")
                else:
                    # Other types
                    if val1 == val2:
                        explanation['key_similarities'].append(f"{feature}: Exact match ({val1})")
                    else:
                        explanation['key_differences'].append(f"{feature}: Different values ({val1} vs {val2})")
        
        return explanation
    
    def incremental_fit(
        self,
        df: pd.DataFrame,
        new_duplicate_pairs: List[Tuple[int, int]],
        learning_rate: float = 0.5
    ) -> 'SupervisedDeduplicationModel':
        """
        Incrementally update the model with new data without full retraining.
        
        Parameters
        ----------
        df : pd.DataFrame
            The new dataset containing records.
        new_duplicate_pairs : List[Tuple[int, int]]
            List of tuples containing index pairs of new known duplicates.
        learning_rate : float, default=0.5
            Rate at which to incorporate new data (0-1).
            
        Returns
        -------
        SupervisedDeduplicationModel
            The updated model.
        """
        # Enable incremental mode
        self.incremental_mode = True
        
        # If no previous model, just do a regular fit
        if not self.trained:
            return self.fit(df, new_duplicate_pairs)
        
        # Check if data schema has changed
        if set(df.columns) != set(self.key_features + self.date_features):
            # Schema change requires full retraining
            return self.fit(df, new_duplicate_pairs)
        
        # Create training pairs from new data
        df1_new, df2_new, y_new = self._create_training_pairs(df, new_duplicate_pairs)
        
        # Generate features for new pairs
        X_new = self._generate_pair_features(df1_new, df2_new)
        
        # Ensure feature columns match
        for feature in self.feature_names_:
            if feature not in X_new:
                X_new[feature] = 0
        
        # Keep only features used in original training
        X_new = X_new[self.feature_names_]
        
        # For LightGBM, we can do true incremental learning
        if self.model_type == 'lightgbm':
            self.model.fit(X_new, y_new, xgb_model=self.model, **{'learning_rate': learning_rate})
        else:
            # For other models, we'll do a simple weighted averaging of predictions
            # This isn't true incremental learning but provides a reasonable approximation
            # Save the current model
            original_model = self.model
            
            # Train a new model on the new data
            self.model = self._create_model()
            self.model.fit(X_new, y_new)
            
            # Store this as a separate model
            new_model = self.model
            
            # Restore original model
            self.model = original_model
            
            # Add the new model to an ensemble
            self.ensemble_models = [original_model, new_model]
            self.ensemble_weights = [1.0 - learning_rate, learning_rate]
        
        # Update fingerprint of the data
        self.previous_data_size = len(df)
        self.previous_features = self.feature_names_
        
        return self