"""Scenario comparison -- diffs two already-run, already-open upstream
sessions. This gateway does not create/manage scenarios itself (that's a
building_*/editing_* dispatcher job for the caller); it only compares
whatever two session_ids it's given."""

from __future__ import annotations

from app.mcp.client import MCPClient


async def compare_scenarios(client: MCPClient, session_id_a: str, session_id_b: str) -> dict:
    balance_a = await client.call_tool("analysis_get_mass_balance", {"session_id": session_id_a})
    balance_b = await client.call_tool("analysis_get_mass_balance", {"session_id": session_id_b})
    return {
        "session_id_a": session_id_a,
        "session_id_b": session_id_b,
        "routing_continuity_error_a": balance_a.get("routing_continuity_error"),
        "routing_continuity_error_b": balance_b.get("routing_continuity_error"),
    }
