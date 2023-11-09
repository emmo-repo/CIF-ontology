"""
# Generate ontology

Python script for generating an ontology corresponding to a CIF dictionary.
"""
from contextlib import redirect_stderr
from os import devnull as DEVNULL
from pathlib import Path
import types
from typing import TYPE_CHECKING
import urllib.request

from CifFile import CifDic

# Remove the print statement concerning 'owlready2_optimized'
# when importing owlready2 (which is imported also in ontopy).
with open(DEVNULL, "w") as handle:  # pylint: disable=unspecified-encoding
    with redirect_stderr(handle):
        from ontopy import World

        from owlready2 import locstr


if TYPE_CHECKING:
    from _typeshed import StrPath
    from typing import Any, Sequence, Set, Union

    from ontopy.ontology import Ontology

# Workaround for flaw in EMMO-Python
# To be removed when EMMO-Python doesn't requires ontologies to import SKOS
import ontopy.ontology  # pylint: disable=wrong-import-position

ontopy.ontology.DEFAULT_LABEL_ANNOTATIONS = [
    "http://www.w3.org/2000/01/rdf-schema#label",
]

ONTOLOGY_DIR = (
    Path(__file__).resolve().parent.parent.parent.joinpath("ontology")
)
"""The absolute, normalized path to the `ontology` directory in this
repository"""


def lang_en(string: str) -> locstr:
    """Converted to an English-localized string.

    Parameters:
        string: The string to be converted.

    Returns:
        An English-localized string. `locstr` is a `str`-based type.

    """
    return locstr(string, lang="en")


class MissingAnnotationError(Exception):
    """Raised when using a cif-dictionary annotation not defined in ddl"""


# pylint: disable=too-few-public-methods,too-many-instance-attributes
class Generator:
    """Class for generating CIF ontology from a CIF dictionary.

    Parameters:
        dicfile: File name of CIF dictionary to generate an ontology for.
        base_iri: Base IRI of the generated ontology.
        comments: Sequence of comments to add to the ontology itself.
        local_ddl: If `True`, the CIF DDL ontology will be loaded from the
            local repository.

    """

    cif_ddl: str

    def __init__(
        self,
        dicfile: "StrPath",
        base_iri: str,
        comments: "Sequence[str]" = (),
        local_ddl: bool = False,
    ) -> None:
        self.cif_ddl = (
            (ONTOLOGY_DIR / "cif-ddl.ttl").as_uri()
            if local_ddl
            else "https://raw.githubusercontent.com/emmo-repo/CIF-ontology/main/"
            "ontology/cif-ddl.ttl"
        )

        self.dicfile = dicfile
        self.dic = CifDic(str(self.dicfile), do_dREL=False)
        self.comments = comments

        # Create new ontology
        self.world = World()
        self.onto = self.world.get_ontology(base_iri)

        # Load cif-ddl ontology and append it to imported ontologies
        self.ddl = self.world.get_ontology(self.cif_ddl).load()
        self.ddl.sync_python_names()
        self.onto.imported_ontologies.append(self.ddl)

        # Load Dublin core for metadata and append it to imported ontologies
        # dcterms = self.world.get_ontology('http://purl.org/dc/terms/').load()
        # self.onto.imported_ontologies.append(dcterms)

        self.items: "Set[dict]" = set()

    def generate(self) -> "Ontology":
        """Generate ontology for the CIF dictionary.

        Returns:
            The generated ontology.

        """
        for item in self.dic:
            self._add_item(item)

        self._add_metadata()
        self.onto.sync_attributes()
        return self.onto

    def _add_item(self, item) -> None:
        """Add dic block `item` to the generated ontology."""
        if "_definition.scope" in item and "_definition.id" in item:
            self._add_category(item)
        else:
            self._add_data_value(item)

    def _add_top(self, item) -> None:
        """Add the top class of the generated ontology.

        Parameters:
            item: Item to be added to the list of categories.

        """
        with self.onto:
            top = types.new_class(
                item["_dictionary.title"], (self.ddl.DictionaryDefinedItem,)
            )
        self._add_annotations(top, item)

    def _add_category(self, item: dict) -> None:
        """Add category.

        Parameters:
            item: Item to be added to the list of categories.

        """
        if item in self.items:
            return
        self.items.add(item)

        if "_definition.id" not in item:
            self._add_top(item)
        else:
            name = item["_definition.id"]
            parent_name = item["_name.category_id"]
            parent_item = self.dic[parent_name]
            if parent_item not in self.items:
                self._add_category(parent_item)

            with self.onto:
                cls = types.new_class(name, (self.onto[parent_name],))
            self._add_annotations(cls, item)

    def _add_data_value(self, item: dict) -> None:
        """Add data item.

        Parameters:
            item: Item to be added as a datum.

        """
        if item in self.items:
            return
        self.items.add(item)

        name = item["_definition.id"]

        parents = []
        parent_name1 = item["_name.category_id"]
        parent = self.dic[parent_name1]
        parent_name = parent["_definition.id"]
        self._add_item(parent)
        parents.append(self.onto[parent_name])

        for ddl_name, value in item.items():
            if ddl_name.startswith("_type."):
                if ddl_name == "_type.dimension":
                    pass
                elif value == "Implied":
                    pass
                else:
                    parents.append(self.ddl[value])

        with self.onto:
            cls = types.new_class(name, tuple(parents))

        self._add_annotations(cls, item)

    def _add_annotations(self, cls: "Any", item: dict) -> None:
        """Add annotations for dic item `item` to generated ontology
        class `cls`.

        Parameters:
            cls: Generated ontology class to which the annotations should
                be added.
            item: Dic item with annotation info.

        """
        for annotation_name, value in item.items():
            # Add new annotation to generated ontology
            if annotation_name not in self.ddl:
                raise MissingAnnotationError(annotation_name)

            # Assign annotation
            annot = getattr(cls, annotation_name)
            annot.append(lang_en(value))

    def _add_metadata(self) -> None:
        """Adds metadata to the generated ontology."""
        for comment in self.comments:
            self.onto.metadata.comment.append(comment)
        self.onto.metadata.comment.append(
            f"Generated with dic2owl from {self.dicfile}"
        )


