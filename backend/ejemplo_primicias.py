"""
Ejemplo de uso del scraper de Primicias
Este archivo reemplaza la funcionalidad del primicias_scraping.py original
"""
from app.services.primicias.title_service import PrimiciasService

def main():
    # Crear instancia del servicio
    service = PrimiciasService()
    
    # Ejemplo 1: Búsqueda por término (equivalente al script original)
    search_term = "Obras"
    print(f"=== BÚSQUEDA POR TÉRMINO: {search_term} ===")
    search_results = service.search_by_term(search_term)
    print(f"Total encontrado: {search_results.total_count}")
    
    for title in search_results.titles[:5]:  # Mostrar solo los primeros 5
        print(f"- {title.text}")
        if title.sentiment:
            print(f"  Sentimiento: {title.sentiment.label.value} "
                  f"({title.sentiment.score:.2f})")
    
    print("\n" + "="*60 + "\n")
    
    # Ejemplo 2: Análisis detallado con citas (funcionalidad original completa)
    print(f"=== ANÁLISIS DETALLADO: {search_term} ===")
    detailed_analysis = service.get_detailed_analysis(search_term)
    
    for i, item in enumerate(detailed_analysis[:3]):  # Solo los primeros 3
        print(f"\nArtículo {i+1}: {item['titulo']}")
        print(f"Enlace: {item['enlace']}")
        print(f"Citas encontradas: {len(item['citas'])}")
        
        for j, (cita, emocion) in enumerate(
            zip(item['citas'][:2], item['emociones'][:2])
        ):
            print(f"  Cita {j+1}: {cita[:100]}...")
            print(f"    Sentimiento: {emocion['label']} "
                  f"({emocion['score']:.2f})")
        print("-" * 50)

if __name__ == "__main__":
    main()
