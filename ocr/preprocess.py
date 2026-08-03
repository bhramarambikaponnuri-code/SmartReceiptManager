import cv2
import numpy as np


class ImagePreprocessor:

    @staticmethod
    def preprocess(image):

        # -------------------------
        # Resize large images
        # -------------------------

        h, w = image.shape[:2]

        max_width = 1500

        if w > max_width:

            scale = max_width / w

            image = cv2.resize(
                image,
                None,
                fx=scale,
                fy=scale,
                interpolation=cv2.INTER_AREA
            )

        # -------------------------
        # Convert to Grayscale
        # -------------------------

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        # -------------------------
        # Increase Contrast (CLAHE)
        # -------------------------

        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8)
        )

        gray = clahe.apply(gray)

        # -------------------------
        # Remove Noise
        # -------------------------

        gray = cv2.fastNlMeansDenoising(
            gray,
            None,
            h=10
        )

        # -------------------------
        # Adaptive Threshold
        # -------------------------

        processed = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            10
        )

        # -------------------------
        # Remove tiny dots
        # -------------------------

        kernel = np.ones((2, 2), np.uint8)

        processed = cv2.morphologyEx(
            processed,
            cv2.MORPH_OPEN,
            kernel
        )

        return processed