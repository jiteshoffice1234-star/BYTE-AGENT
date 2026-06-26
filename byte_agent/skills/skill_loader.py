"""Skill loader and manager."""

import importlib
import os
from pathlib import Path
from typing import Dict, List, Optional

from .base_skill import BaseSkill


class SkillLoader:
    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = Path(skills_dir)
        self.skills: Dict[str, BaseSkill] = {}

    def discover_skills(self) -> List[str]:
        if not self.skills_dir.exists():
            return []
        return [
            d.name for d in self.skills_dir.iterdir()
            if d.is_dir() and (d / "skill.py").exists()
        ]

    def load_skill(self, name: str, agent=None) -> Optional[BaseSkill]:
        try:
            module_path = self.skills_dir / name / "skill.py"
            spec = importlib.util.spec_from_file_location(f"skill_{name}", module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "Skill"):
                skill = module.Skill(agent=agent)
                self.skills[name] = skill
                return skill
        except Exception as e:
            print(f"Error loading skill {name}: {e}")
        return None

    def load_all(self, agent=None) -> Dict[str, BaseSkill]:
        for name in self.discover_skills():
            self.load_skill(name, agent)
        return self.skills

    def get_skill(self, name: str) -> Optional[BaseSkill]:
        return self.skills.get(name)
