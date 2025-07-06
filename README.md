# News Sentiment Return Forecasting

Investigates whether financial news sentiment can be used to predict short-term stock returns. It combines alternative data (news headlines from NewsAPI, tweets from the Twitter API, and Reddit posts from the Reddit API) with traditional financial data to evaluate the predictive power of sentiment signals using machine learning models.

## Features

- Collects historical news articles using NewsAPI, Twitter API and Reddit API.
- Computes daily sentiment scores using rule-based and transformer-based models (VADER and FinBERT).
- Builds supervised datasets aligning sentiment with future returns.
- Trains Linear Regression and XGBoost models for return forecasting.
- Evaluates predictive performance using Mean Squared Error (MSE), Information Coefficient (Spearman Rank) and Directional Accuracy.

## How to Run

1. Set your API keys

```bash
export NEWSAPI_KEY=yourkey
export TWITTER_BEARER_TOKEN=yourkey
export REDDIT_CLIENT_SECRET=yoursecret
export REDDIT_CLIENT_ID=yourclientid
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the pipeline

```bash
python main.py
```
