import cv2
import numpy as np
import pytesseract


class ContourSkull:
    @staticmethod
    def detect_dotted_circle(
        edges,
        min_radius: int = 50,
        max_radius: int = 200,
    ):
        """
        두개골 원형 검출을 위한 HoughCircles 함수

        Args:
            edges: 엣지 검출된 이미지
            min_radius: 최소 반지름 (기본값: 50)
            max_radius: 최대 반지름 (기본값: 200)

        param2:
            값이 작을수록 더 많은 원이 검출됨 (거짓 원도 많이 검출될 수 있음)
            값이 크면 더 확실한 원만 검출됨
            일반적으로 잘 노출되고 대비가 좋은 이미지의 경우 300까지도 설정 가능

        Returns:
            검출된 원의 중심점과 반지름 (x, y, r) 또는 None
        """
        circles = cv2.HoughCircles(
            edges,
            cv2.HOUGH_GRADIENT,
            dp=1,  # Adjust resolution (1 for full resolution)
            minDist=10,  # Minimum distance between detected circle centers
            param1=100,  # Canny high threshold
            param2=100,  # Accumulator threshold (lower -> more circles)
            minRadius=min_radius,  # Minimum radius of the circle
            maxRadius=max_radius,  # Maximum radius of the circle
        )

        if circles is not None:
            circles = np.uint16(np.around(circles))
            return circles[0][0]
        return None

    @staticmethod
    def find_skull_boundaries(param_image, gray_image):
        # 윤곽선 검출
        contours, _ = cv2.findContours(
            param_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        skull_boundary_points = []
        for contour in contours:
            # 면적이 너무 작은 윤곽선 제외
            if cv2.contourArea(contour) > 10:
                # 윤곽선의 모든 점을 추가
                points = contour.reshape(-1, 2)
                skull_boundary_points.extend(points)

        if not skull_boundary_points:
            return None, None

        # numpy 배열로 변환
        points = np.array(skull_boundary_points)

        # y 좌표로 정렬
        sorted_indices = np.argsort(points[:, 1])
        points = points[sorted_indices]

        top_points = points[:2]
        bottom_points = points[-2:]

        # 가장 밝은 점 선택
        top_point = top_points[
            np.argmax(gray_image[top_points[:, 1], top_points[:, 0]])
        ]
        bottom_point = bottom_points[
            np.argmax(gray_image[bottom_points[:, 1], bottom_points[:, 0]])
        ]

        return top_point, bottom_point
