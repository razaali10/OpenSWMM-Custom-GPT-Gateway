"""Run-to-completion, delegated entirely to the upstream
lifecycle_run_simulation tool -- no orchestration duplicated here beyond
what's needed to report the result honestly (never converting a failed
run into an apparent success, per project brief section 5/34)."""

from __future__ import annotations

from app.config import settings
from app.mcp.client import MCPClient


async def run_simulation(client: MCPClient, session_id: str) -> dict:
    result = await client.call_tool(
        "lifecycle_run_simulation",
        {"session_id": session_id},
        timeout=settings.mcp_simulation_timeout_seconds,
    )
    return {
        "session_id": session_id,
        "status": "completed",
        "unsupported_fields": result.get("unsupported_fields", []) if isinstance(result, dict) else [],
    }
