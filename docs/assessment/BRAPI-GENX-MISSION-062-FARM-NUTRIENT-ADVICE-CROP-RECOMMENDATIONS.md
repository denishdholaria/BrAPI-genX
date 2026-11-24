# Mission 062 — Farm authority and crop/nutrient recommendation boundaries

**Prepared parent:** `3c83be9f4ac705febd0145a9a83bfed2529ef664`.

Three source-backed candidate group descriptions explain that farm membership is not a surveyed legal boundary, nutrient advisory strings are not calibrated or actionable fertilizer rates, and crop recommendations do not establish named germplasm identity or scientific efficacy. All three are `STRUCTURAL_DRAFT` proposals with decisions D-205–207, D-394–396 and D-385–387 unratified.

The source OpenAPI operations use `/nutrient-advices`; RFC-132 incorrectly used `/nutrient-advice`, so its prose and endpoint naming were corrected without changing the wire schema or endpoint registry. RFC-069's claim that overlapping location membership can be explicitly recorded was qualified: the current Farm schema has no such overlap proof field.

Added group-description pinning and two targeted regression guards. All new local evidence paths resolved against the parent repository tree. Hosted tests must run before full verification can be reported; no official BrAPI changes, candidate schema changes, or scientific/normative promotions.
