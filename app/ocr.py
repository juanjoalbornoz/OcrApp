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

async def process_file(file):
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
        text = pytesseract.image_to_string(image)
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