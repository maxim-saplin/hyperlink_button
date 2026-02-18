from __future__ import annotations

import contextlib
import os
import socket
import subprocess
import time
from dataclasses import dataclass

import requests
from playwright.sync_api import expect, sync_playwright


@dataclass(frozen=True)
class StreamlitServer:
    process: subprocess.Popen[str]
    url: str


def _pick_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


def _wait_for_http(url: str, timeout_s: float = 30.0) -> None:
    deadline = time.time() + timeout_s
    last_exc: Exception | None = None
    while time.time() < deadline:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200:
                return
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
        time.sleep(0.25)
    raise RuntimeError(f"Timed out waiting for {url}: {last_exc}")


@contextlib.contextmanager
def run_streamlit_app(script_path: str) -> StreamlitServer:
    port = _pick_free_port()
    url = f"http://127.0.0.1:{port}"

    env = os.environ.copy()
    env.setdefault("BROWSER_GATHER_USAGE_STATS", "false")

    cmd = [
        "python",
        "-m",
        "streamlit",
        "run",
        script_path,
        "--server.headless=true",
        "--server.address=127.0.0.1",
        f"--server.port={port}",
        "--server.fileWatcherType=none",
    ]

    process = subprocess.Popen(
        cmd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    try:
        _wait_for_http(url)
        yield StreamlitServer(process=process, url=url)
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=10)


def test_hyperlink_button_is_link_like_and_scoped() -> None:
    with run_streamlit_app("examples/e2e_app.py") as server:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(server.url, wait_until="networkidle")

            link_btn = page.get_by_role("button", name="Link action")
            normal_btn = page.get_by_role("button", name="Normal action")
            expect(link_btn).to_be_visible()
            expect(normal_btn).to_be_visible()

            link_style = link_btn.evaluate(
                "(el) => { const s = getComputedStyle(el); return { tdl: s.textDecorationLine, bg: s.backgroundColor, br: s.borderTopStyle, pad: s.paddingTop }; }"
            )
            normal_style = normal_btn.evaluate(
                "(el) => { const s = getComputedStyle(el); return { tdl: s.textDecorationLine, bg: s.backgroundColor, br: s.borderTopStyle }; }"
            )

            assert "underline" in str(link_style["tdl"]).lower()
            assert "underline" not in str(normal_style["tdl"]).lower()
            assert str(link_style["br"]) in {"none", ""}

            page.get_by_text("link_clicks:").wait_for()
            expect(page.get_by_text("link_clicks:")).to_contain_text("0")

            link_btn.click()
            expect(page.get_by_text("link_clicked")).to_be_visible()
            expect(page.get_by_text("link_clicks:")).to_contain_text("1")

            normal_btn.click()
            expect(page.get_by_text("normal_clicked")).to_be_visible()
            expect(page.get_by_text("normal_clicks:")).to_contain_text("1")

            browser.close()
