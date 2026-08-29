# Project: OpenSWMM Custom GPT Gateway

You are a senior Python/FastAPI/MCP integration engineer.

Your task is to design and implement a **new standalone GitHub repository** that acts as a Custom GPT Actions gateway in front of the existing OpenSWMM MCP server.

## CRITICAL ARCHITECTURAL REQUIREMENT

The existing OpenSWMM MCP server is authoritative and MUST NOT be modified.

The MCP server exists separately and exposes approximately 565 tools across namespaces such as:

- `lifecycle_*`
- `query_*`
- `forcing_*`
- `analysis_*`
- `building_*`
- `editing_*`
- `hotstart_*`
- `spatial_*`
- `geopackage_*`
- `tables_*`
- `inflows_*`
- `controls_*`
- `climate_*`
- `infrastructure_*`
- `nodes_*`
- `links_*`
- `subcatchments_*`
- `pollutants_*`
- `model_*`
- `quality_*`
- `twod_*`
- `datetime_*`
- `xsect_*`
- `gym_*`

The new project must be a completely separate repository.

Suggested repository name:

`openswmm-gpt-gateway`

Do NOT:
- edit the OpenSWMM MCP repository;
- copy MCP server internals into this repository;
- alter MCP tool implementations;
- monkey-patch the MCP server;
- create a fork that becomes the primary implementation;
- duplicate hydraulic or hydrologic calculation logic;
- reimplement SWMM calculations in the gateway.

The gateway must communicate with the existing MCP server through its published MCP interface.

The architecture must remain:

```text
Custom GPT
    |
    | HTTPS / OpenAPI Actions
    v
openswmm-gpt-gateway
    |
    | MCP client
    v
Existing OpenSWMM MCP Server
    |
    v
EPA SWMM / OpenSWMM / SWMM2D
```

The MCP server remains the authoritative modelling and computational layer.

---

# 1. Objective

Build a production-quality FastAPI service that lets a ChatGPT Custom GPT access the approximately 565 OpenSWMM MCP tools without exposing all 565 as individual OpenAPI operations.

The Custom GPT Actions API should instead expose:

1. high-level engineering workflow endpoints;
2. tool discovery endpoints;
3. approximately 10 grouped MCP dispatcher endpoints.

The gateway should make the complete underlying MCP tool registry accessible while keeping the OpenAPI schema compact and understandable.

---

# 2. Primary design principle

Do not expose one OpenAPI operation per MCP tool.

Instead expose grouped Actions.

Target approximately 20–30 OpenAPI operations total.

The full underlying 565-tool registry must remain dynamically discoverable and callable.

The Custom GPT should be able to:

```text
discover tool
→ inspect schema
→ determine correct action group
→ call exact MCP tool
→ return MCP result
```

The gateway must never fabricate MCP tool schemas or results.

---

# 3. Required grouped Actions

Implement the following grouped execution endpoints.

## 3.1 SWMM Core

Endpoint concept:

`POST /api/v1/tools/core`

Allowed namespaces:

```text
lifecycle_*
model_*
datetime_*
```

Purpose:

- open/close simulations;
- simulation lifecycle;
- stepping;
- timing;
- model configuration;
- unit system;
- metadata;
- date/time utilities.

---

## 3.2 Model Builder

Endpoint:

`POST /api/v1/tools/model-builder`

Allowed namespaces:

```text
building_*
editing_*
tables_*
```

Purpose:

- build models;
- edit models;
- add/delete/rename elements;
- curves;
- time series;
- patterns.

---

## 3.3 Hydrology

Endpoint:

`POST /api/v1/tools/hydrology`

Allowed namespaces primarily:

```text
subcatchments_*
climate_*
```

Also permit explicitly categorized hydrologic `inflows_*` operations such as:

- DWF;
- RDII;
- external hydraulic inflows;
- unit hydrographs.

