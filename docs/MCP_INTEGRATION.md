# MCP Integration

## The one dependency: OPENSWMM_MCP_URL

This repository connects to an existing, independently deployed
`openswmm.mcp` server over its published streamable-HTTP MCP interface.
There is no hardcoded production hostname in code -- `OPENSWMM_MCP_URL` must
be set explicitly (`.env.example` shows this project's own live deployment
as the working example: `https://openswmm.onrender.com/mcp`).

`app/mcp/client.py`'s `MCPClient` wraps `fastmcp.Client(url)` exactly the
way any other MCP client would (Claude Desktop, HuggingChat, a ChatGPT
Developer Mode connector) -- it never imports `openswmm_mcp` or
`openswmm.engine` Python packages, and this repository does not list them as
dependencies at all (see `requirements.txt`). That's the actual mechanism
behind the project brief's "must not modify/import Repository A" constraint
-- it's enforced by dependency list and by the client only ever seeing the
server through its public protocol boundary.

## Connection lifecycle

One persistent connection is opened at process startup
(`app/main.py`'s `lifespan`) and reused for the process's lifetime, not
reconnected per request. If the connection drops mid-call, the client tears
itself down and reconnects lazily on the *next* call rather than retrying
silently within the failed request -- a persistently-down upstream fails
fast and visibly instead of doubling every request's latency while masking
the outage.

## What "the registry is authoritative" means in practice

`app/mcp/registry.py` never hand-maintains a list of the ~565 tools. Every
namespace count, action-group assignment, and tool schema in this
repository's docs and generated Knowledge files was produced by actually
calling `tools/list` against the live server (`scripts/verify_registry.py`,
`scripts/generate_tool_catalog.py`) -- not transcribed from the project
brief's own illustrative examples, which are explicitly marked in that
document as "counts shown above are examples only."

## Verified against the live server while building this repository

- Tool count: 565 (matches the sibling REST gateway's own independent count)
- Namespaces: 24
- All 7 of the project brief's own operation-class worked examples check out
  under this repo's classification heuristic
- The project brief's own search worked example ("change conduit entrance
  and exit losses" → `links_set_loss_coeff`) returns exactly that tool as
  the top hit
- A real tool call (`xsect_list_shapes`) through the full HTTP stack
  (dispatcher → MCP client → live upstream) returns genuine engine data (26
  real cross-section shapes), not a placeholder

## Result unwrapping

FastMCP wraps a tool whose return type is a bare list as
`{"result": [...]}` in `structured_content`, since MCP's `structuredContent`
must be a JSON object. `app/mcp/client.py`'s `call_tool` unwraps this
(`isinstance(content, dict) and set(content.keys()) == {"result"}`) so
callers of this gateway always see the tool's real return shape, never the
wrapper -- this was discovered and verified live while building the sibling
REST gateway against this exact server, and reproduced here.
