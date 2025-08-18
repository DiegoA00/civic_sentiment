from transformers import pipeline
from .interfaces import SentimentAnalyzer
from ...models.shared import SentimentResult, SentimentLabel

class TransformersSentimentAnalyzer(SentimentAnalyzer):
    def __init__(self):
        self.sentiment_pipeline = pipeline('sentiment-analysis')
    
    def analyze_sentiment(self, text: str) -> SentimentResult:
        try:
            result = self.sentiment_pipeline(text)[0]
            label = SentimentLabel.POSITIVE if result['label'] == 'POSITIVE' else SentimentLabel.NEGATIVE
            return SentimentResult(label=label, score=result['score'])
        except Exception:
            return SentimentResult(label=SentimentLabel.NEGATIVE, score=0.0)