Do not route water-quality concentration inflows through this endpoint unless explicitly classified as hydrology.

---

## 3.4 Hydraulics

Endpoint:

`POST /api/v1/tools/hydraulics`

Allowed namespaces:

```text
nodes_*
links_*
xsect_*
```

Purpose:

- node hydraulics;
- storage;
- outfalls;
- dividers;
- conduits;
- pumps;
- weirs;
- orifices;
- outlets;
- culverts;
- hydraulic cross-sections;
- statistics.

---

## 3.5 Forcing and Controls

Endpoint:

`POST /api/v1/tools/forcing-controls`

Allowed namespaces:

```text
forcing_*
controls_*
```

Purpose:

- runtime forcing;
- rainfall overrides;
- climate forcing;
- RTC;
- rules;
- link settings/status.

---

## 3.6 Results and QA/QC

Endpoint:

`POST /api/v1/tools/results`

Allowed namespaces:

```text
query_*
analysis_*
```

Purpose:

- model inventory;
- results;
- flooding;
- capacity;
- statistics;
- continuity;
- mass balance;
- report snapshots;
- time series;
- scenario comparison;
- binary output inspection.

---

## 3.7 Surface 2D

Endpoint:

`POST /api/v1/tools/twod`

Allowed namespace:

```text
twod_*
```

Purpose:

- mesh;
- terrain;
- Manning roughness;
- 2D state;
- surface depths;
- velocities;
- mass balance;
- coupling;
- boundary conditions;
- barriers;
- solver parameters;
- rainfall/evaporation forcing;
- triangle initial conditions.

Keep this separate from general 1D hydraulics.

---

## 3.8 Spatial / GIS

Endpoint:

`POST /api/v1/tools/spatial`

Allowed namespaces:

```text
spatial_*
geopackage_*
```

Purpose:

- coordinates;
- polygons;
- vertices;
- model geometry;
- CRS;
- GeoPackage;
- observed data;
- calibration datasets.

Some spatial operations may involve water quality or LID placement. Create a registry classification so these can still be routed correctly.

---

## 3.9 Water Quality

Endpoint:

`POST /api/v1/tools/water-quality`

Allowed namespaces:

```text
quality_*
pollutants_*
```

Plus explicitly classified water-quality operations from:

```text
inflows_*
spatial_*
```

Purpose:

- pollutants;
- buildup;
- washoff;
- treatment;
- concentrations;
- quality state.

---

## 3.10 Infrastructure / Optimization

Prefer TWO endpoints rather than one if operation count permits.

### Infrastructure

`POST /api/v1/tools/infrastructure`

Allowed namespace:

```text
infrastructure_*
```

Purpose:

- LIDs;
- streets;
- inlets;
- transects.

### State / Optimization

`POST /api/v1/tools/optimization`

Allowed namespaces:

```text
hotstart_*
gym_*
```

Purpose:

- hotstart;
- state cloning;
- optimization;
- RL environments;
- policy application;
- design optimization;
- job management.

If optimization operations require separate privilege controls, implement them.

---

# 4. Tool discovery API

Implement dynamic discovery against the live MCP server.

Do NOT maintain a manually hard-coded catalog of all 565 tools unless used only as a cache or fallback.

The live MCP registry is authoritative.

Implement:

## 4.1 List namespaces

`GET /api/v1/mcp/namespaces`

Example response:

```json
{
  "tool_count": 565,
  "namespaces": {
    "lifecycle": 20,
    "nodes": 50,
    "links": 60,
    "twod": 40
  }
}
```

Counts shown above are examples only.

Always calculate actual counts from the live MCP server.

---

## 4.2 Search tools

`POST /api/v1/mcp/search`

Request:

```json
{
  "query": "change conduit entrance and exit losses",
  "namespace": "links",
  "limit": 10
}
```

Response:

