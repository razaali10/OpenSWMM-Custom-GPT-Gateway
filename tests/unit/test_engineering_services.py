"""Engineering service composition logic against a MOCKED MCP client --
these test derivation/composition logic (thresholds, filtering, sorting),
not the upstream server itself. Field shapes match what was verified
live against this exact upstream server while building the sibling
openswmm-mcp-server REST gateway."""

from __future__ import annotations

import pytest

from app.services import flooding, integrity, model, scenario


class FakeClient:
    def __init__(self, responses: dict[str, object]) -> None:
        self._responses = responses
        self.calls: list[tuple[str, dict]] = []

    async def call_tool(self, tool_name, arguments, *, timeout=None):
        self.calls.append((tool_name, arguments))
        return self._responses[tool_name]


@pytest.mark.asyncio
async def test_get_inventory_counts_by_type():
    client = FakeClient(
        {
            "query_get_system_summary": {"subcatchment_count": 3},
            "query_get_node_info": [
                {"node_type": "JUNCTION"},
                {"node_type": "JUNCTION"},
                {"node_type": "OUTFALL"},
            ],
            "query_get_link_info": [{"link_type": "CONDUIT"}, {"link_type": "CONDUIT"}],
            "twod_get_mesh_summary": {"active": True},
        }
    )
    result = await model.get_inventory(client, "s1")
    assert result["counts"]["junctions"] == 2
    assert result["counts"]["outfalls"] == 1
    assert result["counts"]["conduits"] == 2
    assert result["twod_active"] is True


@pytest.mark.asyncio
async def test_validate_model_reports_parser_diagnostics():
    client = FakeClient(
        {"lifecycle_get_open_diagnostics": {"errors": [], "warnings": ["minor warning"]}}
    )
    result = await model.validate_model(client, "s1")
    assert result["valid"] is True
    assert result["warnings"] == ["minor warning"]


@pytest.mark.asyncio
async def test_validate_model_invalid_when_errors_present():
    client = FakeClient(
        {"lifecycle_get_open_diagnostics": {"errors": ["bad input"], "warnings": []}}
    )
    result = await model.validate_model(client, "s1")
    assert result["valid"] is False


@pytest.mark.asyncio
async def test_integrity_acceptable_below_5_pct():
    # analysis_get_mass_balance reports these as fractions of total inflow
    # (0.003 == 0.3%), not percent -- get_integrity must convert.
    client = FakeClient(
        {
            "analysis_get_mass_balance": {
                "runoff_continuity_error": 0.003,
                "routing_continuity_error": -0.004,
                "routing_stats": {"pct_not_converged": 0.5},
                "max_courant": 0.7,
            }
        }
    )
    result = await integrity.get_integrity(client, "s1")
    assert result["runoff_continuity_error_pct"] == pytest.approx(0.3)
    assert result["routing_continuity_error_pct"] == pytest.approx(-0.4)
    assert result["overall_status"] == "acceptable"


@pytest.mark.asyncio
async def test_integrity_poor_above_10_pct():
    client = FakeClient(
        {
            "analysis_get_mass_balance": {
                "runoff_continuity_error": 0.15,
                "routing_continuity_error": 0.02,
                "routing_stats": {},
                "max_courant": None,
            }
        }
    )
    result = await integrity.get_integrity(client, "s1")
    assert result["runoff_continuity_error_pct"] == pytest.approx(15.0)
    assert result["overall_status"] == "poor"


@pytest.mark.asyncio
async def test_integrity_unknown_with_no_data():
    client = FakeClient(
        {
            "analysis_get_mass_balance": {
                "runoff_continuity_error": None,
                "routing_continuity_error": None,
                "routing_stats": {},
                "max_courant": None,
            }
        }
    )
    result = await integrity.get_integrity(client, "s1")
    assert result["overall_status"] == "unknown"


@pytest.mark.asyncio
async def test_compare_scenarios_converts_fraction_to_pct():
    class TwoSessionFakeClient:
        def __init__(self, by_session: dict[str, dict]) -> None:
            self._by_session = by_session

        async def call_tool(self, tool_name, arguments, *, timeout=None):
            return self._by_session[arguments["session_id"]]

    client = TwoSessionFakeClient(
        {
            "s1": {"routing_continuity_error": 0.003},
            "s2": {"routing_continuity_error": -0.12},
        }
    )
    result = await scenario.compare_scenarios(client, "s1", "s2")
    assert result["routing_continuity_error_a"] == pytest.approx(0.3)
    assert result["routing_continuity_error_b"] == pytest.approx(-12.0)


@pytest.mark.asyncio
async def test_flooding_analysis_filters_zero_volume_and_sorts_descending():
    client = FakeClient(
        {
            "analysis_get_flooding_summary": [
                {"node_id": "J1", "total_flood_volume": 0.0},
                {"node_id": "J2", "total_flood_volume": 12.5, "max_depth": 1.1, "time_flooded": 300},
                {"node_id": "J3", "total_flood_volume": 40.0, "max_depth": 2.0, "time_flooded": 900},
            ]
        }
    )
    result = await flooding.analyze_flooding(client, "s1")
    assert result["flooded_node_count"] == 2
    assert [n["node_id"] for n in result["flooded_nodes"]] == ["J3", "J2"]
    # time_flooded comes back from the engine in seconds; the gateway
    # reports hours.
    j3, j2 = result["flooded_nodes"]
    assert j3["time_flooded"] == pytest.approx(900 / 3600.0)
    assert j2["time_flooded"] == pytest.approx(300 / 3600.0)
