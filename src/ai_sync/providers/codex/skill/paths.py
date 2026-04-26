from dataclasses import dataclass
from pathlib import Path


@dataclass
class SkillPaths:
    root: Path

    @property
    def agents_openai_yaml_file(self) -> Path:
        return self.root / "agents" / "openai.yaml"


@dataclass
class SkillOutputPaths:
    root: Path

    @property
    def skill_md_file(self) -> Path:
        return self.root / "SKILL.md"

    @property
    def agents_openai_yaml_file(self) -> Path:
        return self.root / "agents" / "openai.yaml"


@dataclass
class SkillDeployPaths:
    root: Path

    @property
    def skill_md_file(self) -> Path:
        return self.root / "SKILL.md"

    @property
    def agents_openai_yaml_file(self) -> Path:
        return self.root / "agents" / "openai.yaml"


@dataclass
class SkillDeployUserPaths:
    root: Path

    @property
    def skills_dir(self) -> Path:
        return self.root / ".agents" / "skills"

    def skill_paths(self, skill_name) -> SkillDeployPaths:
        return SkillDeployPaths(self.skills_dir / skill_name)


@dataclass
class SkillDeployProjectPaths:
    root: Path

    @property
    def skills_dir(self) -> Path:
        return self.root / ".agents" / "skills"

    def skill_paths(self, skill_name) -> SkillDeployPaths:
        return SkillDeployPaths(self.skills_dir / skill_name)
