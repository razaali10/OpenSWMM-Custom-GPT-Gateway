"""REAL integration tests against the live, configured upstream MCP
server (OPENSWMM_MCP_URL, default: this project's own Render deployment).

Scope deliberately matches the project brief's own required flow
(section 22): "list tools -> find known tool -> inspect schema ->
execute safe read-only tool." Nothing here calls a WRITE/DESTRUCTIVE/
SIMULATION_CONTROL/OPTIMIZATION tool or requires an open model session
-- that would either mutate the shared production server's state or
require bootstrapping a session, which is out of scope for this
gateway's own test suite (see docs/ARCHITECTURE.md "Known limitation:
model upload").
"""

from __future__ import annotations


def test_health_and_status(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

    r = client.get("/api/v1/status")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["upstream_mcp_reachable"] is True
    assert body["upstream_tool_count"] > 0


def test_list_namespaces_reports_real_counts(client):
    r = client.get("/api/v1/mcp/namespaces")
    assert r.status_code == 200
    body = r.json()
    # The live registry is authoritative -- assert structure and
    # plausibility, not an exact hardcoded 565 that would break the
    # moment the upstream server adds a tool (project brief section 23:
    # "do not hard-fail merely because the total number is not exactly
    # 565 -- the server evolves").
    assert body["tool_count"] > 500
    assert "lifecycle" in body["namespaces"]
    assert "twod" in body["namespaces"]
    assert set(body["action_groups"]) == {
        "core", "model-builder", "hydrology", "hydraulics", "forcing-controls",
        "results", "twod", "spatial", "water-quality", "infrastructure", "optimization",
    }


def test_search_finds_a_known_tool(client):
    r = client.post(
        "/api/v1/mcp/search",
        json={"query": "change conduit entrance and exit losses", "namespace": "links", "limit": 5},
    )
    assert r.status_code == 200
    names = [m["name"] for m in r.json()["matches"]]
    assert "links_set_loss_coeff" in names


def test_get_tool_schema_for_a_known_tool(client):
    r = client.get("/api/v1/mcp/tools/links_set_loss_coeff")
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == "links_set_loss_coeff"
    assert body["action_group"] == "hydraulics"
    assert body["operation_class"] == "WRITE"
    assert body["destructive"] is False


def test_get_tool_schema_404_for_unknown_tool(client):
    r = client.get("/api/v1/mcp/tools/definitely_not_a_real_tool")
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "MCP_TOOL_NOT_FOUND"


def test_dispatch_safe_read_only_tool_end_to_end(client):
    """The one real tool execution this suite performs against the
    shared production upstream -- xsect_list_shapes is a pure read with
    no session/model dependency and no side effects."""
    r = client.post(
        "/api/v1/tools/hydraulics", json={"tool_name": "xsect_list_shapes", "arguments": {}}
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["success"] is True
    assert body["result"]["count"] > 0
    assert any(shape["name"] == "circular" for shape in body["result"]["shapes"])


def test_dispatch_rejects_wrong_action_group(client):
    r = client.post("/api/v1/tools/core", json={"tool_name": "xsect_list_shapes", "arguments": {}})
    assert r.status_code == 400
    assert r.json()["error"]["code"] == "WRONG_ACTION_GROUP"
    assert r.json()["error"]["details"]["correct_action_group"] == "hydraulics"


def test_dispatch_rejects_unknown_tool(client):
    r = client.post("/api/v1/tools/core", json={"tool_name": "does_not_exist_anywhere", "arguments": {}})
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "MCP_TOOL_NOT_FOUND"


def test_openapi_operation_count_fits_gpt_actions_budget(client):
    """Project brief's whole point: ~20-30 operations total, never one
    per MCP tool."""
    r = client.get("/openapi.json")
    ops = [
        op["operationId"]
        for path in r.json()["paths"].values()
        for op in path.values()
        if isinstance(op, dict) and "operationId" in op
    ]
    assert 15 <= len(ops) <= 30
    for group_op in (
        "callSwmmCoreTool", "callModelBuilderTool", "callHydrologyTool", "callHydraulicsTool",
        "callForcingControlsTool", "callResultsTool", "call2DTool", "callSpatialTool",
        "callWaterQualityTool", "callInfrastructureTool", "callOptimizationTool",
    ):
        assert group_op in ops
    for discovery_op in ("listOpenSwmmNamespaces", "searchOpenSwmmTools", "getOpenSwmmToolSchema"):
        assert discovery_op in ops
