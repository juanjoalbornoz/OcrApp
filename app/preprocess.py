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