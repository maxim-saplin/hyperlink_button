from __future__ import annotations

import time

from playwright.sync_api import sync_playwright


def test_demo_click_triggers_rerun() -> None:
    # Assumes a Streamlit server is already running at :8501.
    # (The integration test harness starts it.)
    url = "http://localhost:8501"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")

        # Find the first component iframe.
        frame = None
        for f in page.frames:
            if "/component/hyperlink_button._element.hyperlink_button/" in f.url:
                frame = f
                break
        assert frame is not None

        frame.get_by_role("button", name="Click me").wait_for(
            state="visible", timeout=20_000
        )
        frame.get_by_role("button", name="Click me").click()

        # Rerun is async; give it a moment.
        page.wait_for_timeout(1500)

        text = page.locator("body").inner_text()
        # Streamlit prints dicts as JSON-ish lowercase booleans.
        assert '"clicked":true' in text.replace(" ", "").lower()

        browser.close()
