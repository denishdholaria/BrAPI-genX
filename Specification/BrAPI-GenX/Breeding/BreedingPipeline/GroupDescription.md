# Group BreedingPipeline

**Status:** BrAPI-GenX *candidate* architecture; RFC-154 is not a normative or independently conformance-verified standard. The internal D-BP-14 Compare-and-Set concurrency profile is ratified as a **candidate design**, not as proof of service behavior.

A `BreedingPipeline` represents a stable breeding workstream associated with an authority-qualified BrAPI Program reference. Changes to its planning configuration are expressed as immutable `BreedingPipelineRevision` records. Embedded breeding-scheme versions describe design-time stages and transitions; execution facts remain separate. Actual germplasm, pedigree, crosses, trials, studies and observations retain their official BrAPI resource ownership.

**Established design boundaries:** a new version has a distinct immutable version identity; its published-current pointer is subject to the accepted D-BP-14 optimistic Compare-and-Set candidate. A draft append does not move that published pointer. An identical revision replay is evaluated before a now-stale pointer precondition; different content under the same version identity conflicts. Target contexts distinguish directional Trait references from quantitative ObservationVariable references, whose authoritative Scale constrains units and measurement interpretation.

**Still unresolved:** independent persistence-backed concurrency evidence; publication/withdrawal authority and cross-organisation access; remote Scale resolution and evidence retention; final compatibility and normative promotion. Do not describe the module as a production scheduling service or infer scientific equivalence from operation-neighbor metadata.

**Sources:** [Detailed module design](./README.md), [revision schema](./Schemas/BreedingPipeline.yaml), [candidate operations](./BreedingPipeline_GET_POST.yaml), [canonical RFC-154](../../RFCs/RFC-154-BreedingPipeline.md), and [CAS behavioral acceptance plan](../../../../docs/assessment/BRAPI-GENX-BREEDING-PIPELINE-CAS-BEHAVIORAL-TEST-PLAN.md).
