"""Core functionality for the uvp CLI application."""

import importlib.metadata as metadata

import typer

try:
    __version__ = metadata.version("uvp")
except metadata.PackageNotFoundError:
    __version__ = "development"

app = typer.Typer(
    name="uvp",
    help="All-in-one tool for managing and deploying Python projects",
    add_completion=True,
    no_args_is_help=True,
    pretty_exceptions_enable=False,
)


def version_callback(value: bool) -> None:
    """Show version information and exit."""
    if value:
        typer.echo(f"uvp version: {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
) -> None:
    """Main callback for the CLI application."""
    pass
