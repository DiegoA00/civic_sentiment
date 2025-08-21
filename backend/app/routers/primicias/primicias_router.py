from fastapi import APIRouter, HTTPException
from typing import List
from ...services.primicias.title_service import PrimiciasService
from ...models.shared.title import TitlesResponse

router = APIRouter(prefix="/primicias", tags=["Primicias"])
primicias_service = PrimiciasService()


@router.get("/titles", response_model=TitlesResponse)
async def get_primicias_titles():
    """Get main page titles from Primicias"""
    try:
        return primicias_service.get_titles()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/{search_term}", response_model=TitlesResponse)
async def search_primicias(search_term: str):
    """Search articles by term in Primicias"""
    try:
        return primicias_service.search_by_term(search_term)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/{search_term}")
async def get_detailed_analysis(search_term: str):
    """Get detailed analysis with quotes and sentiment for a search term"""
    try:
        return primicias_service.get_detailed_analysis(search_term)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
