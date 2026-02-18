# Publishing to PyPI (manual)

This repository is a pure-Python package that depends on Streamlit. There is no frontend build.

The commands below assume:

- You have a PyPI account and have enabled 2FA.
- You have Python 3.13+.
- You are using `uv`.

## 1) Prepare your package metadata

1. Update `pyproject.toml`:
   - `project.version`
   - `project.urls.Repository`
   - authors (optional)
2. Ensure `README.md` renders correctly on GitHub and includes basic usage.
3. Ensure `LICENSE` matches your intended license.

## 2) Run tests and build locally

From repo root:

```bash
uv pip install --system -e ".[dev]"
python -m pytest
```

Build sdist + wheel:

```bash
python -m build
```

Check distributions:

```bash
python -m twine check dist/*
```

## 3) Publish to TestPyPI first (recommended)

1. Create a TestPyPI account: https://test.pypi.org/account/register/
2. Create a token: https://test.pypi.org/manage/account/#api-tokens
3. Upload:

```bash
python -m twine upload --repository testpypi dist/*
```

When prompted:
- username: `__token__`
- password: your token (starts with `pypi-`)

4. Install from TestPyPI to verify:

```bash
python -m pip install --index-url https://test.pypi.org/simple/ --no-deps hyperlink_button
```

## 4) Publish to PyPI

1. Create a PyPI token: https://pypi.org/manage/account/#api-tokens
2. Upload:

```bash
python -m twine upload dist/*
```

## 5) Git tags and releases

Recommended:

```bash
git tag v0.1.0
git push --tags
```

## 6) Trusted Publishing (optional)

If you use GitHub Actions, you can configure Trusted Publishing so you do not need to store PyPI
tokens in GitHub secrets. See: https://docs.pypi.org/trusted-publishers/
