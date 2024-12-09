import cv2
import numpy as np


class ImagePreprocessor:
    @staticmethod
    def convert_to_gray(param_image):
        # 그레이스케일 변환
        return cv2.cvtColor(param_image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def blur_with_gaussian(param_image):
        blurred = cv2.GaussianBlur(param_image, (5, 5), 0)
        return blurred

    @staticmethod
    def convert_to_binary(
        param_image, threshold: float = 220, maximum_val: float = 255
    ):
        # 하얀색 테두리 검출을 위한 임계값 처리
        _, binary = cv2.threshold(
            param_image, threshold, maximum_val, cv2.THRESH_BINARY
        )
        return binary

    @staticmethod
    def detect_edges(param_image, threshold1: float = 30, threshold2: float = 150):
        # 엣지 검출
        return cv2.Canny(param_image, threshold1, threshold2, apertureSize=3)

    @staticmethod
    def apply_threshold(param_image, threshold=220):
        blurred = cv2.GaussianBlur(param_image, (5, 5), 0)
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
