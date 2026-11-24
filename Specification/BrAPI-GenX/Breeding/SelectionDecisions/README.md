# BrAPI-GenX — Selection Decisions (Breeding Verdicts)

This **STRUCTURAL_DRAFT** records an asserted breeding selection verdict, not a verified authorization, mandatory evidence review, executed cross, commercial approval or independent service conformance. The request requires an authority-qualified Program reference, dated enumerated verdict and immutable decision ID. Candidate, decision maker, rationale, linked observations and provenance are **optional**.

- The optional `pipelineContext` and `schemeContext` describe exact process versions when applicable. They do not prove an approved decision.
- `schemeContext` contains `breedingSchemeDbId` and `breedingSchemeVersionDbId`; `stageId` must resolve within that version.
- `pipelineContext` contains `breedingPipelineDbId` and `breedingPipelineVersionDbId`; when both contexts exist, their scheme bindings must agree.
- The list filters use authority pairs: `programDbId`/`programServer`, `studyDbId`/`studyServer`, and `candidateGermplasmDbId`/`candidateGermplasmServer`. The stated paired-filter law remains a candidate rule subject to conformance tests.
- GenX ParentCandidateSelection separately represents a parent-specific Boolean verdict using unqualified Program/Germplasm strings. No typed link or lossless mapping between these candidate resources is specified.

Official BrAPI version 2.1 resources remain authoritative for Program, Study, Germplasm, Observation and actual/planned crosses. See [evidence](./GroupDescription.md) and [RFC-008](../../RFCs/RFC-008-Selection-Decisions.md); Q1–Q3 remain open.
