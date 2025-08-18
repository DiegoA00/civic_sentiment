from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class SentimentLabel(Enum):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"

@dataclass
class SentimentResult:
    label: SentimentLabel
    score: float

@dataclass
class Title:
    text: str
    position: int
    sentiment: Optional[SentimentResult] = None

@dataclass
class TitlesResponse:
    url: str
    titles: List[Title]
    total_count: int
    source: str
    
    @property
    def success(self) -> bool:
        return self.total_count > 0
    
    @property
    def positive_sentiment_count(self) -> int:
        return len([t for t in self.titles if t.sentiment and t.sentiment.label == SentimentLabel.POSITIVE])
    
    @property
    def negative_sentiment_count(self) -> int:
        return len([t for t in self.titles if t.sentiment and t.sentiment.label == SentimentLabel.NEGATIVE])
    
    @property
    def positive_sentiment_percentage(self) -> float:
        if self.total_count == 0:
            return 0.0
        return (self.positive_sentiment_count / self.total_count) * 100