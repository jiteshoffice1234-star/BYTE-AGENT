"""BYTE AGENT v2.0 - Professional AI Coding Agent inspired by OpenCode, Codex CLI, Pi, and Aider."""

import os
import re
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any

from .config import Config
from .context import Context
from .session import Session, ContextManager
from ..engine import DecisionEngine, ActionRouter, Intent
from ..llm import create_provider, LLMProvider
from ..training import SYSTEM_PROMPT, CodeTemplates, SmartResponder


class ByteAgent:
    """Professional coding agent with Decision Engine, Multi-Provider LLM, and Tool System."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config.load()
        self.context = Context(working_directory=os.getcwd())
        self.session = Session()
        self.context_manager = ContextManager(max_tokens=getattr(self.config, "max_context_tokens", 8000))
        self.engine = DecisionEngine()
        self.router = ActionRouter()
        self.responder = SmartResponder(agent=self)

        # Create LLM provider
        self.llm: LLMProvider = create_provider(self.config)

        # Register routes
        self._register_routes()

        # Track state
        self.tool_call_count = 0

    def _register_routes(self):
        self.router.register(Intent.GREET, self._handle_greet)
        self.router.register(Intent.BUILD, self._handle_build)
        self.router.register(Intent.READ, self._handle_read)
        self.router.register(Intent.WRITE, self._handle_write)
        self.router.register(Intent.LIST, self._handle_list)
        self.router.register(Intent.SEARCH, self._handle_search)
        self.router.register(Intent.RUN, self._handle_run)
        self.router.register(Intent.GIT, self._handle_git)
        self.router.register(Intent.HELP, self._handle_help)
        self.router.register(Intent.EXPLAIN, self._handle_explain)
        self.router.register(Intent.TEACH, self._handle_teach)
        self.router.register(Intent.DEBUG, self._handle_debug)
        self.router.register(Intent.WIZARD, self._handle_wizard)
        self.router.register(Intent.NAVIGATE, self._handle_navigate)
        self.router.register(Intent.UNKNOWN, self._handle_unknown)

    def process_input(self, user_input: str) -> str:
        # Store in session
        self.session.add_message("user", user_input)

        # Check quit first
        if user_input.strip().lower() in ("quit", "exit", "q", "bye"):
            return "EXIT"

        # Use Decision Engine
        intent = self.engine.decide(user_input)

        # Route to correct handler
        response = self.router.route(intent)

        # Store response
        self.session.add_message("assistant", response)
        self.tool_call_count += 1

        return response

    def _handle_greet(self, intent: Intent) -> str:
        data = intent.data or {}
        if data.get("thanks"):
            return "You're welcome! What else should I build for you?"

        text = (intent.data or {}).get("text", "")
        if "who" in text or "tell me" in text:
            return (
                "I'm **BYTE AGENT v2.0** - a professional AI coding agent.\n\n"
                "**Architecture:** Decision Engine -> Multi-Provider LLM -> Tool System\n"
                "**Features:** Auto-build, Natural Language, Session Management, Git Integration\n"
                "**Models:** OpenAI, Ollama, Anthropic, LiteLLM, or local mock\n\n"
                "Just tell me what you want to build!"
            )
        return "Hey! I'm **BYTE**. Tell me what you want to build and I'll create it!"

    def _handle_build(self, intent: Intent) -> str:
        text = (intent.data or {}).get("raw", "")

        # Use existing project builder
        projects = [
            (["calculator", "calc"], "python", "Calculator", "calculator.py", CodeTemplates._py_calculator),
            (["todo", "to-do", "task list"], "python", "Todo App", "todo.py", CodeTemplates._py_todo),
            (["api", "rest api", "backend"], "python", "REST API", "api.py", CodeTemplates._py_api),
            (["game", "snake"], "python", "Snake Game", "game.py", CodeTemplates._py_game),
            (["password", "pass gen"], "python", "Password Generator", "password_gen.py", CodeTemplates._py_password),
            (["scraper", "web scraper"], "python", "Web Scraper", "scraper.py", CodeTemplates._py_scraper),
            (["weather"], "python", "Weather App", "weather.py", CodeTemplates._py_weather),
            (["file organizer"], "python", "File Organizer", "organizer.py", CodeTemplates._py_file_organizer),
            (["website", "webpage", "homepage", "site"], "html", "Website", "index.html", CodeTemplates._html_website),
            (["login", "sign in", "auth"], "html", "Login Page", "login.html", CodeTemplates._html_login),
            (["dashboard", "admin panel"], "html", "Dashboard", "dashboard.html", CodeTemplates._html_dashboard),
            (["portfolio"], "html", "Portfolio", "portfolio.html", CodeTemplates._html_portfolio),
            (["landing", "landing page"], "html", "Landing Page", "landing.html", CodeTemplates._html_landing),
            (["flask", "web app"], "python", "Flask Web App", "app.py", CodeTemplates._py_flask_app),
            (["database", "db schema"], "sql", "Database Schema", "schema.sql", CodeTemplates._sql_database),
            (["dockerfile"], "docker", "Dockerfile", "Dockerfile", CodeTemplates._dockerfile),
            (["docker compose"], "docker", "Docker Compose", "docker-compose.yml", CodeTemplates._docker_compose),
            (["react app", "react todo"], "react", "React Todo App", "App.jsx", CodeTemplates._react_app),
            (["react component"], "react", "React Components", "components.jsx", CodeTemplates._react_component),
        ]

        for keywords, lang, proj, filename, template_fn in projects:
            if any(k in text.lower() for k in keywords):
                return self._auto_build(filename, proj, lang, template_fn())

        # No match - try LLM
        return self._try_llm_build(text)

    def _auto_build(self, filename: str, project: str, language: str, code: str) -> str:
        path = Path(self.context.working_directory) / filename
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(code)
        except Exception as e:
            return f"[ERROR] Could not write {filename}: {e}"

        extra = ""
        if filename.endswith(".html"):
            extra = f"\n\nOpen `{filename}` in your browser to see it!"
        elif filename.endswith(".py"):
            extra = f"\n\nRun it with: `python {filename}`"
        elif filename == "schema.sql":
            extra = f"\n\nLoad it: `sqlite3 database.db < {filename}`"

        return (
            f"[DONE] **{project}** built and saved to `{filename}`!{extra}\n\n"
            f"```{language}\n{code}\n```\n\n"
            f"File created: {filename}{extra}"
        )

    def _try_llm_build(self, text: str) -> str:
        """Use LLM to build something not in templates."""
        prompt = f"Generate complete, working code for: {text}\nReturn ONLY the code with a filename comment on line 1."
        result = self.llm.chat([
            {"role": "system", "content": "You are BYTE, a coding agent. Generate complete working code. Format: # filename.ext then the code."},
            {"role": "user", "content": prompt}
        ])
        if result.startswith("[LLM Error") or result.startswith("[Ollama Error"):
            return (
                "I couldn't find a template for that. Try being more specific:\n"
                "- `create a calculator in python`\n"
                "- `make a website`\n"
                "- `build a todo app`\n"
                "- Or say `help me build something` for the wizard"
            )
        return f"[DONE] Here's what I built:\n\n{result}\n\nWant me to save this to a file?"

    def _handle_read(self, intent: Intent) -> str:
        text = (intent.data or {}).get("raw", "")
        match = re.search(r"([\w.\-\\/]+\.\w+)", text)
        if match:
            return self.read_file(match.group(1))
        return "Which file should I read? Say: `read filename.ext`"

    def _handle_write(self, intent: Intent) -> str:
        text = (intent.data or {}).get("raw", "")
        return "Use: `write filename.ext` followed by the content."

    def _handle_list(self, intent: Intent) -> str:
        return self.list_files(".")

    def _handle_search(self, intent: Intent) -> str:
        text = (intent.data or {}).get("raw", "")
        parts = text.split(" ", 1)
        pattern = parts[1] if len(parts) > 1 else ""
        if not pattern:
            return "What should I search for? Say: `find *.py` or `search function main`"
        return self.search_files(pattern)

    def _handle_run(self, intent: Intent) -> str:
        text = (intent.data or {}).get("raw", "")
        parts = text.split(" ", 1)
        cmd = parts[1] if len(parts) > 1 else ""
        if not cmd:
            return "What command should I run? Say: `run python script.py`"
        return self.run_command(cmd)

    def _handle_git(self, intent: Intent) -> str:
        text = (intent.data or {}).get("raw", "").lower()
        if "status" in text:
            return self.git_status()
        if "commit" in text:
            return self.git_commit("Update via BYTE AGENT")
        if "push" in text:
            return self.run_command("git push")
        if "pull" in text:
            return self.run_command("git pull")
        if "diff" in text:
            return self.run_command("git diff")
        if "log" in text:
            return self.run_command("git log --oneline -10")
        return self.git_status()

    def _handle_help(self, intent: Intent) -> str:
        return (
            "**BYTE AGENT v2.0 - Professional Coding Agent**\n\n"
            "**Just say what you want:**\n"
            "- `create a calculator` - Auto-builds and saves\n"
            "- `make a website` - Full HTML site\n"
            "- `build a todo app` - Working todo list\n"
            "- `create a login page` - Beautiful login form\n"
            "- `create a game` - Snake game\n"
            "- `make an API` - REST API backend\n\n"
            "**File operations:**\n"
            "- `read <file>` - View file contents\n"
            "- `show me my files` - List directory\n"
            "- `find *.py` - Search files\n\n"
            "**System:**\n"
            "- `run <command>` - Execute terminal\n"
            "- `git status` - Git operations\n"
            "- `where am i` - Current directory\n\n"
            "**Learn:**\n"
            "- `what is a function?` - Explain concepts\n"
            "- `teach me python` - Tutorial\n"
            "- `help me build something` - Guided wizard"
        )

    def _handle_explain(self, intent: Intent) -> str:
        text = (intent.data or {}).get("text", "")
        concepts = {
            "variable": "A **variable** stores data:\n```python\nname = 'BYTE'\nage = 1\nprice = 19.99\n```",
            "function": "A **function** is reusable code:\n```python\ndef greet(name):\n    return f'Hello {name}!'\n\nprint(greet('Alice'))\n```",
            "class": "A **class** is a blueprint for objects:\n```python\nclass Dog:\n    def __init__(self, name):\n        self.name = name\n    def bark(self):\n        return f'{self.name} says woof!'\n```",
            "loop": "A **loop** repeats code:\n```python\nfor i in range(5):\n    print(i)\n\nwhile True:\n    print('hi')\n    break\n```",
            "list": "A **list** stores multiple items:\n```python\nitems = ['a', 'b', 'c']\nitems.append('d')\nprint(items[0])\n```",
            "api": "An **API** lets apps communicate over the internet.\n```\nGET /users -> returns users\nPOST /users -> creates a user\n```",
        }
        for concept, explanation in concepts.items():
            if concept in text:
                return explanation + "\n\nWant me to build something using this? Just ask!"
        return "I can explain: `what is a function?`, `what is a class?`, `explain a loop`"

    def _handle_teach(self, intent: Intent) -> str:
        text = (intent.data or {}).get("text", "")
        if "python" in text:
            return (
                "**Python Tutorial - Learn by Building:**\n\n"
                "1. Variables: `name = 'BYTE'`\n"
                "2. If/Else:\n```python\nif x > 0:\n    print('positive')\nelse:\n    print('negative')\n```\n"
                "3. Loops:\n```python\nfor i in range(5):\n    print(i)\n```\n\n"
                "**Try building:** `create a calculator` - you'll learn everything!"
            )
        return "I can teach you! Try: `teach me python`"

    def _handle_debug(self, intent: Intent) -> str:
        return (
            "Need help debugging? Here's what I can do:\n\n"
            "1. **Show the file:** `read myfile.py`\n"
            "2. **Run and see errors:** `run python myfile.py`\n"
            "3. **Search for issues:** `grep 'error' myfile.py`\n\n"
            "Tell me what's broken and I'll help fix it!"
        )

    def _handle_wizard(self, intent: Intent) -> str:
        return (
            "**BYTE Project Wizard**\n\n"
            "What do you want to build?\n\n"
            "1. `calculator` - A working calculator\n"
            "2. `todo app` - Todo list manager\n"
            "3. `website` - Full HTML/CSS site\n"
            "4. `game` - Snake game\n"
            "5. `login page` - Login form\n"
            "6. `dashboard` - Admin panel\n"
            "7. `API` - REST API backend\n"
            "8. `password generator` - Strong passwords\n"
            "9. `portfolio` - Personal website\n\n"
            "Just type the number or name!"
        )

    def _handle_navigate(self, intent: Intent) -> str:
        text = (intent.data or {}).get("text", "")
        if "where" in text or "pwd" in text:
            return f"Current location: `{self.context.working_directory}`"
        parts = text.split(" ", 2)
        path = parts[-1] if len(parts) > 1 else ""
        return self.change_directory(path)

    def _handle_unknown(self, intent: Intent) -> str:
        text = (intent.data or {}).get("raw", "")
        return self.responder.respond(text)

    # === TOOL IMPLEMENTATIONS ===

    def read_file(self, path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            lines = content.split("\n")
            out = f"--- {path} ({len(lines)} lines) ---\n"
            for i, line in enumerate(lines[:100], 1):
                out += f"{i:4}: {line}\n"
            if len(lines) > 100:
                out += f"\n... ({len(lines) - 100} more lines)"
            return out
        except FileNotFoundError:
            return f"[NOT FOUND] File: {path}"
        except Exception as e:
            return f"[ERROR] {e}"

    def write_file(self, path: str, content: str) -> str:
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"[OK] Created: {path}"
        except Exception as e:
            return f"[ERROR] {e}"

    def list_files(self, path: str = ".") -> str:
        try:
            p = Path(self.context.working_directory) / path
            if not p.exists():
                return f"[NOT FOUND] {path}"
            items = []
            for item in sorted(p.iterdir()):
                if item.is_dir():
                    items.append(f"  [DIR]  {item.name}/")
                else:
                    size = self._format_size(item.stat().st_size)
                    ext = item.suffix[1:] if item.suffix else "FILE"
                    items.append(f"  [{ext.upper():4s}] {item.name} ({size})")
            return "**Files:**\n" + "\n".join(items) if items else "Empty directory"
        except Exception as e:
            return f"[ERROR] {e}"

    def _format_size(self, size: int) -> str:
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size/1024:.1f} KB"
        return f"{size/1024/1024:.1f} MB"

    def search_files(self, pattern: str) -> str:
        try:
            matches = list(Path(self.context.working_directory).rglob(pattern))
            if not matches:
                return f"No files matching: {pattern}"
            out = f"Found {len(matches)} files:\n"
            for m in matches[:30]:
                out += f"  {m.relative_to(self.context.working_directory)}\n"
            return out
        except Exception as e:
            return f"[ERROR] {e}"

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
                out += f"\n[EXIT] {result.returncode}"
            return out.strip() or "[OK] Done"
        except subprocess.TimeoutExpired:
            return "[TIMEOUT] Command exceeded 60s"
        except Exception as e:
            return f"[ERROR] {e}"

    def git_status(self) -> str:
        return self.run_command("git status")

    def git_commit(self, message: str) -> str:
        self.run_command("git add .")
        return self.run_command(f'git commit -m "{message}"')

    def change_directory(self, path: str) -> str:
        try:
            new = Path(self.context.working_directory) / path
            if new.is_dir():
                self.context.working_directory = str(new.resolve())
                return f"[OK] Now in: {self.context.working_directory}"
            return f"[NOT FOUND] {path}"
        except Exception as e:
            return f"[ERROR] {e}"
