"""
habilitar_cors.py
Habilita CORS en CouchDB para que la app Vite (frontend) pueda consumir
las vistas desde el navegador en http://localhost:5173
"""
import requests
from requests.auth import HTTPBasicAuth

# ⚠️ Ajusta estas credenciales a las tuyas
USUARIO = "admin"
PASSWORD = "admin"

auth = HTTPBasicAuth(USUARIO, PASSWORD)
base_httpd = "http://localhost:5984/_node/_local/_config/httpd"
base_cors = "http://localhost:5984/_node/_local/_config/cors"


def configurar(url, valor):
    r = requests.put(url, auth=auth, data=f'"{valor}"')
    print(f"  {url.split('/')[-1]}: {r.status_code}")


print("Habilitando CORS en CouchDB...")
configurar(f"{base_httpd}/enable_cors", "true")
configurar(f"{base_cors}/origins", "*")
configurar(f"{base_cors}/credentials", "true")
configurar(f"{base_cors}/methods", "GET, PUT, POST, HEAD, DELETE")
configurar(f"{base_cors}/headers",
           "accept, authorization, content-type, origin, referer")
print("✅ CORS habilitado.")