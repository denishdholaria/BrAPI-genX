# BrAPI-GenX — Breeding Pipeline Open Maintainer Decisions

**Status:** Advisory decision note; no new decision in this document is ratified.  
**Workstream:** BGX-P1-06  
**Canonical specification:** [RFC-154 — Breeding Pipeline](../../Specification/BrAPI-GenX/RFC-154-BreedingPipeline.md)  
**Approved baseline:** [D-BP-01 through D-BP-13](./BRAPI-GENX-BREEDING-PIPELINE-DECISIONS-APPROVED.md)

This note separates the approved conceptual model from additional wire-level, authorization, authority-resolution, and measurement semantics that must be settled before RFC-154 can become normative.

## 1. Immediate maintainer decision — current published revision concurrency

### Problem

The logical BreedingPipeline exposes one convenience pointer, `currentBreedingPipelineVersionDbId`, to identify the current published revision. Two clients can read revision v3 concurrently and then submit different published revisions. Without a concurrency rule, both may append successfully and the last pointer write can silently replace the other client's current revision. The immutable history remains, but the current pointer no longer expresses a deterministic update outcome.

### Recommended choice: optimistic compare-and-set

Retain the candidate profile in RFC-154 §12.7:

- First registration creates the workstream and its first revision without an expected-current value.
- A new revision under an existing workstream supplies the exact current revision observed by the client; explicit JSON `null` means no current published revision. Omission is not equivalent to null.
- The expected-current precondition is outside the immutable revision payload and its replay fingerprint.
- An identical retry using the same `breedingPipelineVersionDbId` and canonical revision body is replayed before checking a now-stale precondition.
- A new draft appends without moving the current published pointer.
- A new published revision atomically compares the expected pointer, appends the immutable revision, and advances the pointer.
- A withdrawal revision identifies the exact current version being withdrawn, appends an immutable withdrawal revision, and clears the pointer atomically.
- A stale or missing precondition for an existing workstream returns HTTP 409 Conflict and performs no append or pointer mutation.

The revision body uses the repository's JSON Canonicalization Scheme (JCS), RFC 8785, for same-version replay comparison. This profile is a candidate recommendation only; it is not included in D-BP-01 through D-BP-13 and is not maintainer-ratified.

### Alternatives

| Option | Behavior | Assessment |
|---|---|---|
| A — Compare-and-set (recommended) | Client supplies the exact current pointer; append and pointer transition are atomic | Detects lost updates, preserves immutable history, makes concurrent publication outcomes explicit |
| B — Server serialization / last write wins | Server serializes writes but accepts a stale client intent and lets the last publication replace the pointer | Simple client contract, but can silently lose an earlier publication intent |
| C — Multiple current published revisions | Concurrent publications can remain current together | Requires changing the single current pointer into a collection or introducing a separate selection rule; retrieval and downstream consumers become more complex |

**Recommendation:** choose A. If one current published revision is the logical model, the server must detect a stale client baseline rather than silently overwrite it.

**Maintainer action:** ratify A, or reject it and select B or C. Until then, §12.7 remains explicitly candidate-only.

## 2. Publication and withdrawal authorization

The contract must distinguish permission to create a draft from permission to publish or withdraw a strategy used by breeding operations.

**Recommendation:**
- Permit draft registration under the ordinary pipeline write authority.
- Require an explicit publish permission for the transition to `published`.
- Require an explicit withdrawal permission for the transition to `withdrawn`.
- Enforce authorization against the owning BrAPI Program and the pipeline authority/tenant context.
- Record actor, time, reason, and the exact prior/current version in an auditable lifecycle event or equivalent immutable provenance.
- Do not infer publication permission from possession of a general write token.

Do not hard-code scope token names until the repository's authorization model and deployment profile are selected. The decision is whether publish/withdraw are separate governed actions, not the spelling of a token.

**Open choice:** separate publish/withdraw permissions and an auditable event are recommended; final actor roles, delegation rules, and audit-resource shape remain to be approved.

## 3. BrAPI server authority canonicalization and dereferencing

The reference envelope is approved in shape: BrAPI (Breeding Application Programming Interface) generation, exact resource type, authoritative server URI (Uniform Resource Identifier), and server-issued dbId. The canonical server identity and network dereferencing policy remain open.

**Candidate normalization baseline:** RFC 3986 §§6.2.2–6.2.3.

