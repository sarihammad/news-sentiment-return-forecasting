import numpy as np
from scipy.stats import spearmanr
from sklearn.metrics import mean_squared_error


def evaluate_mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Computes Mean Squared Error between true and predicted returns.

    Args:
        y_true (np.ndarray): Ground truth returns.
        y_pred (np.ndarray): Predicted returns.

    Returns:
        float: Mean Squared Error.
    """
    return mean_squared_error(y_true, y_pred)


def evaluate_ic(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Computes Information Coefficient (Spearman correlation) between predictions and actuals.

    Args:
        y_true (np.ndarray): Ground truth returns.
        y_pred (np.ndarray): Predicted returns.

    Returns:
        float: Spearman correlation coefficient.
    """
    ic, _ = spearmanr(y_true, y_pred)
    return ic if np.isscalar(ic) else float(np.array(ic).flatten()[0])


def evaluate_directional_accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Measures the proportion of times the predicted direction matches the true direction.

    Args:
        y_true (np.ndarray): Ground truth returns.
        y_pred (np.ndarray): Predicted returns.

    Returns:
        float: Accuracy of predicting correct direction (up/down).
    """
    return np.mean(np.sign(y_true) == np.sign(y_pred))


def evaluate_model(model, X_test: np.ndarray, y_test: np.ndarray, y_pred: np.ndarray) -> dict:
    """
    Evaluates a trained regression model on test data using MSE, IC, and directional accuracy.

    Args:
        model: Trained regression model.
        X_test (np.ndarray): Test features.
        y_test (np.ndarray): Test targets.

    Returns:
        dict: Evaluation metrics.
    """
    return {
        "MSE": evaluate_mse(y_test, y_pred),
        "IC": evaluate_ic(y_test, y_pred),
        "Directional Accuracy": evaluate_directional_accuracy(y_test, y_pred)
    }