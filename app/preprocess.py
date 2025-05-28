"""
Módulo de preprocesamiento de imágenes para OCR u otras tareas de visión por computadora.

Funciones:
----------
preprocesar_imagen(pil_image):
    Aplica una serie de transformaciones sobre una imagen en formato PIL para mejorar
    su calidad y facilitar el reconocimiento óptico de caracteres (OCR) u otras tareas
    de análisis de imagen.

    El procesamiento incluye:
    - Conversión a escala de grises (si es RGB).
    - Aumento de contraste mediante ecualización del histograma.
    - Binarización con el umbral de Otsu.
    - Reducción de ruido usando filtro de mediana.

Parámetros
----------
pil_image : PIL.Image
    Imagen de entrada en formato PIL.

Retorna
-------
PIL.Image
    Imagen procesada, binarizada y sin ruido, en formato PIL.
"""

import cv2
import numpy as np
from PIL import Image

def preprocesar_imagen(pil_image):
    # Convertir PIL a NumPy
    imagen = np.array(pil_image)

    # Convertir a escala de grises si tiene más de 2 dimensiones (RGB)
    if len(imagen.shape) == 3:
        gris = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
    else:
        gris = imagen

    # Aumentar contraste con ecualización del histograma
    alto_contraste = cv2.equalizeHist(gris)

    # Binarización con Otsu (¡ojo que devuelve 2 valores!)
    _, binaria = cv2.threshold(
        alto_contraste, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # Quitar ruido con mediana
    sin_ruido = cv2.medianBlur(binaria, 3)

    # Volver a PIL
    imagen_final = Image.fromarray(sin_ruido)

    return imagen_final