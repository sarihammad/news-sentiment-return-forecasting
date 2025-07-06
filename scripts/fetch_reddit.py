"""
Fetches Reddit posts from subreddits like r/stocks or r/investing using the Reddit API.

Includes:
- Historical post fetching by keyword/ticker
- Subreddit filtering
- Date range support (limited by Reddit API)
- JSON saving to raw/ directory
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import List
from dotenv import load_dotenv

load_dotenv()

SAVE_DIR = "data/raw/reddit"
os.makedirs(SAVE_DIR, exist_ok=True)

CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = "news-sentiment-script/0.1"

def get_access_token():
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    data = {
        "grant_type": "client_credentials"
    }
    headers = {"User-Agent": USER_AGENT}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers)
    response.raise_for_status()
    return response.json()["access_token"]

def fetch_posts_for_day(query: str, date: str, subreddit: str = "stocks", limit: int = 100) -> List[dict]:
    """
    Fetches Reddit posts from a specific day using Reddit API.

    Args:
        query (str): Keyword or ticker to search for.
        date (str): Date string (YYYY-MM-DD).
        subreddit (str): Subreddit to search in.
        limit (int): Maximum number of results to return.

    Returns:
        List[dict]: List of Reddit post dicts.
    """
    token = get_access_token()
    headers = {"Authorization": f"bearer {token}", "User-Agent": USER_AGENT}

    after = int(datetime.strptime(date, "%Y-%m-%d").timestamp())
    before = int((datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)).timestamp())

    url = f"https://oauth.reddit.com/r/{subreddit}/search"
    params = {
        "q": query,
        "sort": "top",
        "restrict_sr": "true",
        "limit": str(limit),
        "after": after,
        "before": before,
        "t": "day"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"[Reddit API] Error: {response.status_code} - {response.text}")

    posts = response.json().get("data", {}).get("children", [])
    return [p["data"] for p in posts]

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