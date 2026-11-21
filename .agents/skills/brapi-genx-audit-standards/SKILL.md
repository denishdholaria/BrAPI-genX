---
name: brapi-genx-audit-standards
description: Audit standards reuse, overlapping contracts, or claims of novelty in BrAPI-GenX before drafting or extending an interoperability contract.
---

# Audit standards reuse

Start with one exchange an independent consumer needs to perform. State which
meaning it must recover and which source owns the underlying record. Use the
[repository instructions](../../../AGENTS.md) and the applicable parts of the
[specification quality standard](../../../docs/governance/BRAPI-GENX-SPECIFICATION-QUALITY-STANDARD.md).

## Compare the contracts

1. Trace the exchange through the released BrAPI v2.1 operation and its
   request or response schema. Resolve `$ref` and `allOf`, including shared
   components. The [endpoint registry](../../../Specification/ENDPOINT-REGISTRY.json)
   helps locate source files. Use the released contract to settle wire details.
2. Search for a generic operation or resource that can carry the use case.
   Assess the data model and read and write support separately. For example,
   BrAPI v2.1 [Event](../../../Specification/BrAPI-Phenotyping/Events/Schemas/Event.yaml)
   can carry applied irrigation and affected observation units.
   [GET /events](../../../Specification/BrAPI-Phenotyping/Events/Events_GET.yaml)
   is evidence of a read operation. Check write capabilities independently.
3. Compare the relevant companion standard, upstream proposal, and existing
   GenX draft. Cite the exact version, field, and source. Trace identifiers to
   their issuing authority. Where the examples depend on quantities, time,
   or space, check their units, basis, time window, and spatial scope.
4. Walk a minimal example through the existing contracts. Identify the first
   specific fact the receiver cannot recover. Distinguish a structural error
   from an incorrect real-world assertion. A valid plot identifier on an
   irrigation event can still be factually wrong. Detecting that requires
   independent evidence of which plot was irrigated.

## Deliver the finding

For each material finding, give the source evidence, what transfers, what is
ambiguous or lost, and a check another implementation could reproduce.
Recommend reuse, mapping clarification, a demonstrated extension, or deferral.
For an extension, explain how the smallest proposed change preserves the
original source authority. If a claim still depends on an unverified
assumption, name the sample, standard, or decision needed to resolve it.
