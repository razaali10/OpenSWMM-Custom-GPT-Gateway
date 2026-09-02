"""2D surface summary/mass-balance/coupling -- live-only in this
gateway (no snapshot-fallback cache like the sibling REST gateway,
since this gateway has no per-session storage of its own). If the
upstream session has already reached 'ended', these honestly report
{"active": false} -- see the sibling openswmm-mcp-server's
docs/ARCHITECTURE.md "Known engine limitations" #1 for why that happens
and why a caller who needs post-run 2D data should capture it via the
raw /api/v1/tools/twod dispatcher (twod_get_totals/twod_get_stats/etc.)
*before* calling run-simulation to completion.
"""

from __future__ import annotations

from app.mcp.client import MCPClient
from app.services.dispatcher import call_upstream_tool


async def get_twod_summary(client: MCPClient, session_id: str) -> dict:
    mesh = await call_upstream_tool(
        client, "twod_get_mesh_summary", {"session_id": session_id}, retry_safe=True
    )
    if not mesh.get("active"):
        return {"session_id": session_id, "active": False, "mesh": None, "totals": None}
    totals = await call_upstream_tool(client, "twod_get_totals", {"session_id": session_id}, retry_safe=True)
    return {"session_id": session_id, "active": True, "mesh": mesh, "totals": totals}


async def get_twod_mass_balance(client: MCPClient, session_id: str) -> dict:
    mesh = await call_upstream_tool(
        client, "twod_get_mesh_summary", {"session_id": session_id}, retry_safe=True
    )
    if not mesh.get("active"):
        return {"session_id": session_id, "active": False, "terms": {}}
    balance = await call_upstream_tool(
        client, "twod_get_mass_balance", {"session_id": session_id}, retry_safe=True
    )
    return {"session_id": session_id, "active": True, "terms": balance}


async def get_twod_coupling(client: MCPClient, session_id: str) -> dict:
    mesh = await call_upstream_tool(
        client, "twod_get_mesh_summary", {"session_id": session_id}, retry_safe=True
    )
    if not mesh.get("active"):
        return {"session_id": session_id, "active": False, "coupling_map": {}}
    coupling = await call_upstream_tool(
        client, "twod_get_coupling_map", {"session_id": session_id}, retry_safe=True
    )
    return {"session_id": session_id, "active": True, "coupling_map": coupling}
