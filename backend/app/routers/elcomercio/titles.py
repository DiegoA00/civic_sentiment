from fastapi import APIRouter, Query, HTTPException
from ...services.elcomercio import ElComercioTitleService

router = APIRouter(prefix="/elcomercio", tags=["El Comercio"])

@router.get("/titles")
async def get_titles(url: str = Query("https://www.elcomercio.com/ultima-hora/", description="URL to scrape titles from")):
    service = ElComercioTitleService()
    result = service.get_titles(url)
    
    if not result.success:
        raise HTTPException(status_code=404, detail="No titles found")
    
    return {
        "source": result.source,
        "url": result.url,
        "total_titles": result.total_count,
        "titles": [{"position": title.position, "text": title.text} for title in result.titles]
    }