"""BYTE AGENT CLI - Super simple for non-coders."""

import sys
import os
from pathlib import Path

from .core.agent import ByteAgent
from .core.config import Config


# Detect if running in a real terminal
HAS_TTY = sys.stdin.isatty() and sys.stdout.isatty()

# Try to use rich if possible
if HAS_TTY:
    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.markdown import Markdown
        from rich.syntax import Syntax
        RICH_OK = True
    except:
        RICH_OK = False
else:
    RICH_OK = False


def print_response(response, title="BYTE"):
    """Print response, using rich if available."""
    if RICH_OK:
        try:
            console = Console()
            if response.startswith("--- ") and "lines)" in response:
                console.print(Syntax(response, "python", theme="monokai"))
            elif response.startswith("```"):
                lines = response.split("\n")
                lang = lines[0].replace("```", "").strip()
                code = "\n".join(lines[1:-1])
                console.print(Syntax(code, lang or "python", theme="monokai"))
            else:
                panel = Panel(Markdown(response), title=title, border_style="cyan")
                console.print(panel)
            return
        except:
            pass

    # Plain text fallback
    w = 60
    print()
    print("=" * w)
    print(f"  {title}")
    print("=" * w)
    text = response.encode("ascii", "replace").decode("ascii")
    print(text)
    print("=" * w)
    print()


def banner():
    text = """
    ===========================================
       BBBB   Y   Y   TTTTT   EEEE
       B   B   Y Y      T     E
       BBBB     Y       T     EEE
       B   B    Y       T     E
       BBBB     Y       T     EEEE
    ===========================================
       Your AI Coding Agent
       Just type what you want!
    ===========================================
    """
    if RICH_OK:
        try:
            console = Console()
            console.print(Panel(text.strip(), style="bold cyan"))
            console.print("[green]Examples:[/green] create a calculator | make a website | help")
            print()
            return
        except:
            pass
    print(text.strip())
    print("Examples: create a calculator | make a website | help")
    print()


def main():
    banner()
    config = Config.load()
    agent = ByteAgent(config)

    while True:
        try:
            inp = input("You> ")
        except (EOFError, KeyboardInterrupt):
            break

        if not inp.strip():
            continue

        response = agent.process_input(inp)

        if response == "EXIT":
            break

        print_response(response)

    print()
    print("BYTE disconnected. Come back anytime!")


if __name__ == "__main__":
    main()
