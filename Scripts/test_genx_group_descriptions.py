#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from check_genx_group_descriptions import audit, REL

GOOD = ('# Group Jobs\n\n**Status:** candidate and proposed, not normative.\n\n'
        + 'This module covers a reviewed metadata scope. ' * 10
        + '\n**Sources:** [module](./README.md).\n')


class GroupEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.doc = self.root / REL / 'Core/Jobs/GroupDescription.md'
        self.doc.parent.mkdir(parents=True)
        (self.doc.parent / 'README.md').write_text('A cited module contract')
        self.doc.write_text(GOOD)

    def audit(self):
        return audit(self.root, reviewed=frozenset({'Core/Jobs'}))

    def test_reviewed_doc_is_accepted(self):
        self.assertEqual([], self.audit()['errors'])

    def test_missing_reviewed_doc_fails(self):
        self.doc.unlink()
        self.assertTrue(self.audit()['errors'])

    def test_empty_heading_regresses(self):
        self.doc.write_text('# Group Jobs\n')
        self.assertTrue(any('placeholder' in e for e in self.audit()['errors']))

    def test_missing_status_fails(self):
        self.doc.write_text(GOOD.replace('**Status:**', 'Status:'))
        self.assertTrue(self.audit()['errors'])

    def test_missing_source_fails(self):
        self.doc.write_text(GOOD.replace('**Sources:**', 'Sources:'))
        self.assertTrue(self.audit()['errors'])

    def test_dangling_source_fails(self):
        self.doc.write_text(GOOD.replace('./README.md', './missing.md'))
        self.assertTrue(any('dangling' in e for e in self.audit()['errors']))

    def test_remote_link_fails(self):
        self.doc.write_text(GOOD.replace('./README.md', 'https://example.com'))
        self.assertTrue(any('local' in e for e in self.audit()['errors']))

    def test_missing_maturity_qualification_fails(self):
        self.doc.write_text(GOOD.replace('candidate and proposed', 'defined and recorded'))
        self.assertTrue(any('maturity' in e for e in self.audit()['errors']))

    def test_title_only_unreviewed_is_not_failed(self):
        extra = self.root / REL / 'Core/Unreviewed/GroupDescription.md'
        extra.parent.mkdir(parents=True)
        extra.write_text('# Group Unreviewed\n')
        report = self.audit()
        self.assertEqual([], report['errors'])
        self.assertEqual(1, report['deferred'])

    def test_unavailable_root_fails_closed(self):
        self.assertTrue(audit(self.root / 'no-such-repo', frozenset({'Core/Jobs'}))['errors'])


if __name__ == '__main__':
    unittest.main()
