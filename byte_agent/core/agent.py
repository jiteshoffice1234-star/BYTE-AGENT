"""BYTE AGENT - Full Coding Agent like Codex with training."""

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
        self._setup_tools()

    def _setup_tools(self):
        self.tools = {
            "read_file": self.read_file,
            "write_file": self.write_file,
            "edit_file": self.edit_file,
            "create_file": self.create_file,
            "list_files": self.list_files,
            "search_files": self.search_files,
            "grep_content": self.grep_content,
            "run_command": self.run_command,
            "git_status": self.git_status,
            "git_commit": self.git_commit,
            "git_diff": self.git_diff,
            "git_log": self.git_log,
            "cd": self.change_directory,
            "pwd": self.print_working_dir,
        }

    def process_input(self, user_input: str) -> str:
        self.context.add_message("user", user_input)
        response = self._execute(user_input)
        self.context.add_message("assistant", response)
        return response

    def _execute(self, user_input: str) -> str:
        cmd = user_input.strip().lower()
        parts = user_input.strip().split(maxsplit=1)
        command = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""

        if command in ("read", "cat", "open"):
            return self.read_file(args) if args else "Usage: read <filename>"

        elif command in ("write", "save"):
            return self._handle_write(args)

        elif command in ("edit", "modify", "replace"):
            return self._handle_edit(args)

        elif command in ("create", "new", "touch"):
            if args and not args.endswith((".py", ".js", ".ts", ".html", ".css", ".json", ".txt", ".md", ".sql", ".yml", ".yaml", ".toml", ".ini", ".cfg", ".env", ".gitignore", ".dockerfile")):
                return self.responder.respond(user_input)
            return self._handle_create(args)

        elif command in ("ls", "dir", "list", "files"):
            return self.list_files(args or ".")

        elif command in ("find", "search"):
            return self.search_files(args)

        elif command in ("grep", "findtext", "searchtext"):
            return self._handle_grep(args)

        elif command in ("run", "exec", "execute", "cmd", "shell"):
            return self.run_command(args)

        elif command in ("git", "g"):
            return self._handle_git(args)

        elif command in ("cd", "chdir"):
            return self.change_directory(args)

        elif command in ("pwd", "where"):
            return self.print_working_dir()

        elif command in ("help", "h", "?"):
            return self._show_help()

        elif command in ("quit", "exit", "q", "bye"):
            return "EXIT"

        elif command == "version":
            return "BYTE AGENT v0.1.0 - Like Codex, but local."

        else:
            return self.responder.respond(user_input)

    def _handle_write(self, args: str) -> str:
        parts = args.split(" ", 1)
        if len(parts) < 2:
            return "Usage: write <filename> <content>"
        filename = parts[0]
        content = parts[1]
        content = content.replace("\\n", "\n").replace("\\t", "\t")
        return self.write_file(filename, content)

    def _handle_edit(self, args: str) -> str:
        parts = args.split(" ", 2)
        if len(parts) < 3:
            return "Usage: edit <filename> <old_text> <new_text>"
        return self.edit_file(parts[0], parts[1].replace("\\n", "\n"), parts[2].replace("\\n", "\n"))

    def _handle_create(self, args: str) -> str:
        if not args:
            return "Usage: create <filename>"
        return self.create_file(args)

    def _handle_grep(self, args: str) -> str:
        parts = args.split(" ", 1)
        if len(parts) < 2:
            return "Usage: grep <pattern> <path>"
        results = self.grep_content(parts[0], parts[1])
        if not results:
            return f"No matches found"
        output = f"Found {len(results)} matches:\n"
        for r in results[:20]:
            output += f"  {r['file']}:{r['line']}: {r['content']}\n"
        return output

    def _handle_git(self, args: str) -> str:
        parts = args.split(maxsplit=1)
        subcmd = parts[0] if parts else "status"
        git_args = parts[1] if len(parts) > 1 else ""
        cmds = {
            "status": self.git_status,
            "commit": lambda: self.git_commit(git_args or "Update via BYTE AGENT"),
            "diff": self.git_diff,
            "log": self.git_log,
            "add": lambda: self.run_command(f"git add {git_args or '.'}"),
            "push": lambda: self.run_command("git push"),
            "pull": lambda: self.run_command("git pull"),
            "branch": lambda: self.run_command(f"git branch {git_args}"),
        }
        if subcmd in cmds:
            return cmds[subcmd]()
        return self.run_command(f"git {args}")

    def _show_help(self) -> str:
        return (
            "**BYTE AGENT - Like Codex, but local!**\n\n"
            "**BUILD STUFF:**\n"
            "- `create a calculator` - Build a calculator\n"
            "- `create a todo app` - Todo list\n"
            "- `create an API` - REST API\n"
            "- `create a game` - Snake game\n"
            "- `create a website` - Full HTML site\n"
            "- `create a login page` - Login form\n"
            "- `create a password generator` - Password tool\n\n"
            "**CODE COMMANDS:**\n"
            "- `read <file>` - View file (with line numbers!)\n"
            "- `write <file> <content>` - Create/edit file\n"
            "- `edit <file> <old> <new>` - Replace text\n"
            "- `ls` - List files\n"
            "- `find <pattern>` - Search filenames\n"
            "- `grep <text> <path>` - Search file contents\n\n"
            "**SYSTEM:**\n"
            "- `run <command>` - Execute terminal command\n"
            "- `git status` - Git operations\n"
            "- `cd <dir>` - Navigate\n"
            "- `pwd` - Current directory\n\n"
            "**LEARN:**\n"
            "- `explain a function` - Learn concepts\n"
            "- `teach me python` - Start tutorial\n"
            "- `what is a variable?` - Quick explainer"
        )

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
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Created: {path}"
        except Exception as e:
            return f"Error writing {path}: {e}"

    def edit_file(self, path: str, old_text: str, new_text: str) -> str:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if old_text not in content:
                return f"Text not found in {path}"
            with open(path, "w", encoding="utf-8") as f:
                f.write(content.replace(old_text, new_text, 1))
            return f"Edited: {path}"
        except Exception as e:
            return f"Error editing {path}: {e}"

    def create_file(self, path: str) -> str:
        if os.path.exists(path):
            return f"File already exists: {path}"
        return self.write_file(path, "")

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
                    size = item.stat().st_size
                    name = item.name
                    items.append(f"  [FILE] {name} ({size} bytes)")
            if not items:
                return f"Empty directory"
            return f"Contents of {path}:\n" + "\n".join(items)
        except Exception as e:
            return f"Error: {e}"

    def search_files(self, pattern: str) -> str:
        try:
            matches = list(Path(".").rglob(pattern))
            if not matches:
                return f"No files matching: {pattern}"
            out = f"Files matching '{pattern}':\n"
            for m in matches[:30]:
                out += f"  {m}\n"
            return out
        except Exception as e:
            return f"Error: {e}"

    def grep_content(self, pattern: str, path: str = ".") -> List[Dict]:
        results = []
        try:
            regex = re.compile(pattern, re.IGNORECASE)
            for fp in Path(path).rglob("*"):
                if fp.is_file() and fp.stat().st_size < 1_000_000:
                    try:
                        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                            for i, line in enumerate(f, 1):
                                if regex.search(line):
                                    results.append({"file": str(fp), "line": i, "content": line.strip()[:100]})
                    except:
                        pass
        except:
            pass
        return results[:50]

    # === TERMINAL ===

    def run_command(self, command: str) -> str:
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True,
                cwd=self.context.working_directory, timeout=60
            )
            out = result.stdout
            if result.stderr:
                out += f"\nSTDERR: {result.stderr}"
            if result.returncode != 0:
                out += f"\nExit code: {result.returncode}"
            return out.strip() or "Command executed successfully"
        except subprocess.TimeoutExpired:
            return "Command timed out (60s limit)"
        except Exception as e:
            return f"Error: {e}"

    # === GIT ===

    def git_status(self) -> str:
        return self.run_command("git status")

    def git_commit(self, message: str) -> str:
        self.run_command("git add .")
        return self.run_command(f'git commit -m "{message}"')

    def git_diff(self) -> str:
        return self.run_command("git diff")

    def git_log(self) -> str:
        return self.run_command("git log --oneline -10")

    def change_directory(self, path: str) -> str:
        if not path:
            return self.context.working_directory
        try:
            new_path = Path(self.context.working_directory) / path
            if new_path.is_dir():
                self.context.working_directory = str(new_path.resolve())
                return f"Changed to: {self.context.working_directory}"
            return f"Directory not found: {path}"
        except Exception as e:
            return f"Error: {e}"

    def print_working_dir(self) -> str:
        return self.context.working_directory
