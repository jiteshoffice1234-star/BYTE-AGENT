"""BYTE AGENT - Full Coding Agent like Codex."""

import os
import re
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime

from .config import Config
from .context import Context


class ByteAgent:
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config.load()
        self.context = Context(working_directory=os.getcwd())
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
        response = self._execute_command(user_input)
        self.context.add_message("assistant", response)
        return response

    def _execute_command(self, user_input: str) -> str:
        cmd = user_input.strip().lower()
        parts = user_input.strip().split(maxsplit=1)
        command = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""

        if command in ("read", "cat", "open"):
            return self.read_file(args) if args else "Usage: read <filename>"
        
        elif command in ("write", "save"):
            return self._handle_write(args)
        
        elif command in ("edit", "modify"):
            return self._handle_edit(args)
        
        elif command in ("create", "new", "touch"):
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
        
        elif command == "hello" or command == "hi" or command == "hey":
            return f"Hello! I'm {self.config.agent_name}, your coding agent. Type 'help' to see what I can do."
        
        elif command == "who" and "are" in cmd and "you" in cmd:
            return f"I'm {self.config.agent_name} v0.1.0 - A local coding agent like Codex.\nI can read, write, edit, search files, run commands, and work with git."
        
        else:
            return self._smart_response(user_input)

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
        filename = parts[0]
        old_text = parts[1].replace("\\n", "\n")
        new_text = parts[2].replace("\\n", "\n")
        return self.edit_file(filename, old_text, new_text)

    def _handle_create(self, args: str) -> str:
        if not args:
            return "Usage: create <filename>"
        return self.create_file(args)

    def _handle_grep(self, args: str) -> str:
        parts = args.split(" ", 1)
        if len(parts) < 2:
            return "Usage: grep <pattern> <path>"
        pattern = parts[0]
        path = parts[1]
        results = self.grep_content(pattern, path)
        if not results:
            return f"No matches found for '{pattern}' in {path}"
        output = f"Found {len(results)} matches:\n"
        for r in results[:20]:
            output += f"  {r['file']}:{r['line']}: {r['content']}\n"
        return output

    def _handle_git(self, args: str) -> str:
        parts = args.split(maxsplit=1)
        subcmd = parts[0] if parts else "status"
        git_args = parts[1] if len(parts) > 1 else ""

        if subcmd in ("status", "s", "st"):
            return self.git_status()
        elif subcmd in ("commit", "ci"):
            return self.git_commit(git_args or "Update via BYTE AGENT")
        elif subcmd in ("diff", "d"):
            return self.git_diff()
        elif subcmd in ("log", "l"):
            return self.git_log()
        elif subcmd in ("add", "a"):
            return self.run_command(f"git add {git_args or '.'}")
        elif subcmd in ("push", "p"):
            return self.run_command("git push")
        elif subcmd in ("pull",):
            return self.run_command("git pull")
        elif subcmd in ("branch", "b"):
            return self.run_command(f"git branch {git_args}")
        else:
            return self.run_command(f"git {args}")

    def _show_help(self) -> str:
        return """BYTE AGENT - Coding Agent Commands:

FILE OPERATIONS:
  read <file>           Read file contents
  write <file> <text>   Write content to file
  edit <file> <old> <new>  Replace text in file
  create <file>         Create empty file
  ls / list / files     List files in directory

SEARCH:
  find <pattern>        Find files by name
  grep <text> <path>    Search text in files

TERMINAL:
  run <command>         Execute shell command

GIT:
  git status            Show git status
  git commit <msg>      Commit changes
  git diff              Show changes
  git log               Show commit history
  git add <files>       Stage files
  git push              Push to remote

NAVIGATION:
  cd <path>             Change directory
  pwd                   Show current directory

OTHER:
  help                  Show this help
  quit / exit           Exit BYTE AGENT"""

    def _smart_response(self, user_input: str) -> str:
        lower = user_input.lower()

        if any(w in lower for w in ["create a", "make a", "write a", "generate"]):
            return self._handle_code_request(user_input)
        elif any(w in lower for w in ["fix", "debug", "error", "bug"]):
            return self._handle_debug_request(user_input)
        elif any(w in lower for w in ["explain", "what does", "how does"]):
            return self._handle_explain_request(user_input)
        else:
            return f"I can help with coding tasks. Try:\n- 'read <file>' to view code\n- 'write <file> <content>' to create code\n- 'run <cmd>' to execute commands\n- 'help' for all commands"

    def _handle_code_request(self, user_input: str) -> str:
        lower = user_input.lower()
        if "python" in lower or ".py" in lower:
            return "Tell me what Python code to create. Example:\ncreate hello.py\nThen I'll help you write it."
        elif "javascript" in lower or "js" in lower or ".js" in lower:
            return "Tell me what JavaScript code to create. Example:\ncreate app.js"
        elif "html" in lower:
            return "Tell me what HTML to create. Example:\ncreate index.html"
        else:
            return "What language? Then use:\ncreate <filename>\nwrite <filename> <code>"

    def _handle_debug_request(self, user_input: str) -> str:
        return "To debug, I can:\n1. Read your code: read <file>\n2. Search for errors: grep 'error' .\n3. Run and check: run <command>\n\nShow me the error or file to debug."

    def _handle_explain_request(self, user_input: str) -> str:
        return "To explain code, use:\nread <filename>\nI'll analyze and explain it."

    # Tool implementations
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
            new_content = content.replace(old_text, new_text, 1)
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
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
                    items.append(f"  [FILE] {item.name} ({size} bytes)")
            if not items:
                return f"Empty directory: {path}"
            return f"Contents of {path}:\n" + "\n".join(items)
        except Exception as e:
            return f"Error listing {path}: {e}"

    def search_files(self, pattern: str) -> str:
        try:
            matches = list(Path(".").rglob(pattern))
            if not matches:
                return f"No files matching: {pattern}"
            output = f"Files matching '{pattern}':\n"
            for m in matches[:30]:
                output += f"  {m}\n"
            return output
        except Exception as e:
            return f"Error searching: {e}"

    def grep_content(self, pattern: str, path: str = ".") -> List[Dict]:
        results = []
        try:
            regex = re.compile(pattern, re.IGNORECASE)
            for file_path in Path(path).rglob("*"):
                if file_path.is_file() and file_path.stat().st_size < 1000000:
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            for i, line in enumerate(f, 1):
                                if regex.search(line):
                                    results.append({
                                        "file": str(file_path),
                                        "line": i,
                                        "content": line.strip()[:100]
                                    })
                    except:
                        pass
        except:
            pass
        return results[:50]

    def run_command(self, command: str) -> str:
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.context.working_directory,
                timeout=60
            )
            output = result.stdout
            if result.stderr:
                output += f"\nSTDERR: {result.stderr}"
            if result.returncode != 0:
                output += f"\nExit code: {result.returncode}"
            return output.strip() or "Command executed successfully"
        except subprocess.TimeoutExpired:
            return "Command timed out (60s limit)"
        except Exception as e:
            return f"Error: {e}"

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
