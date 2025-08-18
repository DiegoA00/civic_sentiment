from .titles import router as titles_router
from .sentiment import router as sentiment_router
from .search import router as search_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(titles_router)
router.include_router(sentiment_router)
router.include_router(search_router)

__all__ = ['router']