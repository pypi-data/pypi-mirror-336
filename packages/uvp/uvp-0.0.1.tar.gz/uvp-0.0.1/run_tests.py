#!/usr/bin/env python3
"""
Script to run tests with pytest.
"""

import subprocess
import sys


def run_tests():
    """Run pytest and return the exit code."""
    cmd = [
        "python",
        "-m",
        "pytest",
        "tests/",
    ]
    return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(run_tests())
