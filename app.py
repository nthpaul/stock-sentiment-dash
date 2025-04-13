import streamlit as st
import plotly.express as px
from data import get_all_data
import pandas as pd
import yfinance as yf

# Initialize session state for caching
if 'last_ticker' not in st.session_state:
    st.session_state.last_ticker = None

# Streamlit app
st.title("AI-Powered Stock Sentiment Dashboard")
st.markdown("""
This app analyzes social media sentiment about stocks and correlates it with price movements.
Enter any stock ticker to see its analysis.
""")

# Ticker input
ticker = st.text_input("Enter Stock Ticker", value="AAPL").upper()

if ticker:
    # Show loading message
    with st.spinner(f'Loading data for {ticker}...'):
        try:
            # Get basic stock info
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Company info section
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader(f"{info.get('longName', ticker)}")
                st.markdown(f"""
                **Sector:** {info.get('sector', 'N/A')}  
                **Industry:** {info.get('industry', 'N/A')}  
                **Website:** [{info.get('website', 'N/A')}]({info.get('website', '#')})
                """)
            
            with col2:
                st.metric(
                    "Current Price",
                    f"${info.get('currentPrice', 'N/A')}",
                    f"{info.get('regularMarketChangePercent', 0):.2f}%"
                )
            
            # Only fetch new data if ticker changed
            if st.session_state.last_ticker != ticker:
                stock_data, posts, sentiment_trend = get_all_data(ticker=ticker)
                st.session_state.last_ticker = ticker
                st.session_state.stock_data = stock_data
                st.session_state.posts = posts
                st.session_state.sentiment_trend = sentiment_trend
            else:
                stock_data = st.session_state.stock_data
                posts = st.session_state.posts
                sentiment_trend = st.session_state.sentiment_trend

            # Stock price plot
            st.subheader(f"{ticker} Stock Price (Last 7 Days)")
            fig1 = px.line(stock_data, x="Date", y="Close", title=f"{ticker} Closing Price")
            fig1.update_traces(line_color='#2E91E5')
            st.plotly_chart(fig1)

            # Only show sentiment analysis if we have posts
            if not sentiment_trend.empty and 'sentiment' in sentiment_trend.columns:
                # Sentiment trend plot
                st.subheader(f"Sentiment Trend from X Posts about {ticker}")
                fig2 = px.line(
                    sentiment_trend,
                    x="date",
                    y="sentiment",
                    title=f"Average Daily Sentiment for {ticker} (+1 = Positive, -1 = Negative)"
                )
                fig2.update_traces(line_color='#00CC96')
                st.plotly_chart(fig2)

                # Correlation scatter
                st.subheader("Sentiment vs. Price Correlation")
                merged = stock_data.merge(sentiment_trend, left_on="Date", right_on="date")
                if not merged.empty:
                    fig3 = px.scatter(
                        merged,
                        x="sentiment",
                        y="Close",
                        title=f"Sentiment vs. Closing Price for {ticker}",
                        hover_data=["Date"],
                        trendline="ols"
                    )
                    st.plotly_chart(fig3)
                    
                    # Calculate correlation
                    correlation = merged['sentiment'].corr(merged['Close'])
                    st.markdown(f"**Correlation coefficient:** {correlation:.2f}")

                # Show raw posts in an expander
                with st.expander("View Raw X Posts"):
                    if not posts.empty and all(col in posts.columns for col in ["timestamp", "text", "sentiment", "confidence"]):
                        st.dataframe(
                            posts[["timestamp", "text", "sentiment", "confidence"]],
                            column_config={
                                "timestamp": "Time",
                                "text": "Post",
                                "sentiment": st.column_config.NumberColumn(
                                    "Sentiment",
                                    help="1 = Positive, -1 = Negative",
                                    format="%.2f"
                                ),
                                "confidence": st.column_config.ProgressColumn(
                                    "Confidence",
                                    help="Model's confidence in the sentiment prediction",
                                    format="%.0f%%",
                                    min_value=0,
                                    max_value=1,
                                )
                            }
                        )
            else:
                st.warning(f"No social media posts found for {ticker}. This could be due to API rate limits or no recent posts.")
                
        except Exception as e:
            st.error(f"Error loading data for {ticker}. Please make sure you entered a valid ticker symbol.")
            st.exception(e)
else:
    st.info("Please enter a stock ticker symbol (e.g., AAPL for Apple Inc.)")