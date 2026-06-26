"""Search tools."""

import os
import re
from pathlib import Path
from typing import List, Dict


def search_files(pattern: str, path: str = ".", recursive: bool = True) -> List[str]:
    try:
        p = Path(path)
        if recursive:
            matches = [str(f) for f in p.rglob(pattern)]
        else:
            matches = [str(f) for f in p.glob(pattern)]
        return matches[:50]
    except Exception as e:
        return [f"Error: {e}"]


def grep_content(pattern: str, path: str = ".", include: str = "*") -> List[Dict]:
    results = []
    try:
        regex = re.compile(pattern, re.IGNORECASE)
        for file_path in Path(path).rglob(include):
            if file_path.is_file():
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        for i, line in enumerate(f, 1):
                            if regex.search(line):
                                results.append({
                                    "file": str(file_path),
                                    "line": i,
                                    "content": line.strip()
                                })
                except:
                    pass
    except Exception as e:
        return [{"error": str(e)}]
    return results[:100]
