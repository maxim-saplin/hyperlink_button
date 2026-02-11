import streamlit as st

from hyperlink_button import hyperlink_button


st.set_page_config(page_title="hyperlink_button e2e", layout="centered")

st.write("e2e fixture")

clicked = hyperlink_button(
    "First link",
    key="hb1",
    help="Tooltip text",
)
st.markdown(
    f"<div data-testid='hb1-state'>clicked={clicked}</div>",
    unsafe_allow_html=True,
)

clicked_disabled = hyperlink_button(
    "Disabled link",
    key="hb2",
    disabled=True,
)
st.markdown(
    f"<div data-testid='hb2-state'>clicked={clicked_disabled}</div>",
    unsafe_allow_html=True,
)
