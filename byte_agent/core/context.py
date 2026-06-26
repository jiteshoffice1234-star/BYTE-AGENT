"""Simple conversation context tracking."""

import os
from typing import List, Dict, Any


class Context:
    def __init__(self, working_directory: str = ""):
        self.working_directory = working_directory or os.getcwd()
        self.messages: List[Dict[str, str]] = []

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def get_history(self, limit: int = 20) -> List[Dict[str, str]]:
        return self.messages[-limit:]

    def clear(self):
        self.messages.clear()
