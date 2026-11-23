#!/usr/bin/env python3
"""Mutation tests for the RFC traceability/disposition checker."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from check_rfc_governance import check, REGISTER, ARCHIVE, DECISIONS


class RFCGovernanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / ARCHIVE).mkdir(parents=True)
        (self.root / REGISTER).parent.mkdir(parents=True)
        self.files = {}
        for number in ('008', '019', '037', '098'):
            rfc = f'RFC-{number}'
            status = 'proposal, non-normative' if number == '008' else 'deferred; historical'
            decision = {'019': 'D-BP-08', '037': 'D-BP-11', '098': 'D-BP-12'}.get(number, '')
            content = f'# {rfc}\n- Status: {status}\n- Decision: {decision}\n'
            if number == '008':
                content += '\n## 6. Deferred questions\n' + ''.join(f'- RFC-008-Q{i}: Question\n' for i in range(1, 4))
            path = self.root / ARCHIVE / f'{rfc}-Example.md'
            path.write_text(content)
            self.files[rfc] = path
        rows = ['| RFC | Title | Maturity status | Notes |', '|---|---|---|---|']
        for number in ('008', '019', '037', '098'):
            status = 'STRUCTURAL_DRAFT' if number == '008' else 'DEFERRED'
            rows.append(f'| RFC-{number} | Example | {status} | Audited |')
        (self.root / REGISTER).write_text('\n'.join(rows) + '\n')
        (self.root / DECISIONS).write_text(' '.join(f'RFC-008-Q{i}' for i in range(1, 4)))

    def test_valid_pilot(self):
        self.assertEqual([], check(self.root))

    def test_duplicate_register_entry_fails(self):
        path = self.root / REGISTER
        path.write_text(path.read_text() + '| RFC-019 | Duplicate | DEFERRED | Duplicate |\n')
        self.assertIn('Duplicate maturity-register row: RFC-019', check(self.root))

    def test_missing_register_entry_fails(self):
        path = self.root / REGISTER
        path.write_text(path.read_text().replace('| RFC-037 | Example | DEFERRED | Audited |\n', ''))
        self.assertTrue(any('RFC file missing maturity-register entry: RFC-037' in x for x in check(self.root)))

    def test_missing_file_fails(self):
        self.files['RFC-098'].unlink()
        self.assertTrue(any('Maturity-register entry missing RFC file: RFC-098' in x for x in check(self.root)))

    def test_deferral_regression_fails(self):
        path = self.root / REGISTER
        path.write_text(path.read_text().replace('| RFC-019 | Example | DEFERRED', '| RFC-019 | Example | STRUCTURAL_DRAFT'))
        self.assertTrue(any('approved D-BP-08 deferral must be DEFERRED' in x for x in check(self.root)))

    def test_decision_collision_fails(self):
        path = self.files['RFC-008']
        path.write_text(path.read_text().replace('- RFC-008-Q2:', '- D-22:'))
        errors = check(self.root)
        self.assertTrue(any('collides with global' in x for x in errors), errors)

    def test_missing_decision_index_fails(self):
        (self.root / DECISIONS).write_text('RFC-008-Q1 RFC-008-Q3')
        self.assertTrue(any('Decision log missing local question RFC-008-Q2' in x for x in check(self.root)))

    def test_unknown_status_fails(self):
        path = self.root / REGISTER
        path.write_text(path.read_text().replace('| RFC-008 | Example | STRUCTURAL_DRAFT', '| RFC-008 | Example | ACCEPTED'))
        self.assertTrue(any('Unknown maturity status RFC-008: ACCEPTED' in x for x in check(self.root)))


if __name__ == '__main__':
    unittest.main()
