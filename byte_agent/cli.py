"""BYTE AGENT CLI - Like Codex."""

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


def print_banner():
    banner = """
 ___  ___  ________  _________
|\\  \\|\\  \\|\\   __  \\|\\___   ___\\
| \\   __  \\|  \\|\\  \\|___ \\  \\_|
| \\  \\ \\  \\|   \\_\\  \\   \\ \\  \\
| \\  \\_\\  \\|  ___ \\__\\   \\ \\  \\
| \\________\\|\\__\\|__|\\    \\ \\__\\
|_______|____|_______|____|_____|

 v0.1.0 - Local Coding Agent
"""
    console.print(Panel(banner.strip(), style="bold cyan", subtitle="Type 'help' for commands"))


def main():
    print_banner()

    config = Config.load()
    agent = ByteAgent(config)

    console.print(f"[green]Connected to: {agent.context.working_directory}[/green]")
    console.print("[dim]Type 'help' for commands, 'quit' to exit[/dim]\n")

    while True:
        try:
            cwd = os.path.basename(agent.context.working_directory)
            user_input = input(f"[{cwd}]> ")
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input.strip():
            continue

        response = agent.process_input(user_input)

        if response == "EXIT":
            break

        if response.startswith("--- ") and "lines)" in response:
            console.print(Syntax(response, "python", theme="monokai", line_numbers=True))
        elif response.startswith("Contents of"):
            console.print(Panel(response, title="Files", border_style="green"))
        elif response.startswith("Error") or response.startswith("STDERR"):
            console.print(Panel(response, title="Error", border_style="red"))
        elif response.startswith("BYTE AGENT -"):
            console.print(Panel(Markdown(response), title="Help", border_style="yellow"))
        else:
            console.print(Panel(response, title="BYTE", border_style="cyan"))
        console.print()

    console.print("[yellow]Goodbye![/yellow]")


if __name__ == "__main__":
    main()
