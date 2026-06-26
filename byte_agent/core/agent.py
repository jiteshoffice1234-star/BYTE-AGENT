"""Main ByteAgent class."""

import os
from pathlib import Path
from typing import Optional, List, Dict, Any

from .config import Config
from .context import Context


class ByteAgent:
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config.load()
        self.context = Context(working_directory=os.getcwd())
        self._tools = {}
        self._skills = {}
        self._register_default_tools()

    def _register_default_tools(self):
        from ..tools import file_ops, terminal, search, git
        self._tools.update({
            "read_file": file_ops.read_file,
            "write_file": file_ops.write_file,
            "edit_file": file_ops.edit_file,
            "list_files": file_ops.list_files,
            "run_command": terminal.run_command,
            "search_files": search.search_files,
            "grep_content": search.grep_content,
            "git_status": git.git_status,
            "git_commit": git.git_commit,
            "git_diff": git.git_diff,
        })

    def process_input(self, user_input: str) -> str:
        self.context.add_message("user", user_input)

        response = self._generate_response(user_input)

        self.context.add_message("assistant", response)
        return response

    def _generate_response(self, user_input: str) -> str:
        system_prompt = self._build_system_prompt()
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.context.get_history())

        provider = self.config.model_provider.lower()

        if provider == "demo":
            return self._demo_response(user_input)
        elif provider == "ollama":
            return self._call_ollama(messages)
        elif provider == "openai":
            return self._call_openai(messages)
        else:
            return self._call_openai_compatible(messages)

    def _demo_response(self, user_input: str) -> str:
        """Demo mode - responds without AI."""
        user_lower = user_input.lower()

        if any(w in user_lower for w in ["hello", "hi", "hey"]):
            return f"Hello! I'm {self.config.agent_name}, your coding assistant. How can I help?"
        elif "help" in user_lower:
            return """I can help you with:
- Reading, writing, and editing files
- Running terminal commands
- Searching code
- Git operations
- Code review

Just ask me anything!"""
        elif "list files" in user_lower or "what files" in user_lower:
            files = self._tools["list_files"](".")
            return "Files in current directory:\n" + "\n".join(files[:20])
        elif "read" in user_lower:
            return "Tell me which file you'd like me to read."
        elif "git" in user_lower:
            return self._tools["git_status"]()
        elif "who are you" in user_lower:
            return f"I'm {self.config.agent_name}, a local AI coding agent. I'm running in demo mode right now."
        else:
            return f"I heard: '{user_input}'\n\nI'm in demo mode. To use full AI, set up Ollama or add an OpenAI API key."

    def _call_ollama(self, messages: List[Dict]) -> str:
        try:
            import httpx
            url = f"{self.config.base_url or 'http://localhost:11434'}/api/chat"
            payload = {
                "model": self.config.model,
                "messages": messages,
                "stream": False
            }
            with httpx.Client(timeout=120) as client:
                response = client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("message", {}).get("content", "No response")
        except Exception as e:
            return f"Ollama error: {e}\n\nMake sure Ollama is running: ollama serve"

    def _call_openai(self, messages: List[Dict]) -> str:
        try:
            from openai import OpenAI
            client = OpenAI(
                api_key=self.config.api_key or os.getenv("OPENAI_API_KEY"),
                base_url=self.config.base_url
            )
            response = client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI error: {e}"

    def _call_openai_compatible(self, messages: List[Dict]) -> str:
        try:
            import httpx
            url = f"{self.config.base_url}/v1/chat/completions"
            headers = {"Authorization": f"Bearer {self.config.api_key}"}
            payload = {
                "model": self.config.model,
                "messages": messages,
                "temperature": 0.7
            }
            with httpx.Client(timeout=120) as client:
                response = client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"API error: {e}"

    def _build_system_prompt(self) -> str:
        return f"""You are {self.config.agent_name}, a personalized AI coding agent.
You help with coding, debugging, file operations, and software development.
Personality: {self.config.personality}
Working directory: {self.context.working_directory}

Available tools: {', '.join(self._tools.keys())}

Respond concisely and helpfully. When asked to perform actions, use the appropriate tools."""

    def execute_tool(self, tool_name: str, **kwargs) -> Any:
        if tool_name in self._tools:
            return self._tools[tool_name](**kwargs)
        return f"Unknown tool: {tool_name}"
