"""
# `dic2owl` CLI

The `dic2owl` command line interface (CLI) is an easy way of running the
ontology-generation tool for CIF `.dic`-files.
"""
import argparse
import logging
from pathlib import Path


LOGGING_LEVELS = [
    logging.getLevelName(level).lower() for level in range(0, 51, 10)
]


def main(argv: list = None) -> None:
    """Ontologize CIF dictionaries (`.dic`) using OWL.

    Produce an OWL Turtle (`.ttl`) file from a CIF dictionary (`.dic`) file.
    """
    # pylint: disable=import-outside-toplevel
    from dic2owl import __version__
    from dic2owl.dic2owl import main as dic2owl_run

    parser = argparse.ArgumentParser(
        description=main.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--version",
        action="version",
        help="Show the version and exit.",
        version=f"dic2owl version {__version__}",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        help="Set the stdout log-level (verbosity).",
        choices=LOGGING_LEVELS,
        default="info",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Overrule log-level option, setting it to 'debug'.",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="OWL_TTL",
        dest="ttlfile",
        type=Path,
        help=(
            'The generated output file. Example "--output cif_core.ttl". If '
            "output is not provided, the filename will be taken to be similar "
            "to the CIF_DIC file."
        ),
    )
    parser.add_argument(
        "dicfile",
        metavar="CIF_DIC",
        type=Path,
        help=(
            "The CIF dictionary file from which to generate an OWL ontologized"
            " Turtle file."
        ),
    )

    args = parser.parse_args(argv)

    if args.ttlfile is None:
        args.ttlfile = (
            args.dicfile.resolve().name[: -len(args.dicfile.suffix)] + ".ttl"
        )

    if not args.dicfile.resolve().exists():
        # The dic-file does not exist, use it as a string instead so it can be
        # downloaded.
        args.dicfile = str(args.dicfile)

    dic2owl_run(dicfile=args.dicfile, ttlfile=args.ttlfile)
