# hyperlink_button

`hyperlink_button` is a Streamlit custom component that looks like a hoverable text link, but behaves like `st.button`.

## Install

From source (dev):

```bash
python -m pip install -e ".[dev]"
```

## Usage

```python
import streamlit as st
from hyperlink_button import hyperlink_button

clicked = hyperlink_button(
    "Open details",
    help="Does a normal Streamlit rerun",
    type="secondary",
)

st.write("clicked", clicked)
```

## Development

- Build frontend: `cd hyperlink_button/frontend && npm install && npm run build`
- Run demo: `streamlit run examples/demo_app.py`

Streamlit reference docs are available via the local `st_docs/` symlink.
