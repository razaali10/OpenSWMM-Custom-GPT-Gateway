"""Bearer API-key authentication between Custom GPT Actions and this
gateway. Unlike the sibling openswmm-mcp-server project (whose /mcp
endpoint has its own separate, currently-open posture), this gateway
defaults to requiring a key (`auth_mode = "api_key"` by default in
app/config.py) -- it fans out to the full 565-tool surface including
every destructive/optimization operation, so an open-by-default posture
is the wrong default here even though it was acceptable for the
curated, mostly-read-oriented REST gateway.
"""

from __future__ import annotations

from fastapi import Header

from app.config import settings
from app.errors import UnauthorizedError


async def require_api_key(authorization: str | None = Header(default=None)) -> None:
    if settings.auth_mode == "none":
        return

    if settings.auth_mode != "api_key":
        raise UnauthorizedError(
            f"Unknown AUTH_MODE '{settings.auth_mode}'.", {"expected": ["none", "api_key"]}
        )

    if not settings.gateway_api_key:
        raise UnauthorizedError(
            "AUTH_MODE=api_key but GATEWAY_API_KEY is not configured on the server."
        )

    prefix = "Bearer "
    supplied = authorization[len(prefix):] if authorization and authorization.startswith(prefix) else None

    if supplied != settings.gateway_api_key:
        raise UnauthorizedError("Missing or invalid API key. Supply 'Authorization: Bearer <key>'.")
