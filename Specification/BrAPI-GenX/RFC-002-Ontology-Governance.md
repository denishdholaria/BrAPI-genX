# RFC-002: Ontology Term Governance

- Status: **proposal** (not accepted, not normative, grants no implementation authority)
- Builds on: RFC-001 (compatibility law, `ProvenanceEnvelope`, `409` conflict evidence)
- Scope: versioned, namespaced observation-variable terms with conflict rejection
- Non-scope: full Trait/Method/Scale lifecycle, ontology merging, term mappings,
  Crop Ontology alignment — each needs its own RFC

## 1. Problem

Field evidence shows observation-variable identifiers treated as globally
unique while writes from one organization silently overwrite another's
definitions. A shared variable ID with divergent meaning corrupts every
downstream observation, analysis, and prediction without any party noticing.
Governance must make three states distinguishable on the wire: a new term, a
new version of a known term, and a conflicting redefinition (rejected, never
merged silently).

## 2. Object — VariableTerm

Files: `Ontology/Schemas/VariableTerm.yaml`,
`Ontology/Schemas/VariableTermNewRequest.yaml`,
`Ontology/Variables_GET_POST.yaml`,
`Ontology/Variables_VariableDbId_GET.yaml`.

Purpose: give every variable term a namespaced identity, an explicit version,
and a lifecycle state, so redefinition is a visible `409`, not a silent
overwrite.

Fields: `variableDbId` (`{authority}:{type}:{localId}`, required),
`variableName`, `traitDbId`, `traitVersion?`, `methodDbId`, `methodVersion?`,
`scaleDbId`, `scaleVersion?`, `version` (term version, opaque string,
required), `status` (`active`|`deprecated`), `supersededBy?`
(`variableDbId` of the replacement term, same authority),
`ontologyDbId?`, `documentationURL?`, `provenance?`
(`ProvenanceEnvelope` from RFC-001 — who authored this definition and from
what evidence).

Responsibilities: identity, versioning, deprecation links for variable terms.
Non-responsibilities: defining Trait/Method/Scale objects themselves (their
DbIds are references here); ontology merging or cross-authority equivalence
(no `sameAs` in this RFC); full-text ontology search.

Invariants:

1. `variableDbId` is namespaced `{authority}:{type}:{localId}`. Unnamespaced
   IDs are rejected.
2. A published `(variableDbId, version)` pair is immutable. Same pair +
   identical body replays the existing record. Same pair + different body is
   rejected with `409` (same conflict rule as Jobs idempotency, RFC-001 §5).
3. New versions never mutate old ones. Deprecation is explicit (`status:
   deprecated` + `supersededBy`); servers perform no hidden transitions.
4. `GET /variables/{variableDbId}` without `version` returns the most recently
   created version. Version ordering semantics stay `requires decision` (§6).

## 3. Endpoints

- `POST /variables` with `VariableTermNewRequest` → `200` + single term.
  Unknown id creates; known id + new version appends; replay returns existing;
  conflict returns `409` with a plain-text body.
- `GET /variables` with `variableDbId?`, `ontologyDbId?`, `status?` filters +
  standard pagination → list of terms across versions.
- `GET /variables/{variableDbId}` with optional `version` → single term
  (latest created when omitted) or `404`.

`DELETE` is not defined: terms are deprecated, never deleted, so historical
observations keep resolvable definitions.

## 4. Hypothesis, falsifier, verification

- Hypothesis: two organizations can publish same-named variables without
  collision, and any conflicting redefinition is rejected instead of merged.
- Falsifier: a conflicting write that mutates a published version; a term
  readable under an authority that did not publish it without namespacing; a
  replay that duplicates a version.
- Verification: static probes S-09/S-10 plus live probes L-08/L-09 in
  `Conformance/probes.yaml`, executed against the reference test server.

## 5. Explicit unknowns and requires-decision

1. `requires decision`: version ordering and comparison (lexical? semantic?
   per-authority?). Omitted-`version` reads use creation recency only.
2. `requires decision`: whether Trait/Method/Scale references must themselves
   be versioned terms in a later RFC (referenced here by SHOULD-namespaced IDs).
3. `assumption`: authorities coordinate out of band on `localId` uniqueness
   within their own namespace; the wire format cannot enforce it.
4. `unknown`: real merge/mapping workflows between authorities — explicitly
   out of scope until implementer evidence exists.

## 6. File map

```text
Specification/BrAPI-GenX/
  RFC-002-Ontology-Governance.md   this document
  Ontology/README.md + GroupDescription.md
    + Schemas/VariableTerm.yaml + Schemas/VariableTermNewRequest.yaml
    + Variables_GET_POST.yaml + Variables_VariableDbId_GET.yaml
```
