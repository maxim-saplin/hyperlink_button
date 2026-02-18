# Testing strategy and runbook

This document defines a testing strategy for unit, Streamlit widget (AppTest), and headless browser (end‑to‑end) verification for this repository. All runtime/test execution must be performed inside Docker containers (Docker‑only constraint).

Goals
- Provide clear categories of tests to add and maintain.
- Show how to test Streamlit widgets using `streamlit.testing.v1.AppTest`.
- Recommend a headless browser tool and show how to integrate it in Docker (Playwright recommended).
- Provide exact Docker commands to run each test suite.

1) Test categories (what to write)

- Unit tests
  - Focus: pure Python logic, small utility functions, data transformation, and any non‑Streamlit business logic.
  - Framework: `pytest`.<
  - Location convention: `tests/unit/` (not created here per work‑order rules). Keep tests small (<100ms ideally) and deterministic.

- Integration tests (component level)
  - Focus: functions that interact with simple external pieces (local files, small fixtures) or pieces of the Streamlit layer that can be exercised without a full browser (for example, functions that prepare widget state or layout helpers).
  - Framework: `pytest` with fixtures; use Docker to provide any required dependencies.

- Streamlit widget tests (widget behavior)
  - Focus: widget semantics (return values, callback invocation, disabled states, rerun behavior, key stability).
  - Tool: `streamlit.testing.v1.AppTest` (Streamlit's programmatic app tester).
  - Location convention: `tests/widgets/`.

- End‑to‑end headless browser tests (UI verification)
  - Focus: rendered UI, visual regression, event sequences that depend on browser semantics (focus, click ordering), and end‑to‑end behavior across JS + Python boundaries.
  - Tool: Playwright (recommended) or Puppeteer as alternative; Playwright preferred for its Docker support and multi‑browser capability.
  - Location convention: `tests/e2e/`.

2) Streamlit widget testing with streamlit.testing.v1.AppTest

Overview
- `AppTest` runs a Streamlit script in a test harness and allows you to introspect widget states and emulate user events programmatically without a real browser. Use it for widget semantics and callback behavior that don't require full browser rendering.

Basic pattern

```python
from streamlit.testing.v1 import AppTest

def test_widget_behavior(tmp_path):
    script = tmp_path / "app.py"
    script.write_text("""
import streamlit as st
val = st.number_input('n', value=1)
st.write(val * 2)
""")

    with AppTest(str(script)) as app:
        # find the input widget and set value
        input_widget = app.get_widget("number_input")
        input_widget.set_value(3)

        # run until the script reaches a stable state
        app.wait_for_finished()

        # assert on produced output (snapshotting or direct value checks)
        assert "6" in app.get_text()

```

Notes and recommendations
- Use `app.wait_for_finished()` after changing widget values.
- Prefer querying widgets by label or by the widget id returned by AppTest helpers; be explicit about keys when creating widgets to ensure stability across runs.
- Test rerun/callback behavior by simulating a sequence of widget changes and asserting side effects (files written, database calls mocked, etc.).
- Keep AppTest tests fast; they are lighter than full browser e2e but heavier than pure unit tests.

3) Headless browser verification — Playwright

Why Playwright
- Robust multi‑browser support (Chromium, WebKit, Firefox).
- Good Docker images and CI examples; stable API for UI flows and screenshots.

Test structure
- Use Playwright's Python bindings (`playwright` package) or the Playwright CLI. Store tests in `tests/e2e/playwright/`.
- Typical test steps:
  1. Start the Streamlit app inside the test Docker container (bind to 0.0.0.0, explicit port). Use `--server.port` and `--server.headless true` if needed.
  2. Wait for the app to serve (poll the health URL or capture stdout lines that show the URL).
  3. Launch Playwright browser in headless mode and navigate to the app URL.
  4. Interact (clicks, typing, form submission), assert on visible text, DOM elements, or screenshots.

Example Playwright snippet (Python)

```python
from playwright.sync_api import sync_playwright

def test_basic_ui(live_server_url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(live_server_url)
        page.click("text=Click me")
        assert page.locator("#result").inner_text() == "expected"
        browser.close()

```

Docker considerations
- Use Playwright's official Docker images or install the browsers in your test image. Official base: `mcr.microsoft.com/playwright/python` (or `mcr.microsoft.com/playwright` for node).
- Ensure required OS packages (libnss, libatk, fonts) are present if you build your own image.
- Run Playwright tests in headless mode in CI; for local debugging you can run with `headful` mode but still inside Docker.

