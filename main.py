from image_processing.calculate_scale import ScaleCalculator
from image_processing.contour_analysis import ContourAnalyzer
from image_processing.read_image import ImageReader
from ultrasound_processor import UltrasoundImageProcessor
from image_processing.preprocess import ImagePreprocessor
from visualization.display import Display


def main():
    preprocessor = ImagePreprocessor()
    processor = UltrasoundImageProcessor()
    image_path = "image2.jpg"
    output_path = "masked_image.jpg"

    processed_image = processor.process_ultrasound(image_path, output_path, padding=30)
    gray_image = preprocessor.convert_to_gray(processed_image)
    blurred_image = preprocessor.blur_with_gaussian(gray_image)
    binary = preprocessor.convert_to_binary(blurred_image)

    # BPD 측정
    top_point, bottom_point = ContourAnalyzer.find_skull_boundaries(binary, gray_image)
    result, distance = ScaleCalculator.measure_bpd(
        processed_image, top_point, bottom_point
    )

    # 결과 저장
    # ImageSaver.save_with_measurements(result, "result.jpg", distance, top_point, bottom_point)

    # 결과 표시
    Display.show_result(result, distance)


if __name__ == "__main__":
    main()
