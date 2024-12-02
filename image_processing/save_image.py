import cv2

# def save_image(image, output_path):
#     """이미지를 저장하는 함수"""
#     cv2.imwrite(output_path, image)
#     print(f"'{output_path}'로 저장 완료")
#
#

class ImageSaver:
    @staticmethod
    def save_with_measurements(image, filename, distance=None, top_point=None, bottom_point=None):
        if all([distance, top_point, bottom_point]):
            cv2.line(image, tuple(top_point), tuple(bottom_point), (0, 0, 255), 2)
            cv2.circle(image, tuple(top_point), 3, (0, 255, 0), -1)
            cv2.circle(image, tuple(bottom_point), 3, (0, 255, 0), -1)

            mid_point = ((top_point[0] + bottom_point[0])//2, (top_point[1] + bottom_point[1])//2)
            cv2.putText(image, f'BPD: {distance:.1f}px',
                        (mid_point[0]-60, mid_point[1]-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imwrite(filename, image)

    @staticmethod
    def save_image(image, output_path):
        cv2.imwrite(output_path, image)