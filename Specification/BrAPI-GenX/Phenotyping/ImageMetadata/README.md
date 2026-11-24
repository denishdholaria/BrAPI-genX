# BrAPI-GenX — Image Metadata (Phenotyping)

ImageMetadata proposes a separate capture-context record, not an alternative
to the official BrAPI (Breeding Application Programming Interface) version 2.1
Image resource. The official ImageNewRequest already carries timestamp,
width, height, location, observation-unit references and additionalInfo.

GenX requires only capture-record identity, image identifier and capture time
on registration; camera, resolution, context and provenance remain optional.
This draft does not validate sensor calibration, image content, authoritative
image joins, or scientific phenotyping interpretations.

- `POST /genx/v1/image-metadata` (`genxRegisterImageMetadata`) registers one
  `ImageMetadata` (`Schemas/ImageMetadataNewRequest.yaml`). Same
  `imageMetadataDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/image-metadata` (`genxListImageMetadata`) lists records,
  optionally filtered by study, observation unit, or status.
- `GET /genx/v1/image-metadata/{imageMetadataDbId}`
  (`genxGetImageMetadata`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-032-Image-Metadata.md`.