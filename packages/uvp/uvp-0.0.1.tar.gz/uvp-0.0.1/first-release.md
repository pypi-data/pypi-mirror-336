# First Release Instructions

This document outlines the steps needed to publish the package to PyPI using GitHub Actions with
trusted publishing.

## Prerequisites

1. Ensure you have a PyPI account
   - Create one at https://pypi.org/account/register/ if you don't have one

## Setting up PyPI Trusted Publisher

1. Go to PyPI project page (create it if it doesn't exist)
2. Navigate to the "Publishing" tab
3. In the "Trusted publishers" section, click "Add a new publisher"
4. Fill in the following details:
   - Publisher: GitHub Actions
   - Organization: your GitHub username or organization (carlosferreyra)
   - Project: uvp
   - Environment: pypi
   - Workflow name: Publish Python Package

Note: The workflow name must match exactly with what's in your GitHub Actions workflow file.

## Creating the GitHub Actions Workflow

1. Create a new file in your repository at `.github/workflows/publish.yml` with the following
   content:

```yaml
name: Publish Python Package

on:
  release:
    types: [published]

permissions:
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: pypi
      url: https://pypi.org/p/uvp
    permissions:
      id-token: write

    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Install build dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build
      - name: Build package
        run: python -m build
      - name: Publish package
        uses: pypa/gh-action-pypi-publish@release/v1
```

## Publishing Process

1. Ensure your package version in `pyproject.toml` is updated
2. Create and push a new tag:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```
3. Create a new release on GitHub:
   - Go to your repository's Releases page
   - Click "Create a new release"
   - Choose the tag you just created
   - Add release notes
   - Publish the release

The GitHub Action will automatically:

1. Build your package
2. Upload it to PyPI using OIDC authentication
3. Make it available for installation via `uv pip install uvp`

## Verifying the Release

After the workflow completes:

1. Check your package page on PyPI: https://pypi.org/project/uvp/
2. Try installing your package in a new virtual environment:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install uvp
   ```

## Troubleshooting

- If the build fails, check the GitHub Actions logs for detailed error messages
- Ensure your `pyproject.toml` is properly configured with all required metadata
- Verify that your package has a unique name on PyPI
- Make sure all required files are included in your package (check `MANIFEST.in` if you have one)
- If the trusted publisher setup fails, verify that all details match exactly (case-sensitive)
- Ensure the GitHub Actions environment name matches what you configured in PyPI
