"""File operation tools."""

import os
from pathlib import Path
from typing import List, Optional


def read_file(path: str, encoding: str = "utf-8") -> str:
    try:
        with open(path, "r", encoding=encoding) as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"


def write_file(path: str, content: str, encoding: str = "utf-8") -> str:
    try:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding=encoding) as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing file: {e}"


def edit_file(path: str, old_text: str, new_text: str) -> str:
    try:
        content = read_file(path)
        if old_text not in content:
            return f"Text not found in {path}"
        new_content = content.replace(old_text, new_text, 1)
        return write_file(path, new_content)
    except Exception as e:
        return f"Error editing file: {e}"


def list_files(path: str = ".", recursive: bool = False) -> List[str]:
    try:
        p = Path(path)
        if recursive:
            return [str(f.relative_to(path)) for f in p.rglob("*") if f.is_file()]
        else:
            return [str(f) for f in p.iterdir() if f.is_file()]
    except Exception as e:
        return [f"Error: {e}"]
