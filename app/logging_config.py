"""Structured request logging.

Logs request id, action group, MCP tool name (when known), duration,
success/failure, and MCP error class -- never API keys, secrets, or
raw request/response bodies (per project brief section 24).
"""

from __future__ import annotations

import logging
import time
import uuid
from contextvars import ContextVar

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp

from app.config import settings

request_id_var: ContextVar[str] = ContextVar("request_id", default="-")
tool_name_var: ContextVar[str] = ContextVar("tool_name", default="-")


class _ContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get()
        record.tool_name = tool_name_var.get()
        return True


def configure_logging() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s [%(levelname)s] request=%(request_id)s tool=%(tool_name)s %(name)s: %(message)s"
        )
    )
    handler.addFilter(_ContextFilter())

    logger = logging.getLogger("openswmm_gateway")
    logger.setLevel(settings.log_level)
    logger.addHandler(handler)
    logger.propagate = False


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self._logger = logging.getLogger("openswmm_gateway.request")

    async def dispatch(self, request: Request, call_next):
        req_id = str(uuid.uuid4())
        req_token = request_id_var.set(req_id)
        tool_token = tool_name_var.set("-")
        start = time.monotonic()
        try:
            response = await call_next(request)
        except Exception:
            elapsed_ms = (time.monotonic() - start) * 1000
            self._logger.exception(
                "%s %s failed after %.1fms", request.method, request.url.path, elapsed_ms
            )
            raise
        finally:
            request_id_var.reset(req_token)
            tool_name_var.reset(tool_token)

        elapsed_ms = (time.monotonic() - start) * 1000
        self._logger.info(
            "%s %s -> %d (%.1fms)",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )
        response.headers["X-Request-Id"] = req_id
        return response
