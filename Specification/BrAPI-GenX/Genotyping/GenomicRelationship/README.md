# BrAPI-GenX — Genomic Relationship (Scientific Compute)

GenomicRelationship proposes metadata for a genomic relationship matrix,
not a verified pairwise relatedness computation. The matrix reference and
digest are optional; no sample order, genome panel, relatedness estimator,
method version, or content-verification result is required.

The draft does not establish equivalence to a kinship or pedigree matrix.
Official BrAPI version 2.1 contracts remain unchanged.

- `POST /genx/v1/genomic-relationships` (`genxRegisterGenomicRelationship`) registers one
  `GenomicRelationship` (`Schemas/GenomicRelationshipNewRequest.yaml`). Same
  `genomicRelationshipDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/genomic-relationships` (`genxListGenomicRelationships`) lists results,
  optionally filtered by method, study, or status.
- `GET /genx/v1/genomic-relationships/{genomicRelationshipDbId}`
  (`genxGetGenomicRelationship`) retrieves one result.

Details and falsifiers: `../../RFCs/RFC-056-Genomic-Relationship.md`.