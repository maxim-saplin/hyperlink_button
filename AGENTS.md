# Agent Coordination Guide

This repo is being built to satisfy `GOAL.md`.

Core constraints (non-negotiable)
- Docker-only execution for all runtime checks, tests, builds.
- Use `uv` and Python 3.13 inside the container.
- Prefer latest dependency versions; do not manually pin versions (use `uv add`).
- Use `st_docs/` as the canonical Streamlit API reference for behavior parity.

Orchestrator policy (bounded authority)
- Orchestrator edits are limited to governance docs and mechanical integration glue.
- All implementation work must be done by subagents using real patches (`apply_patch`).

Shared/locked files
- Only one active work order may modify any of these at a time:
  - `pyproject.toml`
  - lockfiles (`uv.lock`, etc.)
  - `Dockerfile*`
  - `docker-compose.yml` (if introduced)
  - `AGENTS.md`

Work-order format (required)
- Objective: one sentence.
- Allowed paths: explicit allowlist.
- Forbidden paths: explicit denylist.
- Acceptance criteria: observable outcomes.
- Docker-only verification commands: exact commands to run.
- Model: `azure/gpt-5-mini` by default; escalate to `azure/gpt-5.2-codex` only for hard integration/debugging.

Handoff packet (required from subagents)
- Changed paths (list).
- Why: purpose of the change (no code dump).
- Verification performed: commands + where logs/artifacts live.
- Known limitations + follow-ups.

Quality bar
- Match `st.button` API and behavior (callback semantics, return value, rerun behavior, disabled behavior, key stability).
- Include unit + integration tests.
- Include Streamlit widget testing where applicable.
- Include headless browser verification of the rendered output.
- Provide a minimal example app.
- Provide documentation and an exhaustive PyPI release manual.
