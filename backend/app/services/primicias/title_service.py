from typing import List
from .primicias_service import PrimiciasScraper
from ...models.shared.title import TitlesResponse


class PrimiciasService:
    def __init__(self):
        self.scraper = PrimiciasScraper()
    
    def get_economia_titles(self) -> TitlesResponse:
        """Get economics section titles with sentiment analysis"""
        titles = self.scraper.get_economia_titles_with_sentiment()
        return TitlesResponse(
            url="https://www.primicias.ec/economia/",
            titles=titles,
            total_count=len(titles),
            source="Primicias - Economía"
        )
    
    def get_economia_detailed_analysis(self) -> List[dict]:
        """Get detailed economics analysis with titles, quotes and sentiment"""
        return self.scraper.get_economia_articles_with_sentiment()
