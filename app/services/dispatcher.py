"""The generic grouped-Action executor.

Every /api/v1/tools/{group} endpoint calls exactly one function here:
validate that `tool_name` exists in the live registry and belongs to
`group`, pick a timeout class from its operation_class, forward the call
to the upstream MCP server, and translate any upstream failure into the
gateway's own error envelope. This is the ONE place tool calls actually
happen -- the per-group API routers are thin wrappers that only fix
`group`.
"""

from __future__ import annotations

import json
import logging

from app.config import settings
from app.errors import (
    ToolNotFoundError,
    UpstreamMCPError,
    UpstreamTimeoutError,
    ValidationErrorGW,
    WrongActionGroupError,
)
from app.logging_config import tool_name_var
from app.mcp.client import MCPClient, MCPConnectionError, MCPTimeoutError, MCPUpstreamError
from app.mcp.registry import MCPToolRegistry
from app.schemas.tools import ToolCallRequest, ToolCallResponse

logger = logging.getLogger("openswmm_gateway.dispatcher")


def _parse_arguments(raw: str) -> dict:
    """`arguments` arrives as a JSON-encoded string, not a nested object --
    see ToolCallRequest's docstring for why (a bare `additionalProperties:
    true` object schema is effectively unfillable through ChatGPT's Actions
    layer, confirmed via repeated live testing)."""
    try:
        parsed = json.loads(raw)
    except (json.JSONDecodeError, TypeError) as exc:
        raise ValidationErrorGW(
            "'arguments' must be a JSON-encoded object string, e.g. "
            '\'{"session_id": "my_session"}\'. Got invalid JSON: ' + str(exc),
            {"arguments": raw},
        ) from exc
    if not isinstance(parsed, dict):
        raise ValidationErrorGW(
            "'arguments' must decode to a JSON object, not a list/string/number.",
            {"arguments": raw},
        )
    return parsed


def _timeout_for(operation_class: str) -> float:
    if operation_class == "SIMULATION_CONTROL":
        return settings.mcp_simulation_timeout_seconds
    if operation_class == "OPTIMIZATION":
        return settings.mcp_optimization_timeout_seconds
    return settings.openswmm_mcp_timeout_seconds


async def dispatch(
    group: str,
    request: ToolCallRequest,
    *,
    registry: MCPToolRegistry,
    client: MCPClient,
) -> ToolCallResponse:
    tool_name_var.set(request.tool_name)

    tool = await registry.get_tool(request.tool_name)
    if tool is None:
        raise ToolNotFoundError(
            f"MCP tool '{request.tool_name}' does not exist on the upstream server.",
            {"tool_name": request.tool_name},
        )

    if tool.action_group != group:
        raise WrongActionGroupError(
            f"'{request.tool_name}' belongs to action group '{tool.action_group}', "
            f"not '{group}'. Call POST /api/v1/tools/{tool.action_group} instead.",
            {"tool_name": request.tool_name, "correct_action_group": tool.action_group},
        )

    timeout = _timeout_for(tool.operation_class or "READ")
    arguments = _parse_arguments(request.arguments)

    try:
        result = await client.call_tool(request.tool_name, arguments, timeout=timeout)
    except MCPTimeoutError as exc:
        raise UpstreamTimeoutError(str(exc), {"tool_name": request.tool_name}) from exc
    except MCPUpstreamError as exc:
        raise UpstreamMCPError(
            str(exc), {"tool_name": request.tool_name, "upstream_error_code": exc.tool_error_code}
        ) from exc
    except MCPConnectionError as exc:
        raise UpstreamMCPError(str(exc), {"tool_name": request.tool_name}) from exc

    return ToolCallResponse(success=True, tool_name=request.tool_name, result=result)
