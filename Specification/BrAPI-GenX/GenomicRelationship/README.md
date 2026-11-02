# BrAPI-GenX — Genomic Relationship (Scientific Compute)

Genomic relationship matrices record pairwise genomic relationships
between germplasm. BrAPI v2.1 has no genomic relationship record.

- `POST /genx/v1/genomic-relationships` (`genxRegisterGenomicRelationship`) registers one
  `GenomicRelationship` (`Schemas/GenomicRelationshipNewRequest.yaml`). Same
  `genomicRelationshipDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/genomic-relationships` (`genxListGenomicRelationships`) lists results,
  optionally filtered by method, study, or status.
- `GET /genx/v1/genomic-relationships/{genomicRelationshipDbId}`
  (`genxGetGenomicRelationship`) retrieves one result.

Details and falsifiers: `../RFC-056-Genomic-Relationship.md`.