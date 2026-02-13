# hyperlink_button

`hyperlink_button` is a Streamlit custom component that looks like a hoverable text link, but behaves like `st.button`.

<img width="650" alt="image" src="https://github.com/user-attachments/assets/32e07e55-a575-4c6d-aa87-30da35915d11" />

## Install

From PyPI:
```
pip install hyperlink-button
```

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

## Understanding the Implementation

Ever wondered why a "simple button click" can have bugs? Or why there are multiple ways to fix them?

- **[Why Button Clicks Are Hard](WHY_BUTTON_CLICKS_ARE_HARD.md)** - Deep dive into distributed state synchronization
- **[Visual Guide](VISUAL_GUIDE.md)** - Diagrams and flowcharts explaining the architecture
- **[Diagnostic Summary](DIAGNOSTIC_SUMMARY.md)** - TL;DR of the click event issue
- **[Full Diagnostic Report](DIAGNOSTIC_REPORT.md)** - Complete technical analysis

These documents explain the fundamental challenges of building reliable UI components in distributed web applications.
