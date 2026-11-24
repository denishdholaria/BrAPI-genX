# Mission 058 — Plant health: imagery, pest risk, alerts and intervention claims

**Inspected candidate:** `38ca8c2469acf90c2e300eca1012a4435dba108a`; **integration parent:** `21db3ee2268942b4d25ad4c8e4be5f4e681d97e0`.
**Scope:** Four PlantHealth group descriptions; one RFC and one README compatibility correction; evidence guard and regression tests.

Official BrAPI v2.1 already supports `/images`. CropHealthImage RFC-128 had claimed image records were absent; its current schema contains no image content, reference, spatial footprint, numeric vegetation-index result or validated health classification. The draft is not an image-exchange replacement.

The proposed `IpmStrategy` tactics are free text and do not authorize pesticide treatment. `PestDiseaseRisk` probability is a string without a controlled forecast horizon or validated calibration. `ThresholdAlert` values are untyped strings without units or an executable evaluation model. These scientific and operational limitations are documented without declaring any standards adoption or changes to approved decisions.

Four new descriptions are source linked and regression pinned. All four remain `STRUCTURAL_DRAFT`, with decision groups D-382–384, D-373–375, D-397–399, and D-376–378 unresolved.

Verification: local Markdown source references checked against the inspected Git tree. Full GitHub workflow verification will be required after integration. No official BrAPI contract, candidate schema, OpenAPI operation, semantic-neighbor registry, or normative maturity state has changed.
