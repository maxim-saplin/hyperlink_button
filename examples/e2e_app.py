import streamlit as st

from hyperlink_button import hyperlink_button


st.set_page_config(page_title="Hyperlink Button E2E")

st.title("Hyperlink Button E2E")

if "link_clicks" not in st.session_state:
    st.session_state.link_clicks = 0
if "normal_clicks" not in st.session_state:
    st.session_state.normal_clicks = 0


def bump_link() -> None:
    st.session_state.link_clicks += 1


def bump_normal() -> None:
    st.session_state.normal_clicks += 1


clicked_link = hyperlink_button(
    "Link action",
    key="link_action",
    on_click=bump_link,
    help="E2E link-styled control",
)

if clicked_link:
    st.success("link_clicked")

clicked_normal = st.button(
    "Normal action",
    key="normal_action",
    on_click=bump_normal,
)

if clicked_normal:
    st.success("normal_clicked")

st.markdown(f"link_clicks: `{st.session_state.link_clicks}`")
st.markdown(f"normal_clicks: `{st.session_state.normal_clicks}`")
