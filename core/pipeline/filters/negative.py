from dataclasses import dataclass
from filters.base_filter import BaseFilter, FilterParams
import numpy as np
#import dict
from typing import Dict, Any

@dataclass
class NegativeParams(FilterParams):
    """Parameters for the Negative filter."""
    pass

    def validate(self):
        pass

    def get_param_definitions() -> Dict[str, Any]:
        # No parameters for Negative filter, return empty dictionary
        return {
            # 'foo':{
            #     'type': 'slider',
            #     'min': 0,
            #     'max': 100,
            #     'step': 1,
            #     'default': 0}
        }

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