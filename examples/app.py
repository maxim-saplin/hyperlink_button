from __future__ import annotations

import streamlit as st

from hyperlink_button import hyperlink_button

st.set_page_config(page_title="hyperlink_button demo", layout="centered")

st.title("hyperlink_button")
st.caption("A Streamlit button that looks like a hyperlink.")


def on_clicked(msg: str) -> None:
    st.session_state["clicks"] = st.session_state.get("clicks", 0) + 1
    st.session_state["last_msg"] = msg


clicked = hyperlink_button(
    "Click me",
    help="This is a tooltip",
    icon=":material/open_in_new:",
    icon_position="left",
    type="secondary",
    on_click=on_clicked,
    args=("hello from callback",),
)

st.write("Returned from widget:", clicked)
st.write("clicks:", st.session_state.get("clicks", 0))
st.write("last_msg:", st.session_state.get("last_msg", ""))
