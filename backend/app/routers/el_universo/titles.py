from fastapi import APIRouter, Query, HTTPException
from ...services.lahora.title_service import LaHoraTitleService

router = APIRouter(prefix="/lahora", tags=["La Hora"])

@router.get("/titles")
async def get_titles(q: str = Query(..., description="Término de búsqueda en La Hora", min_length=1)):
    service = LaHoraTitleService()
    result = service.get_titles(q)
    if not result.success:
        raise HTTPException(status_code=404, detail="No titles found")
    return {
        "source": result.source,
        "url": result.url,
        "total_titles": result.total_count,
        "titles": [{"position": title.position, "text": title.text} for title in result.titles]
    }