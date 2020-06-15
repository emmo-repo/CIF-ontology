[![CI tests](https://github.com/emmo-repo/domain-crystallography/workflows/CI%20tests/badge.svg)](https://github.com/emmo-repo/domain-crystallography/actions/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)


domain-crystallography
======================
A crystallography domain ontology based on [EMMO][1] and the [CIF
core][2] dictionary. It is implemented as a formal language.


Status
------
- [ ] Proposal
- [X] accepted, under development
- [ ] official

This domain ontology is work-in-progress (WIP), it is in the process
of being accepted as a task group by the EMMC.

* Application submitted: 15 June 2020
* Application accepted on: TBD


Imported Ontologies
-------------------
This ontology builds on top of EMMO. See the following table for version
compatibilies:

| Imported Ontologies | Version           |
| ------------------- | ----------------- |
| EMMO                | marketplace-1.0.1 |


Obtaining domain-crystallography
--------------------------------
For faster access, this repository now include the correct version of
EMMO as a git submodule.  Hence, use the following command when
cloning this repository:

    git clone --recurse-submodules --shallow-submodules git@github.com:emmo-repo/domain-crystallography.git


Attributions and credits
------------------------

### Contributors
- Jesper Friis, SINTEF
- Francesca Lønstad Bleken, SINTEF
- Joana Francisco Morgado, Fraunhofer IWM
- Casper Welzel Andersen, EPFL

### Projects
- Demystify ontologies - Internal project at [SINTEF](www.sintef.no)
- [MarketPlace](https://www.the-marketplace-project.eu/);
  Grant Agreement No: 760173
  <img src="https://www.the-marketplace-project.eu/content/dam/iwm/the-marketplace-project/images/MARKETPLACE_LOGO_300dpi.png" width="120">


License
-------
The crystallography domain ontology is released under the [Creative
Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/legalcode) license (CC BY 4.0).


[1]: https://github.com/emmo-repo/EMMO
[2]: https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/index.html
