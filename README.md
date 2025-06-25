# 🧾 OCR App - Extracción de texto desde imágenes y PDFs

**Trabajo Final Integrador - Técnicas de Procesamiento Digital de Imágenes**

📅 Año: 2025  
👨🏻‍🏫 Profesor: Juan Ignacio Bonini (@ioanne)
🏫 Institución: IFTS 18
👤 Alumnos:
- Juan Jose Albornoz (@juanjoalbornoz)
- Estefany Herrera Martinez (@hmestefany)
- Carolina Linares (@carolinares03)
- Gonzalo Rey del Castillo (@King-Zalogon)

---

## ✨ Descripción del proyecto

**OcrAPP** es una aplicación web que permite subir imágenes o PDFs escaneados y devuelve el texto extraído en formatos `.docx` y `.txt`.

Su objetivo es facilitar la digitalización de apuntes, estudios médicos, facturas y otros documentos escaneados, combinando procesamiento digital de imágenes con una interfaz clara y práctica.

---

## 🚀 Funcionalidades

- ✅ Extracción de texto desde imágenes (`.jpg`, `.png`) y `.pdf`  
- ✅ Interfaz simple e intuitiva para subir archivos  
- ✅ Preprocesamiento automático de imágenes para mejorar la lectura  
- ✅ Soporte multilenguaje para OCR (incluye español e inglés)  
- ✅ Exportación del texto extraído a archivos `.txt` y `.docx` 
- ✅ Visualización en pantalla del resultado del OCR  
- ✅ (🆕 v1.4.0) **Selector de transformaciones**: podés elegir qué preprocesamientos aplicar a tu imagen antes del OCR

---

## 🧪 Transformaciones disponibles

Al cargar una imagen, podés elegir aplicar una o más de las siguientes transformaciones:

- 🔘 **Color y Contraste**: Escala de grises, inversión de colores, brillo, contraste, CLAHE.
- 🔘 **Filtros y Suavizado**: Desenfoque Gaussiano y Filtro de Mediana.
- 🔘 **Transformaciones Geométricas**: Corrección de inclinación (Deskew), Rotación manual.
- 🔘 **Detección de Bordes**: Filtro de Canny con umbrales ajustables.
- 🔘 **Binarización y Morfología**: Métodos adaptativos y operaciones morfológicas configurables.

Estas herramientas permiten **mejorar la precisión del OCR**, adaptándose a distintas calidades y formatos de documentos.

---

## 🛠️ Tecnologías utilizadas

- **Python 3.11**
- **FastAPI** para el backend
- **OpenCV** para preprocesamiento de imágenes
- **Tesseract OCR** para el reconocimiento de texto
- **Jinja2** para renderizar HTML
- **Docker** para empaquetado y despliegue
- **Render** para el hosting

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

```bash
OcrAPP/
│
├── app/
│   ├── main.py                # Lógica principal y rutas FastAPI
│   ├── ocr.py                 # Funciones de OCR usando Tesseract
│   ├── preprocess.py          # Funciones de preprocesamiento de imágenes
│   ├── templates/
│   │   ├── form.html          # Interfaz web (modo experto)
│   │   └── resultados.html    # Página de resultados OCR
│
├── diagnostics/               # Imágenes preprocesadas para diagnóstico 
├── static/                    # Estilos CSS y otros recursos estáticos
├── uploads/                   # Carpeta donde se almacenan archivos temporales subidos
│
├── Dockerfile                 # Imagen Docker de la aplicación
├── render.yaml                # Configuración para desplegar en Render
├── requirements.txt           # Dependencias del proyecto
├── README.md                  # Documentación del proyecto
└── CHANGELOG.md               # Historial de versiones
```

---

## ❤️ Créditos

Este proyecto fue desarrollado con amor, pruebas, mate y muchas líneas de código por Juanjo, Estefy, Carito y Gonza como parte del trabajo final para la materia **Técnicas de Procesamiento Digital de Imágenes**. Gracias a todos los que acompañaron el proceso, principalmente al profe (@ioanne) por meterse de lleno y potenciarnos 🤗
