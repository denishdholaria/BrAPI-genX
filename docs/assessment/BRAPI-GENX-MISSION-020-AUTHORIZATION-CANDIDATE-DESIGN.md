# Mission 020 — Exact-Relationship Decision Candidate Design

**Date:** 2026-11-24  
**Baseline `main`:** `74575b1e8c2ee98e8fd41f7256b6a1c06960166b`  
**Status:** **NON-NORMATIVE DRAFT SCHEMA ONLY — NOT RATIFIED**.

## Need

The existing governance validator accepts many syntactically followable
`authorizationReference` strings, such as arbitrary `RFC-002` identifiers,
without verifying that the project maintainer authorized **the exact**
relationship's `rejected` or `superseded` terminal transition. This is
a substantive integrity gap, tracked in
[issue #20](https://github.com/denishdholaria/BrAPI-genX/issues/20).

A validation *schema* is not an approval mechanism. It must not silently
convert historical Request for Comments (RFC) proposals into normative
decisions.

## Candidate-only format

A draft decision proposal has the following conceptual fields:

```yaml
schemaVersion: 1
recordType: semantic-neighbor-terminal-decision-candidate
status: draft-not-authorized
decisionId: SEM-CAND-0001
relationshipId: "example.source -> genxOriginal"
sourceCatalogId: example.source
targetOperationId: genxOriginal
action: reject
rationale: "A separately evidenced reason for requesting disposition."
evidenceRefs:
  - docs/assessment/example.md
proposedBy: specification-engineering
proposedAt: "2026-11-24"
```

An optional `supersededBy` is **required only** when
`action: supersede` is proposed. This illustration uses a fictional
source and does not correspond to an approved registry relationship.

## Reversible, opt-in validator

`Scripts/validate_semantic_decision_candidate.py` can verify:

- exact `relationshipId = sourceCatalogId -> targetOperationId`;
- candidate ID pattern, strict draft-only status and known record type;
- action `reject` or `supersede`, valid non-self successor;
- rationale, evidence, proposer attribution, date and unknown fields;
- optionally, relationship and successor IDs against the actual ledger
  using `--ledger`.

The tool **deliberately rejects** `authorizationReference`, claims of
`ratified` status, or unknown fields. Its success message explicitly states
that it has not authorized a disposition.

Run it manually:

```sh
python Scripts/validate_semantic_decision_candidate.py \
  --candidate PATH_TO_DRAFT.yaml \
  --ledger Specification/BrAPI-GenX/Conformance/semantic-neighbor-review.yaml
```

The existing canonical validator, active registry, ledger contents and
published artifacts are untouched. The candidate checker is **not**
automatically used to approve terminal status changes.

## Verification and limitations

`Scripts/test_semantic_decision_candidate.py` contains **14 isolated
positive and adversarial tests** (forged approval status, unrelated
identity, missing known ledger record, unknown successor, self-supersession,
missing rationale, duplicate evidence, invalid date, invalid ledger etc.).
All **14 passed** locally, and Python compilation passed.

Local tested blob hashes (verify after GitHub commit):

- checker: `01a669876936b5f54b8b5e9e75cd449a5883a7d8`;
- tests: `80f93b8eec73b0ce8c2940799fc0f395ff94100f`.

This schema validates *form*, not scientific evidence content or approval
authority. Choosing a maintainer-ratified authorization mechanism (e.g.
exact-ID versioned decision records with a binding to an approved commit)
remains an explicit maintainer decision before enforcement.

Neither official Breeding API (BrAPI) version 2.1 contracts nor any
GenX wire schemas or maturity states were modified.
