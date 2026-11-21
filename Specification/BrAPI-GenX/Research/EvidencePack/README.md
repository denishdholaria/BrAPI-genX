# BrAPI-GenX — EvidencePack

EvidencePack records describe EvidencePack entries.
BrAPI v2.1 has no EvidencePack record.

- `POST /genx/v1/evidence-packs` (`genxRegisterEvidencePack`) registers one
  `EvidencePack` (`Schemas/EvidencePackNewRequest.yaml`). Same
  `evidencePackDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/evidence-packs` (`genxListEvidencePacks`) lists records,
  optionally filtered by status.
- `GET /genx/v1/evidence-packs/{evidencePackDbId}`
  (`genxGetEvidencePack`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-122-EvidencePack.md`.
