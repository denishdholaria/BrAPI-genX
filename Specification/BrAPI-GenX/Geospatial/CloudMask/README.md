# BrAPI-GenX — CloudMask

`CloudMask` is a **draft metadata record** for a possible cloud mask; it is not an actual mask raster, an asset download, a tested cloud-classification model, or a quality-approved remote-sensing product. The registration contract requires only `cloudMaskDbId`; its descriptive spatial fields and provenance are optional, unstructured, and not tied to an official image or raster.

Official BrAPI (Breeding Application Programming Interface) version 2.1 `ImageNewRequest` already exposes image URL and location information. No verified mapping between official Image, GenX `RemoteSensingMetadata`, and this candidate exists.

- `POST /genx/v1/cloud-masks` (`genxRegisterCloudMask`) registers one `CloudMask` (`Schemas/CloudMaskNewRequest.yaml`). Same `cloudMaskDbId` and identical request body is described as replayable; a different body is rejected with `409`.
- `GET /genx/v1/cloud-masks` (`genxListCloudMasks`) lists records, optionally filtered by status.
- `GET /genx/v1/cloud-masks/{cloudMaskDbId}` (`genxGetCloudMask`) retrieves a record.

Source limits and deferred questions: [group description](./GroupDescription.md), [RFC-147](../../RFCs/RFC-147-CloudMask.md).
