#!/usr/bin/env python3
"""Validate a DRAFT semantic-neighbor decision candidate, never authorize it.

This schema and checker are non-normative. They cannot establish maintainer
approval and are not connected to terminal-status enforcement.
"""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re
from typing import Any

import yaml

RECORD_TYPE = 'semantic-neighbor-terminal-decision-candidate'
DRAFT_STATUS = 'draft-not-authorized'
MANDATORY = frozenset({'schemaVersion', 'recordType', 'status', 'decisionId',
                       'relationshipId', 'sourceCatalogId', 'targetOperationId',
                       'action', 'rationale', 'evidenceRefs', 'proposedBy', 'proposedAt'})
OPTIONAL = frozenset({'supersededBy'})
IDENTIFIER = re.compile(r'^SEM-CAND-[0-9]{4,}$')


def validate(record: Any, *, known_ids: set[str] | None = None) -> list[str]:
    if not isinstance(record, dict):
        return ['candidate must be a mapping']
    errors = []
    unknown = set(record) - MANDATORY - OPTIONAL
    if unknown:
        errors.append('unknown candidate fields: ' + ', '.join(sorted(map(str, unknown))))
    for key in sorted(MANDATORY - set(record)):
        errors.append(f'missing required candidate field: {key}')
    if record.get('schemaVersion') != 1 or type(record.get('schemaVersion')) is not int:
        errors.append('schemaVersion must be integer 1')
    if record.get('recordType') != RECORD_TYPE:
        errors.append('invalid recordType')
    if record.get('status') != DRAFT_STATUS:
        errors.append('candidate may only have draft-not-authorized status')
    candidate_id = record.get('decisionId')
    if not isinstance(candidate_id, str) or not IDENTIFIER.fullmatch(candidate_id):
        errors.append('decisionId must match SEM-CAND-0001 style')
    source = record.get('sourceCatalogId')
    target = record.get('targetOperationId')
    relation = record.get('relationshipId')
    if not (isinstance(source, str) and source.strip() and
            isinstance(target, str) and target.strip() and
            relation == f'{source} -> {target}'):
        errors.append('relationshipId must equal sourceCatalogId -> targetOperationId')
    if known_ids is not None and relation not in known_ids:
        errors.append('relationshipId does not exist in supplied governance ledger')
    action = record.get('action')
    if action not in ('reject', 'supersede'):
        errors.append('action must be reject or supersede')
    successor = record.get('supersededBy')
    if action == 'supersede':
        if not isinstance(successor, str) or not successor.strip() or successor == relation:
            errors.append('supersede requires a non-self successor identity')
        elif known_ids is not None and successor not in known_ids:
            errors.append('supersededBy does not exist in supplied governance ledger')
    elif successor is not None:
        errors.append('supersededBy is not allowed for reject action')
    for field in ('rationale', 'proposedBy'):
        value = record.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f'{field} must be a nonempty string')
    refs = record.get('evidenceRefs')
    if not isinstance(refs, list) or not refs or any(not isinstance(ref, str) or not ref.strip() for ref in refs):
        errors.append('evidenceRefs must contain nonempty references')
    elif len(set(refs)) != len(refs):
        errors.append('evidenceRefs must not contain duplicates')
    stamp = record.get('proposedAt')
    if not isinstance(stamp, str) or not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', stamp):
        errors.append('proposedAt must be a YYYY-MM-DD string')
    else:
        try:
            date.fromisoformat(stamp)
        except ValueError:
            errors.append('proposedAt must be a real calendar date')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', required=True, type=Path, help='one draft YAML candidate')
    parser.add_argument('--ledger', type=Path, help='optional actual ledger for exact ID checks')
    args = parser.parse_args()
    try:
        doc = yaml.safe_load(args.candidate.read_text(encoding='utf-8'))
        known_ids = None
        if args.ledger is not None:
            ledger = yaml.safe_load(args.ledger.read_text(encoding='utf-8'))
            if not isinstance(ledger, dict) or not isinstance(ledger.get('entries'), list):
                raise ValueError('ledger must contain an entries list')
            known_ids = {e['id'] for e in ledger['entries'] if isinstance(e, dict) and isinstance(e.get('id'), str)}
        problems = validate(doc, known_ids=known_ids)
    except (OSError, UnicodeError, yaml.YAMLError, ValueError, TypeError) as exc:
        print(f'FAIL: cannot inspect candidate: {exc}')
        return 1
    for message in problems:
        print('FAIL: ' + message)
    if problems:
        return 1
    print('PASS: structurally valid DRAFT candidate; NOT an approval or authorization')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
