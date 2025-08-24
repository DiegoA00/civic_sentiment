from fastapi import APIRouter, Query, HTTPException
from ...services.lahora.politica_service import LaHoraPoliticaService

router = APIRouter(prefix="/lahora/politica", tags=["La Hora Política"])
service = LaHoraPoliticaService()

@router.get("/titles-sentiment")
async def titles_sentiment(num_pages: int = Query(1, ge=1, le=10)):
    titles = service.analyze_titles(num_pages)
    if not titles:
        raise HTTPException(status_code=404, detail="No titles found")
    positive = sum(1 for t in titles if t.sentiment and t.sentiment.label.value == "POSITIVE")
    negative = sum(1 for t in titles if t.sentiment and t.sentiment.label.value == "NEGATIVE")
    return {
        "total": len(titles),
        "positive": positive,
        "negative": negative,
        "percentage_positive": round(positive / len(titles) * 100, 2) if titles else 0,
        "percentage_negative": round(negative / len(titles) * 100, 2) if titles else 0,
        "titles": [{"position": t.position, "text": t.text, "sentiment": t.sentiment.label.value if t.sentiment else None} for t in titles]
    }

@router.get("/content-sentiment")
async def content_sentiment(num_pages: int = Query(1, ge=1, le=10)):
    contents = service.analyze_contents(num_pages)
    filtered = [c for c in contents if c["sentiment"]]
    positive = sum(1 for c in filtered if c["sentiment"].label.value == "POSITIVE")
    negative = sum(1 for c in filtered if c["sentiment"].label.value == "NEGATIVE")
    return {
        "total": len(filtered),
        "positive": positive,
        "negative": negative,
        "percentage_positive": round(positive / len(filtered) * 100, 2) if filtered else 0,
        "percentage_negative": round(negative / len(filtered) * 100, 2) if filtered else 0,
        "contents": [
            {
                "position": c["position"],
                "sentiment": c["sentiment"].label.value if c["sentiment"] else None,
                "content": c["content"][:200]
            }
            for c in filtered
        ]
    }

@router.get("/keywords")
async def keywords(num_pages: int = Query(1, ge=1, le=10)):
    result = service.keywords_by_sentiment(num_pages)
    return result