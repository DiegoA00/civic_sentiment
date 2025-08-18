import requests
from bs4 import BeautifulSoup
import urllib3
from typing import List, Optional

from ..shared.interfaces import TitleScraper
from ...models.shared import Title, ScraperConfig
from .url_builder import ElComercioUrlBuilder

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ElComercioTitleScraper(TitleScraper):
    def __init__(self, config: ScraperConfig):
        self.config = config
    
    def extract_titles(self, url: str) -> List[Title]:
        response = self._fetch_page(url)
        if not response:
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        return self._extract_titles_from_soup(soup)
    
    def search_titles(self, search_term: str) -> List[Title]:
        search_url = ElComercioUrlBuilder.build_search_url(search_term)
        response = self._fetch_page(search_url)
        if not response:
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        return self._extract_search_results_from_soup(soup)
    
    def _fetch_page(self, url: str) -> Optional[requests.Response]:
        try:
            response = requests.get(
                url,
                headers=self.config.headers,
                verify=self.config.verify_ssl,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException:
            return None
    
    def _extract_titles_from_soup(self, soup: BeautifulSoup) -> List[Title]:
        title_elements = soup.find_all('h3')
        titles = []
        
        for position, element in enumerate(title_elements, 1):
            title_text = element.text.strip()
            if title_text:
                titles.append(Title(text=title_text, position=position))
        
        return titles
    
    def _extract_search_results_from_soup(self, soup: BeautifulSoup) -> List[Title]:
        search_result_selectors = [
            'h2.entry-title',
            'h3.entry-title', 
            '.search-result h2',
            '.search-result h3',
            'article h2',
            'article h3'
        ]
        
        titles = []
        position = 1
        
        for selector in search_result_selectors:
            elements = soup.select(selector)
            for element in elements:
                title_text = element.text.strip()
                if title_text and not self._is_duplicate_title(titles, title_text):
                    titles.append(Title(text=title_text, position=position))
                    position += 1
        
        if not titles:
            return self._extract_titles_from_soup(soup)
        
        return titles
    
    def _is_duplicate_title(self, existing_titles: List[Title], new_title: str) -> bool:
        return any(title.text == new_title for title in existing_titles)