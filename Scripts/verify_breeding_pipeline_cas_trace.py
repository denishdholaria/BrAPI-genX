#!/usr/bin/env python3
"""Verify selected recorded BreedingPipeline CAS-01..09 outcomes against D-BP-14.

A trace is supplied by an external harness, not gathered by this module.
Passing a synthetic or self-reported trace does NOT prove service conformance.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from breeding_pipeline_draft_trace import validate_draft_trace

SCENARIOS = frozenset({'CAS-01', 'CAS-02', 'CAS-03', 'CAS-04', 'CAS-06', 'CAS-07', 'CAS-08', 'CAS-09'})


def validate(trace: Any) -> list[str]:
    if not isinstance(trace, dict):
        return ['trace must be a JSON object']
    errors = []
    scenario = trace.get('scenario')
    if scenario not in SCENARIOS:
        return ['unsupported scenario; this verifier covers CAS-01..04 and CAS-06..09 only']
    before, after = trace.get('before'), trace.get('after')
    if not isinstance(before, dict) or not isinstance(after, dict):
        return ['before and after must be state snapshots']
    for label, state in [('before', before), ('after', after)]:
        if 'currentVersionId' not in state or (state['currentVersionId'] is not None and not isinstance(state['currentVersionId'], str)):
            errors.append(f'{label} must identify currentVersionId (string or null)')
        if not isinstance(state.get('revisions'), dict):
            errors.append(f'{label}.revisions must be a mapping')
        if not isinstance(state.get('effects'), dict):
            errors.append(f'{label}.effects must map event IDs to affected revision IDs')
    if errors:
        return errors
    old, new = before['revisions'], after['revisions']
    def invalid_revision(key, record):
        return (not isinstance(key, str) or not key.strip() or not isinstance(record, dict)
                or not isinstance(record.get('fingerprint'), str) or not record['fingerprint'].strip()
                or record.get('publicationState') not in {'draft', 'published', 'withdrawn'})
    if any(invalid_revision(k, v) for k, v in old.items()):
        errors.append('before.revisions must map version IDs to fingerprint and publicationState records')
    if any(invalid_revision(k, v) for k, v in new.items()):
        errors.append('after.revisions must map version IDs to fingerprint and publicationState records')
    if errors:
        return errors
    if old.keys() - new.keys() or any(new.get(version) != digest for version, digest in old.items()):
        errors.append('historical immutable versions must remain unchanged and retrievable')
    if any(not isinstance(k, str) or not k.strip() or not isinstance(v, str) or not v.strip()
           for state in (before, after) for k, v in state['effects'].items()):
        errors.append('effect IDs and their revision IDs must be nonempty strings')
    if any(after['effects'].get(k) != v for k, v in before['effects'].items()):
        errors.append('previously observed lifecycle events must not disappear or change')
    requests, responses = trace.get('requests'), trace.get('responses')
    if not isinstance(requests, list) or not isinstance(responses, list):
        return errors + ['requests and responses must be lists']
    if len(requests) != len(responses) or len(requests) != (2 if scenario in ('CAS-02', 'CAS-06', 'CAS-09') else 1):
        return errors + ['unexpected request/response count for this scenario']
    if any(not isinstance(row, dict) for row in requests + responses):
        return errors + ['requests and responses must contain objects']
    clients = [row.get('client') for row in requests]
    if any(not isinstance(c, str) or not c.strip() for c in clients) or len(set(clients)) != len(clients):
        return errors + ['request clients must have distinct nonempty identities']
    by_response = {row.get('client'): row for row in responses}
    if len(by_response) != len(responses) or set(by_response) != set(clients):
        return errors + ['response client identities must exactly match requests']
    if any(not isinstance(row.get('versionId'), str) or not row['versionId'].strip() or
           not isinstance(row.get('fingerprint'), str) or not row['fingerprint'].strip() for row in requests):
        return errors + ['request versionId and fingerprint must be nonempty strings']
    def unchanged():
        if before != after:
            errors.append('rejected/replayed mutation must not change pointer, history, or effects')
    if scenario == 'CAS-01':
        request, response = requests[0], by_response[clients[0]]
        if request.get('expectedCurrentVersionId') == before.get('currentVersionId'):
            errors.append('CAS-01 must supply a stale expected-current value')
        if request['versionId'] in old:
            errors.append('CAS-01 must attempt a new version ID')
        if response.get('status') != 409 or response.get('errorCode') != 'current-version-precondition-failed':
            errors.append('CAS-01 must reject stale pointer with 409/current-version-precondition-failed')
        unchanged()
    elif scenario in ('CAS-02', 'CAS-06'):
        if trace.get('barrierObserved') is not True:
            errors.append(f'{scenario} requires a recorded simultaneous-start barrier')
        if scenario == 'CAS-02':
            if before.get('currentVersionId') is None:
                errors.append('CAS-02 requires a prior current published revision')
            if any(row.get('expectedCurrentVersionId') != before['currentVersionId'] for row in requests):
                errors.append('both CAS-02 writers must target the same observed baseline')
            conflict_code = 'current-version-precondition-failed'
        else:
            if before.get('currentVersionId') is not None or old:
                errors.append('CAS-06 must start before the logical pipeline exists')
            if any('expectedCurrentVersionId' in row for row in requests):
                errors.append('CAS-06 first creation must omit expected-current (null is not omission)')
            conflict_code = 'pipeline-identity-conflict'
        ids = [row['versionId'] for row in requests]
        if len(set(ids)) != 2 or any(version in old for version in ids):
            errors.append(f'{scenario} requires two distinct new revision identities')
        winners = [row for row in requests if by_response[row['client']].get('status') in (200, 201)]
        losers = [row for row in requests if by_response[row['client']].get('status') == 409 and
                  by_response[row['client']].get('errorCode') == conflict_code]
        if len(winners) != 1 or len(losers) != 1:
            errors.append(f'{scenario} requires one committed winner and one {conflict_code} loser')
        else:
            winner, loser = winners[0], losers[0]
            if (after['currentVersionId'] != winner['versionId']
                    or new.get(winner['versionId'], {}).get('fingerprint') != winner['fingerprint']
                    or new.get(winner['versionId'], {}).get('publicationState') != 'published'):
                errors.append(f'{scenario} final pointer/history must resolve to winner content')
            if loser['versionId'] in new:
                errors.append(f'{scenario} losing revision must not enter history')
            if set(new) - set(old) != {winner['versionId']}:
                errors.append(f'{scenario} must append exactly the winning revision')
            if by_response[winner['client']].get('resultVersionId') != winner['versionId']:
                errors.append(f'{scenario} success must identify the winning revision')
            newly_observed_effects = {event: version for event, version in after['effects'].items()
                                      if event not in before['effects']}
            if any(version != winner['versionId'] for version in newly_observed_effects.values()):
                errors.append(f'{scenario} losing request must not emit a lifecycle side effect')
    elif scenario in ('CAS-07', 'CAS-08', 'CAS-09'):
        errors.extend(validate_draft_trace(trace, before, after, requests, by_response))
    elif scenario == 'CAS-03':
        request, response = requests[0], by_response[clients[0]]
        if request['versionId'] not in old or old[request['versionId']]['fingerprint'] != request['fingerprint']:
            errors.append('CAS-03 replay must be identical to existing immutable content')
        if request.get('expectedCurrentVersionId') == before.get('currentVersionId'):
            errors.append('CAS-03 must test replay against a now-stale expected-current value')
        if response.get('status') not in (200, 201) or response.get('resultVersionId') != request['versionId']:
            errors.append('CAS-03 identical replay must succeed with original revision identity')
        unchanged()
    else:  # CAS-04
        request, response = requests[0], by_response[clients[0]]
        if request['versionId'] not in old or old[request['versionId']]['fingerprint'] == request['fingerprint']:
            errors.append('CAS-04 requires an existing version ID with different canonical content')
        if response.get('status') != 409 or response.get('errorCode') != 'version-content-conflict':
            errors.append('CAS-04 must reject content mutation with 409/version-content-conflict')
        unchanged()
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--trace', type=Path, required=True, help='recorded observation as JSON')
    args = parser.parse_args()
    try:
        data = json.loads(args.trace.read_text(encoding='utf-8'))
        problems = validate(data)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print('FAIL: cannot parse trace: ' + str(exc))
        return 1
    for error in problems:
        print('FAIL: ' + error)
    if problems:
        return 1
    print('PASS: trace satisfies the selected CAS invariants; provenance and real service execution NOT verified')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
