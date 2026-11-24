# BrAPI-GenX — External Vocabulary (Terminology)

External vocabulary sync entries describe synchronization of external
vocabularies into GenX. Official BrAPI version 2.1 already exposes metadata about available ontologies through `/brapi/v2/ontologies`. This draft GenX vocabulary-sync record is only proposed bookkeeping; it does not implement synchronization, term conversion, or a typed link to VariableTerm.

- `POST /genx/v1/external-vocabularies` (`genxRegisterExternalVocabulary`) registers one
  `ExternalVocabulary` (`Schemas/ExternalVocabularyNewRequest.yaml`). Same
  `externalVocabularyDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/external-vocabularies` (`genxListExternalVocabularies`) lists entries,
  optionally filtered by status.
- `GET /genx/v1/external-vocabularies/{externalVocabularyDbId}`
  (`genxGetExternalVocabulary`) retrieves one entry.

Details and falsifiers: `../../RFCs/RFC-083-External-Vocabulary.md`.
