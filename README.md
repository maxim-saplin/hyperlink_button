# hyperlink_button

Streamlit custom component that mirrors `st.button` behavior but renders like a hyperlink.

## Install

```bash
pip install hyperlink_button
```

## Usage

```python
import streamlit as st
from hyperlink_button import button

clicked = button("Open details")
st.write(clicked)
```

## Development

- Install dev deps: `docker compose run --rm dev uv sync --group dev`
- Tests: `docker compose run --rm dev uv run pytest -q`
- Example app: `docker compose run --rm --service-ports dev uv run streamlit run examples/basic_app.py --server.port 8501 --server.address 0.0.0.0`

- Build frontend:
  - `docker compose run --rm dev npm --prefix frontend install`
  - `docker compose run --rm dev npm --prefix frontend run build`

- E2E (Playwright):
  - `docker compose run --rm dev uv sync --group dev --group e2e`
  - `docker compose run --rm dev uv run playwright install --with-deps chromium`
  - `docker compose run --rm dev uv run pytest -q -m e2e`
