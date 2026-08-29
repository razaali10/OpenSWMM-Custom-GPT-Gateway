"""Connect to the configured upstream MCP server and report what it
actually exposes -- run this after any deployment or upstream change.

Usage:
    python -m scripts.verify_registry
"""

from __future__ import annotations

import asyncio

from app.mcp.client import mcp_client
from app.mcp.registry import registry

# A small, stable sample of tools this gateway's engineering endpoints
# depend on. Their absence doesn't fail the script (the brief says not
# to hard-fail on tool count/composition -- the server evolves) but is
# reported clearly since it would mean those endpoints degrade.
CRITICAL_TOOLS = (
    "twod_get_mesh_summary",
    "twod_get_mass_balance",
    "analysis_get_mass_balance",
    "analysis_get_flooding_summary",
    "analysis_compare_scenarios",
    "lifecycle_run_simulation",
    "lifecycle_get_open_diagnostics",
)


async def main() -> None:
    print(f"Connecting to {mcp_client._url} ...")
    try:
        await mcp_client.start()
    except Exception as exc:  # noqa: BLE001
        print(f"MCP server reachable: no ({exc})")
        raise SystemExit(1)

    try:
        print("MCP server reachable: yes")
        tools = await registry.list_tools()
        print(f"Total tools: {len(tools)}")
        print()
        print("Namespaces:")
        for ns, count in (await registry.namespaces()).items():
            print(f"  {ns}: {count}")
        print()
        print("Action groups:")
        for group, count in (await registry.action_groups()).items():
            print(f"  {group}: {count}")
        print()
        print("Critical tools:")
        names = {t.name for t in tools}
        for name in CRITICAL_TOOLS:
            present = "present" if name in names else "MISSING"
            print(f"  {name}: {present}")
    finally:
        await mcp_client.stop()


if __name__ == "__main__":
    asyncio.run(main())
