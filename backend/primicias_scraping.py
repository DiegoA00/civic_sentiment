import requests
from bs4 import BeautifulSoup

home_url = "https://www.primicias.ec"
pagina = 1
indice = []
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
        indice.append({
            "titulo": tag.text.strip(),
            "enlace": f"{home_url}{link}"
        })
    print(f"Página {pagina} procesada.")
    pagina += 1
print(indice)
