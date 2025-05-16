# 🧾 OCR App - Transformaciones para facilitar la lectura automática

**Trabajo Final Integrador - Técnicas de Procesamiento Digital de Imágenes**

📅 Año: 2025  
👨🏻‍🏫 Profesor: Juan Ignacio Bonini  
👤 Alumnos:
- Juan Jose Albornoz
- Estefany Herrera Martinez
- Carolina Linares
- Gonzalo Rey del Castillo 

---

## ✨ Descripción del proyecto

Esta aplicación web permite subir archivos de imagen o PDF escaneados y devuelve un documento `.docx` con el texto extraído, listo para copiar, editar o guardar.

El objetivo es facilitar la lectura automática (OCR) de apuntes, facturas, formularios y cualquier otro documento escaneado, mejorando la accesibilidad al contenido textual.

Desarrollado usando Python, FastAPI, OpenCV y Tesseract OCR, este proyecto integra procesamiento digital de imágenes con una interfaz web simple y amigable.

---

## 🎯 Objetivo del TP

> _“Proponer, diseñar y desarrollar una solución técnica basada en procesamiento digital de imágenes que permita realizar OCR, utilizando programación orientada a objetos y control de versiones con Git.”_

---

## 🚀 Funcionalidades

- 📤 Subida de archivos `.pdf`, `.jpg`, `.jpeg` o `.png`
- 🔎 Extracción de texto mediante OCR con Tesseract
- 📝 Generación automática de archivo `.docx` descargable
- 💻 Interfaz web simple con HTML + CSS
- 📁 Organización modular del código
- 🌐 API REST con FastAPI
- 🧠 Programación orientada a objetos

---

## 🧪 Requisitos del sistema

- Python 3.9 o superior
- macOS, Linux o Windows
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Poppler](https://poppler.freedesktop.org/) (para PDFs)

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

---

### 4. Instalar Tesseract OCR

#### 🖥️ macOS (con Homebrew):

```bash
brew install tesseract
```

#### 🐧 Ubuntu/Debian:

```bash
sudo apt install tesseract-ocr
```

#### 🪟 Windows:

1. Descargar desde [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
2. Agregar la carpeta de instalación al **PATH del sistema**
3. Activar idioma español si se desea

---

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

### 6. Ejecutar la aplicación

```bash
uvicorn app.main:app --reload
```

Luego ingresar a:

📎 http://localhost:8000

---

## 📂 Estructura del proyecto

```
ocr-app/
├── app/
│   ├── main.py          # API principal
│   ├── ocr.py           # Lógica de OCR
│   ├── utils.py         # (futuro) utilidades auxiliares
│   └── templates/
│       └── form.html    # Interfaz HTML
├── static/
│   └── style.css        # Estilos CSS
├── uploads/             # Archivos temporales subidos
├── outputs/             # Resultados generados
├── requirements.txt     # Dependencias del proyecto
├── .gitignore
└── README.md
```

---

## 💬 Posibles mejoras

- 📄 Opción de exportar también a `.txt`
- 🧼 Preprocesamiento de imagen: binarización, mejora de contraste, reducción de ruido
- 🌍 Soporte multilenguaje OCR
- 🖼️ Visualización previa del texto antes de descargar
- 🧰 Dockerización para despliegue fácil
- 🧪 Tests automatizados

---

## ❤️ Créditos

Este proyecto fue desarrollado con amor, mate y muchas líneas de código por Juanjo, Estefy, Carito y Gonza como parte del trabajo final para la materia **Técnicas de Procesamiento Digital de Imágenes**. Gracias a todos los que acompañaron el proceso 🤗
