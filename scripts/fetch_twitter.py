"""
Fetches tweets using Twitter API v2 for a given query or ticker.

Includes:
- Historical tweet fetching via Twitter API (recent 7 days)
- Date range support
- Saving to raw/ directory as JSON

Requires:
- Twitter Developer Bearer Token in .env file as TWITTER_BEARER_TOKEN
- Install dependencies: requests, python-dotenv
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import List
from dotenv import load_dotenv

load_dotenv()
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
SAVE_DIR = "data/raw/twitter"
os.makedirs(SAVE_DIR, exist_ok=True)

def fetch_tweets_for_day(query: str, date: str, max_results: int = 100) -> List[dict]:
    """
    Fetches tweets for a specific day using Twitter API v2 Recent Search endpoint.

    Args:
        query (str): Search keyword or ticker (e.g., "AAPL").
        date (str): Date string in YYYY-MM-DD format.
        max_results (int): Maximum tweets to fetch (max 100 per Twitter API limit).

    Returns:
        List[dict]: List of tweet objects with created_at, text, and author_id fields.
    """
    next_day = (datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    url = "https://api.twitter.com/2/tweets/search/recent"

    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    params = {
        "query": query + " lang:en -is:retweet",
        "start_time": f"{date}T00:00:00Z",
        "end_time": f"{next_day}T00:00:00Z",
        "max_results": min(max_results, 100),
        "tweet.fields": "created_at,author_id,text"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])
    except requests.RequestException as e:
        print(f"[Twitter API] Error fetching {query} on {date}: {e}")
        return []

def save_tweets(tweets: List[dict], date: str, query: str):
    """
    Saves fetched tweets to a local JSON file.

    Args:
        tweets (List[dict]): Tweets to save.
        date (str): Date string in YYYY-MM-DD format.
        query (str): Ticker or keyword used for the search.
    """
    filename = os.path.join(SAVE_DIR, f"{query}_{date}.json")
    with open(filename, "w") as f:
        json.dump(tweets, f, indent=2)

def fetch_range(query: str, start_date: str, end_date: str, max_tweets_per_day: int = 100):
    """
    Fetches tweets for a query across a date range and saves each day's results.

    Args:
        query (str): Keyword or ticker to search.
        start_date (str): Start date (YYYY-MM-DD).
        end_date (str): End date (YYYY-MM-DD).
        max_tweets_per_day (int): Max tweets to fetch per day.
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    for delta in range((end - start).days + 1):
        day = (start + timedelta(days=delta)).strftime("%Y-%m-%d")
        print(f"[Twitter API] Fetching {query} on {day}")
        tweets = fetch_tweets_for_day(query, day, max_tweets_per_day)
        save_tweets(tweets, day, query)