# Mission 059 — Material movement and field-operation evidence boundaries

**Prepared against parent:** `ae85ea4f7ecf6be40d9e626c7f7b0fa0e76ca5c8`.

## Four candidate operations reviewed

- HarvestRecord: quantity and units required; moisture/area optional; no automatic mass-balance reconciliation to BrAPI SeedLot transactions. D-20/D-30–32 remain decision-gated.
- IrrigationEvent: volume and volume unit optional; claims of water application are not calibrated water-balance evidence. Its Location/Study string identifiers are not verified typed links. D-69–71 remain decision-gated.
- PlantingOperation: status may be planned/completed/cancelled; seedingRate is numeric but unit exists only in general provenance, not a unit property. Study/ObservationUnit/CropCycle identities are optional strings. D-196–198 remain decision-gated.
- SprayApplication: free-text rate and optional field reference do not establish chemical identity, lawful dose, operator, application or compliance. RFC-081's preexisting claim of a FieldScouting linkage is corrected. D-241–243 remain decision-gated.

Four `GroupDescription.md` files are source-linked and pinned with test coverage. The RFC-024 and RFC-081 explanations are adjusted without touching wire contracts, scientific acceptance, official BrAPI v2.1, endpoint registries, generated artifacts or governance decisions.

## Verification

Direct Markdown source references checked against parent Git tree. GitHub workflows must pass on integrated commit before a full-success claim.
