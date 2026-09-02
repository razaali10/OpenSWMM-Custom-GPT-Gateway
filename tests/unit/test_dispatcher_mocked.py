"""Dispatcher logic against a MOCKED MCP client/registry -- no network,
and specifically never a real write/destructive call against the shared
production upstream server, per the project brief's explicit testing
rule (section 22): "Do not execute destructive tests against a
production MCP server. Use mocked MCP responses for write/destructive
operations."
"""

from __future__ import annotations

import pytest

from app.config import settings
from app.errors import (
    ToolNotFoundError,
    UpstreamMCPError,
    UpstreamTimeoutError,
    ValidationErrorGW,
    WrongActionGroupError,
)
from app.mcp.client import MCPConnectionError, MCPTimeoutError, MCPUpstreamError
from app.mcp.models import MCPTool
from app.schemas.tools import ToolCallRequest
from app.services.dispatcher import dispatch


class FakeRegistry:
    def __init__(self, tools: dict[str, MCPTool]) -> None:
        self._tools = tools

    async def get_tool(self, name: str) -> MCPTool | None:
        return self._tools.get(name)


class FakeClient:
    def __init__(self, *, result=None, error: Exception | None = None) -> None:
        self._result = result
        self._error = error
        self.calls: list[tuple[str, dict, float | None]] = []

    async def call_tool(self, tool_name, arguments, *, timeout=None):
        self.calls.append((tool_name, arguments, timeout))
        if self._error is not None:
            raise self._error
        return self._result


class FlakyThenOkClient:
    """Fails with the given error on its first N calls, then succeeds --
    models a persistent connection that goes stale between calls but
    recovers once reconnected on retry."""

    def __init__(self, *, error: Exception, fail_times: int, result=None) -> None:
        self._error = error
        self._fail_times = fail_times
        self._result = result
        self.calls: list[tuple[str, dict, float | None]] = []

    async def call_tool(self, tool_name, arguments, *, timeout=None):
        self.calls.append((tool_name, arguments, timeout))
        if len(self.calls) <= self._fail_times:
            raise self._error
        return self._result


DESTRUCTIVE_TOOL = MCPTool(
    name="editing_delete_object",
    namespace="editing",
    description="Delete a model object",
    action_group="model-builder",
    operation_class="DESTRUCTIVE",
    destructive=True,
)
READ_TOOL = MCPTool(
    name="query_get_node_info",
    namespace="query",
    description="Get node info",
    action_group="results",
    operation_class="READ",
    destructive=False,
)


@pytest.mark.asyncio
async def test_dispatch_success_returns_result():
    registry = FakeRegistry({"query_get_node_info": READ_TOOL})
    client = FakeClient(result={"node_id": "J1"})
    response = await dispatch(
        "results",
        ToolCallRequest(tool_name="query_get_node_info", arguments='{"session_id": "s1"}'),
        registry=registry,
        client=client,
    )
    assert response.success is True
    assert response.result == {"node_id": "J1"}
    assert client.calls == [
        ("query_get_node_info", {"session_id": "s1"}, settings.openswmm_mcp_timeout_seconds)
    ]


@pytest.mark.asyncio
async def test_dispatch_wrong_group_never_calls_upstream():
    registry = FakeRegistry({"editing_delete_object": DESTRUCTIVE_TOOL})
    client = FakeClient(result="should never be reached")
    with pytest.raises(WrongActionGroupError) as exc_info:
        await dispatch(
            "results",  # editing_delete_object actually belongs to model-builder
            ToolCallRequest(tool_name="editing_delete_object", arguments="{}"),
            registry=registry,
            client=client,
        )
    assert exc_info.value.details["correct_action_group"] == "model-builder"
    assert client.calls == []  # the destructive tool must never actually be invoked here


@pytest.mark.asyncio
async def test_dispatch_unknown_tool_is_404():
    registry = FakeRegistry({})
    client = FakeClient()
    with pytest.raises(ToolNotFoundError):
        await dispatch(
            "core",
            ToolCallRequest(tool_name="does_not_exist", arguments="{}"),
            registry=registry,
            client=client,
        )
    assert client.calls == []


@pytest.mark.asyncio
async def test_dispatch_translates_upstream_error():
    registry = FakeRegistry({"query_get_node_info": READ_TOOL})
    client = FakeClient(error=MCPUpstreamError("[SESSION_NOT_FOUND] no such session", "SESSION_NOT_FOUND"))
    with pytest.raises(UpstreamMCPError) as exc_info:
        await dispatch(
            "results",
            ToolCallRequest(tool_name="query_get_node_info", arguments="{}"),
            registry=registry,
            client=client,
        )
    assert exc_info.value.status_code == 502
    assert exc_info.value.details["upstream_error_code"] == "SESSION_NOT_FOUND"


