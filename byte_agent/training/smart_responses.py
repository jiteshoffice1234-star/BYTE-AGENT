"""Smart Response System - Makes BYTE understand natural language."""

from .code_templates import CodeTemplates


class SmartResponder:
    """Pattern matches natural language to responses."""

    def __init__(self, agent=None):
        self.agent = agent
        self.patterns = self._init_patterns()

    def _init_patterns(self):
        return [
            # Greetings
            (r"\b(hello|hi|hey|yo|sup|howdy)\b", self._greet),
            (r"\b(good morning|good evening|good afternoon)\b", self._greet_time),
            (r"\b(how are you|what's up|sup)\b", self._greet_response),

            # Identity
            (r"\b(who are you|what are you|tell me about yourself)\b", self._about),
            (r"\b(your name|what is your name)\b", self._name),

            # Code creation patterns
            (r"\b(create|make|build|write|generate)\s+(a\s+)?(python|py)\s+(script|program|app|tool)\b", self._create_python),
            (r"\b(create|make|build|write|generate)\s+(a\s+)?(javascript|js)\s+(script|program|app|tool)\b", self._create_javascript),
            (r"\b(create|make|build|write|generate)\s+(a\s+)?(html|website|webpage|page)\b", self._create_html),
            (r"\b(create|make|build|write|generate)\s+(a\s+)?(react|vue|angular)\s+(app|component|project)\b", self._create_react),

            # Specific projects
            (r"\b(calculator|calc)\b", self._create_calculator),
            (r"\b(todo|to-do|task)\s+(app|list|manager|tracker)\b", self._create_todo),
            (r"\b(api|rest|backend)\s+(api|server|service)\b", self._create_api),
            (r"\b(game|snake|tetris|pacman)\b", self._create_game),
            (r"\b(login|signin|sign-in|auth|authentication)\s+(page|form|system)\b", self._create_login),
            (r"\b(dashboard|admin)\s+(panel|page|dashboard)\b", self._create_dashboard),
            (r"\b(portfolio|personal\s+website)\b", self._create_portfolio),
            (r"\b(password)\s+(generator|gen)\b", self._create_password),
            (r"\b(scraper|scrape|crawl|crawler)\b", self._create_scraper),
            (r"\b(database|db|sqlite|postgres)\s+(schema|setup|create|design)\b", self._create_database),
            (r"\b(docker|containerize|container)\s+(file|compose|setup)\b", self._create_docker),

            # Debug patterns
            (r"\b(debug|fix|repair|solve|error|bug|issue|problem)\b", self._debug),
            (r"\b(error|exception|traceback|crash)\b", self._debug_error),
            (r"\b(syntax|compile)\s+(error|mistake)\b", self._debug_syntax),

            # Explanation patterns
            (r"\b(explain|what does|how does|what is)\s+(this\s+)?(code|function|class|method|line)\b", self._explain_code),
            (r"\b(what is|define|explain)\s+(a\s+)?(variable|function|class|loop|array|object|promise|async|await|decorator|generator|lambda)\b", self._explain_concept),

            # Learning / teaching
            (r"\b(teach|learn|tutorial|guide|how\s+to)\s+(me\s+)?(python|javascript|html|css|react|programming|coding)\b", self._teach),
            (r"\b(learn|study|practice|exercise)\s+(python|javascript|programming)\b", self._learn),

            # File operations
            (r"\b(list|show|view)\s+(all\s+)?(files|directory|folders)\b", self._list_files),
            (r"\b(open|read|show|view)\s+(file\s+)?(\S+\.\w+)\b", self._read_file),

            # Git patterns
            (r"\b(git\s+)?(status|changes|modified)\b", self._git_status),
            (r"\b(git\s+)?(commit|save|checkpoint)\b", self._git_commit),
            (r"\b(git\s+)?(push|upload|sync)\b", self._git_push),
            (r"\b(git\s+)?(pull|download|update)\b", self._git_pull),

            # Terminal patterns
            (r"\b(run|execute|start|launch)\s+(command|script|program|app)\b", self._run_command),
            (r"\b(terminal|shell|cmd|command\s+line)\b", self._terminal_help),

            # Help patterns
            (r"\b(help|commands|what can you do|capabilities)\b", self._help),
            (r"\b(version|what version|latest)\b", self._version),

            # General coding
            (r"\b(code|programming|coding)\b", self._coding_help),
            (r"\b(project|app|application|software)\b", self._project_help),

            # Thanks / appreciation
            (r"\b(thank|thanks|thx|ty|good|great|awesome|perfect)\b", self._thanks),

            # Goodbye
            (r"\b(bye|goodbye|see you|see ya|cya|farewell)\b", self._goodbye),
        ]

    def respond(self, user_input: str) -> str:
        """Match user input to patterns and return response."""
        import re
        for pattern, handler in self.patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                return handler(user_input)
        return self._default(user_input)

    def _greet(self, text):
        return "Hey! I'm BYTE, your local coding agent. What do you want to build today?"

    def _greet_time(self, text):
        return f"Good day! BYTE here, ready to code. What are we building?"

    def _greet_response(self, text):
        return "I'm doing great! Ready to write some code. What can I help you build?"

    def _about(self, text):
        return (
            "I'm **BYTE** - a local AI coding agent that lives on your machine.\n\n"
            "**I can:**\n"
            "- Write code in Python, JavaScript, HTML, CSS, React, SQL, and more\n"
            "- Create complete apps (calculators, todo lists, games, APIs, websites)\n"
            "- Fix bugs and debug errors\n"
            "- Explain code and teach programming\n"
            "- Run terminal commands\n"
            "- Work with git\n"
            "- Search and organize files\n\n"
            "**Try saying:** `'create a calculator'` or `'explain a for loop'`"
        )

    def _name(self, text):
        return "I'm **BYTE** - your local coding agent. Like Codex, but runs entirely on your machine!"

    def _create_python(self, text):
        return "Python! Good choice. What kind of Python project?\n- `create a calculator`\n- `create a todo app`\n- `create an API`\n- `create a game`\n- `create a password generator`"

    def _create_javascript(self, text):
        return "JavaScript! What should I build?\n- `create a todo app`\n- `create a game`\n- `create an API`"

    def _create_html(self, text):
        return "A website! What kind?\n- `create a landing page`\n- `create a login page`\n- `create a dashboard`\n- `create a portfolio`"

    def _create_react(self, text):
        return "React! I can create:\n- `create a react app` (full todo app)\n- `create react components` (Card, Button, Modal)"

    def _create_calculator(self, text):
        return self._offer_code("python", "calculator", "calculator.py", CodeTemplates._py_calculator())

    def _create_todo(self, text):
        return self._offer_code("python", "todo app", "todo.py", CodeTemplates._py_todo())

    def _create_api(self, text):
        return self._offer_code("python", "REST API", "api.py", CodeTemplates._py_api())

    def _create_game(self, text):
        return self._offer_code("python", "Snake game", "game.py", CodeTemplates._py_game())

    def _create_login(self, text):
        return self._offer_code("HTML", "login page", "login.html", CodeTemplates._html_login())

    def _create_dashboard(self, text):
        return self._offer_code("HTML", "dashboard", "dashboard.html", CodeTemplates._html_dashboard())

    def _create_portfolio(self, text):
        return self._offer_code("HTML", "portfolio", "portfolio.html", CodeTemplates._html_portfolio())

    def _create_password(self, text):
        return self._offer_code("python", "password generator", "password_gen.py", CodeTemplates._py_password())

    def _create_scraper(self, text):
        return self._offer_code("python", "web scraper", "scraper.py", CodeTemplates._py_scraper())

    def _create_database(self, text):
        return self._offer_code("SQL", "database schema", "schema.sql", CodeTemplates._sql_database())

    def _create_docker(self, text):
        return (
            "Docker setup! I can create:\n"
            "- `dockerfile` - Multi-stage Dockerfile\n"
            "- `docker compose` - Docker Compose with app + database\n\n"
            "Say: `'create a dockerfile'` or `'docker compose setup'`"
        )

    def _debug(self, text):
        return "I can help debug! What's the issue?\n1. Read the file: `read filename.py`\n2. Search for errors: `run python filename.py`\n3. Tell me the error and I'll suggest fixes"

    def _debug_error(self, text):
        return "Seeing an error? Let me help:\n1. Share the error: paste it or use `run`\n2. Read the file: `read filename.py`\n3. I'll spot the bug and suggest the fix"

    def _debug_syntax(self, text):
        return "Syntax error? Common causes:\n- Missing colon `:` after `if`, `for`, `while`, `def`\n- Missing parenthesis `()`\n- Wrong indentation\n- Missing quotes\n\nSend me the file: `read filename.py`"

    def _explain_code(self, text):
        return "Sure, explain mode! Use:\n`read filename.py`\nI'll show the code with explanations."

    def _explain_concept(self, text):
        lower = text.lower()
        if "variable" in lower:
            return "**Variable**: A container for storing data.\n```python\nname = 'BYTE'        # string\nage = 1              # integer\nprice = 19.99        # float\nis_active = True     # boolean\n```"
        elif "function" in lower:
            return "**Function**: A reusable block of code.\n```python\ndef greet(name):\n    return f'Hello, {name}!'\n\nprint(greet('BYTE'))  # Hello, BYTE!\n```"
        elif "class" in lower:
            return "**Class**: A blueprint for creating objects.\n```python\nclass Dog:\n    def __init__(self, name):\n        self.name = name\n    def bark(self):\n        return f'{self.name} says woof!'\n\ndog = Dog('Buddy')\nprint(dog.bark())  # Buddy says woof!\n```"
        elif "loop" in lower:
            return "**Loop**: Repeat code multiple times.\n```python\n# For loop\nfor i in range(5):\n    print(i)  # 0, 1, 2, 3, 4\n\n# While loop\ncount = 0\nwhile count < 5:\n    print(count)\n    count += 1\n```"
        elif "array" in lower or "list" in lower:
            return "**List**: An ordered collection of items.\n```python\nfruits = ['apple', 'banana', 'cherry']\nfruits.append('date')\nprint(fruits[0])  # apple\nfor f in fruits:\n    print(f)\n```"
        elif "async" in lower or "await" in lower:
            return "**Async/Await**: Handle asynchronous operations.\n```python\nimport asyncio\n\nasync def fetch_data():\n    await asyncio.sleep(1)\n    return 'data loaded!'\n\nasync def main():\n    result = await fetch_data()\n    print(result)\n\nasyncio.run(main())\n```"
        elif "decorator" in lower:
            return "**Decorator**: A function that modifies another function.\n```python\ndef timer(func):\n    def wrapper(*args, **kwargs):\n        import time\n        start = time.time()\n        result = func(*args, **kwargs)\n        print(f'Took {time.time()-start:.2f}s')\n        return result\n    return wrapper\n\n@timer\ndef slow_function():\n    import time\n    time.sleep(1)\n    return 'Done!'\n```"
        return "I can explain programming concepts! Try:\n- `what is a variable?`\n- `explain a function`\n- `what is a class?`\n- `explain async/await`"

    def _teach(self, text):
        lower = text.lower()
        if "python" in lower:
            return (
                "**Python Tutorial** - Let's learn step by step:\n\n"
                "**1. Hello World:**\n"
                "```python\nprint('Hello, World!')\n```\n\n"
                "**2. Variables:**\n"
                "```python\nname = 'BYTE'\nage = 1\n```\n\n"
                "**3. If/Else:**\n"
                "```python\nif age >= 18:\n    print('Adult')\nelse:\n    print('Minor')\n```\n\n"
                "Want me to explain more? Try:\n- `what is a function?`\n- `explain a class`\n- `create a calculator`"
            )
        elif "javascript" in lower:
            return (
                "**JavaScript Tutorial:**\n\n"
                "```javascript\n// Hello World\nconsole.log('Hello!');\n\n// Variables\nlet name = 'BYTE';\nconst age = 1;\n\n// Function\nfunction greet(name) {\n    return `Hello, ${name}!`;\n}\n\n// Arrow function\nconst add = (a, b) => a + b;\n\nconsole.log(greet('BYTE'));\n```"
            )
        return "I can teach programming! Try:\n- `teach me python`\n- `teach me javascript`"

    def _learn(self, text):
        return "Ready to practice! Try:\n1. `create a calculator` - you'll learn functions and logic\n2. `create a todo app` - you'll learn data structures\n3. `explain a loop` - understand iteration"

    def _list_files(self, text):
        if self.agent:
            return self.agent.list_files(".")
        return "Use: `ls` to see files in the current directory."

    def _read_file(self, text):
        import re
        match = re.search(r'(\S+\.\w+)', text)
        if match and self.agent:
            return self.agent.read_file(match.group(1))
        return "Which file should I read? Usage: `read filename.py`"

    def _git_status(self, text):
        if self.agent:
            return self.agent.git_status()
        return "Use: `git status` to see your changes."

    def _git_commit(self, text):
        return "To commit: `git commit your message here`\nThis will add all files and commit."

    def _git_push(self, text):
        return "To push: `git push`"

    def _git_pull(self, text):
        return "To pull: `git pull`"

    def _run_command(self, text):
        return "To run a command: `run python script.py` or `run npm start`"

    def _terminal_help(self, text):
        return "Terminal commands:\n- `run <command>` - execute any shell command\n- `run python --version` - check Python\n- `run node --version` - check Node.js\n- `run dir` (Windows) or `run ls` (Linux/Mac) - list files"

    def _help(self, text):
        return (
            "**BYTE AGENT Commands:**\n\n"
            "**Build Stuff:**\n"
            "- `create a calculator` - Build a calculator app\n"
            "- `create a todo app` - Build a todo list\n"
            "- `create an API` - REST API template\n"
            "- `create a game` - Snake game\n"
            "- `create a website` - Full HTML site\n"
            "- `create a login page` - Login form\n"
            "- `create a password generator` - Password tool\n\n"
            "**Work With Code:**\n"
            "- `read <file>` - View file contents\n"
            "- `write <file> <content>` - Create/edit files\n"
            "- `list files` / `ls` - Show files\n"
            "- `find *.py` - Search files\n\n"
            "**Learn:**\n"
            "- `explain a function` - Learn concepts\n"
            "- `teach me python` - Start tutorial\n"
            "- `what is a variable?` - Quick explanation\n\n"
            "**System:**\n"
            "- `run <command>` - Execute terminal\n"
            "- `git status` - Git operations\n"
            "- `cd <dir>` - Navigate\n"
            "- `help` - This menu"
        )

    def _version(self, text):
        return "**BYTE AGENT v0.1.0** - Like Codex, but local.\nhttps://github.com/jiteshoffice1234-star/BYTE-AGENT"

    def _coding_help(self, text):
        return "I can help with coding! Try:\n- `create a <project>` - Build something\n- `read <file>` - Analyze code\n- `explain <concept>` - Learn\n- `fix` - Debug\n- `help` for all commands"

    def _project_help(self, text):
        return "I can build projects! Try:\n- `create a calculator in python`\n- `create a website`\n- `create a todo app`\n- `create an API`"

    def _thanks(self, text):
        return "You're welcome! What else can I help you build?"

    def _goodbye(self, text):
        return "Goodbye! Come back when you need to build something. Type `quit` to exit."

    def _default(self, text):
        return (
            f"I'm BYTE, your coding agent. I can build, debug, and explain code.\n\n"
            f"**Try saying:**\n"
            f"- `'create a calculator'`\n"
            f"- `'explain a function'`\n"
            f"- `'read config.json'`\n"
            f"- `'run python --version'`\n"
            f"- `'help'` for all commands"
        )

    def _offer_code(self, language, project_name, filename, code):
        """Offer to create a file with generated code."""
        return (
            f"I can create a **{project_name}** in {language}!\n\n"
            f"```{language.lower()}\n{code}\n```\n\n"
            f"Say: `'write {filename} [paste the code above]'`\n"
            f"I'll save it to your machine."
        )
