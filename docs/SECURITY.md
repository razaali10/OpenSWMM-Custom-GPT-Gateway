# Security

## Authentication

`AUTH_MODE=api_key` is the **default** in this repository (`app/config.py`)
-- unlike the sibling REST gateway, which defaults to `none` to match its
own `/mcp`'s existing open posture. That default doesn't apply here: this
gateway fans out to the *entire* tool surface, including every
`DESTRUCTIVE`/`OPTIMIZATION` operation, so an open-by-default posture would
be the wrong choice even though it matched the curated gateway's
mostly-read-oriented endpoint set.

- `api_key` (default): every request except `/health` and `/api/v1/status`
  requires `Authorization: Bearer <GATEWAY_API_KEY>`. Missing or wrong key →
  `401 UNAUTHORIZED`. If `AUTH_MODE=api_key` but `GATEWAY_API_KEY` isn't
  configured, the server **fails closed** (every request rejected) rather
  than silently falling back to open access.
- `none`: no authentication. Local development only -- do not deploy this
  gateway publicly with `AUTH_MODE=none`.

This is a single shared secret for the whole deployment (`Authorization:
Bearer <key>`), appropriate for "this Custom GPT can reach my gateway"
access control, not multi-tenant auth or per-user permissions.

## What this gateway can do to the upstream model

Because this gateway forwards to the *entire* MCP tool surface rather than a
curated subset, a caller with a valid API key can:

- delete arbitrary model objects (`editing_delete_object`)
- rewrite hydraulic/hydrologic properties on any node, link, or subcatchment
- start/cancel optimization jobs and apply their results (`gym_*`)
- overwrite a model file (`building_write_model`)

`getOpenSwmmToolSchema` reports each tool's `operation_class` (including
`destructive: true/false`) so a well-behaved Custom GPT can be built to treat
these with extra care, but **the gateway itself does not block a
DESTRUCTIVE call** -- see `docs/ARCHITECTURE.md` "Known limitations" #2 for
why (no session metadata exists upstream to distinguish a protected baseline
from an expendable scenario). Anyone with the API key has full read/write
access to whatever the upstream server's caller-supplied `session_id`
points at.

## Upstream trust boundary

This gateway trusts the upstream MCP server completely -- it performs no
validation of tool results and no sandboxing of the SWMM engine (that engine
runs in the upstream server's own process, not this one). This process
itself never imports `openswmm_mcp`/`openswmm.engine` and runs no native
code of its own; its only external dependency surface is the MCP protocol
call to `OPENSWMM_MCP_URL`.

## Logging

`app/logging_config.py` logs request id, tool name (when known), method,
path, status, and elapsed time. It never logs API keys, secrets, or raw
request/response bodies (project brief section 24).

## CORS

Empty `ALLOWED_ORIGINS` (the default) grants no cross-origin browser access.
Server-to-server callers (GPT Actions, curl) aren't subject to CORS
regardless. Never set `ALLOWED_ORIGINS=*` while also running
`AUTH_MODE=api_key` with a static shared secret sent from browser JS --
that combination provides close to no real protection.
