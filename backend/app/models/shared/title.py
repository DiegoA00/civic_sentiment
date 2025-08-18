from dataclasses import dataclass
from typing import List

@dataclass
class Title:
    text: str
    position: int

@dataclass
class TitlesResponse:
    url: str
    titles: List[Title]
    total_count: int
    source: str
    
    @property
    def success(self) -> bool:
        return self.total_count > 0