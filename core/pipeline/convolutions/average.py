from dataclasses import dataclass
from convolutions.base_convolution import BaseConvolution, ConvolutionParams
import numpy as np
from scipy.ndimage import convolve

@dataclass
class AverageParams(ConvolutionParams):
    """Parameters for the Average convolution."""
    kernel_size: int = 3

    def validate(self):
        if self.kernel_size % 2 == 0:
            raise ValueError("kernel_size must be odd")
        if self.kernel_size < 3:
            raise ValueError("kernel_size must be at least 3")
        
class AverageConvolution(BaseConvolution):
    @classmethod
    def apply(cls, img: np.array, params: AverageParams) -> np.array:
        """Apply the average convolution to the image.
        
        Args:
            img (np.array): The input image.
            params (AverageParams): The parameters for the convolution.
        
        Returns:
            np.array: The processed image.
        """
        params.validate()
        kernel = cls._create_kernel(params.kernel_size)
        if img.ndim == 2:  # Grayscale image
            return cls._apply_convolution(img, kernel)
        elif img.ndim == 3:  # Color image
            channels = []
            for i in range(img.shape[2]):
                channel = cls._apply_convolution(img[:, :, i], kernel)
                channels.append(channel)
            return np.stack(channels, axis=2)
        else:
            raise ValueError("Unsupported image dimensions")
    
    @classmethod
    def _create_kernel(cls, kernel_size: int) -> np.array:
        """Create the average convolution kernel.
        
        Args:
            kernel_size (int): The size of the kernel.
        
        Returns:
            np.array: The average convolution kernel.
        """
        return np.ones((kernel_size, kernel_size)) / kernel_size**2

    @classmethod
    def _apply_convolution(cls, img: np.array, kernel: np.array) -> np.array:
        """Apply the convolution to the image.
        
        Args:
            img (np.array): The input image.
            kernel (np.array): The convolution kernel.
        
        Returns:
            np.array: The processed image.
        """
        return convolve(img, kernel, mode='reflect')