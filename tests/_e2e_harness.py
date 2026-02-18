from __future__ import annotations

import contextlib
import os
import socket
import subprocess
import sys
import time
import urllib.request
from collections.abc import Iterator


def _get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


@contextlib.contextmanager
def streamlit_server(app_path: str, *, startup_timeout_s: float = 30.0) -> Iterator[str]:
    port = _get_free_port()
    url = f"http://127.0.0.1:{port}"

    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        app_path,
        "--server.headless=true",
        f"--server.port={port}",
        "--server.address=127.0.0.1",
        "--browser.gatherUsageStats=false",
        "--server.runOnSave=false",
    ]
    env = os.environ.copy()

    proc = subprocess.Popen(
        cmd,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
    )

    deadline = time.time() + startup_timeout_s
    last_err: Exception | None = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=1.0) as resp:
                if int(getattr(resp, "status", 200)) == 200:
                    last_err = None
                    break
        except Exception as e:  # noqa: BLE001
            last_err = e
            time.sleep(0.2)

    if last_err is not None:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:  # noqa: BLE001
            proc.kill()
        raise RuntimeError(f"Streamlit server did not start: {last_err}")

    try:
        yield url
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except Exception:  # noqa: BLE001
            proc.kill()
