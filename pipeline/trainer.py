"""
Handles model training for sentiment-driven return prediction.

Currently supports:
- Linear Regression (via scikit-learn)
- XGBoost (optional)
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from typing import Tuple


def train_model(
    X: np.ndarray,
    y: np.ndarray,
    model_type: str = "linear",
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple:
    """
    Trains a regression model to predict returns from sentiment and price features.

    Args:
        X (np.ndarray): Feature matrix.
        y (np.ndarray): Target returns.
        model_type (str): Type of model to train ("linear" or "xgboost").
        test_size (float): Fraction of data to reserve for validation.
        random_state (int): Seed for reproducibility.

    Returns:
        Tuple: (trained model, X_test, y_test, y_pred)
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    if model_type == "linear":
        model = LinearRegression()
    elif model_type == "xgboost":
        from xgboost import XGBRegressor
        model = XGBRegressor(
            n_estimators=100,
            max_depth=3,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            objective="reg:squarederror",
            random_state=random_state
        )
    else:
        raise ValueError(f"Unsupported model type: {model_type}")

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    return model, X_test, y_test, y_pred