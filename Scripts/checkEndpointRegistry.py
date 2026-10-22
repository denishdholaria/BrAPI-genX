#!/usr/bin/env python3
"""Validate identity, completeness, crosswalk integrity, and semantic links in the master endpoint registry."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "Specification" / "ENDPOINT-REGISTRY.json"
EXPECTED_V21 = 201
EXPECTED_GENX = 21
DOMAINS = {f"D{i}" for i in range(1, 8)}
CAPABILITIES = {f"C{i}" for i in range(1, 10)}


def norm_route(path: str) -> str:
    return re.sub(r"\{[^{}]+\}", "{}", path.rstrip("/")) or "/"


def check() -> list[str]:
    errors: list[str] = []
    try:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Cannot load valid JSON registry: {exc}"]

    entries = registry.get("entries")
    if not isinstance(entries, list):
        return ["Registry field 'entries' must be a list."]
    v21 = [e for e in entries if e.get("apiGeneration") == "brapi-v2.1"]
    genx = [e for e in entries if e.get("apiGeneration") == "genx-v3"]
    unknown_generations = [e.get("apiGeneration") for e in entries
                           if e.get("apiGeneration") not in {"brapi-v2.1", "genx-v3"}]
    if unknown_generations:
        errors.append(f"Unknown API generations found: {unknown_generations[:5]}")
    if len(v21) != EXPECTED_V21:
        errors.append(f"Expected {EXPECTED_V21} BrAPI v2.1 entries, found {len(v21)}.")
    if len(genx) != EXPECTED_GENX:
        errors.append(f"Expected {EXPECTED_GENX} GenX entries, found {len(genx)}.")
    if len(entries) != EXPECTED_V21 + EXPECTED_GENX:
        errors.append(f"Expected {EXPECTED_V21 + EXPECTED_GENX} total entries, found {len(entries)}.")

    catalog_ids: list[str] = []
    recommended_ids: list[str] = []
    full_routes: list[str] = []
    source_operation_ids: list[str] = []
    id_to_entry: dict[str, dict] = {}

    for e in entries:
        cid = e.get("catalogId")
        if not isinstance(cid, str) or not cid.strip():
            errors.append(f"Entry has missing catalogue ID: {e.get('method')} {e.get('path')}")
        else:
            catalog_ids.append(cid)
            if cid in id_to_entry:
                errors.append(f"Duplicate catalogue ID: {cid}")
            id_to_entry[cid] = e
            if e.get("apiGeneration") == "brapi-v2.1" and not cid.startswith("brapi-den.brapi-v2-1."):
                errors.append(f"v2.1 entry uses unexpected catalogue namespace: {cid}")
            if e.get("apiGeneration") == "genx-v3" and not cid.startswith("brapi-den.genx.v3."):
                errors.append(f"GenX entry uses unexpected catalogue namespace: {cid}")

        method, path, base = e.get("method"), e.get("path"), e.get("basePath")
        if not isinstance(method, str) or method.upper() != method:
            errors.append(f"{cid}: method must be a non-empty uppercase HTTP method.")
        if not isinstance(path, str) or not path.startswith("/"):
            errors.append(f"{cid}: path must be a relative route template starting with '/'.")
        if not isinstance(base, str) or not base.startswith("/"):
            errors.append(f"{cid}: basePath must be recorded and start with '/'.")
        if isinstance(method, str) and isinstance(path, str) and isinstance(base, str):
            full_routes.append(f"{base} {method} {norm_route(path)}")

        opid = e.get("operationIdInSource")
        recid = e.get("recommendedOperationId")
        if not isinstance(recid, str) or not recid.strip():
            errors.append(f"{cid}: recommendedOperationId is missing.")
        else:
            recommended_ids.append(recid)
        if e.get("apiGeneration") == "brapi-v2.1":
            if opid is not None:
                errors.append(f"{cid}: the inspected v2.1 source should be recorded with null operationIdInSource; do not silently rewrite frozen source contracts.")
            if not str(recid).startswith("brapiV21"):
                errors.append(f"{cid}: v2.1 recommendedOperationId must be clearly separated from GenX names.")
        elif e.get("apiGeneration") == "genx-v3":
            if not isinstance(opid, str) or not opid.startswith("genx"):
                errors.append(f"{cid}: GenX source operationId must be explicitly present and begin with 'genx'.")
        if opid:
            source_operation_ids.append(opid)

        for field in ("operationName", "purpose", "sideEffects", "idempotency",
                      "standardStatus", "implementationStatus", "semanticReviewStatus"):
            if not isinstance(e.get(field), str) or not e[field].strip():
                errors.append(f"{cid}: required field {field} is missing.")
        for field in ("canBeUsedFor", "mustNotBeUsedFor"):
            if not isinstance(e.get(field), list) or not e[field]:
                errors.append(f"{cid}: {field} must be a non-empty list.")
        src = e.get("source")
        if not isinstance(src, dict) or not isinstance(src.get("path"), str) or not src.get("path"):
            errors.append(f"{cid}: source repository path is missing.")
        elif not (ROOT / src["path"]).is_file():
            errors.append(f"{cid}: source file does not exist in this checkout: {src['path']}")

        cl = e.get("classification")
        if not isinstance(cl, dict):
            errors.append(f"{cid}: classification object is missing.")
        else:
            domain = cl.get("primaryDomain")
            if domain is not None and domain not in DOMAINS:
                errors.append(f"{cid}: invalid primaryDomain {domain!r}.")
            for cap in cl.get("crossCuttingCapabilities", []):
                if cap not in CAPABILITIES:
                    errors.append(f"{cid}: invalid cross-cutting capability {cap!r}.")
            for d in cl.get("contextualDomains", []):
                if d not in DOMAINS:
                    errors.append(f"{cid}: invalid contextual domain {d!r}.")

        cw = e.get("bijmantraCrosswalk")
        if not isinstance(cw, dict):
            errors.append(f"{cid}: BijMantra crosswalk evidence object is missing.")
        elif e.get("apiGeneration") == "brapi-v2.1":
            candidates = cw.get("staticPythonDeclarations")
            if not isinstance(candidates, list):
                errors.append(f"{cid}: staticPythonDeclarations must be a list.")
            else:
                if cw.get("candidateCount") != len(candidates):
                    errors.append(f"{cid}: candidateCount disagrees with staticPythonDeclarations.")
                direct = sum(1 for c in candidates if c.get("candidateRole") == "brapi-adapter-source-declaration")
                if cw.get("directBrApiAdapterDeclarationCount") != direct:
                    errors.append(f"{cid}: BrAPI-specific declaration count is inconsistent.")
            if cw.get("runtimeAvailability") != "not-verified":
                errors.append(f"{cid}: runtime availability must remain not-verified.")
        elif e.get("apiGeneration") == "genx-v3":
            if not isinstance(cw.get("relativePathCandidates"), list):
                errors.append(f"{cid}: GenX relativePathCandidates must be a list.")

        for ref in e.get("semanticNeighborCatalogIds", []):
            if ref not in id_to_entry and ref not in catalog_ids:
                # Forward references are checked again after all entries.
                pass

    def duplicates(values: list[str]) -> list[str]:
        return sorted(k for k, count in Counter(values).items() if count > 1)
    for name, values in [
        ("catalogId", catalog_ids),
        ("recommendedOperationId", recommended_ids),
        ("source operationId", source_operation_ids),
        ("full base-path/method/route", full_routes),
    ]:
        for duplicate in duplicates(values):
            errors.append(f"Duplicate {name}: {duplicate}")

    all_catalog_ids = set(catalog_ids)
    relationships = registry.get("semanticRelationships")
    if not isinstance(relationships, list):
        errors.append("semanticRelationships must be a list.")
        relationships = []
    relationship_ids = [r.get("id") for r in relationships]
    for dup in duplicates([x for x in relationship_ids if isinstance(x, str)]):
        errors.append(f"Duplicate semantic relationship ID: {dup}")
    relationship_id_set = set(relationship_ids)
    for relation in relationships:
        for ref in relation.get("brapiV21CatalogIds", []) + relation.get("genxCatalogIds", []):
            if ref not in all_catalog_ids:
                errors.append(f"Relationship {relation.get('id')} references unknown catalogue ID {ref}.")
    for e in entries:
        for ref in e.get("semanticNeighborCatalogIds", []):
            if ref not in all_catalog_ids:
                errors.append(f"{e.get('catalogId')} references unknown semantic neighbor catalogue ID {ref}.")
        for ref in e.get("semanticNeighborIds", []):
            if str(ref).startswith(("SEM-", "OVERLAP-")) and ref not in relationship_id_set:
                errors.append(f"{e.get('catalogId')} references unknown semantic relationship {ref}.")

    bi = registry.get("buildIntegrity", {})
    if bi.get("brapiV21InventoryRows") != EXPECTED_V21:
        errors.append("buildIntegrity.brapiV21InventoryRows must be 201.")
    if bi.get("brapiV21EntriesAdded") != EXPECTED_V21:
        errors.append("buildIntegrity.brapiV21EntriesAdded must be 201.")
    if bi.get("genxEntriesAdded") != EXPECTED_GENX:
        errors.append("buildIntegrity.genxEntriesAdded must be 21.")
    if bi.get("unmatchedV21InventoryRows") != []:
        errors.append("Some BrAPI v2.1 inventory rows did not resolve to a source specification operation.")
    if bi.get("duplicateCatalogIds") != [] or bi.get("duplicateMethodRouteKeys") != []:
        errors.append("Registry build-integrity duplicate lists must be empty.")
    if bi.get("catalogIdsUnique") is not True:
        errors.append("Registry buildIntegrity.catalogIdsUnique is not true.")
    if bi.get("fullBasePathMethodRouteKeysUnique") is not True:
        errors.append("Registry buildIntegrity.fullBasePathMethodRouteKeysUnique is not true.")
    if bi.get("recommendedOperationIdsUnique") is not True:
        errors.append("Registry buildIntegrity.recommendedOperationIdsUnique is not true.")
    cross = bi.get("v21PythonCrosswalk", {})
    if cross.get("endpointsWithAnyExactRouteDeclaration", 0) + cross.get("endpointsWithoutExactRouteDeclaration", 0) != EXPECTED_V21:
        errors.append("BijMantra exact-match and unmatched counts do not reconcile to all v2.1 entries.")
    if cross.get("endpointsWithBrapiSpecificStaticSource", 0) > cross.get("endpointsWithAnyExactRouteDeclaration", 0):
        errors.append("BrAPI-specific static source count cannot exceed all exact route matches.")

    return errors


def main() -> int:
    errors = check()
    if errors:
        print("Endpoint registry validation failed:")
        for error in errors:
            print("- " + error)
        return 1
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    print("Endpoint registry passed structural checks: 201 BrAPI v2.1 entries, 21 proposed GenX entries, unique identities/routes, complete source links, and resolved semantic-neighbor IDs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
