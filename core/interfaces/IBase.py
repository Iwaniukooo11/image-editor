from abc import ABC, abstractmethod
from dataclasses import dataclass
from interfaces.IParams import IParams
import numpy as np

class IBase(ABC):
    @abstractmethod
    def apply(self, img: np.array, params: IParams) -> np.array:
        """Apply the filter to the image.
        
        Args:
            img (np.array): The input image.
            params (FilterParams): The parameters for the filter.
        
        Returns:
            np.array: The image after applying the filter.
        """
        pass