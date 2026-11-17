"""Tests for migrated digest API using verified JCS canonicalization."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from brapi_genx.canonicalization import jcs_canonicalize, JCSError
from brapi_genx.digest import (
    canonical_json_digest,
    request_fingerprint_digest,
    JCS_RFC8785_V1,
)

CORPUS_PATH = Path(__file__).parent.parent / "Specification" / "BrAPI-GenX" / "Conformance" / "digest-vectors.json"


def test_property_order_independence_request_fingerprint():
    payload_a = json.dumps({"b": 2, "a": 1}).encode("utf-8")
    payload_b = json.dumps({"a": 1, "b": 2}).encode("utf-8")
    ca = jcs_canonicalize(payload_a)
    cb = jcs_canonicalize(payload_b)
    assert ca == cb
    d1 = request_fingerprint_digest("op", "POST", ca)
    d2 = request_fingerprint_digest("op", "POST", cb)
    assert d1.value == d2.value
    assert d1.canonicalization_profile == JCS_RFC8785_V1


def test_canonical_json_digest_matches_shared_vectors():
    corpus = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    for vector in corpus["structuredJsonVectors"]:
        result = canonical_json_digest(vector["inputJson"].encode("utf-8"))
        assert result.hex() == vector["expectedSha256"], vector["id"]
        assert result.canonicalization_profile == JCS_RFC8785_V1


def test_numeric_edge_cases_consistent():
    for payload in (b'{"n":1}', b'{"n":1.0}'):
        r = canonical_json_digest(payload)
        assert r.value
    with pytest.raises(JCSError):
        canonical_json_digest(b'{"n":9007199254740992}')


def test_unicode_and_escaping_consistent():
    payload = '{"emoji":"😀","text":"a/b"}'.encode("utf-8")
    result = canonical_json_digest(payload)
    canon = jcs_canonicalize(payload)
    assert result.hex() == hashlib.sha256(canon).hexdigest()


def test_duplicate_properties_rejected_raw_json():
    with pytest.raises(JCSError):
        canonical_json_digest(b'{"a":1,"a":2}')
    with pytest.raises(JCSError):
        request_fingerprint_digest("op", "POST", b'{"a":1,"a":2}')


def test_request_fingerprint_profile_and_determinism():
    payload = b'{"x":5}'
    r1 = request_fingerprint_digest("op", "get", payload, query_params={"q": "1"}, headers={"Content-Type": "application/json"}, contract_version="2")
    r2 = request_fingerprint_digest("op", "GET", payload, query_params={"q": "1"}, headers={"Content-Type": "application/json"}, contract_version="2")
    assert r1.value == r2.value
    assert r1.canonicalization_profile == JCS_RFC8785_V1
    r3 = request_fingerprint_digest("op", "GET", payload, contract_version="3")
    assert r3.value != r1.value
