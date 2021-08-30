"""
# Install `dic2owl`

Run `pip install -e .` when in the folder of this file.
If in the root of the repository run instead `pip install -e ./dic2owl`.

Together with the `dic2owl` package, the CLI tool with the same name will be
installed.
To find out more, run `dic2owl --help` after a successful installation.
"""
from pathlib import Path
import re

from setuptools import setup, find_packages


PACKAGE_DIR = Path(__file__).parent.resolve()

with open(PACKAGE_DIR / "dic2owl/__init__.py", "r") as handle:
    VERSION = AUTHOR = AUTHOR_EMAIL = None
    for line in handle.readlines():
        VERSION_match = re.match(
            r'__version__ = "(?P<version>[0-9]+(\.[0-9]+){2})"', line
        )
        AUTHOR_match = re.match(r'__author__ = "(?P<author>.+)"', line)
        AUTHOR_EMAIL_match = re.match(
            r'__author_email__ = "(?P<email>.+@.+\..+)"', line
        )

        if VERSION_match is not None:
            VERSION = VERSION_match
        if AUTHOR_match is not None:
            AUTHOR = AUTHOR_match
        if AUTHOR_EMAIL_match is not None:
            AUTHOR_EMAIL = AUTHOR_EMAIL_match

    for info, value in {
        "version": VERSION,
        "author": AUTHOR,
        "author email": AUTHOR_EMAIL,
    }.items():
        if value is None:
            raise RuntimeError(
                (
                    f"Could not determine {info} from "
                    f"{PACKAGE_DIR / 'dic2owl/__init__.py'} !"
                )
            )
    VERSION = VERSION.group("version")  # type: ignore
    AUTHOR = AUTHOR.group("author")  # type: ignore
    AUTHOR_EMAIL = AUTHOR_EMAIL.group("email")  # type: ignore

with open(PACKAGE_DIR / "requirements.txt", "r") as handle:
    BASE = [
        f"{_.strip()}"
        for _ in handle.readlines()
        if not _.startswith("#") and "git+" not in _
    ]

with open(PACKAGE_DIR / "requirements_dev.txt", "r") as handle:
    DEV = [
        f"{_.strip()}"
        for _ in handle.readlines()
        if not _.startswith("#") and "git+" not in _
    ]

setup(
    name="dic2owl",
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url="https://github.com/emmo-repo/CIF-ontology",
    description="Ontologize CIF dictionaries (`.dic`) using OWL.",
    long_description=(PACKAGE_DIR / "README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=BASE,
    extras_require={"dev": DEV},
    entry_points={
        "console_scripts": ["dic2owl = dic2owl.cli:main"],
    },
    keywords="crystallography ontology materials",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics",
    ],
)
