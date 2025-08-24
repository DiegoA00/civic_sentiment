from fastapi import APIRouter, Query, HTTPException
from ...services.lahora.sentiment_service import LaHoraSentimentService

router = APIRouter(prefix="/lahora", tags=["La Hora"])

@router.get("/sentiment")
async def analyze_titles_sentiment(q: str = Query(..., description="Término de búsqueda en La Hora", min_length=1)):
    service = LaHoraSentimentService()
    result = service.get_titles_with_sentiment(q)
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