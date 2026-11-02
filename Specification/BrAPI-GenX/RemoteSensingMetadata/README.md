# BrAPI-GenX — RemoteSensingMetadata

RemoteSensingMetadata records describe RemoteSensingMetadata entries.
BrAPI v2.1 has no RemoteSensingMetadata record.

- `POST /genx/v1/remote-sensing-metadata` (`genxRegisterRemoteSensingMetadata`) registers one
  `RemoteSensingMetadata` (`Schemas/RemoteSensingMetadataNewRequest.yaml`). Same
  `remoteSensingMetadataDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/remote-sensing-metadata` (`genxListRemoteSensingMetadata`) lists records,
  optionally filtered by status.
- `GET /genx/v1/remote-sensing-metadata/{remoteSensingMetadataDbId}`
  (`genxGetRemoteSensingMetadata`) retrieves one record.

Details and falsifiers: `../RFC-145-RemoteSensingMetadata.md`.