```json
{
  "matches": [
    {
      "name": "links_set_loss_coeff",
      "namespace": "links",
      "description": "...",
      "action_group": "hydraulics",
      "operation_class": "WRITE"
    }
  ]
}
```

Search should consider:

- tool name;
- namespace;
- MCP description;
- input schema property names;
- manually assigned aliases if necessary.

A simple high-quality lexical/fuzzy search is sufficient initially.

Do not introduce an embedding database unless justified.

---

## 4.3 Get tool schema

`GET /api/v1/mcp/tools/{tool_name}`

Return the live MCP description and input schema.

Example:

```json
{
  "name": "links_set_loss_coeff",
  "namespace": "links",
  "action_group": "hydraulics",
  "description": "...",
  "input_schema": {},
  "operation_class": "WRITE",
  "destructive": false
}
```

Do not rewrite the MCP input schema in a way that could change argument semantics.

Preserve it as closely as practical.

---

# 5. Generic grouped request model

All grouped endpoints should accept a standard request format such as:

```json
{
  "tool_name": "links_set_loss_coeff",
  "arguments": {
    "session_id": "abc123",
    "link_id": "C25"
  }
}
```

Pydantic model:

```python
class ToolCallRequest(BaseModel):
    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)
```

Response should preserve useful MCP result content without unnecessary transformation.

Example:

```json
{
  "success": true,
  "tool_name": "links_set_loss_coeff",
  "result": {},
  "warnings": []
}
```

If the MCP call fails:

```json
{
  "success": false,
  "tool_name": "links_set_loss_coeff",
  "error": {
    "type": "...",
    "message": "..."
  }
}
```

Do not convert a failed MCP result into an apparent success.

---

# 6. Namespace enforcement

Each grouped endpoint MUST enforce its allowed tool set server-side.

Example:

```python
ALLOWED_PREFIXES = {
    "hydraulics": (
        "nodes_",
        "links_",
        "xsect_",
    )
}
```

If a request is sent to:

```text
/api/v1/tools/hydraulics
```

with:

```text
editing_delete_object
```

reject it.

Return a useful 400-series response describing the correct action group if known.

Do not rely on the Custom GPT prompt alone for namespace security.

---

# 7. Tool registry service

Build a central registry abstraction.

Suggested class:

```python
class MCPToolRegistry:
    async def refresh(self) -> None: ...
    async def list_tools(self) -> list[MCPTool]: ...
    async def get_tool(self, name: str) -> MCPTool: ...
    async def search(self, query: str, ...) -> list[MCPTool]: ...
    def get_action_group(self, tool_name: str) -> str: ...
    def get_operation_class(self, tool_name: str) -> str: ...
```

The registry should populate itself dynamically from the MCP server.

Cache tool metadata in memory with a configurable TTL.

Example:

```text
MCP_TOOL_CACHE_TTL_SECONDS=300
```

Provide a manual refresh endpoint only if useful.

Do not persist stale schemas permanently as authoritative data.

---

# 8. MCP client

Implement a clean MCP client abstraction.

Suggested module:

```text
app/mcp/client.py
```

Responsibilities:

- connect to remote MCP server;
- list tools;
- inspect schemas;
- invoke tools;
- propagate MCP errors;
- reconnect where reasonable;
- handle timeout configuration.

Environment variables should include something like:

```text
OPENSWMM_MCP_URL=
OPENSWMM_MCP_TRANSPORT=
OPENSWMM_MCP_TIMEOUT_SECONDS=
```

Do not hardcode a production hostname.

If the existing server supports streamable HTTP MCP, use the official/recommended MCP Python client mechanism.

Do not scrape web pages.

Do not depend on undocumented internal server objects.

---

# 9. Safety classification

Each MCP tool should receive a gateway-side operation classification.

At minimum:

```text
READ
WRITE
SIMULATION_CONTROL
DESTRUCTIVE
OPTIMIZATION
```

Examples:

