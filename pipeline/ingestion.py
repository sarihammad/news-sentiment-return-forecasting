"""
Handles data ingestion for financial return prediction.

Includes:
- Price data fetching using yfinance
"""

import json
import pandas as pd
import yfinance as yf
from datetime import datetime
from typing import List
from dotenv import load_dotenv
import glob

from pipeline.reddit_fetcher import fetch_range as fetch_reddit_range
from pipeline.newsapi_fetcher import fetch_range as fetch_newsapi_range
from pipeline.twitter_fetcher import fetch_range as fetch_twitter_range

load_dotenv()

# price data
def fetch_price_data(tickers: List[str], start_date: str, end_date: str) -> pd.DataFrame:
    """
    Downloads adjusted close prices for given tickers.

    Args:
        tickers (List[str]): Stock tickers.
        start_date (str): Start date (YYYY-MM-DD).
        end_date (str): End date (YYYY-MM-DD).

    Returns:
        pd.DataFrame: Adjusted close prices.
    """
    print(f"[Price] Fetching price data for {tickers}...")
    data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True)
    return data["Close"].ffill().bfill()


def fetch_news_data(tickers: List[str], start_date: str, end_date: str):
    """
    Loads news data from disk for given tickers.

    Assumes that data fetching from NewsAPI, Reddit, and Twitter
    has been handled externally and data is stored in the respective
    directories.

    Args:
        tickers (List[str]): List of tickers or keywords.
        start_date (str): Start date (YYYY-MM-DD).
        end_date (str): End date (YYYY-MM-DD).
    """
    for ticker in tickers:
        fetch_newsapi_range(ticker, start_date, end_date)
        fetch_reddit_range(ticker, start_date, end_date)
        fetch_twitter_range(ticker, start_date, end_date)

    rows = []

    # load NewsAPI articles
    for f in glob.glob("data/raw/newsapi/*.json"):
        with open(f) as file:
            articles = json.load(file)
            for a in articles:
                rows.append({
                    "date": a.get("publishedAt", "")[:10],
                    "title": a.get("title", ""),
                    "description": a.get("description", ""),
                    "content": a.get("content", ""),
                    "source": "NewsAPI"
                })

    # load reddit posts
    for f in glob.glob("data/raw/reddit/*.json"):
        with open(f) as file:
            posts = json.load(file)
            for p in posts:
                rows.append({
                    "date": datetime.utcfromtimestamp(p.get("created_utc", 0)).strftime("%Y-%m-%d"),
                    "title": p.get("title", ""),
                    "description": "",
                    "content": p.get("selftext", ""),
                    "source": "Reddit"
                })

    # load twitter tweets
    for f in glob.glob("data/raw/twitter/*.json"):
        with open(f) as file:
            tweets = json.load(file)
            for t in tweets:
                rows.append({
                    "date": t.get("date", "")[:10],
                    "title": "",
                    "description": "",
                    "content": t.get("content", ""),
                    "source": "Twitter"
                })

    return pd.DataFrame(rows)