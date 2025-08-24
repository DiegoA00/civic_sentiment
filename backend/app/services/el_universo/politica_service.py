import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from ...models.shared import Title, TitlesResponse, ScraperConfig
from ..shared.sentiment_analyzer import TransformersSentimentAnalyzer
from collections import Counter
import re

SPANISH_STOPWORDS = {
    "de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "las", "por", "un", "para", "con", "no", "una",
    "su", "al", "lo", "como", "más", "pero", "sus", "le", "ya", "o", "este", "sí", "porque", "esta", "entre", "cuando",
    "muy", "sin", "sobre", "también", "me", "hasta", "hay", "donde", "quien", "desde", "todo", "nos", "durante", "todos",
    "uno", "les", "ni", "contra", "otros", "ese", "eso", "ante", "ellos", "e", "esto", "mí", "antes", "algunos", "qué",
    "unos", "yo", "otro", "otras", "otra", "él", "tanto", "esa", "estos", "mucho", "quienes", "nada", "muchos", "cual",
    "poco", "ella", "estar", "estas", "algunas", "algo", "nosotros", "mi", "mis", "tú", "te", "ti", "tu", "tus", "ellas",
    "nosotras", "vosotros", "vosotras", "os", "mío", "mía", "míos", "mías", "tuyo", "tuya", "tuyos", "tuyas", "suyo",
    "suya", "suyos", "suyas", "nuestro", "nuestra", "nuestros", "nuestras", "vuestro", "vuestra", "vuestros", "vuestras",
    "esos", "esas", "estoy", "estás", "está", "estamos", "estáis", "están", "esté", "estés", "estemos", "estéis", "estén",
    "estaré", "estarás", "estará", "estaremos", "estaréis", "estarán", "estaría", "estarías", "estaríamos", "estaríais",
    "estarían", "estaba", "estabas", "estábamos", "estabais", "estaban", "estuve", "estuviste", "estuvo", "estuvimos",
    "estuvisteis", "estuvieron", "estuviera", "estuvieras", "estuviéramos", "estuvierais", "estuvieran", "estuviese",
    "estuvieses", "estuviésemos", "estuvieseis", "estuviesen", "estando", "estado", "estada", "estados", "estadas",
    "estad"
}

class ElUniversoTecnologiaService:
    def __init__(self):
        self.config = ScraperConfig.default_browser_config()
        self.session = requests.Session()
        self.session.headers.update(self.config.headers)
        self.sentiment_analyzer = TransformersSentimentAnalyzer()

    def get_titles_and_contents(self, num_pages: int) -> List[Dict]:
        results = []
        for page in range(1, num_pages + 1):
            url = f"https://www.eluniverso.com/larevista/tecnologia/"
            response = self._fetch_page(url)
            if not response:
                continue
            soup = BeautifulSoup(response.text, 'html.parser')
            """
            h2_elements = soup.find_all('h2') #, class_='styles_articule__r7Hpg')
            for h2 in h2_elements:
                a_tag = h2.find('a', class_='styles_linkStyled__pYJA9')
                if a_tag and a_tag.text.strip() and a_tag.has_attr('href'):
                    title_text = a_tag.text.strip()
                    href = a_tag['href']
                    content_text = self._fetch_content(href)
                    results.append({
                        "title": title_text,
                        "content": "" #content_text
                    })
            """
            headlines = soup.find_all('h2')

            if headlines:
                cleaned_headlines = [
                h.get_text(strip=True)
                for h in headlines
                if h.get_text(strip=True)
            ]
            
            for h2 in cleaned_headlines:
                results.append({
                    "title": h2, #title_text,
                    "content": "" #content_text
                })
            
        return results

    def _fetch_page(self, url: str):
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

    def _fetch_content(self, url: str) -> str:
        if not url.startswith("http"):
            url = f"https://www.eluniverso.com/{url}"
        response = self._fetch_page(url)
        if not response:
            return ""
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find('div', class_='styles_contentNews__pC_T6')
        if not content_div:
            return ""
        paragraphs = content_div.find_all('p')
        filtered_paragraphs = [
            p.get_text(strip=True)
            for p in paragraphs
            if p.get_text(strip=True) and "Te puede interesar:" not in p.get_text(strip=True)
        ]
        return "\n".join(filtered_paragraphs)

    def analyze_titles(self, num_pages: int):
        data = self.get_titles_and_contents(num_pages)
        titles = [Title(text=item["title"], position=i+1) for i, item in enumerate(data)]
        for title in titles:
            title.sentiment = self.sentiment_analyzer.analyze_sentiment(title.text)
        return titles

    def analyze_contents(self, num_pages: int):
        data = self.get_titles_and_contents(num_pages)
        contents = []
        for i, item in enumerate(data):
            content = item["content"]
            if content:
                words = content.split()
                chunk_size = 450
                fragments = [
                    " ".join(words[start:start+chunk_size])
                    for start in range(0, len(words), chunk_size)
                ]
                sentiments = [
                    self.sentiment_analyzer.analyze_sentiment(fragment)
                    for fragment in fragments
                ]
                if sentiments:
                    from collections import Counter
                    most_common = Counter([s.label.value for s in sentiments]).most_common(1)[0][0]
                    sentiment = next(s for s in sentiments if s.label.value == most_common)
                else:
                    sentiment = None
            else:
                sentiment = None
            contents.append({
                "position": i+1,
                "content": content,
                "sentiment": sentiment
            })
        return contents

    def keywords_by_sentiment(self, num_pages: int):
        titles = self.analyze_titles(num_pages)
        positive_words = []
        negative_words = []
        for title in titles:
            words = re.findall(r'\w+', title.text.lower())
            filtered_words = [w for w in words if w not in SPANISH_STOPWORDS]
            if title.sentiment and title.sentiment.label.value == "POSITIVE":
                positive_words.extend(filtered_words)
            elif title.sentiment and title.sentiment.label.value == "NEGATIVE":
                negative_words.extend(filtered_words)
        return {
            "positive": Counter(positive_words).most_common(20),
            "negative": Counter(negative_words).most_common(20)
        }