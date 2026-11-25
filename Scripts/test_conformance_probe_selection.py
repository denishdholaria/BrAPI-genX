#!/usr/bin/env python3
"""Regression tests for fail-closed explicit conformance probe selection."""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest

from checkGenXConformance import select_probes, selected_probe_exit_code

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "Scripts" / "checkGenXConformance.py"


class SelectedProbeTests(unittest.TestCase):
    def setUp(self):
        self.probes = [
            {"id": "S-01", "tier": "static", "title": "static"},
            {"id": "L-14", "tier": "live", "title": "live"},
        ]

    def test_unfiltered_run_retains_skip_compatible_selection(self):
        self.assertIs(select_probes(self.probes, None, None), self.probes)

    def test_existing_static_probe_needs_no_server(self):
        self.assertEqual([self.probes[0]], select_probes(self.probes, "S-01"))

    def test_existing_live_probe_with_server(self):
        self.assertEqual([self.probes[1]],
                         select_probes(self.probes, "L-14", "http://example.test/genx/v1"))

    def test_unknown_probe_fails_instead_of_zero_checks(self):
        with self.assertRaisesRegex(ValueError, "found 0"):
            select_probes(self.probes, "L-999", "http://example.test/genx/v1")

    def test_empty_explicit_selection_fails(self):
        with self.assertRaisesRegex(ValueError, "found 0"):
            select_probes(self.probes, "", "http://example.test/genx/v1")

    def test_duplicate_identifiers_fail_instead_of_running_two(self):
        duplicated = self.probes + [dict(self.probes[1])]
        with self.assertRaisesRegex(ValueError, "found 2"):
            select_probes(duplicated, "L-14", "http://example.test/genx/v1")

    def test_invalid_tier_fails(self):
        with self.assertRaisesRegex(ValueError, "invalid probe tier"):
            select_probes([{"id": "X-01", "tier": "unknown"}],
                          "X-01", "http://example.test/genx/v1")

    def test_explicit_live_without_server_fails_instead_of_skip(self):
        with self.assertRaisesRegex(ValueError, "requires --server"):
            select_probes(self.probes, "L-14", None)

    def test_cli_unknown_probe_returns_failure(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--only", "L-999"],
            cwd=ROOT, capture_output=True, text=True, timeout=30,
            check=False,
        )
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("expected exactly one registered probe, found 0",
                      result.stderr)

    def test_cli_live_without_server_returns_failure(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--only", "L-14"],
            cwd=ROOT, capture_output=True, text=True, timeout=30,
            check=False,
        )
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("live probe requires --server", result.stderr)



    def test_explicit_expired_job_probe_without_fixture_fails_instead_of_skip_success(self):
        # No network dependency: L-05 skips before issuing its expired-job GET.
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--only", "L-05",
             "--server", "http://127.0.0.1:1/genx/v1"],
            cwd=ROOT, capture_output=True, text=True, timeout=30,
            check=False,
        )
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("SKIP L-05", result.stdout)
        self.assertIn("needs --expired-job", result.stdout)
        self.assertIn("done: 0 failures, 1 skipped", result.stdout)

    def test_unfiltered_run_still_allows_live_probe_skips(self):
        # Isolate outcome policy without rerunning the full static suite here.
        self.assertEqual(0, selected_probe_exit_code(0, 28, False))
        self.assertEqual(0, selected_probe_exit_code(0, 0, True))
        self.assertEqual(1, selected_probe_exit_code(0, 1, True))
        self.assertEqual(1, selected_probe_exit_code(1, 0, False))

if __name__ == "__main__":
    unittest.main()
