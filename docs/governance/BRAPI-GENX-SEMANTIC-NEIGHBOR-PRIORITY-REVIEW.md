# BrAPI-GenX Priority Semantic-Relationship Review

Status: proposed, non-normative. BrAPI v2.1 contracts remain unchanged.

This document records evidence-backed interpretation for priority semantic
relationships. It does not ratify deferred scientific questions.

## Scope

Priority relationships include the governed `SEM-*` relationships in
`Specification/ENDPOINT-REGISTRY.json` and
`Specification/BrAPI-GenX/Conformance/endpoint-overlaps.yaml`, plus the
cross-scientific-domain registry-only references (ExperimentalProtocol ->
GenomicDatasets). All 153 original registry-only identities remain in the ledger: 150 are still
`inherited-unreviewed` and three ExperimentalProtocol to GenomicDataset links
are now `requires-decision` after a bounded source-contract review.

## Mission 007 update (2026-11-24)

Since the earlier three-link review, five more source-module triads were
examined against current source schemas (15 operation links). The ledger
still retains all 153 identities, with **18 requires-decision** and
**135 inherited-unreviewed**. These five modules are not presumed to be
scientifically equivalent to genomic dataset registration; ArtifactCatalogue
and PipelineProvenance remain plausible *resource* relationship candidates
only with a typed mapping and independent evidence. See
`docs/assessment/BRAPI-GENX-MISSION-007-CROSS-MODULE-RELATIONSHIP-REVIEW.md`. Earlier snapshot counts describe their respective
review dates, not the current ledger.

## Mission 008 — source-backed scientific links (2026-11-24)

Reviewed six potentially related source/target module triads, including existing
YieldMap.harvestRecordDbId and the ambiguous AssayExecution.assayDbId versus
AssayDesign.assayDesignDbId. Source-schema evidence and questions M008-Q1..Q6
are in `docs/assessment/BRAPI-GENX-MISSION-008-EXECUTION-EVIDENCE-REVIEW.md`.
All 153 original links remain; 36 now require decisions and 117 await review.
These are advisory classifications, not scientific equivalence decisions.

## SEM-01 Seed-lot transactions versus GenX ledger records (D-20)

- Authoritative records: BrAPI v2.1 SeedLotTransaction; GenX LotLedgerEntry.
- Representation: both describe real-world material movement.
- Shared concepts: material identity, quantity, source/destination, time.
- Differences: identity model, quantity representation (decimal string in
  GenX), ordering, atomicity, replay guarantees, actor, provenance,
  idempotency.
- Safe mapping: not documented. No one-to-one event mapping or safe mirroring
  contract is established.
- Evidence required: event identity mapping, quantity/unit reconciliation,
  ordering and replay test vectors, authorization and audit rules.
- Status: unresolved-semantic-overlap. Deferred decision D-20 preserved.

## SEM-03 Scientific observations versus telemetry

- Authoritative records: BrAPI v2.1 Observation/ObservationUnit/ObservationVariable;
  GenX TelemetryPoint.
- Representation: V2.1 observations are linked to observation variables and
  observation units/studies. GenX telemetry is device/sensor time series.
- Shared concepts: measured value, timestamp, quality.
- Differences: observation variable linkage, study/unit context, spatial and
  temporal context, provenance, device/sensor identity.
- Safe mapping: not automatic. Requires explicit variable, unit, time,
  quality, study/unit, and provenance rules.
- Evidence required: mapping specification, quality-flag semantics, unit
  conversion rules, provenance envelope examples.
- Status: distinct-with-possible-explicit-mapping.

## SEM-04 VariantSet, Variant, CallSet and Calls versus VariantMatrix

- Authoritative records: BrAPI v2.1 VariantSet/Variant/CallSet/Calls; GenX
  VariantMatrix.
- Representation: VariantMatrix identifies and verifies an external matrix.
- Shared concepts: genomic variant identity and location.
- Differences: VariantMatrix does not provide matrix bytes; does not replace
  VariantSet/Variant/CallSet/Calls; external retrieval contract governs bytes.
