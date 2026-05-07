from bs4 import BeautifulSoup
import json
from config import RUTA_HTML, REGION_HTML

def extraer_jugadores_html(ruta=RUTA_HTML):
    with open(ruta, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "lxml")
    
    jugadores = []
    tablas = soup.find_all("table")
    print(f"[HTML] Se encontraron {len(tablas)} tablas en el archivo.")
    
    for tabla in tablas:
        encabezados = [th.get_text(strip=True).lower().replace(" ", "_")
                       for th in tabla.find_all("th")]
        
        for fila in tabla.find_all("tr"):
            celdas = fila.find_all("td")
            if not celdas:
                continue
            valores = [c.get_text(strip=True) for c in celdas]
            
            if encabezados and len(encabezados) == len(valores):
                jugador = dict(zip(encabezados, valores))
            else:
                jugador = {f"campo_{i}": v for i, v in enumerate(valores)}
            
            jugador["region"] = REGION_HTML
            jugador["fuente"] = "html"
            jugadores.append(jugador)
    
    return jugadores

if __name__ == "__main__":
    datos = extraer_jugadores_html()
    print(f"[HTML] Total jugadores extraídos: {len(datos)}")