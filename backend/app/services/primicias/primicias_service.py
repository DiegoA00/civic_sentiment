import requests
from bs4 import BeautifulSoup
from typing import List
from ...models.shared.title import Title
from ..shared.sentiment_analyzer import TransformersSentimentAnalyzer


class PrimiciasScraper:
    def __init__(self):
        self.base_url = "https://www.primicias.ec"
        self.economia_section = "economia"
        self.max_pages = 3  # Máximo número de páginas a revisar
        self.sentiment_analyzer = TransformersSentimentAnalyzer()
    
    def get_economia_articles_with_sentiment(self) -> List[dict]:
        """Get economics articles with titles and content sentiment analysis"""
        pagina = 1
        resultado = []
        
        while pagina <= self.max_pages:
            try:
                url = f"{self.base_url}/{self.economia_section}/{pagina}/"
                response = requests.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, "html.parser")
                
                articulos = soup.find_all("article", class_="c-article")
                if not articulos:
                    print(f"No se encontraron artículos en página {pagina}. Fin del scraping.")
                    break
                
                # Process all articles on the page
                for articulo in articulos:
                    tag = articulo.find("h2", class_="c-article__title")
                    if tag:
                        title_text = tag.text.strip()
                        link = tag.find("a")["href"]
                        
                        # Analyze title sentiment
                        title_sentiment = self.sentiment_analyzer.analyze_sentiment(title_text)
                        
                        resultado.append({
                            "titulo": title_text,
                            "enlace": f"{self.base_url}{link}",
                            "titulo_sentimiento": {
                                "label": title_sentiment.label.value,
                                "score": title_sentiment.score
                            },
                            "citas": [],
                            "emociones": [],
                            "pagina": pagina
                        })
                
                print(f"Página {pagina} procesada - {len(articulos)} artículos de economía encontrados")
                pagina += 1
                
            except Exception as e:
                print(f"Error en página {pagina}: {e}")
                break
        
        # Process each article to extract quotes and analyze content
        for i, item in enumerate(resultado):
            try:
                response = requests.get(item["enlace"])
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, "html.parser")
                contenido = soup.find_all("p", class_="c-text")
                
                citas = []
                emociones = []
                
                for parrafo in contenido:
                    texto = parrafo.text.strip()
                    if texto and '\"' in texto:
                        citas.append(texto)
                        sentiment_result = self.sentiment_analyzer.analyze_sentiment(texto)
                        emociones.append({
                            "label": sentiment_result.label.value,
                            "score": sentiment_result.score
                        })
                
                resultado[i]["citas"] = citas
                resultado[i]["emociones"] = emociones
                
                print(f"Artículo {i+1}/{len(resultado)} procesado - {len(citas)} citas encontradas.")
                
            except Exception as e:
                print(f"Error procesando artículo {i}: {e}")
                continue
        
        return resultado
    
    def get_economia_titles_with_sentiment(self) -> List[Title]:
        """Get economics article titles with sentiment analysis only"""
        pagina = 1
        titles = []
        
        while pagina <= self.max_pages:
            try:
                url = f"{self.base_url}/{self.economia_section}/{pagina}/"
                response = requests.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, "html.parser")
                
                articulos = soup.find_all("article", class_="c-article")
                if not articulos:
                    print(f"No se encontraron artículos en página {pagina}. Fin del scraping.")
                    break
                
                # Process all articles on the page
                for articulo in articulos:
                    tag = articulo.find("h2", class_="c-article__title")
                    if tag:
                        title_text = tag.text.strip()
                        sentiment = self.sentiment_analyzer.analyze_sentiment(title_text)
                        titles.append(Title(
                            text=title_text,
                            position=len(titles),
                            sentiment=sentiment
                        ))
                
                print(f"Página {pagina} procesada - {len(articulos)} títulos de economía analizados")
                pagina += 1
                
            except Exception as e:
                print(f"Error en página {pagina}: {e}")
                break
        
        return titles
