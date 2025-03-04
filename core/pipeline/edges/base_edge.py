from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np
from interfaces.IBase import IBase
from interfaces.IParams import IParams

class BaseEdge(IBase):
    @abstractmethod
    def apply(self, img: np.array, params: 'EdgeParams') -> np.array:
        """Apply the edge detection to the image.
        
        Args:
            img (np.array): The input image.
            params (EdgeParams): The parameters for the edge detection.
        
        Returns:
            np.array: The processed image.
        """
        pass
    
@dataclass
class EdgeParams(IParams):
    """Base class for edge detection parameters with validation"""
    def validate(self):
        pass