from dataclasses import dataclass
from edges.base_edge import BaseEdge, EdgeParams
import numpy as np
from scipy.ndimage import convolve

@dataclass
class SobelParams(EdgeParams):
    """Parameters for the Sobel edge detection filter."""
    threshold: int = 128

    def validate(self):
        if not isinstance(self.threshold, int):
            raise ValueError("threshold must be an integer")
        
    def get_param_definitions():
        return {
            'threshold': {
                'type': 'slider',
                'min': 0,
                'max': 255,
                'step': 1,
                'default': 128
            }
        }
        
class SobelEdge(BaseEdge):
    @classmethod
    def apply(cls, img: np.array, params: SobelParams) -> np.array:
        """Apply the Sobel edge detection to the image.
        
        Args:
            img (np.array): The input image.
            params (SobelParams): The parameters for the edge detection.
        
        Returns:
            np.array: The processed image.
        """
        params.validate()
        
        # Convert RGB image to grayscale
        if img.ndim == 3:
            img = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)
        
        sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        sobel_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
        
        gradient_x = np.abs(convolve(img, sobel_x, mode='reflect'))
        gradient_y = np.abs(convolve(img, sobel_y, mode='reflect'))
        gradient = np.sqrt(gradient_x ** 2 + gradient_y ** 2)
        
        return np.where(gradient > params.threshold, 255, 0)