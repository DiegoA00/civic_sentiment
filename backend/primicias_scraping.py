import requests
from bs4 import BeautifulSoup
from transformers import pipeline

home_url = "https://www.primicias.ec"
pagina = 1
resultado = []
sentiment_pipeline = pipeline('sentiment-analysis')

while True:
    responseObras = requests.get(f"{home_url}/buscador/?q=Obras&page={pagina}")
    content = responseObras.content
    soup = BeautifulSoup(content, "html.parser")
    if not soup.find("li", class_="active c-pagination__page"):
        break
    articulos = soup.find_all("article", class_="c-article")
    for articulo in articulos:
        tag = articulo.find("h2", class_="c-article__title")
        link = tag.find("a")["href"]
        resultado.append({
            "titulo": tag.text.strip(),
            "enlace": f"{home_url}{link}",
            "citas": [],
            "emociones": []
        })
    print(f"Página {pagina} procesada.")
    pagina += 1

for i in range(len(resultado)):
    responseArticulo = requests.get(resultado[i]["enlace"])
    soup = BeautifulSoup(responseArticulo.content, "html.parser")
    # Aquí puedes extraer la información que necesites del artículo
    print(f"Artículo {i} procesado.")
    contenido = soup.find_all("p", class_="c-text")
    citas = []
    emociones = []
    for parrafo in contenido:
        texto = parrafo.text
        if '\"' in texto:
            citas.append(texto)
            emociones.append(sentiment_pipeline(texto))
    resultado[i]["citas"] = citas
    resultado[i]["emociones"] = emociones

for item in resultado:
    print(f"Artículo: {item['titulo']}")
    print(f"Enlace: {item['enlace']}")
    print("Citas:")
    for cita in item["citas"]:
        print(f" - {cita}")
    print("Emociones:")
    for emocion in item["emociones"]:
        print(f" - {emocion}")
    print("-" * 50)
