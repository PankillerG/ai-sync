from dataclasses import dataclass
from pathlib import Path

from ai_sync.providers import ProviderName


@dataclass
class RulePaths:
    root: Path

    @property
    def providers_dir(self) -> Path:
        return self.root / "providers"

    def provider_dir(self, provider_name: ProviderName) -> Path:
        return self.providers_dir / provider_name


@dataclass
class RuleOutputPaths:
    root: Path

    @property
    def providers_dir(self) -> Path:
        return self.root / "providers"

    def provider_dir(self, provider_name: ProviderName) -> Path:
        return self.providers_dir / provider_name
