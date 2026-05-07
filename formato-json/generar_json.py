"""
generar_json.py
Orquesta la extracción de las 3 fuentes y genera mundial_2026.json
en formato CouchDB: { "docs": [...] }
"""
import json
from extraer_html import extraer_jugadores_html
from extraer_csv import extraer_jugadores_csv
from extraer_pdf import extraer_jugadores_pdf

ARCHIVO_SALIDA = "mundial_2026.json"


def normalizar_tipos(jugador):
    """Convierte campos numéricos a int para que las vistas funcionen bien."""
    campos_numericos = ["goles", "partidos", "edad", "numero",
                        "asistencias", "dorsal"]
    for campo in campos_numericos:
        if campo in jugador:
            try:
                jugador[campo] = int(jugador[campo])
            except (ValueError, TypeError):
                pass
    return jugador


def main():
    print("=" * 60)
    print("INICIANDO INTEGRACIÓN DE DATOS - TALLER 05")
    print("=" * 60)

    print("\n--- HTML (Europa) ---")
    europa = extraer_jugadores_html()

    print("\n--- CSV (Sudamérica) ---")
    sudamerica = extraer_jugadores_csv()

    print("\n--- PDF (Norteamérica/Asia) ---")
    norte_asia = extraer_jugadores_pdf()

    todos = europa + sudamerica + norte_asia
    todos = [normalizar_tipos(j) for j in todos]

    documento_couch = {"docs": todos}

    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        json.dump(documento_couch, f, indent=2, ensure_ascii=False, default=str)

    print("\n" + "=" * 60)
    print(f"✅ Archivo generado: {ARCHIVO_SALIDA}")
    print(f"   Total documentos: {len(todos)}")
    print(f"   - Europa (HTML):           {len(europa)}")
    print(f"   - Sudamérica (CSV):        {len(sudamerica)}")
    print(f"   - Norteamérica/Asia (PDF): {len(norte_asia)}")
    print("=" * 60)


if __name__ == "__main__":
    main()