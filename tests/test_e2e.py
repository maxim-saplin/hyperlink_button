from __future__ import annotations

import importlib.util
import subprocess
import sys
import time
from pathlib import Path

import pytest


@pytest.mark.e2e
def test_click_increments_count() -> None:
    frontend_index = (
        Path(__file__).resolve().parents[1]
        / "src"
        / "hyperlink_button"
        / "frontend"
        / "build"
        / "index.html"
    )
    if not frontend_index.exists():
        pytest.skip(
            "Missing built frontend at src/hyperlink_button/frontend/build/index.html. "
            "Run: docker compose run --rm dev npm --prefix frontend run build"
        )

    if importlib.util.find_spec("playwright") is None:
        pytest.skip(
            "Playwright is not installed. Install e2e deps with: "
            "docker compose run --rm dev uv sync --group dev --group e2e"
        )

    from playwright.sync_api import Error as PlaywrightError
    from playwright.sync_api import sync_playwright

    example_app = Path(__file__).resolve().parents[1] / "examples" / "basic_app.py"
    streamlit_proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(example_app),
            "--server.port",
            "8502",
            "--server.address",
            "127.0.0.1",
            "--server.headless",
            "true",
            "--browser.gatherUsageStats",
            "false",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    def is_ready() -> bool:
        import urllib.error
        import urllib.request

        try:
            with urllib.request.urlopen(
                "http://127.0.0.1:8502/_stcore/health", timeout=1
            ) as resp:
                return 200 <= resp.status < 300
        except (urllib.error.URLError, TimeoutError, ValueError):
            return False

    try:
        deadline = time.time() + 30
        while time.time() < deadline and not is_ready():
            if streamlit_proc.poll() is not None:
                output = ""
                if streamlit_proc.stdout is not None:
                    try:
                        output = streamlit_proc.stdout.read() or ""
                    except Exception:
                        output = ""
                raise RuntimeError(
                    "Streamlit exited before becoming healthy. Output:\n" + output
                )
            time.sleep(0.25)

        if not is_ready():
            raise TimeoutError("Streamlit health endpoint did not become ready")

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto("http://127.0.0.1:8502", wait_until="networkidle")

                frame = page.frame_locator("iframe[title*='hyperlink_button']")
                frame.locator("button.hyperlink-button").click(timeout=10_000)

                page.get_by_text("Click count: 1", exact=False).wait_for(timeout=10_000)
                assert "Click count: 1" in page.inner_text("body")

                browser.close()
        except PlaywrightError as exc:
            msg = str(exc)
            if "Executable doesn't exist" in msg or "browserType.launch" in msg:
                pytest.skip(
                    "Playwright browsers are not installed. Run: "
                    "docker compose run --rm dev uv run playwright install --with-deps chromium"
                )
            raise
    finally:
        streamlit_proc.terminate()
        try:
            streamlit_proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            streamlit_proc.kill()
            streamlit_proc.wait(timeout=10)
