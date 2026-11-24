# Mission 067 — Research reference identity and deferred program authority

**Prepared parent:** `cc6ac4de5cc91d647381a5e48c6ef6a54a276212`.

Reviewed candidate `Project`, `ResearchLocation` and deferred `ResearchProgram` against their actual schema, governing RFC, maturity register and official BrAPI resource ownership.

- `Project` has only optional title and funding strings, not a typed Study or validated grant authority. RFC-089's unsupported typed Study-link claim was corrected.
- `ResearchLocation` duplicates existing official BrAPI v2.1 Locations without a typed Location or Farm link. The RFC-100 absence claim and false link were corrected, as was the module overview.
- `ResearchProgram` is explicitly deferred by approved D-BP-12; official BrAPI Program remains authoritative. The historical RFC-098 compatibility text was adjusted to prevent an implied typed Study link. The documentation **does not** authorize any implementation or release.

Descriptions and regression tests distinguish two STRUCTURAL_DRAFT proposals from one governance-DEFERRED historical candidate. D-265–267 and D-298–300 remain open; D-BP-12 is maintained. All evidence links were checked against the parent Git tree. No official BrAPI change, GenX wire contract, route, generated artifact or governance promotion.

Hosted workflows must run on the integrated commit before full verification is claimed.
