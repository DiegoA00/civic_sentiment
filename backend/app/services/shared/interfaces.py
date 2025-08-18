from abc import ABC, abstractmethod
from typing import List
from ...models.shared import Title, SentimentResult

class TitleScraper(ABC):
    @abstractmethod
    def extract_titles(self, url: str) -> List[Title]:
        pass
    
    @abstractmethod
    def search_titles(self, search_term: str) -> List[Title]:
        pass

class SentimentAnalyzer(ABC):
    @abstractmethod
    def analyze_sentiment(self, text: str) -> SentimentResult:
        pass