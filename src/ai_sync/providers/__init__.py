from enum import StrEnum


class ProviderName(StrEnum):
    CLAUDE = "claude"
    CODEX = "codex"
    OPENCODE = "opencode"


PROVIDER_NAME_VALUES = [provider.value for provider in ProviderName]
