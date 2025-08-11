# Backend - Civic Sentiment

Este proyecto implementa un backend en Python utilizando FastAPI. El objetivo principal es realizar scrapping en tres plataformas (por definir) y exponer los datos obtenidos mediante endpoints para su consumo por el frontend.

## Estructura de carpetas

```
backend/
│   README.md
│   requirements.txt
│   .gitignore
└───app/
    │   main.py
    └───api/
    │   └───__init__.py
    └───scrapers/
    │   └───__init__.py
    └───models/
        └───__init__.py
```

- **app/main.py**: Punto de entrada de la aplicación FastAPI.
- **app/api/**: Endpoints y rutas de la API.
- **app/scrapers/**: Módulos para scrapping de cada plataforma.
- **app/models/**: Definición de modelos de datos y esquemas.

## Requisitos
- Python 3.8+
- FastAPI
- Librerías para scrapping: BeautifulSoup, requests.

## Instalación recomendada

1. Abre una terminal y navega a la carpeta `backend`:
    ```powershell
    cd c:\Users\Diego\Documents\proyectos_varios\Escolares\LP\civic_sentiment\backend
    ```

2. Crea un entorno virtual dentro de la carpeta `backend`:
    ```powershell
    python -m venv venv
    ```

3. Activa el entorno virtual:
    ```powershell
    .\venv\Scripts\Activate
    ```

4. Instala las dependencias desde el archivo `requirements.txt`:
    ```powershell
    pip install -r requirements.txt
    ```

## Ejecución

```powershell
fastapi dev ./app/main.py
```

## Notas
- Los scrapers deben implementarse en `app/scrapers/`.
- Los endpoints para obtener los datos estarán en `app/api/`.
- Los modelos de datos estarán en `app/models/`.

