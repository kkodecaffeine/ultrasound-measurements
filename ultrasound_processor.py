from image_processing.read_image import ImageReader
from image_processing.contour_analysis import ContourAnalyzer
from image_processing.postprocess import ImagePostprocessor
from image_processing.preprocess import ImagePreprocessor
from image_processing.save_image import ImageSaver


class UltrasoundImageProcessor:
    @staticmethod
    def process_ultrasound(
        image_path,
        output_path,
        padding=20,
        min_radius=50,
        max_radius=200,
        max_attempts=5,
    ):
        """
        초음파 이미지를 처리하여 점선 원을 검출하고, 마스킹된 이미지를 저장한다

        image_path (str): 입력 초음파 이미지 경로
        output_path (str): 출력 마스킹 이미지 저장 경로
        padding (int): 원 주변에 추가할 패딩 값
        min_radius (int): 원 검출을 위한 최소 반지름
        max_radius (int): 원 검출을 위한 최대 반지름
        max_attempts (int): 원 검출을 시도할 최대 횟수

        반환값: np.ndarray: 마스킹된 이미지

        예외: ValueError: max_attempts 횟수 내에 원이 검출되지 않을 경우 발생
        """

        for attempt in range(max_attempts):
            image = ImageReader.read(image_path)
            edges = ImagePreprocessor.preprocess_image(image)
            circle = ContourAnalyzer.detect_dotted_circle(edges, min_radius, max_radius)

            if circle is not None:
                # Circle detected, proceed with processing
                mask = ImagePostprocessor.create_circle_mask(
                    image.shape, circle, padding
                )
                masked_image = ImagePostprocessor.apply_mask(image, mask)
                ImageSaver.save_image(masked_image, output_path)
                return masked_image

            # Increment radius range and retry
            min_radius += 50
            max_radius += 100
            print(f"attempt {attempt + 1}: circle not detected")

        # If no circle is detected after max_attempts
        raise ValueError(f"min_radius={min_radius}, max_radius={max_radius}")
