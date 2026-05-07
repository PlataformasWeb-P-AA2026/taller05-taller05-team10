import pandas as pd
import json
from config import RUTA_CSV, REGION_CSV, CODIFICACIONES_CSV

def extraer_jugadores_csv(ruta=RUTA_CSV):
    df = None
    for encoding in CODIFICACIONES_CSV:
        try:
            df = pd.read_csv(ruta, encoding=encoding)
            print(f"[CSV] Leído con codificación: {encoding}")
            break
        except UnicodeDecodeError:
            continue
    
    if df is None:
        raise RuntimeError("No se pudo leer el CSV")
    
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    
    jugadores = []
    for j in df.to_dict(orient="records"):
        jugador = {k: v for k, v in j.items() if pd.notna(v)}
        jugador["region"] = REGION_CSV
        jugador["fuente"] = "csv"
        jugadores.append(jugador)
    
    return jugadores

if __name__ == "__main__":
    datos = extraer_jugadores_csv()
    print(f"[CSV] Total jugadores extraídos: {len(datos)}")