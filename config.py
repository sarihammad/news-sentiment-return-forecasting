"""
Configuration file for sentiment-based return prediction project.

Includes:
- Paths to data directories and files
- Model training parameters
- Ingestion parameters
"""

# file paths
NEWS_DATA_PATH = "data/news_data.csv"
PRICE_DATA_PATH = "data/price_data.csv"

# ingestion settings
START_DATE = "2022-01-01"
END_DATE = "2024-12-31"
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]
NEWS_SOURCES = ["NewsAPI", "Reddit"]

# sentiment model parameters
USE_TRANSFORMER = False  # If False, use Vader or FinBERT

# return computation
RETURN_HORIZON = 1  # next-day return

# train/test split
TEST_SPLIT_RATIO = 0.2

# ml training params
EPOCHS = 10
BATCH_SIZE = 32
LEARNING_RATE = 1e-3