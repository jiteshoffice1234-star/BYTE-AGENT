"""BYTE AGENT CLI."""

import sys
import os
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory

from .core.agent import ByteAgent
from .core.config import Config


console = Console()


def print_banner():
    banner = """
    ╔═══════════════════════════════════════════╗
    ║          BYTE AGENT v0.1.0                ║
    ║    Local AI Coding Assistant              ║
    ╚═══════════════════════════════════════════╝
    """
    console.print(Panel(banner.strip(), style="bold cyan"))


def main():
    print_banner()

    config = Config.load()
    agent = ByteAgent(config)

    history_path = Path(".byte_history")
    session = PromptSession(history=FileHistory(history_path))

    console.print("[green]Ready! Type your message or 'quit' to exit.[/green]\n")

    while True:
        try:
            user_input = session.prompt("You> ")
        except (EOFError, KeyboardInterrupt):
            break

        if user_input.strip().lower() in ("quit", "exit", "q"):
            break

        if not user_input.strip():
            continue

        with console.status("[bold cyan]Thinking...[/bold cyan]"):
            response = agent.process_input(user_input)

        console.print(Panel(Markdown(response), title="BYTE", border_style="cyan"))
        console.print()

    console.print("[yellow]Goodbye![/yellow]")


if __name__ == "__main__":
    main()
