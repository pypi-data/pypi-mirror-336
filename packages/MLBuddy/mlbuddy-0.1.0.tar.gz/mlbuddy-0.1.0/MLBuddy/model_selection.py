import numpy as np
from typing import Dict, Any, Tuple
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, r2_score, make_scorer
from sklearn.model_selection import cross_val_score, KFold
from tqdm import tqdm

from .models.classification import get_classification_models
from .models.regression import get_regression_models

class ModelSelector:
    def __init__(self, task_type: str = "classification"):
        self.task_type = task_type
        self.models = (get_classification_models() if task_type == "classification" 
                      else get_regression_models())
        self.cv = KFold(n_splits=3, shuffle=True, random_state=42)
        
        # Create custom scorers with zero_division=0 to handle the warning
        if task_type == "classification":
            self.precision_scorer = make_scorer(precision_score, average='weighted', zero_division=0)
            self.recall_scorer = make_scorer(recall_score, average='weighted', zero_division=0)
            self.f1_scorer = make_scorer(f1_score, average='weighted', zero_division=0)

    def find_best_model(self, X, y) -> Dict[str, Any]:
        """Find the best performing model using cross-validation"""
        all_scores = {}
        best_score = -np.inf
        best_model = None
        best_model_name = None

        for model_name, model in tqdm(self.models.items(), desc="Training models"):
            # Get cross-validation scores
            if self.task_type == "classification":
                cv_scores = cross_val_score(model, X, y, cv=self.cv, scoring='accuracy')
            else:
                cv_scores = cross_val_score(model, X, y, cv=self.cv, scoring='r2')
            
            current_score = np.mean(cv_scores)
            
            # Store scores
            if self.task_type == "classification":
                # Use custom scorers with zero_division=0
                scores = {
                    'accuracy': current_score,
                    'precision': np.mean(cross_val_score(model, X, y, cv=self.cv, scoring=self.precision_scorer)),
                    'recall': np.mean(cross_val_score(model, X, y, cv=self.cv, scoring=self.recall_scorer)),
                    'f1': np.mean(cross_val_score(model, X, y, cv=self.cv, scoring=self.f1_scorer))
                }
            else:
                scores = {
                    'r2_score': current_score
                }
            
            all_scores[model_name] = scores
            
            if current_score > best_score:
                best_score = current_score
                best_model_name = model_name
                
                # Fit the best model on full training data
                best_model = model
                best_model.fit(X, y)

        return {
            'model': best_model,
            'model_name': best_model_name,
            'score': best_score,
            'all_scores': all_scores
        }

    def evaluate_model(self, model, X, y) -> Dict[str, float]:
        """Evaluate model on test data"""
        if self.task_type == "classification":
            y_pred = model.predict(X)
            return {
                'accuracy': accuracy_score(y, y_pred),
                'precision': precision_score(y, y_pred, average='weighted', zero_division=0),
                'recall': recall_score(y, y_pred, average='weighted', zero_division=0),
                'f1': f1_score(y, y_pred, average='weighted', zero_division=0)
            }
        else:
            return {
                'r2_score': r2_score(y, model.predict(X))
            }