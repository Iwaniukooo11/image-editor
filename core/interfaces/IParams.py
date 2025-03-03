#prepare interface for dataclass with function validate

from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np

@dataclass
class IParams(ABC):
    """Base class for filter parameters with validation."""
    @abstractmethod
    def validate(self):
        pass