"""
config.py
Configuración centralizada para los scripts de extracción y carga de datos.
"""
import os

# ============================================================
# RUTAS DE ARCHIVOS FUENTE
# ============================================================
CARPETA_DATA = os.path.join("..", "data")
RUTA_HTML = os.path.join(CARPETA_DATA, "fuente_html_europa.html")
RUTA_CSV = os.path.join(CARPETA_DATA, "fuente_csv_sudamerica.csv")
RUTA_PDF = os.path.join(CARPETA_DATA, "fuente_pdf_norteamerica_asia.pdf")

# ============================================================
# ARCHIVO DE SALIDA
# ============================================================
ARCHIVO_JSON_SALIDA = "mundial_2026.json"

# ============================================================
# CONFIGURACIÓN DE COUCHDB
# ============================================================
COUCHDB_HOST = "localhost"
COUCHDB_PORT = 5984
COUCHDB_URL = f"http://{COUCHDB_HOST}:{COUCHDB_PORT}"

# Credenciales (solo para operaciones administrativas)
COUCHDB_USUARIO = "admin"
COUCHDB_PASSWORD = "admin"

# Base de datos y vistas
NOMBRE_BD = "jugadores"
DESIGN_DOCUMENT_NAME = "losjugadores"
VISTAS = ["por_club", "por_goles", "por_partidos"]

# ============================================================
# CONFIGURACIÓN DE EXTRACCIÓN
# ============================================================
CAMPOS_NUMERICOS = ["goles", "partidos", "edad", "numero", "asistencias", "dorsal"]
CODIFICACIONES_CSV = ["utf-8", "latin-1", "cp1252"]

# Etiquetas de región
REGION_HTML = "Europa"
REGION_CSV = "Sudamérica"
REGION_PDF = "Norteamérica/Asia"