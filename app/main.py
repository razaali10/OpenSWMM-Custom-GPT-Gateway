"""Application assembly.

This process runs no SWMM engine and imports no openswmm_mcp/openswmm.engine
code. Its entire job is: on startup, open one persistent MCP client
connection to OPENSWMM_MCP_URL; on every request, either serve tool
discovery from the cached registry or forward a tool call to that
connection. See docs/ARCHITECTURE.md.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app.api import discovery, engineering, grouped_tools, health
from app.config import settings
from app.errors import install_error_handlers
from app.logging_config import RequestLoggingMiddleware, configure_logging
from app.mcp.client import mcp_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await mcp_client.start()
    try:
        yield
    finally:
        await mcp_client.stop()


app = FastAPI(
    title="OpenSWMM Custom GPT Gateway",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(RequestLoggingMiddleware)

if settings.allowed_origins_list:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,
        allow_methods=["*"],
        allow_headers=["*"],
    )

install_error_handlers(app)

app.include_router(health.router)
app.include_router(discovery.router, prefix="/api/v1")
app.include_router(grouped_tools.router, prefix="/api/v1")
app.include_router(engineering.router, prefix="/api/v1")


@app.get("/", include_in_schema=False)
async def landing(request: Request) -> HTMLResponse:
    return HTMLResponse(
        "<h1>OpenSWMM Custom GPT Gateway</h1>"
        "<p>A standalone Custom GPT Actions gateway in front of an independently "
        "deployed <a href=\"https://github.com/HydroCouple/openswmm.mcp\">openswmm.mcp</a> "
        "server (~565 tools, dynamically discovered -- never hardcoded here).</p>"
        "<ul>"
        '<li><a href="/docs">/docs</a> -- Swagger UI</li>'
        '<li><a href="/openapi.json">/openapi.json</a> -- raw schema</li>'
        '<li><a href="/health">/health</a></li>'
        '<li><a href="/api/v1/status">/api/v1/status</a> -- upstream connectivity + live tool count</li>'
        "</ul>"
    )
