# Publishing to PyPI: hyperlink_button

This is a step-by-step manual for publishing `hyperlink_button` to PyPI. It assumes you have never published to PyPI, but you have shipped packages to pub.dev.

## What you're publishing

`hyperlink_button` is a Python package that includes built frontend assets under `hyperlink_button/frontend/build/`.

You must build the frontend before building wheels, otherwise the wheel will not contain the compiled JS/CSS and the component will not render.

## Prerequisites

- Python 3.13+
- A PyPI account on `pypi.org` and (recommended) 2FA enabled
- A TestPyPI account on `test.pypi.org`
- CLI tooling (install into a clean venv):

```bash
python -m pip install --upgrade pip
python -m pip install --upgrade build twine
```

Note on `uv`: you can use `uv` to create/run environments. This manual uses portable `python -m ...` commands for the build/publish steps.

## Step 1: Build the frontend assets

```bash
cd hyperlink_button/frontend
npm install
npm run build
```

Confirm the output exists:

```bash
ls -la build
```

## Step 2: Build the Python distributions

From the repo root:

```bash
python -m build
```

You should now have artifacts in `dist/`:

- `hyperlink_button-<version>-py3-none-any.whl`
- `hyperlink_button-<version>.tar.gz`

Validate metadata:

```bash
python -m twine check dist/*
```

## Step 3: Upload to TestPyPI (recommended)

Create a TestPyPI API token. Then upload using environment variables:

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD="<TESTPYPI_TOKEN>"
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Install from TestPyPI to verify:

```bash
python -m pip install --index-url https://test.pypi.org/simple/ --no-deps hyperlink_button==<version>
python -c "import hyperlink_button; print(hyperlink_button)"
```

Run the demo app:

```bash
streamlit run examples/demo_app.py
```

## Step 4: Upload to production PyPI

Create a PyPI API token (project-scoped is preferred).

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD="<PYPI_TOKEN>"
python -m twine upload dist/*
```

## Step 5: Post-publish verification

```bash
python -m pip install --upgrade hyperlink_button
python -c "import hyperlink_button; print('ok')"
streamlit run examples/demo_app.py
```

## Release checklist

- Bump `version` in `pyproject.toml`
- Build frontend (`npm run build`)
- `python -m build`
- `python -m twine check dist/*`
- Upload to TestPyPI and verify install
- Upload to PyPI

## Troubleshooting

- `HTTPError: 403` during upload: you likely used the wrong token or wrong username. Username must be `__token__`.
- `File already exists`: bump the version and rebuild. PyPI will not accept re-upload of the same version.
- Component renders blank after install: verify frontend assets are in the wheel:

```bash
python -c "import zipfile, glob; p=glob.glob('dist/*.whl')[0]; z=zipfile.ZipFile(p); print([n for n in z.namelist() if 'frontend/build' in n][:20])"
```
