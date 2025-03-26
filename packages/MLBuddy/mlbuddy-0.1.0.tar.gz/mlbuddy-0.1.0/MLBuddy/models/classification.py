from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier, VotingClassifier, StackingClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

def get_classification_models():
    """
    Returns a dictionary of instantiated classification models with optimized parameters
    """
    # Define base models for ensembles - with reduced complexity for faster training
    xgb_model = XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=7,
        random_state=42,
        n_jobs=-1,
        eval_metric='logloss',
        tree_method='hist'  # Added faster tree method
    )
    lgbm_model = LGBMClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=10,
        random_state=42,
        n_jobs=-1,
        verbose=-1,
        subsample=0.8,  # Added subsampling for faster training
        feature_fraction=0.8  # Added feature fraction for faster training
    )
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1,
        bootstrap=True,  # Ensure bootstrap is enabled
        max_features='sqrt'  # Use sqrt of features for faster training
    )
    gb_model = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=7,
        random_state=42,
        subsample=0.8  # Added subsampling for faster training
    )
    
    classification_models = {
        'logistic_regression': LogisticRegression(
            C=1.0,
            class_weight='balanced',
            random_state=42,
            max_iter=700,
            solver='liblinear'
        ),
        'naive_bayes': GaussianNB(
            var_smoothing=1e-9
        ),
        'svm': SVC(
            C=1.0,
            kernel='rbf',
            probability=True,
            random_state=42,
            cache_size=1000  # Increased cache size for faster computation
        ),
        'knn': KNeighborsClassifier(
            n_neighbors=5,
            weights='distance',
            algorithm='kd_tree',  # Changed to kd_tree for faster computation
            leaf_size=30  # Optimized leaf size
        ),
        'decision_tree': DecisionTreeClassifier(
            max_depth=10,
            min_samples_split=5,
            random_state=42,
            min_samples_leaf=4  # Added min samples per leaf for faster training
        ),
        'random_forest': rf_model,
        'gradient_boosting': gb_model,
        'xgboost': xgb_model,
        'lightgbm': lgbm_model,
        'adaboost': AdaBoostClassifier(
            n_estimators=100,
            learning_rate=1.0,
            random_state=42
        ),
        
        # Ensemble models - optimized for faster training
        'ensemble_stack_1': StackingClassifier(
            estimators=[
                ('xgb', xgb_model),
                ('lgbm', lgbm_model),
                ('rf', rf_model)
            ],
            final_estimator=LogisticRegression(C=1.0, max_iter=700),
            cv=2,  # Reduced from 3 to 2 for faster training
            n_jobs=-1
        ),
        'ensemble_stack_2': StackingClassifier(
            estimators=[
                ('xgb', xgb_model),
                ('gb', gb_model),
                ('rf', rf_model)
            ],
            final_estimator=LogisticRegression(C=1.0, max_iter=700),
            cv=2,  # Reduced from 3 to 2 for faster training
            n_jobs=-1
        ),
        'ensemble_voting': VotingClassifier(
            estimators=[
                ('xgb', xgb_model),
                ('lgbm', lgbm_model),
                ('rf', rf_model)
            ],
            voting='soft',
            n_jobs=-1
        )
    }
    return classification_models
