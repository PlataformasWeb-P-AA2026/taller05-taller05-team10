"""
cargar_couchdb.py
1. Crea la BD 'jugadores'
2. Carga mundial_2026.json
3. Crea el design document 'losjugadores' con las 3 vistas
"""
import json
import requests
from requests.auth import HTTPBasicAuth

# === CONFIGURACIÓN ===
COUCHDB_URL = "http://localhost:5984"
USUARIO = "admin"           # ⚠️ Cambia por tu usuario
PASSWORD = "admin"          # ⚠️ Cambia por tu contraseña
NOMBRE_BD = "jugadores"
ARCHIVO_JSON = "mundial_2026.json"

auth = HTTPBasicAuth(USUARIO, PASSWORD)


def crear_base_datos():
    url = f"{COUCHDB_URL}/{NOMBRE_BD}"
    r = requests.put(url, auth=auth)
    if r.status_code == 201:
        print(f"✅ BD '{NOMBRE_BD}' creada.")
    elif r.status_code == 412:
        print(f"ℹ️  BD '{NOMBRE_BD}' ya existe.")
    else:
        print(f"⚠️  {r.status_code}: {r.text}")
        r.raise_for_status()


def cargar_documentos():
    with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    url = f"{COUCHDB_URL}/{NOMBRE_BD}/_bulk_docs"
    r = requests.post(
        url, auth=auth,
        headers={"Content-Type": "application/json"},
        data=json.dumps(data, ensure_ascii=False).encode("utf-8")
    )
    r.raise_for_status()

    resultado = r.json()
    exitosos = sum(1 for d in resultado if "ok" in d)
    fallidos = len(resultado) - exitosos
    print(f"✅ Documentos cargados: {exitosos}")
    if fallidos:
        print(f"⚠️  Errores: {fallidos}")


def crear_vistas():
    design_doc = {
        "_id": "_design/losjugadores",
        "language": "javascript",
        "views": {
            "por_club": {
                "map": (
                    "function(doc) {\n"
                    "  if (doc.club_actual) {\n"
                    "    emit(doc.club_actual, doc);\n"
                    "  }\n"
                    "}"
                )
            },
            "por_goles": {
                "map": (
                    "function(doc) {\n"
                    "  if (doc.goles) {\n"
                    "    emit(doc.goles, doc);\n"
                    "  }\n"
                    "}"
                )
            },
            "por_partidos": {
                "map": (
                    "function(doc) {\n"
                    "  if (doc.partidos) {\n"
                    "    emit(doc.partidos, doc);\n"
                    "  }\n"
                    "}"
                )
            }
        }
    }

    url = f"{COUCHDB_URL}/{NOMBRE_BD}/_design/losjugadores"

    existente = requests.get(url, auth=auth)
    if existente.status_code == 200:
        design_doc["_rev"] = existente.json()["_rev"]
        print("ℹ️  Design document existente, se actualizará.")

    r = requests.put(
        url, auth=auth,
        headers={"Content-Type": "application/json"},
        data=json.dumps(design_doc)
    )
    if r.status_code in (201, 202):
        print("✅ Vistas 'por_club', 'por_goles', 'por_partidos' creadas.")
    else:
        print(f"⚠️  {r.status_code}: {r.text}")


if __name__ == "__main__":
    crear_base_datos()
    cargar_documentos()
    crear_vistas()
    print(f"\n🎉 Listo. Verifica en: {COUCHDB_URL}/_utils")