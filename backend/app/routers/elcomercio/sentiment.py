from fastapi import APIRouter, Query, HTTPException
from ...services.elcomercio import ElComercioSentimentService

router = APIRouter(prefix="/elcomercio", tags=["El Comercio"])

@router.get("/sentiment")
async def analyze_titles_sentiment(url: str = Query("https://www.elcomercio.com/ultima-hora/", description="URL to scrape and analyze sentiment")):
    service = ElComercioSentimentService()
    result = service.get_titles_with_sentiment(url)
    
    if not result.success:
        raise HTTPException(status_code=404, detail="No titles found")
    
    return {
        "source": result.source,
        "url": result.url,
        "total_titles": result.total_count,
        "positive_sentiment_percentage": round(result.positive_sentiment_percentage, 2),
        "sentiment_summary": {
            "positive": result.positive_sentiment_count,
            "negative": result.negative_sentiment_count
        },
        "titles": [
            {
                "position": title.position,
                "text": title.text,
                "sentiment": {
                    "label": title.sentiment.label.value,
                    "score": round(title.sentiment.score, 3)
                } if title.sentiment else None
            }
            for title in result.titles
        ]
    }