from fastapi import APIRouter, HTTPException
from typing import List
from ...services.primicias.title_service import PrimiciasService
from ...models.shared.title import TitlesResponse

router = APIRouter(prefix="/primicias", tags=["Primicias"])
primicias_service = PrimiciasService()


@router.get("/economia/titles", response_model=TitlesResponse)
async def get_economia_titles():
    """Get economics section titles with sentiment analysis"""
    try:
        return primicias_service.get_economia_titles()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/economia/analysis")
async def get_economia_detailed_analysis():
    """Get detailed economics analysis with titles, quotes and sentiment"""
    try:
        return primicias_service.get_economia_detailed_analysis()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
