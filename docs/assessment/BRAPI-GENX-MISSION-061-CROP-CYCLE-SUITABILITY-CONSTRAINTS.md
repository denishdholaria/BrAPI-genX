# Mission 061 — Crop cycles, sowing, suitability and local constraints

**Prepared parent:** `b229dd5c4658d509bb83bc6ad5b22e7b82f043cd`.

Four source-based draft group descriptions distinguish crop-cycle timing from actual planting/harvest evidence, optional untyped crop suitability scores from validated site assessment, proposed sowing windows from completed planting, and claimed local constraints from enforceable regulations.

The CropCycle RFC-029 compatibility paragraph now correctly states that Location/Study identifiers are optional strings without established typed referential integrity. The LocalConstraint RFC-139 problem paragraph no longer claims an unstructured metadata record can enforce legal restrictions; jurisdiction, source authority, effective intervals and rule evaluation are missing.

Questions D-84–86, D-388–390, D-403–405, D-415–417 stay decision-gated. No official BrAPI or candidate OpenAPI schema, operations, endpoint registry, scientific mapping, actual legal rule or maturity has changed. All evidence links were resolved against the parent Git tree and regression tests were added. Full hosted verification will be required after integration.
