"""
Fetches financial news articles using the NewsAPI.

Includes:
- Daily article fetching by keyword or ticker
- Date range control
- NewsAPI request handling
- JSON saving to raw/ directory
"""

import os
import requests
import json
from datetime import datetime, timedelta
from typing import List

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

BASE_URL = "https://newsapi.org/v2/everything"
SAVE_DIR = "data/raw/newsapi"
os.makedirs(SAVE_DIR, exist_ok=True)

def fetch_articles_for_day(query: str, date: str, page_size: int = 100) -> List[dict]:
    """
    Fetches news articles for a specific query on a given date.

    Args:
        query (str): Keyword or ticker to search for.
        date (str): Date in YYYY-MM-DD format.
        page_size (int): Number of articles per page (max 100).

    Returns:
        List[dict]: List of news articles.
    """
    params = {
        "q": query,
        "from": date,
        "to": date,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": page_size,
        "apiKey": NEWSAPI_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch articles: {response.status_code} {response.text}")
    data = response.json()
    return data.get("articles", [])

def save_articles(articles: List[dict], date: str, ticker: str):
    """
    Saves the fetched articles as a JSON file.

    Args:
        articles (List[dict]): List of news article objects.
        date (str): Date string used in filename.
        ticker (str): Ticker or keyword used in search.
    """
    filename = os.path.join(SAVE_DIR, f"{ticker}_{date}.json")
    with open(filename, "w") as f:
        json.dump(articles, f, indent=2)

def fetch_range(query: str, start_date: str, end_date: str):
    """
    Fetches articles for a query from start_date to end_date (inclusive).

    Args:
        query (str): Keyword or ticker.
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    for delta in range((end - start).days + 1):
        day = (start + timedelta(days=delta)).strftime("%Y-%m-%d")
        print(f"Fetching {query} articles for {day}...")
        try:
            articles = fetch_articles_for_day(query, day)
            save_articles(articles, day, query)
        except Exception as e:
            print(f"Error on {day}: {e}")