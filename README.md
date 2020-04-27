[![pipeline](https://gitlab.cc-asp.fraunhofer.de/ontology/domains/crystallography/badges/master/pipeline.svg)](https://gitlab.cc-asp.fraunhofer.de/ontology/domains/crystallography/pipelines/latest)


Crystallography
===============
A toplevel crystallography domain ontology based on [EMMO][1] and the
[CIF core][2] dictionary. It is implemented as a formal language.


Imported ontologies
-------------------
This ontology builds on top of EMMO. See the following table for version
compatibilies:

| Imported ontologies | Version           |
| ------------------- | ----------------- |
| EMMO                | marketplace-1.0.1 |


Obtaining crystallography
-------------------------
This repository now include the correct version of EMMO as a git submodule.
Hence, use the following command when cloning this repository:

    git clone --recurse-submodules --shallow-submodules git@gitlab.cc-asp.fraunhofer.de:ontology/domains/crystallography.git


Attributions and credits
------------------------

### Authors
- Jesper Friis, SINTEF
- Francesca Lønstad Bleken, SINTEF
- Joana Francisco Morgado, Fraunhofer IWM
- Casper Welzel Andersen, EPFL

### Projects
- [MarketPlace](https://www.the-marketplace-project.eu/);
  Grant Agreement No: 760173
  <img src="https://www.the-marketplace-project.eu/content/dam/iwm/the-marketplace-project/images/MARKETPLACE_LOGO_300dpi.png" width="120">


License
-------
The crystallography domain ontology is released under the [Creative
Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/legalcode) license (CC BY 4.0).


[1]: https://github.com/emmo-repo/EMMO
[2]: https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/index.html
