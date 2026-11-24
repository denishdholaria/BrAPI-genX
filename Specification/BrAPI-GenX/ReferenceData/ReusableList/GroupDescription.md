# Group ReusableList

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 090; not a replacement for the official Breeding Application Programming Interface (BrAPI) version 2.1 `List` resource.

The candidate `ReusableList` record provides a namespaced `reusableListDbId` and lifecycle `status` (`active`, `superseded`, `withdrawn`) with optional list/cohort `name`, a `members` array of strings, `supersedes`, and provenance. Proposed operations register, list with optional status filter, and retrieve a candidate record. The same-identity replay rule is proposed behavior, not independently verified durability.

**Boundaries:** Official BrAPI already supports general item lists via `/brapi/v2/lists`. The GenX draft does not define an interoperable translation to `listDbId`, type checks for membership, a pinned biological identity, or a reason official lists cannot satisfy the workflow. Member strings have no enforced Germplasm or Sample resource identity (D-270). Name/membership requiredness remains undecided (D-268–D-269). Neither cohort membership nor list name demonstrates scientific selection validity or access entitlement.

**Sources:** [GenX module overview](./README.md), [candidate list schema](./Schemas/ReusableList.yaml), [registration schema](./Schemas/ReusableListNewRequest.yaml), [draft operations](./ReusableList_GET_POST.yaml), [RFC-090](../../RFCs/RFC-090-Reusable-List.md), [official BrAPI Lists](../../../BrAPI-Core/Lists/README.md), and [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
