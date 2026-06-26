"""LLM Provider Abstraction - Support any AI model backend."""

import os
import json
import subprocess
from typing import List, Dict, Optional, Any
from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Abstract base for LLM providers."""

    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI / any OpenAI-compatible API."""

    def __init__(self, model: str = "gpt-4", api_key: str = "", base_url: Optional[str] = None):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.base_url = base_url

    @property
    def name(self) -> str:
        return f"openai/{self.model}"

    def chat(self, messages: List[Dict], **kwargs) -> str:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 4096),
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[LLM Error: {e}]"


class OllamaProvider(LLMProvider):
    """Local Ollama models."""

    def __init__(self, model: str = "codellama", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    @property
    def name(self) -> str:
        return f"ollama/{self.model}"

    def chat(self, messages: List[Dict], **kwargs) -> str:
        try:
            import httpx
            url = f"{self.base_url}/api/chat"
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": kwargs.get("temperature", 0.7),
                    "num_predict": kwargs.get("max_tokens", 4096),
                }
            }
            with httpx.Client(timeout=120) as client:
                resp = client.post(url, json=payload)
                resp.raise_for_status()
                data = resp.json()
                return data.get("message", {}).get("content", "[No response]")
        except Exception as e:
            return f"[Ollama Error: {e}]"


class AnthropicProvider(LLMProvider):
    """Anthropic Claude API."""

    def __init__(self, model: str = "claude-3-opus-20240229", api_key: str = ""):
        self.model = model
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY", "")

    @property
    def name(self) -> str:
        return f"anthropic/{self.model}"

    def chat(self, messages: List[Dict], **kwargs) -> str:
        try:
            import httpx
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            # Convert OpenAI-style messages to Anthropic format
            system = ""
            converted = []
            for m in messages:
                if m["role"] == "system":
                    system = m["content"]
                elif m["role"] == "assistant":
                    converted.append({"role": "assistant", "content": m["content"]})
                else:
                    converted.append({"role": "user", "content": m["content"]})

            payload = {
                "model": self.model,
                "max_tokens": kwargs.get("max_tokens", 4096),
                "messages": converted,
            }
            if system:
                payload["system"] = system

            with httpx.Client(timeout=120) as client:
                resp = client.post("https://api.anthropic.com/v1/messages", json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()
                return data["content"][0]["text"]
        except Exception as e:
            return f"[Anthropic Error: {e}]"


class LiteLLMProvider(LLMProvider):
    """LiteLLM-based provider for 100+ models."""

    def __init__(self, model: str = "gpt-4"):
        self.model = model

    @property
    def name(self) -> str:
        return f"litellm/{self.model}"

    def chat(self, messages: List[Dict], **kwargs) -> str:
        try:
            from litellm import completion
            response = completion(
                model=self.model,
                messages=messages,
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 4096),
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[LiteLLM Error: {e}]"


class MockProvider(LLMProvider):
    """Demo mode - no AI needed."""

    def __init__(self):
        self._responses = {
            "hello": "Hey! I'm BYTE. What should we build today?",
            "help": self._help_text(),
            "who": "I'm BYTE AGENT v2.0 - Your local AI coding partner.",
        }

    @property
    def name(self) -> str:
        return "mock/demo"

    def chat(self, messages: List[Dict], **kwargs) -> str:
        last = messages[-1]["content"].lower() if messages else ""
        for key, resp in self._responses.items():
            if key in last:
                return resp
        return self._default_text()

    def _help_text(self):
        return ("I can build anything you describe! Try:\n"
                "- create a calculator\n"
                "- make a website\n"
                "- build a todo app\n"
                "- create a game\n"
                "- help me build something")

    def _default_text(self):
        return ("Tell me what you want to build and I'll create it!\n"
                "Examples: 'create a calculator', 'make a website'")


def create_provider(config) -> LLMProvider:
    """Factory - create the right provider from config."""
    provider = getattr(config, "model_provider", "demo").lower()

    if provider == "openai":
        return OpenAIProvider(
            model=getattr(config, "model", "gpt-4"),
            api_key=getattr(config, "api_key", ""),
            base_url=getattr(config, "base_url", None)
        )
    elif provider == "ollama":
        return OllamaProvider(
            model=getattr(config, "model", "codellama"),
            base_url=getattr(config, "base_url", "http://localhost:11434")
        )
    elif provider == "anthropic":
        return AnthropicProvider(
            model=getattr(config, "model", "claude-3-opus-20240229"),
            api_key=getattr(config, "api_key", "")
        )
    elif provider == "litellm":
        return LiteLLMProvider(model=getattr(config, "model", "gpt-4"))
    else:
        return MockProvider()
