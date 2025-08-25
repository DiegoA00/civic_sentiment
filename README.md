# CivicSentiment

Este proyecto es una plataforma para el análisis de opinión ciudadana, que consta de un *backend* en Python para el *scraping* y análisis de datos, y un *frontend* en Flutter para la visualización de los resultados.

## 1. Instalación y ejecución del Backend

Para que el *backend* funcione correctamente, necesitas tener instalado Python 3.9 o una versión superior (hasta 3.12).

### Para Windows

1. Abre una terminal y navega a la carpeta `backend`:
   
   ```powershell
   cd civic_sentiment/backend
   ```
3. Crea un entorno virtual dentro de la carpeta backend:
   ```powershell
   python -m venv venv
   ```
3. Activa el entorno virtual:
   ```powershell
   .\venv\Scripts\Activate
   ```
4. Instala las dependencias desde el archivo requirements.txt:
   ```powershell
   pip install -r requirements.txt
   ```
5. Inicia el servidor del backend:
   ```powershell
   fastapi dev ./app/main.py
   ```

### Para macOS y Linux
1.  Abre una terminal y navega a la carpeta backend:
   ```bash
   cd civic_sentiment/backend
   ```
2. Crea un entorno virtual dentro de la carpeta backend:
   ```bash
   python3 -m venv venv
   ```

3. Activa el entorno virtual:
   ```bash
   source venv/bin/activate
   ```

4. Instala las dependencias desde el archivo requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```
5. Inicia el servidor del backend:
   ```bash
   fastapi dev ./app/main.py
   ```

## 2. Instalación y ejecución del Frontend
El frontend está desarrollado en Flutter. Si no lo tienes instalado, puedes seguir las instrucciones oficiales [aquí](https://docs.flutter.dev/get-started/install).

1. Abre una nueva terminal y navega a la carpeta del frontend:
   ```powershell
   cd civic_sentiment/frontend/civic_sentiment_app
   ```
2. Descarga las dependencias del proyecto:
   
   ```powershell
   flutter pub get
   ```
3. Inicia la aplicación en el navegador:
   
   ```powershell
   flutter run
   ```

El proyecto ahora debería estar ejecutándose completamente en tu máquina.
