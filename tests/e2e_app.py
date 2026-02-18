from __future__ import annotations

import streamlit as st

from hyperlink_button import hyperlink_button


st.set_page_config(page_title="e2e", layout="centered")

st.write("E2E style checks")

hyperlink_button("Hyperlink Button", key="hlb_e2e")
st.button("Normal Button", key="normal_e2e")
