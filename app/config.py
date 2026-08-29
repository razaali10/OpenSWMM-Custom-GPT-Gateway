"""Gateway configuration via environment variables.

No production hostname is hardcoded here -- OPENSWMM_MCP_URL must be set
explicitly (see .env.example for the actual value used by this project's
own deployments).
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class GatewaySettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # -- Upstream MCP server (Repository A) ------------------------------
    openswmm_mcp_url: str
    openswmm_mcp_timeout_seconds: float = 30.0
    mcp_simulation_timeout_seconds: float = 300.0
    mcp_optimization_timeout_seconds: float = 30.0

    # -- Registry cache ----------------------------------------------------
    mcp_tool_cache_ttl_seconds: int = 300

    # -- Networking --------------------------------------------------
    port: int = 8080

    # -- Auth ----------------------------------------------------------
    # "none" (local dev only) or "api_key" (required in any shared deployment).
    auth_mode: str = "api_key"
    gateway_api_key: str | None = None

    # -- CORS ------------------------------------------------------------
    allowed_origins: str = ""

    log_level: str = "INFO"

    @property
    def allowed_origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]


settings = GatewaySettings()
