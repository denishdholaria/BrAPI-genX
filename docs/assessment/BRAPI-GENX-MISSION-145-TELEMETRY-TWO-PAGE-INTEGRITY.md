# Mission 145 — Complete telemetry pagination traversal

**Status:** implemented; hosted verification required before merge.
**Scope:** registered live probe L-28, existing runner, manifest guard and negative regressions.
**Baseline:** \`main\` at \`f389044fde13f9aeaeaf631ff98ea9a5dd571d8c\`.

## Reproducible false-positive risk

L-28 used to POST three telemetry readings, request only page zero with
\`pageSize=2\`, and verify the first two returned rows and a reported
\`totalCount=3\`. A conforming-looking but defective server could claim three
records while silently omitting or changing the unrequested third record.
The first page and its arithmetic would still pass.

This is an assurance gap in the existing conformance procedure, not evidence
for a new scientific operation or an altered pagination contract.

## Bounded correction

1. Keep the original three-point POST and captured request body.
2. Request both \`page=0&pageSize=2\` and \`page=1&pageSize=2\`.
3. Derive each expected ordered slice independently from the submitted
   sample timestamps; require the complete **two plus one** record partition.
4. Verify each page's explicit integer \`currentPage\`, \`pageSize\`,
   \`totalCount\` and \`totalPages\` against (page index, 2, 3, 2).
5. Verify every originally submitted record field, including units, quality
   and nested provenance where present, while permitting additional
   server-managed fields.
6. Reject missing, duplicated, substituted, malformed or modified rows and
   missing or inconsistent second-page metadata.
7. Guard all three registered steps and their concrete assertions in
   \`validate_probe_manifest\`. Extend existing negative regression suites;
   preserve their existing required hosted workflow commands.

## Verification

Run the repository's established required checks:

\`\`\`sh
python Scripts/test_telemetry_pagination_slice.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
\`\`\`

The hosted conformance workflow must also execute the Python live-reference
probe and independent-runtime checks, with specification generation successful
before merging. Only hosted run results may be described as passed.

## Boundaries

No published Breeding Application Programming Interface v2.1 contract,
GenX wire schema, endpoint registry, maturity level, or embargo metadata
visibility policy is changed. This verifies the page-boundary semantics
exposed by the reference implementation, not transactional snapshot isolation
under concurrent writes or arbitrary pagination depths across large datasets.