- Safe mapping: complementary reference only.
- Evidence required: external retrieval contract, authorization rules, matrix
  metadata validation fixtures.
- Status: complementary-reference-not-data-replacement.

## SEM-06 VariableTerm versus official BrAPI ObservationVariable and OntologyTerm

- Authoritative records: BrAPI v2.1 ObservationVariable, OntologyTerm; GenX
  VariableTerm.
- Representation: V2.1 contracts are not interchangeable with GenX's
  namespaced, versioned VariableTerm.
- Shared concepts: term label, definition, ontology reference.
- Differences: namespace, versioning, authority, lifecycle, cross-authority
  mapping.
- Safe mapping: distinct schema purpose. Term equivalence and authority
  mapping need a separate rule.
- Evidence required: term equivalence policy, namespace governance, versioning
  and deprecation rules, cross-authority mapping tests.
- Status: distinct-schema-purpose.

## SEM-05 FAIR packages versus referenced data files

- Authoritative records: BrAPI v2.1 metadata.datafiles; GenX FAIRPackage.
- Representation: FAIRPackage adds citation, licensing, access-rights, and
  embargo metadata around payload references.
- Shared concepts: file reference, access and metadata.
- Differences: FAIRPackage is not a payload-byte endpoint; no persistent
  identifier minting or restricted-access approval workflow is implied.
- Safe mapping: complementary metadata, not byte transport.
- Evidence required: access policy semantics, embargo evaluation, identifier
  minting contract.
- Status: complementary-metadata-not-byte-transport.

## SEM-07 Model registration versus inference execution

- Authoritative records: GenX ModelArtifact; GenX Job.
- Representation: model registry endpoints manage model metadata and lifecycle.
  Inference is submitted as a supported Job.
- Shared concepts: model identity, version, lifecycle status.
- Differences: registration/read versus execution; no synchronous infer route.
- Safe mapping: distinct resources.
- Evidence required: jobType advertisement, model lifecycle and revocation
  rules, inference result provenance.
- Status: distinct-resources.

## Cross-scientific-domain registry-only references

**2026-11-23 triage:** All three inherited ExperimentalProtocol get/list/register
→ GenomicDataset register links now require a maintainer decision; this is
not an accepted relationship, approval to delete, or scientific equivalence.
See [the source-contract review](../../docs/assessment/BRAPI-GENX-EXPERIMENTAL-PROTOCOL-GENOMIC-DATASET-REVIEW.md).


- Relationship: ExperimentalProtocol (D2, Breeding) -> GenomicDatasets (D3,
  Genotyping) appears in 3 inherited registry-only references.
- Representation: ExperimentalProtocol records describe experimental design;
  GenomicDatasets describe prepared genomic datasets.
- Shared concepts: possible linkage between experimental design and genomic
  data.
- Differences: domain ownership, identity, lifecycle, authorization, and data
  ownership are not aligned.
- Safe mapping: not documented.
- Evidence required: explicit cross-domain reference contract, authorization,
  provenance, and study linkage rules.
- Status: inherited-unreviewed; marked priority in the ledger.

## SEM-02 V2.1 search-results lifecycle versus GenX Jobs

- Authoritative records: BrAPI v2.1 search lifecycle; GenX Job.
- Representation: Jobs is a general asynchronous-work lifecycle; V2.1 search
  uses a search-specific lifecycle.
- Shared concepts: asynchronous operation tracking.
- Differences: search result identifiers versus jobDbId, job types.
- Safe mapping: complementary only when explicitly advertised.
- Status: complementary.

## SEM-04 / others

See `endpoint-overlaps.yaml` for full rationale.

## Potentially misleading relationships

- The 153 inherited registry-only references were generated as additional
  neighbor links and are not evidence of scientific equivalence. Many link
  unrelated modules to a small set of target operations (GenomicDatasets,
  FieldScouting, VariableTerms, CropCycle, HarvestRecords, AssayDesign,
  VcfImport). They must not be treated as approved mappings.
- Similar names or compatible field types do not establish equivalence.
- The drift-regression gate remains in force; no new unreviewed references
  may be introduced.
