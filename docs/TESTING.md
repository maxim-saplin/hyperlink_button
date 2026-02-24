Testing strategy (minimal)

Files created in this repo:

- `tests/test_unit_component.py` - pytest unit tests that monkeypatch the component runtime and assert Python-side click behaviour and callback invocation.
- `tests/test_app_smoke.py` - a smoke test that runs `example_app.py` with `streamlit run` and ensures the process starts.
- `playwright/tests/hyperlink_e2e.spec.ts` - Playwright e2e test that spawns a Streamlit subprocess, navigates to the app, accesses the component iframe and clicks the button.

Running tests

1) Unit tests (pytest):

   - Ensure dev deps: `pip install -e .[dev]` or `pip install pytest streamlit`.
   - Run `pytest -q`.

2) Playwright e2e:

   - Install Playwright and browsers: `npm i -D @playwright/test && npx playwright install`.
   - Run `npx playwright test`.

Design notes

- Unit tests keep the Python-side logic isolated; they monkeypatch `_hyperlink_button_component` so tests don't require a running frontend.
- Smoke test ensures the example app launches under `streamlit run`.
- Playwright test interacts with the component inside the iframe using `components.html` fallback button; this provides a realistic integration test without a built JS component.
