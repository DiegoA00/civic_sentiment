from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import news
from .services.scraping_sentiment_analysis_eluniverso import scrape_website

app = FastAPI(title="News Sentiment API")

# Allow requests from Flutter frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(news.router)

@app.get("/")
async def root():
    messages = scrape_website("https://www.eluniverso.com/")

    cleaned_headlines = [
        h.get_text(strip=True)
        for h in messages
        if h.get_text(strip=True)
    ]

    return {"message": cleaned_headlines}
