#!/usr/bin/env python3
"""Read-only GenX group evidence and RFC maturity report.

Reviewed group prose, RFC maturity and independently demonstrated service
conformance are different dimensions. This command never equates them.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re

from check_genx_group_descriptions import REL, REVIEWED, audit

ROOT = Path(__file__).resolve().parents[1]
MATURITY = Path('docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md')
RFC_ID = re.compile(r'RFC-\d{3}')


def register_maturity(root: Path) -> dict[str, str]:
    path = root / MATURITY
    if not path.is_file():
        raise ValueError(f'missing maturity register: {path}')
    statuses: dict[str, str] = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        if not line.startswith('|'):
            continue
        columns = [item.strip() for item in line.strip('|').split('|')]
        if len(columns) < 3 or not RFC_ID.fullmatch(columns[0]):
            continue
        identifier, maturity = columns[0], columns[2]
        if identifier in statuses:
            raise ValueError(f'duplicate RFC maturity row: {identifier}')
        if maturity not in {'STRUCTURAL_DRAFT', 'DEFERRED', 'CONTRACT_VALIDATED',
                            'SEMANTICALLY_REVIEWED'}:
            raise ValueError(f'unknown RFC maturity status: {identifier}: {maturity}')
        statuses[identifier] = maturity
    if not statuses:
        raise ValueError('no RFC maturity rows were found')
    return statuses


def summarize(root: Path, reviewed: frozenset[str] = REVIEWED) -> dict:
    root = root.resolve()
    checked = audit(root, reviewed=reviewed)
    if checked['errors']:
        raise ValueError('group description guard failed: ' + '; '.join(checked['errors']))
    maturity = register_maturity(root)
    genx = root / REL
    modules = []
    by_section: dict[str, Counter[str]] = {}
    for path in sorted(genx.glob('*/*/GroupDescription.md')):
        module = path.parent.relative_to(genx).as_posix()
        readme = path.parent / 'README.md'
        if not readme.is_file():
            raise ValueError(f'missing module overview: {module}')
        ids = sorted(set(RFC_ID.findall(readme.read_text(encoding='utf-8'))))
        states = {identifier: maturity.get(identifier, 'UNVERIFIED_RFC_REFERENCE')
                  for identifier in ids}
        evidence_reviewed = module in reviewed
        label = ('source-backed-description' if evidence_reviewed
                 else 'evidence-deferred')
        modules.append({'module': module, 'descriptionEvidence': label,
                        'rfcIdsFromReadme': ids, 'rfcMaturityFromRegister': states})
        section = module.split('/')[0]
        by_section.setdefault(section, Counter())[label] += 1
    if len(modules) != checked['total']:
        raise ValueError('discovered modules changed during coverage audit')
    return {
        'totalModules': len(modules),
        'reviewedDescriptions': checked['reviewed'],
        'deferredDescriptions': checked['deferred'],
        'perSection': {section: dict(sorted(counts.items()))
                       for section, counts in sorted(by_section.items())},
        'modules': modules,
        'interpretation': ('Description evidence review and candidate RFC maturity '
                           'are separate. Neither establishes scientific adoption, '
                           'production readiness or independent service conformance.')
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        report = summarize(args.root)
    except (ValueError, OSError, UnicodeError) as exc:
        print(f'FAIL: {exc}')
        return 1
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"GenX modules: {report['totalModules']}; source-backed descriptions: "
              f"{report['reviewedDescriptions']}; evidence-deferred: "
              f"{report['deferredDescriptions']}")
        for section, counts in report['perSection'].items():
            print(f"{section}: {counts.get('source-backed-description', 0)} reviewed, "
                  f"{counts.get('evidence-deferred', 0)} deferred")
        print(report['interpretation'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
