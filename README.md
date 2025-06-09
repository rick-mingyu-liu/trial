# Ethereum ETF Sentiment Dashboard

A lightweight NLP dashboard for analyzing public sentiment around Ethereum ETF news headlines. Built with **Streamlit**, the dashboard lets you:

- Scrape and analyze news headlines  
- Visualize sentiment distribution  
- Generate a word cloud of popular keywords  
- Fetch real-time Ethereum price from CoinGecko  
- Filter headlines by sentiment: Positive, Negative, Neutral, or All  

---

## Project Structure
- requirements.txt - Python dependencies
- app.py - Streamlit dashboard
- analyzer.py - VADER sentiment scoring
- scraper.py - Headline scraper using NewsAPI
- visualizer.py - Generates and saves sentiment histogram + word clouds  

## Tech Stack
- Python 3
- Streamlit
- VADER Sentiment
- NewsAPI.org (for scraping)
- CoinGecko API (for live ETH price)
- Matplotlib 
- WordCloud
- Pandas

## How to Run
1. **Install requirements**:
```bash
pip install -r requirements.txt
```

2. Set up .env file:
```bash
NEWSAPI_KEY=your key
COINGECKO_ETH_URL=https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd
```

3. **Run Streamlit app**:
```bash
streamlit run app.py
```