from image_processing.calculate_scale import ScaleCalculator
from image_processing.read_image import ImageReader
from ultrasound_processor import UltrasoundImageProcessor
from visualization.display import Display

def main():
    processor = UltrasoundImageProcessor()
    image_path = "image7.jpg"
    output_path = "masked_image.jpg"

    processed_image = processor.process_ultrasound(image_path, output_path, padding=30)

    # 이미지 읽기
    image = ImageReader.read(image_path)

    # BPD 측정
    result, distance = ScaleCalculator.measure_bpd(processed_image)

    print(result, distance)
    # 결과 저장
    # ImageSaver.save_with_measurements(result, "result.jpg", distance, top_point, bottom_point)

    # 결과 표시
    Display.show_result(result, distance)

if __name__ == "__main__":
    main()
