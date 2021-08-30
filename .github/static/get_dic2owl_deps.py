"""
# Retrieve dependencies

Retrieve dependencies from a `requirements.txt`-style file.
"""
import argparse
from pathlib import Path
import re
from typing import Set


def main(argv_input: list = None) -> Set[str]:
    """Retrieve dependencies"""
    parser = argparse.ArgumentParser(
        description=main.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "requirements_files",
        metavar="FILE",
        type=Path,
        nargs="+",
        help="The path(s) to one or several requirements.txt-style file(s).",
    )
    args = parser.parse_args(argv_input)

    requirements_regex = re.compile(
        r"^(?P<name>[A-Za-z0-9_-]+)(~=|>=|==).*\n$"
    )
    dependencies = set()
    for file in args.requirements_files:
        if not file.exists():
            raise FileNotFoundError(f"Could not find {file} !")
        with open(file.resolve(), "r") as handle:
            for line in handle.readlines():
                match = requirements_regex.fullmatch(line)
                if match is None:
                    raise ValueError(
                        (
                            "Couldn't determine package name from line:\n\n  "
                            f"{line}"
                        )
                    )
                dependencies.add(match.group("name"))
    return dependencies


if __name__ == "__main__":
    from sys import argv

    parsed_dependencies = main(argv[1:])
    grep_extended_regex = f"({'|'.join(parsed_dependencies)})"
    print(grep_extended_regex)
