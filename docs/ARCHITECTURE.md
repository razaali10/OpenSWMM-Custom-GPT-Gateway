# Architecture

## What this repository is

A standalone FastAPI service that lets a ChatGPT Custom GPT reach the
**entire ~565-tool surface** of an existing, independently deployed
[openswmm.mcp](https://github.com/HydroCouple/openswmm.mcp) server, without
exposing 565 individual OpenAPI operations (GPT Actions has a practical cap
around 30 operations per schema).

```
Custom GPT
    |
    | HTTPS / OpenAPI Actions  (~26 operations total)
    v
openswmm-gpt-gateway   <-- this repository
    |
    | MCP client (streamable-HTTP, remote)
    v
Existing OpenSWMM MCP Server   <-- Repository A, NOT modified, NOT imported
    |
    v
EPA SWMM / OpenSWMM / SWMM2D engine
```

This is a **sibling** project to `openswmm-mcp-server` (the curated REST
gateway with ~21 hand-composed endpoints), not a replacement for it. Both
point at the same live MCP server and can run simultaneously. The difference:

| | openswmm-mcp-server (REST gateway) | This repository |
|---|---|---|
| Endpoint count | ~21, each hand-composed | ~26, ~11 of which are generic dispatchers |
| Tool coverage | The subset each composed endpoint calls internally | **All** ~565 tools, dynamically |
| Session/file management | Owns its own session registry + file storage | None -- caller supplies `session_id` for an already-open upstream session |
| Best for | A small number of common workflows, simplest possible Custom GPT experience | Full tool access when 100% feature parity with MCP matters more than a curated experience |

## Why a dispatcher, not one operation per tool

The gateway exposes ~10 "grouped" endpoints (`POST /api/v1/tools/{group}`),
each accepting a generic `{tool_name, arguments}` body:

```json
{"tool_name": "links_set_loss_coeff", "arguments": {"session_id": "abc123", "link_id": "C25"}}
```

Every tool from the live registry is assigned to exactly one group
(`app/security/tool_policy.py`), by namespace prefix with a small number of
explicit overrides for tools whose name doesn't match their real engineering
domain (`spatial_get_quality` → `water-quality`, not `spatial`). A call to
the wrong group is rejected server-side with the correct group named in the
error -- this is enforced in code (`app/services/dispatcher.py`), never left
to the calling model's own judgment.

```
discover tool (searchOpenSwmmTools / listOpenSwmmNamespaces)
  → inspect schema (getOpenSwmmToolSchema)
  → determine correct action group (returned by the discovery calls)
  → call exact MCP tool (POST /api/v1/tools/{group})
  → return MCP result verbatim
```

## Action groups

| Group | Namespaces | Endpoint |
|---|---|---|
| core | `lifecycle_`, `model_`, `datetime_` | `POST /api/v1/tools/core` |
| model-builder | `building_`, `editing_`, `tables_` | `POST /api/v1/tools/model-builder` |
| hydrology | `subcatchments_`, `climate_`, `inflows_` | `POST /api/v1/tools/hydrology` |
| hydraulics | `nodes_`, `links_`, `xsect_` | `POST /api/v1/tools/hydraulics` |
| forcing-controls | `forcing_`, `controls_` | `POST /api/v1/tools/forcing-controls` |
| results | `query_`, `analysis_` | `POST /api/v1/tools/results` |
| twod | `twod_` | `POST /api/v1/tools/twod` |
| spatial | `spatial_`, `geopackage_` | `POST /api/v1/tools/spatial` |
| water-quality | `quality_`, `pollutants_` | `POST /api/v1/tools/water-quality` |
| infrastructure | `infrastructure_` | `POST /api/v1/tools/infrastructure` |
| optimization | `hotstart_`, `gym_` | `POST /api/v1/tools/optimization` |

Confirmed live against the deployed upstream (565 tools, 24 namespaces):

```
core: 67, forcing-controls: 22, hydraulics: 114, hydrology: 98,
infrastructure: 43, model-builder: 56, optimization: 34, results: 29,
spatial: 28, twod: 34, water-quality: 40
```

Run `python -m scripts.verify_registry` any time to get this live, not from
this document (which will drift as the upstream server evolves).

## Registry and dynamic discovery

`app/mcp/registry.py` (`MCPToolRegistry`) is the single source of truth for
tool metadata, refreshed from the live server with an in-memory TTL cache
(`MCP_TOOL_CACHE_TTL_SECONDS`, default 300s) -- never a hand-maintained
static catalog. Discovery endpoints:

- `GET /api/v1/mcp/namespaces` -- live namespace + action-group counts
- `POST /api/v1/mcp/search` -- lexical/fuzzy search over name, namespace,
  description, and argument names (no embedding database; verified against
  the project's own worked example -- searching *"change conduit entrance
  and exit losses"* correctly surfaces `links_set_loss_coeff` first)
- `GET /api/v1/mcp/tools/{tool_name}` -- the tool's real, live input schema,
  action group, and safety classification

## Safety classification

Every tool gets an `operation_class`: `READ`, `WRITE`, `SIMULATION_CONTROL`,
`DESTRUCTIVE`, or `OPTIMIZATION` (`app/security/tool_policy.py`). Classified
by namespace + verb heuristic (`gym_*` is always `OPTIMIZATION`;
`lifecycle_*` defaults to `SIMULATION_CONTROL` except pure getters; verbs
`delete_`/`clear_` are `DESTRUCTIVE`; `get_`/`list_`/`is_`/etc. are `READ`;
everything else is `WRITE`) -- verified against all seven of the project
brief's own worked examples (`tests/unit/test_tool_policy.py`). This
classification drives per-operation-class timeouts (see below); it is
reported to callers via `getOpenSwmmToolSchema` but does not currently block
a call outright (see "Known limitations").

## Timeouts

Three timeout classes (`app/config.py`), selected by the tool's
`operation_class`:

- `OPENSWMM_MCP_TIMEOUT_SECONDS` (default 30s) -- `READ`/`WRITE`
- `MCP_SIMULATION_TIMEOUT_SECONDS` (default 300s) -- `SIMULATION_CONTROL`
- `MCP_OPTIMIZATION_TIMEOUT_SECONDS` (default 30s) -- `OPTIMIZATION`

A timeout is reported as `504 UPSTREAM_MCP_TIMEOUT`, never silently
misreported as a successful simulation.

## Error semantics

One error envelope for everything:

```json
{"error": {"code": "WRONG_ACTION_GROUP", "message": "...", "details": {}}}
```

| Status | Code | When |
|---|---|---|
| 400 | `BAD_REQUEST` / `WRONG_ACTION_GROUP` | Invalid tool/group combination |
| 401 | `UNAUTHORIZED` | Missing/invalid API key |
| 404 | `MCP_TOOL_NOT_FOUND` | Tool doesn't exist on the live registry |
| 409 | `CONFLICT` | Reserved for future session/state-conflict use |
| 422 | `VALIDATION_ERROR` | Reserved for future request-shape validation |
| 502 | `UPSTREAM_MCP_ERROR` | The upstream MCP server itself rejected the call, or was unreachable |
| 504 | `UPSTREAM_MCP_TIMEOUT` | The upstream server didn't respond within its operation class's timeout |

## Known limitations

### 1. No file upload / session ownership

Unlike the sibling `openswmm-mcp-server` REST gateway, **this gateway owns no
file storage and does not create sessions on the caller's behalf.** Every
engineering endpoint (`/api/v1/engineering/*`) takes a caller-supplied
`session_id` for a session that must already be open on the upstream server.
To open one, call `lifecycle_open_model` through `POST /api/v1/tools/core`
directly, exactly as any MCP client would -- but that tool's `inp_path`
argument must point to a location the *upstream server's own process* can
read from its filesystem. This gateway has no mechanism to get a `.inp` file
onto that filesystem itself. In practice this means: use a model already
present in the upstream server's environment, or open one via the sibling
REST gateway (which shares the same session pool -- see its own
`docs/ARCHITECTURE.md`) and reuse that exact `session_id` here.

### 2. Baseline protection is not technically enforced

Section 10 of the project brief asks for baseline-vs-scenario protection
(reject destructive operations against a protected baseline session). The
upstream MCP server exposes no session metadata distinguishing "baseline"
from "scenario" sessions -- there is no flag, tag, or naming convention this
gateway can rely on. Per the brief's own instruction ("do not invent
scenario semantics if the MCP server does not expose sufficient
information"), this is **not implemented**, and is documented here rather
than faked. `operation_class: DESTRUCTIVE` is reported to callers via
`getOpenSwmmToolSchema` so a well-behaved Custom GPT can choose to be
cautious, but the gateway itself does not block the call.

### 3. Docker build not executed in this environment

No Docker daemon was available in the environment this repository was built
in. The `Dockerfile` was verified by static review (paths match the actual
`app/` package layout; `requirements.txt` matches versions already proven to
install and run in this exact environment) rather than an actual
`docker build`. Recommend running a real build before first deployment.

### 4. Integration tests exercise discovery + one safe read, not the full engineering workflow

Per the project brief's own testing rule (section 22: "do not execute
destructive tests against a production MCP server"), the live integration
suite (`tests/integration/`) is scoped to what that rule actually allows
against the shared production upstream: discovery (list/search/schema) and
one safe, session-independent read-only tool call
(`xsect_list_shapes`). The `/api/v1/engineering/*` endpoints' composition
logic is tested with a mocked client instead
(`tests/unit/test_engineering_services.py`) -- correct given limitation #1
above (there's no session to safely test against without either mutating
shared state or depending on the sibling repository's own session
bootstrap).
