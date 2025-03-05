from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np
from typing import Dict, Any

@dataclass
class IParams(ABC):
    """Base class for filter parameters with validation."""
    @abstractmethod
    def validate(self):
        pass
    
    @abstractmethod
    def get_param_definitions() ->  Dict[str, Any]:
        """
        Returns a JSON-compatible dictionary defining the parameters for the filter.
        
        The dictionary should have parameter names as keys and parameter definitions as values.
        Each parameter definition must be JSON-serializable and should include:
        - 'type': UI element type ('slider', 'dropdown', 'radio', etc.)
        - Other attributes specific to the UI element (min, max, options, etc.)
        - 'default': Default value for the parameter
        
        Example:
        {
            'brightness': {
                'type': 'slider',
                'min': -100,
                'max': 100,
                'step': 1,
                'default': 0
            },
            'method': {
                'type': 'radio',
                'options': {
                    'avg': 'Average',
                    'luminosity': 'Weighted (Luminosity)'
                },
                'default': 'luminosity'
            }
        }
        """
        raise NotImplementedError("Subclasses must implement get_param_definitions")