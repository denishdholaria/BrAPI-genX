"""Tests for PostgreSQL idempotency integration in the Python reference server."""

import importlib.util
import json
import os
import sys
import threading
import time
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SERVER_PATH = ROOT / "Scripts" / "genx_test_server.py"
sys.path.insert(0, str(ROOT / "src"))

spec = importlib.util.spec_from_file_location("genx_test_server_under_test", SERVER_PATH)
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)

from brapi_genx.idempotency import PostgresIdempotencyStore, IdempotencyIdentity

DSN = os.environ.get("GENX_IDEMPOTENCY_DSN", "postgresql://postgres:postgres@localhost/brapi_genx_idempotency")


@pytest.fixture
def pg_store():
    s = PostgresIdempotencyStore(DSN, response_ttl=__import__("datetime").timedelta(days=7),
                                 tombstone_ttl=__import__("datetime").timedelta(days=30), lease_seconds=2)
    s.migrate()
    s.purge()
    yield s
    try:
        s.purge()
    except Exception:
        pass
    s.close()


def test_env_based_postgres_initialization(monkeypatch):
    monkeypatch.setenv("GENX_IDEMPOTENCY_DSN", DSN)
    s = server.create_idempotency_store()
    assert isinstance(s, PostgresIdempotencyStore)
    s.close()


def test_dependency_injection():
    pg = PostgresIdempotencyStore(DSN)
    pg.migrate()
    pg.purge()
    st = server.Store(idempotency_store=pg)
    assert st.idempotency_store is pg
    assert st.idempotency_mode == "authoritative"
    st.close()


def test_dependency_injection_via_dsn():
    st = server.Store(idempotency_dsn=DSN)
    assert isinstance(st.idempotency_store, PostgresIdempotencyStore)
    assert st.idempotency_mode == "authoritative"
    st.close()


def test_startup_failure_no_silent_fallback(monkeypatch):
    monkeypatch.setenv("GENX_IDEMPOTENCY_DSN", "postgresql://postgres:postgres@127.0.0.1:1/does_not_exist")
    with pytest.raises(Exception):
        server.create_idempotency_store()
    # create_server must propagate, not fall back to in-memory
    with pytest.raises(Exception):
        server.create_server(port=0, init_from_env=True)


def test_no_silent_inmemory_fallback_when_configured(monkeypatch):
    monkeypatch.setenv("GENX_IDEMPOTENCY_DSN", "postgresql://postgres:postgres@127.0.0.1:1/does_not_exist")
    st = server.Store(init_from_env=False)
    # without env opt-in, stays in-memory
    assert st.idempotency_mode == "non_authoritative_dev"
    assert st.idempotency_store is None


def test_shutdown_cleanup(pg_store):
    httpd = server.create_server(port=0, idempotency_store=pg_store, delay=0, init_from_env=False)
    assert httpd.idempotency_store is pg_store
    httpd.server_close()
    assert pg_store._closed is True


def test_request_execution_and_replay(pg_store):
    httpd = server.create_server(port=0, idempotency_store=pg_store, delay=0, init_from_env=False)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.2)
    try:
        base = f"http://127.0.0.1:{httpd.server_port}"
        body = {"jobType": "analysis", "parameters": {"x": 1}, "idempotencyKey": "test-key-1"}
        data = json.dumps(body).encode()
        req = urllib.request.Request(base + "/genx/v1/jobs", data=data,
                                    headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req) as resp:
            assert resp.status == 202
            first = json.load(resp)
        job_id = first["result"]["jobDbId"]

        # replay same body
        req2 = urllib.request.Request(base + "/genx/v1/jobs", data=data,
                                     headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req2) as resp:
            assert resp.status == 200
            second = json.load(resp)
        assert second["result"]["jobDbId"] == job_id
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=5)


def test_conflict_through_integrated_store(pg_store):
    httpd = server.create_server(port=0, idempotency_store=pg_store, delay=0, init_from_env=False)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.2)
    try:
        base = f"http://127.0.0.1:{httpd.server_port}"
        body1 = {"jobType": "analysis", "parameters": {"x": 1}, "idempotencyKey": "conflict-key"}
        body2 = {"jobType": "analysis", "parameters": {"x": 2}, "idempotencyKey": "conflict-key"}
        for b in (body1,):
            req = urllib.request.Request(base + "/genx/v1/jobs", data=json.dumps(b).encode(),
                                        headers={"Content-Type": "application/json"}, method="POST")
            urllib.request.urlopen(req).read()
        req2 = urllib.request.Request(base + "/genx/v1/jobs", data=json.dumps(body2).encode(),
                                     headers={"Content-Type": "application/json"}, method="POST")
        try:
            urllib.request.urlopen(req2)
            assert False, "expected 409"
        except urllib.error.HTTPError as e:
            assert e.code == 409
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=5)