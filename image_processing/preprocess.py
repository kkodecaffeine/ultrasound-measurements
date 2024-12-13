import cv2
import numpy as np
import pytesseract


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
    def blur_text_regions(param_image, param_gray_image):
        # 텍스트 영역을 블러 처리하는 함수
        boxes = pytesseract.image_to_boxes(param_gray_image)

        # 각 검출된 텍스트 영역을 블러 처리
        for b in boxes.splitlines():
            b = b.split()
            x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
            y = param_image.shape[0] - y  # OpenCV와 Tesseract 의 y 좌표는 반대 방향
            h = param_image.shape[0] - h

            # 블러 처리
            roi = param_image[h:y, x:w]
            roi = cv2.GaussianBlur(roi, (25, 25), 50)
            param_image[h:y, x:w] = roi

        return param_image

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
        edges = cv2.Canny(filtered, 30, 180)
        kernel = np.ones((3, 3), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)

        return edges
