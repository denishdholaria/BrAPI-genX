# BrAPI-GenX — CloudMask

CloudMask records describe CloudMask entries.
BrAPI v2.1 has no CloudMask record.

- `POST /genx/v1/cloud-masks` (`genxRegisterCloudMask`) registers one
  `CloudMask` (`Schemas/CloudMaskNewRequest.yaml`). Same
  `cloudMaskDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/cloud-masks` (`genxListCloudMask`) lists records,
  optionally filtered by status.
- `GET /genx/v1/cloud-masks/{cloudMaskDbId}`
  (`genxGetCloudMask`) retrieves one record.

Details and falsifiers: `../RFC-146-CloudMask.md`.
