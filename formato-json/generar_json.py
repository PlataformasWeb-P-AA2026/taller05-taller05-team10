import json
from extraer_html import extraer_jugadores_html
from extraer_csv import extraer_jugadores_csv
from extraer_pdf import extraer_jugadores_pdf
from config import ARCHIVO_JSON_SALIDA, CAMPOS_NUMERICOS

def normalizar_tipos(jugador):
    for campo in CAMPOS_NUMERICOS:
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

    with open(ARCHIVO_JSON_SALIDA, "w", encoding="utf-8") as f:
        json.dump(documento_couch, f, indent=2, ensure_ascii=False, default=str)

    print("\n" + "=" * 60)
    print(f"✅ Archivo generado: {ARCHIVO_JSON_SALIDA}")
    print(f"   Total documentos: {len(todos)}")
    print(f"   - Europa (HTML):           {len(europa)}")
    print(f"   - Sudamérica (CSV):        {len(sudamerica)}")
    print(f"   - Norteamérica/Asia (PDF): {len(norte_asia)}")
    print("=" * 60)

if __name__ == "__main__":
    main()