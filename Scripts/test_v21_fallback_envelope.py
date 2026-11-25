#!/usr/bin/env python3
"""A legacy calls key alone is not sufficient for L-06 negotiation."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest
from unittest import mock

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class FallbackEnvelopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid = json.loads(
            (CONF / "fixtures/serverinfo_v21_only.json").read_text(encoding="utf-8")
        )
        manifest = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in manifest["probes"] if p["id"] == "L-06")

    def exercise(self, document, status=200):
        outcomes = checker.Results()
        with mock.patch.object(checker, "http_call", return_value=(status, document)) as call:
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, outcomes, None, None,
            )
        call.assert_called_once()
        return outcomes

    def check_rejection(self, mutate):
        candidate = copy.deepcopy(self.valid)
        mutate(candidate)
        self.assertTrue(checker.v21_fallback_calls_problems(candidate))
        self.assertEqual(1, self.exercise(candidate).failures)

    def test_valid_fallback_passes(self):
        self.assertEqual([], checker.v21_fallback_calls_problems(self.valid))
        self.assertEqual(0, self.exercise(self.valid).failures)

    def test_unexpected_http_status_rejected(self):
        self.assertEqual(1, self.exercise(self.valid, status=500).failures)

    def test_null_calls_rejected(self):
        self.check_rejection(lambda d: d["result"].update(calls=None))

    def test_string_calls_rejected(self):
        self.check_rejection(lambda d: d["result"].update(calls="GET"))

    def test_empty_calls_rejected(self):
        self.check_rejection(lambda d: d["result"].update(calls=[]))

    def test_missing_service_rejected(self):
        self.check_rejection(lambda d: d["result"]["calls"][0].pop("service"))

    def test_nonarray_versions_rejected(self):
        self.check_rejection(lambda d: d["result"]["calls"][0].update(versions="2.1"))

    def test_empty_methods_rejected(self):
        self.check_rejection(lambda d: d["result"]["calls"][0].update(methods=[]))

    def test_nonstring_method_rejected(self):
        self.check_rejection(lambda d: d["result"]["calls"][0].update(methods=[42]))

    def test_nonobject_call_rejected(self):
        self.check_rejection(lambda d: d["result"].update(calls=["bad"]))

    def test_missing_result_rejected(self):
        self.check_rejection(lambda d: d.pop("result"))

    def test_static_fixture_passes_same_validator(self):
        results = checker.Results()
        with mock.patch.object(checker, "load_json", return_value=copy.deepcopy(self.valid)):
            checker.check_v21_fallback_shape(
                str(ROOT), {"id": "S-08", "title": "fallback shape"}, {},
                results,
            )
        self.assertEqual(0, results.failures)


if __name__ == "__main__":
    unittest.main()
