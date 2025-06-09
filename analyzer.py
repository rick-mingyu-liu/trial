from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
import os

# Input/output file paths
INPUT_FILE = "files/ethereum_etf_headlines.txt"
OUTPUT_FILE = "files/sentiment_scores.csv"
os.makedirs("files", exist_ok=True)

def load_headlines(file_path=INPUT_FILE):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[ERROR] Failed to load headlines: {e}")
        return []

def analyze_sentiment(headlines):
    analyzer = SentimentIntensityAnalyzer()
    results = []

    for headline in headlines:
        score = analyzer.polarity_scores(headline)
        results.append({
            "headline": headline,
            "compound": score["compound"],
            "pos": score["pos"],
            "neu": score["neu"],
            "neg": score["neg"]
        })

    return results

def save_results(results, output_file=OUTPUT_FILE):
    try:
        with open(output_file, "w", encoding="utf-8", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["headline", "compound", "pos", "neu", "neg"])
            writer.writeheader()
            for row in results:
                writer.writerow(row)
        print(f"[INFO] Wrote sentiment scores to {output_file}")
    except Exception as e:
        print(f"[ERROR] Failed to write sentiment file: {e}")

if __name__ == "__main__":
    headlines = load_headlines()
    if not headlines:
        print("[WARNING] No headlines to analyze.")
    else:
        scores = analyze_sentiment(headlines)
        save_results(scores)

        avg_score = sum([s["compound"] for s in scores]) / len(scores)
        print(f"\n[INFO] Analyzed {len(scores)} headlines")
        print(f"[INFO] Average compound score: {avg_score:.3f}")
