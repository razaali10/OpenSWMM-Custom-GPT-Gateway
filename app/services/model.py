"""Model inventory/validation -- read-only composition over query_* tools.

Every engineering endpoint in this gateway takes a caller-supplied
`session_id` for an *already open* upstream session. This gateway owns no
file storage of its own (see docs/ARCHITECTURE.md "Known limitation:
model upload") -- opening a model is done through the core dispatcher
(`lifecycle_open_model` via POST /api/v1/tools/core), not through a
dedicated upload endpoint.
"""

from __future__ import annotations

from app.mcp.client import MCPClient


async def get_inventory(client: MCPClient, session_id: str) -> dict:
    summary = await client.call_tool("query_get_system_summary", {"session_id": session_id})
    nodes = await client.call_tool("query_get_node_info", {"session_id": session_id})
    links = await client.call_tool("query_get_link_info", {"session_id": session_id})
    twod = await client.call_tool("twod_get_mesh_summary", {"session_id": session_id})

    node_list = nodes if isinstance(nodes, list) else [nodes]
    link_list = links if isinstance(links, list) else [links]

    def _count(items: list[dict], key: str, value: str) -> int:
        return sum(1 for item in items if item.get(key) == value)

    return {
        "session_id": session_id,
        "counts": {
            "subcatchments": summary.get("subcatchment_count", 0),
            "junctions": _count(node_list, "node_type", "JUNCTION"),
            "outfalls": _count(node_list, "node_type", "OUTFALL"),
            "storage_nodes": _count(node_list, "node_type", "STORAGE"),
            "conduits": _count(link_list, "link_type", "CONDUIT"),
            "pumps": _count(link_list, "link_type", "PUMP"),
            "orifices": _count(link_list, "link_type", "ORIFICE"),
            "weirs": _count(link_list, "link_type", "WEIR"),
        },
        "twod_active": bool(twod.get("active", False)),
    }


async def validate_model(client: MCPClient, session_id: str) -> dict:
    diagnostics = await client.call_tool("lifecycle_get_open_diagnostics", {"session_id": session_id})
    errors = list(diagnostics.get("errors", []))
    warnings = list(diagnostics.get("warnings", []))
    return {
        "session_id": session_id,
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }
