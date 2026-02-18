from __future__ import annotations

import streamlit as st

from hyperlink_button import hyperlink_button


st.set_page_config(page_title="hyperlink_button demo", layout="centered")

st.title("hyperlink_button")
st.caption("`hyperlink_button` behaves like `st.button` but looks like a text link.")

st.subheader("Hyperlink-styled")
clicked_link = hyperlink_button(
    "Open details",
    key="open_details",
    help="This triggers a normal Streamlit button click event.",
    icon=":material/link:",
)

st.subheader("Normal")
clicked_normal = st.button("Normal button", key="normal")

st.divider()
st.write({"hyperlink_button": clicked_link, "st.button": clicked_normal})
