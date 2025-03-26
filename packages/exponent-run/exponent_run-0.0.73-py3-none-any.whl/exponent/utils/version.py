import subprocess
from importlib.metadata import Distribution, PackageNotFoundError
from json import JSONDecodeError
from typing import List, Literal, Optional, Union, cast, Any
import sys
import click
from httpx import Client, HTTPError
from packaging.version import Version
import pkg_resources
import platform


def get_python_path() -> str:
    """Get the path to the Python interpreter."""
    try:
        return subprocess.check_output(["which", "python"]).decode().strip()
    except Exception:
        return "unknown"


def get_sys_executable() -> str:
    """Get the path to the Python interpreter."""
    return str(sys.executable)


def get_installed_version() -> Union[str, Literal["unknown"]]:
    """Get the installed version of exponent-run.

    Returns:
        The installed version of exponent-run if it can be determined, otherwise "unknown"
    """
    try:
        return Distribution.from_name("exponent-run").version
    except PackageNotFoundError as e:
        click.echo(f"Error reading version: {e}", err=True)
        return "unknown"


def get_installed_metadata() -> Union[Any, Literal["unknown"]]:
    """Get the installed metadata of exponent-run.

    Returns:
        The installed metadata of exponent-run if it can be determined, otherwise "unknown"
    """
    try:
        return Distribution.from_name("exponent-run").metadata
    except PackageNotFoundError as e:
        click.echo(f"Error reading metadata: {e}", err=True)
        return "unknown"


def get_installer() -> Union[str, Literal["unknown"]]:
    """Get the installer of exponent-run.

    Returns:
        The installer of exponent-run if it can be determined, otherwise "unknown"
    """
    try:
        return cast(
            str,
            pkg_resources.get_distribution("exponent-run").get_metadata("INSTALLER"),
        )
    except Exception:
        return "unknown"


def get_latest_pypi_exponent_version() -> Optional[str]:
    """Get the latest version of Exponent available on PyPI.

    Returns:
        The newest version of Exponent available on PyPI, or None if an error occurred.
    """
    try:
        return cast(
            str,
            (
                Client()
                .get("https://pypi.org/pypi/exponent-run/json")
                .json()["info"]["version"]
            ),
        )
    except (HTTPError, JSONDecodeError, KeyError):
        click.secho(
            "An unexpected error occurred communicating with PyPi, please check your network and try again.",
            fg="red",
        )
        return None


def check_exponent_version() -> Optional[tuple[str, str]]:
    """Check if there is a newer version of Exponent available on PyPI .

    Returns:
        None
    """

    installed_version = get_installed_version()
    if installed_version == "unknown":
        click.secho("Unable to determine current Exponent version.", fg="yellow")
        return None

    if (latest_version := get_latest_pypi_exponent_version()) and Version(
        latest_version
    ) > Version(installed_version):
        return installed_version, latest_version

    return None


def _get_upgrade_command() -> List[str]:
    """Get the install command for exponent."""

    return [sys.executable, "-m", "pip", "install", "--upgrade", "exponent-run"]


def _ask_continue_without_updating() -> None:
    if click.confirm("Continue without updating?", default=False):
        click.secho("Using outdated version.", fg="red")
    else:
        sys.exit(1)


def upgrade_exponent(
    *,
    current_version: str,
    new_version: str,
    force: bool,
    is_upgrade_cmd: bool = False,
) -> None:
    """Upgrade Exponent to the passed in version.

    Args:
        current_version: The current version of Exponent.
        new_version: The new version of Exponent.
        force: Whether to force the upgrade without prompting for confirmation.

    Returns:
        None
    """
    new_version_str = (
        f"New version available: exponent-run=={new_version} (current: {current_version})\n"
        "See https://docs.exponent.run/installation for details.\n"
    )
    upgrade_command = _get_upgrade_command()

    upgrade_command_str = " ".join(upgrade_command)

    if platform.system() == "Windows":
        click.secho(
            f"{new_version_str}\nRun this command to update:\n{upgrade_command_str}",
            fg="yellow",
            bold=True,
        )
        if not is_upgrade_cmd:
            _ask_continue_without_updating()
        return

    if not force:
        click.secho(
            f"{new_version_str}\nUpdate command: '{upgrade_command_str}'",
            fg="yellow",
            bold=True,
        )

        if not click.confirm("Update now?", default=True):
            return
    else:
        click.echo(f"Current version: {current_version}")
        click.echo(f"New version available: {new_version}")

    click.secho("Updating...", bold=True, fg="yellow")
    subprocess.check_call(upgrade_command)

    click.secho(f"Successfully upgraded Exponent to version {new_version}!", fg="green")

    click.echo("Re-run exponent to use the latest version.")
    exit(1)
