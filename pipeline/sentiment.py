"""
Computes sentiment scores from news headlines or articles.

Supports rule-based (VADER) and transformer-based (FinBERT) sentiment models.
"""

import pandas as pd

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def compute_vader_sentiment(news_df: pd.DataFrame) -> pd.Series:
    """
    Computes compound sentiment score using VADER.

    Args:
        news_df (pd.DataFrame): News headlines with a 'title' column.

    Returns:
        pd.Series: Compound sentiment scores for each headline.
    """
    sid = SentimentIntensityAnalyzer()
    return news_df["title"].apply(lambda x: sid.polarity_scores(x)["compound"])


def compute_finbert_sentiment(news_df: pd.DataFrame) -> pd.Series:
    """
    Computes sentiment using FinBERT model.

    Args:
        news_df (pd.DataFrame): News headlines with a 'title' column.

    Returns:
        pd.Series: Sentiment scores (positive - negative probability).
    """
    tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
    model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")
    model.eval()

    sentiments = []
    for text in news_df["title"]:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            logits = model(**inputs).logits
            probs = F.softmax(logits, dim=-1).squeeze()
            sentiment_score = probs[2].item() - probs[0].item()  # positive - negative
        sentiments.append(sentiment_score)

    return pd.Series(sentiments)


def compute_sentiment_scores(news_df: pd.DataFrame, model: str = "finbert") -> pd.Series:
    """
    Computes sentiment scores using specified model.

    Args:
        news_df (pd.DataFrame): News headlines DataFrame.
        model (str): Sentiment model to use: 'vader' or 'finbert'.

    Returns:
        pd.Series: Sentiment scores.
    """
    if model == "vader":
        return compute_vader_sentiment(news_df)
    elif model == "finbert":
        return compute_finbert_sentiment(news_df)
    else:
        raise ValueError("Invalid model. Choose 'vader' or 'finbert'.")