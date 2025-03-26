from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor, StackingRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor

def get_regression_models():
    """
    Returns a dictionary of instantiated regression models with optimized parameters
    """
    # Define base models for ensembles
    xgb_model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=6, random_state=42, n_jobs=-1)
    lgbm_model = LGBMRegressor(n_estimators=100, learning_rate=0.1, max_depth=15, random_state=42, n_jobs=-1, verbose=-1)
    rf_model = RandomForestRegressor(n_estimators=100, max_depth=15, min_samples_split=5, random_state=42, n_jobs=-1)
    gb_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    
    regression_models = {
        'linear_regression': LinearRegression(
            n_jobs=-1,
            fit_intercept=True
        ),
        'ridge': Ridge(
            alpha=1.0,
            random_state=42,
            solver='auto'
        ),
        'lasso': Lasso(
            alpha=0.1,
            random_state=42,
            max_iter=2000
        ),
        'elastic_net': ElasticNet(
            alpha=0.1,
            l1_ratio=0.5,
            random_state=42,
            max_iter=2000
        ),
        'polynomial_regression': Pipeline([
            ('poly', PolynomialFeatures(degree=2)),
            ('linear', LinearRegression(fit_intercept=True))
        ]),
        'svr': SVR(
            kernel='rbf',
            C=1.0,
            epsilon=0.1,
            gamma='scale'
        ),
        'decision_tree': DecisionTreeRegressor(
            max_depth=10,
            min_samples_split=5,
            random_state=42
        ),
        'random_forest': rf_model,
        'gradient_boosting': gb_model,
        'xgboost': xgb_model,
        'lightgbm': lgbm_model,
        
        # Ensemble models
        'ensemble_stack_1': StackingRegressor(
            estimators=[
                ('xgb', xgb_model),
                ('lgbm', lgbm_model),
                ('rf', rf_model)
            ],
            final_estimator=Ridge(alpha=1.0),
            cv=5
        ),
        'ensemble_stack_2': StackingRegressor(
            estimators=[
                ('xgb', xgb_model),
                ('gb', gb_model),
                ('rf', rf_model)
            ],
            final_estimator=Ridge(alpha=1.0),
            cv=5
        ),
        'ensemble_voting': VotingRegressor(
            estimators=[
                ('xgb', xgb_model),
                ('lgbm', lgbm_model),
                ('rf', rf_model)
            ]
        )
    }
    return regression_models