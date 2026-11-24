# Mission 070 — Assay designs, execution records, vendor orders and probe identity

**Parent inspected:** `e2b3ae7acbe0f9325fd3e49b257a6286af8b1e23` (Mission 069), 2026-11-24.
**Scope:** evidence-backed text corrections, group descriptions and regression tests only. No published API, registry, candidate schema or official source changes.

## Source-verified interoperability findings

1. **Official vendor-order overlap (highest risk).** Official BrAPI 2.1 has `GET` and `POST /brapi/v2/vendor/orders`, plus related status/results endpoints. GenX RFC-073 and its module overview falsely claimed no vendor-order record existed, and the RFC claimed direct Sample and GenomicDataset identifiers absent from the actual candidate schema. Candidate vendorOrderDbId is not official orderId. An independent profile/mapping decision is required before proposing duplicate operational semantics.
2. **Marker and physical-probe identity.** BrAPI `/brapi/v2/markerpositions` filters by `variantDbId`; GenX MarkerProbe's optional `markerDbId` is neither documented nor validated as a Variant identity. A probeSequence string is not biological validation or evidence of binding.
3. **Design versus execution.** GenX AssayDesign records no required markers, platform, versioned method or dataset reference. GenX AssayExecution has optional `assayDbId`, not a required typed reference to `assayDesignDbId`. Neither registration proves a physical laboratory run, assay result, quality control or repeatability.
4. **Claimed ingestion.** GenX VendorOrder requires only an identifier in its request; vendor, sampleCount, platform and resultIngestedAt are optional. No explicit Sample, GenomicDataset, official orderId or serviceIds references are modeled. A timestamp is not an evidence-backed ingestion certificate.

## Artifacts and evidence

- Four guarded `Genotyping/*/GroupDescription.md` files cite local candidate schemas, draft operations, official BrAPI sources and Request for Comments.
- RFC-061, RFC-113, RFC-073 and RFC-071 compatibility/problem statements are aligned with actual schemas. Four corresponding README overviews no longer claim unsupported linkage or absent official vendor-order behavior.
- The group checker gains four reviewed modules (105 → **109 of 156**, 47 deferred). A schema-derived regression test verifies current required fields, absence of unratified references, official vendor-order GET/POST and the `variantDbId` marker-position boundary.

## Governance and next actions

D-181–183, D-337–339, D-217–219 and D-211–213 remain open. No candidate wire payload change, identifier mapping, terminal relationship approval, maturity promotion, reference-server conformance or independent service evidence is introduced. This is documentation/source-contract assurance, **not** evidence that the stated replay and lifecycle invariants were independently executed.

Falsifiers: an official BrAPI vendor-order route missing from its source, a candidate schema with mandatory validated Sample/GenomicDataset relationship, or independently ratified mapping between the two marker identifiers would require revision of this assessment and regression assertions.

Run `python3 Scripts/check_genx_group_descriptions.py`, `python3 Scripts/test_genx_group_descriptions.py`, `python3 Scripts/report_genx_evidence_coverage.py --check`, and full applicable repository gates on the integrated head. A hosted run must be observed before claiming hosted verification.
