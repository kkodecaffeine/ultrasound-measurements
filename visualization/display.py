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


# def visualize_result(image, contours, bpd_distance, centroid1, centroid2):
#     """BPD 계산 결과와 윤곽선을 이미지에 시각화"""
#     # 입력 이미지가 이미 grayscale인 경우 처리
#     if len(image.shape) == 2:  # 그레이스케일 이미지인 경우
#         output_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
#     elif len(image.shape) == 3 and image.shape[2] == 3:  # 컬러 이미지인 경우
#         output_image = image.copy()
#     else:
#         raise ValueError("Unsupported image format")
#
#     # 모든 윤곽선 그리기
#     for contour in contours:
#         cv2.drawContours(output_image, [contour], -1, (0, 255, 0), 3)  # 초록색 윤곽선
#
#     # BPD 표시
#     cv2.putText(output_image, f"BPD: {bpd_distance:.2f} mm", (50, 50),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
#
#     # 중심점 표시
#     cv2.circle(output_image, centroid1, 5, (255, 0, 0), -1)  # 첫 번째 중심점
#     cv2.circle(output_image, centroid2, 5, (255, 0, 0), -1)  # 두 번째 중심점
#     cv2.line(output_image, centroid1, centroid2, (255, 0, 0), 2)  # 중심점 간 선
#
#     # 이미지 출력
#     cv2.imshow("BPD Result Visualization", output_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()


def show_images(images, titles):
    """
    여러 이미지를 화면에 표시
    """
    for img, title in zip(images, titles):
        cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()