```text
query_get_node_info
READ

analysis_get_mass_balance
READ

links_set_loss_coeff
WRITE

building_add_node
WRITE

lifecycle_step_simulation
SIMULATION_CONTROL

editing_delete_object
DESTRUCTIVE

gym_start_optimization
OPTIMIZATION
```

Implement classification primarily using:

1. exact overrides for exceptional tools;
2. namespace;
3. action verbs in the tool name.

Keep classification rules in a dedicated module.

Suggested:

```text
app/security/tool_policy.py
```

---

# 10. Baseline protection

The gateway must support safe engineering workflows.

The source/baseline model is authoritative.

Do not silently mutate an authoritative baseline model.

Where session/scenario metadata makes this possible, support a concept such as:

```text
baseline
working
scenario
```

At minimum:

- READ operations may run against baseline;
- simulation operations may run against baseline;
- WRITE operations should preferably target a working/scenario session;
- DESTRUCTIVE operations should be rejected against protected baseline sessions;
- destructive operations should require explicit request metadata where practical.

Do not invent scenario semantics if the MCP server does not expose sufficient information.

If baseline protection cannot be enforced technically because the upstream session does not expose enough metadata, document this limitation prominently.

---

# 11. High-level engineering endpoints

In addition to raw grouped MCP access, implement or retain a small set of high-level engineering workflow endpoints where they provide real value.

Do not duplicate SWMM calculations.

High-level endpoints should orchestrate underlying MCP tools.

Candidate endpoints:

```text
POST /api/v1/engineering/validate-model

POST /api/v1/engineering/run-simulation

GET /api/v1/engineering/simulation-integrity

GET /api/v1/engineering/model-inventory

GET /api/v1/engineering/flooding-analysis

GET /api/v1/engineering/summary

POST /api/v1/engineering/compare-scenarios

GET /api/v1/engineering/twod-summary

GET /api/v1/engineering/twod-mass-balance

GET /api/v1/engineering/twod-coupling
```

Do not expose a high-level endpoint if it would simply duplicate a single MCP call without adding meaningful workflow or safety value.

---

# 12. Simulation integrity workflow

The engineering layer must treat execution integrity as mandatory before interpreting simulation results.

Where supported by available MCP tools, assess:

1. simulation completed;
2. errors/warnings;
3. continuity / mass balance;
4. numerical stability;
5. simulation period;
6. rainfall/event;
7. 2D continuity if active.

Do not return a simple:

```json
{"status": "passed"}
```

without underlying evidence.

Return raw relevant metrics.

Example:

```json
{
  "simulation_completed": true,
  "flow_continuity_error_pct": 0.3,
  "runoff_continuity_error_pct": 0.2,
  "twod_continuity_error_pct": 0.7,
  "warnings": [],
  "interpretation": "..."
}
```

Never fabricate thresholds if the gateway has not been configured with them.

---

# 13. Flooding analysis workflow

Create a high-level flooding-analysis service only if it can be based on real MCP outputs.

Recommended diagnostic sequence:

```text
flooded node
→ node inflow
→ depth/head/surcharge
→ upstream link capacity
→ downstream capacity
→ backwater/outlet restrictions
→ storage
→ 1D/2D exchange
→ likely cause
```

Do not simply report flood volume.

Clearly distinguish:

- MCP-computed evidence;
- gateway engineering interpretation;
- uncertainty.

---

# 14. 1D / 2D handling

The OpenSWMM server includes native 2D capabilities.

The gateway must not assume water leaving the 1D drainage system is lost if an active coupled 2D surface exists.

When appropriate, engineering workflows should inspect available tools including:

```text
twod_get_mesh_summary
twod_get_mesh_geometry
twod_get_mass_balance
twod_get_coupling_map
twod_get_stats
twod_get_totals
twod_get_state
twod_get_state_bulk
```

Do not hardcode these as the only available 2D tools.

Discover the current registry.

---

