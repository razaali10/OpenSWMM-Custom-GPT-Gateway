"""Run-to-completion, delegated entirely to the upstream
lifecycle_run_simulation tool -- no orchestration duplicated here beyond
what's needed to report the result honestly (never converting a failed
run into an apparent success, per project brief section 5/34)."""

from __future__ import annotations

from app.config import settings
from app.mcp.client import MCPClient
from app.services.dispatcher import call_upstream_tool


async def run_simulation(client: MCPClient, session_id: str) -> dict:
    # SIMULATION_CONTROL, like the raw dispatcher's classification --
    # never auto-retried, since a connection failure here may have already
    # reached and started/completed the run upstream (see
    # call_upstream_tool's docstring; this exact ambiguity was observed
    # live during GPT_Smoke_Test.md Part B).
    result = await call_upstream_tool(
        client,
        "lifecycle_run_simulation",
        {"session_id": session_id},
        timeout=settings.mcp_simulation_timeout_seconds,
        retry_safe=False,
    )
    return {
        "session_id": session_id,
        "status": "completed",
        "unsupported_fields": result.get("unsupported_fields", []) if isinstance(result, dict) else [],
    }
