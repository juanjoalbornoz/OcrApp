# 🧾 OCR App - Transformaciones para facilitar la lectura automática

**Trabajo Final Integrador - Técnicas de Procesamiento Digital de Imágenes**

📅 Año: 2025  
👨🏻‍🏫 Profesor: Juan Ignacio Bonini
🏫 Institución: IFTS 18
👤 Alumnos:
- Juan Jose Albornoz
- Estefany Herrera Martinez
- Carolina Linares
- Gonzalo Rey del Castillo

---

## ✨ Descripción del proyecto

**OcrAPP** es una aplicación web que permite subir imágenes o PDFs escaneados y devuelve el texto extraído en formatos `.docx` y `.txt`.

Su objetivo es facilitar la digitalización de apuntes, estudios médicos, facturas y otros documentos escaneados, combinando procesamiento digital de imágenes con una interfaz clara y práctica.

---

## 🚀 Funcionalidades

- 📤 Subida de archivos `.pdf`, `.jpg`, `.jpeg` o `.png`
- 🧼 Opción de mejora de imagen antes del OCR (preprocesamiento)
- 🔎 Extracción de texto con Tesseract OCR (configurado con `psm 4` u `6`)
- 📝 Exportación en formato `.docx` y `.txt`
- 🖥️ Interfaz web visual con botones de descarga
- 🌐 API REST con FastAPI
- 📁 Organización modular del código
- 🧠 Programación orientada a objetos
- ✅ Control de versiones con Git
- 🗂️ Registro de cambios (`CHANGELOG.md`)

---

## 🧼 Casos de uso del preprocesamiento

El usuario puede elegir aplicar mejora de imagen antes del OCR. A continuación se muestran las situaciones en las que conviene o no utilizar esta opción:

| Tipo de documento                          | ¿Aplicar mejora? | Motivo                                                                 |
|--------------------------------------------|------------------|------------------------------------------------------------------------|
| 📄 PDF limpio y generado por computadora   | ❌ No             | Ya tiene buena calidad, el OCR funciona bien directamente              |
| 📸 Foto de celular con sombras o torcido   | ✅ Sí             | Mejora contraste y claridad para reconocimiento                        |
| 🧾 Documento escaneado con letra chica     | ✅ Sí             | Binarización ayuda a separar texto del fondo                          |
| 🖋️ Documento con firmas o sellos           | ❌ No             | La binarización puede deformar o eliminar partes importantes           |
| 📃 Formularios con muchas tablas           | ✅ o ❌ Dependiendo| Probar ambas, puede funcionar mejor sin mejora si las líneas son nítidas|

---

## 🐳 Despliegue con Docker (Render)

Esta app ahora puede ejecutarse y desplegarse usando contenedores Docker.

### Archivos agregados:

- `Dockerfile`: contiene las instrucciones para construir la imagen con Tesseract y Poppler
- `render.yaml`: configuración para despliegue automático en Render

### Despliegue en la nube

La app está desplegada en:  
🔗 [https://ocrapp.data-bi.ar](https://ocrapp.data-bi.ar)

---

## ⚙️ Instalación y ejecución local

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/ocr-app.git
cd ocr-app
```

### 2. Crear y activar el entorno virtual

```bash
python3 -m venv env

# Linux/macOS:
source env/bin/activate

# Windows:
env\Scripts\activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Instalar Tesseract OCR

#### macOS:

```bash
brew install tesseract
```

#### Ubuntu:

```bash
sudo apt install tesseract-ocr
```

#### Windows:

Descargar desde [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)

### 5. Instalar Poppler (para PDFs)

#### macOS:

```bash
brew install poppler
```

#### Ubuntu:

```bash
sudo apt install poppler-utils
```

---

## 🚀 Ejecutar la aplicación

```bash
uvicorn app.main:app --reload
```

📎 Luego ingresá a: http://localhost:8000

---

## 📂 Estructura del proyecto

```
ocr-app/
├── app/
│   ├── main.py          # API principal
│   ├── ocr.py           # Lógica de OCR
│   ├── preprocess.py    # Mejora de imagen
│   └── templates/
│       └── form.html    # Formulario web
├── static/
│   └── style.css        # Estilos
├── uploads/             # Archivos temporales
├── outputs/             # Archivos generados
├── requirements.txt
├── README.md
├── CHANGELOG.md
└── .gitignore
```

---

## ❤️ Créditos

Este proyecto fue desarrollado con amor, pruebas, mate y muchas líneas de código por Juanjo, Estefy, Carito y Gonza como parte del trabajo final para la materia **Técnicas de Procesamiento Digital de Imágenes**. Gracias a todos los que acompañaron el proceso 🤗