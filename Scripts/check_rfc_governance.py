#!/usr/bin/env python3
"""Fail-closed structural checks for the RFC archive and audited disposition pilot.

This gate checks traceability, not scientific correctness or normative maturity.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

REGISTER = Path('docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md')
ARCHIVE = Path('Specification/BrAPI-GenX/RFCs')
DECISIONS = Path('Specification/BrAPI-GenX/DECISIONS.md')
STATES = {'STRUCTURAL_DRAFT', 'SEMANTICALLY_REVIEWED', 'CONTRACT_VALIDATED', 'DEFERRED'}
DEFERRED_APPROVALS = {'RFC-019': 'D-BP-08', 'RFC-037': 'D-BP-11', 'RFC-098': 'D-BP-12'}
ROW = re.compile(r'^\| (RFC-\d{3}) \|[^\n]*\| (\w+) \|[^\n]*\|$')
FILE = re.compile(r'^(RFC-\d{3})-.+\.md$')


def check(root: Path) -> list[str]:
    """Return actionable errors; never modify repository files."""
    errors: list[str] = []
    register = (root / REGISTER).read_text(encoding='utf-8')
    decisions = (root / DECISIONS).read_text(encoding='utf-8')
    paths: dict[str, Path] = {}
    for path in sorted((root / ARCHIVE).glob('RFC-*.md')):
        match = FILE.fullmatch(path.name)
        if not match:
            errors.append(f'Unexpected RFC filename: {path.name}')
            continue
        if match[1] in paths:
            errors.append(f'Duplicate RFC filename/number: {match[1]}')
        paths[match[1]] = path
    statuses: dict[str, str] = {}
    for line in register.splitlines():
        match = ROW.fullmatch(line)
        if not match:
            if re.match(r'^\| RFC-\d{3} \|', line):
                errors.append(f'Malformed maturity-register row: {line[:90]}')
            continue
        rfc, status = match.groups()
        if rfc in statuses:
            errors.append(f'Duplicate maturity-register row: {rfc}')
        statuses[rfc] = status
        if status not in STATES:
            errors.append(f'Unknown maturity status {rfc}: {status}')
    if not paths or not statuses:
        errors.append('RFC archive or maturity register is empty')
    for rfc in sorted(set(paths) - set(statuses)):
        errors.append(f'RFC file missing maturity-register entry: {rfc}')
    for rfc in sorted(set(statuses) - set(paths)):
        errors.append(f'Maturity-register entry missing RFC file: {rfc}')
    for rfc, decision in DEFERRED_APPROVALS.items():
        if statuses.get(rfc) != 'DEFERRED':
            errors.append(f'{rfc}: approved {decision} deferral must be DEFERRED in register')
        if rfc not in paths:
            continue
        content = paths[rfc].read_text(encoding='utf-8')
        if not re.search(r'^- Status: deferred\b', content, re.M):
            errors.append(f'{rfc}: RFC must identify itself as deferred')
        if decision not in content:
            errors.append(f'{rfc}: approved deferral decision {decision} missing')
    if 'RFC-008' in paths:
        content = paths['RFC-008'].read_text(encoding='utf-8')
        questions = content.split('## 6. Deferred questions', 1)
        if len(questions) != 2:
            errors.append('RFC-008: missing Deferred questions section')
        else:
            section = questions[1].split('\n## ', 1)[0]
            for i in range(1, 4):
                marker = f'RFC-008-Q{i}'
                if not re.search(rf'^- {marker}:', section, re.M):
                    errors.append(f'RFC-008: missing local question {marker}')
                if marker not in decisions:
                    errors.append(f'Decision log missing local question {marker}')
            if re.search(r'^- D-\d+:', section, re.M):
                errors.append('RFC-008: local question collides with global D- identifier')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        errors = check(args.root)
    except (OSError, UnicodeError) as exc:
        print(f'FAIL: cannot read RFC governance source: {exc}')
        return 1
    if errors:
        for error in errors:
            print(f'FAIL: {error}')
        return 1
    print('PASS: RFC archive/register alignment and audited deferrals (no maturity promotion)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
