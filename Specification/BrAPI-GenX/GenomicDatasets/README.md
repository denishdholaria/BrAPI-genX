# BrAPI-GenX — Genomic Datasets (Molecular Data Preparation)

Genomic datasets record prepared molecular data: reference assembly, pipeline
provenance, sample/variant counts, access policy, and release status. They
support reproducibility and publication of genotyping results. BrAPI v2.1
standardizes variants, call sets, and external matrix references but not dataset
preparation, pipeline provenance, or release/access policy.

- `POST /genx/v1/genomic-datasets` (`genxRegisterGenomicDataset`) registers one
  `GenomicDataset` (`Schemas/GenomicDatasetNewRequest.yaml`). Same
  `genomicDatasetDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/genomic-datasets` (`genxListGenomicDatasets`) lists datasets,
  optionally filtered by type, reference assembly, or release status.
- `GET /genx/v1/genomic-datasets/{genomicDatasetDbId}`
  (`genxGetGenomicDataset`) retrieves one dataset.

Details and falsifiers: `../RFC-013-Genomic-Datasets.md`.