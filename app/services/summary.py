"""Composes the other engineering services into one concise summary --
never re-derives their logic (project brief: "orchestrate underlying MCP
tools", "do not duplicate SWMM calculations"). Always carries an explicit
limitations disclaimer, matching the sibling REST gateway's own
engineering-integrity posture: never claim compliance/certification."""

from __future__ import annotations

from app.mcp.client import MCPClient
from app.services import flooding as flooding_service
from app.services import integrity as integrity_service
from app.services import model as model_service
from app.services import twod as twod_service


async def get_engineering_summary(client: MCPClient, session_id: str) -> dict:
    inventory = await model_service.get_inventory(client, session_id)
    integrity = await integrity_service.get_integrity(client, session_id)
    flooding = await flooding_service.analyze_flooding(client, session_id)

    twod_summary: dict = {"active": False}
    if inventory["twod_active"]:
        twod_summary = await twod_service.get_twod_summary(client, session_id)

    return {
        "session_id": session_id,
        "inventory": inventory,
        "integrity": integrity,
        "flooding": {
            "flooded_node_count": flooding["flooded_node_count"],
        },
        "twod_active": inventory["twod_active"],
        "limitations": [
            "This summary is generated from the actual simulation results above -- it does "
            "not constitute professional engineering certification, municipal code compliance "
            "review, or an approval of any kind.",
            "This gateway composes results from the upstream openswmm.mcp server; it performs "
            "no independent hydraulic calculation of its own.",
        ],
    }
