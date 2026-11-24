# BrAPI-GenX — Genomic Datasets (Molecular Data Preparation)

GenomicDataset proposes metadata alongside official BrAPI version 2.1
VariantSets, CallSets and ReferenceSets. The current schema has no typed
VariantSet, CallSet or VariantMatrix identifier; optional pipeline, digest,
release and access-policy values do not establish reproducibility, released
files or enforced permissions.

- `POST /genx/v1/genomic-datasets` (`genxRegisterGenomicDataset`) registers one
  `GenomicDataset` (`Schemas/GenomicDatasetNewRequest.yaml`). Same
  `genomicDatasetDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/genomic-datasets` (`genxListGenomicDatasets`) lists datasets,
  optionally filtered by type, reference assembly, or release status.
- `GET /genx/v1/genomic-datasets/{genomicDatasetDbId}`
  (`genxGetGenomicDataset`) retrieves one dataset.

Details and falsifiers: `../../RFCs/RFC-013-Genomic-Datasets.md`.