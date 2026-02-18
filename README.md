# hyperlink_button

`hyperlink_button` is a tiny helper that behaves like `st.button` but renders like a hoverable text link.

- Same call signature as Streamlit `st.button` (Streamlit 1.54.0)
- Returns the same `bool` click value
- Scoped CSS so only this widget instance is restyled

## Install

```bash
python -m pip install hyperlink_button
```

## Usage

```python
import streamlit as st

from hyperlink_button import hyperlink_button

st.write("Normal Streamlit button:")
st.button("Normal")

st.write("Hyperlink-styled button:")
if hyperlink_button("Open details", key="open_details"):
    st.success("Clicked")
```

Run the demo app:

```bash
streamlit run examples/app.py
```

## Development (uv)

```bash
uv pip install --system -e ".[dev]"
python -m pytest
python -m playwright install --with-deps chromium
python -m pytest -m e2e
```
