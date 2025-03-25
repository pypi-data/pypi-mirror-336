"""
Shared pytest fixtures for all tests.
"""

import site
import sys
from pathlib import Path

import pytest

# Add site-packages and src directory to the path for imports
site_packages = site.getsitepackages()[0]
sys.path.insert(0, site_packages)
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def sample_fixture():
    """Sample fixture for demonstration purposes."""
    return {"test_data": "value"}
