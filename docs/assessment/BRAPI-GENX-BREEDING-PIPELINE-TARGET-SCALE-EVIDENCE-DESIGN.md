# BreedingPipeline Target-Scale Validation Evidence — Candidate Design

**Status:** Engineering proposal for maintainer review. Non-normative. No new public endpoint or schema component is introduced by this document.

**Scope:** Immutable evidence that a quantitative BreedingPipeline target was evaluated against a specific authority-qualified BrAPI v2.1 ObservationVariable Scale at a recorded time.

## 1. Design objective

A published quantitative breeding objective must remain interpretable after the remote ObservationVariable or its Scale changes. The immutable pipeline revision preserves the target and its authority-qualified ObservationVariable reference. A separate immutable evidence record should preserve the Scale projection actually used to validate that target.

The record answers four distinct questions:

1. Which exact immutable pipeline revision and target requirement was evaluated?
2. Which authority-qualified ObservationVariable was resolved?
3. What Scale values were observed and used by the validator?
4. Which versioned validation profile produced the successful result, and when?

The record is evidence of a validation event. It is not a new BrAPI measurement resource, a second source of truth for live Scale metadata, proof that the remote authority was trustworthy, or a cryptographic signature.

## 2. Existing repository mechanisms and ownership boundary

The existing mechanisms are not interchangeable:

- **ProvenanceEnvelope** is a generic embedded provenance envelope. Its current EvidenceLink binds endpoint/schema/digest concepts but does not define the exact per-target Scale projection or immutable target locator required here.
- **PipelineProvenance** is a Genotyping bioinformatics pipeline-run record. Its stated purpose is not breeding-target measurement validation; reusing it would conflate two domain concepts.
- **TargetTraitRequirement** remains a breeding objective. It must not acquire a copied Scale, duplicate unit field, or mutable validation status.
- **BrAPI-GenX/DECISIONS.md** and the Cluster 1 approval record are the authorities for digest decisions. D-02 accepts JCS-RFC8785 for generic canonical JSON but explicitly does not select a universal cryptographic hash algorithm.

The existing src/brapi_genx/digest.py uses SHA-256 internally. That is implementation evidence for the current helper, not proof that SHA-256 is an approved external or universal GenX digest algorithm. The documentation correction associated with this slice does not change digest behavior.

## 3. Candidate evidence-record model

One evidence record is associated with one quantitative target requirement in one immutable pipeline revision. The model below is conceptual, not an OpenAPI schema:

```text
TargetScaleValidationEvidenceCandidate
  evidenceRecordId                 immutable identifier; token/namespace open
  pipelineContext
    breedingPipelineDbId
    breedingPipelineVersionDbId    exact immutable revision
  targetBinding
    targetContextId
    traitRequirementIndex          zero-based position in that revision's array
  observationVariableReference    exact BrAPI v2.1 authority-qualified reference
  scaleProjection
    scaleName                      optional, preserve as received
    scalePUI                       optional, preserve as received
    ontologyReference              optional, preserve as received
    dataType
    decimalPlaces                  preserve null versus absent
    units                          preserve null versus absent; never infer
    validValues                    preserve object, including categories and bounds
  sourceRetrievedAt                timestamp of source retrieval
  validatedAt                      timestamp of local rule evaluation
  validationProfile
    profileId
    profileVersion
  validationResult                 passed for publication evidence
  snapshotFingerprint              optional until hash algorithm is selected
```

### Exact target binding

The binding tuple is:

**(breedingPipelineDbId, breedingPipelineVersionDbId, targetContextId, traitRequirementIndex)**.

The evidence record's observationVariableReference must equal the traitReference at that exact target position, including all four reference members: apiGeneration, resourceType, server, and dbId.

The immutable revision identity makes the array index stable for the record's lifetime. A new revision must receive new validation evidence for each quantitative target under this candidate publication profile; evidence must not silently migrate to a different revision or target position. Direction-only Trait objectives do not require Scale-validation evidence.

### Scale projection

The projection should retain the BrAPI v2.1 Scale fields that affect interpretation or validation:

- dataType;
- decimalPlaces;
- units;
- the complete validValues object, including minimumValue, maximumValue, and/or categories when present;
- optionally scaleName, scalePUI, and ontologyReference to aid interpretation.

Preserve null and omitted fields as received; they are not interchangeable in an evidence fingerprint. Do not infer a unit when units is null or absent. Do not use the deprecated BrAPI v2.1 validValues.min and validValues.max as substitutes for minimumValue and maximumValue. They may be retained as source fields for historical display, but the candidate validator must not treat them as the v2.1 bounds.

The projection is stored in the evidence artifact, not copied into the target requirement or treated as a live BrAPI Scale resource.

## 4. Snapshot fingerprint: fixed preimage, algorithm still open

D-02 accepts the JCS-RFC8785 canonicalization method for generic JSON. It does not select the cryptographic hash algorithm. Therefore this candidate design fixes the structured preimage but does not mandate an algorithm or publish a fabricated digest value.

The candidate preimage object is exactly:

```json
{
  "apiGeneration": "brapi-v2.1",
  "resourceType": "ObservationVariable",
  "server": "<exact server string from the pipeline reference>",
  "dbId": "<server-issued ObservationVariable dbId>",
  "scaleProjection": {
    "dataType": "Numerical",
    "decimalPlaces": 2,
    "units": "t/ha",
    "validValues": {
      "minimumValue": "0",
      "maximumValue": "20"
    }
  }
}
```

The preimage includes the exact server string used in the immutable target reference. It does not assume that two syntactically different URIs are equivalent; RFC-154 §12.9's full canonicalization and deployment profile remain open. The entire present scaleProjection is included, not only the fields that happened to be checked by one implementation.

