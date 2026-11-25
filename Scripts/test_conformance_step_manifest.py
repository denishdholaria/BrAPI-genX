#!/usr/bin/env python3
"""Guard against unrecognized live call steps and silently empty POST bodies."""
from __future__ import annotations

import copy
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml
from checkGenXConformance import validate_probe_manifest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "Specification" / "BrAPI-GenX" / "Conformance" / "probes.yaml"
SCRIPT = ROOT / "Scripts" / "checkGenXConformance.py"


class StepDirectiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))

    def rejects(self, probe_id, index, mutate):
        probes = copy.deepcopy(self.baseline["probes"])
        step = next(p for p in probes if p["id"] == probe_id)["calls"][index]
        mutate(step)
        with self.assertRaises(ValueError) as caught:
            validate_probe_manifest(probes)
        return str(caught.exception)

    def test_existing_forty_nine_probes_are_executable(self):
        self.assertIsNone(validate_probe_manifest(self.baseline["probes"]))

    def test_unknown_body_fixture_rejected(self):
        self.assertIn("unknown body_fixture",
            self.rejects("L-13", 1,
                         lambda s: s.update(body_fixture="live_modle_conflict")))

    def test_null_body_fixture_rejected(self):
        self.assertIn("unknown body_fixture",
            self.rejects("L-13", 1,
                         lambda s: s.update(body_fixture=None)))

    def test_missing_post_body_fixture_rejected(self):
        self.assertIn("POST requires",
            self.rejects("L-13", 1,
                         lambda s: s.pop("body_fixture")))

    def test_misspelled_body_fixture_key_rejected(self):
        self.assertIn("unknown live call directive",
            self.rejects("L-13", 1,
                         lambda s: s.update(body_fixtuer="live_model_conflict")))

    def test_unknown_capture_flag_rejected(self):
        self.assertIn("unknown live call directive",
            self.rejects("L-13", 0,
                         lambda s: s.update(captuer_model=True)))

    def test_false_capture_flag_rejected(self):
        self.assertIn("capture_model must be true",
            self.rejects("L-13", 0,
                         lambda s: s.update(capture_model=False)))

    def test_string_capture_flag_rejected(self):
        self.assertIn("capture_model must be true",
            self.rejects("L-13", 0,
                         lambda s: s.update(capture_model="true")))

    def test_body_fixture_on_get_rejected(self):
        self.assertIn("body_fixture requires POST",
            self.rejects("L-06", 0,
                         lambda s: s.update(body_fixture="live_submit")))

    def test_capture_flag_on_get_rejected(self):
        self.assertIn("capture/concurrent directives need POST",
            self.rejects("L-06", 0,
                         lambda s: s.update(capture_job=True)))

    def test_replay_capture_with_body_fixture_rejected(self):
        self.assertIn("replay_capture needs a POST",
            self.rejects("L-01", 1,
                         lambda s: s.update(body_fixture="live_submit")))

    def test_wait_terminal_needs_capture_job(self):
        self.assertIn("wait_terminal requires capture_job",
            self.rejects("L-07", 0,
                         lambda s: s.pop("capture_job")))

    def test_unknown_extra_call_directive_rejected(self):
        self.assertIn("unknown live call directive",
            self.rejects("L-06", 0,
                         lambda s: s.update(verified_status=True)))

    def test_concurrent_post_directive_on_get_rejected(self):
        def mutate(step):
            step["concurrent_posts"] = 8
            step["assert"]["single_effect"] = True
        self.assertIn("capture/concurrent directives need POST",
                      self.rejects("L-06", 0, mutate))

    def test_cli_rejects_misspelled_body_fixture_before_network(self):
        candidate = copy.deepcopy(self.baseline)
        next(p for p in candidate["probes"] if p["id"] == "L-13")[
            "calls"][1]["body_fixture"] = "live_modle_conflict"
        with tempfile.TemporaryDirectory() as folder:
            directory = Path(folder) / "Specification" / "BrAPI-GenX" / "Conformance"
            directory.mkdir(parents=True)
            (directory / "probes.yaml").write_text(
                yaml.safe_dump(candidate, sort_keys=False), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--root", folder,
                 "--only", "L-13", "--server", "http://127.0.0.1:1/genx/v1"],
                cwd=ROOT, text=True, capture_output=True, timeout=30,
                check=False,
            )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("unknown body_fixture", result.stderr)


if __name__ == "__main__":
    unittest.main()
