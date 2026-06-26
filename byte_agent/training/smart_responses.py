"""Smart Response System - Natural language understanding that auto-executes tasks."""

import os
import re
from .code_templates import CodeTemplates


class SmartResponder:
    """Understands natural language and auto-executes tasks."""

    def __init__(self, agent=None):
        self.agent = agent

    def respond(self, user_input: str) -> str:
        text = user_input.strip().lower()

        # --- GREETINGS ---
        if re.match(r"^(hello|hi|hey|yo|sup|howdy|good\s+(morning|evening|afternoon))", text):
            return self._greet()

        if re.search(r"(how are you|what'?s up|how('s| is) it going)", text):
            return self._how_are_you()

        if re.search(r"(who are you|what are you|tell me about yourself|your name)", text):
            return self._about()

        # --- THANKS ---
        if re.search(r"(thank|thanks|thx|ty)", text):
            return self._thanks()

        # --- GOODBYE ---
        if re.search(r"(bye|goodbye|see you|cya|farewell)", text):
            return self._goodbye()

        # --- HELP ---
        if re.search(r"(help|what can you do|what do you do|capabilities|commands)", text):
            return self._help()

        # --- WHAT'S HERE / LIST FILES ---
        if re.search(r"(what'?s here|what (files|projects|stuff) (do i have|are here|you got)|show (me )?(my )?(files|projects|stuff)|list|ls|dir)", text):
            return self._list_projects()

        # --- READ / SHOW FILE ---
        match = re.search(r"(read|open)\s+(file\s+)?([\w.\-\\/]+)", text, re.IGNORECASE)
        if match:
            return self._read_file(match.group(3))
        match = re.search(r"(show|view)\s+me\s+([\w.\-\\/]+)", text, re.IGNORECASE)
        if match:
            return self._read_file(match.group(2))
        # Also handle: "show me the file called hello.py"
        match = re.search(r"(show|view)\s+(me\s+)?(the\s+)?(file\s+)?(called\s+|named\s+)?([\w.\-\\/]+)", text, re.IGNORECASE)
        if match:
            return self._read_file(match.group(6))

        # --- RUN / EXECUTE ---
        match = re.search(r"(run|execute|start|launch)\s+(.+)" , text, re.IGNORECASE)
        if match:
            return self._run(match.group(2))

        # --- GIT ---
        if re.search(r"(git\s+)?(status|changes|modified)", text):
            return self._git_status()
        if re.search(r"(git\s+)?(commit|save|checkpoint)", text):
            return self._git_commit()
        if re.search(r"(git\s+)?(push|upload)", text):
            return self._git_push()
        if re.search(r"(git\s+)?(pull|download|update)", text):
            return self._git_pull()

        # --- NAVIGATION ---
        match = re.search(r"(go to|open (folder|directory)|cd)\s+(.+)" , text, re.IGNORECASE)
        if match:
            return self._cd(match.group(3))
        if re.search(r"(where am i|current (folder|directory)|pwd)", text):
            return self._pwd()

        # --- VERSION ---
        if re.search(r"(what (version|release) (are you|is this)|version)", text):
            return "BYTE AGENT v1.0 - Like Codex, but local and free."

        # --- EXPLAIN CONCEPTS ---
        concept_map = {
            "variable": "A **variable** stores data:\n```python\nname = 'Alice'\nage = 25\nprice = 19.99\n```",
            "function": "A **function** is reusable code:\n```python\ndef greet(name):\n    return f'Hello {name}!'\n\nprint(greet('Alice'))  # Hello Alice!\n```",
            "class": "A **class** is a blueprint for objects:\n```python\nclass Dog:\n    def __init__(self, name):\n        self.name = name\n    def bark(self):\n        return f'{self.name} says woof!'\n\nd = Dog('Rex')\nprint(d.bark())\n```",
            "loop": "A **loop** repeats code:\n```python\nfor i in range(5):\n    print(i)  # 0 1 2 3 4\n\nwhile True:\n    print('infinite')\n    break\n```",
            "array": "An **array/list** stores multiple items:\n```python\nfruits = ['apple', 'banana', 'cherry']\nfruits.append('date')\nprint(fruits[0])  # apple\n```",
            "api": "An **API** lets apps talk to each other over the internet.\n```\nGET /users --> returns all users\nPOST /users --> creates a user\n```",
        }
        for concept, explanation in concept_map.items():
            if concept in text and re.search(rf"(what (is|'s|does)|explain|define|tell me about)\s+(a |an |the )?{concept}", text):
                return explanation + "\n\nWant me to build something using this? Just ask!"

        # --- TEACH / LEARN ---
        if re.search(r"(teach|learn|tutorial|teach me|how to (code|program|build))", text):
            return self._teach(text)

        # --- WIZARD MODE ---
        if re.search(r"(help me (build|make|create|start)|i want to (build|make|create|start)|guide me|wizard|i don'?t know)", text):
            return self._wizard()

        # --- BUILD PROJECTS (auto-create & save files!) ---
        result = self._try_build_project(text)
        if result:
            return result.replace("\U0001f389", ">>").replace("\u2705", "[OK]")

        # --- DEBUG / FIX ---
        if re.search(r"(debug|fix|repair|error|bug|issue|problem|broken|not working)", text):
            return self._debug(text)

        # --- DEFAULT ---
        return self._default(text)

    def _greet(self):
        return "Hey! I'm **BYTE**. I can build apps, websites, games, and more - just tell me what you want!\n\nTry: `create a calculator` or `make me a website` or `help me build something`"

    def _how_are_you(self):
        return "Ready to build something awesome! What can I create for you today?"

    def _about(self):
        return (
            "I'm **BYTE** - your personal AI coding agent!\n\n"
            "**I can build:**\n"
            "- Calculator, Todo app, Games, Websites, Login pages\n"
            "- APIs, Databases, Password generators, Dashboards\n"
            "- Portfolios, Landing pages, and more!\n\n"
            "**Just tell me what you want** and I'll create it for you.\n"
            "No coding knowledge needed - just describe it in plain English!"
        )

    def _thanks(self):
        return "You're welcome! What else should I build for you?"

    def _goodbye(self):
        return "Goodbye! Come back anytime you need something built."

    def _help(self):
        return (
            "**Just tell me what you want in plain English!**\n\n"
            "**Examples:**\n"
            "- `create a calculator` --> builds and saves calculator.py\n"
            "- `make me a website` --> creates a full HTML website\n"
            "- `build a todo app` --> creates a working todo list\n"
            "- `create a login page` --> makes a beautiful login form\n"
            "- `show me my files` --> lists everything here\n"
            "- `read my file` --> shows any file's contents\n"
            "- `teach me python` --> starts a tutorial\n"
            "- `help me build something` --> guided wizard\n\n"
            "**That's it!** Just type what you want and I'll do the rest."
        )

    def _list_projects(self):
        if self.agent:
            return self.agent.list_files(".")
        return "Use: `list files` or `show me my files`"

    def _read_file(self, path):
        if self.agent:
            return self.agent.read_file(path)
        return f"Can't read {path} - agent not connected"

    def _run(self, cmd):
        if self.agent:
            result = self.agent.run_command(cmd)
            return f"Ran: {cmd}\n\n{result}"
        return f"Can't run {cmd} - agent not connected"

    def _git_status(self):
        if self.agent:
            return self.agent.git_status()
        return "Use: `git status`"

    def _git_commit(self):
        return "I'll commit your changes. Say: `commit my changes with message: fixed the bug`"

    def _git_push(self):
        if self.agent:
            return self.agent.run_command("git push")
        return "Can't push - agent not connected"

    def _git_pull(self):
        if self.agent:
            return self.agent.run_command("git pull")
        return "Can't pull - agent not connected"

    def _cd(self, path):
        if self.agent:
            return self.agent.change_directory(path)
        return f"Can't navigate - agent not connected"

    def _pwd(self):
        if self.agent:
            return self.agent.print_working_dir()
        return "Unknown"

    def _teach(self, text):
        if "python" in text:
            return (
                "**Python Basics - Let's learn!**\n\n"
                "**1. Hello World:**\n"
                "```python\nprint('Hello, World!')\n```\n"
                "**2. Variables:**\n"
                "```python\nname = 'BYTE'\nage = 1\n```\n"
                "**3. If/Else:**\n"
                "```python\nif age >= 18:\n    print('Adult')\nelse:\n    print('Minor')\n```\n\n"
                "Want to practice? Say: `create a calculator` and I'll build it with you!"
            )
        elif "javascript" in text:
            return (
                "**JavaScript Basics:**\n"
                "```javascript\n// Hello World\nconsole.log('Hello!');\n\n// Variables\nlet name = 'BYTE';\nconst age = 1;\n\n// Function\nfunction greet(name) {\n    return `Hello, ${name}!`;\n}\n```"
            )
        elif "html" in text:
            return (
                "**HTML Basics:**\n"
                "```html\n<!DOCTYPE html>\n<html>\n<head>\n    <title>My Page</title>\n</head>\n<body>\n    <h1>Hello!</h1>\n    <p>This is a paragraph.</p>\n</body>\n</html>\n```\n\n"
                "Want me to make a full website? Just say: `create a website`"
            )
        else:
            return "I can teach you! Try:\n- `teach me python`\n- `teach me javascript`\n- `teach me html`"

    def _wizard(self):
        return (
            "**BYTE Project Wizard** - Let's build something together!\n\n"
            "What do you want to build?\n\n"
            "1. `calculator` - A working calculator\n"
            "2. `todo app` - A todo list manager\n"
            "3. `website` - A full HTML website\n"
            "4. `game` - A fun snake game\n"
            "5. `login page` - A login form\n"
            "6. `dashboard` - An admin dashboard\n"
            "7. `api` - A REST API backend\n"
            "8. `password generator` - Generate strong passwords\n\n"
            "Just type the number or name of what you want!"
        )

    def _try_build_project(self, text: str) -> str:
        """Try to match the text to a project and auto-build it."""
        projects = [
            # (keywords, language, project_name, filename, template_method)
            (["calculator", "calc"], "python", "Calculator", "calculator.py", CodeTemplates._py_calculator),
            (["todo", "to-do", "task list", "task manager"], "python", "Todo App", "todo.py", CodeTemplates._py_todo),
            (["api", "rest api", "backend", "server"], "python", "REST API", "api.py", CodeTemplates._py_api),
            (["game", "snake", "pygame"], "python", "Snake Game", "game.py", CodeTemplates._py_game),
            (["password", "pass gen", "password generator"], "python", "Password Generator", "password_gen.py", CodeTemplates._py_password),
            (["scraper", "web scraper", "crawler"], "python", "Web Scraper", "scraper.py", CodeTemplates._py_scraper),
            (["weather", "weather app"], "python", "Weather App", "weather.py", CodeTemplates._py_weather),
            (["file organizer", "organizer"], "python", "File Organizer", "organizer.py", CodeTemplates._py_file_organizer),
            (["flask", "web app", "webapp"], "python", "Flask Web App", "app.py", CodeTemplates._py_flask_app),
            (["website", "webpage", "homepage"], "html", "Website", "index.html", CodeTemplates._html_website),
            (["login", "sign in", "signin", "auth", "authentication"], "html", "Login Page", "login.html", CodeTemplates._html_login),
            (["dashboard", "admin panel", "admin"], "html", "Dashboard", "dashboard.html", CodeTemplates._html_dashboard),
            (["portfolio", "personal site", "portfolio website"], "html", "Portfolio", "portfolio.html", CodeTemplates._html_portfolio),
            (["landing", "landing page", "marketing page"], "html", "Landing Page", "landing.html", CodeTemplates._html_landing),
            (["database", "db schema", "sql schema"], "sql", "Database Schema", "schema.sql", CodeTemplates._sql_database),
            (["dockerfile", "docker file", "container"], "docker", "Dockerfile", "Dockerfile", CodeTemplates._dockerfile),
            (["docker compose", "docker-compose"], "docker", "Docker Compose", "docker-compose.yml", CodeTemplates._docker_compose),
            (["react app", "react todo"], "react", "React Todo App", "App.jsx", CodeTemplates._react_app),
            (["react component", "react card", "react button", "react modal"], "react", "React Components", "components.jsx", CodeTemplates._react_component),
        ]

        for keywords, lang, proj, filename, template_fn in projects:
            if any(k in text for k in keywords):
                return self._auto_build(proj, lang, filename, template_fn)

        # Check for generic "create/make/build/write/generate a ... in ..."
        if re.search(r"(create|make|build|write|generate|i want|i need)", text):
            return (
                "I can build many things! Try:\n"
                "- `calculator` - `todo app` - `website` - `game`\n"
                "- `login page` - `dashboard` - `api` - `password generator`\n"
                "- Or say `help me build something` for the wizard!"
            )

        return None

    def _auto_build(self, project_name: str, language: str, filename: str, template_fn) -> str:
        """Automatically create the file and show the user."""
        code = template_fn()
        filepath = filename

        # Auto-save the file
        if self.agent:
            result = self.agent.write_file(filepath, code)
            saved_msg = f"[OK] **Created {filepath}**"
        else:
            saved_msg = f"[FILE] Here's your {project_name}:"

        # For HTML files, tell them they can open in browser
        extra = ""
        if filename.endswith(".html"):
            extra = f"\n\nOpen `{filename}` in your browser to see it!"
        elif filename.endswith(".py"):
            extra = f"\n\nRun it with: `run python {filename}`"

        return (
            f">> **{project_name} built successfully!**{extra}\n\n"
            f"```{language}\n{code}\n```\n\n"
            f"{saved_msg}{extra}"
        )

    def _debug(self, text):
        return (
            "Need help fixing something? Let me help:\n\n"
            "1. **Show me the file:** `read myfile.py`\n"
            "2. **Show me the error:** `run python myfile.py`\n"
            "3. **Describe the problem:** Tell me what's wrong\n\n"
            "Or try: `fix my python code` and I'll help debug it!"
        )

    def _default(self, text):
        # Check if it sounds like they want something
        if re.search(r"(want|need|would like|can you|could you)", text):
            return "Just tell me what you want to build and I'll create it!\nExample: `create a calculator` or `make me a website`"

        return (
            "I'm not sure what you mean. Try:\n"
            "- `create a calculator` - Build something\n"
            "- `help` - See what I can do\n"
            "- `help me build something` - Guided wizard"
        )
