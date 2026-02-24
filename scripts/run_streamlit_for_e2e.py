from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


def _wait_for_streamlit(host: str, port: int, timeout_s: float) -> None:
    url = f"http://{host}:{port}/_stcore/health"
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Streamlit app for e2e tests")
    parser.add_argument("--app", default="examples/app.py")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", default="8501")
    parser.add_argument("--ready-timeout", default="20", help="Seconds to wait for server")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    app_path = root / args.app
    if not app_path.exists():
        raise SystemExit(f"App not found: {app_path}")

    env = os.environ.copy()
    env["PYTHONPATH"] = str(root / "src")

    host = str(args.host)
    port = int(args.port)
    ready_timeout = float(args.ready_timeout)

    command = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(app_path),
        "--server.port",
        str(port),
        "--server.address",
        host,
        "--server.headless",
        "true",
        "--browser.gatherUsageStats",
        "false",
    ]

    proc = subprocess.Popen(command, env=env)
    try:
        _wait_for_streamlit(host=host, port=port, timeout_s=ready_timeout)
        return proc.wait()
    finally:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except Exception:
                proc.kill()


if __name__ == "__main__":
    raise SystemExit(main())
