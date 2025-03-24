import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import re
import os
from gtts import gTTS
from googletrans import Translator

# News Scraping Function
def scrape_news(company_name):
    search_url = f"https://www.bing.com/news/search?q={company_name}&FORM=HDRSC6"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("a", {"class": "title"}, limit=10)  # Extract 10 news articles
    
    news_data = []
    for article in articles:
        title = article.text
        link = article["href"]
        summary = fetch_article_summary(link)  
        
        news_data.append({"title": title, "summary": summary, "url": link})

    return news_data

# Fetch Full Article Content (if needed)
def fetch_article_summary(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        content = " ".join([p.text for p in paragraphs[:5]])  # Extract first 5 paragraphs
        return re.sub(r"\s+", " ", content.strip())  
    except:
        return "Summary unavailable."

# Sentiment Analysis
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Comparative Analysis
def compare_sentiments(news_list):
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for news in news_list:
        sentiment_counts[news["sentiment"]] += 1
    return sentiment_counts

# Convert Text to Hindi Speech (Updated with Translation)
def text_to_speech_hindi(text, filename="output.mp3"):
    translator = Translator()
    
    try:
        translated_text = translator.translate(text, src="en", dest="hi").text
        print("✅ Translated Hindi Text:", translated_text)  # Debugging output

        if translated_text == text:  # If translation fails
            translated_text = "अनुवाद विफल रहा। कृपया पुनः प्रयास करें।"

        tts = gTTS(translated_text, lang="hi")  # Use the translated Hindi text
        tts.save(filename)
        return filename

    except Exception as e:
        print("❌ Translation Error:", e)
        return "Translation failed."
