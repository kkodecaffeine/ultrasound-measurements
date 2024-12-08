import cv2


class ImageReader:
    @staticmethod
    def read(image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Image not found at path: {image_path}")

        return image
