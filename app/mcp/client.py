"""The gateway's one and only path to Repository A (the existing
openswmm.mcp server) -- a real remote MCP client over its published
streamable-HTTP interface. No openswmm_mcp/openswmm.engine import ever
happens in this repository; this module only ever sees the server through
its network-exposed MCP protocol, exactly like any other MCP client
(Claude Desktop, a ChatGPT connector, HuggingChat, ...).
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from fastmcp import Client
from fastmcp.exceptions import ToolError

from app.config import settings

logger = logging.getLogger("openswmm_gateway.mcp_client")


class MCPUpstreamError(Exception):
    """The upstream MCP server itself rejected/errored a tool call.

    Maps to HTTP 502 at the API layer -- distinct from a timeout (504) or
    a gateway-side validation problem (400/404/422).
    """

    def __init__(self, message: str, tool_error_code: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.tool_error_code = tool_error_code


class MCPTimeoutError(Exception):
    """The upstream MCP server did not respond within the configured
    timeout for this operation class. Maps to HTTP 504."""


class MCPConnectionError(Exception):
    """Could not reach the upstream MCP server at all (DNS/connection
    refused/TLS/etc, as opposed to a tool-level error). Maps to HTTP 502."""


class MCPClient:
    """Owns one persistent connection to the upstream MCP server for the
    gateway's lifetime. Reconnects lazily on the next call if the
    connection drops -- this is a long-lived remote dependency (a
    separately deployed, separately operated server), not something this
    process controls the lifecycle of."""

    def __init__(self, url: str) -> None:
        self._url = url
        self._client: Client | None = None
        self._cm = None
        self._lock = asyncio.Lock()

    async def start(self) -> None:
        await self._connect()

    async def stop(self) -> None:
        await self._disconnect()

    async def _connect(self) -> None:
        self._cm = Client(self._url)
        try:
            self._client = await asyncio.wait_for(
                self._cm.__aenter__(), timeout=settings.openswmm_mcp_timeout_seconds
            )
        except (asyncio.TimeoutError, TimeoutError) as exc:
            self._cm = None
            raise MCPTimeoutError(
                f"Timed out connecting to upstream MCP server at {self._url}"
            ) from exc
        except Exception as exc:  # noqa: BLE001 -- genuinely any connection failure
            self._cm = None
            raise MCPConnectionError(
                f"Could not connect to upstream MCP server at {self._url}: {exc}"
            ) from exc

    async def _disconnect(self) -> None:
        if self._cm is not None:
            try:
                await self._cm.__aexit__(None, None, None)
            except Exception:  # noqa: BLE001 -- best-effort teardown
                pass
            self._cm = None
            self._client = None

    async def _ensure_connected(self) -> Client:
        if self._client is None:
            async with self._lock:
                if self._client is None:
                    await self._connect()
        assert self._client is not None
        return self._client

    async def list_tools(self):
        """Return the live tool list exactly as reported by the upstream
        MCP server -- this is the authoritative source; nothing here is
        cached at this layer (the registry above does its own caching)."""
        client = await self._ensure_connected()
        try:
            return await asyncio.wait_for(
                client.list_tools(), timeout=settings.openswmm_mcp_timeout_seconds
            )
        except (asyncio.TimeoutError, TimeoutError) as exc:
            raise MCPTimeoutError("Timed out listing tools from upstream MCP server") from exc
        except Exception as exc:  # noqa: BLE001
            # A dropped connection surfaces here as a generic transport
            # error; force a reconnect on the *next* call rather than
            # retrying silently now, so a persistently-down upstream fails
            # fast and visibly instead of doubling every request's latency.
            await self._disconnect()
            raise MCPConnectionError(f"Failed to list tools from upstream MCP server: {exc}") from exc

    async def call_tool(
        self, tool_name: str, arguments: dict[str, Any], *, timeout: float | None = None
    ) -> Any:
        """Call a tool on the upstream server and return its structured
        result verbatim (after the same {"result": [...]} single-key
        list-wrapping unwrap used throughout this project -- see
        openswmm-mcp-server's app/mcp_client.py for where this was first
        discovered live against this exact server)."""
        client = await self._ensure_connected()
        effective_timeout = timeout if timeout is not None else settings.openswmm_mcp_timeout_seconds
        try:
            result = await asyncio.wait_for(
                client.call_tool(tool_name, arguments), timeout=effective_timeout
            )
        except (asyncio.TimeoutError, TimeoutError) as exc:
            raise MCPTimeoutError(
                f"Tool call to '{tool_name}' timed out after {effective_timeout}s"
            ) from exc
        except ToolError as exc:
            code = _extract_error_code(str(exc))
            raise MCPUpstreamError(str(exc), tool_error_code=code) from exc
        except Exception as exc:  # noqa: BLE001
            await self._disconnect()
            raise MCPConnectionError(f"Failed to call '{tool_name}': {exc}") from exc

        content = result.structured_content if result.structured_content is not None else result.data
        if isinstance(content, dict) and set(content.keys()) == {"result"}:
            return content["result"]
        return content


def _extract_error_code(message: str) -> str | None:
    import re

    match = re.match(r"^\[([A-Z_]+)\]", message)
    return match.group(1) if match else None


mcp_client = MCPClient(settings.openswmm_mcp_url)
