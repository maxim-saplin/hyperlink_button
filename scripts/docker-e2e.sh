#!/usr/bin/env bash
set -euo pipefail

docker build -t hyperlink_button:dev .
docker build -f Dockerfile.e2e -t hyperlink_button:e2e .

docker run --rm \
  -v "$PWD:/app" -w /app \
  hyperlink_button:e2e \
  bash -lc "uv sync --dev && uv run pytest -q tests/e2e"
