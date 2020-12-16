[![CI tests](https://github.com/emmo-repo/domain-crystallography/workflows/CI%20tests/badge.svg)](https://github.com/emmo-repo/domain-crystallography/actions/)


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
| EMMO                | 1.0.0-alpha2      |


Obtaining domain-crystallography
--------------------------------

This ontology build on EMMO-1.0.0-alpha2. The correct path to 
the inferred verion 'emmo-inferred' is specified in the catalog file, catalog-v001.xml.

The domain ontology is obtained with:

    git clone git@github.com:emmo-repo/domain-crystallography.git

When opening batteryInterface.owl in Protege, the correct version of emmo-inferred will
be downloaded and imported.

In EMMO-python correct import is obatined with 

   get_ontology('crystallography.owl).load(url_from_catalog=True)





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
