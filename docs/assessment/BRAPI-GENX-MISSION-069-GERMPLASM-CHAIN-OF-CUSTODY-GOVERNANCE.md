# Mission 069 — Material acquisition, custody, disposal, quarantine and duplicate identity

**Prepared parent:** `bf420d63c5e690012514ad674072943f62f9eaf4`.

Five source-based Germplasm module descriptions distinguish candidate metadata from verified movement, scientific identity, physical receipt or authorization.

- Acquisition has required seed lot/source/date but no receiving signatures, material quantity or field collection/quarantine relationship.
- CustodyTransfer allows both material identifiers and both party identities to be missing; a claimed accepted state is not verified authenticated custody.
- DisposalRecord allows both material identities and quantity units to be absent, so its completed state is not automatic inventory debit or legal destruction proof.
- Quarantine has required lot/reason/date but no mandatory release date, inspector approval or pathogen clearance.
- DuplicateReview has no controlled candidate identity or second candidate field; a decision string cannot establish germplasm equivalence.

RFC-104 compatibility prose was corrected to avoid a false BrAPI Germplasm typed-link claim. Deferred decision sets D-121–123, D-187–189, D-193–195, D-87–89 and D-310–312 remain open. The checker pins five descriptions and mutation tests; direct source links are verified against parent tree. No official BrAPI or candidate wire contract, inventory transaction, legal/scientific approval or independent conformance changes.

Hosted verification required on integrated commit.
