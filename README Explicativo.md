# Taller 05 · Integración de Datos con CouchDB y Vite

> **Universidad Técnica Particular de Loja (UTPL)**  
> **Plataformas Web** · 2025-2026 · **Equipo 10**

Proyecto académico que demuestra la integración de datos provenientes de múltiples fuentes heterogéneas (**HTML**, **CSV**, **PDF**), su transformación a un formato común (**JSON**), su almacenamiento en una base de datos NoSQL (**Apache CouchDB**) y su consulta desde una aplicación web moderna construida con **Vite**.

---

## 📋 Tabla de contenidos

1. [Descripción del proyecto](#-descripción-del-proyecto)
2. [Tecnologías y librerías utilizadas](#-tecnologías-y-librerías-utilizadas)
3. [Requisitos previos](#-requisitos-previos)
4. [Estructura del proyecto](#-estructura-del-proyecto)
5. [Paso 1 · Preparación de datos](#-paso-1--preparación-de-datos)
6. [Paso 2 · Configuración de CouchDB ⚠️ IMPORTANTE](#-paso-2--configuración-de-couchdb-️-importante)
7. [Paso 3 · Carga de datos y creación de vistas](#-paso-3--carga-de-datos-y-creación-de-vistas)
8. [Paso 4 · Ejecución del Frontend](#-paso-4--ejecución-del-frontend)
9. [Solución de problemas](#-solución-de-problemas)

---

## 🎯 Descripción del proyecto

El taller consiste en construir una **pipeline de datos completa** que:

1. **Lee** información sobre jugadores de fútbol del Mundial 2026 desde tres archivos con formatos distintos:
   - `fuente_html_europa.html` (jugadores europeos)
   - `fuente_csv_sudamerica.csv` (jugadores sudamericanos)
   - `fuente_pdf_norteamerica_asia.pdf` (jugadores de Norteamérica y Asia)
2. **Transforma** los datos heterogéneos en un único archivo JSON con el formato `{ "docs": [...] }` requerido por CouchDB.
3. **Carga** los documentos en una base de datos CouchDB mediante un script de Python.
4. **Genera** vistas (consultas predefinidas) usando funciones Map en JavaScript.
5. **Consume** las vistas desde una aplicación frontend en Vite con la identidad visual de la UTPL.

---

## 🛠 Tecnologías y librerías utilizadas

### Backend de datos (Python)

| Librería | Propósito | ¿Por qué esta y no otra? |
|----------|-----------|--------------------------|
| **`pdfplumber`** | Extracción de tablas desde PDF | Detecta automáticamente tablas y columnas. **Se descartaron `PyPDF2`** (no extraía bien el texto, devolvía 0 registros) **y `pdfminer.six`** (extraía el texto fragmentado en columnas, mezclando los datos). |
| **`BeautifulSoup4` + `lxml`** | Parsing de HTML | Estándar de la industria, robusto y rápido. Maneja HTML mal formado mejor que `html.parser`. |
| **`pandas`** | Lectura de CSV | Maneja codificaciones automáticamente (UTF-8, Latin-1, CP1252) y limpia valores `NaN`. **Se descartó el módulo `csv` nativo** porque no maneja bien archivos con caracteres especiales del español (acentos, ñ). |
| **`requests`** | Comunicación con CouchDB | Más flexible y didáctico que la librería `couchdb`. Permite ver exactamente qué pasa en cada petición HTTP. **Se descartó `curl`** porque el taller exige usar Python. |

### Base de datos

| Tecnología | Propósito |
|------------|-----------|
| **Apache CouchDB** | Base de datos NoSQL orientada a documentos. Permite almacenar documentos heterogéneos (no todos los jugadores tienen los mismos campos) sin definir esquemas previos. Su modelo de **vistas con funciones Map/Reduce** es ideal para los requerimientos del taller. |

### Frontend

| Librería | Propósito | ¿Por qué esta y no otra? |
|----------|-----------|--------------------------|
| **Vite** | Build tool y dev server | Mucho más rápido que Webpack/Create React App. HMR (Hot Module Replacement) instantáneo. |
| **DataTables (`datatables.net-dt`)** | Componente de tabla interactiva | Provee búsqueda, ordenamiento y paginación **gratis**. **Se descartó construir la tabla manualmente** porque era reinventar la rueda y agregaba 80+ líneas de código innecesarias. |
| **CSS3 puro** | Estilización con colores UTPL | **Se descartó Tailwind** porque para un proyecto pequeño como este, el CSS plano es más rápido de aplicar y no requiere configuración extra (PostCSS, plugins, etc.). |

---

## ✅ Requisitos previos

Antes de empezar, asegúrate de tener instalado en tu máquina **Windows**:

| Software | Versión recomendada | Enlace de descarga |
|----------|---------------------|--------------------|
| **Python** | 3.10  | [python.org](https://www.python.org/downloads/) |
| **Node.js** | 22  | [nodejs.org](https://nodejs.org/) |
| **Apache CouchDB** | 3.x | [couchdb.apache.org](https://couchdb.apache.org/#download) |
| **Git** | Cualquiera | [git-scm.com](https://git-scm.com/) |

> 💡 **Verifica las instalaciones** abriendo PowerShell y ejecutando:
> ```powershell
> python --version
> node --version
> npm --version
> ```

---

## 📂 Estructura del proyecto

```
taller05-taller05-team10/
├── data/                                       # Archivos fuente (no modificar)
│   ├── fuente_csv_sudamerica.csv
│   ├── fuente_html_europa.html
│   └── fuente_pdf_norteamerica_asia.pdf
│
├── formato-json/                               # Scripts Python de extracción y carga
│   ├── extraer_html.py                         # Extrae datos del HTML
│   ├── extraer_csv.py                          # Extrae datos del CSV
│   ├── extraer_pdf.py                          # Extrae datos del PDF
│   ├── generar_json.py                         # Orquesta los 3 scripts y genera el JSON
│   ├── cargar_couchdb.py                       # Carga el JSON y crea las vistas
│   └── mundial_2026.json                       # Generado automáticamente
│
├── frontend/                                   # Aplicación Vite
│   ├── public/
│   ├── src/
│   │   ├── main.js                             # Lógica de consumo de las vistas
│   │   └── style.css                           # Estilos con colores UTPL
│   ├── index.html                              # Estructura HTML con título y footer
│   └── package.json
│
├── capturas/                                   # Capturas de evidencias
│
├── README.md                                   # Este archivo
└── evidencias.md                               # Documento de evidencias
```

---

## 🚀 Paso 1 · Preparación de datos

### 1.1. Instalación de dependencias Python

Abre **PowerShell** en la raíz del proyecto y ejecuta:

```powershell
cd formato-json
pip install pdfplumber beautifulsoup4 lxml pandas requests pikepdf
```


### 1.2. Generación del JSON unificado

Desde la carpeta `formato-json/`, ejecuta:

```powershell
python generar_json.py
```

Este script:

1. Llama a `extraer_html.py` → Lee la tabla del HTML con BeautifulSoup4.
2. Llama a `extraer_csv.py` → Lee el CSV con pandas (manejo automático de codificación).
3. Llama a `extraer_pdf.py` → Extrae las tablas del PDF con pdfplumber (maneja correctamente las tablas que continúan entre páginas sin repetir encabezados).
4. Unifica los registros en una lista.
5. Normaliza los tipos de datos (convierte `edad`, `goles` y `partidos` a enteros).
6. Genera el archivo `mundial_2026.json` con el formato exigido por CouchDB:

```json
{
  "docs": [
    { "nombre": "...", "seleccion": "...", "edad": 25, "goles": 10, ... },
    { "nombre": "...", "seleccion": "...", "edad": 30, "goles": 5, ... }
  ]
}
```

**Resultado esperado:**

```
============================================================
INICIANDO INTEGRACIÓN DE DATOS - TALLER 05
============================================================

--- HTML (Europa) ---       [HTML] Total jugadores extraídos: XX
--- CSV (Sudamérica) ---    [CSV] Total jugadores extraídos: XX
--- PDF (Norteamérica/Asia) --- [PDF] Total jugadores extraídos: 40

============================================================
✅ Archivo generado: mundial_2026.json
   Total documentos: XXX
============================================================
```

---

## 🛢 Paso 2 · Configuración de CouchDB ⚠️ IMPORTANTE

### 2.1. Verificar que CouchDB esté corriendo

Abre tu navegador y entra a:

```
http://localhost:5984/_utils
```

Deberías ver la interfaz de **Fauxton** (panel de administración de CouchDB).

> 💡 Si CouchDB no inicia automáticamente, ve a "Servicios" en Windows y arranca el servicio "Apache CouchDB".

### 2.2. Crear la base de datos `jugadores`

1. En Fauxton, click en el botón **"Create Database"** (esquina superior derecha).
2. Nombre: `jugadores`
3. Selecciona **"Non-partitioned"**.
4. Click en **"Create"**.

### 2.3. ⚠️ DESHABILITAR PERMISOS (Paso CRÍTICO para replicabilidad)

> **🚨 ESTE ES EL PASO MÁS IMPORTANTE DE TODA LA CONFIGURACIÓN.**  
> Sin esto, **el frontend no podrá leer los datos** y obtendrás errores `401 Unauthorized` o `403 Forbidden` desde el navegador.

**Por qué es necesario:** Por defecto, CouchDB exige autenticación para cualquier operación. Esto causa problemas tanto con el script Python (al cargar los datos) como con el frontend Vite (al consumir las vistas desde el navegador, donde se mezcla con la complejidad de CORS y autenticación Basic). Para un entorno de desarrollo/académico local, **liberar los permisos de la BD `jugadores`** elimina toda esta complejidad.

**Pasos exactos:**

1. En Fauxton, abre la base de datos `jugadores`.
2. En el menú lateral izquierdo, click en el ícono de **Permissions** (🔒 candado).
3. Verás dos secciones: **Admins** y **Members**.
4. **Borra TODOS los nombres y roles** de ambas secciones:
   - En **Admins** → Vacía los campos "Names" y "Roles".
   - En **Members** → Vacía los campos "Names" y "Roles".
5. Deja **todos los campos en blanco** y guarda los cambios.

> 💡 Esto hace que la BD `jugadores` sea **públicamente accesible** dentro de tu máquina local, lo que permite que el script Python cargue datos sin problemas y que el frontend Vite las consulte sin necesidad de manejar tokens, headers Authorization ni configuraciones complejas de CORS.

> ⚠️ **Nota de seguridad:** Esta configuración solo es válida para entornos locales de desarrollo/académicos. **NUNCA** hagas esto en un entorno de producción.

---

## 📥 Paso 3 · Carga de datos y creación de vistas

### 3.1. Cargar el JSON a CouchDB

Desde la carpeta `formato-json/`, ejecuta:

```powershell
python cargar_couchdb.py
```

Este script realiza tres operaciones automáticamente:

#### a) Verificación/creación de la BD

Comprueba si la BD `jugadores` existe. Si no existe, la crea.

#### b) Carga de documentos

Hace un `POST` al endpoint `_bulk_docs` de CouchDB con todos los jugadores del JSON:

```python
url = f"{COUCHDB_URL}/{NOMBRE_BD}/_bulk_docs"
requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))
```

#### c) Creación del Design Document `losjugadores` con las 3 vistas

Hace un `PUT` con la definición del Design Document que contiene las 3 vistas en JavaScript.

### 3.2. Estructura de las vistas

Cada vista usa una **función Map** que indexa los documentos por un campo específico:

**Vista `por_club`:**
```javascript
function(doc) {
  if (doc.club_actual) {
    emit(doc.club_actual, doc);
  }
}
```

**Vista `por_goles`:**
```javascript
function(doc) {
  if (doc.goles) {
    emit(doc.goles, doc);
  }
}
```

**Vista `por_partidos`:**
```javascript
function(doc) {
  if (doc.partidos) {
    emit(doc.partidos, doc);
  }
}
```

**Resultado esperado:**

```
✅ BD 'jugadores' creada (o ya existía).
✅ Documentos cargados: XXX
✅ Vistas 'por_club', 'por_goles', 'por_partidos' creadas.

🎉 Listo. Verifica en: http://localhost:5984/_utils
```

### 3.3. Verificar las vistas

En Fauxton:

1. Entra a la BD `jugadores`.
2. En el menú lateral, click en **"Design Documents"**.
3. Click en `_design/losjugadores`.
4. Verás las tres vistas. Click en cada una y luego en **"Run Query"** para ver los resultados.

---

## 🎨 Paso 4 · Ejecución del Frontend

### 4.1. Instalar dependencias Node

Desde la raíz del proyecto:

```powershell
cd frontend
npm install
```

Esto instalará Vite y DataTables (ya están declaradas en `package.json`).

### 4.2. Levantar el servidor de desarrollo

```powershell
npm run dev
```

**Resultado esperado:**

```
  VITE v5.x.x  ready in 350 ms

  ➜  Local:   http://localhost:5173/
```

### 4.3. Abrir en el navegador

Ve a `http://localhost:5173/`.

Deberías ver la aplicación con:

- **Header azul** (`#003DA5`) con el título "Mundial 2026 · Jugadores".
- **Subtítulo amarillo** (`#FFD100`) con el nombre de la UTPL.
- **Selector de vistas** (Por Club, Por Goles, Por Partidos).
- **Input de filtro** para búsquedas por clave exacta.
- **Tabla DataTables** con los resultados (búsqueda interna, paginación y ordenamiento incluidos).
- **Footer azul oscuro** con identificación de la UTPL y el equipo.

### 4.4. Funcionalidades implementadas

- ✅ **Cambio de vista** mediante el `<select>` superior.
- ✅ **Filtro por clave exacta** usando el endpoint `?key=...` de CouchDB.
- ✅ **Búsqueda libre** dentro de la tabla (provista por DataTables).
- ✅ **Paginación** automática (10 registros por página).
- ✅ **Ordenamiento** por cualquier columna haciendo click en el encabezado.
- ✅ **Diseño responsivo** con colores institucionales UTPL.

---



## 🩹 Solución de problemas


### El PDF extrae menos jugadores de los esperados

Esto puede pasar cuando una tabla continúa en la siguiente página sin repetir el encabezado. El script `extraer_pdf.py` ya maneja este caso detectando si la primera fila de cada tabla es un encabezado o un dato.


---

## 👥 Equipo

**Equipo 10** · Plataformas Web · UTPL · 2025-2026

---

## 📄 Licencia

Proyecto académico desarrollado para fines educativos en el marco de la asignatura **Plataformas Web** de la **Universidad Técnica Particular de Loja**.
