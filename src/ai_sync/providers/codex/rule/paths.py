from dataclasses import dataclass
from pathlib import Path


@dataclass
class RuleOutputPaths:
    root: Path

    def subrule_md_file(self, subrule_name: str) -> Path:
        return self.root / f"{subrule_name}.md"


@dataclass
class RuleDeployUserPaths:
    root: Path

    @property
    def agents_md_file(self) -> Path:
        return self.root / ".codex" / "AGENTS.md"


@dataclass
class RuleDeployProjectPaths:
    root: Path

    @property
    def agents_md_file(self) -> Path:
        return self.root / "AGENTS.md"
