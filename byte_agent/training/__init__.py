"""BYTE AGENT Training Module - Makes BYTE smart like Codex."""

from .prompt import SYSTEM_PROMPT, PERSONALITY_PROMPTS
from .code_templates import CodeTemplates
from .smart_responses import SmartResponder

__all__ = ["SYSTEM_PROMPT", "PERSONALITY_PROMPTS", "CodeTemplates", "SmartResponder"]