# 15. Optimization isolation

Treat `gym_*` tools as higher-risk / higher-cost operations.

Implement separate policy for:

- starting optimization jobs;
- cancelling jobs;
- applying designs;
- applying policies;
- interactive environment manipulation.

Prefer endpoint:

```text
POST /api/v1/tools/optimization
```

instead of mixing these operations with ordinary engineering analysis.

Where possible expose useful job metadata in responses.

Do not start optimization implicitly just because a user asks for a recommendation.

---

# 16. Authentication

Provide configurable API authentication between Custom GPT Actions and this gateway.

Minimum acceptable approach:

```text
Authorization: Bearer <API_KEY>
```

Configuration:

```text
GATEWAY_API_KEY=
```

Do not commit secrets.

Include:

```text
.env.example
```

Add middleware or dependency-based authentication.

Health endpoint may remain unauthenticated if desired.

---

# 17. OpenAPI schema

Produce a Custom GPT-friendly OpenAPI 3.x schema.

File:

```text
openapi_custom_gpt.yaml
```

Requirements:

- concise operation IDs;
- meaningful descriptions;
- avoid exposing all 565 tools individually;
- use grouped dispatcher actions;
- include discovery actions;
- include high-level engineering actions;
- clear request/response schemas;
- do not use unsupported OpenAPI features unnecessarily;
- keep descriptions focused enough for tool selection.

Suggested operation IDs:

```text
listOpenSwmmNamespaces
searchOpenSwmmTools
getOpenSwmmToolSchema

callSwmmCoreTool
callModelBuilderTool
callHydrologyTool
callHydraulicsTool
callForcingControlsTool
callResultsTool
call2DTool
callSpatialTool
callWaterQualityTool
callInfrastructureTool
callOptimizationTool

validateModel
runSimulation
getSimulationIntegrity
getModelInventory
analyzeFlooding
getEngineeringSummary
compareScenarios
get2DSummary
get2DMassBalance
get2DCoupling
```

Adjust only where necessary.

---

# 18. Knowledge generation

Create a utility that can generate Custom GPT Knowledge documentation from the live MCP registry.

Command concept:

```bash
python -m scripts.generate_tool_catalog
```

Generate:

```text
generated/
  OpenSWMM_MCP_Tool_Catalog.md
  OpenSWMM_Tool_Routing_Guide.md
```

## Tool Catalog

Include for every MCP tool:

- tool name;
- namespace;
- action group;
- description;
- operation class;
- destructive status;
- input arguments/schema;
- output information if available.

Example:

```markdown
## links_set_loss_coeff

Namespace: links  
Action Group: hydraulics  
Operation Class: WRITE  
Destructive: No

### Description

...

### Input Schema

...
```

Do not manually invent missing MCP descriptions.

---

# 19. Routing guide

Generate a second concise Knowledge file organized around engineering tasks.

Examples:

```text
Model inventory
Flood investigation
Pipe capacity review
Pump analysis
Storage analysis
Rainfall-runoff review
Groundwater review
RDII review
Water quality review
2D surface flooding
1D/2D coupling
RTC controls
Model construction
Model modification
Scenario comparison
LID design
Optimization
```

The routing guide should map engineering tasks to likely namespaces/tools.

It may use curated logic, but clearly distinguish:

```text
preferred tools
supporting tools
write operations
```

---

# 20. Custom GPT instruction template

Create:

```text
docs/CUSTOM_GPT_INSTRUCTIONS.md
```

It should provide a ready-to-copy prompt for configuring the OpenSWMM Engineer Custom GPT.

Include rules such as:

