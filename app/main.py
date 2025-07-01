# ... tus imports originales
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException, Response, Cookie

import json
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

from app.ocr import process_file
from app.database import init_db

app = FastAPI(title="OCR Pro API - Expert Edition")

# --- Definición de Rutas del Proyecto ---
APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent
TEMPLATES_DIR = APP_DIR / "templates"
STATIC_DIR = PROJECT_ROOT / "static"
UPLOADS_DIR = PROJECT_ROOT / "uploads"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
DIAGNOSTICS_DIR = PROJECT_ROOT / "diagnostics"

templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

UPLOADS_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)
DIAGNOSTICS_DIR.mkdir(exist_ok=True)

# Inicializar base de datos al arrancar la aplicación
try:
    init_db()
    print("✅ Base de datos inicializada correctamente")
except Exception as e:
    print(f"❌ Error al inicializar la base de datos: {e}")

# Health check endpoint para Render
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "OCR Pro API is running"}

# Función auxiliar para hashear contraseñas
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Obtener usuario actual desde la cookie
def get_current_user_id(request: Request):
    return request.cookies.get("user_id")

# Obtener información completa del usuario actual
def get_current_user(request: Request):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return None
    
    conn = sqlite3.connect(APP_DIR / "ocrapp.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {"id": user[0], "email": user[1]}
    return None

# Ruta principal
@app.get("/", response_class=HTMLResponse)
async def get_upload_form(request: Request):
    user = get_current_user(request)
    error = request.query_params.get("error")
    redirect_to = request.query_params.get("redirect_to")
    
    # Cargar presets del usuario si está logueado
    user_presets = []
    if user:
        conn = sqlite3.connect(APP_DIR / "ocrapp.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, config FROM presets WHERE user_id = ? ORDER BY name", (user["id"],))
        presets_data = cursor.fetchall()
        conn.close()
        
        user_presets = [
            {"id": preset[0], "name": preset[1], "config": json.loads(preset[2])}
            for preset in presets_data
        ]
    
    return templates.TemplateResponse("form.html", {
        "request": request,
        "user": user,
        "user_id": user["id"] if user else None,
        "user_presets": user_presets,
        "login_error": error,
        "redirect_to": redirect_to
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

        # Guardar resultados en una cookie temporal para permitir redirección después del login
        results_data = {
            "nombre_base": nombre_base,
            "diagnostic_image": diagnostic_image_path,
            "opciones": opciones_preproceso
        }
        
        response = templates.TemplateResponse("resultados.html", {
            "request": request,
            "nombre_base": nombre_base,
            "diagnostic_image": diagnostic_image_path,
            "opciones": opciones_preproceso,
            "user": get_current_user(request),
            "user_id": get_current_user_id(request)
        })
        
        # Guardar los resultados en una cookie temporal (válida por 1 hora)
        response.set_cookie(
            key="temp_results",
            value=json.dumps(results_data),
            max_age=3600,  # 1 hora
            httponly=True
        )
        
        return response
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
    error = request.query_params.get("error")
    redirect_to = request.query_params.get("redirect_to")
    return templates.TemplateResponse("register.html", {
        "request": request,
        "error": error,
        "redirect_to": redirect_to
    })

# Ruta GET de login
@app.get("/login", response_class=HTMLResponse)
def show_login_form(request: Request):
    error = request.query_params.get("error")
    redirect_to = request.query_params.get("redirect_to")
    return templates.TemplateResponse("login.html", {
        "request": request,
        "login_error": error,
        "redirect_to": redirect_to
    })

# Ruta POST de registro
@app.post("/register")
def register(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    redirect_to: str = Form(None)
):
    if password != confirm_password:
        error_url = "/register?error=1"
        if redirect_to:
            error_url = f"/register?error=1&redirect_to={redirect_to}"
        return RedirectResponse(url=error_url, status_code=303)

    hashed_pw = hash_password(password)
    conn = sqlite3.connect(APP_DIR / "ocrapp.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_pw))
        conn.commit()
        user_id = cursor.lastrowid
        
        # Determinar URL de redirección
        redirect_url = "/"
        if redirect_to:
            # Validar que la redirección sea segura (misma aplicación)
            if redirect_to.startswith("/") and not redirect_to.startswith("//"):
                redirect_url = redirect_to
        
        response = RedirectResponse(url=redirect_url, status_code=302)
        response.set_cookie(key="user_id", value=str(user_id))
        return response
    except sqlite3.IntegrityError:
        error_url = "/register?error=2"
        if redirect_to:
            error_url = f"/register?error=2&redirect_to={redirect_to}"
        return RedirectResponse(url=error_url, status_code=303)
    finally:
        conn.close()

# Ruta de login corregida con redirección a / y mensaje de error
@app.post("/login")
def login(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    redirect_to: str = Form(None)
):
    hashed_pw = hash_password(password)
    conn = sqlite3.connect(APP_DIR / "ocrapp.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ? AND password = ?", (email, hashed_pw))
    user = cursor.fetchone()
    conn.close()
    if user:
        # Determinar URL de redirección
        redirect_url = "/"
        if redirect_to:
            # Validar que la redirección sea segura (misma aplicación)
            if redirect_to.startswith("/") and not redirect_to.startswith("//"):
                redirect_url = redirect_to
        
        response = RedirectResponse(url=redirect_url, status_code=302)
        response.set_cookie(key="user_id", value=str(user[0]))
        return response
    else:
        # Mantener parámetro de redirección en caso de error
        error_url = "/?error=1"
        if redirect_to:
            error_url = f"/?error=1&redirect_to={redirect_to}"
        return RedirectResponse(url=error_url, status_code=302)

# Ruta de logout
@app.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("user_id")
    return response

# Ruta GET para recuperar contraseña - paso 1 (pedir email)
@app.get("/forgot-password", response_class=HTMLResponse)
def show_forgot_password_form(request: Request):
    error = request.query_params.get("error")
    return templates.TemplateResponse("forgot_password.html", {
        "request": request,
        "error": error
    })

# Ruta POST para verificar email y mostrar presets
@app.post("/forgot-password")
def verify_email_for_recovery(
    request: Request,
    email: str = Form(...)
):
    # Verificar si el email está bloqueado
    is_blocked, time_remaining = is_email_blocked_for_recovery(email)
    if is_blocked:
        return RedirectResponse(url=f"/forgot-password?error=5&time={time_remaining}", status_code=303)
    
    conn = sqlite3.connect(APP_DIR / "ocrapp.db")
    cursor = conn.cursor()
    
    # Verificar si el email existe
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return RedirectResponse(url="/forgot-password?error=1", status_code=303)
    
    user_id = user[0]
    
    # Obtener presets del usuario
    cursor.execute("SELECT id, name FROM presets WHERE user_id = ?", (user_id,))
    user_presets = cursor.fetchall()
    
    if not user_presets:
        conn.close()
        return RedirectResponse(url="/forgot-password?error=2", status_code=303)
    
    # Mezclar presets del usuario con otros aleatorios para mayor seguridad
    import random
    
    # Seleccionar un preset correcto del usuario
    correct_preset = random.choice(user_presets)
    
    # Agregar algunos presets más del usuario si tiene varios (máximo 2 adicionales)
    user_presets_sample = [p for p in user_presets if p[0] != correct_preset[0]]
    additional_user_presets = random.sample(user_presets_sample, min(2, len(user_presets_sample)))
    
    # Obtener presets de otros usuarios para confundir
    needed_others = max(2, 5 - len(additional_user_presets) - 1)  # Al menos 2, hasta completar 5 total
    cursor.execute("SELECT id, name FROM presets WHERE user_id != ? ORDER BY RANDOM() LIMIT ?", (user_id, needed_others))
    other_presets = cursor.fetchall()
    
    conn.close()
    
    # Combinar todos los presets
    all_presets = [correct_preset] + additional_user_presets + list(other_presets)
    
    # Asegurar que tengamos al menos 5 opciones (rellenar con nombres genéricos si es necesario)
    while len(all_presets) < 5:
        fake_names = [
            "Documento general",
            "Configuración estándar", 
            "Preset básico",
            "Ajustes por defecto",
            "Modo automático",
            "Configuración rápida",
            "Preset universal"
        ]
        fake_name = random.choice([name for name in fake_names if name not in [p[1] for p in all_presets]])
        all_presets.append((9999 + len(all_presets), fake_name))  # ID imposible para presets falsos
    
    # Limitar a máximo 7 opciones para no sobrecargar al usuario
    if len(all_presets) > 7:
        # Mantener el preset correcto y mezclar el resto
        other_options = [p for p in all_presets if p[0] != correct_preset[0]]
        other_options = random.sample(other_options, 6)
        all_presets = [correct_preset] + other_options
    
    # Mezclar todas las opciones
    random.shuffle(all_presets)
    
    return templates.TemplateResponse("password_recovery_challenge.html", {
        "request": request,
        "email": email,
        "presets": all_presets,
        "correct_preset_id": correct_preset[0]
    })

# Ruta POST para verificar preset seleccionado
@app.post("/verify-preset")
def verify_preset_selection(
    request: Request,
    email: str = Form(...),
    selected_preset_id: int = Form(...),
    correct_preset_id: int = Form(...)
):
    # Verificar si el email está bloqueado antes de procesar
    is_blocked, time_remaining = is_email_blocked_for_recovery(email)
    if is_blocked:
        return RedirectResponse(url=f"/forgot-password?error=5&time={time_remaining}", status_code=303)
    
    if selected_preset_id != correct_preset_id:
        # Registrar el intento fallido y bloquear por 10 minutos
        record_failed_recovery_attempt(email)
        return RedirectResponse(url="/forgot-password?error=3", status_code=303)
    
    # Si la verificación es exitosa, limpiar cualquier bloqueo previo
    clear_recovery_attempts(email)
    
    return templates.TemplateResponse("reset_password.html", {
        "request": request,
        "email": email,
        "verified": True
    })

# Ruta POST para cambiar la contraseña
@app.post("/reset-password")
def reset_password(
    email: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...)
):
    if new_password != confirm_password:
        return RedirectResponse(url="/forgot-password?error=4", status_code=303)
    
    hashed_pw = hash_password(new_password)
    conn = sqlite3.connect(APP_DIR / "ocrapp.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE email = ?", (hashed_pw, email))
    conn.commit()
    conn.close()
    
    return RedirectResponse(url="/?success=1", status_code=302)

# Ruta para guardar preset
@app.post("/guardar_preset")
async def guardar_preset(
    request: Request,
    preset_name: str = Form(...),
    opciones: str = Form(...),
    nombre_base: str = Form(...),
    diagnostic_image: str = Form(...)
):
    user_id = get_current_user_id(request)
    if not user_id:
        return RedirectResponse(url="/", status_code=302)

    import json
    conn = sqlite3.connect(APP_DIR / "ocrapp.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO presets (user_id, name, config) VALUES (?, ?, ?)",
        (user_id, preset_name, opciones)
    )
    conn.commit()
    conn.close()

    return templates.TemplateResponse("resultados.html", {
        "request": request,
        "nombre_base": nombre_base,
        "diagnostic_image": diagnostic_image,
        "opciones": json.loads(opciones),
        "user": get_current_user(request),
        "user_id": user_id,
        "preset_saved": preset_name  # Indicar que se guardó un preset
    })

# Ruta para mostrar resultados guardados (después del login)
@app.get("/resultados", response_class=HTMLResponse)
def show_saved_results(request: Request):
    user = get_current_user(request)
    
    # Obtener los resultados guardados de la cookie temporal
    temp_results = request.cookies.get("temp_results")
    if not temp_results:
        # Si no hay resultados guardados, redirigir al inicio
        return RedirectResponse(url="/", status_code=302)
    
    try:
        results_data = json.loads(temp_results)
        
        response = templates.TemplateResponse("resultados.html", {
            "request": request,
            "nombre_base": results_data["nombre_base"],
            "diagnostic_image": results_data["diagnostic_image"],
            "opciones": results_data["opciones"],
            "user": user,
            "user_id": user["id"] if user else None
        })
        
        return response
        
    except (json.JSONDecodeError, KeyError):
        # Si hay error al decodificar, redirigir al inicio
        return RedirectResponse(url="/", status_code=302)

# Funciones para el sistema de bloqueo de recuperación de contraseña
def is_email_blocked_for_recovery(email: str) -> tuple[bool, str]:
    """
    Verifica si un email está bloqueado para recuperación de contraseña.
    Retorna: (is_blocked, time_remaining_message)
    """
    conn = sqlite3.connect(APP_DIR / "ocrapp.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT blocked_until FROM password_recovery_blocks 
        WHERE email = ? ORDER BY id DESC LIMIT 1
    """, (email,))
    result = cursor.fetchone()
    conn.close()
    
    if not result or not result[0]:
        return False, ""
    
    blocked_until = datetime.fromisoformat(result[0])
    now = datetime.now()
    
    if now < blocked_until:
        time_remaining = blocked_until - now
        minutes_remaining = int(time_remaining.total_seconds() / 60) + 1
        return True, f"{minutes_remaining} minutos"
    
    return False, ""

def record_failed_recovery_attempt(email: str):
    """
    Registra un intento fallido de recuperación de contraseña.
    Si es el primer fallo, bloquea por 10 minutos.
    """
    conn = sqlite3.connect(APP_DIR / "ocrapp.db")
    cursor = conn.cursor()
    
    now = datetime.now()
    blocked_until = now + timedelta(minutes=10)
    
    # Verificar si ya existe un registro para este email
    cursor.execute("""
        SELECT id, failed_attempts FROM password_recovery_blocks 
        WHERE email = ? ORDER BY id DESC LIMIT 1
    """, (email,))
    result = cursor.fetchone()
    
    if result:
        # Actualizar el registro existente
        new_attempts = result[1] + 1
        cursor.execute("""
            UPDATE password_recovery_blocks 
            SET failed_attempts = ?, blocked_until = ?, updated_at = ?
            WHERE id = ?
        """, (new_attempts, blocked_until.isoformat(), now.isoformat(), result[0]))
    else:
        # Crear un nuevo registro
        cursor.execute("""
            INSERT INTO password_recovery_blocks 
            (email, failed_attempts, blocked_until, updated_at)
            VALUES (?, 1, ?, ?)
        """, (email, blocked_until.isoformat(), now.isoformat()))
    
    conn.commit()
    conn.close()

def clear_recovery_attempts(email: str):
    """
    Limpia los intentos de recuperación para un email (cuando tiene éxito).
    """
    conn = sqlite3.connect(APP_DIR / "ocrapp.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE password_recovery_blocks 
        SET failed_attempts = 0, blocked_until = NULL
        WHERE email = ?
    """, (email,))
    
    conn.commit()
    conn.close()