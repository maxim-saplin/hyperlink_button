import os
import subprocess
import time

import pytest
import requests


def _wait_http_ok(url: str, timeout_s: float = 30.0) -> None:
    start = time.time()
    last_err: Exception | None = None
    while time.time() - start < timeout_s:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200:
                return
        except Exception as e:  # noqa: BLE001
            last_err = e
        time.sleep(0.3)
    raise RuntimeError(f"Server did not become ready: {url} ({last_err})")


@pytest.mark.e2e
def test_click_and_disabled_behavior():
    pytest.importorskip("playwright")
    from playwright.sync_api import sync_playwright

    # If browsers aren't installed, skip with a clear hint.
    try:
        from playwright.sync_api import Error as PlaywrightError
    except Exception:  # noqa: BLE001
        PlaywrightError = Exception

    port = 8511
    env = os.environ.copy()
    env.setdefault("STREAMLIT_SERVER_HEADLESS", "true")

    proc = subprocess.Popen(
        [
            "python",
            "-m",
            "streamlit",
            "run",
            "tests/fixtures/app_for_e2e.py",
            f"--server.port={port}",
            "--server.headless=true",
            "--server.address=127.0.0.1",
        ],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    try:
        _wait_http_ok(f"http://127.0.0.1:{port}")

        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
            except PlaywrightError as e:
                msg = str(e)
                if "playwright install" in msg or "Executable doesn't exist" in msg:
                    pytest.skip(
                        "Playwright browsers not installed. Run: playwright install"
                    )
                raise
            page = browser.new_page()
            page.goto(f"http://127.0.0.1:{port}")

            # Component renders inside iframes; locate by test id from Python.
            frame1 = page.frame_locator(
                "iframe[title='hyperlink_button._component.hyperlink_button']"
            ).nth(0)
            frame2 = page.frame_locator(
                "iframe[title='hyperlink_button._component.hyperlink_button']"
            ).nth(1)

            hb = frame1.locator("[data-testid='hyperlink-button-hb1']")
            hb_button = hb.locator("button")
            hb_button.wait_for(state="visible", timeout=30000)

            # Initial state should be false.
            assert (
                page.locator("[data-testid='hb1-state']").inner_text()
                == "clicked=False"
            )

            hb_button.click()
            page.wait_for_timeout(500)
            assert (
                page.locator("[data-testid='hb1-state']").inner_text() == "clicked=True"
            )

            # Next rerun without click should reset to False.
            page.reload()
            assert (
                page.locator("[data-testid='hb1-state']").inner_text()
                == "clicked=False"
            )

            # Tooltip: title attribute should exist.
            assert hb_button.get_attribute("title") == "Tooltip text"

            # Disabled should not toggle.
            hb2 = frame2.locator("[data-testid='hyperlink-button-hb2']")
            hb2_button = hb2.locator("button")
            hb2_button.wait_for(state="visible", timeout=30000)
            assert hb2_button.is_disabled()
            hb2_button.click(force=True)
            page.wait_for_timeout(500)
            assert (
                page.locator("[data-testid='hb2-state']").inner_text()
                == "clicked=False"
            )

            browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
