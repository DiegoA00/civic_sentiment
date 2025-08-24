from app.models.shared import ScraperConfig
from app.services.lahora.title_scraper import LaHoraTitleScraper

if __name__ == "__main__":
    config = ScraperConfig.default_browser_config()
    scraper = LaHoraTitleScraper(config)
    search_term = "obras publicas"
    titles = scraper.search_titles(search_term)
    if not titles:
        print("No se encontraron títulos o hubo un error en la petición.")
    else:
        for title in titles:
            print(f"{title.position}. {title.text}")