- Require an absolute HTTP or HTTPS base URI with an authority.
- Reject user information, query, and fragment components.
- Lowercase scheme and DNS host.
- Normalize percent-encoding hex case, decode unreserved characters only, remove dot segments, and remove the default port.
- Normalize an empty HTTP(S) path to `/`.
- Preserve path case, reserved percent-encoded octets, and non-empty trailing slash; the configured BrAPI base path is part of the server identity.
- Do not replace the declared authority with a redirect target during canonicalization.

**Security recommendation:** URI normalization does not itself authorize a network fetch. Runtime dereferencing should be restricted to explicitly configured/trusted authorities, with outbound-request controls and redirect restrictions. Do not let an arbitrary request URI become an unrestricted server-side fetch target.

**Open choices:** whether production authorities must be HTTPS-only; how private/test HTTP authorities are registered; the internationalized DNS name profile; DNS rebinding and proxy rules; redirect policy; and whether authority onboarding is an administrator-managed trust registry or a tenant-controlled registry.

## 4. Quantitative target validation against BrAPI Scale

The official BrAPI v2.1 schema defines an ObservationVariable as a unique combination of Trait, Method, and Scale. Its Scale defines `dataType`, `decimalPlaces`, `units`, and `validValues`; the v2.1 `minimumValue` and `maximumValue` fields are strings, while older `min` and `max` fields are deprecated.

Source contracts:
- [ObservationVariable](https://github.com/plantbreeding/BrAPI/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/ObservationVariables/Schemas/ObservationVariable.yaml)
- [VariableBaseClass](https://github.com/plantbreeding/BrAPI/blob/brapi-V2.1/Specification/Components/Schemas/VariableBaseClass.yaml)
- [ScaleBaseClass](https://github.com/plantbreeding/BrAPI/blob/brapi-V2.1/Specification/Components/Schemas/ScaleBaseClass.yaml)
- [TraitDataType](https://github.com/plantbreeding/BrAPI/blob/brapi-V2.1/Specification/BrAPI-Schema/BrAPI-Common/TraitDataType.json)

**Recommended semantic rules:**
- A direction-only objective may cite a Trait or ObservationVariable.
- A quantitative threshold or range must cite an authority-qualified ObservationVariable whose resolved Scale has `dataType: Numerical`.
- Units come from the BrAPI Scale; GenX must not accept a conflicting free-text unit.
- Enforce configured minimumValue/maximumValue bounds.
- When decimalPlaces is explicitly defined, reject a target requiring more precision rather than silently rounding or truncating it.
- Do not guess precision when decimalPlaces is null or absent.
- A categorical Scale must not be coerced into a numeric measurement.

**Open choice — dereferencing point:** either synchronously resolve the ObservationVariable at registration, or permit unresolved draft references but require successful resolution and validation before publication. The recommended lifecycle is draft may remain unverified, but publication must resolve and validate the reference. A published pipeline revision should preserve enough Scale evidence (authoritative reference plus an immutable snapshot of the relevant dataType, decimalPlaces, units, and validValues) to explain the target semantics even if the remote BrAPI record later changes.

**Open choice — exact precision and bounds:** confirm the meaning of decimalPlaces as a maximum reported precision for targets, whether min/max bounds are inclusive, and how scale changes are handled. No silent unit conversion or implicit rounding should occur.

## 5. Required evidence before normative promotion

1. Maintainer ratification of the current-pointer concurrency model.
2. Approved publish/withdraw actor permissions and lifecycle audit behavior.
3. Approved authority URI normalization, trusted-server onboarding, and dereferencing policy.
4. Approved target-scale resolution timing and immutable scale-evidence profile.
5. Positive and negative contract fixtures for the approved choices.
6. Behavior-level tests against a real implementation, including simultaneous publication attempts, replay after pointer movement, authority collisions, unavailable authority servers, wrong resource types, scale bounds, and precision.

## 6. Status boundary

- D-BP-01 through D-BP-13 remain the only ratified breeding design decisions recorded in the approval file.
- This note does not ratify the CAS profile or any other open technical choice.
- RFC-014 remains historical; RFC-154 remains an approved candidate design.
- The candidate fixtures and static checkers prove only the invariants they test. They do not prove production database atomicity, remote authority availability, authorization enforcement, or interoperability with an independently implemented server.
- No official BrAPI v2.1 source contract is modified by this workstream.
