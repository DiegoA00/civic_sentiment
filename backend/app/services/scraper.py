import requests
from bs4 import BeautifulSoup
from transformers import pipeline

# Sentiment analyzer
sentiment_pipeline = pipeline('sentiment-analysis')

def scrape_headlines(url: str):
    """Scrape headlines from a newspaper URL and analyze sentiment."""
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines_elements = soup.find_all('h2')  # or other tags depending on the site

    results = []
    for elem in headlines_elements:
        title = elem.text.strip()
        if title:
            sentiment = sentiment_pipeline(title)[0]['label']
            results.append({
                'title': title,
                'source': url,
                'sentiment': sentiment
            })
    return results
