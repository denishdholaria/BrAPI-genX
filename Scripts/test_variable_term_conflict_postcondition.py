#!/usr/bin/env python3
"""Mission 122: rejected variable-term rewrite must preserve original version."""
from __future__ import annotations

import copy
from pathlib import Path
from unittest import mock
import unittest
from urllib.parse import quote

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class VariableTermConflictReadbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        doc = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in doc["probes"] if p["id"] == "L-09")

    def test_registered_versioned_post_conflict_readback(self):
        self.assertEqual(3, len(self.probe["calls"]))
        final = self.probe["calls"][2]
        self.assertEqual("GET", final["method"])
        self.assertEqual(
            "/variable-terms/{variableDbId}?version={termVersion}", final["path"])
        self.assertIs(True, final["assert"]["unchanged_term_record"])

    def exercise(self, mutate=None, read_status=200, conflict_status=409):
        seen = []
        original = {}

        def fake_http(_server, method, path, body=None, token=None):
            seen.append((method, path))
            if len(seen) == 1:
                self.assertEqual(("POST", "/variable-terms"), (method, path))
                original.update(copy.deepcopy(body))
                return 200, {"result": copy.deepcopy(body)}
            if len(seen) == 2:
                self.assertEqual(("POST", "/variable-terms"), (method, path))
                self.assertEqual(original["variableDbId"], body["variableDbId"])
                self.assertEqual(original["version"], body["version"])
                self.assertNotEqual(original["scaleDbId"], body["scaleDbId"])
                return conflict_status, {"result": {}}
            if len(seen) == 3:
                expected = ("/variable-terms/" +
                            quote(original["variableDbId"], safe=":") +
                            "?version=" + quote(original["version"], safe=""))
                self.assertEqual(("GET", expected), (method, path))
                stored = copy.deepcopy(original)
                if mutate is not None:
                    stored = mutate(stored)
                return read_status, {"result": stored}
            self.fail("unexpected additional HTTP call")

        outcome = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, outcome, None, None)
        return outcome.failures, seen

    def test_unchanged_record_passes(self):
        failures, seen = self.exercise()
        self.assertEqual(0, failures)
        self.assertEqual(3, len(seen))

    def test_extra_server_managed_attribute_can_coexist(self):
        self.assertEqual(0, self.exercise(
            lambda stored: {**stored, "retrievedAt": "2026-11-25T00:00:00Z"})[0])

    def test_conflict_response_can_hide_mutated_scale_only_until_readback(self):
        def mutate(stored):
            stored["scaleDbId"] = "institute-b:scale:t_per_hectare"
            return stored
        self.assertEqual(1, self.exercise(mutate)[0])

    def test_mutated_nested_provenance_actor_fails(self):
        def mutate(stored):
            stored["provenance"]["actor"] = "actor:unexpected-curator"
            return stored
        self.assertEqual(1, self.exercise(mutate)[0])

    def test_mutated_nested_provenance_digest_fails(self):
        def mutate(stored):
            stored["provenance"]["inputsDigest"] = "f" * 64
            return stored
        self.assertEqual(1, self.exercise(mutate)[0])

    def test_wrong_term_version_fails(self):
        def mutate(stored):
            stored["version"] = "2"
            return stored
        self.assertEqual(1, self.exercise(mutate)[0])

    def test_wrong_term_identifier_fails(self):
        def mutate(stored):
            stored["variableDbId"] = "other:variable:unexpected"
            return stored
        self.assertEqual(1, self.exercise(mutate)[0])

    def test_missing_field_fails(self):
        def mutate(stored):
            stored.pop("scaleDbId")
            return stored
        self.assertEqual(1, self.exercise(mutate)[0])

    def test_missing_provenance_fails(self):
        def mutate(stored):
            stored.pop("provenance")
            return stored
        self.assertEqual(1, self.exercise(mutate)[0])

    def test_changed_method_version_fails(self):
        def mutate(stored):
            stored["methodVersion"] = "999"
            return stored
        self.assertEqual(1, self.exercise(mutate)[0])

    def test_missing_result_fails(self):
        self.assertEqual(1, self.exercise(lambda stored: None)[0])

    def test_malformed_result_fails(self):
        self.assertEqual(1, self.exercise(lambda stored: [stored])[0])

    def test_unavailable_get_fails(self):
        self.assertEqual(1, self.exercise(read_status=404)[0])

    def test_unexpected_conflict_status_fails_before_get(self):
        failures, seen = self.exercise(conflict_status=200)
        self.assertEqual(1, failures)
        self.assertEqual(2, len(seen))


if __name__ == "__main__":
    unittest.main()
