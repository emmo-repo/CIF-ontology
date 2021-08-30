"""PyTest fixtures for `dic2owl`."""
# pylint: disable=import-outside-toplevel,consider-using-with,too-many-branches
# pylint: disable=redefined-outer-name,inconsistent-return-statements
from enum import Enum
from pathlib import Path
from typing import List, Optional, TYPE_CHECKING, Union

import pytest


class CLI(Enum):
    """Enumeration of CLIs."""

    CIF2OWL = "cif2owl"
    DIC2OWL = "dic2owl"


if TYPE_CHECKING:
    from subprocess import CompletedProcess
    from typing import Callable

    CLIRunner = Callable[
        [
            Optional[List[str]],
            Optional[Union[CLI, str]],
            Optional[str],
            Optional[Union[Path, str]],
        ],
        CompletedProcess,
    ]


@pytest.fixture(scope="session")
def clirunner() -> "CLIRunner":
    """Call `dic2owl` CLI"""
    from subprocess import run, CalledProcessError
    from tempfile import TemporaryDirectory

    def _clirunner(
        options: Optional[List[str]] = None,
        cli: Optional[Union[CLI, str]] = None,
        expected_error: Optional[str] = None,
        run_dir: Optional[Union[Path, str]] = None,
    ) -> Union["CompletedProcess", CalledProcessError]:
        """Call `dic2owl` CLI

        Parameters:
            options: Options with which to call `cli`, e.g., `--version`.
            cli: The CLI to call, defaults to `dic2owl`.
            expected_error: Sub-string expected in error output, if an error is
                expected.
            run_dir: The directory to use as current work directory when
                running the CLI.

        Returns:
            The return class for a successful call to `subprocess.run()`.

        """
        options = options or []

        if not isinstance(options, list):
            try:
                options = list(options)
            except TypeError as exc:
                raise TypeError("options must be a list of strings.") from exc

        if cli is not None:
            try:
                cli = CLI(cli)
            except ValueError as exc:
                raise ValueError(
                    f"{cli!r} is not a recognized CLI. Recognized CLIs: "
                    f"{list(CLI.__members__)}"
                ) from exc
        else:
            cli = CLI.DIC2OWL

        if run_dir is None:
            run_dir = TemporaryDirectory()
        elif isinstance(run_dir, Path):
            run_dir = run_dir.resolve()
        else:
            try:
                run_dir = Path(run_dir).resolve()
            except TypeError as exc:
                raise TypeError(f"{run_dir} is not a valid path.") from exc

        try:
            output = run(
                args=[cli.value] + options,
                capture_output=True,
                check=True,
                cwd=run_dir.name
                if isinstance(run_dir, TemporaryDirectory)
                else run_dir,
                text=True,
            )
            if expected_error:
                pytest.fail(
                    "Expected the CLI call to fail with an error containing "
                    f"the sub-string: {expected_error}"
                )
        except CalledProcessError as error:
            if expected_error:
                if (
                    expected_error in error.stdout
                    or expected_error in error.stderr
                ):
                    # Expected error, found expected sub-string as well.
                    return error

                pytest.fail(
                    "The CLI call failed as expected, but the expected "
                    "error sub-string could not be found in stdout or "
                    f"stderr. Sub-string: {expected_error}"
                )
            else:
                pytest.fail(
                    "The CLI call failed when it didn't expect to.\n"
                    f"Information: {error}"
                )
        else:
            return output
        finally:
            if isinstance(run_dir, TemporaryDirectory):
                run_dir.cleanup()

    return _clirunner


@pytest.fixture(scope="session")
def top_dir() -> Path:
    """Return repository path."""
    return Path(__file__).parent.parent.parent.resolve()


@pytest.fixture(scope="session")
def cif_ttl(top_dir: Path) -> str:
    """Read and return CIF-Core minimized Turtle file (generated from the
    accompanying dictionary).

    NOTE: The commend conerning the file location has been removed manually
        from this file.
    """
    with open(
        top_dir / "tests/dic2owl/static/cif_core_minimized.ttl", "r"
    ) as handle:
        content = handle.read()
    return content
