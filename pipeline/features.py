"""
Feature engineering for news-based sentiment forecasting.

Merges price and sentiment data, constructs lagged features, and
prepares supervised learning datasets.
"""

import pandas as pd
import numpy as np
from typing import Tuple


def build_dataset(
    price_df: pd.DataFrame,
    sentiment_df: pd.DataFrame,
    lookback: int = 5,
    horizon: int = 1
) -> Tuple[np.ndarray, np.ndarray, list]:
    """
    Combines price and sentiment data to form a supervised learning dataset.

    Args:
        price_df (pd.DataFrame): Daily closing prices with DatetimeIndex.
        sentiment_df (pd.DataFrame): Daily sentiment scores with 'date' and 'sentiment' columns.
        lookback (int): Number of past days used as input features.
        horizon (int): Days ahead to predict the return.

    Returns:
        Tuple[np.ndarray, np.ndarray, list]: Features (X), targets (y), and corresponding dates.
    """
    # Compute log returns
    log_returns = np.log(price_df / price_df.shift(1)).dropna()

    # Merge with sentiment
    sentiment_df['date'] = pd.to_datetime(sentiment_df['date'])
    sentiment_df = sentiment_df.set_index('date').resample('D').mean().ffill()
    sentiment_df = sentiment_df.reindex(log_returns.index).ffill()

    # Align on date
    combined = log_returns.to_frame(name='return').join(sentiment_df)

    # Build supervised dataset
    X, y, dates = [], [], []
    for i in range(lookback, len(combined) - horizon):
        window = combined.iloc[i - lookback:i]
        target = combined['return'].iloc[i + horizon]
        X.append(window.values.flatten())
        y.append(target)
        dates.append(combined.index[i + horizon])

    return np.array(X), np.array(y), dates