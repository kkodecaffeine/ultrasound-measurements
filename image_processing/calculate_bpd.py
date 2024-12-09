from typing import Any

import cv2
import numpy as np


class ScaleCalculator:
    @staticmethod
    def measure_scale_distance(tick_positions):
        # 각 스케일바 간의 거리 측정
        spacings = np.diff(tick_positions)
        return spacings

    @staticmethod
    def calculate_distance(point1, point2):
        return np.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

    @staticmethod
    def measure_bpd(
        param_image,
        top_point: tuple[Any, Any] | tuple[Any, None],
        bottom_point: tuple[Any, Any] | tuple[Any, None],
    ):
        result = param_image.copy()

        if top_point is not None and bottom_point is not None:
            # 거리 계산
            distance = np.sqrt(
                (bottom_point[0] - top_point[0]) ** 2
                + (bottom_point[1] - top_point[1]) ** 2
            )

            # 결과 시각화
            cv2.line(result, tuple(top_point), tuple(bottom_point), (0, 0, 255), 2)
            cv2.circle(result, tuple(top_point), 3, (0, 255, 0), -1)
            cv2.circle(result, tuple(bottom_point), 3, (0, 255, 0), -1)

            # 거리 표시
            mid_point = (
                (top_point[0] + bottom_point[0]) // 2,
                (top_point[1] + bottom_point[1]) // 2,
            )
            cv2.putText(
                result,
                f"BPD: {distance:.1f}px",
                (mid_point[0] - 60, mid_point[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )
            return result, distance

        return result, None
