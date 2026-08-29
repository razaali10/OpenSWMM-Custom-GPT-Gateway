"""Shared fixtures.

Env vars must be set before app.config/app.main import (settings are read
at import time). Points at this project's own live deployment by
default -- override OPENSWMM_MCP_URL to test against a different one.
"""

from __future__ import annotations

import os

os.environ.setdefault("OPENSWMM_MCP_URL", "https://openswmm.onrender.com/mcp")
os.environ.setdefault("OPENSWMM_MCP_TIMEOUT_SECONDS", "60")
os.environ.setdefault("AUTH_MODE", "none")

import pytest


@pytest.fixture(scope="session")
def client():
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as c:
        yield c
