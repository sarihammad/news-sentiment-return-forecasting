"""
Main script for sentiment-based return prediction.

Steps:
1. Ingest price and news data
2. Compute sentiment scores
3. Generate sentiment-return pairs
4. Train ML model to predict returns using sentiment features
5. Evaluate predictive performance
"""

from pipeline.ingestion import fetch_price_data, fetch_news_data
from pipeline.sentiment import compute_sentiment_scores
from pipeline.features import build_dataset
from pipeline.trainer import train_model
from pipeline.evaluator import evaluate_model
import config

def main():
    print("Loading price data...")
    price_df = fetch_price_data(config.TICKERS, config.START_DATE, config.END_DATE)

    print("Loading news data...")
    news_df = fetch_news_data(config.TICKERS, config.START_DATE, config.END_DATE)

    print("Computing sentiment scores...")
    sentiment_df = compute_sentiment_scores(news_df)

    print("Building dataset...")
    X, y = build_dataset(sentiment_df, price_df, config.RETURN_HORIZON)

    print("Training model...")
    model, X_test, y_test, y_pred = train_model(X, y, model_type="linear", test_size=config.TEST_SPLIT_RATIO)

    print("Evaluating model...")
    metrics = evaluate_model(model, X_test, y_test, y_pred)
    print("Evaluation metrics:", metrics)
    print("Evaluation complete.")

if __name__ == "__main__":
    main()