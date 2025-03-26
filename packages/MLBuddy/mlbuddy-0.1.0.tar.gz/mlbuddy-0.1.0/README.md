# MLBuddy
MLBuddy is a simple yet powerful machine learning automation library that helps you quickly build, evaluate, and compare multiple machine learning models with minimal code.

## Features
- Automatic preprocessing of data
- Support for both classification and regression tasks
- Built-in model selection with optimized hyperparameters
- Model performance comparison through a leaderboard
- Easy evaluation on test data
- Ensemble models for improved performance

## Quick Start

```python
import pandas as pd
from MLBuddy import MLBuddy
from sklearn.model_selection import train_test_split

# Load your dataset
df = pd.read_csv('your_dataset.csv')

# Split into train and test sets
train, test = train_test_split(df, test_size=0.2, random_state=42)

# Initialize MLBuddy with your target column and task type
predictor = MLBuddy(label='target_column', task_type='classification')  # or 'regression'

# Fit models on training data
predictor.fit(train)

# View model performance leaderboard
print(predictor.leaderboard())

# Evaluate the best model on test data
test_performance = predictor.evaluate(test)
print(test_performance)
```


## Supported Models
### Classification
- Logistic Regression
- Naive Bayes
- Support Vector Machine (SVM)
- K-Nearest Neighbors (KNN)
- Decision Tree
- Random Forest
- Gradient Boosting
- XGBoost
- LightGBM
- AdaBoost
- Ensemble models (stacking and voting)
### Regression
- Linear Regression
- Ridge Regression
- Lasso Regression
- Elastic Net
- Polynomial Regression
- Support Vector Regression (SVR)
- Decision Tree
- Random Forest
- Gradient Boosting
- XGBoost
- LightGBM
- Ensemble models (stacking and voting)
## Advanced Usage
### Custom Preprocessing
MLBuddy automatically handles:

- Missing value imputation
- Categorical encoding
- Feature scaling
- Feature selection
### Performance Metrics Classification
- Accuracy
- Precision
- Recall
- F1 Score Regression
- R² Score

## License
This project is licensed under the MIT License - see the LICENSE file for details.