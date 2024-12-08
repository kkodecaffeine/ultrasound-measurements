import cv2

class Display:
    @staticmethod
    def show_result(image, distance=None):
        if distance is not None:
            print(f"측정된 BPD: {distance:.1f} 픽셀")
            cv2.imshow("BPD Measurement", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("두개골 경계를 찾을 수 없습니다.")