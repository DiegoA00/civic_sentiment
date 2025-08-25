from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import news
from app.routers.elcomercio import router as elcomercio_router
from app.routers.primicias.primicias_router import router as primicias_router
from app.routers.lahora import router as lahora_router
from app.routers.lahora.politica import router as lahora_politica_router
from app.routers.el_universo.politica import router as eluniverso_tecnologia_router
from .services.scraping_sentiment_analysis_eluniverso import analyzed_results

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
app.include_router(elcomercio_router)
app.include_router(primicias_router)
app.include_router(lahora_router)
app.include_router(lahora_politica_router)
app.include_router(eluniverso_tecnologia_router)

@app.get("/")
async def root():
    analyzed_headlines = analyzed_results("https://www.eluniverso.com/", "El Universo")
    return analyzed_headlines