# Convert CIF dictionaries to OWL Turtle files - dic2owl

This Python package presents a CLI `dic2owl` that can convert a CIF dictionary to an OWL Turtle file using the schema developed in the EMMO-Crystallography EMMC Task Group.

## Ontologization schema

The early schema development can be found in the [#16](https://github.com/emmo-repo/CIF-ontology/issues/16) issue.

It has been developed by the EMMO-Crystallography EMMC Task Group, which consists of:

- Casper Welzel Andersen, EPFL
- Jesper Friis, SINTEF
- James Hester
- Saulius Grazulis
- Rickard Armiento
- Emanuele Ghedini
- Francesca Lønstad Bleken, SINTEF
- Joana Morgado, Fraunhofer IWM
- Stuart Chalk

## Related work and dependencies

This package relies on the [PyCIFRW](https://bitbucket.org/jamesrhester/pycifrw) package developed by James Hester to parse CIF (`.cif`) and CIF dictionary (`.dic`) files.

## Author

Jesper Friis, SINTEF

Casper Welzel Andersen, EPFL
James Hester
