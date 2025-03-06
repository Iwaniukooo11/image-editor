import sys
import os
from typing import List, Tuple
import numpy as np
from interfaces.IBase import IBase
from interfaces.IParams import IParams

class ImagePipeline:
    def __init__(self,img: np.array):
        """Initialize the ImagePipeline with an empty list of steps."""
        self.__steps: List[Tuple[IBase, IParams]] = []
        self.__img = img
        
    def add_step(self, filter: IBase, params: IParams):
        """Add a filter step to the pipeline with validation.
        
        Args:
            filter (IBase): The filter to be applied.
            params (IParams): The parameters for the filter.
        """
        if not isinstance(filter, IBase):
            raise TypeError("filter must be an instance of IBase")
        if not isinstance(params, IParams):
            raise TypeError("params must be an instance of IParams")
        self.__steps.append((filter, params))
        
    def execute(self) -> np.array:
        """Execute the pipeline on the given image.
        
        Args:
            img (np.array): The input image.
        
        Returns:
            np.array: The processed image.
        """
        img=self.__img
        for filter, params in self.__steps:
            img = filter.apply(img, params)
        return img
    
    def clear(self):
        """Clear all steps from the pipeline."""
        self.__steps = []

    def get_steps(self):
        """Get the list of steps in the pipeline."""
        return self.__steps