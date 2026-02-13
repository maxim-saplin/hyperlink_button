# Publishing Workflows

This repository has two automated publishing workflows for the `hyperlink_button` package.

## Workflows Overview

| Workflow | File | Triggers | Purpose | Secret |
|----------|------|----------|---------|--------|
| **Test PyPI** | `publish-to-testpypi.yml` | Push to main/branch, tags, manual | Testing & development | `TESTPYPI_API_KEY` |
| **Production PyPI** | `publish-to-pypi.yml` | Tags (`v*`), manual only | Production releases | `PYPI_API_KEY` |

## Quick Start

### Testing a Release (Test PyPI)

1. Push changes to `main` branch
2. Workflow automatically builds and publishes to Test PyPI
3. Test installation:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ hyperlink-button
   ```

### Publishing a Production Release (PyPI)

1. Update version in `pyproject.toml`
2. Commit and push to `main`
3. Create and push a version tag:
   ```bash
   git tag v0.1.1
   git push origin v0.1.1
   ```
4. Workflow automatically publishes to PyPI
5. Install the package:
   ```bash
   pip install hyperlink-button
   ```

## Detailed Documentation

- **Test PyPI Workflow:** [TESTPYPI_WORKFLOW.md](TESTPYPI_WORKFLOW.md)
- **Production PyPI Workflow:** [PYPI_WORKFLOW.md](PYPI_WORKFLOW.md)

## Workflow Actions

Both workflows perform the same build steps:
1. ✅ Checkout repository
2. ✅ Build frontend (Node.js 20)
3. ✅ Build Python package (Python 3.13)
4. ✅ Validate with twine check
5. ✅ Publish to respective PyPI repository

## Required Secrets

Configure these in: Repository Settings → Secrets and variables → Actions

- `TESTPYPI_API_KEY` - Token from https://test.pypi.org/manage/account/token/
- `PYPI_API_KEY` - Token from https://pypi.org/manage/account/token/

## Best Practices

1. **Always test first:** Use Test PyPI before publishing to production
2. **Use semantic versioning:** MAJOR.MINOR.PATCH
3. **Tag releases:** Match tag version to package version
4. **Document changes:** Create GitHub releases with changelogs

## Links

- **Test PyPI Package:** https://test.pypi.org/project/hyperlink-button/
- **PyPI Package:** https://pypi.org/project/hyperlink-button/
- **GitHub Actions:** https://github.com/maxim-saplin/hyperlink_button/actions
