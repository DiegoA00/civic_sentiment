from .title_scraper import LaHoraTitleScraper
from ...models.shared import TitlesResponse, ScraperConfig

class LaHoraTitleService:
    def __init__(self):
        self.scraper = LaHoraTitleScraper(ScraperConfig.default_browser_config())
    
    def get_titles(self, search_term: str) -> TitlesResponse:
        titles = self.scraper.search_titles(search_term)
        return TitlesResponse(
            url=f"https://www.lahora.com.ec/buscar?query={search_term.replace(' ', '+')}",
            titles=titles,
            total_count=len(titles),
            source="La Hora"
        )