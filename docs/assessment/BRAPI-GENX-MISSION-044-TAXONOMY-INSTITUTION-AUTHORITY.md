# Mission 044 — Taxonomic identity and institutional authority

**Date:** 2026-11-24
**Inspected parent:** `22140a5a3809ff1cbd6570cc412eb6a0528139e2`
**Status:** source-backed candidate documentation; no new normative contract.

## Verified incumbent evidence

The official BrAPI v2.1 `GermplasmNewRequest.yaml` has genus, species, speciesAuthority, subtaxon, taxonIds and instituteCode fields. Official TaxonID adds a source-scoped taxonId. Its GermplasmMCPD fields preserve holding and donor institute semantics. GenX TaxonName, CropSpecies and InstitutionCode candidate records instead have optional strings and no typed links to official Germplasm, WIEWS institutes, external accepted taxonomic names or other GenX taxon objects.

**External reference context, not a newly adopted profile:** Taxonomic Databases Working Group Darwin Core terms at https://dwc.tdwg.org/terms/ distinguish taxonomic name/accepted-name identities. FAO World Information and Early Warning System institutional code documentation at https://www.fao.org/wiews/background/en and MCPD version 2.1 at https://docs.genesys-pgr.org/docs/providers/preparing-mcpd/mcpd-2.1/ establish that an institution code authority exists outside GenX. These sources do not certify any draft identity crosswalk.

## Decision boundaries

- TaxonName: D-238–D-240 remain open (requiredness, synonyms, external authority).
- CropSpecies: D-283–D-285 remain open (requiredness and TaxonName linkage).
- InstitutionCode: D-286–D-288 remain open, including the scientifically questionable proposed institution-to-TaxonName link.

Three RFCs and three module overviews now acknowledge existing official BrAPI taxonomic/institutional fields instead of asserting an absent feature, and remove false claims of current typed links. Three direct-source group descriptions are pinned and tested; the group inventory grows from 23 to **26 reviewed, 130 deferred of 156**. Relative evidence links were checked against the Git tree. Only editorial, checker and test files changed; no official sources, operation paths, registry identities or schema fields were changed.

## Verification

Run `python Scripts/check_genx_group_descriptions.py`, `python Scripts/test_genx_group_descriptions.py`, and the complete hosted static/live and specification generation workflows. Hosted outcomes must be verified before reporting success.
