"""
Fetches Reddit posts from subreddits like r/stocks or r/investing using Pushshift API.

Includes:
- Historical post fetching by keyword/ticker
- Subreddit filtering
- Date range support
- JSON saving to raw/ directory
"""

import os
import requests
import json
from datetime import datetime, timedelta
from typing import List

SAVE_DIR = "data/raw/reddit"
os.makedirs(SAVE_DIR, exist_ok=True)

PUSHSHIFT_URL = "https://api.pushshift.io/reddit/search/submission"

def fetch_posts_for_day(query: str, date: str, subreddit: str = "stocks") -> List[dict]:
    """
    Fetches Reddit posts from a specific day and subreddit.

    Args:
        query (str): Keyword or ticker to search for.
        date (str): Date string (YYYY-MM-DD).
        subreddit (str): Subreddit to search in.

    Returns:
        List[dict]: List of Reddit post dicts.
    """
    after = int(datetime.strptime(date, "%Y-%m-%d").timestamp())
    before = int((datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)).timestamp())

    params = {
        "q": query,
        "subreddit": subreddit,
        "after": after,
        "before": before,
        "size": 100,
        "sort": "desc",
        "sort_type": "score"
    }

    response = requests.get(PUSHSHIFT_URL, params=params)
    if response.status_code != 200:
        raise Exception(f"Pushshift error: {response.status_code} {response.text}")
    return response.json().get("data", [])

def save_posts(posts: List[dict], date: str, query: str):
    """
    Saves Reddit posts to a JSON file.

    Args:
        posts (List[dict]): List of post dicts.
        date (str): Date used in filename.
        query (str): Search query used in filename.
    """
    filename = os.path.join(SAVE_DIR, f"{query}_{date}.json")
    with open(filename, "w") as f:
        json.dump(posts, f, indent=2)

def fetch_range(query: str, start_date: str, end_date: str, subreddit: str = "stocks"):
    """
    Fetches Reddit posts for a range of dates.

    Args:
        query (str): Keyword or ticker to search.
        start_date (str): Start date (YYYY-MM-DD).
        end_date (str): End date (YYYY-MM-DD).
        subreddit (str): Subreddit to search in.
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    for delta in range((end - start).days + 1):
        day = (start + timedelta(days=delta)).strftime("%Y-%m-%d")
        print(f"Fetching Reddit posts for {query} on {day}...")
        try:
            posts = fetch_posts_for_day(query, day, subreddit)
            save_posts(posts, day, query)
        except Exception as e:
            print(f"Error fetching {day}: {e}")