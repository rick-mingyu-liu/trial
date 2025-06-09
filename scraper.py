from newsapi import NewsApiClient
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()
API_KEY = os.getenv("NEWSAPI_KEY")

# Ensure output folder exists
OUTPUT_DIR = "files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def scrape_ethereum_etf_headlines(api_key, num_articles=30, output_file="files/ethereum_etf_headlines.txt"):
    newsapi = NewsApiClient(api_key=api_key)

    try:
        result = newsapi.get_everything(
            q="Ethereum ETF",
            language="en",
            sort_by="publishedAt",
            page_size=min(num_articles, 100)
        )
    except Exception as e:
        print(f"[ERROR] API call failed: {e}")
        return []

    if not result['articles']:
        print("[WARNING] No headlines found.")
        return []

    headlines = [article['title'] for article in result['articles']]

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            for line in headlines:
                f.write(line + "\n")
        print(f"[INFO] Wrote {len(headlines)} headlines to {output_file}")
    except Exception as e:
        print(f"[ERROR] Could not write to file: {e}")

    return headlines

if __name__ == "__main__":
    headlines = scrape_ethereum_etf_headlines(API_KEY)
    print("\n=== Sample Headlines ===")
    for i, h in enumerate(headlines[:10], 1):
        print(f"{i}. {h}")
