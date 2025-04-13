import yfinance as yf
import pandas as pd
from transformers import pipeline
import tweepy
import os
from datetime import datetime, timedelta
from typing import List, Dict
from dotenv import load_dotenv
import json
from pathlib import Path
import time

# Load environment variables from .env file
print("Loading environment variables...")
load_dotenv()

# X API Configuration
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Cache configuration
CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)
CACHE_DURATION = timedelta(minutes=15)  # Cache tweets for 15 minutes

def load_cache(ticker: str) -> tuple[pd.DataFrame, datetime]:
    """Load cached tweets for a ticker if they exist and are recent."""
    cache_file = CACHE_DIR / f"{ticker}_tweets.json"
    if cache_file.exists():
        with open(cache_file) as f:
            cache_data = json.load(f)
            cache_time = datetime.fromisoformat(cache_data['timestamp'])
            if datetime.utcnow() - cache_time < CACHE_DURATION:
                print(f"Using cached tweets for {ticker} from {cache_time}")
                return pd.DataFrame(cache_data['tweets']), cache_time
    return pd.DataFrame(), None

def save_cache(ticker: str, tweets: list[dict]):
    """Save tweets to cache with current timestamp."""
    cache_file = CACHE_DIR / f"{ticker}_tweets.json"
    cache_data = {
        'timestamp': datetime.utcnow().isoformat(),
        'tweets': tweets
    }
    with open(cache_file, 'w') as f:
        json.dump(cache_data, f)

def get_twitter_client() -> tweepy.Client:
    """
    Create and verify a Twitter API client using bearer token authentication.
    Raises ValueError with detailed message if credentials are missing or invalid.
    """
    if not TWITTER_BEARER_TOKEN:
        raise ValueError(
            "Missing Twitter API credentials: TWITTER_BEARER_TOKEN\n"
            "Please set this environment variable in your .env file:\n"
            "TWITTER_BEARER_TOKEN=your_bearer_token_here"
        )
    
    try:
        # For search-only operations, we only need the bearer token
        client = tweepy.Client(
            bearer_token=TWITTER_BEARER_TOKEN,
            wait_on_rate_limit=True
        )
        return client
        
    except tweepy.TweepyException as e:
        raise ValueError(
            f"Failed to authenticate with Twitter API: {str(e)}\n"
            "Please verify your bearer token is correct."
        )

def analyze_sentiment(posts):
    classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    results = classifier(posts["text"].tolist())
    posts["sentiment"] = [1 if r["label"] == "POSITIVE" else -1 for r in results]
    posts["confidence"] = [r["score"] for r in results]
    return posts

def get_x_posts(ticker: str = "AAPL", days: int = 7) -> pd.DataFrame:
    """
    Fetch recent X posts about a specific stock ticker.
    Uses caching to avoid rate limits and provide faster responses.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., "AAPL")
        days (int): Number of days of historical data to fetch
    
    Returns:
        pd.DataFrame: DataFrame containing posts with timestamp and text
    """
    # Try to load from cache first
    cached_df, cache_time = load_cache(ticker)
    if not cached_df.empty:
        return cached_df

    try:
        client = get_twitter_client()
        
        # Format search query for stock mentions
        query = f"${ticker} OR #{ticker} -is:retweet lang:en"
        
        # Calculate time window - start with last 24 hours to avoid rate limits
        end_time = datetime.utcnow() - timedelta(seconds=30)
        start_time = end_time - timedelta(days=1)  # Start with 1 day
        
        print(f"Searching tweets from {start_time} to {end_time}")
        
        # Fetch tweets
        tweets = []
        try:
            print("Fetching tweets (this might take a moment due to rate limits)...")
            response = client.search_recent_tweets(
                query=query,
                start_time=start_time,
                end_time=end_time,
                max_results=100,  # Max allowed per request
                tweet_fields=['created_at', 'text']
            )
            
            if response and response.data:
                for tweet in response.data:
                    tweets.append({
                        'timestamp': tweet.created_at,
                        'text': tweet.text,
                        'date': tweet.created_at.date()
                    })
                
                # Cache the results
                save_cache(ticker, tweets)
                
        except tweepy.TooManyRequests as e:
            print("Rate limit exceeded. Using cached data if available or returning empty results.")
            if not cached_df.empty:
                return cached_df
            return pd.DataFrame(columns=['timestamp', 'text', 'date'])
            
        except tweepy.TweepyException as e:
            print(f"Error during tweet search: {str(e)}")
            if not cached_df.empty:
                return cached_df
            return pd.DataFrame(columns=['timestamp', 'text', 'date'])
        
        if not tweets:
            print(f"Warning: No tweets found for {ticker} in the last 24 hours")
            if not cached_df.empty:
                return cached_df
            return pd.DataFrame(columns=['timestamp', 'text', 'date'])
        
        df = pd.DataFrame(tweets)
        print(f"Found {len(df)} tweets")
        return df
    
    except Exception as e:
        print(f"Error fetching tweets: {str(e)}")
        if not cached_df.empty:
            return cached_df
        return pd.DataFrame(columns=['timestamp', 'text', 'date'])

def get_all_data(ticker="AAPL"):
    try:
        stock_data = get_stock_data(ticker)
        posts = get_x_posts(ticker)  # Updated to use real X API
        
        if not posts.empty:
            posts = analyze_sentiment(posts)
            sentiment_trend = posts.groupby("date")["sentiment"].mean().reset_index()
        else:
            # Handle case when no posts are found
            sentiment_trend = pd.DataFrame(columns=['date', 'sentiment'])
        
        return stock_data, posts, sentiment_trend
        
    except ValueError as e:
        # Handle authentication errors
        print(f"Authentication Error: {str(e)}")
        # Return empty DataFrames with expected columns
        stock_data = get_stock_data(ticker)
        posts = pd.DataFrame(columns=['timestamp', 'text', 'date', 'sentiment', 'confidence'])
        sentiment_trend = pd.DataFrame(columns=['date', 'sentiment'])
        return stock_data, posts, sentiment_trend

def get_stock_data(ticker="AAPL", period="7d"):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    df = df[["Close"]].reset_index()
    df["Date"] = df["Date"].dt.date
    return df

if __name__ == "__main__":
    stock_data, posts, sentiment_trend = get_all_data()
    print("Stock Data:\n", stock_data.head())
    print("Posts with Sentiment:\n", posts[["text", "sentiment", "confidence"]])
    print("Sentiment Trend:\n", sentiment_trend)