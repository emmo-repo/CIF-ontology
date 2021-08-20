#!/usr/bin/env python
"""
# Generate ontology

Python script for generating an ontology corresponding to a CIF dictionary.
"""
from contextlib import redirect_stderr
from os import devnull as DEVNULL
from pathlib import Path

# import textwrap
import types
from typing import Union, Sequence
import urllib.request

from CifFile import CifDic

# Remove the print statement concerning 'owlready2_optimized'
# when importing owlready2 (which is imported also in emmo).
with open(DEVNULL, "w") as handle:
    with redirect_stderr(handle):
        from emmo import World
        from emmo.ontology import Ontology

        from owlready2 import locstr


# Workaround for flaw in EMMO-Python
# To be removed when EMMO-Python doesn't requires ontologies to import SKOS
import emmo.ontology  # noqa: E402
emmo.ontology.DEFAULT_LABEL_ANNOTATIONS = [
    "http://www.w3.org/2000/01/rdf-schema#label",
]

"""The absolute, normalized path to the `ontology` directory in this
repository"""
ONTOLOGY_DIR = Path(__file__).resolve().parent.parent.parent.joinpath(
    "ontology")


def en(string: str) -> locstr:
    """Converted to an English-localized string.

    Parameters:
        string: The string to be converted.

    Returns:
        An English-localized string. `locstr` is a `str`-based type.

    """
    return locstr(string, lang="en")


class MissingAnnotationError(Exception):
    """Raised when using a cif-dictionary annotation not defined in ddl
    """


class Generator:
    """Class for generating CIF ontology from a CIF dictionary.

    Parameters:
        dicfile: File name of CIF dictionary to generate an ontology for.
        base_iri: Base IRI of the generated ontology.
        comments: Sequence of comments to add to the ontology itself.
    """
    # TODO:
    # Should `comments` be replaced with a dict `annotations` for annotating
    # the ontology itself?  If so, we should import Dublin Core.

    def __init__(
            self,
            dicfile: str,
            base_iri: str,
            comments: Sequence[str] = (),
    ) -> None:
        self.dicfile = dicfile
        self.dic = CifDic(dicfile, do_dREL=False)
        self.comments = comments

        # Create new ontology
        self.world = World()
        self.onto = self.world.get_ontology(base_iri)

        # Load cif-ddl ontology and append it to imported ontologies
        cif_ddl = ONTOLOGY_DIR / "cif-ddl.ttl"
        self.ddl = self.world.get_ontology(str(cif_ddl)).load()
        self.ddl.sync_python_names()
        self.onto.imported_ontologies.append(self.ddl)

        # Load Dublin core for metadata and append it to imported ontologies
        #dcterms = self.world.get_ontology('http://purl.org/dc/terms/').load()
        #self.onto.imported_ontologies.append(dcterms)

        self.items = set()

    def generate(self) -> Ontology:
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
                item["_dictionary.title"], (self.ddl.DictionaryDefinedItem, )
            )
        self._add_annotations(top, item)

    def _add_category(self, item) -> None:
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
        parent_name = parent['_definition.id']
        self._add_item(parent)
        parents.append(self.onto[parent_name])

        for ddl_name, value in item.items():
            if ddl_name.startswith('_type.'):
                if ddl_name == '_type.dimension':
                    # TODO - fix special case
                    pass
                elif value == 'Implied':
                    # TODO - fix special case
                    pass
                else:
                    parents.append(self.ddl[value])

        with self.onto:
            cls = types.new_class(name, tuple(parents))

        self._add_annotations(cls, item)

    def _add_annotations(self, cls, item) -> None:
        """Add annotations for dic item `item` to generated on ontology
        class `cls`.

        Parameters:
            cls: Generated ontology class to wich the annotations should
                 be added.
            item: Dic item with annotation info.

        """
        for annotation_name, value in item.items():

            # Add new annotation to generated ontology
            if annotation_name not in self.ddl:
                raise MissingAnnotationError(annotation_name)

            # Assign annotation
            annot = getattr(cls, annotation_name)
            annot.append(en(value))

    def _add_metadata(self):
        """Adds metadata to the generated ontology."""
        # TODO:
        # Is there a way to extract metadata from the dic object like
        # _dictionary_audit.version?
        #onto.set_version(version="XXX")

        for comment in self.comments:
            self.onto.metadata.comment.append(comment)
        self.onto.metadata.comment.append(
            f'Generated with dic2owl from {self.dicfile}')


def main(dicfile: Union[str, Path], ttlfile: Union[str, Path]) -> Generator:
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
            urllib.request.urlretrieve(baseurl + dic, dic)

    gen = Generator(dicfile=dicfile, base_iri=base_iri)
    onto = gen.generate()
    onto.save(
        ttlfile if isinstance(ttlfile, str) else str(ttlfile.resolve()),
        overwrite=True,
    )

    return gen  # XXX - just for debugging


if __name__ == "__main__":
    # main()

    # for debugging and testing...
    self = gen = main("cif_core.dic", "cif_core.ttl")
    dic = self.dic
    ddl = self.ddl
    onto = self.onto
