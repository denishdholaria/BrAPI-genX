# Mission 042 — Evidence-gated core BrAPI overlap: Lists, Crops and People

**Date:** 2026-11-24
**Planned parent commit:** `0c9a132282ae35ee489e18c4857dac1a6a592524` (Mission 041)
**Status:** planned integration commit; hosted verification is not claimed until complete.

## Verified source overlap

The preserved official BrAPI v2.1 sources contain a `/lists` operation, `/commoncropnames` operation and `/people` operation, alongside respective documentation and resource schemas where relevant. GenX RFC-090, RFC-094, and RFC-097 formerly described these capabilities as absent in BrAPI without acknowledging existing official operations.

- RFC-090 now acknowledges official `List` and explains that draft `members` are unconstrained strings, not typed Germplasm/Sample links.
- RFC-094 acknowledges the official multi-crop discovery operation and explains that the distinct proposed record has no typed Germplasm or GenX TaxonName link.
- RFC-097 acknowledges official `People`; the proposed PersonReference has no typed reference to any official People or GenX Project identity and is not an authentication or authorization record.

## Boundaries and tests

Three source-backed group descriptions carry official ownership, optional fields, existing distinctions and unresolved decisions. The protected group set grows from 20 to **23** of 156, leaving **133 deferred**. Two focused tests protect the reviewed identities and assert the corresponding official operations remain acknowledged in both README and RFC. The official Common Crop Names path contains spaces, so the official source path is recorded verbatim in the prose rather than using a link encoding unsupported by the current direct-file evidence checker.

No underlying GenX schema, operation, endpoint register, official BrAPI source, approved scientific relationship or maturity status has been changed. Substantive identity mappings remain contingent on evidence and separate maintainer decisions.