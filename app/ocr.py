from pathlib import Path
from pdf2image import convert_from_path
import pytesseract
import cv2
import numpy as np
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

    if file.filename.endswith(".pdf"):
        images = convert_from_path(file_path)
    else:
        image = Image.open(file_path)
        images = [image]

    # OCR
    full_text = ""
    for image in images:
        text = pytesseract.image_to_string(image)
        full_text += text + "\n\n"

    # Guardar como docx
    doc = Document()
    doc.add_paragraph(full_text)
    output_path = Path(OUTPUT_FOLDER) / f"{file_path.stem}.docx"
    doc.save(output_path)

    return output_path