import requests
from bs4 import BeautifulSoup
from gtts import gTTS
from textblob import TextBlob
import os

# Function to scrape news from Google News
def scrape_news(query: str):
    url = f"https://news.google.com/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return [{"error": "Failed to fetch news"}]

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []

    for item in soup.select("article"):
        title = item.get_text()
        link = item.find("a")["href"] if item.find("a") else "#"
        articles.append({"title": title, "url": f"https://news.google.com{link}"})

    return articles[:10]  # Return top 10 news articles

# Function for sentiment analysis
def analyze_sentiment(text: str):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    sentiment = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"
    return {"text": text, "sentiment": sentiment, "polarity": polarity}

# Function to convert text to Hindi speech
def text_to_speech_hindi(text: str):
    tts = gTTS(text, lang="hi")
    audio_path = "output.mp3"
    tts.save(audio_path)
    return audio_path
