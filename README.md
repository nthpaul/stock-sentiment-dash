# Stock Sentiment Dashboard

A real-time dashboard that analyzes stock market sentiment using X (Twitter) posts and correlates it with stock prices. Built with Python, Streamlit, and AI-powered sentiment analysis.

## Demo

![Dashboard Demo](screenshot.png)

The dashboard provides real-time stock information and sentiment analysis. Above shows NVIDIA Corporation (NVDA) with its current price, sector, industry, and website information.

## Features

- Real-time stock data for any publicly traded company
- Company information including sector, industry, and current price
- X (Twitter) post analysis for stock-related discussions
- AI-powered sentiment analysis using DistilBERT
- Interactive visualizations with Plotly:
  - Stock price trends
  - Social media sentiment analysis
  - Price-sentiment correlation with trend lines
- Smart caching system to handle API rate limits
- Responsive design with real-time updates

## Demo Features

- Enter any stock ticker (e.g., AAPL, MSFT, TSLA)
- View company details and current stock price
- See stock price trends over the last 7 days
- Analyze social media sentiment about the stock
- Explore correlation between sentiment and price
- View individual X posts with sentiment scores
- Track sentiment confidence levels

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

4. Enter any stock ticker to analyze

## Usage Guide

1. **Enter a Stock Ticker**

   - Type any valid stock symbol in the input box
   - The app will automatically load company data

2. **Company Information**

   - View company name, sector, and industry
   - See current stock price and daily change
   - Access company website

3. **Stock Analysis**

   - Track stock price trends
   - View sentiment analysis from social media
   - Explore price-sentiment correlation
   - See correlation coefficient

4. **Social Media Analysis**
   - View sentiment trends over time
   - Explore individual X posts
   - See sentiment scores and confidence levels
   - Track sentiment changes

## Data Sources

- Stock Data: Yahoo Finance (yfinance)
- Social Media: X (Twitter) API
- Sentiment Analysis: DistilBERT model

## Troubleshooting

- If you see "Rate limit exceeded" messages, the app will use cached data if available
- Cached data is stored for 15 minutes to avoid API rate limits
- Make sure your X API credentials are correctly set in the `.env` file
- Invalid ticker symbols will show an error message
- Check that all dependencies are installed correctly

## Technical Details

- Stock data: yfinance
- Sentiment analysis: DistilBERT (Hugging Face Transformers)
- X API: tweepy
- Frontend: Streamlit
- Visualization: Plotly Express
- Data handling: pandas
- State management: Streamlit session state
- Caching: Local file system

## Performance Notes

- The app uses smart caching to minimize API calls
- Data is cached per ticker
- Sentiment analysis is performed only when new data is fetched
- Real-time price updates for current trading day

## License

MIT License - feel free to use this project for your own purposes.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## Future Enhancements

- Support for multiple stock comparison
- Historical sentiment analysis
- Advanced technical indicators
- Custom time range selection
- Export data functionality
- Additional social media sources
