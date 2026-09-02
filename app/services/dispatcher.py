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


async def call_upstream_tool(
    client: MCPClient,
    tool_name: str,
    arguments: dict,
    *,
    timeout: float | None = None,
    retry_safe: bool,
):
    """Call an upstream MCP tool and translate any failure into this
    gateway's own GatewayError vocabulary (structured code/message/details,
    proper 502/504 status) -- the one place BOTH the raw grouped dispatcher
    (below) and every /api/v1/engineering/* convenience endpoint funnel
    through, so neither path silently degrades to a bare 500.

    A long-lived connection (see app/mcp/client.py's docstring) can go
    stale between calls in a way that only surfaces once something tries
    to use it -- observed live as a transport error on a call that had, in
    fact, already reached and completed on the upstream server. Retrying
    is only safe when `retry_safe=True` -- pass that only for operations
    that are idempotent by nature (READ tools; never WRITE,
    SIMULATION_CONTROL, DESTRUCTIVE, or OPTIMIZATION, since the failed
    attempt may have already executed upstream)."""
    try:
        return await client.call_tool(tool_name, arguments, timeout=timeout)
    except MCPTimeoutError as exc:
        raise UpstreamTimeoutError(str(exc), {"tool_name": tool_name}) from exc
    except MCPUpstreamError as exc:
        raise UpstreamMCPError(
            str(exc), {"tool_name": tool_name, "upstream_error_code": exc.tool_error_code}
        ) from exc
    except MCPConnectionError as exc:
        if retry_safe:
            logger.warning("Connection error on '%s', retrying once: %s", tool_name, exc)
            try:
                return await client.call_tool(tool_name, arguments, timeout=timeout)
            except (MCPTimeoutError, MCPUpstreamError, MCPConnectionError) as retry_exc:
                raise UpstreamMCPError(
                    f"Retry after connection error also failed: {retry_exc}",
                    {"tool_name": tool_name},
                ) from retry_exc
        raise UpstreamMCPError(
            f"{exc} -- this call may not be safely retryable, so the request may "
            "have already reached and executed on the upstream server before this "
            "transport failure; verify actual state with a read-only tool "
            "(e.g. getSimulationIntegrity, lifecycle_list_sessions) before assuming "
            "it did not happen, and before retrying it yourself.",
            {"tool_name": tool_name, "possibly_executed": True},
        ) from exc


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

    operation_class = tool.operation_class or "READ"
    timeout = _timeout_for(operation_class)
    arguments = _parse_arguments(request.arguments)

    result = await call_upstream_tool(
        client,
        request.tool_name,
        arguments,
        timeout=timeout,
        retry_safe=(operation_class == "READ"),
    )

    return ToolCallResponse(success=True, tool_name=request.tool_name, result=result)
