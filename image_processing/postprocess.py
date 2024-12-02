import cv2
import numpy as np

class ImagePostprocessor:
    @staticmethod
    def create_circle_mask(image_shape, circle, padding=20):
        mask = np.zeros(image_shape[:2], dtype=np.uint8)
        cv2.circle(mask, (circle[0], circle[1]), circle[2] + padding, 255, -1)
        return mask

    @staticmethod
    def apply_mask(image, mask):
        masked_image = cv2.bitwise_and(image, image, mask=mask)
        masked_image[mask == 0] = [0, 0, 0]
        return masked_image
