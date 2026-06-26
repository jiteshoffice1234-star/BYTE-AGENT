"""Example skill: Git Commit."""

from byte_agent.skills.base_skill import BaseSkill
from byte_agent.tools.git import git_status, git_add, git_commit


class Skill(BaseSkill):
    name = "smart_commit"
    description = "Analyzes changes and creates a meaningful commit"
    version = "0.1.0"

    def execute(self, message: str = "") -> str:
        status = git_status()

        if "nothing to commit" in status:
            return "No changes to commit"

        git_add(".")

        if not message:
            message = self._generate_commit_message(status)

        result = git_commit(message)
        return f"Committed: {message}\n{result}"

    def _generate_commit_message(self, status: str) -> str:
        return "Update via BYTE AGENT"
