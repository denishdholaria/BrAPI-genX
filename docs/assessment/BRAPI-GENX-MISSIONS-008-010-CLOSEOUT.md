# BrAPI-GenX — Missions 008–010 Autonomous Development Closeout

**Date:** 2026-11-24  
**Starting main:** `423e7f2f0b174c8dc4d9b06d356da2697ed53944`  
**Inspected final implementation main:** `9405a486a7fa9e67229cb66e8e62a1191913fae5`  
**Status:** three bounded engineering milestones committed on `main`; hosted and independent conformance **not yet verified**. All findings are BrAPI-GenX internal, non-normative design evidence.

## 1. Mission 008 — Six scientifically plausible semantic-neighbor groups

**Commit:** [`af6994084f0da82e1d1811c03b63309526ed3a23`](https://github.com/denishdholaria/BrAPI-genX/commit/af6994084f0da82e1d1811c03b63309526ed3a23)

- Reviewed 18 operation-level neighbors across **AssayExecution → AssayDesign**, **VcfExport → VcfImport**, **FieldBook → FieldScouting**, **YieldMap → HarvestRecords**, **QualityFlag → VariableTerms**, and **ReferenceAssembly → GenomicDatasets**.
- For each entry retained stable ID and inherited registry provenance; supplied the actual source schema, target schema, assessment, rationale and open question.
- Classified exactly 18 `inherited-unreviewed → requires-decision`. **No approval, rejection, deletion, route change or normative promotion.**
- Preserved the already-present optional `YieldMap.harvestRecordDbId`, distinguishing a resource-level derivation reference from operation-level equivalence.
- Recorded the six scientific questions M008-Q1..Q6 in [the assessment](./BRAPI-GENX-MISSION-008-EXECUTION-EVIDENCE-REVIEW.md) and [issue #18](https://github.com/denishdholaria/BrAPI-genX/issues/18).

## 2. Mission 009 — Source-contract evidence regression gate

**Commit:** [`a974f83c8689b681dee39df895d362afe585aec4`](https://github.com/denishdholaria/BrAPI-genX/commit/a974f83c8689b681dee39df895d362afe585aec4)

- Added `Scripts/check_scientific_contract_boundaries.py`. It verifies required/present/absent field claims in the 12 corresponding source schemas and checks the six reviewed ledger triads and citation preservation.
- Added `Scripts/test_scientific_contract_boundaries.py` with **12 local positive/mutation tests**, including removal of an existing harvest source reference, loss of a required harvest quantity unit, additions of formerly absent field references, deleted contracts, changed statuses, missing citations and malformed inputs.
- Both scripts were added to the static conformance and specification-build GitHub Actions workflows. The checker is fail-closed on drift *relative to the recorded assessment*, not a prohibition on intentional redesign: a deliberate schema evolution requires evidence and tests to be updated together.

### Verification actually completed for Mission 009

Executed in an isolated local Python environment:

```sh
cd /mnt/data/brapigenx_mission009
python3 -m unittest -v test_scientific_contract_boundaries.py
python3 -m py_compile check_scientific_contract_boundaries.py test_scientific_contract_boundaries.py
```

**Result:** 12/12 passed; compilation succeeded. The checked-in Git blob hashes equal the byte-for-byte locally tested files:

- Checker `14a67ffe8df4a071424d632345f2b4167b051096`
- Test `5ec6565a43a9c37bd4bc5aeba3db2921a8ffbf30`

A separate connector-based inspection checked all **12 actual checked-in schemas** for the new gate's relevant field-presence/absence and requiredness assertions and found **zero mismatches**. This is a structural comparison, not a full local checkout or scientific behavior test.

## 3. Mission 010 — RFC-154 authority-filter duplication hardening

**Commit:** [`9405a486a7fa9e67229cb66e8e62a1191913fae5`](https://github.com/denishdholaria/BrAPI-genX/commit/9405a486a7fa9e67229cb66e8e62a1191913fae5)

- Identified a potential **ambiguous query-parameter declaration**: the existing `parameter_map` uses a dictionary keyed by parameter name, so duplicates could be hidden before authority-qualification checks.
- Added `require_unique_parameter_names` in `Scripts/check_breeding_pipeline_api_contract.py`, called on PopulationAdvancement GET and SelectionDecisions GET before dictionary conversion. It rejects repeated explicit `(in, name)` identities and repeated `$ref` references, while permitting same names in distinct parameter locations.
- Added six dedicated positive/mutation tests in `Scripts/test_breeding_pipeline_parameter_duplicates.py`, and wired them into both workflows.
- Verified that the explicit parameter names in the two current source operation files were not duplicated at the inspected baseline. No wire-contract field or route was changed.

### Verification actually completed for Mission 010

Executed in an isolated local Python environment:

```sh
cd /mnt/data/brapigenx_mission010
python3 -m unittest -v test_breeding_pipeline_parameter_duplicates.py
python3 -m py_compile test_breeding_pipeline_parameter_duplicates.py
```

**Result:** six helper-unit tests passed. The local test module Git blob equals the committed blob `402c62cb4066a4d3c0568c5a3242a1cbcae1eb70`. The tests were executed against a standalone copy of the inserted helper (matching its code), **not** the full checked-out BreedingPipeline static checker. See [the Mission 010 design report](./BRAPI-GENX-MISSION-010-PARAMETER-IDENTITY-ASSURANCE.md) for this limitation.

## 4. Current governed inventory

| Measure | Current |
|---|---:|
| Original semantic-neighbor IDs retained | 153 |
| `requires-decision` with documentary triage | 36 |
| `inherited-unreviewed` | 117 |
| Normatively accepted or rejected through these missions | 0 |
| Numbered RFCs modified or promoted | 0 |

**Authority remains unchanged:** the maintainer decides scientific meaning, compatibility and any terminal relationship disposition. The difference between independent resource identity, typed reference and operation-level discovery must not be collapsed.

## 5. Verification limitations, deployment policy and handoff

- **Not run:** entire checked-out-repository conformance suite, independent server tests, authenticated source-resolution and Scale tests, GenX reference server, generated artifact consistency, or hosted Continuous Integration (CI).
- The user reports exhausted GitHub Actions monthly minutes with expected reset on **2026-12-01**, tracked in [issue #15](https://github.com/denishdholaria/BrAPI-genX/issues/15). Hosted checks must be rerun after the budget becomes available; their prior pre-step failures are not evidence of bad contract tests.
- **Zero official BrAPI version 2.1 source contract changes**; **zero GenX route or operation-identity changes**; **zero unapproved RFC status upgrades**.
- **Recommended next small slices:** review the remaining 117 inherited neighbor links with science-first schema comparisons; collect independent behavioral acceptance evidence for RFC-154, particularly current-revision compare-and-set concurrency, authority trust, publication authorization/audit and target Scale validation. In all cases preserve explicit unresolved policy questions instead of choosing them implicitly.

**Engineering result:** source-backed scientific review expanded; regression checks now catch accidental loss of documented identifiers and ambiguous authority-filter declarations. Full conformance and release readiness remain conditional on actual executing tests and maintainer decisions.
