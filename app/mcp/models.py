"""Plain data shapes for MCP tool metadata -- independent of fastmcp's own
internal types, so the rest of the app doesn't depend on fastmcp beyond
this one module boundary."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MCPTool:
    name: str
    namespace: str
    description: str
    input_schema: dict[str, Any] = field(default_factory=dict)
    action_group: str | None = None
    operation_class: str | None = None
    destructive: bool = False
