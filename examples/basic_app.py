import streamlit as st

from hyperlink_button import button

st.title("Hyperlink Button Demo")
st.write(
    "This component mirrors st.button but renders like a link once frontend exists."
)

if "click_count" not in st.session_state:
    st.session_state["click_count"] = 0

clicked = button("Open details")
if clicked:
    st.session_state["click_count"] += 1

st.write(f"Click count: {st.session_state['click_count']}")
