import cv2
import numpy as np

class ScaleCalculator:
    @staticmethod
    def calculate_distance(point1, point2):
        return np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

    @staticmethod
    def measure_bpd(image):
        result = image.copy()
        from .contour_analysis import ContourAnalyzer

        top_point, bottom_point = ContourAnalyzer.find_vertical_skull_boundaries(image)

        if top_point is not None and bottom_point is not None:
        # 거리 계산
            distance = np.sqrt((bottom_point[0] - top_point[0])**2 + (bottom_point[1] - top_point[1])**2)

            # 결과 시각화
            cv2.line(result, tuple(top_point), tuple(bottom_point), (0, 0, 255), 2)
            cv2.circle(result, tuple(top_point), 3, (0, 255, 0), -1)
            cv2.circle(result, tuple(bottom_point), 3, (0, 255, 0), -1)

            # 거리 표시
            mid_point = ((top_point[0] + bottom_point[0])//2, (top_point[1] + bottom_point[1])//2)
            cv2.putText(result, f'BPD: {distance:.1f}px',
                            (mid_point[0]-60, mid_point[1]-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            return result, distance

        return result, None


# def measure_scalebar_length(image):
#     # 이미지가 BGR인지 확인 후 그레이스케일로 변환
#     if len(image.shape) == 3:
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     else:
#         gray = image
#
#     # 이진화 처리
#     _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
#
#     # 윤곽선 검출
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
#     max_height = 0
#     scalebar_contour = None
#
#     for contour in contours:
#         x, y, w, h = cv2.boundingRect(contour)
#         aspect_ratio = h / w if w > 0 else 0
#
#         # 디버깅 출력 추가
#         # print(f"Contour at ({x}, {y}, {w}, {h}) with aspect ratio {aspect_ratio}")
#
#         # 스케일바 조건 확인
#         if aspect_ratio > 3 and (x < image.shape[1] * 0.2 or x > image.shape[1] * 0.8):
#             if h > max_height:
#                 max_height = h
#                 scalebar_contour = contour
#
#     if scalebar_contour is None:
#         print("스케일바를 찾을 수 없음")
#         return 0
#
#     return max_height
#
#
# def calculate_scale_factor(scalebar_length_pixels):
#     scalebar_real_length_cm = 14
#     if scalebar_length_pixels == 0:
#         return None
#     return scalebar_real_length_cm / scalebar_length_pixels
