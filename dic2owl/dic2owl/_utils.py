"""Utility functions, classes, and variables for use in dic2owl."""
from contextlib import redirect_stderr
from os import devnull as DEVNULL

# Remove the print statement concerning 'owlready2_optimized'
# when importing owlready2 (which is imported also in ontopy).
with open(DEVNULL, "w", encoding="utf8") as handle:
    with redirect_stderr(handle):
        from owlready2 import locstr


def lang_en(string: str) -> locstr:
    """Converted to an English-localized string.

    Parameters:
        string: The string to be converted.

    Returns:
        An English-localized string. `locstr` is a `str`-based type.

    """
    return locstr(string, lang="en")


class MissingAnnotationError(Exception):
    """Raised when using a CIF dictionary annotation not defined in CIF-DDL."""