If a fingerprint is adopted, the candidate procedure is:

1. Construct the preimage above using the source projection as retrieved.
2. Serialize the value with the accepted JCS-RFC8785 profile.
3. Apply a separately selected and named cryptographic hash algorithm.
4. Store the algorithm identifier, canonicalization profile/version, digest purpose, and defined encoding alongside the value.

The algorithm and external envelope must be approved before a digest is a required interoperable field. SHA-256 is not silently selected by this proposal. A digest detects a difference relative to a trusted expected digest; it does not authenticate the authority, prove retrieval, or replace a signature/trust mechanism.

## 5. Candidate publication lifecycle

1. **Draft registration:** A draft may contain a quantitative ObservationVariable reference without resolved Scale evidence. The system must not represent it as validated or publishable.
2. **Publication preflight:** Resolve the exact authority-qualified BrAPI v2.1 ObservationVariable under a separately approved authority-trust and outbound-request policy. Reject wrong resource types, ambiguous authority resolution, unavailable sources, invalid responses, and non-numerical Scale values.
3. **Validation:** Check the target values against the Scale's numerical type, configured valid-value bounds, categories where applicable, and explicitly defined decimal precision. Do not round, truncate, convert units, or substitute another authority.
4. **Evidence preparation:** Create a candidate immutable evidence record bound to the exact pipeline revision, target context, array index, and ObservationVariable reference. Capture the relevant Scale projection and source retrieval/validation timestamps.
5. **Atomic publication:** Persist the evidence record with the immutable published revision and current-pointer change in the same database transaction/atomic commit boundary. The external fetch is performed before the transaction; persistence of the evidence record, revision append, current-pointer transition, and any required audit/outbox item must commit or roll back together.
6. **Failure:** If dereferencing or validation fails, leave the workstream's current pointer and revision history unchanged. The draft remains a draft. Do not persist a successful evidence record.
7. **Later source change:** Never mutate a previously published revision or its evidence. A new published revision resolves and records the then-observed Scale under a new evidence identity. Historical readers can still interpret the prior target using its prior projection.
8. **Replay:** Apply D-BP-14 replay precedence and D-24's fresh-authorization-before-disclosure requirement. An identical immutable revision replay returns its already-bound evidence; it does not create a second evidence record or silently fetch a new Scale and rewrite history.

The required reference field/link from a pipeline revision to its evidence record, evidence-record endpoint (if any), identifier namespace, correction relationship, and persistence location are not selected here.

## 6. Candidate validation semantics requiring explicit treatment

- minimumValue and maximumValue are candidate inclusive bounds and must be parsed as decimal strings, not binary floating-point numbers.
- A non-numerical dataType cannot satisfy a quantitative threshold/range.
- When validValues.categories governs the Scale, accepted values must match the permitted category values; the field must not be treated as an unrestricted interval.
- If decimalPlaces is null or absent, the Scale has not specified a precision limit; the validator must not invent one.
- For exact-decimal strings, the candidate profile counts all fractional digits, including trailing zeroes, against an explicit decimalPlaces value. This is a proposed lexical rule, not a ratified scientific policy.
- A JSON number does not reliably preserve the source lexical number of decimal places after parsing/canonicalization. Whether a target must use exactDecimal whenever the Scale declares decimalPlaces, or whether canonical numeric value precision is sufficient, remains an explicit decision.
- units are not inferred. No unit conversion is performed. A missing unit is recorded as missing/null and remains a source-definition limitation.

## 7. Immutability, correction, and retention

A successfully published evidence record is immutable and append-only. It must not be edited or deleted in place. A demonstrably incorrect evidence record is corrected by appending a new record with a distinct identity and an explicit correction/supersession link once that relationship is approved. The original remains available as historical evidence.

Retention duration, archival policy, source revalidation cadence, and the definition of “fresh enough” at publication are unresolved. A later remote Scale change does not rewrite past evidence. It affects future publication validation and may require a new pipeline revision.

## 8. Security and trust boundaries

The evidence record is not proof that an authority is trusted. Before runtime dereferencing is enabled, the implementation needs an approved authority onboarding/trust model and outbound-request controls covering DNS rebinding, private/link-local address access, redirects, proxies, response size, timeouts, and credential handling. User-supplied URIs must never become unrestricted server-side fetch targets.

No credentials, bearer tokens, cookies, or authorization headers are stored in the Scale projection or fingerprint preimage. The actor/tenant audit fields and delegation semantics remain governed separately by D-22 and RFC-154 §12.10.

## 9. Reuse and non-reuse

Do not reuse PipelineProvenance for this record: that resource is specifically described as Genotyping bioinformatics pipeline-run provenance. Do not assume the current generic ProvenanceEnvelope alone is sufficient; it may ultimately carry a link to this artifact, but the typed target binding and snapshot semantics must be defined first.

This model creates no new public endpoint, response schema, or required field on BreedingPipelineRevision. The link/storage/API decision remains open pending maintainer review.

## 10. Required decisions and evidence

Before normative promotion, the maintainer must decide:

1. evidence-record identity and whether it is a separate resource or a linked immutable provenance artifact;
2. the exact revision-to-evidence reference location and retrieval operation, if any;
3. cryptographic hash algorithm and external digest envelope, separate from D-02's approved JCS method;
4. trusted authority onboarding and outbound-request policy;
5. freshness/revalidation rule and how to treat remote Scale changes;
6. decimal precision treatment for JSON-number targets and trailing zeroes in exact-decimal strings;
7. evidence retention, correction, and actor/audit requirements;
8. independent-service atomicity and remote-reference conformance evidence.

Until those decisions are made, the model is a candidate engineering design, not an accepted public contract.
