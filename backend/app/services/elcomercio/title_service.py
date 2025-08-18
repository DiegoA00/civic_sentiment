from .title_scraper import ElComercioTitleScraper
from ...models.shared import TitlesResponse, ScraperConfig

class ElComercioTitleService:
    def __init__(self):
        self.scraper = ElComercioTitleScraper(ScraperConfig.default_browser_config())
    
    def get_titles(self, url: str = "https://www.elcomercio.com/ultima-hora/") -> TitlesResponse:
        titles = self.scraper.extract_titles(url)
        return TitlesResponse(
            url=url,
            titles=titles,
            total_count=len(titles),
            source="El Comercio"
        )