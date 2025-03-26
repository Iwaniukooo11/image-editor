from dataclasses import dataclass
from filters.base_filter import BaseFilter, FilterParams
import numpy as np

@dataclass
class GrayscaleParams(FilterParams):
    """Parameters for the Grayscale filter."""
    method: str = "luminosity"
    intensity: float = 1.0

    def validate(self):
         if self.method not in ["luminosity", "average", "lightness"]:
             raise ValueError("method must be one of 'luminosity', 'average', or 'lightness'")
         
    
    def get_param_definitions():
        return {
            'method': {
                'type': 'radio',
                'options': {
                    'luminosity': 'Weighted (Luminosity)',
                    'average': 'Average',
                    'lightness': 'Lightness'
                },
                'default': 'luminosity'
            },
            'intensity': {
                'type': 'slider',
                'min': 0,
                'max': 2,
                'step': 0.01,
                'default': 1.0
            }
        }
         
class GrayscaleFilter(BaseFilter):
    @classmethod
    # def apply(self, img: np.array, params: GrayscaleParams) -> np.array:
    #     """Convert the image to grayscale using the specified method.
        
    #     Args:
    #         img (np.array): The input image.
    #         params (GrayscaleParams): The parameters for the filter.
        
    #     Returns:
    #         np.array: The grayscale image.
    #     """
    #     params.validate()
    #     if params.method == "luminosity":
    #         img = np.dot(img[...,:3], [0.21, 0.72, 0.07])
    #     elif params.method == "average":
    #         img = np.mean(img, axis=-1)
    #     elif params.method == "lightness":
    #         img = np.max(img, axis=-1)
    #     return img * params.intensity
    def apply(self, img: np.array, params: GrayscaleParams) -> np.array:
        """Convert the image to grayscale using the specified method."""
        params.validate()
        original_shape = img.shape
        
        if params.method == "luminosity":
            gray = np.dot(img[...,:3], [0.21, 0.72, 0.07])
        elif params.method == "average":
            gray = np.mean(img, axis=-1)
        elif params.method == "lightness":
            gray = np.max(img, axis=-1)
            
        gray = gray * params.intensity
        
        result = np.zeros_like(img)
        for i in range(min(3, original_shape[2])):  
            result[..., i] = gray
            
        return result