from __future__ import annotations

from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

from tests._e2e_harness import streamlit_server


@pytest.mark.e2e
def test_hyperlink_button_is_link_like_and_scoped() -> None:
    app_path = str(Path(__file__).with_name("e2e_app.py"))
    with streamlit_server(app_path) as url:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")

            link_btn = page.get_by_role("button", name="Hyperlink Button")
            normal_btn = page.get_by_role("button", name="Normal Button")

            assert link_btn.is_visible()
            assert normal_btn.is_visible()

            # Link-like assertions.
            link_padding_left = link_btn.evaluate("el => window.getComputedStyle(el).paddingLeft")
            assert link_padding_left == "0px"

            link_border_top = link_btn.evaluate("el => window.getComputedStyle(el).borderTopWidth")
            assert link_border_top in ("0px", "0")

            link_bg = link_btn.evaluate("el => window.getComputedStyle(el).backgroundColor")
            assert link_bg in ("rgba(0, 0, 0, 0)", "transparent")

            link_btn.hover()
            link_dec = link_btn.evaluate("el => window.getComputedStyle(el).textDecorationLine")
            assert "underline" in link_dec

            # Scoping assertions: normal button must not be link-styled.
            normal_padding_left = normal_btn.evaluate(
                "el => window.getComputedStyle(el).paddingLeft"
            )
            assert normal_padding_left != "0px"

            normal_btn.hover()
            normal_dec = normal_btn.evaluate("el => window.getComputedStyle(el).textDecorationLine")
            assert "underline" not in normal_dec

            browser.close()
