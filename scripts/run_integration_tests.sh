#!/usr/bin/env bash
set -euo pipefail

PORT=8501

cleanup() {
  if [[ -n "${ST_PID:-}" ]]; then
    kill "$ST_PID" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

uv run streamlit run examples/demo.py --server.port "$PORT" --server.address 0.0.0.0 --server.headless true --server.fileWatcherType none > /tmp/streamlit_test.log 2>&1 &
ST_PID=$!

for _ in $(seq 1 60); do
  if curl -fsS "http://localhost:${PORT}/_stcore/health" >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

uv run pytest -q tests/test_demo_click.py
