from fastapi import APIRouter, Query, HTTPException
from ...services.elcomercio import ElComercioSearchService

router = APIRouter(prefix="/elcomercio", tags=["El Comercio"])

@router.get("/search")
async def search_titles_with_sentiment(
    q: str = Query(..., description="Search term to look for in El Comercio", min_length=1)
):
    service = ElComercioSearchService()
    result = service.search_with_sentiment(q)
    
    if not result.success:
        raise HTTPException(status_code=404, detail=f"No results found for search term: {q}")
    
    return {
        "search_term": q,
        "source": result.source,
        "url": result.url,
        "total_results": result.total_count,
        "positive_sentiment_percentage": round(result.positive_sentiment_percentage, 2),
        "sentiment_summary": {
            "positive": result.positive_sentiment_count,
            "negative": result.negative_sentiment_count
        },
        "results": [
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