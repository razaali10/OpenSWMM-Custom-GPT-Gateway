"""Generate Custom GPT Knowledge documentation from the LIVE MCP
registry -- never hand-invents a missing description (project brief
section 18).

Usage:
    python -m scripts.generate_tool_catalog
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from app.mcp.client import mcp_client
from app.mcp.registry import registry

OUTPUT_DIR = Path(__file__).parent.parent / "generated"

# Maps action groups to the engineering tasks they're most relevant to,
# for the routing guide. Curated, and explicitly labeled as such.
TASK_TO_GROUPS = {
    "Model inventory": ["core", "results"],
    "Flood investigation": ["results", "hydraulics", "twod"],
    "Pipe capacity review": ["hydraulics", "results"],
    "Pump analysis": ["hydraulics", "results"],
    "Storage analysis": ["hydraulics", "results"],
    "Rainfall-runoff review": ["hydrology", "results"],
    "Groundwater review": ["hydrology"],
    "RDII review": ["hydrology"],
    "Water quality review": ["water-quality"],
    "2D surface flooding": ["twod", "results"],
    "1D/2D coupling": ["twod", "hydraulics"],
    "RTC controls": ["forcing-controls"],
    "Model construction": ["model-builder", "core"],
    "Model modification": ["model-builder"],
    "Scenario comparison": ["results", "core"],
    "LID design": ["infrastructure", "hydrology"],
    "Optimization": ["optimization"],
}


async def generate_catalog() -> str:
    tools = await registry.list_tools()
    tools.sort(key=lambda t: t.name)

    lines = ["# OpenSWMM MCP Tool Catalog", "", f"Generated from the live upstream server -- {len(tools)} tools.", ""]
    current_namespace = None
    for tool in tools:
        if tool.namespace != current_namespace:
            current_namespace = tool.namespace
            lines.append(f"## Namespace: {current_namespace}")
            lines.append("")
        lines.append(f"### {tool.name}")
        lines.append("")
        lines.append(f"- **Namespace**: {tool.namespace}")
        lines.append(f"- **Action Group**: {tool.action_group}")
        lines.append(f"- **Operation Class**: {tool.operation_class}")
        lines.append(f"- **Destructive**: {'Yes' if tool.destructive else 'No'}")
        lines.append("")
        lines.append("**Description**")
        lines.append("")
        lines.append(tool.description or "_(no description provided by the upstream server)_")
        lines.append("")
        props = (tool.input_schema.get("properties") or {}) if tool.input_schema else {}
        if props:
            lines.append("**Input arguments**")
            lines.append("")
            for name, schema in props.items():
                type_hint = schema.get("type", "any")
                lines.append(f"- `{name}` ({type_hint})")
            lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


async def generate_routing_guide() -> str:
    action_groups = await registry.action_groups()
    lines = [
        "# OpenSWMM Tool Routing Guide",
        "",
        "Curated mapping from engineering tasks to the action groups most likely to contain "
        "the right tool -- use listOpenSwmmNamespaces/searchOpenSwmmTools/getOpenSwmmToolSchema "
        "to find the exact tool and its real input schema before calling it.",
        "",
    ]
    for task, groups in TASK_TO_GROUPS.items():
        lines.append(f"## {task}")
        lines.append("")
        lines.append(f"Preferred action groups: {', '.join(f'`{g}`' for g in groups)}")
        lines.append("")
    lines.append("## All action groups (live tool counts)")
    lines.append("")
    for group, count in action_groups.items():
        lines.append(f"- `{group}`: {count} tools")
    return "\n".join(lines)


async def main() -> None:
    await mcp_client.start()
    try:
        OUTPUT_DIR.mkdir(exist_ok=True)
        catalog = await generate_catalog()
        (OUTPUT_DIR / "OpenSWMM_MCP_Tool_Catalog.md").write_text(catalog, encoding="utf-8")
        routing = await generate_routing_guide()
        (OUTPUT_DIR / "OpenSWMM_Tool_Routing_Guide.md").write_text(routing, encoding="utf-8")
        print(f"Wrote {OUTPUT_DIR / 'OpenSWMM_MCP_Tool_Catalog.md'}")
        print(f"Wrote {OUTPUT_DIR / 'OpenSWMM_Tool_Routing_Guide.md'}")
    finally:
        await mcp_client.stop()


if __name__ == "__main__":
    asyncio.run(main())
