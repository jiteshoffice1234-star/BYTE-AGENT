"""BYTE AGENT CLI v2.0 - Professional AI Coding Agent."""

import sys
import os
from pathlib import Path

from .core.agent import ByteAgent
from .core.config import Config


def print_box(text, title="BYTE"):
    """ASCII box printer - works on any terminal."""
    w = 58
    lines = text.split("\n")
    safe_lines = []
    for line in lines:
        try:
            safe_lines.append(line.encode("ascii", "replace").decode("ascii"))
        except:
            safe_lines.append("[encoded]")

    print()
    print(f"  {'='*w}")
    print(f"  {title}")
    print(f"  {'='*w}")
    for line in safe_lines:
        if len(line) > w:
            print(f"  {line[:w]}")
            print(f"  {line[w:]}")
        else:
            print(f"  {line}")
    print(f"  {'='*w}")
    print()


def main():
    config_file = Path("config.json")
    config = Config.load(str(config_file) if config_file.exists() else "config.json")

    print()
    print("  ==========================================================")
    print("    BBBB   Y   Y   TTTTT   EEEE                          ")
    print("    B   B   Y Y      T     E     AGENT v2.0                ")
    print("    BBBB     Y       T     EEE                            ")
    print("    B   B    Y       T     E                              ")
    print("    BBBB     Y       T     EEEE  Professional Coding Agent ")
    print("  ==========================================================")
    print()
    print("  Just tell me what you want to build!")
    print("  Examples: 'create a calculator' | 'make a website' | 'help'")
    print()

    agent = ByteAgent(config)

    while True:
        try:
            inp = input("  You> ")
        except (EOFError, KeyboardInterrupt):
            break

        if not inp.strip():
            continue

        response = agent.process_input(inp)

        if response == "EXIT":
            break

        print_box(response)

    print()
    print("  BYTE disconnected. Come back anytime!")
    print()


if __name__ == "__main__":
    main()
