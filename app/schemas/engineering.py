"""Response shapes for the small set of high-level engineering
endpoints. Field names match what was verified live against this exact
upstream MCP server while building the sibling openswmm-mcp-server REST
gateway (see that repo's docs/ARCHITECTURE.md) -- not re-guessed here.
"""

from __future__ import annotations

from pydantic import BaseModel


class ModelInventoryResponse(BaseModel):
    session_id: str
    counts: dict
    twod_active: bool


class ModelValidateResponse(BaseModel):
    session_id: str
    valid: bool
    errors: list[str]
    warnings: list[str]


class SimulationRunResponse(BaseModel):
    session_id: str
    status: str
    unsupported_fields: list[str] = []


class SimulationIntegrityResponse(BaseModel):
    session_id: str
    completed: bool
    runoff_continuity_error_pct: float | None
    routing_continuity_error_pct: float | None
    max_courant: float | None
    pct_steps_not_converged: float | None
    overall_status: str


class FloodedNode(BaseModel):
    node_id: str
    total_flood_volume: float | None
    max_depth: float | None
    time_flooded: float | None


class FloodingAnalysisResponse(BaseModel):
    session_id: str
    flooded_node_count: int
    flooded_nodes: list[FloodedNode]


class EngineeringSummaryResponse(BaseModel):
    session_id: str
    inventory: dict
    integrity: dict
    flooding: dict
    twod_active: bool
    limitations: list[str]


class ScenarioCompareRequest(BaseModel):
    session_id_a: str
    session_id_b: str


class ScenarioCompareResponse(BaseModel):
    session_id_a: str
    session_id_b: str
    routing_continuity_error_a: float | None
    routing_continuity_error_b: float | None


class TwoDSummaryResponse(BaseModel):
    session_id: str
    active: bool
    mesh: dict | None = None
    totals: dict | None = None


class TwoDMassBalanceResponse(BaseModel):
    session_id: str
    active: bool
    terms: dict


class TwoDCouplingResponse(BaseModel):
    session_id: str
    active: bool
    coupling_map: dict
