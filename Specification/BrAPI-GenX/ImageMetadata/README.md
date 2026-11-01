# BrAPI-GenX — Image Metadata (Phenotyping)

Image metadata records the capture details and provenance of phenotyping
images. BrAPI v2.1 has images but no image metadata record.

- `POST /genx/v1/image-metadata` (`genxRegisterImageMetadata`) registers one
  `ImageMetadata` (`Schemas/ImageMetadataNewRequest.yaml`). Same
  `imageMetadataDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/image-metadata` (`genxListImageMetadata`) lists records,
  optionally filtered by study, observation unit, or status.
- `GET /genx/v1/image-metadata/{imageMetadataDbId}`
  (`genxGetImageMetadata`) retrieves one record.

Details and falsifiers: `../RFC-032-Image-Metadata.md`.