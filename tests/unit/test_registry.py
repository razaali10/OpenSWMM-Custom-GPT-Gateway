"""Registry behavior against a MOCKED MCP client -- no network. Live
discovery against the real upstream is covered separately in
tests/integration/test_live_discovery.py."""

from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from app.mcp.registry import MCPToolRegistry


@dataclass
class FakeUpstreamTool:
    name: str
    description: str = ""
    inputSchema: dict = field(default_factory=dict)


class FakeClient:
    def __init__(self, tools: list[FakeUpstreamTool]) -> None:
        self._tools = tools
        self.list_calls = 0

    async def list_tools(self):
        self.list_calls += 1
        return self._tools


FAKE_TOOLS = [
    FakeUpstreamTool("query_get_node_info", "Get node info", {"properties": {"session_id": {}}}),
    FakeUpstreamTool("links_set_loss_coeff", "Set entrance/exit loss coefficients for a conduit"),
    FakeUpstreamTool("links_get_loss_coeff", "Get loss coefficients"),
    FakeUpstreamTool("gym_start_optimization", "Start an optimization job"),
]


@pytest.mark.asyncio
async def test_registry_builds_classified_tools():
    registry = MCPToolRegistry(FakeClient(FAKE_TOOLS), ttl_seconds=300)
    tools = await registry.list_tools()
    assert len(tools) == 4
    by_name = {t.name: t for t in tools}
    assert by_name["query_get_node_info"].operation_class == "READ"
    assert by_name["query_get_node_info"].action_group == "results"
    assert by_name["links_set_loss_coeff"].operation_class == "WRITE"
    assert by_name["links_set_loss_coeff"].action_group == "hydraulics"
    assert by_name["gym_start_optimization"].operation_class == "OPTIMIZATION"


@pytest.mark.asyncio
async def test_registry_caches_within_ttl():
    client = FakeClient(FAKE_TOOLS)
    registry = MCPToolRegistry(client, ttl_seconds=300)
    await registry.list_tools()
    await registry.list_tools()
    await registry.list_tools()
    assert client.list_calls == 1  # only the first call actually hit the "upstream"


@pytest.mark.asyncio
async def test_registry_force_refresh_bypasses_cache():
    client = FakeClient(FAKE_TOOLS)
    registry = MCPToolRegistry(client, ttl_seconds=300)
    await registry.list_tools()
    await registry.refresh(force=True)
    assert client.list_calls == 2


@pytest.mark.asyncio
async def test_get_tool_returns_none_for_unknown():
    registry = MCPToolRegistry(FakeClient(FAKE_TOOLS), ttl_seconds=300)
    assert await registry.get_tool("does_not_exist") is None
    tool = await registry.get_tool("links_set_loss_coeff")
    assert tool is not None
    assert tool.destructive is False


@pytest.mark.asyncio
async def test_search_matches_the_project_briefs_own_worked_example():
    # Project brief section 4.2's own example query and expected top hit.
    registry = MCPToolRegistry(FakeClient(FAKE_TOOLS), ttl_seconds=300)
    results = await registry.search("change conduit entrance and exit losses", namespace="links")
    assert results
    assert results[0].name == "links_set_loss_coeff"


@pytest.mark.asyncio
async def test_search_respects_namespace_filter():
    # Fuzzy scoring is never exactly zero for two non-empty strings, so
    # assert what the filter actually guarantees: no out-of-namespace
    # tool (gym_start_optimization) can appear, even though its name
    # shares characters with the query.
    registry = MCPToolRegistry(FakeClient(FAKE_TOOLS), ttl_seconds=300)
    results = await registry.search("optimization", namespace="links")
    assert all(t.namespace == "links" for t in results)
    assert "gym_start_optimization" not in {t.name for t in results}


@pytest.mark.asyncio
async def test_namespaces_and_action_groups_counts():
    registry = MCPToolRegistry(FakeClient(FAKE_TOOLS), ttl_seconds=300)
    namespaces = await registry.namespaces()
    assert namespaces == {"gym": 1, "links": 2, "query": 1}
    action_groups = await registry.action_groups()
    assert action_groups == {"hydraulics": 2, "optimization": 1, "results": 1}
