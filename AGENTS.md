# Agent Guide (hyperlink_button)

Project goal: ship a publishable Python package `hyperlink_button` that provides a Streamlit custom component with the same *Python API* and *behavior* as `st.button`, but rendered like hoverable hyperlink text.

Hard constraints
- Do all installs/builds/tests/runtime checks in Docker. Avoid running project CLIs on the host.
- Use Python 3.13+ and `uv`.
- Do not pin dependency versions in `pyproject.toml` (prefer bare names like `streamlit`).
- Keep the implementation minimal; avoid scaffolding bloat.

Repository expectations (to be created)
- Python package: `hyperlink_button/` with the public API and component wrapper.
- Frontend: `frontend/` builds static assets bundled into the Python wheel/sdist.
- Tests: `tests/` with unit + integration tests; use Streamlit widget testing where possible.
- Example app: `examples/basic_app.py` demonstrating the widget.
- Docs: concise README + a publishing manual for PyPI.

Docker workflow
- Prefer `docker compose` commands. The container must mount the repo.
- If a `compose.yaml` exists, use it; otherwise create one before doing further work.

Expected commands (once Docker files exist)
- Build image: `docker compose build`
- Install deps (dev): `docker compose run --rm dev uv sync --group dev`
- Run tests: `docker compose run --rm dev uv run pytest -q`
- Build frontend (if separate): `docker compose run --rm dev <frontend build cmd>`
- Run example app: `docker compose run --rm --service-ports dev uv run streamlit run examples/basic_app.py --server.port 8501 --server.address 0.0.0.0`

Button behavior requirements
- Match `st.button` signature as closely as possible:
  `label, key=None, help=None, on_click=None, args=None, kwargs=None, type="secondary", icon=None, disabled=False, use_container_width=False`
- Return value must be `True` only on the run triggered by a click, otherwise `False`.
- `on_click` callback must be invoked on click with `args/kwargs`, like Streamlit.
- Styling must look like a standard hyperlink (hover underline, pointer cursor), while still being a true interactive widget (keyboard accessible).

When you finish a unit of work
- Report: files changed, how to run verification in Docker, and any open questions.
- Do not commit unless the user explicitly asks.
