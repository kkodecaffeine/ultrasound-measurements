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