def main(
    dicfile: "Union[str, Path]",
    ttlfile: "Union[str, Path]",
    local_ontologies: bool = False,
) -> Generator:
    """Main function for ontology generation.

    Parameters:
        dicfile: Absolute or relative path to the `.dic`-file to be converted
            to an ontology.
            This can be either a local path or a URL path.
        ttlfile: Absolute or relative path to the Turtle (`.ttl`) file to
            be created from the `dicfile`.
            The Turtle file contains the generated ontology in OWL.
            This **must** be a local path.

            !!! important
                The file will be overwritten if it already exists.
        local_ontologies: If `True`, the ontologies used to generate the
            ontology will be loaded from the local repository.
            If `False`, the ontologies will be loaded from the latest commit in
            the `main` branch on GitHub.

    Returns:
        The setup ontology generator class. This is mainly returned for
        debugging reasons.

    """
    base_iri = "http://emmo.info/CIF-ontology/ontology/cif_core#"

    dicfile = dicfile if isinstance(dicfile, str) else str(dicfile.resolve())

    # Download the CIF dictionaries to current directory
    baseurl = "https://raw.githubusercontent.com/COMCIFS/cif_core/master/"
    for dic in ("ddl.dic", "templ_attr.cif", "templ_enum.cif", dicfile):
        if not Path(dic).resolve().exists():
            print("downloading", dic)
            # Since `baseurl` is used, the retrieved URL will never be a
            # `file://` or similar.
            urllib.request.urlretrieve(baseurl + dic, dic)  # nosec

    gen = Generator(
        dicfile=dicfile, base_iri=base_iri, local_ddl=local_ontologies
    )
    onto = gen.generate()
    onto.save(
        ttlfile if isinstance(ttlfile, str) else str(ttlfile.resolve()),
        overwrite=True,
    )

    return gen
