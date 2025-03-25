"""Base commands for the uvp CLI application."""

import subprocess
import sys
from inspect import get_annotations

import typer

from uvp.core import app

get_annotations(typer.Argument)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """UVP: All-in-one tool for managing and deploying Python projects.

    Built with uv as the main package manager.
    """
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())


@app.command()
def version() -> None:
    """Show the version of uvp."""
    from uvp.core import __version__

    typer.echo(f"uvp version: {__version__}")


@app.command()
def info() -> None:
    """Show information about the uvp installation."""
    import platform

    from uvp.core import __version__

    typer.echo("UVP Information:")
    typer.echo(f"Python version: {sys.version.split()[0]}")
    typer.echo(f"Platform: {platform.platform()}")
    typer.echo(f"UVP version: {__version__}")

    # Display uv version if available
    try:
        result = subprocess.run(
            ["uv", "--version"], capture_output=True, text=True, check=True
        )
        typer.echo(f"uv version: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        typer.echo("uv: Not installed or not found in PATH")


# Package management commands
@app.command(name="install")
def pkg_install(
    packages: list[str] = typer.Argument(help="Package(s) to install"),
    dev: bool = typer.Option(
        False, "--dev", "-d", help="Install as development dependency"
    ),
) -> None:
    """Install packages using uv."""
    cmd = ["uv", "pip", "install"]
    if dev:
        cmd.append("--dev")
    cmd.extend(packages)

    try:
        subprocess.run(cmd, check=True)
        typer.echo("✅ Packages installed successfully")
    except subprocess.CalledProcessError:
        typer.echo("❌ Failed to install packages", err=True)
        raise typer.Exit(code=1)
