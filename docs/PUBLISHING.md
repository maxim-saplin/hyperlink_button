# Publishing to PyPI

This guide assumes you are using Docker for all builds/tests and `uv` for tooling.

## 1. Update metadata

- Bump the version in `pyproject.toml`.
- Update `README.md` if needed.

## 2. Run tests in Docker

- `docker compose run --rm dev uv sync --group dev`
- `docker compose run --rm dev uv run pytest -q`

If you want to include the minimal headless browser verification:

- `docker compose run --rm dev npm --prefix frontend install`
- `docker compose run --rm dev npm --prefix frontend run build`
- `docker compose run --rm dev uv sync --group dev --group e2e`
- `docker compose run --rm dev uv run playwright install --with-deps chromium`
- `docker compose run --rm dev uv run pytest -q -m e2e`

## 3. Build distributions

If using `uv`:

- `docker compose run --rm dev uv build`

If you prefer `build`:

- `docker compose run --rm dev uv run python -m build`

Artifacts should appear in `dist/`.

## 4. Verify packages

- `docker compose run --rm dev uv run twine check dist/*`

## 5. Upload to TestPyPI (recommended)

- Create an API token at https://test.pypi.org/manage/account/token/
- Upload:
  - `docker compose run --rm -e TWINE_USERNAME=__token__ -e TWINE_PASSWORD=YOUR_TOKEN dev uv run twine upload --repository testpypi dist/*`

## 6. Upload to PyPI

- Create an API token at https://pypi.org/manage/account/token/
- Upload:
  - `docker compose run --rm -e TWINE_USERNAME=__token__ -e TWINE_PASSWORD=YOUR_TOKEN dev uv run twine upload dist/*`

## 7. Tag the release (optional)

- Create a git tag matching the version (e.g., `v0.1.0`) and push it.

## Notes

- Do not pin dependency versions in `pyproject.toml`.
- Ensure `frontend/build` is included in the sdist/wheel before publishing.
