import pdfplumber
import json
from config import RUTA_PDF, REGION_PDF

def es_encabezado(fila):
    if not fila or not any(fila):
        return False
    primera_celda = (fila[0] or "").strip().lower()
    if "nombre" in primera_celda or "_jugador_" in primera_celda:
        return "nombre" in primera_celda
    return False

def extraer_jugadores_pdf(ruta=RUTA_PDF):
    jugadores = []
    
    try:
        with pdfplumber.open(ruta) as pdf:
            print(f"[PDF] Documento con {len(pdf.pages)} página(s).")
            
            for num_pagina, pagina in enumerate(pdf.pages, start=1):
                print(f"[PDF] Procesando página {num_pagina}...")
                tablas = pagina.extract_tables()
                
                if not tablas:
                    print(f"[PDF]   ⚠️ No se detectaron tablas")
                    continue
                
                print(f"[PDF]   {len(tablas)} tabla(s) detectada(s)")
                
                for idx_tabla, tabla in enumerate(tablas, 1):
                    if not tabla or len(tabla) < 1:
                        continue
                    
                    primera_fila = tabla[0]
                    
                    if es_encabezado(primera_fila):
                        print(f"[PDF]   Tabla {idx_tabla} - Con encabezado")
                        filas_datos = tabla[1:]
                    else:
                        print(f"[PDF]   Tabla {idx_tabla} - Sin encabezado")
                        filas_datos = tabla
                    
                    for fila in filas_datos:
                        if not fila or not any(fila):
                            continue
                        
                        valores = [(v or "").strip() for v in fila]
                        
                        if len(valores) >= 5 and valores[0]:
                            jugador = {
                                "nombre": valores[0],
                                "seleccion": valores[1],
                                "posicion": valores[2],
                                "edad": valores[3],
                                "goles": valores[4],
                                "region": REGION_PDF,
                                "fuente": "pdf"
                            }
                            jugadores.append(jugador)
        
        print(f"\n[PDF] Total jugadores extraídos: {len(jugadores)}")
        
    except Exception as e:
        print(f"[PDF] ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return []
    
    return jugadores

if __name__ == "__main__":
    datos = extraer_jugadores_pdf()