#!/usr/bin/env python3
"""Inventory executable references to semantic-neighbor metadata without asserting semantics.

This is a lexical guard for newly introduced consumer surfaces. It does not
prove that a consumer invokes an operation or that a relationship is valid.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CODE_ROOTS = ('Scripts', 'src', 'generator')
CODE_EXTENSIONS = frozenset({'.py', '.js', '.jsx', '.ts', '.tsx', '.rs', '.java', '.kt', '.go'})
REFERENCE = re.compile(r'\b(?:semanticNeighborIds|semanticNeighborCatalogIds|semanticNeighbors|registryOnlyNeighbors)\b')
REVIEWED = {
    'Scripts/auditEndpointRegistrySourceConsistency.py': 'source/registry-drift-auditor',
    'Scripts/checkEndpointRegistry.py': 'registry-structural-validator',
    'Scripts/checkGenXEndpointCatalog.py': 'source-contract-validator',
    'Scripts/check_registry_drift_regression.py': 'historical-drift-regression-validator',
    'Scripts/check_semantic_neighbor_governance.py': 'governance-validator',
    'Scripts/generateEndpointArtifacts.py': 'documentation-renderer',
    'Scripts/semantic_neighbor_lineage.py': 'governance-lineage-helper',
}
SELF = {'Scripts/report_semantic_neighbor_consumers.py',
        'Scripts/test_semantic_neighbor_consumers.py'}


def inventory(root: Path, *, reviewed: dict[str, str] | None = None) -> dict:
    approved = REVIEWED if reviewed is None else reviewed
    findings, problems = [], []
    for directory in CODE_ROOTS:
        base = root / directory
        if not base.exists():
            continue
        for path in sorted(base.rglob('*')):
            if not path.is_file() or path.suffix not in CODE_EXTENSIONS:
                continue
            rel = path.relative_to(root).as_posix()
            if rel in SELF or path.name.startswith('test_') or '__pycache__' in path.parts:
                continue
            try:
                lines = path.read_text(encoding='utf-8').splitlines()
            except (OSError, UnicodeError) as exc:
                problems.append(f'{rel}: cannot inspect source: {exc}')
                continue
            hits = [{'line': i, 'fields': sorted(set(REFERENCE.findall(line)))}
                    for i, line in enumerate(lines, 1) if REFERENCE.search(line)]
            if not hits:
                continue
            role = approved.get(rel)
            findings.append({'path': rel, 'role': role, 'hits': hits})
            if not role:
                problems.append(f'{rel}: unreviewed executable semantic-neighbor consumer')
    found = {f['path'] for f in findings}
    for path, role in sorted(approved.items()):
        if not role or path not in found:
            problems.append(f'{path}: reviewed consumer missing or no longer matches; update the inventory')
    return {'consumerCount': len(findings), 'consumers': findings,
            'problems': sorted(problems),
            'limitations': ('Literal reference scanner over executable source roots only; '
                            'does not detect indirect/dynamic access or prove semantic safety.')}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--json', action='store_true', help='print a machine-readable audit')
    args = parser.parse_args()
    result = inventory(args.root)
    if args.json:
        print(json.dumps(result, sort_keys=True, indent=2))
    else:
        print(f"Executable semantic-neighbor consumers: {result['consumerCount']}")
        for entry in result['consumers']:
            print(f"  {entry['path']}: {entry['role'] or 'UNREVIEWED'} "
                  f"({len(entry['hits'])} matching lines)")
        for error in result['problems']:
            print('FAIL: ' + error)
        print(result['limitations'])
    return int(bool(result['problems']))


if __name__ == '__main__':
    raise SystemExit(main())
