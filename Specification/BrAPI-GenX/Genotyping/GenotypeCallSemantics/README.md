# BrAPI-GenX — Genotype Call Semantics (Genomics)

GenotypeCallSemantics proposes interpretation metadata alongside official
BrAPI version 2.1 CallSets. The callSetDbId field is optional and not a
validated join. Free-text missingness/zygosity conventions and optional
numeric confidenceThreshold do not prove consistent application to calls.

- `POST /genx/v1/genotype-call-semantics` (`genxRegisterGenotypeCallSemantics`) registers one
  `GenotypeCallSemantics` (`Schemas/GenotypeCallSemanticsNewRequest.yaml`). Same
  `genotypeCallSemanticsDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/genotype-call-semantics` (`genxListGenotypeCallSemantics`) lists records,
  optionally filtered by call set or status.
- `GET /genx/v1/genotype-call-semantics/{genotypeCallSemanticsDbId}`
  (`genxGetGenotypeCallSemantics`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-072-Genotype-Call-Semantics.md`.
