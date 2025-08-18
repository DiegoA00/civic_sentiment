from abc import ABC, abstractmethod
from typing import List
from ...models.shared import Title

class TitleScraper(ABC):
    @abstractmethod
    def extract_titles(self, url: str) -> List[Title]:
        pass