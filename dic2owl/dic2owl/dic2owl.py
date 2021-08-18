#!/usr/bin/env python
"""
# Generate ontology

Python script for generating an ontology corresponding to a CIF dictionary.
"""
from contextlib import redirect_stderr
from os import devnull as DEVNULL
from pathlib import Path

# import textwrap
# import types
from typing import Union
import urllib.request

# Remove the print statement concerning 'owlready2_optimized'
# when importing owlready2 (which is imported also in emmo).
with open(DEVNULL, "w") as handle:
    with redirect_stderr(handle):
        from emmo import World
        from emmo.ontology import Ontology

        # import owlready2
        from owlready2 import locstr

from CifFile import CifDic


# Workaround for EMMO-Python
# Make sure that we can load cif-ddl.ttl which doesn't import SKOS
import emmo.ontology

emmo.ontology.DEFAULT_LABEL_ANNOTATIONS = [
    "http://www.w3.org/2000/01/rdf-schema#label",
]

"""Return the absolute, normalized path to the `ontology` directory in this repository"""
ONTOLOGY_DIR = Path(__file__).resolve().parent.parent.parent.joinpath("ontology")


def en(string: str) -> locstr:
    """Converted to an English-localized string.

    Parameters:
        string: The string to be converted.

    Returns:
        An English-localized string. `locstr` is a `str`-based type.

    """
    return locstr(string, lang="en")


class Generator:
    """Class for generating CIF ontology from a CIF dictionary.

    Parameters:
        dicfile (str): File name of CIF dictionary to generate an ontology for.
        base_iri (str): Base IRI of the generated ontology.

    """

    def __init__(
        self,
        dicfile: str,
        base_iri: str,
    ) -> None:
        self.dic = CifDic(dicfile, do_dREL=False)

        # Load cif-ddl ontology
        self.world = World()
        cif_ddl = ONTOLOGY_DIR / "cif-ddl.ttl"
        self.ddl = self.world.get_ontology(str(cif_ddl)).load()
        self.ddl.sync_python_names()

        # Create new ontology
        self.onto = self.world.get_ontology(base_iri)
        self.onto.imported_ontologies.append(self.ddl)

        self.categories = set()

    def generate(self) -> Ontology:
        """Generate ontology for the CIF dictionary.

        Returns:
            The generated ontology.

        """
        self._add_dic_top()

        for item in self.dic:
            if "_definition.scope" in item and "_definition.id" in item:
                self._add_category(item)
            else:
                self._add_data_value(item)
        return self.onto

    def _add_dic_top(self) -> None:
        """Add the top class of the generated ontology."""
        pass

    def _add_category(self, item: dict) -> None:
        """Add category.

        Parameters:
            item: Item to be added to the list of categories.

        """
        if item in self.categories:
            return
        self.categories.add(item)

        print("*** category", item)
        name = item["_definition.id"]
        parent_name = item["_name.category_id"]
        parent_item = self.dic[parent_name]
        # if parent_item not in self.categories:
        #    self._add_category(parent_item)
        #
        # with self.onto:
        #
        #    cat = types.new_class(name, (self.onto[parent_name], ))

    #        name = item["_definition.id"]
    #        descr = item.get("_description.text")
    #        lname = "_" + name.lstrip("_").lower()
    #        with self.onto:
    #            if item.get("_definition.class"):
    #                loop = types.new_class(lname + "_LOOP", (self.top.LOOP,))
    #                loop.prefLabel.append(en(loop.name.lstrip("_")))
    #                packet = types.new_class(lname + "_PACKET", (self.top.PACKET,))
    #                packet.prefLabel.append(en(packet.name.lstrip("_")))
    #                cat = types.new_class(name, (self.top.CATEGORY,))
    #                cat.prefLabel.append(en(cat.name.lstrip("_")))
    #                if descr:
    #                    cat.comment.append(en(textwrap.dedent(descr)))
    #                loop.is_a.append(self.top.hasSpatialDirectPart.some(packet))
    #                loop.is_a.append(self.top.hasSpatialPart.only(cat))
    #            else:
    #                print("** ignoring category:", name)

    def _add_data_value(self, item: dict) -> None:
        """Add data item.

        Parameters:
            item: Item to be added as a datum.

        """
        realname = item["_definition.id"]