```text
The OpenSWMM tool registry is dynamically available through
searchOpenSwmmTools and getOpenSwmmToolSchema.

Do not guess MCP tool parameters.

If the correct raw MCP tool is uncertain:
1. search for it;
2. retrieve its schema;
3. call the corresponding grouped Action.

Preserve the authoritative baseline.

Before consequential hydraulic interpretation:
1. verify simulation execution;
2. review continuity/mass balance;
3. review warnings;
4. verify relevant simulation period/event.

For flooding:
diagnose hydraulic cause before recommending changes.

For coupled 1D/2D models:
evaluate surface mass balance and coupling before assuming
1D flooding represents lost water.

Clearly distinguish:
- model-computed evidence;
- engineering interpretation;
- assumptions;
- recommendations.

Never fabricate model results or MCP outputs.
```

---

# 21. Repository structure

Use a clean structure similar to:

```text
openswmm-gpt-gateway/
│
├── app/
│   ├── main.py
│   ├── config.py
│   │
│   ├── api/
│   │   ├── health.py
│   │   ├── discovery.py
│   │   ├── grouped_tools.py
│   │   └── engineering.py
│   │
│   ├── mcp/
│   │   ├── client.py
│   │   ├── registry.py
│   │   └── models.py
│   │
│   ├── services/
│   │   ├── dispatcher.py
│   │   ├── simulation.py
│   │   ├── flooding.py
│   │   ├── integrity.py
│   │   └── twod.py
│   │
│   ├── security/
│   │   ├── auth.py
│   │   └── tool_policy.py
│   │
│   └── schemas/
│       ├── common.py
│       ├── tools.py
│       └── engineering.py
│
├── scripts/
│   ├── generate_tool_catalog.py
│   └── verify_registry.py
│
├── generated/
│   └── .gitkeep
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── CUSTOM_GPT_SETUP.md
│   ├── CUSTOM_GPT_INSTRUCTIONS.md
│   ├── SECURITY.md
│   └── MCP_INTEGRATION.md
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
├── openapi_custom_gpt.yaml
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── .env.example
├── .gitignore
├── README.md
└── LICENSE
```

Adjust if justified, but keep a modular separation.

---

# 22. Testing

Write meaningful tests.

## Unit tests

Test:

- prefix routing;
- namespace grouping;
- operation classification;
- destructive detection;
- request validation;
- MCP error propagation;
- authentication;
- tool search;
- cache behavior.

## Integration tests

Where an MCP server is available, test:

```text
list tools
→ find known tool
→ inspect schema
→ execute safe read-only tool
```

Do not execute destructive tests against a production MCP server.

Use mocked MCP responses for write/destructive operations.

---

# 23. Registry verification

Create:

```text
scripts/verify_registry.py
```

This should connect to the configured MCP server and report:

```text
MCP server reachable: yes
Total tools: N

Namespaces:
analysis: N
building: N
controls: N
...
twod: N
```

Also verify critical tools if present:

```text
twod_get_mesh_summary
twod_get_mass_balance
analysis_compare_scenarios
```

Do not hard-fail merely because the total number is not exactly 565.

The server evolves.

Treat the live count as authoritative.

---

# 24. Observability

Add structured logging.

Log at least:

- request ID;
- action group;
- MCP tool name;
- execution duration;
- success/failure;
- MCP error class.

Do NOT log:

- API keys;
- secrets;
- sensitive large model payloads by default.

Provide configurable log level.

---

# 25. Timeouts

MCP operations can vary substantially in execution time.

Provide configurable timeout classes, for example:

```text
MCP_DEFAULT_TIMEOUT_SECONDS=
MCP_SIMULATION_TIMEOUT_SECONDS=
MCP_OPTIMIZATION_TIMEOUT_SECONDS=
```

Do not allow an HTTP timeout to be misreported as a successful simulation.

For genuinely long-running optimization operations, preserve upstream job-based behavior rather than blocking unnecessarily.

---

# 26. Error semantics

Return useful HTTP status codes.

Examples:

```text
400
invalid tool/group combination

401
authentication failure

404
MCP tool does not exist

409
operation conflicts with session/model state

422
argument validation issue

502
upstream MCP error

504
MCP timeout
```

