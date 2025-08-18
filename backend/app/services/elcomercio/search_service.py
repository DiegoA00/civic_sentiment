from typing import List
from .title_scraper import ElComercioTitleScraper
from .url_builder import ElComercioUrlBuilder
from ..shared.sentiment_analyzer import TransformersSentimentAnalyzer
from ...models.shared import Title, TitlesResponse, ScraperConfig

class ElComercioSearchService:
    def __init__(self):
        self.scraper = ElComercioTitleScraper(ScraperConfig.default_browser_config())
        self.sentiment_analyzer = TransformersSentimentAnalyzer()
    
    def search_with_sentiment(self, search_term: str) -> TitlesResponse:
        titles = self.scraper.search_titles(search_term)
        analyzed_titles = self._analyze_titles_sentiment(titles)
        search_url = ElComercioUrlBuilder.build_search_url(search_term)
        
        return TitlesResponse(
            url=search_url,
            titles=analyzed_titles,
            total_count=len(analyzed_titles),
            source=f"El Comercio - Búsqueda: {search_term}"
        )
    
    def _analyze_titles_sentiment(self, titles: List[Title]) -> List[Title]:
        for title in titles:
            title.sentiment = self.sentiment_analyzer.analyze_sentiment(title.text)
        return titles