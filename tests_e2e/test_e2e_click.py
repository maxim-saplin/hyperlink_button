from __future__ import annotations

import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest

sync_playwright = pytest.importorskip("playwright.sync_api").sync_playwright


ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.e2e
def test_click_increments_counter():
    port = 8511
    app_path = ROOT / "examples" / "app.py"
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(app_path),
            "--server.port",
            str(port),
            "--server.address",
            "localhost",
            "--server.headless",
            "true",
            "--browser.gatherUsageStats",
            "false",
        ],
        env={
            **os.environ,
            "PYTHONPATH": str(ROOT / "src"),
        },
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        _wait_for_streamlit(port=port, timeout_s=20)

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"http://localhost:{port}", wait_until="domcontentloaded")

            btn = _find_component_button_in_any_iframe(page)

            style = btn.evaluate(
                """(el) => {
                  const cs = getComputedStyle(el);
                  return {
                    backgroundColor: cs.backgroundColor,
                    borderTopStyle: cs.borderTopStyle,
                    cursor: cs.cursor,
                    textDecorationLine: cs.textDecorationLine,
                  };
                }"""
            )

            assert style["borderTopStyle"] == "none"
            assert style["cursor"] == "pointer"

            btn.hover()
            hover_style = btn.evaluate(
                """(el) => {
                  const cs = getComputedStyle(el);
                  return { textDecorationLine: cs.textDecorationLine };
                }"""
            )
            assert "underline" in str(hover_style["textDecorationLine"])

            btn.click()

            page.wait_for_selector("text=clicks:")
            page.wait_for_selector("text=1", timeout=15000)
            browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except Exception:
            proc.kill()


def _wait_for_streamlit(port: int, timeout_s: float) -> None:
    url = f"http://localhost:{port}/_stcore/health"
    deadline = time.time() + timeout_s
    last_err: Exception | None = None

    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as resp:
                if 200 <= resp.status < 300:
                    return
        except (OSError, urllib.error.URLError) as e:
            last_err = e
        time.sleep(0.2)

    msg = f"Timed out waiting for Streamlit at {url}"
    if last_err is not None:
        msg = f"{msg} (last error: {last_err})"
    raise RuntimeError(msg)


def _find_component_button_in_any_iframe(page):
    start = time.time()
    while time.time() - start < 15:
        for iframe_el in page.query_selector_all("iframe"):
            frame = iframe_el.content_frame()
            if frame is None:
                continue
            by_testid = frame.locator("[data-testid='hyperlink-button']")
            if by_testid.count() > 0:
                return by_testid.first
        time.sleep(0.2)
    raise AssertionError("Did not find hyperlink_button iframe with data-testid")
