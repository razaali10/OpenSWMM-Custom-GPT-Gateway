"""Dynamic tool discovery -- lets a Custom GPT find the exact MCP tool it
needs and inspect its real input schema before calling it through a
grouped Action, instead of the model guessing tool names/arguments.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.errors import ToolNotFoundError
from app.mcp.registry import registry
from app.schemas.tools import (
    NamespacesResponse,
    ToolInfo,
    ToolSchemaResponse,
    ToolSearchRequest,
    ToolSearchResponse,
)
from app.security.auth import require_api_key

router = APIRouter(tags=["discovery"], dependencies=[Depends(require_api_key)])


@router.get(
    "/mcp/namespaces",
    response_model=NamespacesResponse,
    operation_id="listOpenSwmmNamespaces",
    summary="List every tool namespace and action group on the live upstream server, with counts",
)
async def list_namespaces() -> NamespacesResponse:
    namespaces = await registry.namespaces()
    action_groups = await registry.action_groups()
    return NamespacesResponse(
        tool_count=sum(namespaces.values()), namespaces=namespaces, action_groups=action_groups
    )


@router.post(
    "/mcp/search",
    response_model=ToolSearchResponse,
    operation_id="searchOpenSwmmTools",
    summary="Search the live tool registry by name, namespace, description, or argument names",
)
async def search_tools(request: ToolSearchRequest) -> ToolSearchResponse:
    matches = await registry.search(request.query, namespace=request.namespace, limit=request.limit)
    return ToolSearchResponse(
        matches=[
            ToolInfo(
                name=t.name,
                namespace=t.namespace,
                action_group=t.action_group or "core",
                description=t.description,
                operation_class=t.operation_class or "READ",
                destructive=t.destructive,
            )
            for t in matches
        ]
    )


@router.get(
    "/mcp/tools/{tool_name}",
    response_model=ToolSchemaResponse,
    operation_id="getOpenSwmmToolSchema",
    summary="Get one tool's live description, input schema, action group, and safety classification",
)
async def get_tool_schema(tool_name: str) -> ToolSchemaResponse:
    tool = await registry.get_tool(tool_name)
    if tool is None:
        raise ToolNotFoundError(
            f"MCP tool '{tool_name}' does not exist on the upstream server.", {"tool_name": tool_name}
        )
    return ToolSchemaResponse(
        name=tool.name,
        namespace=tool.namespace,
        action_group=tool.action_group or "core",
        description=tool.description,
        operation_class=tool.operation_class or "READ",
        destructive=tool.destructive,
        input_schema=tool.input_schema,
    )
