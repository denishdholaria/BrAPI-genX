# Mission 057 — Plant health: observation, diagnostic and scouting boundaries

**Inspected commit:** `0d215fbe3fa10506e6f680552f724f732d2b1fe2`.
**Scope:** Four source-backed GroupDescriptions, three candidate RFC explanatory corrections, two README corrections, checker pinning and regression checks.

The preserved official BrAPI v2.1 `Observations` resource already supports phenotypic disease-related measurements. A separately named GenX record is not evidence of an absent standard feature. RFC-123 and RFC-127 now acknowledge the overlap and unverified need for separate event/summary identity.

The FieldScouting proposal previously asserted Study/Location/Farm references, while its schema offers only an optional plain-string `fieldDbId`. RFC-074 now describes the absence of typed links.

Four source-backed group descriptions distinguish symptoms, diagnostic evidence, work-order/scouting notes and resistance claims, including the optional free-text properties and open decisions. These are candidate **STRUCTURAL_DRAFT** records, not certified clinical diagnoses, completed field work, germplasm resistance classifications or independently verified service contracts.

Verification: direct Markdown source links checked against this commit's tree; regression tests added for descriptions, incumbent `/observations` operation and lack of typed scouting links. Hosted checks are required on the integrated commit before claiming full success. No schema, official BrAPI contract, operation, registry, generated artifact, maturity decision or scientific relationship was changed.
