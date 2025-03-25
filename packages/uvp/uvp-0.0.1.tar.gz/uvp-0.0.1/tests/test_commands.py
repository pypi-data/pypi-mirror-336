"""
Tests for commands module functionality.
"""

import subprocess
from unittest.mock import MagicMock, patch

import typer

from uvp.commands import base


def test_base_imports():
    """Test that commands.base module imports correctly."""
    assert base is not None


def test_main_with_no_subcommand():
    """Test the main callback function with no subcommand."""
    ctx = MagicMock()
    ctx.invoked_subcommand = None

    with patch("typer.echo") as mock_echo:
        base.main(ctx)
        # Check if help was shown
        assert ctx.get_help.called
        assert mock_echo.called


def test_version_command():
    """Test the version command."""
    with (
        patch("importlib.metadata.version") as mock_version,
        patch("typer.echo") as mock_echo,
    ):
        mock_version.return_value = "0.0.1"  # Match version in pyproject.toml
        base.version()
        mock_echo.assert_called_once_with("uvp version: 0.0.1")


def test_version_command_development():
    """Test the version command when package is not found."""
    with (
        patch("uvp.core.__version__", "development"),
        patch("typer.echo") as mock_echo,
    ):
        base.version()
        mock_echo.assert_called_once_with("uvp version: development")


def test_info_command():
    """Test the info command."""
    with (
        patch("typer.echo") as mock_echo,
        patch("platform.platform", return_value="Test Platform"),
        patch("sys.version", "3.10.0"),
        patch("subprocess.run") as mock_run,
    ):
        # Mock successful uv version check
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "0.5.0\n"
        mock_run.return_value = mock_result

        base.info()

        # Verify all expected outputs were echoed
        assert mock_echo.call_count >= 4
        mock_echo.assert_any_call("UVP Information:")
        mock_echo.assert_any_call("Python version: 3.10.0")
        mock_echo.assert_any_call("Platform: Test Platform")
        mock_echo.assert_any_call("uv version: 0.5.0")


def test_pkg_install_command():
    """Test the pkg_install command."""
    with patch("typer.echo") as mock_echo, patch("subprocess.run") as mock_run:
        # Call the command with test packages
        base.pkg_install(packages=["pytest", "coverage"], dev=False)

        # Verify the subprocess.run was called with correct arguments
        mock_run.assert_called_once_with(
            ["uv", "pip", "install", "pytest", "coverage"], check=True
        )

        # Verify success message
        mock_echo.assert_any_call("✅ Packages installed successfully")


def test_pkg_install_command_dev():
    """Test the pkg_install command with dev flag."""
    with patch("typer.echo") as mock_echo, patch("subprocess.run") as mock_run:
        # Call the command with test packages and dev flag
        base.pkg_install(packages=["pytest", "coverage"], dev=True)

        # Verify the subprocess.run was called with correct arguments
        mock_run.assert_called_once_with(
            ["uv", "pip", "install", "--dev", "pytest", "coverage"], check=True
        )

        # Verify success message
        mock_echo.assert_any_call("✅ Packages installed successfully")


def test_pkg_install_command_failure():
    """Test the pkg_install command when it fails."""
    with (
        patch("typer.echo") as mock_echo,
        patch("subprocess.run") as mock_run,
    ):
        # Make subprocess.run raise CalledProcessError
        mock_run.side_effect = subprocess.CalledProcessError(
            1, ["uv", "pip", "install"]
        )

        # Call the command with test packages and expect typer.Exit
        try:
            base.pkg_install(packages=["non-existent-package"])
            assert False, "Expected typer.Exit to be raised"
        except typer.Exit as e:
            assert e.exit_code == 1

        # Verify error message
        mock_echo.assert_called_with("❌ Failed to install packages", err=True)
