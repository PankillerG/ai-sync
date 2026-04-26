from enum import StrEnum


class EntityType(StrEnum):
    SKILL = "skill"
    RULE = "rule"
    # AGENT = "agent"
    # MCP = "mcp"


ENTITY_TYPES = tuple(EntityType)
ENTITY_TYPE_VALUES = [entity.value for entity in ENTITY_TYPES]
