from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np
from interfaces.IBase import IBase
from interfaces.IParams import IParams


class BaseConvolution(IBase):
    @abstractmethod
    def apply(self, img: np.array, kernel: np.array) -> np.array:
        """Apply the convolution to the image.
        
        Args:
            img (np.array): The input image.
            kernel (np.array): The convolution kernel.
        
        Returns:
            np.array: The processed image.
        """
        pass
    
    @abstractmethod
    def _create_kernel(self, kernel_size: int) -> np.array:
        """Create the convolution kernel.
        
        Args:
            kernel_size (int): The size of the kernel.
        
        Returns:
            np.array: The convolution kernel.
        """
        pass
    
class ConvolutionParams(IParams):
    """Base class for convolution parameters."""
    def validate(self):
        pass
    
    # def get_param_definitions():
    #     return {}