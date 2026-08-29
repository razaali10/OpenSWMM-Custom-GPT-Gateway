"""Simulation-integrity reporting -- raw evidence, never a bare
{"status": "passed"} (project brief section 12). overall_status is
derived strictly from continuity-error magnitude, matching the sibling
REST gateway's own verified approach."""

from __future__ import annotations

from app.mcp.client import MCPClient

_NOT_CONVERGED_PCT_THRESHOLD = 5.0


async def get_integrity(client: MCPClient, session_id: str) -> dict:
    balance = await client.call_tool("analysis_get_mass_balance", {"session_id": session_id})

    routing_stats = balance.get("routing_stats") or {}
    pct_not_converged = routing_stats.get("pct_not_converged")

    runoff_err = balance.get("runoff_continuity_error")
    routing_err = balance.get("routing_continuity_error")

    worst = max((abs(v) for v in (runoff_err, routing_err) if v is not None), default=None)
    if worst is None:
        overall_status = "unknown"
    elif worst <= 5:
        overall_status = "acceptable"
    elif worst <= 10:
        overall_status = "marginal"
    else:
        overall_status = "poor"

    return {
        "session_id": session_id,
        "completed": True,
        "runoff_continuity_error_pct": runoff_err,
        "routing_continuity_error_pct": routing_err,
        "max_courant": balance.get("max_courant"),
        "pct_steps_not_converged": pct_not_converged,
        "overall_status": overall_status,
    }
