"""Simulation-integrity reporting -- raw evidence, never a bare
{"status": "passed"} (project brief section 12). overall_status is
derived strictly from continuity-error magnitude, matching the sibling
REST gateway's own verified approach.

analysis_get_mass_balance reports *_continuity_error as a fraction of
total inflow (e.g. 0.003 for 0.3%), not a percentage -- confirmed against
this server's own .rpt output. Convert to percent here so the *_pct
field names and the overall_status thresholds below are both honest."""

from __future__ import annotations

from app.mcp.client import MCPClient


def _to_pct(fraction: float | None) -> float | None:
    return fraction * 100 if fraction is not None else None


async def get_integrity(client: MCPClient, session_id: str) -> dict:
    balance = await client.call_tool("analysis_get_mass_balance", {"session_id": session_id})

    routing_stats = balance.get("routing_stats") or {}
    pct_not_converged = routing_stats.get("pct_not_converged")

    runoff_err_pct = _to_pct(balance.get("runoff_continuity_error"))
    routing_err_pct = _to_pct(balance.get("routing_continuity_error"))

    worst = max((abs(v) for v in (runoff_err_pct, routing_err_pct) if v is not None), default=None)
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
        "runoff_continuity_error_pct": runoff_err_pct,
        "routing_continuity_error_pct": routing_err_pct,
        "max_courant": balance.get("max_courant"),
        "pct_steps_not_converged": pct_not_converged,
        "overall_status": overall_status,
    }
