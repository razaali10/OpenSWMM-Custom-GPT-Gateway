"""Auth-mode behavior, tested against app.security.auth.require_api_key
directly (settings monkeypatched for the duration of one test) -- the
module-level `settings` singleton is read at process-import time, so
exercising api_key mode against the live app would require restarting
the whole process under different env vars."""

import pytest

from app.config import settings
from app.errors import UnauthorizedError
from app.security.auth import require_api_key


@pytest.mark.asyncio
async def test_missing_key_rejected(monkeypatch):
    monkeypatch.setattr(settings, "auth_mode", "api_key")
    monkeypatch.setattr(settings, "gateway_api_key", "secret123")
    with pytest.raises(UnauthorizedError):
        await require_api_key(authorization=None)


@pytest.mark.asyncio
async def test_wrong_key_rejected(monkeypatch):
    monkeypatch.setattr(settings, "auth_mode", "api_key")
    monkeypatch.setattr(settings, "gateway_api_key", "secret123")
    with pytest.raises(UnauthorizedError):
        await require_api_key(authorization="Bearer wrong")


@pytest.mark.asyncio
async def test_correct_bearer_key_accepted(monkeypatch):
    monkeypatch.setattr(settings, "auth_mode", "api_key")
    monkeypatch.setattr(settings, "gateway_api_key", "secret123")
    await require_api_key(authorization="Bearer secret123")  # must not raise


@pytest.mark.asyncio
async def test_auth_mode_none_never_requires_a_key():
    await require_api_key(authorization=None)  # must not raise (test env default)


@pytest.mark.asyncio
async def test_api_key_mode_without_configured_key_fails_closed(monkeypatch):
    monkeypatch.setattr(settings, "auth_mode", "api_key")
    monkeypatch.setattr(settings, "gateway_api_key", None)
    with pytest.raises(UnauthorizedError):
        await require_api_key(authorization="Bearer anything")
