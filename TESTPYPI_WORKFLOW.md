# Test PyPI Publishing Workflow

This repository includes a GitHub Actions workflow to automatically publish the `hyperlink_button` package to **Test PyPI** for testing purposes.

**For production releases to PyPI, see [PYPI_WORKFLOW.md](PYPI_WORKFLOW.md)**

## Workflow File

`.github/workflows/publish-to-testpypi.yml`

## Triggers

The workflow runs automatically on:
- **Push to branches:** `main` or `copilot/publish-to-test-pypi`
- **Version tags:** Tags starting with `v` (e.g., `v0.1.0`, `v1.0.0`)
- **Manual trigger:** Via workflow_dispatch in GitHub Actions UI

## Prerequisites

### 1. Test PyPI API Token
The workflow requires a Test PyPI API token stored as a GitHub secret:
- **Secret name:** `TESTPYPI_API_KEY`
- **How to create:** Visit https://test.pypi.org/manage/account/token/
- **How to add to GitHub:** Repository Settings → Secrets and variables → Actions → New repository secret

### 2. Required Files
- Frontend source: `hyperlink_button/frontend/`
- Python package: `hyperlink_button/`
- Build configuration: `pyproject.toml`

## Workflow Steps

1. **Checkout repository** - Gets the latest code
2. **Set up Node.js 20** - Required for frontend build
3. **Build frontend** - Compiles React/TypeScript components
4. **Set up Python 3.13** - Required for package build
5. **Install build tools** - Installs `build` and `twine`
6. **Build package** - Creates wheel and source distribution
7. **Validate package** - Runs `twine check` to verify metadata
8. **Publish to Test PyPI** - Uploads package using API token

## Manual Workflow Trigger

To manually trigger the workflow:

1. Go to Actions tab: https://github.com/maxim-saplin/hyperlink_button/actions
2. Select "Publish to Test PyPI" workflow
3. Click "Run workflow" button
4. Select the branch to run from
5. Click "Run workflow" to start

## Viewing Workflow Runs

Visit: https://github.com/maxim-saplin/hyperlink_button/actions/workflows/publish-to-testpypi.yml

## Approving First-Time Workflows

If a workflow shows `action_required` status:
1. Visit the specific run URL
2. Review the workflow
3. Click "Approve and run" button

## Testing the Package

After successful publication, test installation:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ hyperlink_button
```

Note: The `--extra-index-url` is needed for dependencies that aren't on Test PyPI.

## Troubleshooting

### Workflow not running
- Check if the secret `TESTPYPI_API_KEY` is set
- Verify the branch name matches the trigger configuration
- Check workflow permissions in repository settings

### Build failures
- Frontend build: Ensure Node.js version compatibility
- Python build: Verify `pyproject.toml` configuration
- Check workflow logs for specific error messages

### Upload failures
- Verify Test PyPI token is valid and not expired
- Check if the version already exists (use `--skip-existing`)
- Ensure package metadata is compatible (Metadata-Version 2.2)

## Package Metadata Compatibility

The package uses `setuptools<77` to ensure compatibility with Test PyPI's metadata parser (Metadata-Version 2.2). This prevents errors related to newer metadata fields like `license-expression`.
