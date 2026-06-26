"""BYTE AGENT CLI - Like Codex, but local."""

import sys
import os
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.table import Table

from .core.agent import ByteAgent
from .core.config import Config


console = Console()


def banner():
    b = """
    ===============================================
       BBBB  Y   Y TTTTT EEEE
       B   B  Y Y    T   E
       BBBB    Y     T   EEE
       B   B   Y     T   E
       BBBB    Y     T   EEEE
    ===============================================
       v0.1.0 - Local Coding Agent
       Like Codex, but on YOUR machine
    ===============================================
    """
    console.print(Panel(b.strip(), style="bold cyan"))


def main():
    banner()
    config = Config.load()
    agent = ByteAgent(config)
    cwd_display = agent.context.working_directory
    console.print(f"[green]>> Connected:[/green] {cwd_display}")
    console.print("[dim]>> Type 'help' for commands, 'quit' to exit[/dim]\n")

    while True:
        try:
            short = os.path.basename(agent.context.working_directory) or agent.context.working_directory
            inp = input(f"[{short}]> ")
        except (EOFError, KeyboardInterrupt):
            break

        if not inp.strip():
            continue

        response = agent.process_input(inp)

        if response == "EXIT":
            break

        if response.startswith("--- ") and "lines)" in response:
            console.print(Syntax(response, "python", theme="monokai", line_numbers=True))
        elif response.startswith("Contents of"):
            console.print(Panel(response, title="Files", border_style="green"))
        elif response.startswith("Error") or response.startswith("STDERR"):
            console.print(Panel(response, title="Error", border_style="red"))
        elif response.startswith("```"):
            lines = response.split("\n")
            lang = lines[0].replace("```", "").strip()
            code = "\n".join(lines[1:-1])
            console.print(Syntax(code, lang or "python", theme="monokai"))
        else:
            console.print(Panel(Markdown(response), title="BYTE", border_style="cyan"))
        console.print()

    console.print("[yellow]>> BYTE AGENT disconnected[/yellow]")


if __name__ == "__main__":
    main()
