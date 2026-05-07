"""
extraer_html.py
Extrae datos de jugadores europeos desde el HTML en ../data/
"""
from bs4 import BeautifulSoup
import json
import os

# Ruta relativa desde formato-json/ hacia data/
RUTA_HTML = os.path.join("..", "data", "fuente_html_europa.html")


def extraer_jugadores_html(ruta=RUTA_HTML):
    with open(ruta, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "lxml")

    jugadores = []
    tablas = soup.find_all("table")
    print(f"[HTML] Se encontraron {len(tablas)} tablas en el archivo.")

    for tabla in tablas:
        encabezados = [
            th.get_text(strip=True).lower().replace(" ", "_")
            for th in tabla.find_all("th")
        ]

        for fila in tabla.find_all("tr"):
            celdas = fila.find_all("td")
            if not celdas:
                continue
            valores = [c.get_text(strip=True) for c in celdas]

            if encabezados and len(encabezados) == len(valores):
                jugador = dict(zip(encabezados, valores))
            else:
                jugador = {f"campo_{i}": v for i, v in enumerate(valores)}

            jugador["region"] = "Europa"
            jugador["fuente"] = "html"
            jugadores.append(jugador)

    return jugadores


if __name__ == "__main__":
    datos = extraer_jugadores_html()
    print(f"[HTML] Total jugadores extraídos: {len(datos)}")
    if datos:
        print("[HTML] Ejemplo del primer registro:")
        print(json.dumps(datos[0], indent=2, ensure_ascii=False))