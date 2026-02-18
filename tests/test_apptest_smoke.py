from __future__ import annotations

from streamlit.testing.v1 import AppTest


def test_demo_app_renders() -> None:
    at = AppTest.from_file("examples/demo.py").run()
    # The app should render a title and at least one component iframe.
    assert at.title[0].value == "hyperlink_button"
