"""BYTE AGENT - Your AI Coding Agent. Just type what you want."""

import os
import re
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any

from .config import Config
from .context import Context
from ..training import SYSTEM_PROMPT, PERSONALITY_PROMPTS, CodeTemplates, SmartResponder


class ByteAgent:
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config.load()
        self.context = Context(working_directory=os.getcwd())
        self.responder = SmartResponder(agent=self)

    def process_input(self, user_input: str) -> str:
        self.context.add_message("user", user_input)

        cmd = user_input.strip().lower()

        # Handle direct commands first
        if cmd in ("quit", "exit", "q", "bye"):
            return "EXIT"

        # Everything else goes to smart responder
        response = self.responder.respond(user_input)
        self.context.add_message("assistant", response)
        return response

    # === FILE TOOLS ===

    def read_file(self, path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            lines = content.split("\n")
            output = f"--- {path} ({len(lines)} lines) ---\n"
            for i, line in enumerate(lines[:100], 1):
                output += f"{i:4}: {line}\n"
            if len(lines) > 100:
                output += f"\n... ({len(lines) - 100} more lines)"
            return output
        except FileNotFoundError:
            return f"File not found: {path}"
        except Exception as e:
            return f"Error reading {path}: {e}"

    def write_file(self, path: str, content: str) -> str:
        try:
            filepath = Path(path)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            return f"[OK] Created `{path}` ({filepath.stat().st_size} bytes)"
        except Exception as e:
            return f"Error writing {path}: {e}"

    def list_files(self, path: str = ".") -> str:
        try:
            p = Path(path)
            if not p.exists():
                return f"Directory not found: {path}"
            items = []
            for item in sorted(p.iterdir()):
                if item.is_dir():
                    items.append(f"  [DIR]  {item.name}/")
                else:
                    ext = item.name.split(".")[-1] if "." in item.name else ""
                    tag = {"py": "PY", "js": "JS", "ts": "TS", "html": "HTML", "css": "CSS", "md": "MD", "json": "JSON", "txt": "TXT", "yml": "YML", "yaml": "YAML"}.get(ext, "FILE")
                    size = item.stat().st_size
                    items.append(f"  [{tag:4s}] {item.name} ({self._format_size(size)})")
            if not items:
                return "Empty directory"
            return "**Files here:**\n" + "\n".join(items)
        except Exception as e:
            return f"Error: {e}"

    def _format_size(self, size: int) -> str:
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size/1024:.1f} KB"
        else:
            return f"{size/1024/1024:.1f} MB"

    # === TERMINAL ===

    def run_command(self, command: str) -> str:
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True,
                cwd=self.context.working_directory, timeout=60
            )
            out = result.stdout
            if result.stderr:
                out += f"\n[WARN] {result.stderr}"
            if result.returncode != 0:
                out += f"\n[FAIL] Exit code: {result.returncode}"
            return out.strip() or "[OK] Done"
        except subprocess.TimeoutExpired:
            return "[TIMEOUT] Command timed out (60s limit)"
        except Exception as e:
            return f"[FAIL] Error: {e}"

    # === GIT ===

    def git_status(self) -> str:
        return self.run_command("git status")

    def change_directory(self, path: str) -> str:
        if not path:
            return self.context.working_directory
        try:
            new_path = Path(self.context.working_directory) / path
            if new_path.is_dir():
                self.context.working_directory = str(new_path.resolve())
                return f"[DIR] Now in: {self.context.working_directory}"
            return f"Directory not found: {path}"
        except Exception as e:
            return f"Error: {e}"

    def print_working_dir(self) -> str:
        return f"[LOC] {self.context.working_directory}"
