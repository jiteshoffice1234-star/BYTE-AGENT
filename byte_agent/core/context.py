"""Context management for conversations."""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime


@dataclass
class Message:
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Context:
    messages: List[Message] = field(default_factory=list)
    working_directory: str = ""
    project_info: Dict[str, Any] = field(default_factory=dict)

    def add_message(self, role: str, content: str, **metadata):
        self.messages.append(Message(role=role, content=content, metadata=metadata))

    def get_history(self, limit: int = 50) -> List[Dict[str, str]]:
        recent = self.messages[-limit:]
        return [{"role": m.role, "content": m.content} for m in recent]

    def clear(self):
        self.messages.clear()
