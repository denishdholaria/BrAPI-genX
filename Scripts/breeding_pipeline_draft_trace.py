#!/usr/bin/env python3
"""Check D-BP-14 CAS-07..09 state transitions in externally recorded traces.

These checks interpret observations, not prove that a live service produced them.
Common schema/immutability checks are owned by verify_breeding_pipeline_cas_trace.
"""
from __future__ import annotations

from typing import Any

SCENARIOS = frozenset({'CAS-07', 'CAS-08', 'CAS-09'})


def validate_draft_trace(
    trace: dict[str, Any], before: dict[str, Any], after: dict[str, Any],
    requests: list[dict[str, Any]], by_response: dict[str, dict[str, Any]],
) -> list[str]:
    """Check first publication and non-current draft append behavior."""
    scenario = trace['scenario']
    if scenario not in SCENARIOS:
        return [f'unsupported draft trace scenario: {scenario}']
    errors: list[str] = []
    old = before['revisions']
    new = after['revisions']
    current = before['currentVersionId']
    created_ids = {request['versionId'] for request in requests}
    if len(created_ids) != len(requests) or any(version in old for version in created_ids):
        errors.append(f'{scenario} requires distinct, never-before-used version identities')
    if set(new) - set(old) != created_ids:
        errors.append(f'{scenario} must append exactly the requested new revisions')
    expected_status = 'published' if scenario == 'CAS-07' else 'draft'
    for request in requests:
        client = request['client']
        version = request['versionId']
        response = by_response[client]
        if request.get('requestedPublicationState') != expected_status:
            errors.append(f'{scenario}: submitted publication intent must be {expected_status}')
        if response.get('status') not in (200, 201) or response.get('resultVersionId') != version:
            errors.append(f'{scenario}: successful append must identify its exact version')
        if (new.get(version, {}).get('fingerprint') != request['fingerprint']
                or new.get(version, {}).get('publicationState') != expected_status):
            errors.append(f'{scenario}: new revision must retain requested content and {expected_status} state')
        if scenario in ('CAS-08', 'CAS-09'):
            if request.get('basedOnVersionId') != current:
                errors.append(f'{scenario}: draft must record current published revision as preparation baseline')
            if 'supersedes' in request or 'corrects' in request:
                errors.append(f'{scenario}: draft must not claim published supersedes/corrects relationship')
    if scenario == 'CAS-07':
        if trace.get('pipelineExistsBefore') is not True or current is not None:
            errors.append('CAS-07 requires an existing pipeline with no current published version')
        if 'expectedCurrentVersionId' not in requests[0] or requests[0]['expectedCurrentVersionId'] is not None:
            errors.append('CAS-07 requires explicit null expected-current (not omission)')
        if after['currentVersionId'] != requests[0]['versionId']:
            errors.append('CAS-07 must publish the newly appended revision as current')
    else:
        if not isinstance(current, str) or not current or old.get(current, {}).get('publicationState') != 'published':
            errors.append(f'{scenario} requires a current published baseline')
        if any(request.get('expectedCurrentVersionId') != current for request in requests):
            errors.append(f'{scenario}: drafts must use the observed expected-current baseline')
        if after['currentVersionId'] != current:
            errors.append(f'{scenario}: draft append must not move the current published pointer')
        if scenario == 'CAS-09' and trace.get('barrierObserved') is not True:
            errors.append('CAS-09 requires a recorded concurrent start barrier')
    added_effects = {key: value for key, value in after['effects'].items()
                     if key not in before['effects']}
    if any(version not in created_ids for version in added_effects.values()):
        errors.append(f'{scenario}: unexpected lifecycle event for unrelated revision')
    return errors
