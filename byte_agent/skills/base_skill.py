"""Base skill class."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseSkill(ABC):
    name: str = "unnamed"
    description: str = ""
    version: str = "0.1.0"

    def __init__(self, agent=None):
        self.agent = agent

    @abstractmethod
    def execute(self, **kwargs) -> str:
        pass

    def get_info(self) -> Dict[str, str]:
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version
        }
