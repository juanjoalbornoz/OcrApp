# Imagen base de Python (actualizada para mayor compatibilidad)
FROM python:3.11-slim

# Evitar prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema necesarias para Tesseract y Poppler
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-spa \
    poppler-utils \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Crear y moverse al directorio de la app
WORKDIR /app

# Copiar archivo de dependencias primero para aprovechar caché
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código fuente
COPY . .

# Crear directorios necesarios
RUN mkdir -p uploads outputs diagnostics

# Exponer el puerto que usará la app
EXPOSE 10000

# Comando para ejecutar la aplicación con Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
