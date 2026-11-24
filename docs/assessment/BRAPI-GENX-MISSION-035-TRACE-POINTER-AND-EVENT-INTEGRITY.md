# Mission 035 — Persistent pointer and event integrity for CAS evidence

**Date:** 2026-11-24. **Parent `main`:** `b02bb9ef033a2d3fa898b05769fa7681e4a4de27`.

The existing offline D-BP-14 Compare-and-Set (CAS) trace checker
previously accepted certain self-consistent but logically impossible
before/after snapshots: a non-null published-current pointer with no
corresponding version, a draft or withdrawn version treated as
published-current, or an event referring to a revision absent from
the snapshot.

**Correction:** the pure `snapshot_integrity_errors()` helper
requires each non-null pointer to resolve to a published revision
present in the same snapshot, and each lifecycle event's affected
version ID to be among that snapshot's recorded revisions. Null
current pointers (including a pipeline with drafts or no versions)
remain permitted. The main trace verifier now invokes these
invariants on both before/after snapshots before scenario checks.

**Verification:** 10/10 isolated tests passed in
`/mnt/data/genx_mission035`, Python compilation passed. Exact
tested Git object hashes:

- `breeding_pipeline_trace_integrity.py` —
  `43d6a11982d9eaa33c3096b81c9ee1977dbe7614`
- `test_breeding_pipeline_trace_integrity.py` —
  `908d6389aadac1e9eb7a41beee00a341cfca3afe`

Three main trace integration mutations assert that orphan pointers,
draft-current pointers and orphan audit events are actually denied.
The existing 30-case main suite should reach **33 tests** after
integration. The checked-out hosted static conformance job provides
the definitive combined regression evidence.

**Scope:** these are integrity checks on an untrusted captured trace;
they do not prove a real service persisted state, enforced permissions,
serialized concurrent clients, or emitted the events described.
No production application, official BrAPI (Breeding API) version 2.1
source, GenX public endpoint or normative RFC (Request for Comments)
maturity was changed.
