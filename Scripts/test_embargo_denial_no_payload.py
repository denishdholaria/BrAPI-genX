#!/usr/bin/env python3
"""Mission 138: embargoed package GET must not leak content via a 403 body."""
from __future__ import annotations

import copy
import io
import json
from pathlib import Path
from unittest import mock
import unittest
from urllib.error import HTTPError

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class EmbargoDenialPayloadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        manifest = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in manifest["probes"] if p["id"] == "L-20")

    def test_registered_embargo_get_checks_denial(self):
        self.assertEqual(2, len(self.probe["calls"]))
        self.assertEqual("live_package_embargoed", self.probe["calls"][0]["body_fixture"])
        self.assertIs(True, self.probe["calls"][1]["assert"]["embargo_denial_no_payload"])

    def exercise(self, denied=None, status=403, mutate_post=None):
        original = {}
        calls = []

        def fake_http(_server, method, path, body=None, token=None):
            calls.append((method, path))
            if len(calls) == 1:
                self.assertEqual(("POST", "/fair-packages"), (method, path))
                original.update(copy.deepcopy(body))
                response = copy.deepcopy(body)
                if mutate_post is not None:
                    response = mutate_post(response)
                return 200, {"result": response}
            if len(calls) == 2:
                self.assertEqual(("GET", "/fair-packages/" + original["packageDbId"]),
                                 (method, path))
                data = denied(copy.deepcopy(original)) if denied else {
                    "error": "package '" + original["packageDbId"] + "' is embargoed"
                }
                return status, data
            self.fail("unexpected third request")

        outcome = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, outcome, None, None)
        return outcome.failures, calls

    def test_plaintext_denial_wrapped_as_error_passes(self):
        self.assertEqual(0, self.exercise()[0])

    def test_empty_denial_body_passes(self):
        self.assertEqual(0, self.exercise(denied=lambda r: {})[0])

    def test_generic_denial_status_mapping_passes(self):
        self.assertEqual(0, self.exercise(
            denied=lambda r: {"status": [{"message": "Access denied"}]})[0])

    def test_successful_get_fails(self):
        self.assertEqual(1, self.exercise(status=200)[0])

    def test_full_original_record_leak_fails(self):
        self.assertEqual(1, self.exercise(denied=lambda r: {"result": r})[0])

    def test_nested_payload_refs_leak_fails(self):
        self.assertEqual(1, self.exercise(
            denied=lambda r: {"error": {"payloadRefs": r["payloadRefs"]}})[0])

    def test_title_leak_in_text_error_fails(self):
        self.assertEqual(1, self.exercise(
            denied=lambda r: {"error": "Forbidden " + r["title"]})[0])

    def test_doi_leak_in_text_error_fails(self):
        self.assertEqual(1, self.exercise(
            denied=lambda r: {"error": r["identifiers"][0]["value"]})[0])

    def test_evidence_digest_leak_in_text_error_fails(self):
        self.assertEqual(1, self.exercise(
            denied=lambda r: {"error": r["payloadRefs"][0]["responseDigest"]})[0])

    def test_evidence_endpoint_leak_in_text_error_fails(self):
        self.assertEqual(1, self.exercise(
            denied=lambda r: {"error": r["payloadRefs"][0]["endpoint"]})[0])

    def test_license_leak_in_text_error_fails(self):
        self.assertEqual(1, self.exercise(
            denied=lambda r: {"error": "License=" + r["license"]})[0])

    def test_creator_leak_in_text_error_fails(self):
        self.assertEqual(1, self.exercise(
            denied=lambda r: {"error": r["creators"][0]})[0])

    def test_publisher_leak_in_text_error_fails(self):
        self.assertEqual(1, self.exercise(
            denied=lambda r: {"error": r["publisher"]})[0])

    def test_embargo_date_leak_in_text_error_fails(self):
        self.assertEqual(1, self.exercise(
            denied=lambda r: {"error": r["embargoUntil"]})[0])

    def test_unstructured_denial_body_fails(self):
        self.assertEqual(1, self.exercise(denied=lambda r: "private")[0])

    def test_unexpected_data_envelope_fails(self):
        self.assertEqual(1, self.exercise(denied=lambda r: {"data": []})[0])

    def test_wrong_captured_package_identifier_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_post=lambda r: {**r, "packageDbId": "other:package:wrong"})[0])

    def test_http_call_preserves_plain_text_403_for_inspection(self):
        url = "http://example.test/genx/v1/fair-packages/id"
        error = HTTPError(url, 403, "Forbidden", {}, io.BytesIO(b"Forbidden: private title"))
        with mock.patch.object(checker.urlrequest, "urlopen", side_effect=error):
            status, payload = checker.http_call(
                "http://example.test/genx/v1", "GET", "/fair-packages/id"
            )
        self.assertEqual(403, status)
        self.assertEqual({"error": "Forbidden: private title"}, payload)

    def test_http_call_keeps_structured_json_403(self):
        url = "http://example.test/genx/v1/fair-packages/id"
        raw = json.dumps({"result": {"title": "private"}}).encode("utf-8")
        error = HTTPError(url, 403, "Forbidden", {}, io.BytesIO(raw))
        with mock.patch.object(checker.urlrequest, "urlopen", side_effect=error):
            status, payload = checker.http_call(
                "http://example.test/genx/v1", "GET", "/fair-packages/id"
            )
        self.assertEqual(403, status)
        self.assertEqual({"result": {"title": "private"}}, payload)


if __name__ == "__main__":
    unittest.main()
