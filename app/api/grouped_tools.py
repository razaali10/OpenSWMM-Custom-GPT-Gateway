"""The ~10-11 grouped MCP dispatcher Actions -- this is how a Custom GPT
reaches all ~565 upstream tools without exposing 565 individual OpenAPI
operations. Each endpoint accepts {tool_name, arguments} and forwards to
exactly the tools whose action_group matches; anything else is rejected
server-side (never left to the model's own judgment -- see
app/services/dispatcher.py and app/security/tool_policy.py).
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.mcp.client import mcp_client
from app.mcp.registry import registry
from app.schemas.tools import ToolCallRequest, ToolCallResponse
from app.security.auth import require_api_key
from app.security.tool_policy import ACTION_GROUPS
from app.services.dispatcher import dispatch

router = APIRouter(tags=["grouped-tools"], dependencies=[Depends(require_api_key)])

_GROUP_META: dict[str, tuple[str, str, str]] = {
    # group -> (operationId, summary, namespace hint for the description)
    "core": ("callSwmmCoreTool", "Call a lifecycle_*/model_*/datetime_* tool", "lifecycle_, model_, datetime_"),
    "model-builder": ("callModelBuilderTool", "Call a building_*/editing_*/tables_* tool", "building_, editing_, tables_"),
    "hydrology": ("callHydrologyTool", "Call a subcatchments_*/climate_*/inflows_* tool", "subcatchments_, climate_, inflows_"),
    "hydraulics": ("callHydraulicsTool", "Call a nodes_*/links_*/xsect_* tool", "nodes_, links_, xsect_"),
    "forcing-controls": ("callForcingControlsTool", "Call a forcing_*/controls_* tool", "forcing_, controls_"),
    "results": ("callResultsTool", "Call a query_*/analysis_* tool", "query_, analysis_"),
    "twod": ("call2DTool", "Call a twod_* tool", "twod_"),
    "spatial": ("callSpatialTool", "Call a spatial_*/geopackage_* tool", "spatial_, geopackage_"),
    "water-quality": ("callWaterQualityTool", "Call a quality_*/pollutants_* tool", "quality_, pollutants_"),
    "infrastructure": ("callInfrastructureTool", "Call an infrastructure_* tool", "infrastructure_"),
    "optimization": ("callOptimizationTool", "Call a hotstart_*/gym_* tool", "hotstart_, gym_"),
}

assert set(_GROUP_META) == set(ACTION_GROUPS), "grouped_tools.py routes must match tool_policy.ACTION_GROUPS"


def _make_endpoint(group: str):
    async def endpoint(request: ToolCallRequest) -> ToolCallResponse:
        return await dispatch(group, request, registry=registry, client=mcp_client)

    endpoint.__name__ = f"call_{group.replace('-', '_')}_tool"
    return endpoint


for _group, (_op_id, _summary, _namespaces) in _GROUP_META.items():
    router.add_api_route(
        f"/tools/{_group}",
        _make_endpoint(_group),
        methods=["POST"],
        response_model=ToolCallResponse,
        operation_id=_op_id,
        summary=_summary,
        description=(
            f"Dispatches to any tool whose action group is '{_group}' "
            f"(namespaces: {_namespaces}). Rejects tool_name values that "
            "belong to a different action group -- call the correct "
            "/api/v1/tools/{group} endpoint instead, per the error's "
            "correct_action_group field. "
            "`arguments` accepts every key from that tool's own "
            "input_schema (from getOpenSwmmToolSchema) by name, with no "
            "allow-list and no special-cased or reserved keys -- session_id "
            "is an ordinary argument like any other, never rejected. "
            "Example: {\"tool_name\": \"building_create_model\", "
            "\"arguments\": {\"session_id\": \"my_session\"}}."
        ),
    )
