

👨🏻‍🏫 Profesor: Juan Ignacio Bonini
🏫 Institución: IFTS Nº 18

👤 Alumnos:

    Juan José Albornoz

    Estefany Herrera Martínez

    Carolina Linares

    Gonzalo Rey del Castillo

✨ Descripción del proyecto

OcrAPP es una aplicación web que permite subir imágenes o archivos PDF y devuelve el texto extraído en formatos .docx y .txt, aplicando procesamiento digital de imágenes para mejorar la precisión del OCR.

Su objetivo es facilitar la digitalización de apuntes, estudios médicos, facturas y otros documentos escaneados, combinando visión por computadora con una interfaz web simple y funcional.
🚀 Funcionalidades

    📤 Subida de archivos .pdf, .jpg, .jpeg o .png

    🧼 Opción de mejora de imagen antes del OCR (preprocesamiento)

    🔎 Extracción de texto usando Tesseract OCR (psm 4)

    📝 Exportación en formatos .docx y .txt

    🌐 Interfaz web con FastAPI + Jinja2

    📁 Código modular, organizado y reutilizable

    🐳 Despliegue en la nube con Docker y Render

    ✅ Control de versiones con Git

    📜 Registro de cambios (CHANGELOG.md)

🧠 Arquitectura y módulos
Módulo	Descripción
main.py	Entrypoint de FastAPI. Maneja las rutas /, /upload y /descargar. Conecta interfaz web con la lógica OCR.
ocr.py	Lógica de procesamiento del archivo: guarda, convierte, preprocesa, extrae texto, guarda resultado.
preprocess.py	Funciones para mejorar la imagen antes del OCR (binarización, contraste, etc.).
templates/	HTML renderizado con Jinja2 para la UI.
static/	Archivos CSS, JS, o imágenes estáticas.
🧼 ¿Cuándo conviene aplicar preprocesamiento?
Tipo de documento	¿Aplicar mejora?	Motivo
📄 PDF limpio y generado por computadora	❌ No	El OCR ya funciona bien sin intervención
📸 Foto de celular con sombras o torcido	✅ Sí	Mejora contraste y legibilidad del texto
🧾 Documento escaneado con letra chica	✅ Sí	Mejora el contraste y separación texto-fondo
🖋️ Documento con firmas o sellos	❌ No	Podría perder información relevante
📃 Formularios con muchas tablas	✅ / ❌	Depende de la calidad, conviene probar ambos enfoques
🐳 Despliegue con Docker

Esta app es fácilmente desplegable vía Docker, incluyendo las dependencias necesarias como Tesseract y Poppler.
Archivos relevantes:

    Dockerfile: construye la imagen con las herramientas necesarias.

    render.yaml: configuración para despliegue automático en Render.

🔗 App desplegada en producción:
https://ocrapp.data-bi.ar
⚙️ Instalación local
1. Clonar el proyecto

git clone https://github.com/tu_usuario/ocr-app.git
cd ocr-app

2. Crear entorno virtual

python3 -m venv env

# Linux/macOS:
source env/bin/activate

# Windows:
env\Scripts\activate

3. Instalar dependencias

pip install -r requirements.txt

4. Instalar Tesseract OCR
macOS:

brew install tesseract

Ubuntu:

sudo apt install tesseract-ocr

Windows:

Descargar desde: UB Mannheim Tesseract
5. Instalar Poppler (para convertir PDFs)
macOS:

brew install poppler

Ubuntu:

sudo apt install poppler-utils

▶️ Ejecutar la aplicación

uvicorn app.main:app --reload

📎 Acceder en el navegador: http://localhost:8000
📂 Estructura del proyecto

ocr-app/
├── app/
│   ├── main.py          # API principal (FastAPI)
│   ├── ocr.py           # Lógica OCR (procesamiento)
│   ├── preprocess.py    # Mejora de imagen
│   └── templates/       # HTML (Jinja2)
│       └── form.html
├── static/
│   └── style.css        # Estilos
├── uploads/             # Archivos temporales
├── outputs/             # Archivos generados
├── requirements.txt
├── Dockerfile
├── render.yaml
├── README.md
├── CHANGELOG.md
└── .gitignore

❤️ Créditos

Este proyecto fue desarrollado con pruebas, aprendizaje, colaboración y muchos mates por:

    Juan José Albornoz

    Estefany Herrera Martínez

    Carolina Linares

    Gonzalo Rey del Castillo

Trabajo final para la materia Técnicas de Procesamiento Digital de Imágenes. ¡Gracias a quienes acompañaron este proceso! 🤗