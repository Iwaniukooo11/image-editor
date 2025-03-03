from dataclasses import dataclass
from filters.base_filter import BaseFilter, FilterParams
import numpy as np

@dataclass
class BrightnessParams(FilterParams):
    """Parameters for the Brightness filter."""
    value: int = 0

    def validate(self):
        if not isinstance(self.value, int):
            raise ValueError("value must be an integer")
        
class BrightnessFilter(BaseFilter):
    @classmethod
    def apply(self, img: np.array, params: BrightnessParams) -> np.array:
        """Adjust the brightness of the image.
        
        Args:
            img (np.array): The input image.
            params (BrightnessParams): The parameters for the filter.
        
        Returns:
            np.array: The image with adjusted brightness.
        """
        params.validate()
        img = img + params.value
        return np.clip(img, 0, 255)