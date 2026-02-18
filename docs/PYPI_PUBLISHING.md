# Publishing to PyPI (Step-by-step)

This guide assumes you have published packages to `pub.dev` before, but have not published to PyPI.

## What you publish

PyPI packages are built artifacts:

- `sdist` (source distribution): a `.tar.gz`
- `wheel` (built distribution): a `.whl`

For Streamlit components, the wheel must include the built frontend assets.

## One-time account setup

1. Create a PyPI account:
   - Production: https://pypi.org/account/register/
   - TestPyPI: https://test.pypi.org/account/register/
2. Enable 2FA.
3. Create an API token:
   - PyPI token page: https://pypi.org/manage/account/token/
   - TestPyPI token page: https://test.pypi.org/manage/account/token/

## Prepare the package

1. Update metadata in `pyproject.toml`:
   - `project.name`, `project.version`, `project.description`, `project.urls`, etc.
2. Build the frontend and vendor it into the Python package:

```bash
cd frontend
npm install
npm run build

cd /work
rm -rf src/hyperlink_button/frontend/dist
mkdir -p src/hyperlink_button/frontend
cp -R frontend/dist src/hyperlink_button/frontend/
```

3. Run tests:

```bash
uv run pytest
scripts/run_integration_tests.sh
```

## Build distributions

From the repo root:

```bash
uv build --sdist --wheel -o dist
```

Confirm the wheel contains the frontend:

```bash
uv run python - <<"PY"
import zipfile
z = zipfile.ZipFile("dist/hyperlink_button-0.1.0-py3-none-any.whl")
print([n for n in z.namelist() if "hyperlink_button/frontend/dist" in n])
PY
```

## Upload to TestPyPI (recommended first)

Install `twine` in a clean environment (inside the container is fine):

```bash
uv pip install twine
```

Upload:

```bash
uv run python -m twine upload --repository testpypi dist/*
```

When prompted:

- Username: `__token__`
- Password: your `pypi-...` token

## Verify installation from TestPyPI

Create a new venv and install from TestPyPI:

```bash
python -m venv /tmp/hb-venv
source /tmp/hb-venv/bin/activate

pip install --index-url https://test.pypi.org/simple/ --no-deps hyperlink-button
pip install streamlit

python -c "import hyperlink_button; print(hyperlink_button.hyperlink_button)"
```

## Upload to PyPI

Once TestPyPI looks good:

```bash
uv run python -m twine upload dist/*
```

## Versioning

- PyPI does not allow re-uploading the same version.
- If you need to fix a release: bump `project.version` and rebuild.
