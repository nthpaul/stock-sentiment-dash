import streamlit as st
import plotly.express as px
from data import get_all_data
import pandas as pd

# Fetch data
stock_data, posts, sentiment_trend = get_all_data(ticker="AAPL")

# Streamlit app
st.title("AI-Powered Stock Sentiment Dashboard")
st.markdown("""
This app uses AI to analyze X posts about AAPL, showing how sentiment correlates with stock prices.
""")

# Stock price plot
st.subheader("AAPL Stock Price (Last 7 Days)")
fig1 = px.line(stock_data, x="Date", y="Close", title="AAPL Closing Price")
st.plotly_chart(fig1)

# Only show sentiment analysis if we have posts
if not sentiment_trend.empty and 'sentiment' in sentiment_trend.columns:
    # Sentiment trend plot
    st.subheader("Sentiment Trend from X Posts")
    fig2 = px.line(sentiment_trend, x="date", y="sentiment", title="Average Daily Sentiment (+1 = Positive, -1 = Negative)")
    st.plotly_chart(fig2)

    # Correlation scatter
    st.subheader("Sentiment vs. Price Correlation")
    merged = stock_data.merge(sentiment_trend, left_on="Date", right_on="date")
    if not merged.empty:
        fig3 = px.scatter(merged, x="sentiment", y="Close", title="Sentiment vs. Closing Price", hover_data=["Date"])
        st.plotly_chart(fig3)
else:
    st.warning("No sentiment data available. This could be due to API rate limits or no recent posts found.")

# Show raw posts
st.subheader("Sample X Posts")
if not posts.empty and all(col in posts.columns for col in ["timestamp", "text", "sentiment", "confidence"]):
    st.dataframe(posts[["timestamp", "text", "sentiment", "confidence"]])
else:
    st.warning("No X posts available for display.")