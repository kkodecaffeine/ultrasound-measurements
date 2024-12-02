from image_processing.read_image import ImageReader
from image_processing.contour_analysis import ContourAnalyzer
from image_processing.postprocess import ImagePostprocessor
from image_processing.preprocess import ImagePreprocessor
from image_processing.save_image import ImageSaver




class UltrasoundImageProcessor:
    @staticmethod
    def process_ultrasound(image_path, output_path, padding=20):
        image = ImageReader.read(image_path)
        edges = ImagePreprocessor.preprocess_image(image)
        circle = ContourAnalyzer.detect_dotted_circle(edges)

        if circle is None:
            raise ValueError("원을 검출할 수 없습니다")

        mask = ImagePostprocessor.create_circle_mask(image.shape, circle, padding)
        masked_image = ImagePostprocessor.apply_mask(image, mask)
        ImageSaver.save_image(masked_image, output_path)

        return masked_image