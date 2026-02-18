hyperlink_button usage
======================

This document explains the public API, behavior, and limitations of `hyperlink_button()` - a Streamlit-compatible widget inspired by `st.button` but which renders as a hyperlink-styled button.

API
---

`hyperlink_button` matches the `st.button` signature for the Streamlit version in this repo.

For Streamlit 1.54.0 (current Docker image), the signature is:

`hyperlink_button(label, key=None, help=None, on_click=None, args=None, kwargs=None, *, type='secondary', icon=None, icon_position='left', disabled=False, use_container_width=None, width='content', shortcut=None) -> bool`

- Return value: `True` on the run where the widget was activated (clicked), else `False`.

Behavior and parity with `st.button`
-----------------------------------

- `hyperlink_button` aims for API parity with `st.button`'s synchronous behavior: it returns a boolean that is `True` only on the run when the user activates the widget.
- `key` stability: provide a `key` to ensure consistent behavior across reruns.
- Rerun model: interactions trigger Streamlit reruns. Use the return value to drive app logic like `if hyperlink_button("Go"):`.

Styling approach
----------------

- The widget is implemented by calling `st.button(...)` and then restyling that specific rendered button to look like a hyperlink.
- Scoping is done with a per-call marker element plus a targeted CSS selector, so other Streamlit buttons in the app are not affected.

Limitations and browser support
-------------------------------

- CSS features: the implementation may use modern selectors for scoping. In particular, `:has()` is convenient but not universally supported (not supported in some older browsers). The widget does not rely critically on `:has()` for essential functionality; when `:has()` is unavailable styles may be slightly different but widget remains usable.
- Accessibility: the widget attempts to follow accessible patterns (role, ARIA where applicable) but may not match native `st.button` in every assistive context. Test with your target screen readers.
- Cross-origin resource restrictions: the widget does not perform remote navigation by default. If you provide `href`-like behavior via callbacks, validate the target URLs.
- Server-side callbacks: the library matches Streamlit's rerun model and does not provide client-only callback hooks.

Examples
--------

Minimal usage:

```py
import streamlit as st
from hyperlink_button import hyperlink_button

if "clicks" not in st.session_state:
    st.session_state.clicks = 0

def bump():
    st.session_state.clicks += 1

clicked = hyperlink_button("Check updates", key="updates", on_click=bump)
st.write("Clicked this run:", clicked)
st.write("Total clicks:", st.session_state.clicks)
```

Troubleshooting notes
---------------------

- If the control doesn't appear styled as expected, verify that host CSS or themes aren't overriding the widget's rules. Adding a stronger selector or inline style via `style` can help.
- If interactions don't trigger reruns, ensure the Streamlit app isn't intercepting events in custom components or theme code.

Handoff
-------

Changed paths:
- `docs/usage.md`

Why:
- Provide user-facing documentation for the widget API, styling, and limitations.

Verification performed:
- Documentation-only; no runtime checks performed.
