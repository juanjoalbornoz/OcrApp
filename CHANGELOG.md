# 📓 Changelog

Todos los cambios relevantes de este proyecto se documentan acá.

---

## [1.3.0] - 2025-05-16
### ✨ Agregado
- Configuración Docker (`Dockerfile`) para contenerizar OcrAPP
- Archivo `render.yaml` para despliegue automático en Render
- Configuración de subdominio personalizado: `ocrapp.data-bi.ar`

### 🚀 Despliegue
- OcrAPP ahora está online con FastAPI corriendo desde un contenedor con soporte completo para OCR en la nube

---

## [1.2.0] - 2025-05-16
### ✨ Agregado
- Checkbox en la interfaz para activar o desactivar el preprocesamiento de imagen
- Mejora del preprocesamiento: aumento de contraste, binarización con Otsu y reducción de ruido
- Cambio del parámetro Tesseract a `--psm 4` para mejor segmentación de texto
- Actualización del README con tabla comparativa sobre cuándo aplicar mejoras

---

## [1.1.0] - 2025-05-16
### ✨ Agregado
- Funcionalidad para exportar el texto también en formato `.txt`
- Pantalla intermedia luego del procesamiento con botones de descarga
- Estilos CSS para mejorar la experiencia del usuario

---

## [1.0.0] - 2025-05-15
### 🚀 Creado
- Versión inicial de la app OCR
- Subida de imagen o PDF escaneado
- Extracción de texto con Tesseract OCR
- Generación automática de documento `.docx`
- Interfaz HTML básica
