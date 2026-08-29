"""Dynamic tool registry -- the live upstream MCP server is the sole
source of truth. This module never hand-maintains a static catalog of
the ~565 tools; it lists them from the server and caches that list in
memory for MCP_TOOL_CACHE_TTL_SECONDS, per the project's brief ("do not
persist stale schemas permanently as authoritative data").
"""

from __future__ import annotations

import asyncio
import time
from difflib import SequenceMatcher

from app.config import settings
from app.mcp.client import MCPClient, mcp_client
from app.mcp.models import MCPTool
from app.security import tool_policy


def _get_description(tool) -> str:
    return getattr(tool, "description", None) or ""


def _get_input_schema(tool) -> dict:
    return getattr(tool, "inputSchema", None) or getattr(tool, "input_schema", None) or {}


class MCPToolRegistry:
    def __init__(self, client: MCPClient, ttl_seconds: int) -> None:
        self._client = client
        self._ttl_seconds = ttl_seconds
        self._tools: dict[str, MCPTool] = {}
        self._last_refresh: float = 0.0
        self._lock = asyncio.Lock()

    async def refresh(self, *, force: bool = False) -> None:
        now = time.monotonic()
        if not force and self._tools and (now - self._last_refresh) < self._ttl_seconds:
            return
        async with self._lock:
            now = time.monotonic()
            if not force and self._tools and (now - self._last_refresh) < self._ttl_seconds:
                return
            raw_tools = await self._client.list_tools()
            tools: dict[str, MCPTool] = {}
            for t in raw_tools:
                name = t.name
                tools[name] = MCPTool(
                    name=name,
                    namespace=tool_policy.namespace_of(name),
                    description=_get_description(t),
                    input_schema=_get_input_schema(t),
                    action_group=tool_policy.get_action_group(name),
                    operation_class=tool_policy.get_operation_class(name),
                    destructive=tool_policy.is_destructive(name),
                )
            self._tools = tools
            self._last_refresh = time.monotonic()

    async def list_tools(self) -> list[MCPTool]:
        await self.refresh()
        return list(self._tools.values())

    async def get_tool(self, name: str) -> MCPTool | None:
        await self.refresh()
        return self._tools.get(name)

    async def namespaces(self) -> dict[str, int]:
        tools = await self.list_tools()
        counts: dict[str, int] = {}
        for t in tools:
            counts[t.namespace] = counts.get(t.namespace, 0) + 1
        return dict(sorted(counts.items()))

    async def action_groups(self) -> dict[str, int]:
        tools = await self.list_tools()
        counts: dict[str, int] = {}
        for t in tools:
            group = t.action_group or "core"
            counts[group] = counts.get(group, 0) + 1
        return dict(sorted(counts.items()))

    async def tools_in_group(self, group: str) -> list[MCPTool]:
        tools = await self.list_tools()
        return [t for t in tools if t.action_group == group]

    async def search(
        self, query: str, *, namespace: str | None = None, limit: int = 10
    ) -> list[MCPTool]:
        tools = await self.list_tools()
        if namespace:
            tools = [t for t in tools if t.namespace == namespace]

        query_lower = query.lower()
        scored: list[tuple[float, MCPTool]] = []
        for t in tools:
            score = _lexical_score(query_lower, t)
            if score > 0:
                scored.append((score, t))
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [t for _, t in scored[:limit]]

    def get_action_group(self, tool_name: str) -> str:
        return tool_policy.get_action_group(tool_name)

    def get_operation_class(self, tool_name: str) -> str:
        return tool_policy.get_operation_class(tool_name)


def _lexical_score(query_lower: str, tool: MCPTool) -> float:
    """Simple, dependency-free lexical/fuzzy scoring -- deliberately not
    an embedding search (per the project brief: "a simple high-quality
    lexical/fuzzy search is sufficient initially; do not introduce an
    embedding database unless justified")."""
    name_lower = tool.name.lower()
    desc_lower = tool.description.lower()
    schema_props = " ".join((tool.input_schema.get("properties") or {}).keys()).lower()

    score = 0.0
    if query_lower == name_lower:
        score += 10.0
    if query_lower in name_lower:
        score += 5.0
    for word in query_lower.split():
        if word in name_lower:
            score += 2.0
        if word in tool.namespace.lower():
            score += 1.0
        if word in desc_lower:
            score += 1.0
        if word in schema_props:
            score += 0.5
    score += SequenceMatcher(None, query_lower, name_lower).ratio() * 2.0
    return score


registry = MCPToolRegistry(mcp_client, settings.mcp_tool_cache_ttl_seconds)
