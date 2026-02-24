from pathlib import Path

import pytest

AppTest = pytest.importorskip("streamlit.testing.v1").AppTest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_APP = ROOT / "examples" / "app.py"


def test_example_app_runs_without_exception():
    app = AppTest.from_file(str(EXAMPLE_APP))
    app.run(timeout=30)
    assert len(app.exception) == 0
