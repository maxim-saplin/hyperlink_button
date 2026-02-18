import streamlit as st

from hyperlink_button import hyperlink_button


st.set_page_config(page_title="Hyperlink Button")

st.title("Hyperlink Button")
st.write("A hyperlink-like element that looks and feels like a button.")

if "clicks" not in st.session_state:
    st.session_state.clicks = 0


def handle_click() -> None:
    st.session_state.clicks += 1


clicked = hyperlink_button(
    "Check updates",
    key="updates",
    on_click=handle_click,
    help="Demonstrates click return + callback",
)

if clicked:
    st.success("hyperlink_button returned True on this run.")

st.write("Callback count:", st.session_state.clicks)
