#!/usr/bin/env python
"""Python script for generating an ontology corresponding to a CIF dictionary.
"""
import os
import types
import textwrap
import urllib.request

from emmo import World
import owlready2
from owlready2 import locstr

from CifFile import CifDic


def en(s):
    """Returns `s` converted to a localised string in english."""
    return locstr(s, lang='en')


class Generator:
    """Class for generating CIF ontology from a CIF dictionary.

    Parameters:
    dicfile : string
        File name of CIF dictionary to generate an ontology for.
    base_iri : string
        Base IRI of the generated ontology.
    cif_top : string
        URI or file name of the cif_top ontology that will be imported.
    """
    def __init__(self, dicfile, base_iri, cif_top='cif_top.ttl'):
        self.cd = CifDic(dicfile, do_dREL=False)
        self.cif_top = cif_top
        self.categories = set()

        # Load cif_top ontology
        self.world = World()
        self.top = self.world.get_ontology(cif_top).load()
        self.top.sync_python_names()

        # Create new ontology
        self.onto = self.world.get_ontology(base_iri)
        self.onto.imported_ontologies.append(self.top)

    def generate(self):
        """Generate ontology for the CIF dictionary."""
        # Add categories first so they are available when we add data items.
        # A category seems to be characterised by having a _definition.scope
        # attribute.
        for item in self.cd:
            if '_definition.scope' in item:
                self._add_category(item)

        # Add data items
        for item in self.cd:
            if '_definition.scope' not in item:
                self._add_data_value(item)

        return self.onto

    def _add_category(self, item):
        """Add category."""
        if item in self.categories:
            return
        self.categories.add(item)

        name = item['_definition.id']
        descr = item.get('_description.text')
        lname = '_' + name.lstrip('_').lower()
        with self.onto:
            if item.get('_definition.class'):
                table = types.new_class(lname + '_TABLE', (self.top.TABLE, ))
                table.prefLabel.append(en(table.name.lstrip('_')))
                row = types.new_class(lname + '_ROW', (self.top.ROW, ))
                row.prefLabel.append(en(row.name.lstrip('_')))
                cat = types.new_class(name, (self.top.CATEGORY, ))
                cat.prefLabel.append(en(cat.name.lstrip('_')))
                if descr:
                    cat.comment.append(en(textwrap.dedent(descr)))
                table.is_a.append(self.top.hasSpatialDirectPart.some(row))
                table.is_a.append(self.top.hasSpatialPart.only(cat))
            else:
                print('** ignoring category:', name)

    def _add_data_value(self, item):
        """Add data item."""
        name = item['_definition.id']
        descr = item.get('_description.text')
        units = item.get('_units.code')
        aliases = item.get('_alias.definition_id')
        examples = item.get('_description_example.detail', [])
        examples.extend(item.get('_description_example.case', []))
        dimension = item.get('_type.dimension')

        container_name = item.get('_type.container', 'Single')
        type_name = item.get('_type.contents', 'Text')
        category_name = item['_name.category_id'].upper()
        row_name = '_%s_ROW' % item['_name.category_id']

        container = self.onto[container_name]
        _type = self.onto[type_name]
        category = self.onto[category_name]

        with self.onto:

            if container_name == 'Single':
                e = types.new_class(name, (_type, ))
            else:
                e = types.new_class(name, (container, ))
                if container_name == 'List':
                    e.is_a.append(self.top.hasSpatialDirectPart.some(_type))
                else:
                    e.is_a.append(self.top.hasSpatialPart.some(_type))

            if category.disjoint_unions:
                category.disjoint_unions[0].append(e)
            else:
                category.disjoint_unions.append([e])
            e.prefLabel.append(en(name.lstrip('_')))

            # Hmm, _name is already used internally by owlready2.Ontology
            # so `e._name.append(name)` won't work.
            # We have to add the tripple the hard way...
            o, d = owlready2.to_literal(name)  # not localised
            self.onto._set_data_triple_spod(
                s=e.storid,
                p=self.onto.world._props['_name'].storid,
                o=o, d=d)

            if aliases:
                e.altLabel.extend(en(a) for a in aliases)
            if descr:
                e.comment.append(en(textwrap.dedent(descr)))
            if examples:
                e.example.extend(en(textwrap.dedent(ex)) for ex in examples)
            if units:
                e._unit.append(units)  # not localised
            if dimension:
                e._dimension.append(dimension)  # not localised
            if row_name in self.onto:
                row = self.onto[row_name]
                row.is_a.append(self.top.hasSpatialDirectPart.max(1, e))
            else:
                print('** no row:', name)


def main():
    base_iri = 'http://emmo.info/domain-crystallography/cif_core#'

    # Download the CIF dictionaries to current directory
    baseurl = 'https://raw.githubusercontent.com/COMCIFS/cif_core/master/'
    for dic in 'ddl.dic', 'cif_core.dic', 'templ_attr.cif', 'templ_enum.cif':
        if not os.path.exists(dic):
            print('downloading', dic)
            urllib.request.urlretrieve(baseurl + dic, dic)

    gen = Generator(dicfile='cif_core.dic', base_iri=base_iri)
    onto = gen.generate()

    # Annotate ontology
    onto.sync_attributes()
    onto.set_version(version='0.0.1')
    onto.metadata.abstract = (
        'CIF core ontology generated from the CIF core definitions at '
        'https://raw.githubusercontent.com/COMCIFS/cif_core/master/'
    )

    onto.save('cif_core.ttl', overwrite=True)

    return gen  # XXX - just for debugging


if __name__ == '__main__':
    #main()

    # for debugging and testing...
    self = gen = main()
    top = self.top
    onto = self.onto
    cd = self.cd
    sid = cd['space_group_symop.id']
    s = cd['SPACE_GROUP_SYMOP']