4) Test data, fixtures, and mocking

- Mock external calls (network, cloud APIs) in unit and widget tests using `responses`, `pytest-mock`, or `unittest.mock`.
- For E2E tests, prefer local fixtures or a test container of dependent services; avoid hitting production services.

5) Exact Docker commands to run each suite

Notes: these commands assume your project provides a test image or that you will run tests inside a development image that includes Python 3.13, `uv`, Streamlit, Playwright and test dependencies. Adjust image name `hyperlink_button-test` to your CI image name.

- Unit tests (pytest):

```bash
# Build test image (if you have a Dockerfile.test or a test target)
docker build -f Dockerfile -t hyperlink_button-test .

# Run pytest unit tests only
docker run --rm \
  -v "$PWD":/app -w /app \
  -e PYTHONPATH=/app \
  hyperlink_button-test \
  bash -lc "pytest -q tests/unit"
```

- Streamlit widget tests (AppTest):

```bash
docker run --rm \
  -v "$PWD":/app -w /app \
  -e PYTHONPATH=/app \
  hyperlink_button-test \
  bash -lc "pytest -q tests/widgets"
```

- Playwright E2E (headless browser) — single container run

```bash
# Start Streamlit app in background inside the container and run Playwright tests in same container.
docker run --rm \
  -v "$PWD":/app -w /app \
  -e PYTHONPATH=/app \
  -p 8501:8501 \
  hyperlink_button-test \
  bash -lc "streamlit run examples/e2e_app.py --server.port 8501 & sleep 2 && pytest -q tests/e2e"
```

Notes on the command above:
- The app start command should point at a minimal example app that exposes the UI you want to test (e.g. `examples/e2e_app.py`). If your repo uses a different path, update it accordingly.
- The `sleep 2` is a simple synchronization; prefer a healthcheck loop that polls `http://127.0.0.1:8501` until available for robustness.

- Playwright E2E (preferred CI pattern — two containers)

```bash
# 1) Start the app container (detached)
docker run -d --name app-under-test -v "$PWD":/app -w /app -p 8501:8501 hyperlink_button-test \
  bash -lc "streamlit run examples/e2e_app.py --server.port 8501"

# 2) Run Playwright tests from a test runner container that can reach the app
docker run --rm --network host -v "$PWD":/app -w /app hyperlink_button-test \
  bash -lc "pytest -q tests/e2e"

# 3) Teardown
docker rm -f app-under-test
```

6) CI integration notes

- Keep tests small and split into fast (unit) and slow (e2e) buckets; run fast tests on every push and run E2E on merge/main or nightly.
- Cache Docker layers for dependencies to speed up CI.
- Use Playwright's `--shard` options or pytest-xdist to parallelize E2E where possible.

7) Verification commands (documentation only)

- Run all tests (unit + widgets + e2e) in one container (simple):

```bash
docker run --rm -v "$PWD":/app -w /app -p 8501:8501 hyperlink_button-test \
  bash -lc "streamlit run examples/e2e_app.py --server.port 8501 & sleep 2 && pytest -q"
```

- Run only widget tests:

```bash
docker run --rm -v "$PWD":/app -w /app hyperlink_button-test bash -lc "pytest -q tests/widgets"
```

- Run Playwright tests locally (debug headful):

```bash
docker run --rm -it -v "$PWD":/app -w /app -p 8501:8501 --cap-add=SYS_ADMIN hyperlink_button-test \
  bash -lc "streamlit run examples/e2e_app.py --server.port 8501 & sleep 2 && pytest tests/e2e -k playwright -s"
```

8) Recommended next steps for implementers

1. Add `tests/unit/`, `tests/widgets/`, `tests/e2e/` skeletons and example tests that follow the patterns above.
2. Create a small `examples/e2e_app.py` that exposes the widget flows the E2E tests will exercise.
3. Build a Docker test image that includes Python 3.13, `uv`, Streamlit, Playwright browsers, and test dependencies. Prefer installing browsers via Playwright's install step (e.g. `playwright install --with-deps` or use Playwright official image).
4. Add CI jobs: fast (unit + widgets) and slow (playwright e2e).

Contact/Notes
- This plan follows the repo constraint to run tests only inside Docker and uses `streamlit.testing.v1.AppTest` for widget semantics plus Playwright for robust headless browser verification.
