# BrAPI-GenX — Doubled Haploid Programs (Breeding)

This **STRUCTURAL_DRAFT** registers a proposed program descriptor, not an experimentally verified doubled-haploid outcome. Official BrAPI version 2.1 Cross records already recognize `crossType: DOUBLE_HAPLOID`; a program-wide process descriptor has a distinct, unvalidated scope.

- `POST /genx/v1/doubled-haploid-programs` (`genxRegisterDoubledHaploidProgram`) registers `DoubledHaploidProgram` (`Schemas/DoubledHaploidProgramNewRequest.yaml`), requiring only the candidate ID, Program string and induction `method`. Donor, haploid/doubled counts, dates and provenance are optional, even at `completed`.
- `GET /genx/v1/doubled-haploid-programs` (`genxListDoubledHaploidPrograms`) lists records optionally filtered by Program/status.
- `GET /genx/v1/doubled-haploid-programs/{doubledHaploidProgramDbId}` (`genxGetDoubledHaploidProgram`) retrieves a record.

Identical-body replay and `409` conflicting replay are candidate behavior, not independently proven persistent operations. No ploidy assay, lineage or derived Germplasm validation exists. See [evidence](./GroupDescription.md), [RFC-020](../../RFCs/RFC-020-Doubled-Haploid.md); D-57–D-59 remain open.
