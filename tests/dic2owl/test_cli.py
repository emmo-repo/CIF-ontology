"""Tests for `dic2owl.cli`."""
# pylint: disable=import-outside-toplevel
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .conftest import CLIRunner


def test_version(clirunner: "CLIRunner") -> None:
    """Test `--version`."""
    from dic2owl import __version__

    output = clirunner(["--version"])
    assert output.stdout == f"dic2owl version {__version__}\n"


def test_local_file(
    clirunner: "CLIRunner", top_dir: Path, cif_ttl: str
) -> None:
    """Test a normal/default run with minimum input.

    NOTE: The commend conerning the file location has been removed from the
        static test Turtle file.
    """
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as tmpdir:
        options = [
            str(top_dir / "tests/dic2owl/static/cif_core_minimized.dic")
        ]
        output = clirunner(options, run_dir=tmpdir)

        assert (
            "downloading" in output.stdout
        ), f"STDOUT: {output.stdout}\nSTDERR: {output.stderr}"

        generated_ttl = ""
        with open(Path(tmpdir) / "cif_core_minimized.ttl", "r") as handle:
            for line in handle.readlines():
                if "dic2owl" in line:
                    # Skip comment line concerning the file location
                    pass
                else:
                    generated_ttl += line

        assert generated_ttl == cif_ttl

        content = [_ for _ in Path(tmpdir).iterdir() if _.is_file()]
        assert len(content) == 4, (
            "Since `dic2owl` downloads 3 files and the TTL file is generated "
            "here, the temporary folder should contain a total of 4 files, "
            f"but instead it contains {len(content)} file(s): {content}"
        )


def test_output(clirunner: "CLIRunner", top_dir: Path, cif_ttl: str) -> None:
    """Test `--output`.

    NOTE: The commend conerning the file location has been removed from the
        static test Turtle file.
    """
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as tmpdir:
        out_ttl = f"{tmpdir}/test.ttl"
        options = [
            "--output",
            out_ttl,
            str(top_dir / "tests/dic2owl/static/cif_core_minimized.dic"),
        ]
        output = clirunner(options)

        assert (
            "downloading" in output.stdout
        ), f"STDOUT: {output.stdout}\nSTDERR: {output.stderr}"

        generated_ttl = ""
        with open(out_ttl, "r") as handle:
            for line in handle.readlines():
                if "dic2owl" in line:
                    # Skip comment line concerning the file location
                    pass
                else:
                    generated_ttl += line

        assert generated_ttl == cif_ttl

        content = [_ for _ in Path(tmpdir).iterdir() if _.is_file()]
        assert len(content) == 1, (
            "Since `dic2owl` downloads 3 files, but in another directory and "
            "only the generated TTL file is in the temporary folder, there "
            "should only be 1 file in the temporary folder. But instead it "
            f"contains {len(content)} file(s): {content}"
        )
