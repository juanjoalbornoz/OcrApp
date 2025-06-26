# ... tus imports originales
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException, Response, Cookie

import sqlite3
import hashlib
from pathlib import Path

from app.ocr import process_file

app = FastAPI(title="OCR Pro API - Expert Edition")

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

# Función auxiliar para hashear contraseñas
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Obtener usuario actual desde la cookie
def get_current_user_id(request: Request):
    return request.cookies.get("user_id")

# Ruta principal
@app.get("/", response_class=HTMLResponse)
async def get_upload_form(request: Request):
    user_id = get_current_user_id(request)
    error = request.query_params.get("error")
    return templates.TemplateResponse("form.html", {
        "request": request,
        "user_id": user_id,
        "login_error": error
    })

# Ruta para subir archivo
@app.post("/upload", response_class=HTMLResponse)
async def handle_file_upload(
    request: Request,
    file: UploadFile = File(...),
    grayscale: bool = Form(False),
    invert_colors: bool = Form(False),
    brillo: int = Form(0),
    contraste: float = Form(1.0),
    hist_equalization: bool = Form(False),
    clahe_clip_limit: float = Form(2.0),
    gaussian_blur: bool = Form(False),
    gaussian_kernel: int = Form(3),
    median_blur: bool = Form(False),
    median_kernel: int = Form(3),
    deskew: bool = Form(False),
    rotation: int = Form(0),
    canny_edge: bool = Form(False),
    canny_thresh1: int = Form(100),
    canny_thresh2: int = Form(200),
    binarization: bool = Form(False),
    binarization_method: str = Form("adaptive"),
    morphology: bool = Form(False),
    morph_op: str = Form("erosion"),
    morph_iter: int = Form(1)
):
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

        return templates.TemplateResponse("resultados.html", {
            "request": request,
            "nombre_base": nombre_base,
            "diagnostic_image": diagnostic_image_path,
            "opciones": opciones_preproceso
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")

# Ruta para descargar archivos generados
@app.get("/descargar/{nombre_archivo}")
async def download_generated_file(nombre_archivo: str):
    if nombre_archivo.endswith(('.docx', '.txt')):
        ruta = OUTPUTS_DIR / nombre_archivo
    elif nombre_archivo.endswith(('.png', '.jpg', '.jpeg')):
        ruta = DIAGNOSTICS_DIR / nombre_archivo
    else:
        raise HTTPException(status_code=400, detail="Tipo de archivo no válido para descarga.")

    if not ruta.is_file():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    return FileResponse(path=ruta, media_type="application/octet-stream", filename=nombre_archivo)

# Ruta GET de registro
@app.get("/register", response_class=HTMLResponse)
def show_register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# Ruta POST de registro
@app.post("/register")
def register(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    if password != confirm_password:
        return RedirectResponse(url="/register?error=1", status_code=303)

    hashed_pw = hash_password(password)
    conn = sqlite3.connect(APP_DIR / "ocrapp.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_pw))
        conn.commit()
        user_id = cursor.lastrowid
        response = RedirectResponse(url="/", status_code=302)
        response.set_cookie(key="user_id", value=str(user_id))
        return response
    except sqlite3.IntegrityError:
        return RedirectResponse(url="/register?error=2", status_code=303)
    finally:
        conn.close()

# Ruta de login corregida con redirección a / y mensaje de error
@app.post("/login")
def login(
    response: Response,
    email: str = Form(...),
    password: str = Form(...)
):
    hashed_pw = hash_password(password)
    conn = sqlite3.connect(APP_DIR / "ocrapp.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ? AND password = ?", (email, hashed_pw))
    user = cursor.fetchone()
    conn.close()
    if user:
        response = RedirectResponse(url="/", status_code=302)
        response.set_cookie(key="user_id", value=str(user[0]))
        return response
    else:
        return RedirectResponse(url="/?error=1", status_code=302)

# Ruta de logout
@app.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("user_id")
    return response