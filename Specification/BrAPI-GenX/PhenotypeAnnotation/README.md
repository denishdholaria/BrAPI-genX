# BrAPI-GenX — Phenotype Annotation (Phenotyping)

Phenotype annotations record scored or annotated observations for an
observation unit and variable. BrAPI v2.1 has observations but no
annotation record.

- `POST /genx/v1/phenotype-annotations` (`genxRecordPhenotypeAnnotation`) registers one
  `PhenotypeAnnotation` (`Schemas/PhenotypeAnnotationNewRequest.yaml`). Same
  `phenotypeAnnotationDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/phenotype-annotations` (`genxListPhenotypeAnnotations`) lists records,
  optionally filtered by study, observation unit, or variable.
- `GET /genx/v1/phenotype-annotations/{phenotypeAnnotationDbId}`
  (`genxGetPhenotypeAnnotation`) retrieves one record.

Details and falsifiers: `../RFC-044-Phenotype-Annotation.md`.