import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from typing import Optional, List, Dict, Tuple

class DataPreprocessor:
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.numeric_columns = None
        self.categorical_columns = None
        self.target_encoder = LabelEncoder()
        self.is_fitted = False
        
    def preprocess(self, df: pd.DataFrame, target_column: str) -> Tuple[pd.DataFrame, Dict]:
        """
        Preprocess the data by handling missing values, encoding categorical variables,
        and scaling numerical features.
        
        Args:
            df: Input DataFrame
            target_column: Name of the target variable column
            
        Returns:
            Tuple of (preprocessed DataFrame, preprocessing_info)
        """
        df = df.copy()
        
        # Identify column types
        if not self.is_fitted:
            self.numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
            self.categorical_columns = df.select_dtypes(include=['object']).columns
        
        # Handle missing values
        df = self._handle_missing_values(df)
        
        # Separate features and target
        X = df.drop(target_column, axis=1)
        y = df[target_column]
        
        # First time preprocessing (fit)
        if not self.is_fitted:
            # Encode categorical variables
            for col in self.categorical_columns:
                if col != target_column:
                    self.label_encoders[col] = LabelEncoder()
                    X[col] = self.label_encoders[col].fit_transform(X[col])
            
            # Scale numeric features
            numeric_features = [col for col in self.numeric_columns if col != target_column]
            if numeric_features:
                X[numeric_features] = self.scaler.fit_transform(X[numeric_features])
            
            # Encode target if categorical
            if target_column in self.categorical_columns:
                y = self.target_encoder.fit_transform(y)
            
            self.is_fitted = True
            
        # Transform only (for test data)
        else:
            # Handle categorical variables
            for col in self.categorical_columns:
                if col != target_column:
                    # Handle unseen categories
                    X[col] = X[col].map(lambda x: x if x in self.label_encoders[col].classes_ else self.label_encoders[col].classes_[0])
                    X[col] = self.label_encoders[col].transform(X[col])
            
            # Scale numeric features
            numeric_features = [col for col in self.numeric_columns if col != target_column]
            if numeric_features:
                X[numeric_features] = self.scaler.transform(X[numeric_features])
            
            # Encode target if categorical
            if target_column in self.categorical_columns:
                y = self.target_encoder.transform(y)
        
        # Combine processed features with target
        processed_df = X.copy()
        processed_df[target_column] = y
        
        # Create preprocessing info dictionary
        preprocessing_info = {
            'numeric_columns': list(self.numeric_columns),
            'categorical_columns': list(self.categorical_columns),
            'label_encoders': self.label_encoders,
            'target_encoder': self.target_encoder if target_column in self.categorical_columns else None,
            'scaler': self.scaler
        }
        
        return processed_df, preprocessing_info
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in the DataFrame"""
        # Fill numeric missing values with median
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        for col in numeric_cols:
            df[col] = df[col].fillna(df[col].median())
        
        # Fill categorical missing values with mode
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            df[col] = df[col].fillna(df[col].mode()[0])
        
        return df 