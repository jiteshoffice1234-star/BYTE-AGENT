"""Session management."""

import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class Session:
    def __init__(self, sessions_dir: str = ".byte_sessions"):
        self.sessions_dir = Path(sessions_dir)
        self.sessions_dir.mkdir(exist_ok=True)
        self.current_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.messages: List[Dict[str, Any]] = []

    def add_message(self, role: str, content: str, metadata: Dict[str, Any] = None):
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        })

    def save(self):
        session_file = self.sessions_dir / f"{self.current_session_id}.json"
        with open(session_file, "w") as f:
            json.dump({
                "id": self.current_session_id,
                "messages": self.messages
            }, f, indent=2)

    def load(self, session_id: str) -> bool:
        session_file = self.sessions_dir / f"{session_id}.json"
        if session_file.exists():
            with open(session_file) as f:
                data = json.load(f)
                self.messages = data.get("messages", [])
                self.current_session_id = session_id
                return True
        return False

    def list_sessions(self) -> List[str]:
        return [f.stem for f in self.sessions_dir.glob("*.json")]
