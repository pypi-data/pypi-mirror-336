import pandas as pd
from tqdm import tqdm
from typing import Optional, Dict, Any
from .preprocessing import DataPreprocessor
from .model_selection import ModelSelector

class MLBuddy:  # Changed back to MLBuddy from MLBud
    def __init__(self, label: str, task_type: str = "classification"):
        """
        Initialize MLBuddy
        
        Args:
            label: Name of the target column
            task_type: Either "classification" or "regression"
        """
        self.label = label
        self.task_type = task_type
        self.preprocessor = DataPreprocessor()
        self.model_selector = ModelSelector(task_type=task_type)
        self.best_model_info = None
        self.leaderboard_df = None
        self.preprocessing_info = None

    def fit(self, train_data: pd.DataFrame) -> None:
        """
        Fit the predictor on training data
        """
        print("Preprocessing data...")
        processed_df, self.preprocessing_info = self.preprocessor.preprocess(train_data, target_column=self.label)
        
        X = processed_df.drop(self.label, axis=1)
        y = processed_df[self.label]
        
        print("\nTraining and evaluating models...")
        self.best_model_info = self.model_selector.find_best_model(X, y)
        self._create_leaderboard()
        
    def _create_leaderboard(self) -> None:
        """Create leaderboard DataFrame from model results"""
        scores = self.best_model_info['all_scores']
        metrics = ['accuracy', 'precision', 'recall', 'f1'] if self.task_type == "classification" else ['r2_score']
        
        data = []
        for model_name, model_scores in scores.items():
            if self.task_type == "classification":
                data.append([
                    model_name,
                    model_scores['accuracy'],
                    model_scores['precision'],
                    model_scores['recall'],
                    model_scores['f1']
                ])
            else:
                data.append([model_name, model_scores['r2_score']])
        
        columns = ['model'] + metrics
        self.leaderboard_df = pd.DataFrame(data, columns=columns)
        self.leaderboard_df = self.leaderboard_df.sort_values(
            by=metrics[0], 
            ascending=False
        ).reset_index(drop=True)
    
    def leaderboard(self) -> pd.DataFrame:
        """Return the leaderboard of model performances"""
        if self.leaderboard_df is None:
            raise ValueError("Must call fit() before accessing leaderboard")
        return self.leaderboard_df

    def evaluate(self, test_data: pd.DataFrame) -> Dict[str, float]:
        """Evaluate the best model on test data"""
        if self.best_model_info is None:
            raise ValueError("Must call fit() before evaluate()")
            
        print(f"\nEvaluating best model ({self.best_model_info['model_name']}) on test data...")
        
        processed_test, _ = self.preprocessor.preprocess(test_data, target_column=self.label)
        X_test = processed_test.drop(self.label, axis=1)
        y_test = processed_test[self.label]
        
        return self.model_selector.evaluate_model(
            self.best_model_info['model'],
            X_test,
            y_test
        )