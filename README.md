# CIF Ontology

[![CI tests](https://github.com/emmo-repo/CIF-ontology/workflows/CI/badge.svg)](https://github.com/emmo-repo/CIF-ontology/actions/)
[![DOI](https://zenodo.org/badge/272473769.svg)](https://zenodo.org/badge/latestdoi/272473769)

This repository provides an ontologisation of the CIF Dictionary Definition Language ([DDLm](https://www.iucr.org/resources/cif/ddl/ddlm)) and the [CIF core dictionary](https://www.iucr.org/resources/cif/dictionaries/cif_core) by IUCr.
The development version of these dictionaries can be found in the [COMCIFS/cif_core](https://github.com/COMCIFS/cif_core) GitHub repository.

The CIF Ontology has no dependencies to any upper ontology.
But the EMMC crystallography task group is providing an EMMO-based [Crystallography Domain Ontology](https://github.com/emmo-repo/domain-crystallography), which is based on both the CIF Ontology and [EMMO](https://github.com/emmo-repo/EMMO).

## Obtaining CIF-ontology

A table with available releases can be found in [the documentation](https://emmo-repo.github.io/CIF-ontology/).

### Manually generating the cif core ontology

It is also possible to clone this repository and generate the CIF ontology.

First clone this repository with

```console
git clone https://github.com/emmo-repo/CIF-ontology.git
```

and then run the `dic2owl` tool following the instructions in the [dic2owl/README.md](dic2owl/README.md) file.

## Attributions and credits

### Contributors

- Jesper Friis, SINTEF
- James Hester
- Casper Welzel Andersen, EPFL
- Saulius Grazulis
- Rickard Armiento
- Emanuele Ghedini
- Francesca Lønstad Bleken, SINTEF
- Joana Morgado, Fraunhofer IWM
- Stuart Chalk

### Contributing projects

- Demystify ontologies - Internal project at [SINTEF](www.sintef.no)
- [MarketPlace](https://www.the-marketplace-project.eu/);
  Grant Agreement No: 760173
  <!-- markdownlint-disable-next-line MD033 -->
  <img src="https://www.the-marketplace-project.eu/content/dam/iwm/the-marketplace-project/images/MARKETPLACE_LOGO_300dpi.png" width="120">
- [OntoTrans](https://ontotrans.eu/);
  Grant Agreement No: 862136
  <!-- markdownlint-disable-next-line MD033 -->
  <img src="https://ontotrans.eu/wp-content/uploads/2020/05/ot_logo_rosa_gro%C3%9F.svg" height="50">
- [BIG-MAP](https://www.big-map.eu/);
  Grant Agreement No: 957189
  <!-- markdownlint-disable-next-line MD033 -->
  <img src="https://avatars1.githubusercontent.com/u/72801303?s=200&v=4" height="50">

## License

The CIF ontology is released under the [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/legalcode) license (CC BY 4.0).
See also the [LICENSE](LICENSE) file.
