#!/usr/bin/env python3
"""Check internal consistency of an independently captured pipeline state snapshot.

This guards against fabricated or incomplete *trace shape*. It cannot verify
that the service really persisted the snapshot or emitted its listed events.
"""
from __future__ import annotations

from typing import Any


def snapshot_integrity_errors(label: str, state: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    revisions = state.get('revisions')
    effects = state.get('effects')
    if not isinstance(revisions, dict) or not isinstance(effects, dict):
        return [f'{label}: revisions/effects must be mappings']
    current = state.get('currentVersionId')
    if current is not None:
        if not isinstance(current, str) or not current.strip():
            errors.append(f'{label}: currentVersionId must be a nonempty version ID or null')
        elif current not in revisions:
            errors.append(f'{label}: currentVersionId must resolve to an included revision')
        elif not isinstance(revisions[current], dict) or revisions[current].get('publicationState') != 'published':
            errors.append(f'{label}: currentVersionId must resolve to a published revision')
    for event, version in effects.items():
        if isinstance(version, str) and version not in revisions:
            errors.append(f'{label}: lifecycle event {event!r} refers to absent revision {version!r}')
    return errors
