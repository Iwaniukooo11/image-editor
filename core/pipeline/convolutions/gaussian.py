from dataclasses import dataclass
from convolutions.base_convolution import BaseConvolution, ConvolutionParams
import numpy as np
from scipy.ndimage import convolve

@dataclass
class GaussianParams(ConvolutionParams):
    """Parameters for the Gaussian convolution."""
    kernel_size: int = 3
    sigma: float = 1.0

    def validate(self):
        if self.kernel_size % 2 == 0:
            raise ValueError("kernel_size must be odd")
        if self.kernel_size < 3:
            raise ValueError("kernel_size must be at least 3")
        if self.sigma <= 0:
            raise ValueError("sigma must be positive")
    def get_param_definitions():
        return {
            'kernel_size': {
                'type': 'slider',
                'min': 3,
                'max': 21,
                'step': 2,
                'default': 3
            },
            'sigma': {
                'type': 'slider',
                'min': 0.1,
                'max': 5.0,
                'step': 0.1,
                'default': 1.0
            }
        }
        
class GaussianConvolution(BaseConvolution):
    @classmethod
    def apply(cls, img: np.array, params: GaussianParams) -> np.array:
        """Apply the Gaussian convolution to the image.
        
        Args:
            img (np.array): The input image.
            params (GaussianParams): The parameters for the convolution.
        
        Returns:
            np.array: The processed image.
        """
        params.validate()
        kernel = cls._create_kernel(params.kernel_size, params.sigma)
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
    def _create_kernel(cls, kernel_size: int, sigma: float) -> np.array:
        """Create the Gaussian convolution kernel.
        
        Args:
            kernel_size (int): The size of the kernel.
            sigma (float): The standard deviation of the Gaussian.
        
        Returns:
            np.array: The Gaussian convolution kernel.
        """
        kernel = np.fromfunction(
            lambda x, y: (1 / (2 * np.pi * sigma**2)) * np.exp(-((x - (kernel_size - 1) / 2)**2 + (y - (kernel_size - 1) / 2)**2) / (2 * sigma**2)),
            (kernel_size, kernel_size)
        )
        return kernel / np.sum(kernel)
 
    @classmethod
    def _apply_convolution(cls, img: np.array, kernel: np.array) -> np.array:
        """Apply the convolution to the image.
        
        Args:
            img (np.array): The input image.
            kernel (np.array): The convolution kernel.
        """
        return convolve(img, kernel, mode='constant', cval=0.0)