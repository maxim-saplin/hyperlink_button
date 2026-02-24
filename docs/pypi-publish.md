PyPI publishing guide

This checklist builds and publishes `hyperlink-button` to TestPyPI and PyPI.
It assumes you already have a working Python environment and are familiar with packaging basics.

Prerequisites

- Accounts: TestPyPI + PyPI
- API tokens for both indexes
- Tools installed in this repo: `uv sync --group dev`

One-time setup (tokens)

1) Create API tokens

- TestPyPI: https://test.pypi.org/manage/account/token/
- PyPI: https://pypi.org/manage/account/token/

2) Export them as environment variables

Recommended (avoids shell history leaks):

```bash
export TWINE_USERNAME="__token__"
export TWINE_PASSWORD_TESTPYPI="pypi-..."
export TWINE_PASSWORD_PYPI="pypi-..."
```

Release steps

1) Ensure frontend assets are built

The published package must include `src/hyperlink_button/frontend/build/`.

```bash
cd src/hyperlink_button/frontend
npm install
npm run build
cd -
```

2) Bump version

Edit `[project].version` in `pyproject.toml`.

3) Build artifacts

```bash
rm -rf dist/
uv run python -m build
```

4) Validate artifacts

```bash
uv run python -m twine check dist/*
```

5) Upload to TestPyPI

```bash
TWINE_USERNAME="__token__" \
TWINE_PASSWORD="$TWINE_PASSWORD_TESTPYPI" \
uv run python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

6) Install from TestPyPI and smoke test

Use a clean virtualenv if possible:

```bash
pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple \
  hyperlink-button==<VERSION>
```

7) Upload to PyPI

```bash
TWINE_USERNAME="__token__" \
TWINE_PASSWORD="$TWINE_PASSWORD_PYPI" \
uv run python -m twine upload dist/*
```

Notes

- If you get 403 errors, verify you used the correct token for the index (TestPyPI vs PyPI).
- Keep `dist/` uncommitted.
