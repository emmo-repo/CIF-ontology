"""Tests for `dic2owl.cli`."""
# pylint: disable=import-outside-toplevel
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import Callable

    from .conftest import CLIRunner, CompletedProcess


@pytest.mark.parametrize("use_subprocess", [True, False])
def test_version(clirunner: "CLIRunner", use_subprocess: bool) -> None:
    """Test `--version`."""
    from dic2owl import __version__

    output = clirunner(["--version"], use_subprocess=use_subprocess)
    assert output.stdout == f"dic2owl version {__version__}\n"


@pytest.mark.parametrize("use_subprocess", [True, False])
def test_local_file(
    clirunner: "CLIRunner",
    top_dir: Path,
    cif_ttl: str,
    create_location_free_ttl: "Callable[[Path], str]",
    use_subprocess: bool,
) -> None:
    """Test a normal/default run with minimum input.

    NOTE: The comment conerning the file location has been removed from the
        static test Turtle file.
    """
    from tempfile import TemporaryDirectory

    from rdflib.graph import Graph

    with TemporaryDirectory() as tmpdir:
        options = [
            str(top_dir / "tests" / "dic2owl" / "static" / "cif_core_minimized.dic")
        ]
        output: "CompletedProcess" = clirunner(
            options, run_dir=tmpdir, use_subprocess=use_subprocess
        )

        assert (
            "downloading" in output.stdout
        ), f"STDOUT: {output.stdout}\nSTDERR: {output.stderr}"

        generated_ttl = create_location_free_ttl(
            Path(tmpdir) / "cif_core_minimized.ttl"
        )

        generated = Graph()
        generated.parse(data=generated_ttl)

        cif = Graph()
        cif.parse(data=cif_ttl)

        for triple in generated:
            assert triple in cif, triple

        content = [_ for _ in Path(tmpdir).iterdir() if _.is_file()]
        assert len(content) == 4, (
            "Since `dic2owl` downloads 3 files and the TTL file is generated "
            "here, the temporary folder should contain a total of 4 files, "
            f"but instead it contains {len(content)} file(s): {content}"
        )


@pytest.mark.parametrize("use_subprocess", [True, False])
def test_output(
    clirunner: "CLIRunner",
    top_dir: Path,
    cif_ttl: str,
    create_location_free_ttl: "Callable[[Path], str]",
    use_subprocess: bool,
) -> None:
    """Test `--output`.

    NOTE: The comment conerning the file location has been removed from the
        static test Turtle file.
    """
    from tempfile import TemporaryDirectory

    from rdflib.graph import Graph

    with TemporaryDirectory() as tmpdir:
        out_ttl = Path(tmpdir) / "cif_core_minimized.ttl"
        options = [
            "--output",
            str(out_ttl),
            str(top_dir / "tests" / "dic2owl" / "static" / "cif_core_minimized.dic"),
        ]
        output: "CompletedProcess" = clirunner(options, use_subprocess=use_subprocess)

        assert (
            "downloading" in output.stdout
        ), f"STDOUT: {output.stdout}\nSTDERR: {output.stderr}"

        generated_ttl = create_location_free_ttl(out_ttl)

        generated = Graph()
        generated.parse(data=generated_ttl)

        cif = Graph()
        cif.parse(data=cif_ttl)

        for triple in generated:
            assert triple in cif, triple

        content = [_ for _ in Path(tmpdir).iterdir() if _.is_file()]
        assert len(content) == 1, (
            "Since `dic2owl` downloads 3 files, but in another directory and "
            "only the generated TTL file is in the temporary folder, there "
            "should only be 1 file in the temporary folder. But instead it "
            f"contains {len(content)} file(s): {content}"
        )
