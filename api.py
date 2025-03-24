from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from utils import scrape_news, analyze_sentiment, text_to_speech_hindi

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains (Change for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "FastAPI backend is running!"}

@app.get("/news/{query}")
def get_news(query: str):
    news = scrape_news(query)
    if not news:
        raise HTTPException(status_code=404, detail="No news found")
    return {"query": query, "articles": news}

@app.get("/sentiment/{query}")
def get_sentiment(query: str):
    news = scrape_news(query)
    if not news:
        raise HTTPException(status_code=404, detail="No news found")

    sentiment_results = [{"title": article["title"], "sentiment": analyze_sentiment(article["title"])} for article in news]
    return {"query": query, "sentiments": sentiment_results}

@app.get("/tts/")
def get_tts(text: str):
    try:
        audio_path = text_to_speech_hindi(text)
        return {"message": "TTS generated successfully", "audio_path": audio_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
