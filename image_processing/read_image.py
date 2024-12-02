import cv2

import cv2


class ImageReader:
    @staticmethod
    def read(image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Image not found at path: {image_path}")
        return image

# def read_image(image_path, convert_to_gray=True):
#     """
#     이미지를 읽고 필요하면 그레이스케일로 변환
#
#     Args:
#         image_path (str): 이미지 경로
#         convert_to_gray (bool): True (그레이스케일로 변환)
#
#     Returns:
#         numpy.ndarray: 읽어들인 이미지
#
#     Raises:
#         FileNotFoundError: 이미지 파일이 없을 경우 예외 발생
#     """
#     image = cv2.imread(image_path)
#     if image is None:
#         raise FileNotFoundError(f"Image not found at path: {image_path}")
#
#     if convert_to_gray:
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#     return image
#
# def read_image_in_grayscale(image_path):
#     """
#     이미지를 그레이스케일로 바로 읽기
#
#     Args:
#         image_path (str): 이미지 경로
#
#     Returns:
#         numpy.ndarray: 그레이스케일로 읽은 이미지
#
#     Raises:
#         FileNotFoundError: 이미지 파일이 없을 경우 예외 발생
#     """
#     image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#     if image is None:
#         raise FileNotFoundError(f"Image not found at path: {image_path}")
#
#     return image
