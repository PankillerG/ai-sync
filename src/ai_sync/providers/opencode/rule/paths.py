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
    def opencode_dir(self) -> Path:
        return self.root / ".config" / "opencode"

    @property
    def opencode_json_file(self) -> Path:
        return self.opencode_dir / "opencode.json"

    @property
    def rules_dir(self) -> Path:
        return self.opencode_dir / "ai-sync-rules"

    def rule_dir(self, rule_name: str) -> Path:
        return self.rules_dir / rule_name


@dataclass
class RuleDeployProjectPaths:
    root: Path

    @property
    def opencode_json_file(self) -> Path:
        return self.root / "opencode.json"

    @property
    def rules_dir(self) -> Path:
        return self.root / "ai-sync-rules"

    def rule_dir(self, rule_name: str) -> Path:
        return self.rules_dir / rule_name
