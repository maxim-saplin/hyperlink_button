# hyperlink-button

Streamlit widget that behaves like `st.button` but looks like a hyperlink.

Status: alpha.

## Install

```bash
pip install hyperlink-button
```

## Usage

```python
import streamlit as st
from hyperlink_button import hyperlink_button

st.title("Demo")

if hyperlink_button("Click me", key="demo"):
    st.success("Clicked!")
```

## Dev quickstart (Docker)

This repo is designed to run inside a Docker container named `dev-5`.

```bash
docker build -t hyperlink_button_dev-5 -f docker/dev-5.Dockerfile .
docker run --rm -it --name dev-5 -p 8501:8501 \
  -v "$PWD:/work" \
  -w /work \
  hyperlink_button_dev-5 bash
```

Inside the container:

```bash
uv run streamlit run examples/demo.py --server.port 8501 --server.address 0.0.0.0
```

## Tests

```bash
uv run pytest
scripts/run_integration_tests.sh
```
