"""Decision Engine - Routes user input to the right handler."""

import re
from typing import Optional, Callable, Any


class Intent:
    """Represents what the user wants to do."""

    # Intent types
    GREET = "greet"
    BUILD = "build"
    READ = "read"
    WRITE = "write"
    LIST = "list"
    SEARCH = "search"
    RUN = "run"
    GIT = "git"
    HELP = "help"
    EXPLAIN = "explain"
    TEACH = "teach"
    DEBUG = "debug"
    WIZARD = "wizard"
    NAVIGATE = "navigate"
    QUIT = "quit"
    UNKNOWN = "unknown"

    def __init__(self, type: str, confidence: float = 1.0, data: Any = None):
        self.type = type
        self.confidence = confidence
        self.data = data or {}


class DecisionEngine:
    """Deterministically routes user input to the correct handler."""

    def __init__(self):
        self._routes = self._build_routes()

    def _build_routes(self):
        return [
            # Quit
            (r"^(quit|exit|q|bye|goodbye)$", Intent.QUIT),

            # Greetings
            (r"^(hello|hi|hey|yo|sup|howdy|good\s+(morning|evening|afternoon))", Intent.GREET),
            (r"(how are you|what'?s up|how's it going)", Intent.GREET),
            (r"(who are you|what are you|your name|tell me about yourself)", Intent.GREET),

            # Help
            (r"(help|what can you do|commands|capabilities|what do you do)", Intent.HELP),

            # Wizard
            (r"(help me (build|make|create|start|get started)|i don'?t know|guide me|wizard)", Intent.WIZARD),

            # List files
            (r"(what'?s here|what (files|projects|stuff) (do i have|are here|you got)|show (me )?(my )?(files|projects|stuff|directory)|list|ls|dir)", Intent.LIST),

            # Read file
            (r"(read|open|show|view)\s+(me\s+)?(the\s+)?(file\s+)?(called\s+|named\s+)?([\w.\-\\/]+)", Intent.READ),

            # Write file
            (r"(write|save|create\s+file)\s+([\w.\-\\/]+)\s+", Intent.WRITE),

            # Build project (natural language)
            (r"(create|make|build|generate|i want|i need|could you make|can you build)", Intent.BUILD),

            # Run command
            (r"(run|execute|start|launch)\s+", Intent.RUN),

            # Git
            (r"(git|commit|push|pull|status|branch)", Intent.GIT),

            # Navigate
            (r"(go to|open (folder|directory)|cd)\s+", Intent.NAVIGATE),
            (r"(where am i|current (folder|directory)|pwd)", Intent.NAVIGATE),

            # Explain concepts
            (r"(what is|explain|define|tell me about|how does)\s+(a |an |the )?(variable|function|class|loop|array|list|api|decorator|async|await|promise)", Intent.EXPLAIN),

            # Teach / Learn
            (r"(teach|learn|tutorial|how to|show me how)", Intent.TEACH),

            # Debug
            (r"(debug|fix|repair|error|bug|issue|problem|broken|not working|crash)", Intent.DEBUG),

            # Thanks
            (r"(thank|thanks|thx)", None),  # Handled inline

            # Search
            (r"(search|find|grep|locate)\s+", Intent.SEARCH),

            # Version
            (r"(version|what version)", Intent.HELP),
        ]

    def decide(self, user_input: str) -> Intent:
        """Analyze input and return the intent."""
        text = user_input.strip().lower()

        for pattern, intent_type in self._routes:
            if re.search(pattern, text):
                if intent_type is None:
                    # Inline handlers (like thanks)
                    return Intent(Intent.GREET, 0.9, {"thanks": True})
                return Intent(intent_type, 0.95, {"raw": user_input, "text": text})

        # Default - try to build from any remaining text
        return Intent(Intent.UNKNOWN, 0.3, {"raw": user_input, "text": text})


class ActionRouter:
    """Routes intents to the correct handler function."""

    def __init__(self):
        self.handlers = {}

    def register(self, intent_type: str, handler: Callable):
        self.handlers[intent_type] = handler

    def route(self, intent: Intent) -> str:
        handler = self.handlers.get(intent.type)
        if handler:
            return handler(intent)
        return f"I'm not sure what to do with that. Try 'help' to see what I can do."
