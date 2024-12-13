from image_processing.calculate_bpd import ScaleCalculator
from image_processing.calculate_scalebar import ScaleBarCalculator
from image_processing.contour_scalebar import ContourScaleBar
from image_processing.contour_skull import ContourSkull
from image_processing.read_image import ImageReader
from ultrasound_processor import UltrasoundImageProcessor
from image_processing.preprocess import ImagePreprocessor
from visualization.display import Display


def main():
    preprocessor = ImagePreprocessor()
    processor = UltrasoundImageProcessor()
    image_path = "image5.jpg"
    output_path = "masked_image.jpg"

    image = ImageReader.read(image_path)

    # 문자/숫자 검출하여 블러 처리
    gray_image = preprocessor.convert_to_gray(image)
    blurred_text_image = preprocessor.blur_text_regions(image, gray_image)

    # 스케일-바 검출
    gray_image = preprocessor.convert_to_gray(blurred_text_image)
    binary = preprocessor.convert_to_binary(gray_image, 200, 255)
    scalebar_contour = ContourScaleBar.find_scalebar_boundaries(gray_image, binary)
    scale_factor = ScaleBarCalculator.measure_scalebar_factor(scalebar_contour, image)

    processed_image = processor.process_ultrasound(image_path, output_path, padding=30)
    gray_image = preprocessor.convert_to_gray(processed_image)
    blurred_image = preprocessor.blur_with_gaussian(gray_image)
    binary = preprocessor.convert_to_binary(blurred_image)

    # BPD 측정
    top_point, bottom_point = ContourSkull.find_skull_boundaries(binary, gray_image)
    result, distance = ScaleCalculator.measure_bpd(
        processed_image, top_point, bottom_point
    )

    # # 결과 저장
    # # ImageSaver.save_with_measurements(result, "result.jpg", distance, top_point, bottom_point)
    #
    # 결과 표시
    Display.show_result(result, distance, scale_factor)


if __name__ == "__main__":
    main()
