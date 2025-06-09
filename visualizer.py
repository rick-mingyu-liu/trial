import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

# Ensure output folder exists
OUTPUT_DIR = "images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_scores(csv_file="sentiment_scores.csv"):
    try:
        return pd.read_csv(csv_file)
    except Exception as e:
        print(f"[ERROR] Failed to load CSV: {e}")
        return pd.DataFrame()

def plot_histogram(df, bins=10, output_path="images/sentiment_histogram.png"):
    if df.empty:
        print("[WARNING] DataFrame is empty.")
        return

    plt.figure(figsize=(8, 5))
    plt.hist(df["compound"], bins=bins, edgecolor='black', alpha=0.7)
    plt.title("Sentiment Distribution (Ethereum ETF Headlines)")
    plt.xlabel("Compound Sentiment Score")
    plt.ylabel("Number of Headlines")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"[INFO] Histogram saved to {output_path}")
    plt.close()

def generate_wordcloud(df, filter_fn, output_path, title="Word Cloud"):
    filtered = df[df.apply(filter_fn, axis=1)]

    if filtered.empty:
        print(f"[WARNING] No data found for {title}.")
        return

    text = " ".join(filtered["headline"].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"[INFO] {title} saved to {output_path}")
    plt.close()

if __name__ == "__main__":
    df = load_scores()

    plot_histogram(df)

    generate_wordcloud(
        df,
        filter_fn=lambda row: row["compound"] >= 0.05,
        output_path="images/positive_wordcloud.png",
        title="Positive Headlines Word Cloud"
    )

    generate_wordcloud(
        df,
        filter_fn=lambda row: row["compound"] <= -0.05,
        output_path="images/negative_wordcloud.png",
        title="Negative Headlines Word Cloud"
    )

    generate_wordcloud(
        df,
        filter_fn=lambda row: -0.05 < row["compound"] < 0.05,
        output_path="images/neutral_wordcloud.png",
        title="Neutral Headlines Word Cloud"
    )
