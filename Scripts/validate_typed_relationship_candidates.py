#!/usr/bin/env python3
"""Validate proposal-only scientific relationship records; never promote them.

Navigational semanticNeighborIds stay separate and are never an input here.
"""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re
from typing import Any

import yaml

REL = Path('Specification/BrAPI-GenX/Conformance/typed-relationship-candidates.yaml')
TYPES = frozenset({'typed-resource-reference', 'provenance-derivation',
                   'operation-contract-equivalence'})
REQUIRED = frozenset({'candidateId', 'status', 'relationKind', 'sourceSchema',
                      'targetSchema', 'claim', 'evidenceRefs', 'unresolvedQuestions',
                      'proposedBy', 'proposedAt'})
ID = re.compile(r'SCI-REL-[0-9]{4,}')


def valid_path(value: Any, root: Path | None) -> bool:
    if not isinstance(value, str) or not value.startswith('Specification/') or '\\' in value:
        return False
    path = Path(value)
    if path.is_absolute() or '..' in path.parts or path.suffix not in {'.yaml', '.yml'}:
        return False
    return root is None or (root / path).is_file()


def check(document: Any, *, root: Path | None = None) -> list[str]:
    if not isinstance(document, dict) or set(document) != {'schemaVersion', 'entries'}:
        return ['candidate register must contain only schemaVersion and entries']
    if type(document['schemaVersion']) is not int or document['schemaVersion'] != 1:
        return ['schemaVersion must be integer 1']
    if not isinstance(document['entries'], list):
        return ['entries must be a list']
    errors: list[str] = []
    seen: set[str] = set()
    for index, record in enumerate(document['entries']):
        key = f'candidate[{index}]'
        if not isinstance(record, dict):
            errors.append(f'{key}: must be a mapping')
            continue
        if set(record) != REQUIRED:
            errors.append(f'{key}: unexpected or missing candidate fields')
        identifier = record.get('candidateId')
        if not isinstance(identifier, str) or not ID.fullmatch(identifier):
            errors.append(f'{key}: invalid candidateId')
        elif identifier in seen:
            errors.append(f'{key}: duplicate candidateId')
        else:
            seen.add(identifier)
        if record.get('status') != 'proposal-only':
            errors.append(f'{key}: only proposal-only status is permitted')
        if record.get('relationKind') not in TYPES:
            errors.append(f'{key}: unsupported scientific relationKind')
        for field in ('sourceSchema', 'targetSchema'):
            if not valid_path(record.get(field), root):
                errors.append(f'{key}: {field} must resolve to a repository-local schema YAML')
        for field in ('claim', 'proposedBy'):
            if not isinstance(record.get(field), str) or not record[field].strip():
                errors.append(f'{key}: {field} must be a nonempty string')
        for field in ('evidenceRefs', 'unresolvedQuestions'):
            value = record.get(field)
            if (not isinstance(value, list) or not value or
                    any(not isinstance(x, str) or not x.strip() for x in value) or
                    len(value) != len(set(x for x in value if isinstance(x, str)))):
                errors.append(f'{key}: {field} requires distinct nonempty strings')
        stamp = record.get('proposedAt')
        if not isinstance(stamp, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', stamp):
            errors.append(f'{key}: proposedAt must be a YYYY-MM-DD string')
        else:
            try:
                date.fromisoformat(stamp)
            except ValueError:
                errors.append(f'{key}: proposedAt must be a calendar date')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        doc = yaml.safe_load((args.root / REL).read_text(encoding='utf-8'))
        errors = check(doc, root=args.root)
    except (OSError, UnicodeError, yaml.YAMLError, ValueError) as exc:
        print('FAIL: could not validate candidate register: ' + str(exc))
        return 1
    for message in errors:
        print('FAIL: ' + message)
    if errors:
        return 1
    print(f"PASS: {len(doc['entries'])} structural scientific-relationship candidates; NONE authorized or normative")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