Where MCP provides structured error details, preserve them safely.

---

# 27. Do not fabricate argument schemas

This rule is critical.

If the live MCP server exposes:

```text
links_set_loss_coeff
```

but the gateway has not successfully retrieved its input schema, do not invent arguments.

Return a discovery/schema error.

The gateway must be schema-aware, not assumption-driven.

---

# 28. Avoid unnecessary argument duplication

The grouped dispatcher schema should remain generic.

Do not create giant Pydantic models containing hundreds of possible parameters.

Use:

```python
tool_name: str
arguments: dict[str, Any]
```

Validate tool existence/group server-side and allow the upstream MCP schema/tool call to perform tool-specific validation.

If the MCP SDK provides JSON-schema validation before execution, use it.

---

# 29. README

Write a complete README covering:

1. purpose;
2. architecture;
3. why this is a separate repository;
4. prerequisites;
5. local setup;
6. environment configuration;
7. connecting to OpenSWMM MCP;
8. running FastAPI;
9. Docker deployment;
10. authentication;
11. OpenAPI/Custom GPT setup;
12. generating Knowledge files;
13. running tests;
14. safety model;
15. limitations.

Include a clear architecture diagram.

Example:

```text
┌─────────────────────┐
│ OpenSWMM Custom GPT │
└─────────┬───────────┘
          │ HTTPS
          ▼
┌─────────────────────────┐
│ openswmm-gpt-gateway    │
│                         │
│ Actions / discovery     │
│ policy / engineering    │
└─────────┬───────────────┘
          │ MCP
          ▼
┌─────────────────────────┐
│ Existing OpenSWMM MCP   │
│ ~565 dynamically        │
│ discoverable tools      │
└─────────┬───────────────┘
          │
          ▼
┌─────────────────────────┐
│ SWMM / OpenSWMM / 2D    │
└─────────────────────────┘
```

---

# 30. Separate repository enforcement

This requirement must be explicit throughout the implementation.

Assume:

```text
Repository A:
openswmm / openswmm.mcp
```

already exists.

Create:

```text
Repository B:
openswmm-gpt-gateway
```

Repository B is allowed to:

- connect to Repository A's running MCP server;
- depend on public MCP SDK packages;
- document the MCP server URL;
- discover MCP tools dynamically.

Repository B must not:

- import code using relative/local imports from Repository A;
- modify Repository A;
- require Repository A's Git working tree;
- write files inside Repository A;
- require a Git submodule of Repository A;
- copy proprietary/internal server implementation files into Repository B.

The repositories must be independently deployable.

---

# 31. Development sequence

Implement in this order.

## Phase 1 — inspect and plan

Before changing code:

1. inspect the current working directory;
2. confirm whether this is already a new standalone repository;
3. if the working directory is the OpenSWMM MCP repository, STOP modifying files there;
4. create or switch to a sibling/new directory for `openswmm-gpt-gateway`;
5. document the intended architecture.

Do not modify the MCP repository.

---

## Phase 2 — MCP connectivity

Implement:

- config;
- MCP client;
- list tools;
- tool schema retrieval;
- test connection.

Demonstrate live registry enumeration.

---

## Phase 3 — registry

Implement:

- namespace extraction;
- action group assignment;
- tool search;
- operation classification;
- caching.

---

## Phase 4 — grouped Actions

Implement all grouped dispatch endpoints.

Verify namespace enforcement.

---

## Phase 5 — high-level engineering API

Implement only workflows that can be grounded in MCP evidence.

Prioritize:

- inventory;
- simulation;
- simulation integrity;
- flooding;
- 2D summary;
- scenario comparison.

---

## Phase 6 — Custom GPT assets

Generate:

```text
openapi_custom_gpt.yaml
docs/CUSTOM_GPT_INSTRUCTIONS.md
generated/OpenSWMM_MCP_Tool_Catalog.md
generated/OpenSWMM_Tool_Routing_Guide.md
```

