from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from pathlib import Path
import os

from app.ocr import process_file

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/upload")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    preprocesar: bool = Form(False)
):
    nombre_base = await process_file(file, preprocesar)
    return templates.TemplateResponse(
        "resultados.html",
        {"request": request, "nombre_base": nombre_base}
    )

from fastapi.responses import FileResponse

@app.get("/descargar/{nombre_archivo}")
async def descargar_archivo(nombre_archivo: str):
    ruta = Path("outputs") / nombre_archivo
    if ruta.exists():
        return FileResponse(ruta, media_type="application/octet-stream", filename=nombre_archivo)
    return {"error": "Archivo no encontrado"}