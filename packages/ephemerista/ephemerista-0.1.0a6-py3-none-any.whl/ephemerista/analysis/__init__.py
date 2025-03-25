"""The analyses package.

This packages provides classes for all analyses supported by Ephemerista.
"""

import abc
from typing import Generic, TypeVar

from ephemerista import BaseModel

T = TypeVar("T")


class Analysis(BaseModel, Generic[T], abc.ABC):
    """Base class for analyses."""

    def __init__(self, **data):
        super().__init__(**data)

    @abc.abstractmethod
    def analyze(self, **kwargs) -> T:
        """Run the analysis."""
        raise NotImplementedError()
