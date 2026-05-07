
"""
extraer_csv.py
Extrae datos de jugadores sudamericanos desde el CSV en ../data/
"""
import pandas as pd
import json
import os

RUTA_CSV = os.path.join("..", "data", "fuente_csv_sudamerica.csv")


def extraer_jugadores_csv(ruta=RUTA_CSV):
    df = None
    for encoding in ["utf-8", "latin-1", "cp1252"]:
        try:
            df = pd.read_csv(ruta, encoding=encoding)
            print(f"[CSV] Leído correctamente con codificación: {encoding}")
            break
        except UnicodeDecodeError:
            continue

    if df is None:
        raise RuntimeError("No se pudo leer el CSV con ninguna codificación.")

    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    jugadores = []
    for j in df.to_dict(orient="records"):
        jugador = {k: v for k, v in j.items() if pd.notna(v)}
        jugador["region"] = "Sudamérica"
        jugador["fuente"] = "csv"
        jugadores.append(jugador)

    return jugadores


if __name__ == "__main__":
    datos = extraer_jugadores_csv()
    print(f"[CSV] Total jugadores extraídos: {len(datos)}")
    if datos:
        print("[CSV] Ejemplo del primer registro:")
        print(json.dumps(datos[0], indent=2, ensure_ascii=False, default=str))