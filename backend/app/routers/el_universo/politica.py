from fastapi import APIRouter, Query, HTTPException
from ...services.el_universo.politica_service import ElUniversoTecnologiaService
from ...models.shared.title import TitlesResponse

router = APIRouter(prefix="/eluniverso/tecnologia", tags=["El Universo Tecnologia"])
service = ElUniversoTecnologiaService()

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

@router.get("/economia/analysis")
async def get_economia_detailed_analysis():
    """Get detailed economics analysis with titles, quotes and sentiment"""
    try:
        return service.get_economia_detailed_analysis()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/economia/titles", response_model=TitlesResponse)
async def get_economia_titles():
    """Get economics section titles with sentiment analysis"""
    try:
        return service.get_economia_titles()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))