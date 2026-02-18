#!/usr/bin/env bash
set -euo pipefail

docker build -t hyperlink_button:dev .
docker run --rm -p 8501:8501 -v "$PWD:/app" -w /app hyperlink_button:dev bash -lc "uv sync --dev && uv run streamlit run examples/basic_app.py --server.address=0.0.0.0 --server.port=8501"
