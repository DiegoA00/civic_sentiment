from abc import ABC, abstractmethod
from typing import List
from ...models.shared import Title, SentimentResult

class TitleScraper(ABC):
    @abstractmethod
    def extract_titles(self, url: str) -> List[Title]:
        pass

class SentimentAnalyzer(ABC):
    @abstractmethod
    def analyze_sentiment(self, text: str) -> SentimentResult:
        pass