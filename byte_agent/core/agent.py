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
            return f"Error: {str(e)}"

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
