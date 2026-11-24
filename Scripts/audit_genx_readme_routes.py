#!/usr/bin/env python3
"""Audit explicit GenX README endpoint claims against the endpoint registry.

README prose is non-normative. Missing claims are reported as coverage gaps;
incorrect claims can be made blocking with --strict and a chosen --module.
This tool does not change API paths, operation identifiers, or source schemas.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = Path("Specification/ENDPOINT-REGISTRY.json")
GENX = PurePosixPath("Specification/BrAPI-GenX")
CLAIM = re.compile(
    r"`(GET|POST|PUT|PATCH|DELETE)\s+(/genx/v1/[^`\s]+)`\s*\(\s*`([^`]+)`\s*\)",
    re.IGNORECASE,
)


def audit(root: Path, modules: list[str] | None = None) -> dict[str, Any]:
    errors: list[str] = []
    discrepancies: list[dict[str, str]] = []
    uncovered: list[dict[str, str]] = []
    expected: dict[str, set[tuple[str, str, str]]] = {}
    claims_checked = 0
    try:
        registry = json.loads((root / REGISTRY).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return {"claimsChecked": 0, "modulesChecked": 0, "mismatches": [],
                "uncovered": [], "errors": [f"Cannot load registry: {exc}"]}
    if not isinstance(registry, dict) or not isinstance(registry.get("entries"), list):
        return {"claimsChecked": 0, "modulesChecked": 0, "mismatches": [],
                "uncovered": [], "errors": ["Invalid endpoint registry entries"]}
    for record in registry["entries"]:
        if not isinstance(record, dict) or record.get("apiGeneration") != "genx-v1":
            continue
        source = record.get("source")
        path = source.get("path") if isinstance(source, dict) else None
        if not isinstance(path, str):
            errors.append(f"{record.get('catalogId')}: missing source path")
            continue
        source_path = PurePosixPath(path)
        if (source_path.is_absolute() or ".." in source_path.parts or
                not source_path.is_relative_to(GENX)):
            errors.append(f"{record.get('catalogId')}: unsafe source path {path}")
            continue
        parts = source_path.relative_to(GENX).parts
        if len(parts) != 3:
            errors.append(f"{record.get('catalogId')}: invalid module ownership {path}")
            continue
        module = "/".join(parts[:2])
        method = record.get("method")
        route = record.get("path")
        operation = record.get("operationIdInSource")
        if (not isinstance(method, str) or not isinstance(route, str) or
                not route.startswith("/") or not isinstance(operation, str) or
                not operation.strip()):
            errors.append(f"{record.get('catalogId')}: invalid method/path/operation")
            continue
        expected.setdefault(module, set()).add((method.upper(), "/genx/v1" + route, operation))

    requested = sorted(set(modules)) if modules is not None else sorted(expected)
    for module in requested:
        pieces = PurePosixPath(module).parts
        if (len(pieces) != 2 or ".." in pieces or module not in expected):
            errors.append(f"Unknown or unsafe GenX module: {module}")
            continue
        readme = root / GENX / module / "README.md"
        try:
            prose = readme.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{module}: cannot read README: {exc}")
            continue
        claims = [(m.group(1).upper(), m.group(2), m.group(3))
                  for m in CLAIM.finditer(prose)]
        distinct = set(claims)
        claims_checked += len(distinct)
        for method, route, operation in sorted(distinct):
            if (method, route, operation) not in expected[module]:
                discrepancies.append({"module": module, "method": method,
                                      "route": route, "operationId": operation,
                                      "reason": "not registered for this module"})
        for method, route, operation in sorted(expected[module] - distinct):
            uncovered.append({"module": module, "method": method,
                              "route": route, "operationId": operation})
    return {"claimsChecked": claims_checked,
            "modulesChecked": len([m for m in requested if m in expected]),
            "mismatches": discrepancies, "uncovered": uncovered, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--module", action="append", default=None,
                        help="Only audit this Domain/Module; repeat for more")
    parser.add_argument("--strict", action="store_true",
                        help="Fail for mismatched README claims, not absent claims")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = audit(args.root, args.module)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"README claims checked: {result['claimsChecked']}; "
              f"modules: {result['modulesChecked']}; mismatches: "
              f"{len(result['mismatches'])}; uncovered operations: "
              f"{len(result['uncovered'])}")
        for item in result['errors']:
            print("ERROR: " + item)
        for item in result['mismatches']:
            print("MISMATCH: " + json.dumps(item, sort_keys=True))
        print("README coverage gaps are advisory; endpoint contracts are authoritative.")
    return int(bool(result['errors']) or (args.strict and bool(result['mismatches'])))


if __name__ == "__main__":
    raise SystemExit(main())
