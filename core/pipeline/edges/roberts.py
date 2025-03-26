from dataclasses import dataclass
from edges.base_edge import BaseEdge, EdgeParams
import numpy as np
from scipy.ndimage import convolve

@dataclass
class RobertsParams(EdgeParams):
    """Parameters for the Roberts edge detection filter."""
    threshold: int = 128

    def validate(self):
        if not isinstance(self.threshold, int):
            raise ValueError("threshold must be an integer")
        
    def get_param_definitions():
        return {
            'threshold': {
                'type': 'slider',
                'min': 0,
                'max': 21,
                'step': 1,
                'default': 2
            }
        }
        
class RobertsEdge(BaseEdge):
    # @classmethod
    # def apply(cls, img: np.array, params: RobertsParams) -> np.array:
    #     """Apply the Roberts edge detection to the image.
        
    #     Args:
    #         img (np.array): The input image.
    #         params (RobertsParams): The parameters for the edge detection.
        
    #     Returns:
    #         np.array: The processed image.
    #     """
    #     params.validate()
    #     roberts_x = np.array([[1, 0], [0, -1]])
    #     roberts_y = np.array([[0, 1], [-1, 0]])
        
    #     if img.ndim == 3:
    #         img = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)
        
    #     gradient_x = np.abs(convolve(img, roberts_x, mode='reflect'))
    #     gradient_y = np.abs(convolve(img, roberts_y, mode='reflect'))
    #     gradient = np.sqrt(gradient_x ** 2 + gradient_y ** 2)
        
    #     return np.where(gradient > params.threshold, 255, 0)
    @classmethod
    def apply(cls, img: np.array, params: RobertsParams) -> np.array:
        """Apply the Roberts edge detection to the image."""
        params.validate()
        
        original_shape = img.shape
        has_color = img.ndim == 3
        
        if has_color:
            gray_img = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)
        else:
            gray_img = img
        
        roberts_x = np.array([[1, 0], [0, -1]])
        roberts_y = np.array([[0, 1], [-1, 0]])
        
        gradient_x = np.abs(convolve(gray_img, roberts_x, mode='reflect'))
        gradient_y = np.abs(convolve(gray_img, roberts_y, mode='reflect'))
        gradient = np.sqrt(gradient_x ** 2 + gradient_y ** 2)
        
        edge_img = np.where(gradient > params.threshold, 255, 0).astype(np.uint8)
        
        if has_color:
            result = np.zeros_like(img)
            for i in range(min(3, original_shape[2])):  
                result[..., i] = edge_img
            return result
        else:
            return edge_img