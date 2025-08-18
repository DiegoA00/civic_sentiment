from typing import List
from .title_scraper import ElComercioTitleScraper
from ..shared.sentiment_analyzer import TransformersSentimentAnalyzer
from ...models.shared import Title, TitlesResponse, ScraperConfig

class ElComercioSentimentService:
    def __init__(self):
        self.scraper = ElComercioTitleScraper(ScraperConfig.default_browser_config())
        self.sentiment_analyzer = TransformersSentimentAnalyzer()
    
    def get_titles_with_sentiment(self, url: str = "https://www.elcomercio.com/ultima-hora/") -> TitlesResponse:
        titles = self.scraper.extract_titles(url)
        analyzed_titles = self._analyze_titles_sentiment(titles)
        
        return TitlesResponse(
            url=url,
            titles=analyzed_titles,
            total_count=len(analyzed_titles),
            source="El Comercio"
        )
    
    def _analyze_titles_sentiment(self, titles: List[Title]) -> List[Title]:
        for title in titles:
            title.sentiment = self.sentiment_analyzer.analyze_sentiment(title.text)
        return titles