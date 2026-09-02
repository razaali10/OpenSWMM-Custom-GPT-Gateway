from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ToolCallRequest(BaseModel):
    """Generic grouped-dispatcher request body -- deliberately not one
    giant Pydantic model per tool (project brief section 28). The
    upstream MCP server validates `arguments` against the real tool
    schema; this gateway only validates that `tool_name` exists and
    belongs to the endpoint's action group before forwarding.

    `arguments` is a plain flat object with no allow-list: every key from
    the tool's own input_schema (as returned by getOpenSwmmToolSchema) is
    an ordinary key here, including session_id -- nothing is special-cased
    or rejected. A model populating this field from an untyped
    `additionalProperties: true` object with no listed `properties` has
    nothing else to imitate, which is exactly the failure mode the
    `examples` below exist to prevent (see GPT_Smoke_Test.md Part B)."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "tool_name": "building_create_model",
                    "arguments": {"session_id": "my_session"},
                },
                {
                    "tool_name": "links_set_loss_coeff",
                    "arguments": {
                        "session_id": "my_session",
                        "link_id": "C1",
                        "inlet": 0.5,
                        "outlet": 1.0,
                        "avg": 0.0,
                    },
                },
            ]
        }
    )

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
