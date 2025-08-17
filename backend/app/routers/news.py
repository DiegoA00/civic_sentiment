from fastapi import APIRouter, HTTPException, Query
from app.services.scraper import scrape_headlines

router = APIRouter(prefix="/news", tags=["News"])

@router.get("/scrape")
async def get_news(url: str = Query(..., description="URL of the newspaper")):
    try:
        data = scrape_headlines(url)
        return {"headlines": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
