#!/usr/bin/env python3
"""Strict structural binding between terminal ledger rows and approved decision records.

Approval attribution requires maintainer-controlled repository governance. This
module checks exact binding; it does not cryptographically prove who approved it.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
import re
from typing import Any

import yaml

DECISIONS_REL = Path('Specification/BrAPI-GenX/Conformance/semantic-neighbor-terminal-decisions.yaml')
DECISION_ID = re.compile(r'SEM-DEC-[0-9]{4,}')
APPROVAL_URL = re.compile(
    r'https://github\.com/denishdholaria/BrAPI-genX/(?:issues/[0-9]+#issuecomment-[0-9]+|commit/[0-9a-f]{40})'
)
FIELDS = frozenset({'decisionId', 'relationshipId', 'action', 'approvedBy', 'approvedAt',
                    'approvalEvidence', 'rationale', 'evidenceRefs'})


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_register(document: Any, *, known_ids: set[str] | None = None) -> list[str]:
    """Validate register shape and unique, scoped decision identities."""
    if not isinstance(document, dict) or set(document) != {'schemaVersion', 'entries'}:
        return ['terminal decision register must contain only schemaVersion and entries']
    if type(document['schemaVersion']) is not int or document['schemaVersion'] != 1:
        return ['terminal decision register schemaVersion must be integer 1']
    if not isinstance(document['entries'], list):
        return ['terminal decision register entries must be a list']
    errors: list[str] = []
    ids: set[str] = set()
    relationships: set[str] = set()
    for number, entry in enumerate(document['entries']):
        prefix = f'decision[{number}]'
        if not isinstance(entry, dict):
            errors.append(f'{prefix}: must be a mapping')
            continue
        action = entry.get('action')
        expected = FIELDS | ({'supersededBy'} if action == 'supersede' else set())
        if set(entry) != expected:
            errors.append(f'{prefix}: fields must exactly match the decision schema')
        did = entry.get('decisionId')
        if not _text(did) or not DECISION_ID.fullmatch(did):
            errors.append(f'{prefix}: invalid decisionId')
        elif did in ids:
            errors.append(f'{prefix}: duplicate decisionId {did}')
        else:
            ids.add(did)
        rid = entry.get('relationshipId')
        if not _text(rid) or ' -> ' not in rid:
            errors.append(f'{prefix}: relationshipId must be canonical')
        elif rid in relationships:
            errors.append(f'{prefix}: duplicate relationshipId {rid}')
        else:
            relationships.add(rid)
        if known_ids is not None and rid not in known_ids:
            errors.append(f'{prefix}: relationshipId absent from retained ledger')
        if action not in ('reject', 'supersede'):
            errors.append(f'{prefix}: invalid action')
        if action == 'supersede':
            successor = entry.get('supersededBy')
            if not _text(successor) or successor == rid:
                errors.append(f'{prefix}: supersede requires different successor')
            elif known_ids is not None and successor not in known_ids:
                errors.append(f'{prefix}: successor absent from retained ledger')
        if entry.get('approvedBy') != 'project-maintainer':
            errors.append(f'{prefix}: approvedBy must be project-maintainer')
        stamp = entry.get('approvedAt')
        if not _text(stamp) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', stamp):
            errors.append(f'{prefix}: approvedAt must be YYYY-MM-DD')
        else:
            try:
                date.fromisoformat(stamp)
            except ValueError:
                errors.append(f'{prefix}: approvedAt is not a valid date')
        if not _text(entry.get('approvalEvidence')) or not APPROVAL_URL.fullmatch(entry['approvalEvidence']):
            errors.append(f'{prefix}: approvalEvidence must be a repository issue comment or immutable commit URL')
        if not _text(entry.get('rationale')):
            errors.append(f'{prefix}: missing rationale')
        refs = entry.get('evidenceRefs')
        if (not isinstance(refs, list) or not refs or
                any(not _text(ref) for ref in refs) or
                len(refs) != len(set(x for x in refs if isinstance(x, str)))):
            errors.append(f'{prefix}: evidenceRefs must be nonempty, distinct string references')
    return errors


def terminal_decision_errors(entry: dict[str, Any], document: dict[str, Any]) -> list[str]:
    """Require one exact approved-record match for a terminal ledger transition."""
    if entry.get('reviewStatus') not in ('rejected', 'superseded'):
        return []
    rid = entry.get('id', '<missing id>')
    decision_id = entry.get('authorizationReference')
    if not _text(decision_id) or not DECISION_ID.fullmatch(decision_id):
        return [f'{rid}: terminal authorizationReference must name an exact SEM-DEC decision']
    matches = [d for d in document['entries'] if d.get('decisionId') == decision_id]
    if len(matches) != 1:
        return [f'{rid}: terminal authorizationReference has no unique approved decision record']
    decision = matches[0]
    if decision.get('relationshipId') != rid:
        return [f'{rid}: approved decision relationshipId differs from ledger identity']
    expected = 'reject' if entry['reviewStatus'] == 'rejected' else 'supersede'
    if decision.get('action') != expected:
        return [f'{rid}: approved decision action does not match terminal ledger status']
    if expected == 'supersede' and decision.get('supersededBy') != entry.get('supersededBy'):
        return [f'{rid}: approved supersededBy differs from ledger successor']
    return []


def load_register(root: Path, *, known_ids: set[str] | None = None) -> tuple[dict | None, list[str]]:
    path = root / DECISIONS_REL
    try:
        document = yaml.safe_load(path.read_text(encoding='utf-8'))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        return None, [f'cannot load terminal decision register: {exc}']
    errors = validate_register(document, known_ids=known_ids)
    return (document if not errors else None), errors
