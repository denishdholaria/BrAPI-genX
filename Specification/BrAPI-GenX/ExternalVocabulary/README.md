# BrAPI-GenX — External Vocabulary (Terminology)

External vocabulary sync entries describe synchronization of external
vocabularies into GenX. BrAPI v2.1 has no external vocabulary record.

- `POST /genx/v1/external-vocabularies` (`genxRegisterExternalVocabulary`) registers one
  `ExternalVocabulary` (`Schemas/ExternalVocabularyNewRequest.yaml`). Same
  `externalVocabularyDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/external-vocabularies` (`genxListExternalVocabularies`) lists entries,
  optionally filtered by status.
- `GET /genx/v1/external-vocabularies/{externalVocabularyDbId}`
  (`genxGetExternalVocabulary`) retrieves one entry.

Details and falsifiers: `../RFC-083-External-Vocabulary.md`.
