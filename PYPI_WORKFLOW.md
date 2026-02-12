# Production PyPI Publishing Workflow

This repository includes a GitHub Actions workflow to automatically publish the `hyperlink_button` package to **production PyPI** (pypi.org).

## Workflow File

`.github/workflows/publish-to-pypi.yml`

## Triggers

The workflow runs **only** on:
- **Version tags:** Tags starting with `v` (e.g., `v0.1.0`, `v1.0.0`)
- **Manual trigger:** Via workflow_dispatch in GitHub Actions UI

**Note:** This workflow does NOT trigger on pushes to branches. This is a conservative approach to ensure production releases are intentional.

## Prerequisites

### 1. PyPI API Token
The workflow requires a production PyPI API token stored as a GitHub secret:
- **Secret name:** `PYPI_API_KEY`
- **How to create:** Visit https://pypi.org/manage/account/token/
- **How to add to GitHub:** Repository Settings → Secrets and variables → Actions → New repository secret

### 2. Required Files
- Frontend source: `hyperlink_button/frontend/`
- Python package: `hyperlink_button/`
- Build configuration: `pyproject.toml`

## Workflow Steps

1. **Checkout repository** - Gets the latest code from the tag
2. **Set up Node.js 20** - Required for frontend build
3. **Build frontend** - Compiles React/TypeScript components
4. **Set up Python 3.13** - Required for package build
5. **Install build tools** - Installs `build` and `twine`
6. **Build package** - Creates wheel and source distribution
7. **Validate package** - Runs `twine check` to verify metadata
8. **Publish to PyPI** - Uploads package using API token

## Publishing a New Version

### Option 1: Create a Version Tag (Recommended)

This is the standard way to publish a new version:

1. Update the version in `pyproject.toml`:
   ```toml
   version = "0.1.1"  # Update this
   ```

2. Commit the version change:
   ```bash
   git add pyproject.toml
   git commit -m "Bump version to 0.1.1"
   git push origin main
   ```

3. Create and push a version tag:
   ```bash
   git tag v0.1.1
   git push origin v0.1.1
   ```

4. The workflow will automatically trigger and publish to PyPI

### Option 2: Manual Workflow Trigger

To manually trigger the workflow without creating a tag:

1. Go to Actions tab: https://github.com/maxim-saplin/hyperlink_button/actions
2. Select "Publish to PyPI" workflow
3. Click "Run workflow" button
4. Select the branch to run from (usually `main`)
5. Click "Run workflow" to start

**Warning:** When manually triggering, ensure the version in `pyproject.toml` has been updated and doesn't already exist on PyPI.

## Viewing Workflow Runs

Visit: https://github.com/maxim-saplin/hyperlink_button/actions/workflows/publish-to-pypi.yml

## After Successful Publication

Once published, the package will be available at:
- **PyPI page:** https://pypi.org/project/hyperlink-button/
- **Install command:**
  ```bash
  pip install hyperlink-button
  ```

## Differences from Test PyPI Workflow

| Feature | Test PyPI | Production PyPI |
|---------|-----------|-----------------|
| Workflow file | `publish-to-testpypi.yml` | `publish-to-pypi.yml` |
| Secret name | `TESTPYPI_API_KEY` | `PYPI_API_KEY` |
| Repository URL | https://test.pypi.org | https://pypi.org |
| Triggers | Push to main/branch, tags, manual | **Tags only**, manual |
| Upload flag | `--skip-existing` | None (fail if exists) |
| Purpose | Testing/development | Production releases |

## Troubleshooting

### Version already exists
If you get an error that the version already exists on PyPI:
- Update the version in `pyproject.toml`
- PyPI does not allow re-uploading the same version
- Consider using semantic versioning: MAJOR.MINOR.PATCH

### Workflow not running from tag
- Ensure the tag starts with `v` (e.g., `v0.1.0`, not `0.1.0`)
- Check that the tag was pushed: `git push origin v0.1.0`
- Verify the tag exists: `git tag -l`

### Build failures
- Frontend build: Ensure Node.js version compatibility
- Python build: Verify `pyproject.toml` configuration
- Check workflow logs for specific error messages

### Upload failures
- Verify PyPI token is valid and not expired
- Ensure the version doesn't already exist on PyPI
- Check package metadata is compatible (use `twine check`)

## Best Practices

1. **Always test on Test PyPI first:**
   - Push to `main` branch to test the build on Test PyPI
   - Verify the package installs correctly
   - Then create a version tag for production

2. **Use semantic versioning:**
   - MAJOR version: Breaking changes
   - MINOR version: New features (backward compatible)
   - PATCH version: Bug fixes

3. **Keep version in sync:**
   - Update `pyproject.toml` version before tagging
   - Tag name should match package version (e.g., `v0.1.1` for version `0.1.1`)

4. **Document releases:**
   - Create GitHub releases with changelogs
   - Tag releases correspond to PyPI versions

## Package Metadata Compatibility

The package uses `setuptools<77` to ensure compatibility with PyPI's metadata parser (Metadata-Version 2.2). This prevents errors related to newer metadata fields like `license-expression`.
