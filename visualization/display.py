import cv2


class Display:
    @staticmethod
    def show_result(param_image, distance=None, scale_factor: float = 0):
        if distance is not None:
            distance_mm = distance * scale_factor  # 픽셀 거리를 mm로 변환

            cv2.putText(
                param_image,
                f"BPD: {distance_mm:.2f} cm",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2,
            )
            cv2.imshow("BPD Measurement", param_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("두개골 경계를 찾을 수 없습니다")
