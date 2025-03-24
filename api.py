from fastapi import FastAPI
from utils import scrape_news, analyze_sentiment, compare_sentiments, text_to_speech_hindi
import os

app = FastAPI()

@app.get("/news/{company}")
def get_news(company: str):
    news_articles = scrape_news(company)
    for news in news_articles:
        news["sentiment"] = analyze_sentiment(news["summary"])
    
    sentiment_summary = compare_sentiments(news_articles)
    
    return {"articles": news_articles, "sentiment_summary": sentiment_summary}

@app.get("/tts/")
def generate_tts(text: str):
    audio_file = text_to_speech_hindi(text)
    return {"audio_file": audio_file}
