# AGENTS.md

This repo is building `hyperlink_button`: a Streamlit custom element that matches Streamlit’s stock `st.button` API/behavior, but renders/feels like a typical hoverable text link (NOT Streamlit’s existing `link_button`).

## Non-negotiables (Constraints)
- Docker-only: ALL work (installs, builds, tests, running Streamlit) happens inside a Docker container with this repo mounted in. Do not run project CLIs on the host except Docker commands needed to build/run the container.
- Delegate-first: prefer doing work via subagents; avoid solo implementation unless it’s a tiny fix not worth delegating.
- Python: target `>=3.13`.
- Dependency policy: use `uv` and “latest by default” deps; do not pin versions in `pyproject.toml` unless there is a concrete compatibility reason.
- Verification is required: unit + integration tests; use Streamlit widget testing; use headless browsing to verify what Streamlit renders.

## Repo resources
- `st_docs/` is a symlink to a local checkout of Streamlit docs. Treat it as READ-ONLY research material. Do not modify, vendor, or commit docs content.

## Expected deliverables (Project-level)
- A publishable PyPI package (metadata, build, distribution ready).
- Automated tests covering behavior and rendering expectations.
- A simple example/test app users can run to validate the control.
- Exhaustive “how to publish to PyPI” manual aimed at someone new to PyPI (but experienced with pub.dev).

## Docker workflow (How you must run things)
- All commands must be runnable via Docker (e.g., `docker compose run --rm ...` or `docker run --rm ...`).
- If you propose a command, write it in Docker form and note the container working directory.
- If Docker files don’t exist yet, your task may include creating them, but keep images lean and reproducible.

## Python + uv workflow (Inside container)
- Use `uv` for env + installs + running tools.
- Prefer patterns like:
  - `uv sync` (if lock/pyproject exists)
  - `uv add <pkg>` (add dependencies; avoid version pins)
  - `uv run pytest -q`
- Set `requires-python = ">=3.13"` when creating packaging metadata.

## Testing requirements
- Unit tests: fast, deterministic.
- Integration tests: exercise Streamlit behavior end-to-end as needed.
- Streamlit widget testing: use Streamlit’s official widget testing utilities where applicable.
- Headless rendering check: use a headless browser (e.g., Playwright) inside Docker to confirm DOM/behavior.

## Subagent operating rules
- Be concise and fight bloat. Prefer the simplest working approach.
- Make changes only within your assigned scope; don’t refactor unrelated areas.
- Don’t introduce secrets or commit sensitive files (e.g., `.env`, `.pypirc`).
- Don’t run destructive git commands.

## What to return (Required format)
When you finish a task, report:
- Files changed (explicit list of paths)
- Commands run (Docker form)
- Test evidence (what ran, pass/fail, key output lines)
- Notes/risks (only if actionable)

## Delegation/model guidance
- Use higher-intelligence coding models for implementation-heavy tasks (e.g., azure/gpt-5.2-codex / azure/gpt-5.2).
- Use cheaper models for scanning docs or quick repo surveys (e.g., azure/gpt-5-mini / azure/gpt-5-nano).
- If you need follow-up iterations, prefer resumable sessions (opencode-subagent); for one-off Q&A, use a single task agent.
