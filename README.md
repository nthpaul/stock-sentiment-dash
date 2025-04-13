# Stock Sentiment Dashboard

A real-time dashboard that analyzes stock market sentiment using X (Twitter) posts and correlates it with stock prices. Built with Python, Streamlit, and AI-powered sentiment analysis.

## Features

- Real-time stock price data using yfinance
- X (Twitter) post analysis for stock-related discussions
- AI-powered sentiment analysis using DistilBERT
- Interactive visualizations with Plotly
- Sentiment vs. Price correlation analysis
- Caching system to handle API rate limits

## Prerequisites

- Python 3.12 or higher
- X (Twitter) API credentials (see below)
- pip (Python package manager)

## Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/stock-sentiment-dash.git
cd stock-sentiment-dash
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up X API credentials:
   - Go to [Twitter Developer Portal](https://developer.twitter.com)
   - Create a new project and app
   - Get your Bearer Token
   - Create a `.env` file in the project root with:

```
TWITTER_BEARER_TOKEN=your_bearer_token_here
```

## Running the App

1. Make sure your virtual environment is activated
2. Run the Streamlit app:

```bash
streamlit run app.py
```

3. Open your browser at `http://localhost:8501`

## Usage

- The dashboard shows real-time stock data for AAPL (Apple Inc.)
- Stock price chart shows the last 7 days of closing prices
- Sentiment analysis is performed on recent X posts mentioning the stock
- Sentiment trend shows how social media sentiment changes over time
- Correlation plot helps visualize the relationship between sentiment and price
- Raw X posts are displayed with their sentiment scores

## Troubleshooting

- If you see "Rate limit exceeded" messages, the app will use cached data if available
- Cached data is stored for 15 minutes to avoid API rate limits
- Make sure your X API credentials are correctly set in the `.env` file
- Check that all dependencies are installed correctly

## Technical Details

- Stock data: yfinance
- Sentiment analysis: DistilBERT (Hugging Face Transformers)
- X API: tweepy
- Frontend: Streamlit
- Visualization: Plotly Express
- Data handling: pandas

## License

MIT License - feel free to use this project for your own purposes.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
