"""Scenario comparison -- diffs two already-run, already-open upstream
sessions. This gateway does not create/manage scenarios itself (that's a
building_*/editing_* dispatcher job for the caller); it only compares
whatever two session_ids it's given.

analysis_get_mass_balance reports routing_continuity_error as a fraction
of total inflow, not a percentage (see app.services.integrity) -- converted
to percent here so it's directly comparable to getSimulationIntegrity's
*_pct fields and the QAQC_Playbook continuity tiers, even though these
field names don't carry a _pct suffix themselves."""

from __future__ import annotations

from app.mcp.client import MCPClient


async def compare_scenarios(client: MCPClient, session_id_a: str, session_id_b: str) -> dict:
    balance_a = await client.call_tool("analysis_get_mass_balance", {"session_id": session_id_a})
    balance_b = await client.call_tool("analysis_get_mass_balance", {"session_id": session_id_b})

    err_a = balance_a.get("routing_continuity_error")
    err_b = balance_b.get("routing_continuity_error")

    return {
        "session_id_a": session_id_a,
        "session_id_b": session_id_b,
        "routing_continuity_error_a": err_a * 100 if err_a is not None else None,
        "routing_continuity_error_b": err_b * 100 if err_b is not None else None,
    }
