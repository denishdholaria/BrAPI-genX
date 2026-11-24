# BrAPI-GenX — Pipeline Provenance (Genotyping)

Pipeline provenance records describe bioinformatics pipeline runs.
Official BrAPI version 2.1 already supports genotyping reference and variant records. This GenX candidate describes optional pipeline metadata, not an executed workflow, verified computing environment, or typed dataset lineage.

- `POST /genx/v1/pipeline-provenances` (`genxRegisterPipelineProvenance`) registers one
  `PipelineProvenance` (`Schemas/PipelineProvenanceNewRequest.yaml`). Same
  `pipelineProvenanceDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/pipeline-provenances` (`genxListPipelineProvenances`) lists records,
  optionally filtered by status.
- `GET /genx/v1/pipeline-provenances/{pipelineProvenanceDbId}`
  (`genxGetPipelineProvenance`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-116-Pipeline-Provenance.md`.