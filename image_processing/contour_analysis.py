import cv2
import numpy as np
import pytesseract

class ContourAnalyzer:
    @staticmethod
    def detect_dotted_circle(edges):
        circles = cv2.HoughCircles(
            edges,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=300,
            param1=50,
            param2=25,
            minRadius=150,
            maxRadius=400
        )

        if circles is not None:
            circles = np.uint16(np.around(circles))
            return circles[0][0]
        return None

    @staticmethod
    def find_vertical_skull_boundaries(image):
        # 그레이스케일 변환
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 이미지 전처리
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # 하얀색 테두리 검출을 위한 임계값 처리
        _, thresh = cv2.threshold(blurred, 220, 255, cv2.THRESH_BINARY)

        # 윤곽선 검출
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 각 윤곽선의 점들을 저장할 리스트
        all_points = []

        for contour in contours:
                # 면적이 너무 작은 윤곽선 제외
                if cv2.contourArea(contour) > 100:
                        # 윤곽선의 모든 점을 추가
                        points = contour.reshape(-1, 2)
                        all_points.extend(points)

        if not all_points:
                return None, None

        # numpy 배열로 변환
        points = np.array(all_points)

        # y 좌표로 정렬
        sorted_indices = np.argsort(points[:, 1])
        points = points[sorted_indices]

        n = len(points)
        top_points = points[:n//10]
        bottom_points = points[-n//2:][:2]

        # 가장 밝은 점 선택
        top_point = top_points[np.argmax(gray[top_points[:, 1], top_points[:, 0]])]
        bottom_point = bottom_points[np.argmax(gray[bottom_points[:, 1], bottom_points[:, 0]])]

        return top_point, bottom_point

# def find_contours(binary_image):
#     """이진화된 이미지에서 윤곽선 검출"""
#     # 이미지 전처리
#     # 입력 이미지가 BGR인지 확인 후 그레이스케일로 변환
#     if len(binary_image.shape) == 3:
#         gray = cv2.cvtColor(binary_image, cv2.COLOR_BGR2GRAY)
#     else:
#         gray = binary_image
#
#     _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
#
#     # 윤곽선 찾기
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
#     if len(contours) == 0:
#         print("하얀 테두리 윤곽선이 없음")
#         return []
#
#     # 곡선 형태의 윤곽선만 필터링 (너무 직선인 윤곽선 제외)
#     filtered_contours = []
#     for contour in contours:
#         # 곡선일수록 길이가 길어지는 특성을 이용
#         if cv2.arcLength(contour, True) > 100:  # 일정 길이 이상인 곡선만 선택
#             # filtered_contours.append(contour)
#             # 윤곽선 내부 평균 강도 계산
#             mask = np.zeros_like(gray, dtype=np.uint8)
#             cv2.drawContours(mask, [contour], -1, 255, thickness=-1)  # 윤곽선 내부 채움
#             mean_intensity = cv2.mean(gray, mask=mask)[0]
#
#             # 평균 강도 조건
#             if mean_intensity > 180:  # 밝기가 충분히 높은 영역만 선택
#                 filtered_contours.append(contour)
#
#     # 가장 긴 두 개의 곡선만 선택
#     filtered_contours = sorted(filtered_contours, key=cv2.contourArea, reverse=True)[:2]
#
#     return filtered_contours
#
# def calculate_centroid(contour):
#     M = cv2.moments(contour)
#     if M["m00"] != 0:
#         cx = int(M["m10"] / M["m00"])
#         cy = int(M["m01"] / M["m00"])
#         return (cx, cy)
#     return None
#
# def calculate_bpd_with_centroids(contours, scale_factor):
#     if len(contours) < 2:
#         print("두 개 이상의 곡선을 찾을 수 없음")
#         return None
#
#     max_distance = 0
#     best_pair = None
#
#     for i in range(len(contours)):
#         for j in range(i + 1, len(contours)):
#             for point1 in contours[i]:
#                 for point2 in contours[j]:
#                     x1, y1 = point1[0]
#                     x2, y2 = point2[0]
#                     dx = x2 - x1
#                     dy = y2 - y1
#                     slope = abs(dx / dy) if dy != 0 else float('inf')
#                     distance = np.sqrt(dx**2 + dy**2)
#                     if slope < 0.5 and distance > max_distance:  # 기울기 조건 완화
#                         max_distance = distance
#                         best_pair = ((x1, y1), (x2, y2))
#
#     if best_pair is None:
#         print("조건을 만족하는 점 쌍을 찾을 수 없음")
#         return None
#
#     point1, point2 = best_pair
#     distance_mm = max_distance * scale_factor
#     print(f"BPD: {distance_mm:.2f} mm")
#     return distance_mm, point1, point2
#
# def is_text_contour(contour):
#     """텍스트 윤곽선 판별 함수."""
#     x, y, w, h = cv2.boundingRect(contour)
#     aspect_ratio = w / h
#     return 10 < w < 200 and 10 < h < 50 and 2.0 < aspect_ratio < 10.0
#
# def is_semi_circle(contour):
#     """반원 검증 함수."""
#     perimeter = cv2.arcLength(contour, True)
#     area = cv2.contourArea(contour)
#     if perimeter == 0 or area == 0:
#         return False
#
#     # 원형성 계산
#     circularity = (4 * np.pi * area) / (perimeter ** 2)
#
#     # 반원이므로 원형성은 낮지만 여전히 일정 수준 이상
#     if circularity < 0.1:
#         # 열려 있는 곡선인지 확인 (닫힌 곡선은 제외)
#         bounding_rect = cv2.boundingRect(contour)
#         width, height = bounding_rect[2], bounding_rect[3]
#         aspect_ratio = width / height
#         if aspect_ratio > 1.5:  # 반원이 일반적으로 가로로 길게 펼쳐진 경우
#             return True
#
#     return False
#
# def mask_text_areas(image):
#     # 입력 이미지가 BGR인지 확인 후 그레이스케일로 변환
#     if len(image.shape) == 3:
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     else:
#         gray = image
#
#     # 텍스트 영역 검출 (pytesseract)
#     detection_boxes = pytesseract.image_to_boxes(gray)
#
#     mask = np.ones(image.shape[:2], dtype=np.uint8) * 255  # 전체를 흰색으로 초기화
#
#     for box in detection_boxes.splitlines():
#         b = box.split()
#         x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
#
#         # 텍스트 영역을 검출하여 그 영역을 마스크 처리 (검은색으로)
#         cv2.rectangle(mask, (x, image.shape[0] - y), (w, image.shape[0] - h), (0, 0, 0), -1)
#
#     # 마스크와 이미지를 같은 크기 및 타입으로 맞추기
#     mask = cv2.resize(mask, (image.shape[1], image.shape[0]))
#
#     # 스케일바 영역은 마스킹 처리하지 않음 (BPD 계산시 사용될 수 있도록)
#     height, width = image.shape[:2]
#     scalebar_x1 = int(width * 0.8)  # 스케일바 영역의 시작점
#     scalebar_x2 = width  # 스케일바 영역의 끝점
#     mask[:, scalebar_x1:scalebar_x2] = 255  # 스케일바 부분을 흰색으로 처리 (마스크하지 않음)
#
#     return cv2.bitwise_and(image, image, mask=cv2.bitwise_not(mask))
#
#
# def mask_semi_circles(image, contours):
#     mask = np.zeros_like(image, dtype=np.uint8)
#     output = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)  # 원본 이미지를 컬러로 변환
#
#     for idx, contour in enumerate(contours):
#         if is_text_contour(contour):  # 텍스트 윤곽선 무시
#             continue
#
#         if is_semi_circle(contour):
#             cv2.drawContours(output, [contour], -1, (0, 255, 0), 2) # 초록색으로 표시
#             cv2.drawContours(mask, [contour], -1, 255, -1)  # 초록색 영역 마스킹
#
#     masked_image = cv2.bitwise_and(image, image, mask=cv2.bitwise_not(mask))
#     return masked_image
