import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import requests
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()
ETH_API_URL = st.secrets["COINGECKO_ETH_URL"]

# === Streamlit page setup ===
st.set_page_config(page_title="Ethereum ETF Sentiment Dashboard", layout="wide")

# === Load Sentiment Data ===
@st.cache_data
def load_data():
    return pd.read_csv("files/sentiment_scores.csv")

# === Get Live ETH Price ===
@st.cache_data(ttl=300)
def get_eth_price():
    try:
        res = requests.get(ETH_API_URL)
        data = res.json()
        return float(data["ethereum"]["usd"])
    except:
        return None

# === Main Dashboard ===
st.title("📈 Ethereum ETF Sentiment Dashboard")

eth_price = get_eth_price()
if eth_price:
    st.markdown(f"### 💰 Current ETH Price: **${eth_price:,.2f}**")
else:
    st.warning("Could not fetch Ethereum price from API.")

df = load_data()

# === Sidebar: Sentiment Filter ===
st.sidebar.title("🔍 Filter Sentiment")
sentiment = st.sidebar.radio("Select sentiment type:", ("All", "Positive", "Negative", "Neutral"))

if sentiment == "Positive":
    filtered = df[df["compound"] >= 0.05]
elif sentiment == "Negative":
    filtered = df[df["compound"] <= -0.05]
elif sentiment == "Neutral":
    filtered = df[(df["compound"] > -0.05) & (df["compound"] < 0.05)]
else:
    filtered = df

# === Headlines Table ===
st.subheader("📰 Headlines")
table_display = filtered[["headline", "compound"]].copy()
table_display.index = range(1, len(table_display) + 1)
st.dataframe(table_display, use_container_width=True)

# === Histogram ===
st.subheader("📊 Sentiment Score Distribution")
fig, ax = plt.subplots(figsize=(6, 4))
ax.hist(filtered["compound"], bins=10, color='skyblue', edgecolor='black')
ax.set_title("Compound Sentiment Histogram")
ax.set_xlabel("Sentiment Score")
ax.set_ylabel("Frequency")
st.pyplot(fig)

# === Word Cloud ===
st.subheader("☁️ Word Cloud of Headlines")
text = " ".join(filtered["headline"].dropna())
if text:
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    fig_wc, ax_wc = plt.subplots(figsize=(10, 4))
    ax_wc.imshow(wordcloud, interpolation="bilinear")
    ax_wc.axis("off")
    st.pyplot(fig_wc)
else:
    st.info("No headlines available to render a word cloud.")
