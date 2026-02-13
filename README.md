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

## Why Not Just Use Streamlit's Built-in Button?

**Streamlit's standard button (`st.button`)** uses Streamlit's built-in widget system:
- **Native widget**: Registered in Streamlit's core widget registry with `register_widget()`
- **Protobuf messages**: Communicates via `ButtonProto` protobuf messages to the frontend
- **Trigger-based state**: Uses `value_type="trigger_value"` - returns True only on the script run where clicked
- **No iframe**: Rendered directly in Streamlit's main React app, not in a separate iframe

**Custom components (like `hyperlink_button`)** are different:
- **Separate iframe**: Each component runs in its own isolated iframe with its own React context
- **Counter-based state**: Uses incrementing counter to detect clicks (subject to iframe remount issues)
- **Custom styling**: Can implement completely custom appearance (like hyperlink style)
- **Trade-off**: More flexibility but complexity in state synchronization across iframe boundary

**Why use custom component approach?**
- Streamlit's built-in widgets have fixed styling and behavior
- Cannot make a built-in button look like a plain text hyperlink
- Custom components allow full control over appearance while maintaining button functionality

The iframe remount bug exists because custom components must synchronize state across the iframe boundary, while built-in widgets don't have this issue.

## Solutions to the Iframe Remount Bug

Three solutions have been identified and analyzed. See **[SOLUTIONS.md](SOLUTIONS.md)** for detailed comparison:

1. **Detect & Reset** (Quick fix, 10 min) - Detect when counter resets and fix it reactively
2. **Use Timestamps** (Robust, 1 hour) - Replace counter with timestamps that never decrease  
3. **Sync Counter** (Perfect, 3 hours) - Persist counter in session state and restore on mount

Each solution has different trade-offs in complexity, robustness, and implementation time. The solutions document provides detailed code examples, pros/cons, and a decision guide.
