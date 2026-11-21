# BrAPI-GenX — Crop Trait Dictionary (Terminology)

Crop trait dictionary entries describe crop-specific trait definitions.
BrAPI v2.1 has no crop trait dictionary record.

- `POST /genx/v1/crop-trait-dictionaries` (`genxRegisterCropTraitDictionary`) registers one
  `CropTraitDictionary` (`Schemas/CropTraitDictionaryNewRequest.yaml`). Same
  `cropTraitDictionaryDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/crop-trait-dictionaries` (`genxListCropTraitDictionaries`) lists entries,
  optionally filtered by status.
- `GET /genx/v1/crop-trait-dictionaries/{cropTraitDictionaryDbId}`
  (`genxGetCropTraitDictionary`) retrieves one entry.

Details and falsifiers: `../../RFCs/RFC-088-Crop-Trait-Dictionary.md`.
