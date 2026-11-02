# BrAPI-GenX — Genotype Call Semantics (Genomics)

Genotype call semantics records describe the missing-call policy, zygosity
encoding, and confidence conventions applied to a BrAPI CallSet. BrAPI v2.1
has no genotype call semantics record.

- `POST /genx/v1/genotype-call-semantics` (`genxRegisterGenotypeCallSemantics`) registers one
  `GenotypeCallSemantics` (`Schemas/GenotypeCallSemanticsNewRequest.yaml`). Same
  `genotypeCallSemanticsDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/genotype-call-semantics` (`genxListGenotypeCallSemantics`) lists records,
  optionally filtered by call set or status.
- `GET /genx/v1/genotype-call-semantics/{genotypeCallSemanticsDbId}`
  (`genxGetGenotypeCallSemantics`) retrieves one record.

Details and falsifiers: `../RFC-072-Genotype-Call-Semantics.md`.
