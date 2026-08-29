# OpenSWMM Custom GPT Gateway

A standalone Custom GPT Actions gateway in front of an existing, independently
deployed [openswmm.mcp](https://github.com/HydroCouple/openswmm.mcp) server.
It exposes that server's **entire ~565-tool registry** through ~26 OpenAPI
operations -- ~11 grouped dispatcher Actions, 3 discovery endpoints, ~10
high-level engineering endpoints, and health/status -- instead of one
operation per tool, which GPT Actions cannot practically support at that
scale (~30 operations is the practical ceiling per Action schema).

## Why this is a separate repository

The existing `openswmm.mcp` server (Repository A) is authoritative and is
never modified or imported by this project. This repository (Repository B)
only ever reaches it through its published MCP interface, over the network,
exactly like any other MCP client (Claude Desktop, HuggingChat, a ChatGPT
Developer Mode connector). It has no dependency on `openswmm_mcp` or
`openswmm.engine` Python packages at all -- see `requirements.txt`. The two
repositories are independently deployable and can run simultaneously against
the same upstream server; see `docs/ARCHITECTURE.md` for how this differs
from the sibling `openswmm-mcp-server` REST gateway (~21 hand-composed
endpoints vs. this repo's ~11 generic dispatchers covering all 565 tools).

```
Custom GPT
    |
    | HTTPS / OpenAPI Actions  (~26 operations)
    v
openswmm-gpt-gateway  <-- this repository
    |
    | MCP client (streamable-HTTP, remote, no local import)
    v
Existing OpenSWMM MCP Server  (~565 tools, dynamically discovered)
    |
    v
EPA SWMM / OpenSWMM / SWMM2D engine
```

## Prerequisites

- Python 3.13 (or any 3.12+)
- An already-running `openswmm.mcp` server reachable over HTTPS (this
  project's own: `https://openswmm.onrender.com/mcp`)

## Local setup

```bash
pip install -r requirements.txt
cp .env.example .env    # edit OPENSWMM_MCP_URL if needed
uvicorn app.main:app --reload --port 8080
```

Then visit `http://localhost:8080/docs` for Swagger UI, or
`http://localhost:8080/api/v1/status` to confirm live upstream connectivity.

## Environment configuration

See `.env.example` for the full list. The only required variable is
`OPENSWMM_MCP_URL` -- there is no hardcoded production hostname in code.

## Connecting to OpenSWMM MCP

`app/mcp/client.py` opens one persistent connection at startup and reuses it
for the process's lifetime. See `docs/MCP_INTEGRATION.md` for the full
connection-lifecycle and result-unwrapping details, all verified live
against the actual deployed server while building this repository.

## Running FastAPI

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

## Docker deployment

```bash
docker build -t openswmm-gpt-gateway .
docker run -p 8080:8080 --env-file .env openswmm-gpt-gateway
```

Or `docker compose up --build` (reads the same env vars via
`docker-compose.yml`'s defaults). **Note:** the Docker build itself was
verified by static review only in this project's own build environment (no
Docker daemon was available there) -- run a real `docker build` before your
first deployment.

## Authentication

`AUTH_MODE=api_key` is the default (unlike the sibling REST gateway) -- this
gateway exposes destructive/optimization tools, so an open-by-default
posture is the wrong choice here. See `docs/SECURITY.md`.

## OpenAPI / Custom GPT setup

See `docs/CUSTOM_GPT_SETUP.md` for the full walkthrough and
`docs/CUSTOM_GPT_INSTRUCTIONS.md` for a ready-to-paste Instructions
template. Short version: import `openapi_custom_gpt.yaml` (edit its
`servers:` URL first) as a GPT Action, select Bearer auth, paste your
`GATEWAY_API_KEY`.

## Generating Knowledge files

```bash
python -m scripts.generate_tool_catalog
```

Writes `generated/OpenSWMM_MCP_Tool_Catalog.md` (every tool, from the live
registry, with its real description/schema/classification -- never
hand-invented) and `generated/OpenSWMM_Tool_Routing_Guide.md` (curated
task → action-group mapping). Both were generated against the live server
while building this repository; regenerate after any upstream change.

```bash
python -m scripts.verify_registry
```

Reports live reachability, total tool count, namespace/action-group counts,
and whether the small set of tools this gateway's engineering endpoints
depend on are still present.

## Running tests

```bash
pytest
```

44 tests: unit tests for classification, registry caching/search, dispatcher
routing/error-translation, auth, and engineering-service composition logic
(all against mocked MCP responses -- see `tests/unit/`), plus integration
tests against the real live upstream server, scoped to discovery and one
safe read-only tool call per the project's own testing rule ("do not execute
destructive tests against a production MCP server" -- see
`tests/integration/`).

## Safety model

Every tool gets a `READ`/`WRITE`/`SIMULATION_CONTROL`/`DESTRUCTIVE`/
`OPTIMIZATION` classification (`app/security/tool_policy.py`), reported via
`getOpenSwmmToolSchema`. Each grouped dispatcher endpoint enforces its
allowed tool set server-side -- a wrong tool/group combination is rejected
with a `400` naming the correct group, never silently routed or left to the
calling model's judgment. See `docs/SECURITY.md` for what this gateway can
and cannot protect against.

## Limitations

- **No file upload / session management** -- this gateway takes a
  caller-supplied `session_id` for an already-open upstream session; it
  owns no storage of its own.
- **Baseline protection is not technically enforced** -- the upstream server
  exposes no metadata to distinguish a protected baseline session from an
  expendable scenario.
- **Docker build unverified** in this project's own build environment (no
  Docker daemon available there).
- **Integration tests are scoped to discovery + one safe read**, not a full
  engineering workflow, per the project's own testing rule against a shared
  production upstream.

Full detail on all four: `docs/ARCHITECTURE.md` "Known limitations".

## Source

- [openswmm.mcp](https://github.com/HydroCouple/openswmm.mcp) -- the MCP
  server this gateway connects to (not modified, not imported)
- [openswmm.engine](https://github.com/HydroCouple/openswmm.engine) -- the
  SWMM 6 engine bindings that server wraps
- The sibling `openswmm-mcp-server` REST gateway -- a curated, ~21-endpoint
  alternative against the same upstream server, better suited when a small
  set of common workflows matters more than full tool coverage
