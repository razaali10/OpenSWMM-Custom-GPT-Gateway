from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ToolCallRequest(BaseModel):
    """Generic grouped-dispatcher request body -- deliberately not one
    giant Pydantic model per tool (project brief section 28). The
    upstream MCP server validates the tool's actual arguments against its
    real schema; this gateway only validates that `tool_name` exists and
    belongs to the endpoint's action group before forwarding.

    `arguments` is a JSON-ENCODED STRING, not a nested object -- e.g.
    '{"session_id": "my_session"}'. This is deliberate, not a REST
    convention choice: three separate live tests against a real Custom
    GPT showed the model unable to populate a bare `{type: object,
    additionalProperties: true}` field with no listed `properties` --
    ChatGPT's Actions layer appears to treat such a field as having no
    fillable keys at all, regardless of the field's own examples, and the
    model reported (incorrectly) that the dispatcher itself rejected
    ordinary arguments like session_id. A `string` field has no such
    "closed object" ambiguity: the model can always construct the JSON
    text freely. The gateway parses it back into a dict before forwarding
    to the upstream tool (see app/services/dispatcher.py). Include every
    key from the tool's own input_schema (via getOpenSwmmToolSchema) that
    you want to set -- there is no allow-list and nothing is
    special-cased or rejected, session_id included."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "tool_name": "building_create_model",
                    "arguments": '{"session_id": "my_session"}',
                },
                {
                    "tool_name": "links_set_loss_coeff",
                    "arguments": (
                        '{"session_id": "my_session", "link_id": "C1", '
                        '"inlet": 0.5, "outlet": 1.0, "avg": 0.0}'
                    ),
                },
            ]
        }
    )

    tool_name: str
    arguments: str = Field(
        default="{}",
        description=(
            "JSON-encoded object of the tool's arguments, e.g. "
            '\'{"session_id": "my_session"}\'. Not a nested JSON object -- '
            "a string containing JSON text. See examples."
        ),
    )


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
