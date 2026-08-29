"""High-level engineering workflow endpoints -- orchestrate the raw
dispatcher tools where that genuinely adds workflow/safety value.
Everything here takes a caller-supplied `session_id` for an
already-open upstream session (see app/services/model.py's module
docstring for why: this gateway owns no file storage of its own)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.mcp.client import mcp_client
from app.schemas.engineering import (
    EngineeringSummaryResponse,
    FloodingAnalysisResponse,
    ModelInventoryResponse,
    ModelValidateResponse,
    ScenarioCompareRequest,
    ScenarioCompareResponse,
    SimulationIntegrityResponse,
    SimulationRunResponse,
    TwoDCouplingResponse,
    TwoDMassBalanceResponse,
    TwoDSummaryResponse,
)
from app.security.auth import require_api_key
from app.services import flooding as flooding_service
from app.services import integrity as integrity_service
from app.services import model as model_service
from app.services import scenario as scenario_service
from app.services import simulation as simulation_service
from app.services import summary as summary_service
from app.services import twod as twod_service

router = APIRouter(prefix="/engineering", tags=["engineering"], dependencies=[Depends(require_api_key)])


@router.get(
    "/model-inventory",
    response_model=ModelInventoryResponse,
    operation_id="getModelInventory",
    summary="Structured element counts and 2D mesh status for an already-open session",
)
async def model_inventory(session_id: str = Query(...)) -> ModelInventoryResponse:
    return ModelInventoryResponse(**await model_service.get_inventory(mcp_client, session_id))


@router.post(
    "/validate-model",
    response_model=ModelValidateResponse,
    operation_id="validateModel",
    summary="Report the upstream parser's open diagnostics (errors/warnings) for a session",
)
async def validate_model(session_id: str = Query(...)) -> ModelValidateResponse:
    return ModelValidateResponse(**await model_service.validate_model(mcp_client, session_id))


@router.post(
    "/run-simulation",
    response_model=SimulationRunResponse,
    operation_id="runSimulation",
    summary="Run an already-open session's simulation to completion (synchronous)",
)
async def run_simulation(session_id: str = Query(...)) -> SimulationRunResponse:
    return SimulationRunResponse(**await simulation_service.run_simulation(mcp_client, session_id))


@router.get(
    "/simulation-integrity",
    response_model=SimulationIntegrityResponse,
    operation_id="getSimulationIntegrity",
    summary="Raw continuity-error and numerical-stability metrics -- never a bare pass/fail",
)
async def simulation_integrity(session_id: str = Query(...)) -> SimulationIntegrityResponse:
    return SimulationIntegrityResponse(**await integrity_service.get_integrity(mcp_client, session_id))


@router.get(
    "/flooding-analysis",
    response_model=FloodingAnalysisResponse,
    operation_id="analyzeFlooding",
    summary="Flooded nodes ranked by volume, from analysis_get_flooding_summary",
)
async def flooding_analysis(session_id: str = Query(...)) -> FloodingAnalysisResponse:
    return FloodingAnalysisResponse(**await flooding_service.analyze_flooding(mcp_client, session_id))


@router.get(
    "/summary",
    response_model=EngineeringSummaryResponse,
    operation_id="getEngineeringSummary",
    summary="Composed inventory + integrity + flooding + 2D summary, with a limitations disclaimer",
)
async def engineering_summary(session_id: str = Query(...)) -> EngineeringSummaryResponse:
    return EngineeringSummaryResponse(**await summary_service.get_engineering_summary(mcp_client, session_id))


@router.post(
    "/compare-scenarios",
    response_model=ScenarioCompareResponse,
    operation_id="compareScenarios",
    summary="Diff continuity results between two already-run upstream sessions",
)
async def compare_scenarios(body: ScenarioCompareRequest) -> ScenarioCompareResponse:
    return ScenarioCompareResponse(
        **await scenario_service.compare_scenarios(mcp_client, body.session_id_a, body.session_id_b)
    )


@router.get(
    "/twod-summary",
    response_model=TwoDSummaryResponse,
    operation_id="get2DSummary",
    summary="2D mesh size and surface totals for a session, if the 2D surface is active",
)
async def twod_summary(session_id: str = Query(...)) -> TwoDSummaryResponse:
    return TwoDSummaryResponse(**await twod_service.get_twod_summary(mcp_client, session_id))


@router.get(
    "/twod-mass-balance",
    response_model=TwoDMassBalanceResponse,
    operation_id="get2DMassBalance",
    summary="Detailed 2D mass-balance terms for a session, if the 2D surface is active",
)
async def twod_mass_balance(session_id: str = Query(...)) -> TwoDMassBalanceResponse:
    return TwoDMassBalanceResponse(**await twod_service.get_twod_mass_balance(mcp_client, session_id))


@router.get(
    "/twod-coupling",
    response_model=TwoDCouplingResponse,
    operation_id="get2DCoupling",
    summary="1D/2D coupling map for a session, if the 2D surface is active",
)
async def twod_coupling(session_id: str = Query(...)) -> TwoDCouplingResponse:
    return TwoDCouplingResponse(**await twod_service.get_twod_coupling(mcp_client, session_id))
