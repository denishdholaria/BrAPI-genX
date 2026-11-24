# BrAPI-GenX — Crop Trait Dictionary (Terminology)

Crop trait dictionary entries describe crop-specific trait definitions.
Official BrAPI version 2.1 already provides Traits, Ontologies, and Observation Variables. The candidate GenX crop-trait dictionary is a separate ungoverned record; a free-form crop reference and trait string cannot establish an official crop/trait mapping.

- `POST /genx/v1/crop-trait-dictionaries` (`genxRegisterCropTraitDictionary`) registers one
  `CropTraitDictionary` (`Schemas/CropTraitDictionaryNewRequest.yaml`). Same
  `cropTraitDictionaryDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/crop-trait-dictionaries` (`genxListCropTraitDictionaries`) lists entries,
  optionally filtered by status.
- `GET /genx/v1/crop-trait-dictionaries/{cropTraitDictionaryDbId}`
  (`genxGetCropTraitDictionary`) retrieves one entry.

Details and falsifiers: `../../RFCs/RFC-088-Crop-Trait-Dictionary.md`.
