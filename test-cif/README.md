# Test CIF files

The test CIF files can be divided into two sets:

- Files in the `feature-oriented` set have been manually constructed by adding or removing certain features from existing entries from the Crystallography Open Database.
  They are intended to provide a greater granularity and could potentially be used for test driven development.
  Each test file contains a CIF header comment that describes the CIF/DDLm features that is being covered.
- Files in the `peer-reviewed` set were originally provided as supplementary material of peer-reviewed publications.
  Most of these files have not been changed in any way except for minor syntactic corrections that were required to successfully parse the file (see `the peer-reviewed/download-cifs` script for more details).
