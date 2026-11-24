#!/usr/bin/env python3
"""Mutation tests for conservative Python non-executable span filtering."""
from __future__ import annotations

import unittest

from semantic_neighbor_python_scan import executable_python_lines


class PythonScanTests(unittest.TestCase):
    def test_module_docstring_not_consumer(self):
        content = '"""This explains semanticNeighborIds only."""\n'
        self.assertNotIn('semanticNeighborIds', '\n'.join(executable_python_lines(content)))

    def test_function_docstring_not_consumer(self):
        content = 'def f():\n    """Explain registryOnlyNeighbors"""\n    return 1\n'
        self.assertNotIn('registryOnlyNeighbors', '\n'.join(executable_python_lines(content)))

    def test_class_docstring_not_consumer(self):
        content = 'class C:\n    """About semanticNeighbors"""\n    pass\n'
        self.assertNotIn('semanticNeighbors', '\n'.join(executable_python_lines(content)))

    def test_inline_comment_not_consumer(self):
        content = 'n = 1  # semanticNeighborCatalogIds documentation\n'
        self.assertNotIn('semanticNeighborCatalogIds', '\n'.join(executable_python_lines(content)))
        self.assertIn('n = 1', '\n'.join(executable_python_lines(content)))

    def test_runtime_string_key_still_consumer(self):
        content = 'refs = record.get("semanticNeighborIds", [])  # navigation only\n'
        self.assertIn('semanticNeighborIds', '\n'.join(executable_python_lines(content)))

    def test_runtime_error_message_still_consumer(self):
        content = 'raise ValueError("registryOnlyNeighbors malformed")\n'
        self.assertIn('registryOnlyNeighbors', '\n'.join(executable_python_lines(content)))

    def test_docstring_and_code_on_same_line(self):
        content = 'def f(): "semanticNeighbors"; return x["semanticNeighborIds"]\n'
        visible = '\n'.join(executable_python_lines(content))
        self.assertNotIn('semanticNeighbors', visible)
        self.assertIn('semanticNeighborIds', visible)

    def test_multiline_docstring_preserves_following_code(self):
        content = ('def f():\n    """\n    semanticNeighbors\n    """\n'
                   '    return row["semanticNeighborCatalogIds"]\n')
        visible = '\n'.join(executable_python_lines(content))
        self.assertNotIn('semanticNeighbors', visible)
        self.assertIn('semanticNeighborCatalogIds', visible)
        self.assertEqual(5, len(executable_python_lines(content)))

    def test_malformed_python_falls_back_conservatively(self):
        content = 'this is not valid Python syntax # semanticNeighborIds\n'
        self.assertEqual(content.splitlines(), executable_python_lines(content))

    def test_non_docstring_literal_is_still_scanned(self):
        content = 'x = "semanticNeighbors"\n'
        self.assertIn('semanticNeighbors', '\n'.join(executable_python_lines(content)))


if __name__ == '__main__':
    unittest.main()

