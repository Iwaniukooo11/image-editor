from dataclasses import dataclass
from filters.base_filter import BaseFilter, FilterParams
import numpy as np

@dataclass
class ContrastParams(FilterParams):
    """Parameters for the Contrast filter."""
    value: float = 1.0

    def validate(self):
        if not isinstance(self.value, (int, float)):
            raise ValueError("value must be a number")
        
class ContrastFilter(BaseFilter):
    @classmethod
    def apply(self, img: np.array, params: ContrastParams) -> np.array:
        """Adjust the contrast of the image.
        
        Args:
            img (np.array): The input image.
            params (ContrastParams): The parameters for the filter.
        
        Returns:
            np.array: The image with adjusted contrast.
        """
        params.validate()
        img = (img - 128) * params.value + 128
        return np.clip(img, 0, 255)