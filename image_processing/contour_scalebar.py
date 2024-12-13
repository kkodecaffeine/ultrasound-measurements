import cv2


class ContourScaleBar:
    @staticmethod
    def find_scalebar_boundaries(param_image, binary):
        # 윤곽선 검출
        contours, _ = cv2.findContours(
            binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        scalebar_contour = []
        for contour in contours:
            # 윤곽선의 경계 사각형 계산
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h  # 가로/세로 비율

            # 세로로 긴 스케일 바 탐지 (이미지의 좌/우 15% 위치)
            if aspect_ratio > 3 and (
                x < param_image.shape[1] * 0.15 or x > param_image.shape[1] * 0.85
            ):
                scalebar_contour.append((x, y, w, h))

        return scalebar_contour
