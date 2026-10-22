Next-generation BrAPI design surface. **Proposal status: not accepted, not normative.**

- BrAPI V2.1 (`BrAPI-Core`, `BrAPI-Phenotyping`, `BrAPI-Genotyping`, `BrAPI-Germplasm`) stays frozen. Nothing in this directory changes V2.1 behavior.
- GenX objects are additive and optional.
- Start point: [RFC-001-GenX-Skeleton](./RFC-001-GenX-Skeleton.md).
- Wiring into `generator/` and `BrAPI-Schema/` remains deferred pending decision.
- **Scientific classification proposal:** [CLASSIFICATION.md](./CLASSIFICATION.md) proposes a seven-domain taxonomy distinct from shared contract mechanisms. The machine-readable registry is [Conformance/domain-classification.yaml](./Conformance/domain-classification.yaml). Neither is community-ratified.

See also: [DECISIONS.md](./DECISIONS.md), [ENDPOINT-IDENTITY.md](./ENDPOINT-IDENTITY.md), and [ADOPTION.md](./ADOPTION.md).