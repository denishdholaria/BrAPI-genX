# Mission 047 — Germplasm passport and conservation metadata boundaries

**Date:** 2026-11-24
**Prepared parent:** `00196e00191372c1bfd979e2222591fa973e256a`
**Disposition:** three explicitly source-backed STRUCTURAL_DRAFT candidate descriptions, not scientific approval.

Official BrAPI version 2.1 already exposes `GET /germplasm/{germplasmDbId}/mcpd` and `GermplasmMCPD`, including `collectingMissionIdentifier` and institutional identifiers. The new GenX McpdAdapter carries optional `source` metadata but no executable conversion or validated schema mapping; CollectingMission has optional `title` but no typed Germplasm identity; ConservationMembership uses a free-form `memberDbId` and `program` with no enforced accession or conservation-program relationship.

Three RFC compatibility laws and module READMEs were corrected to avoid claiming typed identity links absent from their candidate schemas. D-301–D-309 remain unresolved. External MCPD/WIEWS authorities remain unchanged; no endorsement of conservation custody, exchange rights, or taxonomy is implied.

New group descriptions and regression tests extend protected modules to **36/156** (120 deferred). The source-backed missing-link inventory becomes **15**.

No official BrAPI contract, GenX wire schema, endpoint registry, generated catalogue, independent-service conformance or maturity status was changed. Run hosted static/live checks and specification generation on integration.
