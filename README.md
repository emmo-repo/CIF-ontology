[![CI tests](https://github.com/emmo-repo/CIF-ontology/workflows/CI/badge.svg)](https://github.com/emmo-repo/CIF-ontology/actions/)
[![DOI](https://zenodo.org/badge/272473769.svg)](https://zenodo.org/badge/latestdoi/272473769)


# CIF ontology

A crystallography domain ontology based on [EMMO][1] and the [CIF core][2] dictionary.
It is implemented as a formal language.

## Status

- [ ] Proposal
- [X] Accepted, under development
- [ ] Official

This ontology is work-in-progress (WIP).
It is part of the overall process of developing a domain ontology for crystallography.

## Imported Ontologies

This ontology builds on top of EMMO.
See the following table for version compatibilies:

| Imported Ontologies | Version           |
| ------------------- | ----------------- |
| emmo-inferred       | 1.0.0-beta        |

## Generator tool (`dic2owl`)

This repository contains both ontologies (under [`/ontology`](ontology)) and the `dic2owl` generator tool (under [`/dic2owl`](dic2owl)), written in Python.

Go to the [README](dic2owl/README.md) of `dic2owl` to read more about the generator tool.

## Obtaining CIF-ontology

This ontology build on EMMO-1.0.0-beta.
The correct path to the inferred verion 'emmo-inferred' is specified in the catalog file, [`catalog-v001.xml`](ontology/catalog-v001.xml).

The domain ontology is obtained with:

```console
git clone https://github.com/emmo-repo/CIF-ontology.git
```

When opening [cif.ttl](https://raw.githubusercontent.com/emmo-repo/CIF-ontology/main/ontology/cif.ttl) in Protégé, the correct version of emmo-inferred will be downloaded and imported.

In EMMO-python correct import is obtained with

```python
from emmo import get_ontology

# Loading crystallography from local repository
cif_onto = get_ontology('/path/to/cif.ttl').load(url_from_catalog=True)

# Loading crystallography from web
cif_onto = get_ontology('https://raw.githubusercontent.com/emmo-repo/CIF-ontology/main/ontology/cif.ttl').load()
```

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

### Projects

- Demystify ontologies - Internal project at [SINTEF](www.sintef.no)
- [MarketPlace](https://www.the-marketplace-project.eu/);
  Grant Agreement No: 760173
  <img src="https://www.the-marketplace-project.eu/content/dam/iwm/the-marketplace-project/images/MARKETPLACE_LOGO_300dpi.png" width="120">
- [OntoTrans](https://ontotrans.eu/);
  Grant Agreement No: 862136
  <img src="https://ontotrans.eu/wp-content/uploads/2020/05/ot_logo_rosa_gro%C3%9F.svg" height="50">
- [BIG-MAP](https://www.big-map.eu/);
  Grant Agreement No: 957189
  <img src="https://avatars1.githubusercontent.com/u/72801303?s=200&v=4" height="50">

License
-------

The CIF ontology is released under the [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/legalcode) license (CC BY 4.0).
See also the [LICENSE](LICENSE) file.

[1]: https://github.com/emmo-repo/EMMO
[2]: https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/index.html
