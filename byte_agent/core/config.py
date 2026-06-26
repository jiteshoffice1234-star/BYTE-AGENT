"""Configuration management."""

import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Config:
    agent_name: str = "BYTE"
    personality: str = "helpful"
    model_provider: str = "openai"
    model: str = "gpt-4"
    api_key: str = ""
    base_url: Optional[str] = None
    theme: str = "cyberpunk"
    memory_enabled: bool = True
    max_context_tokens: int = 8000
    auto_commit: bool = False
    skills_enabled: bool = True
    debug_mode: bool = False
    log_level: str = "INFO"

    @classmethod
    def load(cls, path: str = "config.json") -> "Config":
        config_path = Path(path)
        if config_path.exists():
            with open(config_path) as f:
                data = json.load(f)
            return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
        return cls()

    def save(self, path: str = "config.json"):
        with open(path, "w") as f:
            json.dump(self.__dict__, f, indent=2)