---

## Phase 7 — tests and deployment

Add:

- unit tests;
- integration tests;
- Dockerfile;
- docker-compose;
- CI workflow if appropriate.

---

# 32. Git practices

Initialize this as its own Git repository.

Do not perform destructive Git operations.

Use meaningful commits.

Suggested commit sequence:

```text
feat: initialize standalone OpenSWMM GPT gateway
feat: add remote MCP client and registry discovery
feat: add grouped MCP action dispatchers
feat: add engineering workflow services
feat: add Custom GPT OpenAPI schema
feat: add generated MCP knowledge catalog
test: add registry and dispatcher coverage
docs: document deployment and Custom GPT setup
```

If GitHub CLI authentication is available, create a new GitHub repository named:

```text
openswmm-gpt-gateway
```

Do not create the repository under an unintended organization or account without checking the authenticated GitHub context first.

If repository creation credentials are unavailable, leave the local Git repo complete and print the exact commands the user should run.

---

# 33. Quality requirements

Use:

- Python 3.12 or current compatible version;
- FastAPI;
- Pydantic v2;
- async I/O;
- type annotations;
- clear docstrings where useful;
- pytest;
- httpx for HTTP testing where appropriate;
- official MCP client libraries where practical.

Prefer simple maintainable architecture over excessive abstraction.

Do not build unnecessary frontend/UI components.

This project is primarily an API gateway for Custom GPT Actions.

---

# 34. Engineering integrity requirements

Never:

- fabricate simulation outputs;
- fabricate MCP responses;
- fabricate tool availability;
- silently suppress MCP warnings;
- convert failed simulations into success;
- claim engineering compliance without evidence;
- overwrite authoritative models;
- infer 2D mass conservation from 1D results alone.

When providing engineering interpretation, label the distinction between:

```text
MODEL EVIDENCE
ENGINEERING INTERPRETATION
ASSUMPTION
RECOMMENDATION
```

---

# 35. Acceptance criteria

The project is complete when all of the following are true.

### Architecture

- standalone repository exists;
- no modifications made to the OpenSWMM MCP server repository;
- gateway communicates remotely with MCP.

### Discovery

- live MCP tools can be listed;
- live total tool count is reported;
- namespaces are dynamically identified;
- individual tool schemas can be retrieved;
- tools can be searched.

### Execution

- all discovered tools can be routed through an appropriate grouped Action where policy permits;
- wrong Action-group routing is rejected;
- MCP errors are preserved.

### Custom GPT

- OpenAPI schema is importable into Custom GPT Actions;
- approximately 10 grouped tool Actions exist;
- discovery operations exist;
- engineering endpoints exist;
- operation IDs are understandable.

### Knowledge

- tool catalog can be generated from the live server;
- routing guide is generated;
- Custom GPT instruction document exists.

### Safety

- read/write/destructive classifications exist;
- destructive tools receive stricter treatment;
- secrets are not committed;
- authoritative MCP server remains untouched.

### Testing

- unit tests pass;
- integration discovery tests pass when MCP server is configured.

---

# 36. Final delivery

When finished, provide:

1. final repository tree;
2. explanation of architecture;
3. list of OpenAPI operations;
4. actual MCP tool count discovered;
5. namespace counts;
6. test results;
7. startup command;
8. Docker startup command;
9. Custom GPT configuration instructions;
10. any limitations;
11. Git status;
12. GitHub repository URL if it was created.

Also explicitly state:

```text
The existing OpenSWMM MCP server repository was not modified.
```

Do not merely describe what should be built.

Implement the repository, run the tests, inspect the generated OpenAPI schema, and verify the MCP registry against the configured server wherever access is available.

If access to the live MCP endpoint is unavailable, implement the full gateway with mocked test fixtures and clearly identify which integration checks remain dependent on the live server.