"""
Ejemplo de uso del scraper de Primicias - Sección Economía
Este archivo analiza todos los artículos de la sección de economía
"""
from app.services.primicias.title_service import PrimiciasService


def main():
    # Crear instancia del servicio
    service = PrimiciasService()
    
    # Ejemplo 1: Obtener títulos de economía con análisis de sentimiento
    print("=== TÍTULOS DE ECONOMÍA - PRIMICIAS ===")
    economia_titles = service.get_economia_titles()
    print(f"Total de títulos: {economia_titles.total_count}")
    print(f"Fuente: {economia_titles.source}")
    
    for title in economia_titles.titles[:5]:  # Mostrar solo los primeros 5
        print(f"- {title.text}")
        if title.sentiment:
            print(f"  Sentimiento: {title.sentiment.label.value} "
                  f"({title.sentiment.score:.2f})")
    
    print("\n" + "="*70 + "\n")
    
    # Ejemplo 2: Análisis detallado completo de economía
    print("=== ANÁLISIS DETALLADO - ECONOMÍA ===")
    detailed_analysis = service.get_economia_detailed_analysis()
    print(f"Total de artículos analizados: {len(detailed_analysis)}")
    
    for i, item in enumerate(detailed_analysis[:3]):  # Solo los primeros 3
        print(f"\nArtículo {i+1}: {item['titulo']}")
        print(f"Página: {item['pagina']}")
        print(f"Enlace: {item['enlace']}")
        
        # Mostrar sentimiento del título
        titulo_sentiment = item['titulo_sentimiento']
        print(f"Sentimiento del título: {titulo_sentiment['label']} "
              f"({titulo_sentiment['score']:.2f})")
        
        # Mostrar citas encontradas
        print(f"Citas encontradas: {len(item['citas'])}")
        
        for j, (cita, emocion) in enumerate(
            zip(item['citas'][:2], item['emociones'][:2])
        ):
            print(f"  Cita {j+1}: {cita[:100]}...")
            print(f"    Sentimiento: {emocion['label']} "
                  f"({emocion['score']:.2f})")
        print("-" * 60)


if __name__ == "__main__":
    main()
