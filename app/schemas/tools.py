from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ToolCallRequest(BaseModel):
    """Generic grouped-dispatcher request body -- deliberately not one
    giant Pydantic model per tool (project brief section 28). The
    upstream MCP server validates `arguments` against the real tool
    schema; this gateway only validates that `tool_name` exists and
    belongs to the endpoint's action group before forwarding."""

    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class ToolCallResponse(BaseModel):
    success: bool
    tool_name: str
    result: Any = None
    warnings: list[str] = Field(default_factory=list)


class ToolInfo(BaseModel):
    name: str
    namespace: str
    action_group: str
    description: str
    operation_class: str
    destructive: bool


class ToolSchemaResponse(ToolInfo):
    input_schema: dict[str, Any] = Field(default_factory=dict)


class NamespacesResponse(BaseModel):
    tool_count: int
    namespaces: dict[str, int]
    action_groups: dict[str, int]


class ToolSearchRequest(BaseModel):
    query: str
    namespace: str | None = None
    limit: int = Field(default=10, ge=1, le=100)


class ToolSearchResponse(BaseModel):
    matches: list[ToolInfo]
