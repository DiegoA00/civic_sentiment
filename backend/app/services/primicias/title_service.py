from typing import List
from .primicias_service import PrimiciasScraper
from ...models.shared.title import Title, TitlesResponse


class PrimiciasService:
    def __init__(self):
        self.scraper = PrimiciasScraper()
    
    def get_titles(self) -> TitlesResponse:
        """Get main page titles"""
        titles = self.scraper.extract_titles()
        return TitlesResponse(
            url="https://www.primicias.ec",
            titles=titles,
            total_count=len(titles),
            source="Primicias"
        )
    
    def search_by_term(self, search_term: str) -> TitlesResponse:
        """Search articles by term"""
        titles = self.scraper.search_titles(search_term)
        return TitlesResponse(
            url=f"https://www.primicias.ec/buscador/?q={search_term}",
            titles=titles,
            total_count=len(titles),
            source="Primicias"
        )
    
    def get_detailed_analysis(self, search_term: str) -> List[dict]:
        """Get detailed analysis with quotes and sentiment"""
        return self.scraper.get_article_quotes_with_sentiment(search_term)
