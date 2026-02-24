hyperlink-button

A minimal Streamlit component that behaves like `st.button` but looks like hoverable hyperlink text.

Install

```bash
pip install hyperlink-button
```

Usage

```python
import streamlit as st

from hyperlink_button import hyperlink_button


st.title("Demo")

if hyperlink_button("Click me", icon=":material/open_in_new:"):
    st.write("Clicked!")
else:
    st.write("Not clicked")
```

Run the example app

```bash
uv sync --group dev
uv run streamlit run examples/app.py
```

Frontend development (Streamlit Components v1)

The Python wrapper prefers the bundled build at `src/hyperlink_button/frontend/build/` when it exists.
To use the Vite dev server (hot reload), temporarily move that directory away.

Terminal A (frontend):

```bash
cd src/hyperlink_button/frontend
npm install
npm run dev
```

Terminal B (python + Streamlit):

```bash
mv src/hyperlink_button/frontend/build src/hyperlink_button/frontend/build.bak
uv run streamlit run examples/app.py
```

Rebuild the bundled assets:

```bash
rm -rf src/hyperlink_button/frontend/build
cd src/hyperlink_button/frontend
npm run build
```

Tests

```bash
uv run pytest
```

E2E (Playwright)

```bash
uv run python -m playwright install
uv run pytest -q -m e2e tests_e2e
```

Build

```bash
uv run python -m build
```

Publishing

See `docs/pypi-publish.md`.
