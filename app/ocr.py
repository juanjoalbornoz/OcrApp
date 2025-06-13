import uuid
import io
from pathlib import Path
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
from docx import Document
from fastapi import UploadFile

from app.preprocess import ImagePreprocessor

async def process_file(
    file: UploadFile,
    opciones_preproceso: dict,
    upload_folder: Path,
    output_folder: Path,
    diagnostic_folder: Path
):
    nombre_base = f"{uuid.uuid4()}_{Path(file.filename).stem}"
    file_path = upload_folder / f"{nombre_base}{Path(file.filename).suffix}"
    
    file_content = await file.read()
    file_path.write_bytes(file_content)

    # --- Convertir archivo a imágenes ---
    images = []
    if file.filename.lower().endswith(".pdf"):
        try:
            images = convert_from_path(file_path, dpi=300)
        except Exception as e:
            print(f"Error al convertir PDF. Asegúrate de que Poppler esté en el PATH. Error: {e}")
            raise ValueError("Error al procesar el PDF. Poppler podría no estar instalado.")
    else:
        image = Image.open(io.BytesIO(file_content)).convert("RGB")
        images = [image]

    # --- Inicializar salida ---
    full_text = ""
    diagnostic_image_path = None
    custom_config = r'--oem 3 --psm 6 -l spa'

    # --- Procesar cada imagen ---
    for i, image in enumerate(images):
        print(f"Procesando página/imagen {i + 1}...")

        # Usar el preprocesador con clase
        preprocessor = ImagePreprocessor(opciones_preproceso)
        imagen_procesada = preprocessor.process(image)

        # Guardar imagen diagnóstica solo para la primera
        if i == 0:
            diagnostic_file_name = f"{nombre_base}_diagnostic.png"
            diagnostic_path_full = diagnostic_folder / diagnostic_file_name
            imagen_procesada.save(diagnostic_path_full)
            diagnostic_image_path = diagnostic_file_name

        try:
            text = pytesseract.image_to_string(imagen_procesada, config=custom_config)
            full_text += text.strip() + "\n\n"
        except pytesseract.TesseractError as e:
            print(f"Error de Tesseract en la página {i+1}: {e}")
            full_text += f"[Error al procesar página {i+1}]\n\n"

    # --- Guardar salida .txt y .docx ---
    output_txt = output_folder / f"{nombre_base}.txt"
    output_txt.write_text(full_text, encoding="utf-8")

    doc = Document()
    doc.add_paragraph(full_text)
    output_docx = output_folder / f"{nombre_base}.docx"
    doc.save(output_docx)
    
    file_path.unlink()

    return nombre_base, diagnostic_image_path
