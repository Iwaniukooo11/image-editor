from dataclasses import dataclass
from convolutions.base_convolution import BaseConvolution, ConvolutionParams
import numpy as np
from scipy.ndimage import convolve

@dataclass
class SharpeningParams(ConvolutionParams):
    """Parameters for the sharpening convolution."""
    kernel_size: int = 3
    alpha: int = 1.0

    def validate(self):
        if self.kernel_size % 2 == 0:
            raise ValueError("kernel_size must be odd")
        if self.kernel_size < 3:
            raise ValueError("kernel_size must be at least 3")
        if self.alpha <= 0:
            raise ValueError("alpha must be positive")
        
    def get_param_definitions():
        return {
            'kernel_size': {
                'type': 'slider',
                'min': 3,
                'max': 21,
                'step': 2,
                'default': 3
            },
            'alpha': {
                'type': 'slider',
                'min': 0.1,
                'max': 5.0,
                'step': 0.1,
                'default': 1.0
            }
        }
        
class SharpeningConvolution(BaseConvolution):
    @classmethod
    def apply(cls, img: np.array, params: SharpeningParams) -> np.array:
        """Apply the sharpening convolution to the image.
        
        Args:
            img (np.array): The input image.
            params (SharpeningParams): The parameters for the convolution.
        
        Returns:
            np.array: The processed image.
        """
        params.validate()
        kernel = cls._create_kernel(params.kernel_size, params.alpha)
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
    def _create_kernel(cls, kernel_size: int, alpha: float) -> np.array:
        """Create the sharpening convolution kernel.
        
        Args:
            kernel_size (int): The size of the kernel.
            alpha (float): The strength of the sharpening effect.
        
        Returns:
            np.array: The sharpening convolution kernel.
        """
        kernel = np.full((kernel_size, kernel_size), -1 / (kernel_size**2 - 1))
        kernel[kernel_size // 2, kernel_size // 2] = 1 + alpha
        return kernel

    @classmethod
    def _apply_convolution(cls, img: np.array, kernel: np.array) -> np.array:
        """Apply the convolution to the image.
        
        Args:
            img (np.array): The input image.
            kernel (np.array): The convolution kernel.
        
        Returns:
            np.array: The processed image.
        """
        return convolve(img, kernel)