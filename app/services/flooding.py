"""Flooding analysis -- reports MCP-computed evidence only. This gateway
does not attempt the sibling REST gateway's downstream-capacity
root-cause heuristic here; that requires per-node upstream/downstream
link traversal that belongs in a dedicated engineering service if this
gateway later needs it. For now this reports the flooded-node evidence
straight from analysis_get_flooding_summary, honestly scoped.

analysis_get_flooding_summary reports time_flooded in seconds; converted
to hours here to match every other duration this gateway reports."""

from __future__ import annotations

from app.mcp.client import MCPClient


async def analyze_flooding(client: MCPClient, session_id: str) -> dict:
    flooding = await client.call_tool(
        "analysis_get_flooding_summary", {"session_id": session_id, "min_flood_volume": 0.0}
    )
    flooded = [f for f in flooding if f.get("total_flood_volume", 0) > 0]
    return {
        "session_id": session_id,
        "flooded_node_count": len(flooded),
        "flooded_nodes": [
            {
                "node_id": f["node_id"],
                "total_flood_volume": f.get("total_flood_volume"),
                "max_depth": f.get("max_depth"),
                "time_flooded": (
                    f["time_flooded"] / 3600.0 if f.get("time_flooded") is not None else None
                ),
            }
            for f in sorted(flooded, key=lambda f: f.get("total_flood_volume", 0), reverse=True)
        ],
    }
