#!/usr/bin/env python
"""Python script for generating an ontology corresponding to a CIF dictionary.
"""
import os
import types
import textwrap
import urllib.request

from emmo import World
from CifFile import ReadCif


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
        self.cf = ReadCif(dicfile)
        self.cif_top = cif_top
        self.categories = set()

        # Load cif_top ontology
        self.world = World()
        self.top = self.world.get_ontology(cif_top).load()
        self.top.sync_python_names()

        # Create new ontology
        self.onto = self.world.get_ontology(base_iri)
        self.onto.imported_ontologies.append(self.top)

    def generate(self, dics=None):
        """Generate ontology for the given sequence of CIF dictionary names.
        By default the dictionaries are inferred from the `dicfile`."""
        if dics is None:
            dics = self.cf.keys()
        for dicname in dics:
            self._generate_dic(dicname)
        return self.onto

    def _generate_dic(self, dicname):
        """Generate ontology for dictionary `name`."""
        # Add categories first so they are available when we add data items.
        # A category seems to be characterised by having a _definition.scope
        # attribute.
        for item in self.cf.get_children(dicname):
            if '_definition.scope' in item:
                self._add_category(item)

        # Add data items
        for item in self.cf.get_children(dicname):
            if '_definition.scope' not in item:
                self._add_data_item(item)

    def _add_category(self, item):
        """Add category."""
        if item in self.categories:
            return
        self.categories.add(item)

        name = item['_definition.id']
        descr = item.get('_description.text')
        lname = '_' + name.lstrip('_').lower()
        with self.onto:
            if item.get('_definition.class') in ('Loop', 'Set'):
                table = types.new_class(lname + '_TABLE', (self.top.TABLE, ))
                table.prefLabel.append(table.name.lstrip('_'))
                row = types.new_class(lname + '_ROW', (self.top.ROW, ))
                row.prefLabel.append(row.name.lstrip('_'))
                cat = types.new_class(name, (self.top.CATEGORY, ))
                cat.prefLabel.append(cat.name.lstrip('_'))
                if descr:
                    cat.comment.append(textwrap.dedent(descr))
                table.is_a.append(self.top.hasSpatialDirectPart.some(row))
                table.is_a.append(self.top.hasSpatialPart.only(cat))
            else:
                print('** ignoring category:', name)

    def _add_data_item(self, item):
        """Add data item."""
        name = item['_definition.id']
        descr = item.get('_description.text')
        units = item.get('_units.code')
        aliases = item.get('_alias.definition_id')
        category_name = item['_name.category_id'].upper()
        row_name = '_%s_ROW' % item['_name.category_id']
        if category_name in self.onto:
            category = self.onto[category_name]
            with self.onto:
                # FIXME - inherit from type instead of category
                e = types.new_class(name, (category, ))
                if category.disjoint_unions:
                    category.disjoint_unions[0].append(e)
                else:
                    category.disjoint_unions.append([e])
                e.prefLabel.append(name.lstrip('_'))
                if aliases:
                    e.altLabel.extend(aliases)
                if descr:
                    e.comment.append(textwrap.dedent(descr))
                if units:
                    e._unit.append(units)
                if row_name in self.onto:
                    row = self.onto[row_name]
                    row.is_a.append(self.top.hasSpatialDirectPart.max(1, e))
                else:
                    print('** no row:', name)
        else:
            print('** no category:', name)


def main():
    # Download the CIF dictionaries to current directory
    baseurl = 'https://raw.githubusercontent.com/COMCIFS/cif_core/master/'
    for dic in 'ddl.dic', 'cif_core.dic', 'templ_attr.cif', 'templ_enum.cif':
        if not os.path.exists(dic):
            print('downloading', dic)
            urllib.request.urlretrieve(baseurl + dic, dic)

    gen = Generator(dicfile='cif_core.dic',
                    base_iri='http://emmo.info/crystallography/cif_core#')
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
    items = self.cf.get_children('core_dic')
    sid = items['space_group_symop.id']
    s = items['SPACE_GROUP_SYMOP']
