from __future__ import annotations

import streamlit as st

from hyperlink_button._element import _hyperlink_button


st.write("component name", _hyperlink_button.name)
st.write("component path", _hyperlink_button.path)


# This relies on internal Streamlit runtime structures.
try:
    runtime = st.runtime.get_instance()
    registry = runtime.component_registry
    st.write("registry class", registry.__class__.__name__)
    # Best-effort attempt to introspect.
    for attr in [
        "_components",
        "_component_metadata",
        "_components_by_name",
        "_name_to_path",
    ]:
        if hasattr(registry, attr):
            st.write(attr, getattr(registry, attr))
except Exception as e:
    st.exception(e)
