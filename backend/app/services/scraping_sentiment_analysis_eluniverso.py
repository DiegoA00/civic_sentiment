import os
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
# import tensorflow as tf

# # Suppress all TensorFlow logs
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
# tf.get_logger().setLevel('ERROR')

sentiment_pipeline = pipeline('sentiment-analysis') #, framework='tf')

def analyze_headline(headline):
    result = sentiment_pipeline(headline)[0]

    label = result['label']
    # score = result['score']
    return label

def scrape_website(url):

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        headlines = soup.find_all('h2')

        if headlines:
            cleaned_headlines = [
            h.get_text(strip=True)
            for h in headlines
            if h.get_text(strip=True)
        ]
            return cleaned_headlines
        
        else:
            print('Error, could not find headline')
            return None
        
    except requests.exceptions.RequestException as e:
        print(f'An error ocurred: {e}')
        return None
    
    except Exception as e:
        print(f'An unexpected error ocurred: {e}')
        return None
    
def analyzed_results(url: str, newspaper_name: str) -> list[dict]:
    """Return headlines with sentiment label and newspaper name."""
    headlines = scrape_website(url)
    results = []
    for hl in headlines:
        label = analyze_headline(hl)
        results.append({
            'headline': hl,
            'label': label,
            'newspaper': newspaper_name
        })
    return results

if __name__ == "__main__":
    url = 'https://www.eluniverso.com/'