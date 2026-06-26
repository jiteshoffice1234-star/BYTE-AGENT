"""Example skill: Code Review."""

from byte_agent.skills.base_skill import BaseSkill


class Skill(BaseSkill):
    name = "code_review"
    description = "Reviews code for issues and suggestions"
    version = "0.1.0"

    def execute(self, code: str = "", language: str = "python") -> str:
        if not code:
            return "No code provided for review"

        prompt = f"""Review this {language} code and provide:
1. Any bugs or issues found
2. Code quality suggestions
3. Performance improvements

Code:
```{language}
{code}
```"""

        if self.agent:
            return self.agent._generate_response(prompt)
        return "Agent not connected"
