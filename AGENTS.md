# BrAPI-GenX agent instructions

## Purpose and authority

BrAPI-GenX is an independently governed specification and conformance project.
Extend interoperability from official BrAPI v2.1 and established agricultural
standards toward a broader agricultural knowledge fabric. Preserve the
identity, authority, context, and provenance of the original records.

Follow the current maintainer instruction and applicable accepted decisions.
The principal architect scopes work and reviews evidence. The maintainer has
final authority for scientific policy, normative specifications, and
compatibility decisions. Use the [project decision authority](docs/governance/BRAPI-GENX-PROJECT-DECISION-AUTHORITY.md),
[maturity register](docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md),
and [decision log](Specification/BrAPI-GenX/DECISIONS.md). A passing prototype
or fixture does not change an RFC's maturity.

When working inside the BijMantra consolidation workspace, also read the
parent `AGENTS.md` for cross-workspace boundaries. BijMantra implementations
and the Ambika catalogue supply requirements and comparative evidence.

## Local workflow

- Work on local `main` for routine changes. Use a separate branch for risky
  or experimental work where isolation helps, or when the maintainer asks.
  The maintainer handles backups of `main`.
- Check the working tree and inspected commit before editing. Preserve
  existing local work and keep the change within the assigned slice.
- State one observable outcome and how it will be verified. Inspect the
  relevant contracts, consumers, and tests before changing them.
- Follow the maintainer's authorization for pushes, pull requests, and
  merges. Report the exact commit or working-tree state at handoff.

## Standards reuse and novelty

Before proposing a resource, field, or operation:

1. Name a scientific exchange or workflow that loses meaning today. Cite a
   documented failure, relevant research, or a reproducible example. Label
   claims that still need verification as hypotheses.
2. Inspect the published BrAPI v2.1 operations and resolved OpenAPI schemas.
   Check relevant upstream proposals and companion standards, recording
   versions and maturity. Use draft material with its stated status.
3. Identify what can be reused or clarified through a mapping or profile.
   Make each resource's authoritative source and identifier scope explicit.
   The absence of a specialized endpoint is insufficient evidence of a gap.
4. Propose the smallest compatible extension only for a demonstrated gap.
   Define how an independent implementation could verify its behavior.

Apply the [specification quality standard](docs/governance/BRAPI-GENX-SPECIFICATION-QUALITY-STANDARD.md)
to the scope of the change. Keep experimental design, actual interventions,
observations, and derived results distinct when they describe different
scientific facts. Record units, spatial and temporal context, provenance,
and uncertainty where interpretation depends on them.

## Layout and compatibility

- Follow the [identity standard](docs/project/PROJECT_IDENTITY.md).
  GenX-native operations use `/genx/v1/`. Reserve official BrAPI names,
  version identifiers, and routes for their published meanings.
- Preserve the released BrAPI v2.1 source contracts in
  `Specification/BrAPI-Core/`, `Specification/BrAPI-Germplasm/`,
  `Specification/BrAPI-Genotyping/`, and `Specification/BrAPI-Phenotyping/`.
  Treat generated files as derived output and trace wire-contract claims
  to the released source.
- Use the [GenX specification index](Specification/BrAPI-GenX/README.md)
  to place contracts under `Specification/BrAPI-GenX/<Section>/<Module>/`.
  Keep operations, schemas, and module documentation together. Folder
  placement is for navigation. Scientific ownership and facets are recorded
  in the [module registry](Specification/BrAPI-GenX/Conformance/domain-classification.yaml).
- Preserve stable identifiers. When the task changes an operation or a source
  path, update the [endpoint registry](Specification/ENDPOINT-REGISTRY.json)
  and regenerate affected catalogues with `Scripts/generateEndpointArtifacts.py`.
  Use the [numbered RFC index](Specification/BrAPI-GenX/RFCs/README.md) for
  design proposals.

## Local verification and handoff

Use the relevant local checks. The [static conformance workflow](.github/workflows/genx-static-conformance.yml)
records the test dependencies and the broader suite.

```sh
python3 Scripts/checkEndpointRegistry.py
python3 Scripts/checkGenXEndpointCatalog.py
python3 Scripts/generateEndpointArtifacts.py --check
python3 Scripts/checkGenXConformance.py
```

Run the contract-specific fixtures or tests where the slice calls for them.
Record the inspected SHA, changed files, exact commands and results, skipped
checks, and unresolved decisions. State whether the evidence covers schema
validation, fixtures, the in-memory reference server, or an independent
implementation. Claims about hosted checks require a recorded run that
actually executed.
