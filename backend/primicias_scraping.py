"""
DEPRECATED: Este archivo ha sido migrado a la arquitectura del proyecto.
Usa en su lugar: app/services/primicias/
O ejecuta: python ejemplo_primicias.py
"""

from app.services.primicias.title_service import PrimiciasService

# Mantener compatibilidad con el script original
def main():
    service = PrimiciasService()
    
    # Análisis detallado equivalente al script original
    search_term = "Obras"
    resultado = service.get_detailed_analysis(search_term)
    
    # Mostrar resultados igual que antes
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

if __name__ == "__main__":
    main()
