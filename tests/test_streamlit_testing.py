from __future__ import annotations

from streamlit.testing.v1 import AppTest


def test_click_runs_callback() -> None:
    at = AppTest.from_string(
        """
import streamlit as st
from hyperlink_button import hyperlink_button

if "count" not in st.session_state:
    st.session_state.count = 0

def inc():
    st.session_state.count += 1

hyperlink_button("Hyperlink Button", key="hl", on_click=inc)
st.text(f"count={st.session_state.count}")
"""
    ).run()

    assert at.text[0].value == "count=0"
    at.button[0].click().run()
    assert at.text[0].value == "count=1"
