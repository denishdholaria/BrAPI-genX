#!/usr/bin/env python3
"""Mutation tests for the executable semantic-neighbor consumer inventory."""
from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from report_semantic_neighbor_consumers import inventory, main


class ConsumerInventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, path, content):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding='utf-8')

    def test_known_consumer_is_classified(self):
        self.write('Scripts/read.py', 'value = record["semanticNeighborIds"]\n')
        result = inventory(self.root, reviewed={'Scripts/read.py': 'validator'})
        self.assertEqual([], result['problems'])
        self.assertEqual('validator', result['consumers'][0]['role'])

    def test_unreviewed_script_fails(self):
        self.write('Scripts/run.py', 'neighbors = item.get("semanticNeighbors")\n')
        result = inventory(self.root, reviewed={})
        self.assertIn('unreviewed executable', result['problems'][0])

    def test_new_client_consumer_fails(self):
        self.write('src/client.ts', 'let refs = data.semanticNeighborCatalogIds;\n')
        self.assertEqual(1, len(inventory(self.root, reviewed={})['problems']))

    def test_generator_consumer_is_seen(self):
        self.write('generator/src/A.java', 'String x = "registryOnlyNeighbors";\n')
        self.assertEqual(1, inventory(self.root, reviewed={})['consumerCount'])

    def test_test_files_are_not_inferred_as_runtime(self):
        self.write('Scripts/test_validation.py', 'x = "semanticNeighborIds"\n')
        self.assertEqual(0, inventory(self.root, reviewed={})['consumerCount'])

    def test_documentation_is_excluded(self):
        self.write('docs/report.md', 'semanticNeighborIds\n')
        self.write('Specification/ENDPOINT-CATALOG.md', 'semanticNeighborIds\n')
        self.assertEqual(0, inventory(self.root, reviewed={})['consumerCount'])

    def test_removed_reviewed_consumer_fails_stale_manifest(self):
        self.write('Scripts/read.py', 'no neighbors here\n')
        report = inventory(self.root, reviewed={'Scripts/read.py': 'validator'})
        self.assertIn('no longer matches', report['problems'][0])

    def test_multiple_fields_and_line_order(self):
        self.write('Scripts/read.py', 'x="semanticNeighbors"\ny="semanticNeighborIds"\n')
        result = inventory(self.root, reviewed={'Scripts/read.py': 'validator'})
        self.assertEqual([1, 2], [h['line'] for h in result['consumers'][0]['hits']])
        self.assertEqual(['semanticNeighbors'], result['consumers'][0]['hits'][0]['fields'])

    def test_read_only_inspection(self):
        self.write('Scripts/read.py', 'x="semanticNeighborIds"\n')
        before = (self.root / 'Scripts/read.py').read_bytes()
        inventory(self.root, reviewed={'Scripts/read.py': 'validator'})
        self.assertEqual(before, (self.root / 'Scripts/read.py').read_bytes())

    def test_unreadable_utf8_fails_closed(self):
        p = self.root / 'Scripts/bad.py'
        p.parent.mkdir(exist_ok=True)
        p.write_bytes(b'\xff\xff')
        self.assertIn('cannot inspect source', inventory(self.root, reviewed={})['problems'][0])


if __name__ == '__main__':
    unittest.main()
