# uvp Tests

This directory contains tests for the `uvp` package.

## Running Tests

You can run the tests using one of the following methods:

### Using the run_tests.py script

```bash
./run_tests.py
```

### Using pytest directly

```bash
# Run all tests
uvx pytest

# Run specific test file
python -m pytest tests/test_core.py
```

### Using uv run

```bash
uv run pytest
```

## Test Structure

- `conftest.py`: Contains shared fixtures for tests
- `test_core.py`: Tests for core functionality
- `test_commands.py`: Tests for command modules
- `test_main.py`: Tests for CLI entrypoint

Coverage reports are automatically generated when running tests through pytest thanks to pytest-cov
configuration in pytest.ini.
