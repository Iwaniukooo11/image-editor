from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np
from interfaces.IBase import IBase
from interfaces.IParams import IParams

class BaseFilter(IBase):
    @abstractmethod
    def apply(self, img: np.array, params: 'FilterParams') -> np.array:
        """Apply the filter to the image.
        
        Args:
            img (np.array): The input image.
            params (FilterParams): The parameters for the filter.
        
        Returns:
            np.array: The processed image.
        """
        pass
    
@dataclass
class FilterParams(IParams):
    """Bazowa klasa parametrów z walidacją"""
    def validate(self):
        pass  # Override w klasach pochodnych