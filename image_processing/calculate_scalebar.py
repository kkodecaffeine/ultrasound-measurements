import cv2


class ScaleBarCalculator:
    @staticmethod
    def measure_scalebar_factor(scalebar_contours, param_image):
        # 같은 x 축에 있는 윤곽선 필터링
        threshold = 5  # x 좌표 차이 허용 범위 (픽셀 단위)
        filtered_contours = []

        for contour in scalebar_contours:
            x, y, w, h = contour
            if not filtered_contours or abs(x - filtered_contours[0][0]) <= threshold:
                filtered_contours.append((x, y, w, h))

        sorted_scalebar_contours = sorted(filtered_contours, key=lambda c: c[1])

        # 눈금 간격 측정
        scalebar_widths = []
        for i in range(1, len(sorted_scalebar_contours)):
            _, y1, _, _ = sorted_scalebar_contours[i - 1]
            _, y2, _, _ = sorted_scalebar_contours[i]
            gap = abs(y2 - y1)  # 간격 계산 (절대값 사용)
            scalebar_widths.append(gap)

        # 조건에 따른 값 계산 (1칸을 1cm 로 전제)
        result = []
        if scalebar_widths:
            for width in scalebar_widths:
                if 100 <= width < 200:
                    result.append(width / 2)  # 2칸
                elif 200 <= width < 250:
                    result.append(width / 5)  # 5칸
                elif width >= 250:
                    result.append(width / 10)  # 10칸
                else:
                    result.append(width)

        # 픽셀 단위 눈금 간격 출력
        for i, value in enumerate(result):
            print(f"눈금 {i} ~ {i + 1} 계산된 값: {value:.2f}")

        # 7. 결과 시각화
        for x, y, w, h in sorted_scalebar_contours:
            cv2.rectangle(param_image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # cv2.imshow("Scale Bar Detection", param_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        if not result:  # Check if the result list is empty
            raise ValueError("The result list is empty.")

        if result[0] == 0:  # Check if the first value is 0
            raise ZeroDivisionError("Division by zero is not possible.")

        scale_factor = 1 / result[0]
        print(f"픽셀당 실제 길이: {scale_factor:.2f} cm/pixel")

        return scale_factor
