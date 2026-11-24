#!/usr/bin/env python3
"""Verify documentary traceability of reviewed semantic neighbors.

File presence is evidence hygiene, not proof of a scientific mapping.
The existing semantic-neighbor governance validator owns identity, status,
and transition controls.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

LEDGER = Path('Specification/BrAPI-GenX/Conformance/semantic-neighbor-review.yaml')
REVIEWED = {'requires-decision', 'evidence-backed-proposed'}


def check(root: Path) -> tuple[list[str], int]:
    errors: list[str] = []
    data = yaml.safe_load((root / LEDGER).read_text(encoding='utf-8'))
    if not isinstance(data, dict) or not isinstance(data.get('entries'), list):
        return ['Ledger must contain an entries list'], 0

    reviewed = 0
    root = root.resolve()
    for entry in data['entries']:
        if not isinstance(entry, dict):
            errors.append('Ledger entry is not a mapping')
            continue
        if entry.get('reviewStatus') not in REVIEWED:
            continue
        reviewed += 1
        identity = entry.get('id', '<unknown>')
        sources = entry.get('documentaryEvidence')
        if not isinstance(sources, list) or not sources:
            errors.append(f'{identity}: reviewed entry requires documentaryEvidence list')
            continue
        source_module = entry.get('sourceModule')
        target_module = entry.get('targetModule')
        if not isinstance(source_module, str) or not source_module:
            errors.append(f'{identity}: missing sourceModule')
        if not isinstance(target_module, str) or not target_module:
            errors.append(f'{identity}: missing targetModule')
        found_source = found_target = found_assessment = False
        seen: set[str] = set()
        for raw in sources:
            if not isinstance(raw, str) or not raw.strip():
                errors.append(f'{identity}: documentaryEvidence contains empty/non-string path')
                continue
            if raw in seen:
                errors.append(f'{identity}: repeated documentaryEvidence path: {raw}')
            seen.add(raw)
            path = Path(raw)
            if path.is_absolute() or '..' in path.parts:
                errors.append(f'{identity}: documentaryEvidence must be a repository-relative path: {raw}')
                continue
            resolved = (root / path).resolve()
            if not resolved.is_relative_to(root) or not resolved.is_file():
                errors.append(f'{identity}: documentaryEvidence file missing/outside repository: {raw}')
                continue
            parts = path.parts
            is_schema = (
                len(parts) >= 6
                and parts[0:2] == ('Specification', 'BrAPI-GenX')
                and parts[-2] == 'Schemas'
                and path.suffix in ('.yaml', '.yml')
            )
            if is_schema:
                found_source |= parts[-3] == source_module
                found_target |= parts[-3] == target_module
            found_assessment |= parts[:2] == ('docs', 'assessment') and path.suffix == '.md'
        if not found_source:
            errors.append(f'{identity}: missing existing source-module schema evidence')
        if not found_target:
            errors.append(f'{identity}: missing existing target-module schema evidence')
        if not found_assessment:
            errors.append(f'{identity}: missing existing assessment document evidence')
        if entry.get('reviewStatus') == 'requires-decision':
            if not isinstance(entry.get('rationale'), str) or not entry['rationale'].strip():
                errors.append(f'{identity}: requires-decision without rationale')
            if not isinstance(entry.get('openQuestion'), str) or not entry['openQuestion'].strip():
                errors.append(f'{identity}: requires-decision without openQuestion')
    return errors, reviewed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        errors, reviewed = check(args.root)
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        print(f'FAIL: unable to read semantic-neighbor evidence: {exc}')
        return 1
    if errors:
        for error in errors:
            print(f'FAIL: {error}')
        return 1
    print(f'PASS: reviewed semantic-neighbor source/target/assessment evidence ({reviewed} entries); no scientific endorsement')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