#        name = realname.replace(".", "_")
#        descr = item.get("_description.text")
#        units = item.get("_units.code")
#        aliases = item.get("_alias.definition_id")
#        examples = item.get("_description_example.detail", [])
#        examples.extend(item.get("_description_example.case", []))
#        dimension = item.get("_type.dimension")
#
#        container_name = item.get("_type.container", "Single")
#        datatype_name = item.get("_type.contents", "Text")
#        category_name = item["_name.category_id"].upper()
#        packet_name = "_%s_PACKET" % item["_name.category_id"]
#
#        container = self.onto[container_name]
#        datatype = self.onto[datatype_name]
#        category = self.onto[category_name]
#
#        with self.onto:
#
#            if container_name == "Single":
#                e = types.new_class(name, (datatype,))
#            elif container_name in ("Matrix", "Array"):
#                dims = dimension.strip("[]")
#                if dims:
#                    subarr = self.subarray(dims.split(","), datatype, container_name)
#                    e = types.new_class(name, (subarr,))
#                else:
#                    e = types.new_class(name, (datatype,))
#            else:
#                e = types.new_class(name, (container,))
#                if container_name == "List":
#                    e.is_a.append(self.top.hasSpatialDirectPart.some(datatype))
#                else:
#                    e.is_a.append(self.top.hasSpatialPart.some(datatype))
#
#            if category.disjoint_unions:
#                category.disjoint_unions[0].append(e)
#            else:
#                category.disjoint_unions.append([e])
#            e.prefLabel.append(en(realname.lstrip("_")))
#            if name != realname:
#                e.altLabel.append(en(name.lstrip("_")))
#
#            # Hmm, _name is already used internally by owlready2.Ontology
#            # so `e._name.append(name)` won't work.
#            # We have to add the tripple the hard way...
#            o, d = owlready2.to_literal(realname)  # not localised
#            self.onto._set_data_triple_spod(
#                s=e.storid, p=self.onto.world._props["_name"].storid, o=o, d=d
#            )
#
#            if aliases:
#                e.altLabel.extend(en(a) for a in aliases)
#            if descr:
#                e.comment.append(en(textwrap.dedent(descr)))
#            if examples:
#                e.example.extend(en(textwrap.dedent(ex)) for ex in examples)
#            if units:
#                e._unit.append(units)  # not localised
#            if dimension:
#                e._dimension.append(dimension)  # not localised
#            if datatype:
#                e._datatype.append(datatype)  # not localised
#            if packet_name in self.onto:
#                packet = self.onto[packet_name]
#                packet.is_a.append(self.top.hasSpatialDirectPart.max(1, e))
#            else:
#                print("** no packet:", realname)

#    def subarray(self, dimensions, datatype, container_name):
#        """Returns a reference to an array or matrix corresponding to:
#        - dimensions: list of dimension values
#        - typename: type of elements
#        - container_name: "Array" or "Matrix"
#        If it does not already exists, the subarray is created.  All
#        its spatial direct parts are also generated recursively.
#        """
#        if not dimensions or not dimensions[0]:
#            return datatype
#        name = "Shape" + "x".join(dimensions) + datatype.name + container_name
#        if name not in self.onto:
#            e = types.new_class(name, (self.onto[container_name],))
#            d = int(dimensions.pop(0))
#            e.is_a.append(
#                self.top.hasSpatialDirectPart.exactly(
#                    d, self.subarray(dimensions, datatype, container_name)
#                )
#            )
#        return self.onto[name]


def main(dicfile: Union[str, Path], ttlfile: Union[str, Path]) -> Generator:
    """Main function for ontology generation.

    Parameters:
        dicfile: Absolute or relative path to the `.dic`-file to be converted to an ontology.
            This can be either a local path or a URL path.
        ttlfile: Absolute or relative path to the Turtle (`.ttl`) file to be created from the
            `dicfile`. The Turtle file contains the generated ontology in OWL. This **must** be a
            local path.

            !!! important
                The file will be overwritten if it already exists.

    Returns:
        The setup ontology generator class. This is mainly returned for debugging reasons.

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

    #    # Annotate ontology
    #    onto.sync_attributes()
    #    onto.set_version(version="0.0.1")
    #    onto.metadata.abstract = (
    #        "CIF core ontology generated from the CIF core definitions at "
    #        "https://raw.githubusercontent.com/COMCIFS/cif_core/master/"
    #    )
    #
    #    if ttlfile is None:
    #        ttlfile = Path(dicfile).name[: -len(Path(dicfile).suffix)] + ".ttl"

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
    # sid = cd["space_group_symop.id"]
    # s = cd["SPACE_GROUP_SYMOP"]
