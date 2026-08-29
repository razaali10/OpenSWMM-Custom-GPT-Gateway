# Setting up a Custom GPT against this gateway

## 1. Deploy the gateway

Any host that can run the Dockerfile works (Render, Fly.io, a VPS, ...).
Minimum required env var: `OPENSWMM_MCP_URL` (see `.env.example`). Set
`AUTH_MODE=api_key` and `GATEWAY_API_KEY=<a strong random value>` before
exposing this publicly -- see `docs/SECURITY.md` for why this gateway's
default differs from the sibling REST gateway's.

```bash
docker build -t openswmm-gpt-gateway .
docker run -p 8080:8080 \
  -e OPENSWMM_MCP_URL=https://openswmm.onrender.com/mcp \
  -e AUTH_MODE=api_key \
  -e GATEWAY_API_KEY=your-strong-key-here \
  openswmm-gpt-gateway
```

Verify:
- `https://<your-deployment>/health` → `{"status": "ok", ...}`, no auth needed
- `https://<your-deployment>/api/v1/status` → confirms upstream MCP connectivity and live tool count, no auth needed
- `https://<your-deployment>/docs` → Swagger UI (will prompt for the bearer key to actually try endpoints)

## 2. Get the OpenAPI schema

`openapi_custom_gpt.yaml` at the repo root is generated directly from the
live `/openapi.json` (see the file's own header comment for the exact
command) -- edit its `servers:` URL to your actual deployment before
importing, or point GPT Actions at `https://<your-deployment>/openapi.json`
directly for a schema that's always in sync with the running code.

## 3. Create the Custom GPT

1. **Explore GPTs → Create → Configure.**
2. Name it, then paste `docs/CUSTOM_GPT_INSTRUCTIONS.md`'s template into
   the Instructions field.
3. **Actions → Create new action → Import from URL** (or paste the schema),
   using `openapi_custom_gpt.yaml` with your deployment's URL filled in.
4. **Authentication → API Key → Auth Type: Bearer.** Paste your
   `GATEWAY_API_KEY` value. (This gateway uses a plain
   `Authorization: Bearer <key>` header, not a custom header name -- select
   Bearer, not Custom, in the GPT Actions auth dropdown.)
5. Save, then test with the smoke-test prompts below inside the GPT
   builder's own test pane before publishing.

## 4. Smoke-test prompts

1. *"List the OpenSWMM tool namespaces and how many tools are in each."* →
   expects `listOpenSwmmNamespaces`.
2. *"Find the tool for changing a conduit's entrance and exit loss
   coefficient."* → expects `searchOpenSwmmTools`, should surface
   `links_set_loss_coeff`.
3. *"What arguments does links_set_loss_coeff take?"* → expects
   `getOpenSwmmToolSchema`.
4. *"What cross-section shapes does OpenSWMM support?"* → expects
   `callHydraulicsTool` with `tool_name: "xsect_list_shapes"` -- this is a
   safe, session-independent read, good for confirming the whole pipeline
   works end to end.
5. If you already have an open session on the upstream server (see
   `docs/ARCHITECTURE.md` "Known limitations" #1 for how to get one):
   *"Get the model inventory for session `<id>`."* → expects
   `getModelInventory`.

## 5. What this Custom GPT can do that the curated one can't

Everything the curated `OpenSWMM Engineer` GPT (built against the sibling
`openswmm-mcp-server` REST gateway) can do, plus direct access to the
~500 tools that gateway doesn't expose: model construction/editing
(`building_*`/`editing_*`), infrastructure/LID design, water-quality
configuration, RTC control rules, hotstart state management, and
optimization (`gym_*`). The tradeoff, per `docs/ARCHITECTURE.md`: no
built-in file upload/session management, and no automatic baseline
protection -- both need to be handled carefully by the calling GPT (see
`docs/CUSTOM_GPT_INSTRUCTIONS.md`) or by you directly.
