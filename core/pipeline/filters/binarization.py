from dataclasses import dataclass
from filters.base_filter import BaseFilter, FilterParams
import numpy as np

@dataclass
class BinarizationParams(FilterParams):
    """Parameters for the Binarization filter."""
    threshold: int = 128

    def validate(self):
        if not isinstance(self.threshold, int):
            raise ValueError("threshold must be an integer")
        
class BinarizationFilter(BaseFilter):
    @classmethod
    def apply(self, img: np.array, params: BinarizationParams) -> np.array:
        """Convert the image to binary using the specified threshold.
        
        Args:
            img (np.array): The input image.
            params (BinarizationParams): The parameters for the filter.
        
        Returns:
            np.array: The binary image.
        """
        params.validate()
        return np.where(img > params.threshold, 255, 0)