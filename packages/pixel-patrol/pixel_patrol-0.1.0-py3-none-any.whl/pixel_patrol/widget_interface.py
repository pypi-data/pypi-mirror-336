from abc import ABC, abstractmethod
from typing import List


class ImagePrevalidationWidget(ABC):
    @property
    @abstractmethod
    def tab(self) -> str:
        """Return the name of the tab this widget belongs to."""
        pass

    @property
    def name(self) -> str:
        return type(self).__name__

    def required_columns(self) -> List[str]:
        """Returns required data column names"""
        return []

    @abstractmethod
    def run(self, *args, **kwargs):
        """Execute the widget's functionality."""
        pass
