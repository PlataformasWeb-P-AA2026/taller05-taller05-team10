import json
import requests
from requests.auth import HTTPBasicAuth
from config import (
    COUCHDB_URL, COUCHDB_USUARIO, COUCHDB_PASSWORD,
    NOMBRE_BD, ARCHIVO_JSON_SALIDA, DESIGN_DOCUMENT_NAME
)

auth = HTTPBasicAuth(COUCHDB_USUARIO, COUCHDB_PASSWORD)

def crear_base_datos():
    url = f"{COUCHDB_URL}/{NOMBRE_BD}"
    r = requests.put(url, auth=auth)
    if r.status_code == 201:
        print(f"✅ BD '{NOMBRE_BD}' creada.")
    elif r.status_code == 412:
        print(f"ℹ️  BD '{NOMBRE_BD}' ya existe.")
    else:
        print(f"⚠️  {r.status_code}: {r.text}")

def cargar_documentos():
    with open(ARCHIVO_JSON_SALIDA, "r", encoding="utf-8") as f:
        data = json.load(f)

    url = f"{COUCHDB_URL}/{NOMBRE_BD}/_bulk_docs"
    r = requests.post(url, auth=auth,
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(data, ensure_ascii=False).encode("utf-8"))
    r.raise_for_status()

    resultado = r.json()
    exitosos = sum(1 for d in resultado if "ok" in d)
    fallidos = len(resultado) - exitosos
    print(f"✅ Documentos cargados: {exitosos}")
    if fallidos:
        print(f"⚠️  Errores: {fallidos}")

def crear_vistas():
    design_doc = {
        "_id": f"_design/{DESIGN_DOCUMENT_NAME}",
        "language": "javascript",
        "views": {
            "por_club": {
                "map": "function(doc) { if (doc.club_actual) { emit(doc.club_actual, doc); } }"
            },
            "por_goles": {
                "map": "function(doc) { if (doc.goles) { emit(doc.goles, doc); } }"
            },
            "por_partidos": {
                "map": "function(doc) { if (doc.partidos) { emit(doc.partidos, doc); } }"
            }
        }
    }

    url = f"{COUCHDB_URL}/{NOMBRE_BD}/_design/{DESIGN_DOCUMENT_NAME}"
    existente = requests.get(url, auth=auth)
    if existente.status_code == 200:
        design_doc["_rev"] = existente.json()["_rev"]

    r = requests.put(url, auth=auth,
                     headers={"Content-Type": "application/json"},
                     data=json.dumps(design_doc))
    if r.status_code in (201, 202):
        print("✅ Vistas creadas.")
    else:
        print(f"⚠️  {r.status_code}: {r.text}")

if __name__ == "__main__":
    crear_base_datos()
    cargar_documentos()
    crear_vistas()
    print(f"\n🎉 Listo. Verifica en: {COUCHDB_URL}/_utils")