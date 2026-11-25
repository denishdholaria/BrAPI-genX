#!/usr/bin/env python3
"""Regression tests for fail-closed explicit conformance probe selection."""
from __future__ import annotations

from pathlib import Path
import subprocess
import copy
import tempfile
import yaml
import sys
import unittest

from checkGenXConformance import (select_probes, selected_probe_exit_code,
                                  validate_probe_manifest)

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


class RegistryIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = yaml.safe_load((ROOT / "Specification/BrAPI-GenX/Conformance/probes.yaml").read_text(encoding="utf-8"))
        cls.probes = cls.doc["probes"]

    def mutate(self, fn):
        probes = copy.deepcopy(self.probes)
        fn(probes)
        with self.assertRaises(ValueError) as caught:
            validate_probe_manifest(probes)
        return str(caught.exception)

    def test_checked_in_registry_has_required_static_and_live_baseline(self):
        self.assertIsNone(validate_probe_manifest(self.probes))
        self.assertEqual(49, len(self.probes))

    def test_missing_static_probe_fails(self):
        error = self.mutate(lambda x: x.__setitem__(slice(None), [
            p for p in x if p["id"] != "S-01"
        ]))
        self.assertIn("missing baseline conformance probes: S-01", error)

    def test_missing_live_probe_fails(self):
        error = self.mutate(lambda x: x.__setitem__(slice(None), [
            p for p in x if p["id"] != "L-28"
        ]))
        self.assertIn("L-28", error)

    def test_complete_registry_removal_fails(self):
        error = self.mutate(lambda x: x.clear())
        self.assertIn("missing baseline conformance probes", error)

    def test_duplicate_registration_fails(self):
        error = self.mutate(lambda x: x.append(copy.deepcopy(x[0])))
        self.assertIn("duplicate registered probe identifier", error)

    def test_unknown_static_check_fails(self):
        error = self.mutate(lambda x: x[0].__setitem__("check", "nonexistent"))
        self.assertIn("unknown static check", error)

    def test_live_probe_without_steps_fails(self):
        error = self.mutate(lambda x: next(p for p in x if p["id"] == "L-05").__setitem__("calls", []))
        self.assertIn("missing executable live calls", error)

    def test_wrong_probe_tier_fails(self):
        error = self.mutate(lambda x: x[0].__setitem__("tier", "live"))
        self.assertIn("identifier and tier disagree", error)

    def test_malformed_live_method_fails(self):
        def change(probes):
            live = next(p for p in probes if p["id"] == "L-05")
            live["calls"][0]["method"] = "TRACE"
        error = self.mutate(change)
        self.assertIn("invalid live call", error)

    def test_nonmapping_probe_fails(self):
        error = self.mutate(lambda x: x.append("not a probe"))
        self.assertIn("expected mapping", error)

    def test_future_additional_probe_is_allowed(self):
        probes = copy.deepcopy(self.probes)
        probes.append({
            "id": "S-99",
            "tier": "static",
            "check": self.probes[0]["check"],
            "title": "future, pending governance",
        })
        self.assertIsNone(validate_probe_manifest(probes))

    def test_command_line_empty_manifest_cannot_report_success(self):
        with tempfile.TemporaryDirectory() as root:
            directory = Path(root) / "Specification" / "BrAPI-GenX" / "Conformance"
            directory.mkdir(parents=True)
            (directory / "probes.yaml").write_text(
                yaml.safe_dump({"version": 1, "probes": []}), encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--root", root],
                cwd=ROOT, capture_output=True, text=True, timeout=30,
                check=False,
            )
        self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("missing baseline conformance probes", result.stderr)


if __name__ == "__main__":
    unittest.main()
