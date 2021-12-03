"""Test the `dic2owl.dic2owl.Generator` class."""
# pylint: disable=redefined-outer-name,import-outside-toplevel
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import Callable, List, Optional

    from dic2owl import Generator


@pytest.fixture(scope="session")
def sample_generator_comments() -> "List[str]":
    """The comments to be used for the `sample_generator` fixture."""
    return ["This is a test."]


@pytest.fixture
def sample_generator(
    base_iri: str, cif_dic_path: Path, sample_generator_comments: "List[str]"
) -> "Callable[[Optional[List[str]]], Generator]":
    """Create a generator similar to what is tested in
    `test_initialization()`."""
    from dic2owl import Generator

    def _sample_generator(comments: "Optional[List[str]]" = None) -> Generator:
        """Create and return a `Generator` with specific list of metadata
        comments. By default, the fixture `sample_generator_comments` is
        used."""
        return Generator(
            dicfile=cif_dic_path,
            base_iri=base_iri,
            comments=sample_generator_comments
            if comments is None
            else comments,
        )

    return _sample_generator


def test_initialization(
    base_iri: str, cif_dic_path: Path, sample_generator_comments: "List[str]"
) -> None:
    """Ensure a newly initialized Generator has intended ontologies and
    properties."""
    from CifFile import CifDic
    from dic2owl import Generator

    cif_dictionary = CifDic(str(cif_dic_path), do_dREL=False)

    generator = Generator(
        dicfile=cif_dic_path,
        base_iri=base_iri,
        comments=sample_generator_comments,
    )

    assert generator
    assert generator.dic.WriteOut() == cif_dictionary.WriteOut()
    assert generator.ddl
    assert generator.ddl in generator.onto.imported_ontologies
    assert generator.comments == sample_generator_comments


def test_generate(
    cif_ttl: str,
    create_location_free_ttl: "Callable[[Path], str]",
    sample_generator: "Callable[[Optional[List[str]]], Generator]",
    sample_generator_comments: "List[str]",
) -> None:
    """Test the `generate()` method."""
    from tempfile import NamedTemporaryFile

    generator = sample_generator(None)
    generated_ontology = generator.generate()

    for comment in sample_generator_comments:
        assert comment in generated_ontology.metadata.comment
    assert (
        f"Generated with dic2owl from {generator.dicfile}"
        in generated_ontology.metadata.comment
    )

    generated_ontology = sample_generator([]).generate()

    with NamedTemporaryFile() as output_turtle:
        generated_ontology.save(output_turtle.name, format="turtle")

        generated_ttl = create_location_free_ttl(Path(output_turtle.name))

        assert generated_ttl == cif_ttl
