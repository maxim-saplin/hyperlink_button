# Hyperlink Button

Streamlit hyperlink-style button component with a Docker-only workflow.

## Docker-only quickstart

Build the image:

```bash
docker build -t hyperlink_button:dev .
```

Check toolchain versions:

```bash
docker run --rm hyperlink_button:dev bash -lc "uv --version && python --version"
```

Run the example app (defaults to `examples/basic_app.py`):

```bash
docker run --rm -p 8501:8501 -v "$PWD:/app" -w /app hyperlink_button:dev bash -lc "uv sync --dev && uv run streamlit run examples/basic_app.py --server.address=0.0.0.0 --server.port=8501"
```

Open http://localhost:8501 and click the hyperlink-style button.

## Docker-only verification commands

```bash
docker build -t hyperlink_button:dev .
docker run --rm -v "$PWD:/app" -w /app hyperlink_button:dev bash -lc "uv --version && python --version"
docker run --rm -v "$PWD:/app" -w /app hyperlink_button:dev bash -lc "uv sync --dev && uv run pytest -q --ignore=tests/e2e"
docker run --rm -p 8501:8501 -v "$PWD:/app" -w /app hyperlink_button:dev bash -lc "uv sync --dev && uv run streamlit run examples/basic_app.py --server.address=0.0.0.0 --server.port=8501"
```

## Docker-only tests

```bash
docker run --rm -v "$PWD:/app" -w /app hyperlink_button:dev bash -lc "uv sync --dev && uv run pytest -q --ignore=tests/e2e"
```

Run headless browser E2E (Playwright) in Docker:

```bash
./scripts/docker-e2e.sh
```

Note: if you mount the repo into the container (as shown above), use `uv run ...` to ensure commands execute from the project environment.

## Usage

```python
import streamlit as st
from hyperlink_button import hyperlink_button

st.title("Hyperlink Button")

if "clicks" not in st.session_state:
    st.session_state.clicks = 0

def handle_click():
    st.session_state.clicks += 1

clicked = hyperlink_button("Check updates", key="updates", on_click=handle_click)
st.write("Clicked this run:", clicked)
st.write("Total clicks:", st.session_state.clicks)
```

Links
-----

- Usage docs: `docs/usage.md`
- PyPI release manual: `docs/pypi_release_manual.md`
