"""
diagnosticar_pdf.py
Verifica si el PDF es válido y muestra información básica.
"""
import os

ruta_pdf = os.path.join("..", "data", "fuente_pdf_norteamerica_asia.pdf")

# 1. Verificar que existe
if not os.path.exists(ruta_pdf):
    print(f"❌ El archivo no existe en: {ruta_pdf}")
    exit(1)

print(f"✅ Archivo encontrado: {ruta_pdf}")

# 2. Verificar tamaño
tamaño = os.path.getsize(ruta_pdf)
print(f"📊 Tamaño: {tamaño:,} bytes ({tamaño / 1024:.2f} KB)")

if tamaño < 100:
    print("⚠️  El archivo es sospechosamente pequeño (podría estar vacío o corrupto)")

# 3. Verificar firma PDF
with open(ruta_pdf, "rb") as f:
    primeros_bytes = f.read(10)
    print(f"🔍 Primeros bytes: {primeros_bytes}")
    
    if not primeros_bytes.startswith(b"%PDF"):
        print("❌ NO es un PDF válido (falta la firma %PDF)")
        print("   Esto podría ser un archivo HTML, imagen, o descarga incompleta")
    else:
        version = primeros_bytes[5:8].decode("ascii", errors="ignore")
        print(f"✅ PDF válido, versión: {version}")

# 4. Intentar abrirlo con PyPDF2 (más tolerante a errores)
try:
    from PyPDF2 import PdfReader
    reader = PdfReader(ruta_pdf)
    print(f"✅ PyPDF2 puede leerlo: {len(reader.pages)} página(s)")
except ImportError:
    print("ℹ️  Instala PyPDF2 para más diagnóstico: pip install PyPDF2")
except Exception as e:
    print(f"❌ PyPDF2 también falló: {e}")