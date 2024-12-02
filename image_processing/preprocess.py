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
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        gray = clahe.apply(gray)
        filtered = cv2.bilateralFilter(gray, 11, 17, 17)
        edges = cv2.Canny(filtered, 30, 150)
        kernel = np.ones((3,3), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)

        return edges

# def enhance_contrast(image):
#     """CLAHE를 사용한 이미지 대비 강화."""
#     # 컬러 이미지를 그레이스케일로 변환
#     # if len(image.shape) == 3:  # 컬러 이미지인 경우
#     #     image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     #
#     # # uint8 데이터 타입으로 변환
#     # if image.dtype != np.uint8:
#     #     image = cv2.convertScaleAbs(image)
#
#     # CLAHE 적용
#     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
#     return clahe.apply(image)
#
# def apply_gaussian_blur(image):
#     """가우시안 블러 적용 (노이즈 제거)."""
#     return cv2.GaussianBlur(image, (9, 9), 2)
#
# def binarize_image(image, threshold=150):
#     """이미지를 이진화."""
#     _, binary = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
#     return binary
