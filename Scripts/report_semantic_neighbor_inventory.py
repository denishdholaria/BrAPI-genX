#!/usr/bin/env python3
"""Read-only live review queue for the non-normative semantic-neighbor ledger.

Counts reflect evidence-review status, not scientific acceptance or equivalence.
The historical grouped Markdown document is intentionally a pinned snapshot.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
from typing import Any

import yaml

LEDGER = Path('Specification/BrAPI-GenX/Conformance/semantic-neighbor-review.yaml')
UNREVIEWED = 'inherited-unreviewed'
STATUSES = frozenset({'inherited-unreviewed', 'requires-decision',
                      'evidence-backed-proposed', 'rejected', 'superseded'})


def summarize(ledger: dict[str, Any]) -> dict[str, Any]:
    """Return deterministic counts and unreviewed triads without status promotion."""
    if not isinstance(ledger, dict) or not isinstance(ledger.get('entries'), list):
        raise ValueError('semantic-neighbor ledger must contain an entries list')
    entries = ledger['entries']
    if ledger.get('entry_count') != len(entries):
        raise ValueError('semantic-neighbor ledger entry_count mismatch')
    seen: set[str] = set()
    status_counts: Counter[str] = Counter()
    targets: dict[str, dict[str, Any]] = {}
    groups: dict[tuple[str, str], dict[str, Any]] = {}
    for row in entries:
        if not isinstance(row, dict):
            raise ValueError('semantic-neighbor entry must be a mapping')
        identity, source, target, status = (row.get('id'), row.get('sourceModule'),
                                            row.get('targetOperationId'), row.get('reviewStatus'))
        if any(not isinstance(value, str) or not value.strip()
               for value in (identity, source, target)):
            raise ValueError('semantic-neighbor entry requires ID, source module and target operation')
        if identity in seen:
            raise ValueError(f'duplicate semantic-neighbor identity: {identity}')
        seen.add(identity)
        if status not in STATUSES:
            raise ValueError(f'unknown semantic-neighbor review status: {status!r}')
        status_counts[status] += 1
        info = targets.setdefault(target, {'targetOperationId': target, 'links': 0,
                                           'unreviewed': 0, 'sourceGroups': set()})
        info['links'] += 1
        info['unreviewed'] += status == UNREVIEWED
        info['sourceGroups'].add(source)
        group = groups.setdefault((source, target), {
            'sourceModule': source, 'targetOperationId': target,
            'links': 0, 'statusCounts': Counter()})
        group['links'] += 1
        group['statusCounts'][status] += 1
    target_summary = [
        {'targetOperationId': t, 'links': value['links'],
         'unreviewed': value['unreviewed'], 'sourceGroups': len(value['sourceGroups'])}
        for t, value in targets.items()
    ]
    target_summary.sort(key=lambda r: (-r['links'], r['targetOperationId']))
    unreviewed_groups = [
        {'sourceModule': group['sourceModule'], 'targetOperationId': group['targetOperationId'],
         'links': group['links'], 'unreviewed': group['statusCounts'][UNREVIEWED],
         'statusCounts': dict(sorted(group['statusCounts'].items()))}
        for group in groups.values() if group['statusCounts'][UNREVIEWED]
    ]
    unreviewed_groups.sort(key=lambda r: (-r['unreviewed'], r['targetOperationId'], r['sourceModule']))
    return {
        'totalLinks': len(entries),
        'reviewedOrDecisionPending': len(entries) - status_counts[UNREVIEWED],
        'unreviewedLinks': status_counts[UNREVIEWED],
        'totalGroups': len(groups),
        'unreviewedGroups': len(unreviewed_groups),
        'statusCounts': {status: status_counts[status] for status in sorted(STATUSES)},
        'targetConcentration': target_summary,
        'queue': unreviewed_groups,
        'interpretation': 'Review status only; no scientific equivalence or normative acceptance implied.',
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        '# Live semantic-neighbor review queue (non-normative)', '',
        'Derived from the current governance ledger; no acceptance is implied.', '',
        f"Total relationships: **{report['totalLinks']}**; reviewed/decision-pending: "
        f"**{report['reviewedOrDecisionPending']}**; unreviewed: **{report['unreviewedLinks']}**.",
        f"Groups: **{report['totalGroups']}**; groups with unreviewed links: "
        f"**{report['unreviewedGroups']}**.", '',
        '## Target operation concentration', '',
        '| Target operation | Total links | Unreviewed | Source groups |',
        '|---|---:|---:|---:|',
    ]
    for row in report['targetConcentration']:
        lines.append(f"| `{row['targetOperationId']}` | {row['links']} | "
                     f"{row['unreviewed']} | {row['sourceGroups']} |")
    lines.extend(['', '## Unreviewed work queue', '',
                  '| Source module | Target operation | Unreviewed / links |',
                  '|---|---|---:|'])
    for row in report['queue']:
        lines.append(f"| `{row['sourceModule']}` | `{row['targetOperationId']}` | "
                     f"{row['unreviewed']} / {row['links']} |")
    return '\n'.join(lines) + '\n'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--json', action='store_true', help='machine-readable live queue')
    modes.add_argument('--check', action='store_true', help='validate and print concise counts')
    args = parser.parse_args()
    try:
        doc = yaml.safe_load((args.root / LEDGER).read_text(encoding='utf-8'))
        report = summarize(doc)
    except (OSError, UnicodeError, yaml.YAMLError, ValueError) as exc:
        print(f'FAIL: cannot summarize semantic-neighbor review ledger: {exc}')
        return 1
    if args.check:
        print(f"PASS: {report['totalLinks']} retained relationships, "
              f"{report['reviewedOrDecisionPending']} reviewed/decision-pending, "
              f"{report['unreviewedLinks']} unreviewed across "
              f"{report['unreviewedGroups']} unreviewed groups (no acceptance implied)")
    elif args.json:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        print(render_markdown(report), end='')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
