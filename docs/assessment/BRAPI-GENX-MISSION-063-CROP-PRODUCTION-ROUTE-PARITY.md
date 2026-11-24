# Mission 063 — CropProduction source-to-RFC route parity regression

**Prepared parent:** `bc10cc93e6fb20f5b49c6b32304589572c6a53ba`.

A complete source review of the 16 CropProduction modules found the README/RFC routes and operation identifiers consistent after the editorial corrections in Missions 060 and 062. Before that, RFC-131 and RFC-132 each named singular routes absent from their actual OpenAPI operations.

A new test pins all 16 module-to-RFC identities. For each module, it extracts documented HTTP method, GenX v1 route and operation identifier pairs from both README and RFC text. It independently parses the module's direct OpenAPI YAML operations and requires all three sets to match exactly. It refuses empty documentation sets and detects missing or invented operations.

This regression check will run through the existing `Scripts/test_genx_group_descriptions.py` hosted conformance step. It does not certify candidate behavior, semantic equivalence, or independent implementation. No wire contract, endpoint registry, generated catalogue, official BrAPI sources or maturity decision changes.

Hosted tests must complete on the integrated commit before full acceptance.
