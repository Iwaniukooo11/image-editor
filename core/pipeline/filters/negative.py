from dataclasses import dataclass
from filters.base_filter import BaseFilter, FilterParams
import numpy as np

@dataclass
class NegativeParams(FilterParams):
    """Parameters for the Negative filter."""
    pass

class NegativeFilter(BaseFilter):
    @classmethod
    def apply(self, img: np.array, params: NegativeParams) -> np.array:
        """Convert the image to its negative.
        
        Args:
            img (np.array): The input image.
            params (NegativeParams): The parameters for the filter.
        
        Returns:
            np.array: The negative image.
        """
        return 255 - img