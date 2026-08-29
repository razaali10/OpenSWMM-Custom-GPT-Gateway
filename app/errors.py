"""Structured error responses, one shape for the whole API::

    {"error": {"code": "MCP_TOOL_NOT_FOUND", "message": "...", "details": {}}}

Status codes follow the project brief's error semantics table (section 26):
400 bad group/tool combination, 401 auth failure, 404 unknown tool,
409 state conflict, 422 argument validation, 502 upstream MCP error,
504 upstream MCP timeout.
"""

from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("openswmm_gateway")


class GatewayError(Exception):
    status_code: int = 500
    code: str = "INTERNAL_ERROR"

    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class BadRequestError(GatewayError):
    status_code = 400
    code = "BAD_REQUEST"


class WrongActionGroupError(GatewayError):
    status_code = 400
    code = "WRONG_ACTION_GROUP"


class UnauthorizedError(GatewayError):
    status_code = 401
    code = "UNAUTHORIZED"


class ToolNotFoundError(GatewayError):
    status_code = 404
    code = "MCP_TOOL_NOT_FOUND"


class ConflictError(GatewayError):
    status_code = 409
    code = "CONFLICT"


class ValidationErrorGW(GatewayError):
    status_code = 422
    code = "VALIDATION_ERROR"


class UpstreamMCPError(GatewayError):
    status_code = 502
    code = "UPSTREAM_MCP_ERROR"


class UpstreamTimeoutError(GatewayError):
    status_code = 504
    code = "UPSTREAM_MCP_TIMEOUT"


def _error_body(code: str, message: str, details: dict) -> dict:
    return {"error": {"code": code, "message": message, "details": details}}


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(GatewayError)
    async def _gateway_error(request: Request, exc: GatewayError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_body(exc.code, exc.message, exc.details),
        )

    @app.exception_handler(Exception)
    async def _unhandled(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled error on %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=500,
            content=_error_body("INTERNAL_ERROR", "An internal error occurred.", {}),
        )
