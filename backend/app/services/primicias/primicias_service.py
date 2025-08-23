import requests
from bs4 import BeautifulSoup
from typing import List
from ...models.shared.title import Title
from ..shared.sentiment_analyzer import TransformersSentimentAnalyzer


class PrimiciasScraper:
    def __init__(self):
        self.base_url = "https://www.primicias.ec"
        self.sentiment_analyzer = TransformersSentimentAnalyzer()
    
    def _title_contains_search_term(self, title: str, search_term: str) -> bool:
        """Check if title contains search term (case insensitive)"""
        return search_term.lower() in title.lower()
    
    def search_titles(self, search_term: str) -> List[Title]:
        """Search articles by term and extract titles with sentiment analysis"""
        titles = []
        pagina = 1
        
        while True:
            try:
                url = f"{self.base_url}/buscador/?q={search_term}&page={pagina}"
                response = requests.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, "html.parser")
                
                # Check if there are more pages
                if not soup.find("li", class_="active c-pagination__page"):
                    break
                
                articulos = soup.find_all("article", class_="c-article")
                if not articulos:
                    break
                
                # Only analyze titles that contain the search term
                matching_articles = 0
                for articulo in articulos:
                    tag = articulo.find("h2", class_="c-article__title")
                    if tag:
                        title_text = tag.text.strip()
                        # Only analyze titles that match the search term
                        if self._title_contains_search_term(title_text, search_term):
                            sentiment = self.sentiment_analyzer.analyze_sentiment(
                                title_text
                            )
                            titles.append(Title(
                                text=title_text,
                                position=len(titles),
                                sentiment=sentiment
                            ))
                            matching_articles += 1
                
                print(f"Página {pagina} procesada - {matching_articles} de {len(articulos)} artículos coinciden con '{search_term}'")
                pagina += 1
                
            except Exception as e:
                print(f"Error en página {pagina}: {e}")
                break
        
        return titles
    
    def get_article_quotes_with_sentiment(self, search_term: str) -> List[dict]:
        """Get articles with quotes and sentiment analysis (original functionality)"""
        pagina = 1
        resultado = []
        
        while True:
            try:
                url = f"{self.base_url}/buscador/?q={search_term}&page={pagina}"
                response = requests.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, "html.parser")
                
                if not soup.find("li", class_="active c-pagination__page"):
                    break
                
                articulos = soup.find_all("article", class_="c-article")
                if not articulos:
                    break
                
                # Only process articles whose titles contain the search term
                matching_articles = 0
                for articulo in articulos:
                    tag = articulo.find("h2", class_="c-article__title")
                    if tag:
                        title_text = tag.text.strip()
                        # Only process articles that match the search term
                        if self._title_contains_search_term(title_text, search_term):
                            link = tag.find("a")["href"]
                            resultado.append({
                                "titulo": title_text,
                                "enlace": f"{self.base_url}{link}",
                                "citas": [],
                                "emociones": []
                            })
                            matching_articles += 1
                
                print(f"Página {pagina} procesada - {matching_articles} artículos coinciden con '{search_term}'.")
                pagina += 1
                
            except Exception as e:
                print(f"Error en página {pagina}: {e}")
                break
        
        # Process each article to extract quotes
        for i, item in enumerate(resultado):
            try:
                response = requests.get(item["enlace"])
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, "html.parser")
                contenido = soup.find_all("p", class_="c-text")
                
                citas = []
                emociones = []
                
                for parrafo in contenido:
                    texto = parrafo.text
                    if '\"' in texto:
                        citas.append(texto)
                        sentiment_result = self.sentiment_analyzer.analyze_sentiment(texto)
                        emociones.append({
                            "label": sentiment_result.label.value,
                            "score": sentiment_result.score
                        })
                
                resultado[i]["citas"] = citas
                resultado[i]["emociones"] = emociones
                
                print(f"Artículo {i+1}/{len(resultado)} procesado.")
                
            except Exception as e:
                print(f"Error procesando artículo {i}: {e}")
                continue
        
        return resultado
