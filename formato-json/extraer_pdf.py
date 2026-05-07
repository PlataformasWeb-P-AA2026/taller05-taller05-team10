"""
extraer_pdf.py
Extrae jugadores del PDF usando pdfplumber para detectar tablas.
Maneja correctamente tablas que continúan entre páginas sin repetir encabezados.
"""
import pdfplumber
import json
import os

RUTA_PDF = os.path.join("..", "data", "fuente_pdf_norteamerica_asia.pdf")


def es_encabezado(fila):
    """
    Detecta si una fila es un encabezado o un dato.
    Los encabezados contienen palabras clave, los datos contienen nombres de jugadores.
    """
    if not fila or not any(fila):
        return False
    
    primera_celda = (fila[0] or "").strip().lower()
    
    # Si la primera celda contiene "nombre", es encabezado
    if "nombre" in primera_celda:
        return True
    
    # Si contiene palabras clave de columnas, es encabezado
    palabras_encabezado = ["nombre", "seleccion", "posicion", "edad", "goles"]
    fila_texto = " ".join([str(c or "").lower() for c in fila])
    
    if all(palabra in fila_texto for palabra in palabras_encabezado):
        return True
    
    # Si la primera celda parece un nombre de jugador (ej: "EEUU_Jugador_0"), NO es encabezado
    if "_jugador_" in primera_celda:
        return False
    
    return False


def extraer_jugadores_pdf(ruta=RUTA_PDF):
    jugadores = []
    
    try:
        with pdfplumber.open(ruta) as pdf:
            print(f"[PDF] Documento con {len(pdf.pages)} página(s).")
            
            for num_pagina, pagina in enumerate(pdf.pages, start=1):
                print(f"[PDF] Procesando página {num_pagina}...")
                
                # Extraer tablas
                tablas = pagina.extract_tables()
                
                if not tablas:
                    print(f"[PDF]   ⚠️ No se detectaron tablas en página {num_pagina}")
                    continue
                
                print(f"[PDF]   {len(tablas)} tabla(s) detectada(s)")
                
                for idx_tabla, tabla in enumerate(tablas, 1):
                    if not tabla or len(tabla) < 1:
                        continue
                    
                    primera_fila = tabla[0]
                    
                    # Verificar si la primera fila es encabezado o dato
                    if es_encabezado(primera_fila):
                        print(f"[PDF]   Tabla {idx_tabla} - Encabezados detectados: {primera_fila}")
                        filas_datos = tabla[1:]  # Saltar encabezado
                    else:
                        print(f"[PDF]   Tabla {idx_tabla} - Sin encabezado (continuación de página anterior)")
                        filas_datos = tabla  # Todas las filas son datos
                    
                    # Procesar filas de datos
                    for fila in filas_datos:
                        if not fila or not any(fila):
                            continue
                        
                        valores = [(v or "").strip() for v in fila]
                        
                        # Validar que tenga al menos 5 campos y que el primero parezca un nombre
                        if len(valores) >= 5 and valores[0]:
                            jugador = {
                                "nombre": valores[0],
                                "seleccion": valores[1],
                                "posicion": valores[2],
                                "edad": valores[3],
                                "goles": valores[4],
                                "region": "Norteamérica/Asia",
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
    if datos:
        print(f"\n[PDF] Primeros 3 registros:")
        for i, j in enumerate(datos[:3], 1):
            print(f"\n{i}. {json.dumps(j, indent=2, ensure_ascii=False)}")
        
        print(f"\n[PDF] Últimos 3 registros:")
        for i, j in enumerate(datos[-3:], len(datos)-2):
            print(f"\n{i}. {json.dumps(j, indent=2, ensure_ascii=False)}")
    else:
        print("\n⚠️  No se extrajeron jugadores.")