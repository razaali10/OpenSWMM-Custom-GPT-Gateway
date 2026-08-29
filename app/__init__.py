"""OpenSWMM Custom GPT Gateway.

A standalone FastAPI service that exposes the ~565 tools of an *existing,
independently deployed* openswmm.mcp server to ChatGPT Custom GPT Actions.

This repository never imports openswmm_mcp/openswmm.engine code and never
runs the SWMM engine itself. It is purely a remote MCP client: every
request here ends as a `tools/call` (or `tools/list`) against the
OPENSWMM_MCP_URL configured in the environment. See docs/ARCHITECTURE.md.
"""
