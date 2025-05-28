"""
Módulo de procesamiento OCR de la aplicación.

Responsable de recibir archivos desde la capa web (definida en main.py), aplicar
preprocesamiento de imágenes opcional, extraer texto mediante Tesseract OCR,
y guardar los resultados en archivos `.docx` y `.txt`.

Funciones principales:
- `process_file`: función asincrónica que encapsula todo el flujo de procesamiento.

Este módulo es invocado desde la ruta POST `/upload` en main.py.
"""

from app.preprocess import preprocesar_imagen
from pathlib import Path
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from docx import Document
import uuid
import os

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
Path(OUTPUT_FOLDER).mkdir(exist_ok=True)

async def process_file(file, aplicar_preprocesamiento=True):
    """
    Procesa un archivo (PDF o imagen), extrae su contenido mediante OCR y lo guarda como .docx y .txt.

    El archivo se guarda temporalmente, se convierte a imágenes si es un PDF,
    y se aplica OCR con Tesseract a cada imagen. Opcionalmente se realiza preprocesamiento
    para mejorar la precisión del OCR. El resultado se guarda en dos formatos de texto.

    Esta función es invocada desde el endpoint `/upload` definido en `main.py`.

    Parámetros
    ----------
    file : UploadFile
        Archivo subido por el usuario (puede ser imagen o PDF). Se espera un objeto tipo FastAPI UploadFile.

    aplicar_preprocesamiento : bool, opcional
        Si es True, se aplica una rutina de preprocesamiento a las imágenes antes de ejecutar OCR. Por defecto es True.

    Retorna
    -------
    str
        Nombre base del archivo (sin extensión), que puede usarse para localizar los archivos generados (.docx y .txt)
        dentro del directorio de salida.
    """

    # Guardar archivo temporalmente
    file_path = Path(UPLOAD_FOLDER) / f"{uuid.uuid4()}_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Convertir PDF a imágenes o abrir imagen directamente
    if file.filename.endswith(".pdf"):
        images = convert_from_path(file_path)
    else:
        image = Image.open(file_path)
        images = [image]

    # Extraer texto con Tesseract
    full_text = ""
    for image in images:
        if aplicar_preprocesamiento:
            imagen_procesada = preprocesar_imagen(image)
        else:
            imagen_procesada = image
    
        custom_config = r'--oem 3 --psm 4'
        text = pytesseract.image_to_string(imagen_procesada, config=custom_config)
        full_text += text + "\n\n"

    # Guardar como .docx
    doc = Document()
    doc.add_paragraph(full_text)
    output_docx = Path(OUTPUT_FOLDER) / f"{file_path.stem}.docx"
    doc.save(output_docx)

    # Guardar como .txt
    output_txt = Path(OUTPUT_FOLDER) / f"{file_path.stem}.txt"
    with open(output_txt, "w", encoding="utf-8") as txt_file:
        txt_file.write(full_text)

    # Elegimos cuál devolver por ahora (vamos con .docx de momento)
    return file_path.stem  # devuelve solo el nombre base sin extensión