@pytest.mark.asyncio
async def test_dispatch_translates_timeout():
    registry = FakeRegistry({"query_get_node_info": READ_TOOL})
    client = FakeClient(error=MCPTimeoutError("timed out"))
    with pytest.raises(UpstreamTimeoutError) as exc_info:
        await dispatch(
            "results",
            ToolCallRequest(tool_name="query_get_node_info", arguments="{}"),
            registry=registry,
            client=client,
        )
    assert exc_info.value.status_code == 504


@pytest.mark.asyncio
async def test_dispatch_translates_connection_error():
    registry = FakeRegistry({"query_get_node_info": READ_TOOL})
    client = FakeClient(error=MCPConnectionError("connection refused"))
    with pytest.raises(UpstreamMCPError) as exc_info:
        await dispatch(
            "results",
            ToolCallRequest(tool_name="query_get_node_info", arguments="{}"),
            registry=registry,
            client=client,
        )
    assert exc_info.value.status_code == 502


@pytest.mark.asyncio
async def test_dispatch_retries_once_on_connection_error_for_read_tool():
    # READ tools are idempotent, so a stale-connection failure on the
    # first attempt should be transparently recovered by one retry.
    registry = FakeRegistry({"query_get_node_info": READ_TOOL})
    client = FlakyThenOkClient(
        error=MCPConnectionError("connection refused"), fail_times=1, result={"node_id": "J1"}
    )
    response = await dispatch(
        "results",
        ToolCallRequest(tool_name="query_get_node_info", arguments="{}"),
        registry=registry,
        client=client,
    )
    assert response.success is True
    assert response.result == {"node_id": "J1"}
    assert len(client.calls) == 2


@pytest.mark.asyncio
async def test_dispatch_never_retries_destructive_tool_on_connection_error():
    # A DESTRUCTIVE/WRITE/SIMULATION_CONTROL/OPTIMIZATION call must never
    # be silently retried -- the failed attempt may have already executed
    # upstream, and retrying could double-apply it.
    registry = FakeRegistry({"editing_delete_object": DESTRUCTIVE_TOOL})
    client = FlakyThenOkClient(
        error=MCPConnectionError("connection refused"), fail_times=1, result={"status": "deleted"}
    )
    with pytest.raises(UpstreamMCPError) as exc_info:
        await dispatch(
            "model-builder",
            ToolCallRequest(tool_name="editing_delete_object", arguments="{}"),
            registry=registry,
            client=client,
        )
    assert exc_info.value.details.get("possibly_executed") is True
    assert len(client.calls) == 1


@pytest.mark.asyncio
async def test_dispatch_uses_simulation_timeout_class():
    sim_tool = MCPTool(
        name="lifecycle_run_simulation",
        namespace="lifecycle",
        description="Run",
        action_group="core",
        operation_class="SIMULATION_CONTROL",
        destructive=False,
    )
    registry = FakeRegistry({"lifecycle_run_simulation": sim_tool})
    client = FakeClient(result={"status": "completed"})
    await dispatch(
        "core",
        ToolCallRequest(tool_name="lifecycle_run_simulation", arguments="{}"),
        registry=registry,
        client=client,
    )
    assert client.calls[0][2] == settings.mcp_simulation_timeout_seconds


@pytest.mark.asyncio
async def test_dispatch_rejects_malformed_json_arguments():
    # arguments is a JSON-encoded string (see ToolCallRequest's docstring
    # for why) -- garbage text must fail cleanly before ever reaching the
    # upstream client, not crash or silently forward the raw string.
    registry = FakeRegistry({"query_get_node_info": READ_TOOL})
    client = FakeClient(result="should never be reached")
    with pytest.raises(ValidationErrorGW) as exc_info:
        await dispatch(
            "results",
            ToolCallRequest(tool_name="query_get_node_info", arguments="{not valid json"),
            registry=registry,
            client=client,
        )
    assert exc_info.value.status_code == 422
    assert client.calls == []


@pytest.mark.asyncio
async def test_dispatch_rejects_non_object_json_arguments():
    registry = FakeRegistry({"query_get_node_info": READ_TOOL})
    client = FakeClient(result="should never be reached")
    with pytest.raises(ValidationErrorGW):
        await dispatch(
            "results",
            ToolCallRequest(tool_name="query_get_node_info", arguments="[1, 2, 3]"),
            registry=registry,
            client=client,
        )
    assert client.calls == []


@pytest.mark.asyncio
async def test_dispatch_uses_optimization_timeout_class():
    gym_tool = MCPTool(
        name="gym_start_optimization",
        namespace="gym",
        description="Start optimization",
        action_group="optimization",
        operation_class="OPTIMIZATION",
        destructive=False,
    )
    registry = FakeRegistry({"gym_start_optimization": gym_tool})
    client = FakeClient(result={"job_id": "abc"})
    await dispatch(
        "optimization",
        ToolCallRequest(tool_name="gym_start_optimization", arguments="{}"),
        registry=registry,
        client=client,
    )
    assert client.calls[0][2] == settings.mcp_optimization_timeout_seconds
