"""Regression tests for migrated reference-server canonicalization."""

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER_PATH = ROOT / "Scripts" / "genx_test_server.py"

spec = importlib.util.spec_from_file_location("genx_test_server_under_test", SERVER_PATH)
server = importlib.util.module_from_spec(spec)
sys.path.insert(0, str(ROOT / "src"))
spec.loader.exec_module(server)

canonical = server.canonical
from brapi_genx.canonicalization import jcs_canonicalize_text


def test_order_independence():
    a = canonical({"b": 2, "a": 1})
    b = canonical({"a": 1, "b": 2})
    assert a == b


def test_matches_jcs():
    obj = {"z": [3, 1], "a": {"m": 2, "n": 1}}
    assert canonical(obj) == jcs_canonicalize_text(json.dumps(obj))


def test_non_ascii_literal():
    obj = {"t": "café"}
    out = canonical(obj)
    assert "café" in out
