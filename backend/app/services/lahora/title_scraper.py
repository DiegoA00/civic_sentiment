import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from ...models.shared import Title, ScraperConfig

class LaHoraTitleScraper:
    def __init__(self, config: ScraperConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(config.headers)
    
    def search_titles(self, search_term: str) -> List[Title]:
        url = f"https://www.lahora.com.ec/buscar?query={search_term.replace(' ', '+')}"
        response = self._fetch_page(url)
        if not response:
            return []
        soup = BeautifulSoup(response.text, 'html.parser')
        return self._extract_titles_from_soup(soup)
    
    def _fetch_page(self, url: str) -> Optional[requests.Response]:
        try:
            response = self.session.get(
                url,
                verify=self.config.verify_ssl,
                timeout=self.config.timeout,
                allow_redirects=True
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException:
            return None
    
    def _extract_titles_from_soup(self, soup: BeautifulSoup) -> List[Title]:
        titles = []
        h2_elements = soup.find_all('h2', class_='styles_articule__r7Hpg')
        for position, h2 in enumerate(h2_elements, 1):
            link = h2.find(class_='styles_linkStyled__pYJA9')
            if link and link.text.strip():
                titles.append(Title(text=link.text.strip(), position=position))
        return titles  # Asegura que siempre retorna una lista