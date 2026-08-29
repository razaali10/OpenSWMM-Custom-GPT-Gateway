FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8080

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY scripts ./scripts

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

# OPENSWMM_MCP_URL is required and has no default baked into the image --
# it must be supplied at deploy time (see .env.example). This image
# contains no openswmm.engine/openswmm_mcp code at all; it is a thin
# remote MCP client only.
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}
