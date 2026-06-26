"""Session Management - Save and resume conversations."""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


class Session:
    """Persist conversation sessions."""

    def __init__(self, session_dir: str = ".byte_sessions"):
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(exist_ok=True)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.messages: List[Dict[str, Any]] = []
        self.metadata: Dict[str, Any] = {
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat(),
            "tool_calls": 0,
        }

    def add_message(self, role: str, content: str, **kwargs):
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            **kwargs
        })
        self.metadata["updated"] = datetime.now().isoformat()

    def save(self):
        data = {
            "session_id": self.session_id,
            "metadata": self.metadata,
            "messages": self.messages,
        }
        path = self.session_dir / f"{self.session_id}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load(self, session_id: str) -> bool:
        path = self.session_dir / f"{session_id}.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.session_id = data.get("session_id", session_id)
            self.metadata = data.get("metadata", {})
            self.messages = data.get("messages", [])
            return True
        return False

    def list_sessions(self) -> List[Dict]:
        sessions = []
        for f in sorted(self.session_dir.glob("*.json"), reverse=True)[:20]:
            try:
                with open(f, "r", encoding="utf-8") as jf:
                    data = json.load(jf)
                sessions.append({
                    "id": data.get("session_id", f.stem),
                    "created": data.get("metadata", {}).get("created", ""),
                    "messages": len(data.get("messages", [])),
                })
            except:
                pass
        return sessions

    def clear(self):
        self.messages.clear()

    def get_context(self, limit: int = 20) -> List[Dict]:
        """Get recent messages for LLM context."""
        return self.messages[-limit:]


class ContextManager:
    """Manages context window with smart compression."""

    def __init__(self, max_tokens: int = 8000):
        self.max_tokens = max_tokens

    def compress(self, messages: List[Dict]) -> List[Dict]:
        """Smart compression - keeps system prompt + recent messages."""
        if len(messages) <= 4:
            return messages

        system = [m for m in messages if m.get("role") == "system"]
        recent = messages[-3:] if len(messages) > 3 else messages

        return system + recent
