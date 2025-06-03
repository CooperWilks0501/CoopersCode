# stock_sentiment_analyzer.py

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

# ------------------------------
# Fetch historical stock data
# ------------------------------
def fetch_stock_data(ticker, period="6mo", interval="1d"):
    print(f"Fetching stock data for {ticker}...")
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, interval=interval)
    return hist

# ------------------------------
# Plot stock closing price
# ------------------------------
def plot_stock_price(df, ticker):
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df['Close'], label=f"{ticker} Close Price", color="blue")
    plt.title(f"{ticker} Stock Price Over Time")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# ------------------------------
# Scrape financial news headlines
# ------------------------------
def fetch_yahoo_news(ticker):
    print(f"Scraping Yahoo Finance headlines for {ticker}...")
    url = f"https://finance.yahoo.com/quote/{ticker}?p={ticker}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    headlines = []
    for item in soup.select("li.js-stream-content span[class='']"):
        text = item.get_text(strip=True)
        if text:
            headlines.append(text)
    return headlines

# ------------------------------
# Perform sentiment analysis
# ------------------------------
def analyze_sentiment(headlines):
    print("Analyzing sentiment...")
    sentiments = []
    for headline in headlines:
        blob = TextBlob(headline)
        polarity = blob.sentiment.polarity
        sentiments.append({"headline": headline, "sentiment": polarity})
    return pd.DataFrame(sentiments)

# ------------------------------
# Plot sentiment distribution
# ------------------------------
def plot_sentiment_distribution(sentiment_df, ticker):
    plt.figure(figsize=(10, 5))
    sns.histplot(sentiment_df['sentiment'], bins=20, kde=True, color="green")
    plt.title(f"Sentiment Distribution for {ticker} News Headlines")
    plt.xlabel("Sentiment Polarity")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# ------------------------------
# Main function
# ------------------------------
def main():
    ticker = input("Enter stock ticker (e.g., AAPL, TSLA): ").upper()
    
    # Step 1: Fetch stock data and plot
    df = fetch_stock_data(ticker)
    if df.empty:
        print("No stock data found. Please check the ticker.")
        return
    plot_stock_price(df, ticker)

    # Step 2: Fetch news and analyze sentiment
    headlines = fetch_yahoo_news(ticker)
    if not headlines:
        print("No headlines found.")
        return
    sentiment_df = analyze_sentiment(headlines)
    print("\nSample Headlines with Sentiment Scores:")
    print(sentiment_df.head())

    # Step 3: Plot sentiment distribution
    plot_sentiment_distribution(sentiment_df, ticker)

if __name__ == "__main__":
    main()
