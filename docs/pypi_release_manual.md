PyPI Release Manual
===================

This manual describes a Docker-first, reproducible process to build, test, and publish the `hyperlink_button` package to TestPyPI and PyPI. It assumes repository root contains a Dockerfile that can build the package and run checks. All commands shown run inside a container unless noted.

1. Versioning strategy
----------------------

- Use semantic versioning: `MAJOR.MINOR.PATCH` (e.g. `1.2.3`).
- For pre-releases use hyphenated identifiers: `1.3.0-alpha.1`, `1.3.0rc1`.
- Increment rules:
  - MAJOR for incompatible API changes.
  - MINOR for backwards-compatible feature additions.
  - PATCH for bugfixes.
- Update the version in the canonical place used by the project (do not change lockfiles or Dockerfile). If the project uses a single source of truth file (package __init__ or similar) update that file and the changelog.

2. Prepare a release branch and changelog
----------------------------------------

- Create a release branch: `git checkout -b release/vX.Y.Z`.
- Update the version and add a concise changelog entry summarizing user-facing changes.
- Commit only documentation and version changes in this branch.

3. Build in Docker
------------------

Purpose: make builds reproducible and identical to CI/local release steps.

Suggested Docker build workflow (examples):

```
# Build a release-capable container (replace Dockerfile name if custom)
docker build -t hyperlink-button-release .

# Run the build inside the container.
# This repo uses `uv`, which can build wheels/sdists without installing extra tooling.
docker run --rm -v "$(pwd):/work" -w /work hyperlink-button-release \
  /bin/sh -c "uv build --sdist --wheel --out-dir dist"
```

Notes:
- The container must contain Python 3.13 and `uv`. If the repo provides helper scripts, prefer them.
- Output artifacts will be in `dist/` on the host due to the volume mount.

4. Smoke test in Docker
-----------------------

Before publishing, verify the built wheels install and import in a clean runtime.

```
# Create a temporary container with matching runtime (Python 3.13 + minimal deps)
docker run --rm -v "$(pwd)/dist:/dist" python:3.13-slim /bin/sh -c "\
  pip install --upgrade pip setuptools wheel && \
  pip install /dist/hyperlink_button-*.whl && \
  python -c \"import hyperlink_button; print('OK', hyperlink_button)\""
```

If the import prints `OK` and exits zero, the package is likely sane.

5. Publishing to TestPyPI then PyPI
----------------------------------

Create API tokens in TestPyPI and PyPI (recommended). Use env vars to pass tokens to the container; do NOT commit tokens.

Example publish steps (inside a container):

```
export TWINE_USERNAME=__token__
export TWINE_PASSWORD="$TEST_PYPI_API_TOKEN"

# Upload to TestPyPI
docker run --rm -v "$(pwd):/work" -w /work hyperlink-button-release \
  /bin/sh -c "pip install --upgrade twine && twine upload --repository testpypi dist/*"

# Run a quick install test from TestPyPI in a fresh container
docker run --rm python:3.13-slim /bin/sh -c "pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple hyperlink_button && python -c 'import hyperlink_button; print("imported")'"

# If everything looks good, publish to PyPI
export TWINE_PASSWORD="$PYPI_API_TOKEN"
docker run --rm -v "$(pwd):/work" -w /work hyperlink-button-release \
  /bin/sh -c "pip install --upgrade twine && twine upload dist/*"
```

Notes:
- Use `--repository-url` or `--repository` flags with `twine` if you prefer explicit URLs.
- Consider using `twine check dist/*` before upload to validate metadata.

6. Tagging and release notes
----------------------------

- Create a git tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`.
- Push tag: `git push origin vX.Y.Z`.
- Create a GitHub/GitLab release using the tag and paste your changelog/release notes.
- Release notes should include: highlights, migration notes (if any), and link to docs.

7. How to verify install
------------------------

After publishing to PyPI, verify installation in a clean container:

```
docker run --rm python:3.13-slim /bin/sh -c "pip install hyperlink_button && python -c 'import hyperlink_button; print(hyperlink_button.__version__)'"
```

Also verify your example app or a minimal script that imports and exercises the public API.

8. Troubleshooting
------------------

- Build fails with missing files: ensure `pyproject.toml` includes all package data and `MANIFEST.in` if used.
- Installation fails with binary compatibility errors: check Python version and wheel tags; build wheels for all supported platforms or publish sdist.
- Twine upload rejected: ensure the version is unique on PyPI (can't reuse versions). For collisions, increment the version.
- Tokens not working: ensure token permissions and that you used `__token__` as username.
- Metadata lint errors: run `twine check dist/*` and fix `pyproject.toml` fields.

9. Suggested CI checks (optional)
--------------------------------

- Build artifacts in Docker and store them as CI artifacts.
- Run `twine check` and a smoke install against TestPyPI.
- Automate tagging and GitHub release creation only after manual approval.

10. Security and publishing notes
--------------------------------

- Never commit API tokens. Use secrets in CI and pass them as env vars to Docker.
- Prefer ephemeral test runs in containers; never run build/release on untrusted machines.

Handoff
-------

Changed paths:
- `docs/pypi_release_manual.md`

Why:
- Provide a repeatable, Docker-first release workflow and troubleshooting guidance.

Verification performed:
- Documentation-only; no runtime verification performed here.

Known limitations + follow-ups:
- This doc assumes a Dockerfile and that the project uses `build` and `twine`. Adjust commands to match your repository's tooling.
