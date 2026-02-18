#!/usr/bin/env bash
set -euo pipefail

docker build -t hyperlink_button:dev .
docker run --rm -v "$PWD:/app" -w /app hyperlink_button:dev bash -lc "uv sync --dev && uv run pytest -q --ignore=tests/e2e"
