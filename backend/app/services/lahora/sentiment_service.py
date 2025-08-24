from .title_scraper import LaHoraTitleScraper
from ..shared.sentiment_analyzer import TransformersSentimentAnalyzer
from ...models.shared import TitlesResponse, ScraperConfig

class LaHoraSentimentService:
    def __init__(self):
        self.scraper = LaHoraTitleScraper(ScraperConfig.default_browser_config())
        self.sentiment_analyzer = TransformersSentimentAnalyzer()
    
    def get_titles_with_sentiment(self, search_term: str) -> TitlesResponse:
        titles = self.scraper.search_titles(search_term)
        for title in titles:
            title.sentiment = self.sentiment_analyzer.analyze_sentiment(title.text)
        return TitlesResponse(
            url=f"https://www.lahora.com.ec/buscar?query={search_term.replace(' ', '+')}",
            titles=titles,
            total_count=len(titles),
            source="La Hora"
        )