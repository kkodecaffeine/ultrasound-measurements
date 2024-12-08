import cv2
import numpy as np


class ImagePreprocessor:
    @staticmethod
    def convert_to_gray(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def apply_threshold(gray_image, threshold=220):
        blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)

        return thresh

    @staticmethod
    def preprocess_image(image):
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        gray = (
            cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        )
        gray = clahe.apply(gray)
        filtered = cv2.bilateralFilter(gray, 11, 17, 17)
        edges = cv2.Canny(filtered, 30, 150)
        kernel = np.ones((3, 3), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)

        return edges
