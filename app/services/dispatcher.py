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

import logging

from app.config import settings
from app.errors import ToolNotFoundError, UpstreamMCPError, UpstreamTimeoutError, WrongActionGroupError
from app.logging_config import tool_name_var
from app.mcp.client import MCPClient, MCPConnectionError, MCPTimeoutError, MCPUpstreamError
from app.mcp.registry import MCPToolRegistry
from app.schemas.tools import ToolCallRequest, ToolCallResponse

logger = logging.getLogger("openswmm_gateway.dispatcher")


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

    try:
        result = await client.call_tool(request.tool_name, request.arguments, timeout=timeout)
    except MCPTimeoutError as exc:
        raise UpstreamTimeoutError(str(exc), {"tool_name": request.tool_name}) from exc
    except MCPUpstreamError as exc:
        raise UpstreamMCPError(
            str(exc), {"tool_name": request.tool_name, "upstream_error_code": exc.tool_error_code}
        ) from exc
    except MCPConnectionError as exc:
        raise UpstreamMCPError(str(exc), {"tool_name": request.tool_name}) from exc

    return ToolCallResponse(success=True, tool_name=request.tool_name, result=result)
