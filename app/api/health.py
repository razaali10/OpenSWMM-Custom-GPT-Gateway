from __future__ import annotations

from fastapi import APIRouter

from app.mcp.client import MCPConnectionError, MCPTimeoutError, mcp_client
from app.mcp.registry import registry

router = APIRouter(tags=["system"])


@router.get("/health", operation_id="healthCheck", summary="Liveness check -- never requires auth")
async def health() -> dict:
    return {"status": "ok", "service": "OpenSWMM Custom GPT Gateway", "version": "1.0.0"}


@router.get(
    "/api/v1/status",
    operation_id="getGatewayStatus",
    summary="Liveness plus upstream MCP connectivity and live tool count -- never requires auth",
)
async def status() -> dict:
    try:
        tools = await registry.list_tools()
        return {
            "status": "ok",
            "upstream_mcp_reachable": True,
            "upstream_tool_count": len(tools),
        }
    except (MCPConnectionError, MCPTimeoutError) as exc:
        return {
            "status": "degraded",
            "upstream_mcp_reachable": False,
            "upstream_error": str(exc),
        }
