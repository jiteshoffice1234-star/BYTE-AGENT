"""Persistent memory storage."""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class MemoryStore:
    def __init__(self, storage_path: str = ".byte_memory"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        self.memories: Dict[str, Any] = self._load_memories()

    def _load_memories(self) -> Dict[str, Any]:
        memory_file = self.storage_path / "memories.json"
        if memory_file.exists():
            with open(memory_file) as f:
                return json.load(f)
        return {"facts": [], "preferences": {}, "sessions": []}

    def _save_memories(self):
        memory_file = self.storage_path / "memories.json"
        with open(memory_file, "w") as f:
            json.dump(self.memories, f, indent=2)

    def add_fact(self, fact: str, context: str = ""):
        self.memories["facts"].append({
            "fact": fact,
            "context": context,
            "timestamp": datetime.now().isoformat()
        })
        self._save_memories()

    def set_preference(self, key: str, value: Any):
        self.memories["preferences"][key] = value
        self._save_memories()

    def get_preference(self, key: str, default: Any = None) -> Any:
        return self.memories["preferences"].get(key, default)

    def search_facts(self, query: str) -> List[str]:
        query_lower = query.lower()
        return [
            m["fact"] for m in self.memories["facts"]
            if query_lower in m["fact"].lower()
        ]

    def get_recent_facts(self, limit: int = 10) -> List[str]:
        return [m["fact"] for m in self.memories["facts"][-limit:]]
