# Mission 006 — Eight-RFC Disposition and Authority Pilot

**Assessment date:** 2026-11-23  
**Inspected baseline:** `bf6f78b3509107a71f6ab22f2bd6ec5d09ae8dd9`  
**Scope:** RFC-003, RFC-008, RFC-014, RFC-019, RFC-035, RFC-037,
RFC-098, RFC-154. This is a review artifact, not a normative specification
or maturity-promotion approval.

## Decision basis

- `docs/assessment/BRAPI-GENX-BREEDING-PIPELINE-DECISIONS-APPROVED.md`:
  maintainer-approved D-BP-07 through D-BP-14.
- `docs/assessment/BRAPI-GENX-BREEDING-CROSS-RFC-OVERLAP-REVIEW.md`:
  existing BrAPI v2.1 resource boundary assessment.
- `docs/governance/BRAPI-GENX-SPECIFICATION-QUALITY-STANDARD.md`:
  quality gates E1–E12.
- The numbered RFCs and the maturity register are distinct: in-file
  `proposal`/non-normative wording is not an automatic maturity rating.

## Pilot disposition table

| RFC | Reviewed disposition | Primary authoritative scientific fact | Next required evidence or decision |
|---|---|---|---|
| 003 Seed-Lot Ledger | CONTRACT_VALIDATED; **not accepted** | GenX append-only lot movement entry, complementary to BrAPI SeedLotTransaction | D-20 mapping/event identity, reconciliation and independent service/security evidence |
| 008 SelectionDecision | STRUCTURAL_DRAFT; refine | Actual breeder verdict and rationale, not scheme task definitions | RFC-008-Q1..Q3; evidence/reference authorization; unit and identity review |
| 014 Breeding Pipeline precursor | STRUCTURAL_DRAFT; **historical only** | No independent active resource; RFC-154 is canonical editorial design | Preserve archive; do not generate duplicate source operations |
| 019 ProgenyRecord | **DEFERRED** (D-BP-08) | BrAPI Germplasm/Pedigree/Crosses own existing lineage facts | Demonstrate an immutable formation/family event not already representable |
| 035 PopulationAdvancement | STRUCTURAL_DRAFT; refine | Actual advancement of material/population through a scheme | Exact scheme-version/stage resolution, event identity and tests |
| 037 CrossingSchedule | **DEFERRED** (D-BP-11) | BrAPI PlannedCross/CrossingProject own planned mating | Evidence for distinct scheduling or resource-booking semantics |
| 098 ResearchProgram | **DEFERRED** (D-BP-12) | BrAPI Program owns the overlapping program identity | No independent contract without a newly evidenced nonduplicate concept |
| 154 BreedingPipeline | STRUCTURAL_DRAFT; approved *candidate* design only | Durable breeding workstream and immutable scheme revisions | Remaining authority trust, publication/withdrawal security, Scale validation and independent concurrent service behavior |

## Quality gate and known limitations

1. Every candidate requires an evidence-backed real-world exchange gap (E1),
   explicit ownership/relationships (E2), typed scientific quantities (E3–E5),
   stable identifiers (E6), lifecycle semantics (E7), and precise
   operation/security/standards/conformance evidence (E8–E12).
2. None of the eight is promoted to accepted/normative by this review.
3. **Known register drift corrected:** RFC-019, RFC-037, RFC-098 now reflect
   existing maintainer-approved deferrals. The historic source descriptions
   remain available but are labelled as obsolete gap assertions.
4. **Known decision-identity collision corrected:** RFC-008-Q1..Q3 are
   RFC-local questions, separate from global D-21..D-23.
5. This assessment does not delete operations, change the endpoint registry,
   declare interchangeability, or modify official BrAPI v2.1 sources.

## Follow-up actions

- Add an automated check that register rows and RFC filenames reconcile,
  every explicitly deferred RFC has the matching maturity status, and
  SelectionDecision local question IDs remain unambiguous.
- Inspect independent evidence for the three priority
  ExperimentalProtocol → GenomicDataset operation-neighbor links.
- Use the current mature-contract pilot as a repeatable review model, not
  as grounds for bulk maturity promotion.

**Evidence boundary:** repository documentation and source contract review;
not a deployed-service test or external scientific ratification.
