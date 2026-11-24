# BrAPI-GenX — RemoteSensingMetadata

RemoteSensingMetadata proposes catalogue information about an image
acquisition, not an accessible, calibrated or geometrically verified raster.
The only required registration field is its identity; platform, sensor,
acquisition date, coordinate reference, resolution and provenance are
optional strings or objects. No source raster, footprint, spectral bands or
image-quality verification is required.

Official BrAPI version 2.1 contracts remain separate. Metadata identity
does not prove sensor calibration or a reliable vegetation index.

- `POST /genx/v1/remote-sensing-metadata` (`genxRegisterRemoteSensingMetadata`) registers one
  `RemoteSensingMetadata` (`Schemas/RemoteSensingMetadataNewRequest.yaml`). Same
  `remoteSensingMetadataDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/remote-sensing-metadata` (`genxListRemoteSensingMetadata`) lists records,
  optionally filtered by status.
- `GET /genx/v1/remote-sensing-metadata/{remoteSensingMetadataDbId}`
  (`genxGetRemoteSensingMetadata`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-145-RemoteSensingMetadata.md`.
