import cv2
import numpy as np
from PIL import Image
from typing import Dict, Any


class ImagePreprocessor:
    def __init__(self, options: Dict[str, Any]):
        self.options = options
        self.image = None

    def process(self, pil_image: Image.Image) -> Image.Image:
        self.image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        if "rotation" in self.options:
            self.apply_rotation(self.options["rotation"])
        if self.options.get("deskew", False):
            self.correct_skew()
        if "brillo" in self.options or "contraste" in self.options:
            brillo = self.options.get("brillo", 0)
            contraste = self.options.get("contraste", 1.0)
            self.adjust_brightness_contrast(brillo, contraste)
        if self.options.get("invert_colors", False):
            self.invert_colors()

        self.convert_to_grayscale()

        if self.options.get("hist_equalization", False):
            clip = self.options.get("clahe_clip_limit", 2.0)
            self.equalize_histogram(clip)
        if self.options.get("gaussian_blur", False):
            kernel = self.options.get("gaussian_kernel", 3)
            self.apply_gaussian_blur(kernel)
        if self.options.get("median_blur", False):
            kernel = self.options.get("median_kernel", 3)
            self.apply_median_blur(kernel)
        if self.options.get("canny_edge", False):
            t1 = self.options.get("canny_thresh1", 100)
            t2 = self.options.get("canny_thresh2", 200)
            self.detect_edges(t1, t2)
        if self.options.get("binarization", False):
            method = self.options.get("binarization_method", "adaptive")
            self.binarize(method)
        if self.options.get("morphology", False):
            op = self.options.get("morph_op", "erosion")
            it = self.options.get("morph_iter", 1)
            self.apply_morphology(op, it)

        return self.to_pil()

    def apply_rotation(self, angle: float):
        h, w = self.image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        self.image = cv2.warpAffine(self.image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    def correct_skew(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        angle = self._compute_skew_angle(gray)
        if angle != 0:
            h, w = self.image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            self.image = cv2.warpAffine(self.image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    def adjust_brightness_contrast(self, brillo: int, contraste: float):
        self.image = cv2.convertScaleAbs(self.image, alpha=contraste, beta=brillo)

    def invert_colors(self):
        self.image = cv2.bitwise_not(self.image)

    def convert_to_grayscale(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def equalize_histogram(self, clip_limit: float):
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
        self.image = clahe.apply(self.image)

    def apply_gaussian_blur(self, kernel_size: int):
        self.image = cv2.GaussianBlur(self.image, (kernel_size, kernel_size), 0)

    def apply_median_blur(self, kernel_size: int):
        self.image = cv2.medianBlur(self.image, kernel_size)

    def detect_edges(self, thresh1: int, thresh2: int):
        self.image = cv2.Canny(self.image, thresh1, thresh2)

    def binarize(self, method: str):
        if method == "adaptive":
            self.image = cv2.adaptiveThreshold(
                self.image, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2
            )
        elif method == "otsu":
            _, self.image = cv2.threshold(self.image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    def apply_morphology(self, op_name: str, iterations: int):
        kernel = np.ones((3, 3), np.uint8)
        if op_name == "erosion":
            self.image = cv2.erode(self.image, kernel, iterations=iterations)
        elif op_name == "dilation":
            self.image = cv2.dilate(self.image, kernel, iterations=iterations)
        elif op_name == "opening":
            self.image = cv2.morphologyEx(self.image, cv2.MORPH_OPEN, kernel, iterations=iterations)
        elif op_name == "closing":
            self.image = cv2.morphologyEx(self.image, cv2.MORPH_CLOSE, kernel, iterations=iterations)

    def _compute_skew_angle(self, gray_image: np.ndarray) -> float:
        inverted = cv2.bitwise_not(gray_image)
        coords = np.column_stack(np.where(inverted > 0))
        if coords.shape[0] < 50:
            return 0.0

        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        return angle if abs(angle) > 0.5 else 0.0

    def to_pil(self) -> Image.Image:
        if len(self.image.shape) == 2:
            return Image.fromarray(self.image)
        else:
            return Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
