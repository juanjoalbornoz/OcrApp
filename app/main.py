import os
from pathlib import Path
from fastapi import (
    FastAPI, File, UploadFile, Form, Request,
    HTTPException
)
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

from app.ocr import process_file

app = FastAPI(
    title="OCR Pro API - Expert Edition",
)

# --- Definición de Rutas del Proyecto ---
APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent
TEMPLATES_DIR = APP_DIR / "templates"
UPLOADS_DIR = PROJECT_ROOT / "uploads"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
DIAGNOSTICS_DIR = PROJECT_ROOT / "diagnostics"

templates = Jinja2Templates(directory=TEMPLATES_DIR)

UPLOADS_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)
DIAGNOSTICS_DIR.mkdir(exist_ok=True)

# --- Rutas de la Aplicación ---
@app.get("/", response_class=HTMLResponse)
async def get_upload_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
async def handle_file_upload(
    request: Request,
    file: UploadFile = File(...),
    # --- Parámetros del Formulario Experto ---
    # Color y Contraste
    grayscale: bool = Form(False),
    invert_colors: bool = Form(False),
    brillo: int = Form(0),
    contraste: float = Form(1.0),
    hist_equalization: bool = Form(False),
    clahe_clip_limit: float = Form(2.0),
    # Filtros y Suavizado
    gaussian_blur: bool = Form(False),
    gaussian_kernel: int = Form(3),
    median_blur: bool = Form(False),
    median_kernel: int = Form(3),
    # Transformaciones Geométricas
    deskew: bool = Form(False),
    rotation: int = Form(0),
    # Detección de Bordes
    canny_edge: bool = Form(False),
    canny_thresh1: int = Form(100),
    canny_thresh2: int = Form(200),
    # Binarización y Morfología
    binarization: bool = Form(False),
    binarization_method: str = Form("adaptive"),
    morphology: bool = Form(False),
    morph_op: str = Form("erosion"),
    morph_iter: int = Form(1)
):
    """
    Endpoint que recibe el archivo y todos los parámetros del formulario experto.
    """
    # Agrupar todas las opciones en un único diccionario
    opciones_preproceso = {
        "grayscale": grayscale, "invert_colors": invert_colors, "brillo": brillo,
        "contraste": contraste, "hist_equalization": hist_equalization, 
        "clahe_clip_limit": clahe_clip_limit, "gaussian_blur": gaussian_blur,
        "gaussian_kernel": gaussian_kernel, "median_blur": median_blur, 
        "median_kernel": median_kernel, "deskew": deskew, "rotation": rotation,
        "canny_edge": canny_edge, "canny_thresh1": canny_thresh1, 
        "canny_thresh2": canny_thresh2, "binarization": binarization,
        "binarization_method": binarization_method, "morphology": morphology,
        "morph_op": morph_op, "morph_iter": morph_iter
    }

    try:
        nombre_base, diagnostic_image_path = await process_file(
            file=file,
            opciones_preproceso=opciones_preproceso,
            upload_folder=UPLOADS_DIR,
            output_folder=OUTPUTS_DIR,
            diagnostic_folder=DIAGNOSTICS_DIR
        )
        
        contexto_resultados = {
            "request": request,
            "nombre_base": nombre_base,
            "diagnostic_image": diagnostic_image_path,
            "opciones": opciones_preproceso
        }
        return templates.TemplateResponse("resultados.html", contexto_resultados)

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ocurrió un error al procesar el archivo: {str(e)}")


@app.get("/descargar/{nombre_archivo}")
async def download_generated_file(nombre_archivo: str):
    if nombre_archivo.endswith(('.docx', '.txt')):
        ruta = OUTPUTS_DIR / nombre_archivo
    elif nombre_archivo.endswith(('.png', '.jpg', '.jpeg')):
        ruta = DIAGNOSTICS_DIR / nombre_archivo
    else:
        raise HTTPException(status_code=400, detail="Tipo de archivo no válido para descarga.")

    if not ruta.is_file():
        raise HTTPException(status_code=404, detail=f"Archivo no encontrado: {ruta}")
    
    return FileResponse(path=ruta, media_type="application/octet-stream", filename=nombre_archivo)
