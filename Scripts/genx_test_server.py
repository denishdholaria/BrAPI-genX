#!/usr/bin/env python3
"""
Minimal GenX reference test server (RFC-001). Standard library only.

Implements just enough of the GenX skeleton to execute the live conformance
tier: Jobs lifecycle with idempotency (L-01..L-05, L-07, L-14, L-15),
ServerInfoV3 negotiation (L-06), provenance echo for the `analysis` job type,
versioned ontology terms (L-08, L-09), append-only lot ledgers (L-10, L-11),
model registration with digest-bound inference (L-12..L-15), matrix
references (L-16, L-17), and FAIR packages with embargo (L-18..L-20), and
telemetry batch ingest with aggregates (L-21..L-23).
In-memory state, no persistence, no authentication
(Bearer tokens are accepted and ignored).

Usage:
    python Scripts/genx_test_server.py [--port 8080] [--profile genx|v21]

Profiles:
    genx  Full skeleton: POST/GET/DELETE /jobs, GET /serverinfo (ServerInfoV3)
    v21   V2.1-only: GET /serverinfo returns the calls array; all else 404

Job types (genx profile): germplasm_search, analysis, inference. Anything else is
rejected with 400. A known-expired job JOB_EXPIRED is pre-seeded for L-05.
Inference requires a registered, non-revoked model and returns an echo stub
whose inputsDigest is genuinely computed; revoked or unknown models are
rejected at submit.

Idempotency (prototype behavior): a non-empty Idempotency-Key header takes
precedence over the body idempotencyKey; otherwise the body field is used. The
same key + equal Python-canonicalized parsed JSON body replays the existing job
(200); a different canonical body is rejected with 409. This per-process check,
job creation, and key-index write are atomic under the in-memory lock. Exact
request-equivalence rules, key precedence/body interaction, retention, and
cross-process durability remain unresolved proposal questions (D-24/D-25);
this does not guarantee distributed or durable idempotency.
"""

import argparse
import copy
import json
import uuid
import re
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from brapi_genx.canonicalization import jcs_canonicalize, parse_strict_json, JCSError
try:
    from brapi_genx.idempotency import (
        PostgresIdempotencyStore,
        IdempotencyIdentity,
        IdempotencyStatus,
    )
    _IDEMPOTENCY_IMPORT_ERROR = None
except Exception as _exc:  # pragma: no cover - optional dependency guard
    PostgresIdempotencyStore = None
    IdempotencyIdentity = None
    IdempotencyStatus = None
    _IDEMPOTENCY_IMPORT_ERROR = _exc
import threading
import time
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

TERM_ID_RE = re.compile(r"^[^:/]+:[^:/]+:[^:/]+$")
MODEL_ID_RE = re.compile(r"^[^:/]+:model:[^:/]+$")
MATRIX_ID_RE = re.compile(r"^[^:/]+:matrix:[^:/]+$")
PACKAGE_ID_RE = re.compile(r"^[^:/]+:package:[^:/]+$")
DOI_RE = re.compile(r"^10\.\d{4,}/.+")
PACKAGE_RIGHTS = ("open", "embargoed", "restricted")
DECIMAL_RE = re.compile(r"^-?\d+(\.\d+)?$")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
LEDGER_TYPES = ("adjust", "move", "handoff", "production", "planting", "trade")

SUPPORTED_JOB_TYPES = ("germplasm_search", "analysis", "inference")
TERMINAL = ("COMPLETED", "FAILED", "CANCELLED", "EXPIRED")

GERMPLASM = [
    {"germplasmDbId": "GERM01", "germplasmName": "Germ 01"},
    {"germplasmDbId": "GERM02", "germplasmName": "Germ 02"},
    {"germplasmDbId": "GERM03", "germplasmName": "Germ 03"},
]


def utcnow():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def canonical(doc):
    """JCS-canonicalized form (authoritative, RFC 8785) of a parsed JSON value."""
    raw = json.dumps(doc).encode("utf-8")
    return jcs_canonicalize(raw).decode("utf-8")


def envelope(result=None, data=None, pagination=None, status=None, datafiles=None):
    body = {
        "metadata": {
            "pagination": pagination if pagination is not None else {},
            "status": status if status is not None else [],
            "datafiles": datafiles if datafiles is not None else [],
        },
    }
    if data is not None:
        body["result"] = {"data": data}
    elif result is not None:
        body["result"] = result
    return body


# Default identity used by the reference server when no auth/tenant context is
# available. Tenant/client/principal isolation is still enforced by the store
# schema; the reference server simply operates as a single default principal.
DEFAULT_TENANT_ID = uuid.UUID("00000000-0000-0000-0000-000000000000")
DEFAULT_CLIENT_ID = uuid.UUID("00000000-0000-0000-0000-000000000000")
DEFAULT_PRINCIPAL_ID = uuid.UUID("00000000-0000-0000-0000-000000000000")


class Store:
    def __init__(self, ttl_days=7, delay=1.0, idempotency_store=None, idempotency_dsn=None,
                 init_from_env=False):
        if isinstance(idempotency_store, str):
            idempotency_dsn = idempotency_store
            idempotency_store = None
        if idempotency_store is None and idempotency_dsn is None and init_from_env:
            idempotency_dsn = os.environ.get("GENX_IDEMPOTENCY_DSN")
        if idempotency_store is None and idempotency_dsn:
            idempotency_store = create_idempotency_store(idempotency_dsn)
        self.lock = threading.Lock()
        self.jobs = {}
        self.idempotency = {}  # key -> {"body": canonical, "jobDbId": str}
        self.counter = 0
        self.ttl = timedelta(days=ttl_days)
        self.delay = delay
        self.idempotency_store = idempotency_store
        self.idempotency_mode = (
            "authoritative" if idempotency_store is not None
            else "non_authoritative_dev"
        )
        self.variable_terms = {}  # (variableDbId, version) -> term, insertion ordered
        self.variable_term_order = []
        self.ledger = {}  # seedLotDbId -> [entries in position order]
        self.ledger_keys = {}  # idempotencyKey -> {"lot": ..., "entryDbId": ..., "body": canonical}
        self.ledger_counter = 0
        self.models = {}  # (modelDbId, modelVersion) -> artifact, insertion ordered
        self.model_order = []
        self.matrices = {}  # matrixDbId -> record, insertion ordered
        self.matrix_order = []
        self.packages = {}  # packageDbId -> record, insertion ordered
        self.package_order = []
        self.telemetry = {}  # (deviceDbId, sensorDbId, timestamp) -> point
        past = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.jobs["JOB_EXPIRED"] = {
            "jobDbId": "JOB_EXPIRED",
            "jobType": "germplasm_search",
            "status": "EXPIRED",
            "createdAt": past,
            "updatedAt": past,
            "expiresAt": past,
        }

    def _create_unlocked(self, job_type, parameters, key):
        """Create a job while the caller holds self.lock."""
        self.counter += 1
        job_id = f"JOB_{self.counter:04d}"
        now = utcnow()
        job = {
            "jobDbId": job_id,
            "jobType": job_type,
            "status": "SUBMITTED",
            "createdAt": now,
            "updatedAt": now,
            "expiresAt": (datetime.now(timezone.utc) + self.ttl).strftime(
                "%Y-%m-%dT%H:%M:%SZ"),
        }
        if key:
            job["idempotencyKey"] = key
        self.jobs[job_id] = job
        return copy.deepcopy(job)

    def create(self, job_type, parameters, key):
        with self.lock:
            return self._create_unlocked(job_type, parameters, key)

    def submit_idempotent(self, job_type, parameters, key, body_canonical):
        """Atomically check the idempotency key, create the job, and publish the key."""
        pg = getattr(self, "idempotency_store", None)
        if pg is not None and key:
            identity = IdempotencyIdentity(
                DEFAULT_TENANT_ID, DEFAULT_CLIENT_ID, DEFAULT_PRINCIPAL_ID,
                "genxSubmitAsyncJob", key,
            )
            record, disposition = pg.claim(identity, body_canonical)
            if disposition == "conflict":
                return None, "conflict"
            if disposition == "in_progress":
                return None, "in_progress"
            if disposition == "replay":
                job = getattr(record, "response_body", None)
                if not isinstance(job, dict):
                    job = self.jobs.get(getattr(job, "jobDbId", None)) if isinstance(job, str) else None
                # fall back to in-memory map if present
                if not isinstance(job, dict):
                    seen = self.idempotency.get(key)
                    if seen:
                        job = copy.deepcopy(self.jobs.get(seen["jobDbId"]))
                return (copy.deepcopy(job) if isinstance(job, dict) else None), "replay"
            # acquired
            with self.lock:
                job = self._create_unlocked(job_type, parameters, key)
            try:
                pg.complete(
                    identity, body_canonical, 202, copy.deepcopy(job),
                    "application/json",
                )
            except Exception:
                try:
                    pg.fail(identity, retryable=True, failure_kind="server_error")
                except Exception:
                    pass
            with self.lock:
                if key:
                    self.idempotency[key] = {
                        "body": body_canonical,
                        "jobDbId": job["jobDbId"],
                    }
            return job, "created"

        with self.lock:
            seen = self.idempotency.get(key) if key else None
            if seen:
                job = copy.deepcopy(self.jobs[seen["jobDbId"]])
                if seen["body"] == body_canonical:
                    return job, "replay"
                return None, "conflict"

            job = self._create_unlocked(job_type, parameters, key)
            if key:
                self.idempotency[key] = {
                    "body": body_canonical,
                    "jobDbId": job["jobDbId"],
                }
            return job, "created"

    def get(self, job_id):
        with self.lock:
            job = self.jobs.get(job_id)
            return copy.deepcopy(job) if job else None

    def close(self):
        pg = getattr(self, "idempotency_store", None)
        if pg is not None and hasattr(pg, "close"):
            pg.close()
        self.idempotency_store = None
        self.idempotency_mode = "closed"

    def set_status(self, job_id, status, result=None):
        with self.lock:
            job = self.jobs.get(job_id)
            if not job or job["status"] in TERMINAL:
                return None
            job["status"] = status
            job["updatedAt"] = utcnow()
            if result is not None:
                job["result"] = result
            return copy.deepcopy(job)


def build_result(job_type, parameters, store=None):
    if job_type == "germplasm_search":
        names = set((parameters or {}).get("germplasmNames", []))
        ids = set((parameters or {}).get("germplasmDbIds", []))
        rows = [
            g for g in GERMPLASM
            if (not names and not ids)
            or g["germplasmName"] in names
            or g["germplasmDbId"] in ids
        ]
        return {"data": rows}
    if job_type == "analysis":
        obs = (parameters or {}).get("observation")
        return {"data": [obs] if obs is not None else []}
    if job_type == "inference":
        return build_inference(store, parameters or {})
    return {"data": []}


def resolve_model(store, model_id, version=None):
    with store.lock:
        if version:
            return copy.deepcopy(store.models.get((model_id, version)))
        found = None
        for key in store.model_order:
            if key[0] == model_id:
                found = store.models[key]
        return copy.deepcopy(found) if found else None


def build_inference(store, parameters):
    import hashlib
    model = resolve_model(store, parameters.get("modelDbId"), parameters.get("modelVersion"))
    if model is None or model.get("status") == "revoked":
        return None
    inputs = parameters.get("inputs")
    digest = hashlib.sha256(canonical(inputs).encode("utf-8")).hexdigest()
    return {"data": [{
        "modelDbId": model["modelDbId"],
        "modelVersion": model["modelVersion"],
        "inputsDigest": digest,
        "outputs": {"echo": inputs},
        "uncertainty": {"type": "echo_stub", "value": 0.0},
    }]}


def run_job(store, job_id, job_type, parameters):
    time.sleep(store.delay / 2)
    if not store.set_status(job_id, "RUNNING"):
        return
    time.sleep(store.delay / 2)
    if job_type == "inference":
        result = build_result(job_type, parameters, store)
        if result is None:
            store.set_status(job_id, "FAILED")
            return
        store.set_status(job_id, "COMPLETED", result)
        return
    store.set_status(job_id, "COMPLETED", build_result(job_type, parameters, store))


class Handler(BaseHTTPRequestHandler):
    server_version = "GenXTestServer/0.1"

    def log_message(self, fmt, *args):  # stderr logging, single line per request
        sys.stderr.write(f"{utcnow()} {self.command} {self.path} {fmt % args}\n")

    def _route(self):
        path = urlparse(self.path).path
        for prefix in ("/genx/v1", "/brapi/v2"):
            if path == prefix or path.startswith(prefix + "/"):
                path = path[len(prefix):] or "/"
                break
        return path

    def _send_json(self, code, doc):
        raw = json.dumps(doc).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _send_text(self, code, message):
        raw = f"ERROR - {utcnow()} - {message}\n".encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _read_json(self):
        length = int(self.headers.get("Content-Length") or 0)
        if not length:
            return {}
        raw = self.rfile.read(length)
        try:
            return parse_strict_json(raw)
        except (JCSError, Exception):
            return None

    # -- endpoints ------------------------------------------------------

    def do_GET(self):
        if self.server.profile == "v21" and self._route() != "/serverinfo":
            return self._send_text(404, f"unknown path {self.path}")
        if self._route() == "/serverinfo":
            return self._serverinfo()
        if self._route().startswith("/jobs/"):
            return self._job_get()
        if self._route() == "/jobs":
            return self._job_list()
        if self._route() == "/variable-terms":
            return self._variable_term_list()
        if self._route().startswith("/variable-terms/"):
            return self._variable_term_get()
        if "/ledger" in self._route():
            parts = self._route().strip("/").split("/")
            if len(parts) == 3 and parts[0] == "seedlots" and parts[2] == "ledger":
                return self._ledger_list(parts[1])
        if self._route() == "/models":
            return self._model_list()
        if self._route().startswith("/models/"):
            return self._model_get()
        if self._route() == "/variantmatrices":
            return self._matrix_list()
        if self._route().startswith("/variantmatrices/"):
            return self._matrix_get()
        if self._route() == "/fair-packages":
            return self._package_list()
        if self._route().startswith("/fair-packages/"):
            return self._package_get()
        if self._route() == "/telemetry":
            return self._telemetry_read()
        return self._send_text(404, f"unknown path {self.path}")

    def do_POST(self):
        if self.server.profile == "v21":
            return self._send_text(404, f"unknown path {self.path}")
        if self._route() == "/jobs":
            return self._job_submit()
        if self._route() == "/variable-terms":
            return self._variable_term_publish()
        if "/ledger" in self._route():
            parts = self._route().strip("/").split("/")
            if len(parts) == 3 and parts[0] == "seedlots" and parts[2] == "ledger":
                return self._ledger_append(parts[1])
        if self._route() == "/models":
            return self._model_publish()
        if self._route() == "/variantmatrices":
            return self._matrix_publish()
        if self._route() == "/fair-packages":
            return self._package_publish()
        if self._route() == "/telemetry":
            return self._telemetry_append()
        return self._send_text(404, f"unknown path {self.path}")

    def do_DELETE(self):
        if self.server.profile == "v21":
            return self._send_text(404, f"unknown path {self.path}")
        if self._route().startswith("/jobs/"):
            return self._job_cancel()
        return self._send_text(404, f"unknown path {self.path}")

    def _serverinfo(self):
        if self.server.profile == "v21":
            return self._send_json(200, envelope(result={
                "serverName": "GenX V2.1-only Test Server",
                "organizationName": "The Institute",
                "calls": [
                    {"service": "germplasm/{germplasmDbId}/pedigree",
                     "versions": ["2.0", "2.1"], "methods": ["GET"]},
                    {"service": "germplasm-search",
                     "versions": ["2.0", "2.1"], "methods": ["POST"]},
                ],
            }))
        return self._send_json(200, envelope(result={
            "serverName": "GenX Conformance Test Server",
            "organizationName": "The Institute",
            "organizationURL": "institute.org/home",
            "contactEmail": "contact@institute.org",
            "documentationURL": "institute.org/server",
            "location": "local",
            "calls": [
                {"service": "germplasm/{germplasmDbId}/pedigree",
                 "versions": ["2.0", "2.1"], "methods": ["GET"]},
            ],
            "brapiVersions": ["2.1", "3.0-draft"],
            "capabilities": [
                {
                    "name": "jobs",
                    "versions": [
                        "1.0"
                    ],
                    "methods": [
                        "GET",
                        "POST",
                        "DELETE"
                    ],
                    "jobTypes": list(SUPPORTED_JOB_TYPES),
                    "scopes": [
                        "jobs.submit",
                        "jobs.read"
                    ],
                    "operations": [
                        {
                            "method": "GET",
                            "route": "/genx/v1/jobs",
                            "operationId": "genxListJobs"
                        },
                        {
                            "method": "POST",
                            "route": "/genx/v1/jobs",
                            "operationId": "genxSubmitAsyncJob"
                        },
                        {
                            "method": "GET",
                            "route": "/genx/v1/jobs/{jobDbId}",
                            "operationId": "genxGetAsyncJobById"
                        },
                        {
                            "method": "DELETE",
                            "route": "/genx/v1/jobs/{jobDbId}",
                            "operationId": "genxRequestAsyncJobCancellation"
                        }
                    ]
                },
                {
                    "name": "provenanceEnvelope",
                    "versions": [
                        "1.0"
                    ],
                    "methods": [
                        "GET",
                        "POST"
                    ],
                    "scopes": [],
                    "operations": [
                        {
                            "method": "POST",
                            "route": "/genx/v1/jobs",
                            "operationId": "genxSubmitAsyncJob"
                        },
                        {
                            "method": "GET",
                            "route": "/genx/v1/jobs/{jobDbId}",
                            "operationId": "genxGetAsyncJobById"
                        }
                    ]
                },
                {
                    "name": "variableTerms",
                    "versions": [
                        "1.0"
                    ],
                    "methods": [
                        "GET",
                        "POST"
                    ],
                    "scopes": [
                        "ontology.write"
                    ],
                    "operations": [
                        {
                            "method": "GET",
                            "route": "/genx/v1/variable-terms",
                            "operationId": "genxListVariableTermVersions"
                        },
                        {
                            "method": "POST",
                            "route": "/genx/v1/variable-terms",
                            "operationId": "genxPublishVariableTermVersion"
                        },
                        {
                            "method": "GET",
                            "route": "/genx/v1/variable-terms/{variableDbId}",
                            "operationId": "genxGetVariableTermVersion"
                        }
                    ]
                },
                {
                    "name": "lotLedger",
                    "versions": [
                        "1.0"
                    ],
                    "methods": [
                        "GET",
                        "POST"
                    ],
                    "scopes": [
                        "seedlots.ledger.append",
                        "seedlots.ledger.read"
                    ],
                    "operations": [
                        {
                            "method": "GET",
                            "route": "/genx/v1/seedlots/{seedLotDbId}/ledger",
                            "operationId": "genxListSeedLotLedgerEntries"
                        },
                        {
                            "method": "POST",
                            "route": "/genx/v1/seedlots/{seedLotDbId}/ledger",
                            "operationId": "genxAppendSeedLotLedgerEntry"
                        }
                    ]
                },
                {
                    "name": "modelRegistry",
                    "versions": [
                        "1.0"
                    ],
                    "methods": [
                        "GET",
                        "POST"
                    ],
                    "scopes": [
                        "models.register",
                        "models.read",
                        "jobs.infer"
                    ],
                    "operations": [
                        {
                            "method": "GET",
                            "route": "/genx/v1/models",
                            "operationId": "genxListModelVersions"
                        },
                        {
                            "method": "POST",
                            "route": "/genx/v1/models",
                            "operationId": "genxRegisterModelVersion"
                        },
                        {
                            "method": "GET",
                            "route": "/genx/v1/models/{modelDbId}",
                            "operationId": "genxGetModelVersion"
                        }
                    ]
                },
                {
                    "name": "variantMatrices",
                    "versions": [
                        "1.0"
                    ],
                    "methods": [
                        "GET",
                        "POST"
                    ],
                    "scopes": [
                        "matrices.register",
                        "matrices.read"
                    ],
                    "operations": [
                        {
                            "method": "GET",
                            "route": "/genx/v1/variantmatrices",
                            "operationId": "genxListVariantMatrixReferences"
                        },
                        {
                            "method": "POST",
                            "route": "/genx/v1/variantmatrices",
                            "operationId": "genxRegisterVariantMatrixReference"
                        },
                        {
                            "method": "GET",
                            "route": "/genx/v1/variantmatrices/{matrixDbId}",
                            "operationId": "genxGetVariantMatrixReference"
                        }
                    ]
                },
                {
                    "name": "fairPackages",
                    "versions": [
                        "1.0"
                    ],
                    "methods": [
                        "GET",
                        "POST"
                    ],
                    "scopes": [
                        "packages.register",
                        "packages.read"
                    ],
                    "operations": [
                        {
                            "method": "GET",
                            "route": "/genx/v1/fair-packages",
                            "operationId": "genxListFairPackageMetadata"
                        },
                        {
                            "method": "POST",
                            "route": "/genx/v1/fair-packages",
                            "operationId": "genxRegisterFairPackage"
                        },
                        {
                            "method": "GET",
                            "route": "/genx/v1/fair-packages/{packageDbId}",
                            "operationId": "genxGetFairPackageMetadata"
                        }
                    ]
                },
                {
                    "name": "telemetry",
                    "versions": [
                        "1.0"
                    ],
                    "methods": [
                        "GET",
                        "POST"
                    ],
                    "scopes": [
                        "telemetry.append",
                        "telemetry.read"
                    ],
                    "operations": [
                        {
                            "method": "GET",
                            "route": "/genx/v1/telemetry",
                            "operationId": "genxQueryTelemetrySamplesOrAggregates"
                        },
                        {
                            "method": "POST",
                            "route": "/genx/v1/telemetry",
                            "operationId": "genxAppendTelemetryBatch"
                        }
                    ]
                }
            ],
            "authProfiles": [{"name": "none", "scopes": []}],
        }))

    def _job_list(self):
        store = self.server.store
        query = self._query()
        with store.lock:
            jobs = sorted(store.jobs.values(), key=lambda j: j["jobDbId"])
        if query.get("jobType"):
            jobs = [job for job in jobs if job["jobType"] == query["jobType"]]
        if query.get("status"):
            jobs = [job for job in jobs if job["status"] == query["status"]]
        try:
            page = max(int(query.get("page", "0")), 0)
            size = max(int(query.get("pageSize", str(max(len(jobs), 1)))), 1)
        except ValueError:
            return self._send_text(400, "page and pageSize must be integers")
        total = len(jobs)
        return self._send_json(200, envelope(
            data=jobs[page * size:(page + 1) * size],
            pagination={"totalCount": total, "pageSize": size,
                        "totalPages": max(1, (total + size - 1) // size),
                        "currentPage": page},
        ))

    def _job_submit(self):
        store = self.server.store
        body = self._read_json()
        if body is None:
            return self._send_text(400, "malformed JSON request object")
        job_type = body.get("jobType")
        if job_type not in SUPPORTED_JOB_TYPES:
            return self._send_text(400, f"unknown jobType '{job_type}'")
        warnings = []
        if job_type == "inference":
            params = body.get("parameters") or {}
            model = resolve_model(store, params.get("modelDbId"), params.get("modelVersion"))
            if model is None:
                return self._send_text(400, f"unknown model '{params.get('modelDbId')}'")
            if model.get("status") == "revoked":
                return self._send_text(400, f"model '{model['modelDbId']}' is revoked")
            if model.get("status") == "deprecated":
                warnings.append({"message": f"model '{model['modelDbId']}' is deprecated",
                                 "messageType": "WARNING"})
        key = self.headers.get("Idempotency-Key") or body.get("idempotencyKey")
        canon = canonical(body)
        job, disposition = store.submit_idempotent(
            job_type, body.get("parameters") or {}, key, canon
        )
        if disposition == "conflict":
            return self._send_text(409, "idempotency key already used with a different body")
        if disposition == "in_progress":
            return self._send_text(409, "idempotency key in progress")
        if disposition == "replay":
            return self._send_json(200, envelope(
                result=job,
                status=[{"message": "Replayed existing job",
                         "messageType": "INFO"}],
            ))
        worker = threading.Thread(
            target=run_job,
            args=(store, job["jobDbId"], job_type, body.get("parameters") or {}),
            daemon=True,
        )
        worker.start()
        return self._send_json(202, envelope(
            result=job,
            status=[{"message": "Job accepted", "messageType": "INFO"}] + warnings,
        ))

    def _job_id(self):
        return self._route().split("/jobs/", 1)[1].split("/")[0]

    def _job_get(self):
        job = self.server.store.get(self._job_id())
        if not job:
            return self._send_text(404, f"unknown job '{self._job_id()}'")
        if job["status"] == "EXPIRED":
            slim = {k: v for k, v in job.items() if k != "result"}
            return self._send_json(200, envelope(result=slim))
        return self._send_json(200, envelope(result=job))

    def _job_cancel(self):
        store = self.server.store
        job = store.get(self._job_id())
        if not job:
            return self._send_text(404, f"unknown job '{self._job_id()}'")
        if job["status"] in TERMINAL:
            return self._send_text(400, f"job {job['jobDbId']} is terminal ({job['status']})")
        cancelled = store.set_status(job["jobDbId"], "CANCELLED")
        return self._send_json(200, envelope(result=cancelled))

    # -- versioned variable terms -----------------------------------------------

    def _query(self):
        return {k: v[0] for k, v in parse_qs(urlparse(self.path).query).items()}

    def _variable_term_publish(self):
        store = self.server.store
        body = self._read_json()
        if body is None:
            return self._send_text(400, "malformed JSON request object")
        vid = body.get("variableDbId") or ""
        version = body.get("version") or ""
        if not TERM_ID_RE.match(vid):
            return self._send_text(400, f"variableDbId '{vid}' is not namespaced")
        if not version:
            return self._send_text(400, "missing term version")
        term = copy.deepcopy(body)
        term.setdefault("status", "active")
        if term["status"] not in ("active", "deprecated"):
            return self._send_text(400, f"unknown status '{term['status']}'")
        key = (vid, version)
        with store.lock:
            existing = store.variable_terms.get(key)
            if existing is not None:
                if canonical(existing) == canonical(term):
                    return self._send_json(200, envelope(
                        result=existing,
                        status=[{"message": "Replayed existing term version",
                                 "messageType": "INFO"}],
                    ))
                return self._send_text(
                    409, f"term {vid} version {version} already published "
                         "with a different body")
            store.variable_terms[key] = term
            store.variable_term_order.append(key)
        return self._send_json(200, envelope(
            result=term,
            status=[{"message": "Term version published", "messageType": "INFO"}],
        ))

    def _variable_term_list(self):
        store = self.server.store
        query = self._query()
        with store.lock:
            terms = [store.variable_terms[k] for k in store.variable_term_order]
        for field in ("variableDbId", "ontologyDbId", "status"):
            if query.get(field):
                terms = [t for t in terms if t.get(field) == query[field]]
        try:
            page = max(int(query.get("page", "0")), 0)
            size = max(int(query.get("pageSize", "1000")), 1)
        except ValueError:
            return self._send_text(400, "page and pageSize must be integers")
        total_pages = (len(terms) + size - 1) // size if terms else 0
        return self._send_json(200, envelope(
            data=terms[page * size:(page + 1) * size],
            pagination={"totalCount": len(terms), "pageSize": size,
                        "totalPages": total_pages, "currentPage": page},
        ))

    def _variable_term_id(self):
        return self._route().split("/variable-terms/", 1)[1].split("/")[0]

    def _variable_term_get(self):
        store = self.server.store
        vid = self._variable_term_id()
        version = self._query().get("version")
        with store.lock:
            if version:
                term = store.variable_terms.get((vid, version))
            else:
                term = None
                for key in reversed(store.variable_term_order):
                    if key[0] == vid:
                        term = store.variable_terms[key]
                        break
        if term is None:
            return self._send_text(404, f"unknown term '{vid}'")
        return self._send_json(200, envelope(result=term))

    # -- seed-lot ledger --------------------------------------------

    # -- model registry ---------------------------------------------

    def _model_publish(self):
        store = self.server.store
        body = self._read_json()
        if body is None:
            return self._send_text(400, "malformed JSON request object")
        mid = body.get("modelDbId") or ""
        version = body.get("modelVersion") or ""
        if not MODEL_ID_RE.match(mid):
            return self._send_text(400, f"modelDbId '{mid}' is not namespaced")
        if not version:
            return self._send_text(400, "missing model version")
        digest = body.get("artifactDigest") or ""
        if not DIGEST_RE.match(digest):
            return self._send_text(400, "artifactDigest must be SHA-256 hex")
        artifact = copy.deepcopy(body)
        artifact.setdefault("status", "active")
        if artifact["status"] not in ("active", "deprecated", "revoked"):
            return self._send_text(400, f"unknown status '{artifact['status']}'")
        key = (mid, version)
        with store.lock:
            existing = store.models.get(key)
            if existing is not None:
                if canonical(existing) == canonical(artifact):
                    return self._send_json(200, envelope(
                        result=existing,
                        status=[{"message": "Replayed existing model version",
                                 "messageType": "INFO"}],
                    ))
                return self._send_text(
                    409, f"model {mid} version {version} already registered "
                         "with a different body")
            store.models[key] = artifact
            store.model_order.append(key)
        return self._send_json(200, envelope(
            result=artifact,
            status=[{"message": "Model version registered", "messageType": "INFO"}],
        ))

    def _model_list(self):
        store = self.server.store
        query = self._query()
        with store.lock:
            models = [store.models[k] for k in store.model_order]
        for field in ("modelDbId", "status"):
            if query.get(field):
                models = [m for m in models if m.get(field) == query[field]]
        try:
            page = max(int(query.get("page", "0")), 0)
            size = max(int(query.get("pageSize", "1000")), 1)
        except ValueError:
            return self._send_text(400, "page and pageSize must be integers")
        total_pages = (len(models) + size - 1) // size if models else 0
        return self._send_json(200, envelope(
            data=models[page * size:(page + 1) * size],
            pagination={"totalCount": len(models), "pageSize": size,
                        "totalPages": total_pages, "currentPage": page},
        ))

    def _model_get(self):
        store = self.server.store
        mid = self._route().split("/models/", 1)[1].split("/")[0]
        version = self._query().get("version")
        with store.lock:
            if version:
                artifact = store.models.get((mid, version))
            else:
                artifact = None
                for key in reversed(store.model_order):
                    if key[0] == mid:
                        artifact = store.models[key]
                        break
        if artifact is None:
            return self._send_text(404, f"unknown model '{mid}'")
        return self._send_json(200, envelope(result=artifact))

    # -- variant matrices -------------------------------------------

    MATRIX_FORMATS = ("VCF", "BCF", "VCF_ZARR", "PLINK_BED", "OTHER")

    def _matrix_publish(self):
        store = self.server.store
        body = self._read_json()
        if body is None:
            return self._send_text(400, "malformed JSON request object")
        mid = body.get("matrixDbId") or ""
        if not MATRIX_ID_RE.match(mid):
            return self._send_text(400, f"matrixDbId '{mid}' is not namespaced")
        if body.get("format") not in self.MATRIX_FORMATS:
            return self._send_text(400, f"unknown format '{body.get('format')}'")
        url = body.get("fileURL") or ""
        if not url.startswith(("https://", "drs://")):
            return self._send_text(400, "fileURL must be https:// or drs://")
        digest = body.get("fileDigest") or ""
        if not DIGEST_RE.match(digest):
            return self._send_text(400, "fileDigest must be SHA-256 hex")
        record = copy.deepcopy(body)
        with store.lock:
            existing = store.matrices.get(mid)
            if existing is not None:
                if canonical(existing) == canonical(record):
                    return self._send_json(200, envelope(
                        result=existing,
                        status=[{"message": "Replayed existing matrix reference",
                                 "messageType": "INFO"}],
                    ))
                return self._send_text(
                    409, f"matrix {mid} already registered with different bytes")
            store.matrices[mid] = record
            store.matrix_order.append(mid)
        return self._send_json(200, envelope(
            result=record,
            status=[{"message": "Matrix reference registered", "messageType": "INFO"}],
        ))

    def _matrix_list(self):
        store = self.server.store
        query = self._query()
        with store.lock:
            records = [store.matrices[k] for k in store.matrix_order]
        for field in ("variantSetDbId", "format"):
            if query.get(field):
                records = [m for m in records if m.get(field) == query[field]]
        try:
            page = max(int(query.get("page", "0")), 0)
            size = max(int(query.get("pageSize", "1000")), 1)
        except ValueError:
            return self._send_text(400, "page and pageSize must be integers")
        total_pages = (len(records) + size - 1) // size if records else 0
        return self._send_json(200, envelope(
            data=records[page * size:(page + 1) * size],
            pagination={"totalCount": len(records), "pageSize": size,
                        "totalPages": total_pages, "currentPage": page},
        ))

    def _matrix_get(self):
        mid = self._route().split("/variantmatrices/", 1)[1].split("/")[0]
        record = self.server.store.matrices.get(mid)
        if record is None:
            return self._send_text(404, f"unknown matrix '{mid}'")
        return self._send_json(200, envelope(result=record))

    # -- FAIR packages ----------------------------------------------

    def _package_publish(self):
        store = self.server.store
        body = self._read_json()
        if body is None:
            return self._send_text(400, "malformed JSON request object")
        pid = body.get("packageDbId") or ""
        if not PACKAGE_ID_RE.match(pid):
            return self._send_text(400, f"packageDbId '{pid}' is not namespaced")
        if not (body.get("title") or "").strip():
            return self._send_text(400, "missing title")
        if not (body.get("license") or "").strip():
            return self._send_text(400, "missing license")
        if body.get("accessRights") not in PACKAGE_RIGHTS:
            return self._send_text(400, f"unknown accessRights '{body.get('accessRights')}'")
        for ident in body.get("identifiers") or []:
            if not isinstance(ident, dict) or not ident.get("value"):
                return self._send_text(400, "identifier without value")
            if ident.get("type") == "DOI" and not DOI_RE.match(ident["value"]):
                return self._send_text(400, f"malformed DOI '{ident['value']}'")
        if body.get("embargoUntil"):
            try:
                parse_rfc3339(body["embargoUntil"])
            except ValueError:
                return self._send_text(400, "embargoUntil must be RFC 3339")
        record = copy.deepcopy(body)
        with store.lock:
            existing = store.packages.get(pid)
            if existing is not None:
                if canonical(existing) == canonical(record):
                    return self._send_json(200, envelope(
                        result=existing,
                        status=[{"message": "Replayed existing package",
                                 "messageType": "INFO"}],
                    ))
                return self._send_text(
                    409, f"package {pid} already registered with a different body")
            store.packages[pid] = record
            store.package_order.append(pid)
        return self._send_json(200, envelope(
            result=record,
            status=[{"message": "FAIR package registered", "messageType": "INFO"}],
        ))

    def _package_list(self):
        store = self.server.store
        query = self._query()
        with store.lock:
            records = [store.packages[k] for k in store.package_order]
        for field in ("accessRights", "license"):
            if query.get(field):
                records = [p for p in records if p.get(field) == query[field]]
        try:
            page = max(int(query.get("page", "0")), 0)
            size = max(int(query.get("pageSize", "1000")), 1)
        except ValueError:
            return self._send_text(400, "page and pageSize must be integers")
        total_pages = (len(records) + size - 1) // size if records else 0
        return self._send_json(200, envelope(
            data=records[page * size:(page + 1) * size],
            pagination={"totalCount": len(records), "pageSize": size,
                        "totalPages": total_pages, "currentPage": page},
        ))

    def _package_get(self):
        pid = self._route().split("/fair-packages/", 1)[1].split("/")[0]
        record = self.server.store.packages.get(pid)
        if record is None:
            return self._send_text(404, f"unknown package '{pid}'")
        if record.get("embargoUntil"):
            try:
                embargoed = parse_rfc3339(record["embargoUntil"]) > datetime.now(timezone.utc)
            except ValueError:
                embargoed = False
            if embargoed:
                return self._send_text(403, f"package '{pid}' is embargoed")
        return self._send_json(200, envelope(result=record))

    # -- telemetry ----------------------------------------------------

    TELEMETRY_QUALITY = ("good", "suspect", "bad")
    TELEMETRY_AGG = ("none", "mean", "min", "max", "count")

    def _telemetry_append(self):
        store = self.server.store
        body = self._read_json()
        if not isinstance(body, list):
            return self._send_text(400, "telemetry batch must be an array")
        appended, replayed, conflicts = 0, 0, []
        with store.lock:
            for point in body:
                if not isinstance(point, dict):
                    return self._send_text(400, "telemetry batch elements must be objects")
                device = point.get("deviceDbId") or ""
                sensor = point.get("sensorDbId") or ""
                stamp = point.get("timestamp") or ""
                value = point.get("value")
                if not device or not sensor or not stamp or value is None:
                    return self._send_text(400, "point missing deviceDbId, sensorDbId, timestamp, or value")
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    return self._send_text(400, "point value must be a JSON number")
                try:
                    parse_rfc3339(stamp)
                except ValueError:
                    return self._send_text(400, "point timestamp must be RFC 3339")
                record = copy.deepcopy(point)
                record.setdefault("quality", "good")
                if record["quality"] not in self.TELEMETRY_QUALITY:
                    return self._send_text(400, f"unknown quality '{record['quality']}'")
                key = (device, sensor, stamp)
                existing = store.telemetry.get(key)
                if existing is not None:
                    if existing["value"] == value and canonical(existing) == canonical(record):
                        replayed += 1
                    else:
                        conflicts.append(f"{device}/{sensor}/{stamp}")
                else:
                    store.telemetry[key] = record
                    appended += 1
        return self._send_json(200, envelope(result={
            "appended": appended, "replayed": replayed, "conflicts": conflicts}))

    def _telemetry_read(self):
        store = self.server.store
        query = self._query()
        device = query.get("deviceDbId") or ""
        if not device:
            return self._send_text(400, "missing deviceDbId")
        aggregation = query.get("aggregation", "none")
        if aggregation not in self.TELEMETRY_AGG:
            return self._send_text(400, f"unknown aggregation '{aggregation}'")
        try:
            start = parse_rfc3339(query["from"]) if query.get("from") else None
            end = parse_rfc3339(query["to"]) if query.get("to") else None
            window = int(query.get("windowSeconds", "0") or 0)
        except ValueError:
            return self._send_text(400, "from, to, and windowSeconds must be valid")
        if window < 0:
            return self._send_text(400, "windowSeconds must be non-negative")
        with store.lock:
            points = [p for (d, s, _), p in store.telemetry.items()
                      if d == device
                      and (not query.get("sensorDbId") or s == query["sensorDbId"])]
        rows = []
        for point in points:
            stamp = parse_rfc3339(point["timestamp"])
            if start and stamp < start:
                continue
            if end and stamp >= end:
                continue
            rows.append((stamp, point))
        rows.sort(key=lambda r: r[0])
        if aggregation == "none":
            data = [p for _, p in rows]
        else:
            anchor = start or (rows[0][0] if rows else None)
            buckets = {}
            for stamp, point in rows:
                index = 0 if not window else int((stamp - anchor).total_seconds() // window)
                buckets.setdefault(index, []).append(point["value"])
            data = []
            for index in sorted(buckets):
                values = buckets[index]
                if aggregation == "mean":
                    agg_value = sum(values) / len(values)
                elif aggregation == "min":
                    agg_value = min(values)
                elif aggregation == "max":
                    agg_value = max(values)
                else:
                    agg_value = len(values)
                origin = anchor.timestamp() + index * window if window else anchor.timestamp()
                data.append({
                    "windowStart": datetime.fromtimestamp(origin, tz=timezone.utc).strftime(
                        "%Y-%m-%dT%H:%M:%SZ"),
                    "aggregation": aggregation,
                    "value": agg_value,
                    "sampleCount": len(values),
                })
        try:
            page = max(int(query.get("page", "0")), 0)
            size = max(int(query.get("pageSize", "1000")), 1)
        except ValueError:
            return self._send_text(400, "page and pageSize must be integers")
        total_pages = (len(data) + size - 1) // size if data else 0
        return self._send_json(200, envelope(
            data=data[page * size:(page + 1) * size],
            pagination={"totalCount": len(data), "pageSize": size,
                        "totalPages": total_pages, "currentPage": page},
        ))

    # -- seed-lot ledger --------------------------------------------

    def _ledger_append(self, lot_id):
        store = self.server.store
        body = self._read_json()
        if body is None:
            return self._send_text(400, "malformed JSON request object")
        entry_type = body.get("entryType")
        quantity = body.get("quantity")
        if entry_type not in LEDGER_TYPES:
            return self._send_text(400, f"unknown entryType '{entry_type}'")
        if not isinstance(quantity, str) or not DECIMAL_RE.match(quantity):
            return self._send_text(400, "quantity must be a fixed-scale decimal string")
        for field in ("units", "actor", "occurredAt"):
            if not body.get(field):
                return self._send_text(400, f"missing '{field}'")
        try:
            parse_rfc3339(body["occurredAt"])
        except ValueError:
            return self._send_text(400, "occurredAt must be RFC 3339")
        key = self.headers.get("Idempotency-Key") or body.get("idempotencyKey")
        canon = canonical(body)
        with store.lock:
            seen = store.ledger_keys.get(key) if key else None
            if seen and seen["lot"] == lot_id:
                entries = store.ledger.get(lot_id, [])
                existing = next(
                    (e for e in entries if e["entryDbId"] == seen["entryDbId"]), None)
                if existing is not None and seen["body"] == canon:
                    return self._send_json(200, envelope(
                        result=existing,
                        status=[{"message": "Replayed existing ledger entry",
                                 "messageType": "INFO"}],
                    ))
                return self._send_text(
                    409, "idempotency key already used with a different body")
            store.ledger_counter += 1
            entries = store.ledger.setdefault(lot_id, [])
            entry = copy.deepcopy(body)
            entry["entryDbId"] = f"LEDGER-{store.ledger_counter:04d}"
            entry["seedLotDbId"] = lot_id
            entry["position"] = len(entries)
            entries.append(entry)
            if key:
                store.ledger_keys[key] = {
                    "lot": lot_id, "entryDbId": entry["entryDbId"], "body": canon}
        return self._send_json(200, envelope(
            result=entry,
            status=[{"message": "Ledger entry appended", "messageType": "INFO"}],
        ))

    def _ledger_list(self, lot_id):
        store = self.server.store
        query = self._query()
        with store.lock:
            entries = list(store.ledger.get(lot_id, []))
        if query.get("entryType"):
            entries = [e for e in entries if e.get("entryType") == query["entryType"]]
        try:
            page = max(int(query.get("page", "0")), 0)
            size = max(int(query.get("pageSize", "1000")), 1)
        except ValueError:
            return self._send_text(400, "page and pageSize must be integers")
        total_pages = (len(entries) + size - 1) // size if entries else 0
        return self._send_json(200, envelope(
            data=entries[page * size:(page + 1) * size],
            pagination={"totalCount": len(entries), "pageSize": size,
                        "totalPages": total_pages, "currentPage": page},
        ))


def parse_rfc3339(value):
    text = value.replace("Z", "+00:00") if value.endswith("Z") else value
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        raise ValueError("missing timezone offset")
    return parsed


def create_idempotency_store(dsn=None, migrate=True, validate=True):
    """Initialize a PostgreSQL-backed idempotency store from DSN or env.

    Returns None when no DSN is configured (non-authoritative dev mode).
    Raises if a configured store cannot be initialized or validated.
    """
    if dsn is None:
        dsn = os.environ.get("GENX_IDEMPOTENCY_DSN")
    if not dsn:
        return None
    if PostgresIdempotencyStore is None:
        raise RuntimeError(f"idempotency module unavailable: {_IDEMPOTENCY_IMPORT_ERROR}")
    store = PostgresIdempotencyStore(dsn)
    if migrate:
        store.migrate()
    if validate:
        with store._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
    return store


def create_store(ttl_days=7, delay=1.0, idempotency_store=None, idempotency_dsn=None,
                init_from_env=True, **kwargs):
    if isinstance(idempotency_store, str):
        idempotency_dsn = idempotency_store
        idempotency_store = None
    if idempotency_store is None and idempotency_dsn is None and init_from_env:
        idempotency_dsn = os.environ.get("GENX_IDEMPOTENCY_DSN")
    if idempotency_store is None and idempotency_dsn:
        idempotency_store = create_idempotency_store(idempotency_dsn)
    return Store(
        ttl_days=ttl_days, delay=delay,
        idempotency_store=idempotency_store, **kwargs,
    )


class GenXHTTPServer(ThreadingHTTPServer):
    def server_close(self):
        super().server_close()
        store = getattr(self, "store", None)
        if store is not None and hasattr(store, "close"):
            try:
                store.close()
            except Exception:
                pass


def create_server(port=8080, host="127.0.0.1", profile="genx", ttl_days=7, delay=1.0,
                 idempotency_store=None, idempotency_dsn=None, init_from_env=True,
                 migrate=True, validate=True):
    if isinstance(idempotency_store, str):
        idempotency_dsn = idempotency_store
        idempotency_store = None
    if idempotency_store is None and idempotency_dsn is None and init_from_env:
        idempotency_dsn = os.environ.get("GENX_IDEMPOTENCY_DSN")
    if idempotency_store is None and idempotency_dsn:
        idempotency_store = create_idempotency_store(
            idempotency_dsn, migrate=migrate, validate=validate,
        )
    store = Store(
        ttl_days=ttl_days, delay=delay, idempotency_store=idempotency_store,
    )
    httpd = GenXHTTPServer((host, port), Handler)
    httpd.store = store
    httpd.profile = profile
    httpd.idempotency_store = idempotency_store
    return httpd


def main():
    parser = argparse.ArgumentParser(description="GenX reference test server")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--profile", choices=("genx", "v21"), default="genx")
    parser.add_argument("--ttl-days", type=int, default=7)
    parser.add_argument("--delay", type=float, default=1.0,
                        help="seconds from submit to completion")
    args = parser.parse_args()

    try:
        server = create_server(
            port=args.port, profile=args.profile, ttl_days=args.ttl_days,
            delay=args.delay, init_from_env=True,
        )
    except Exception as exc:
        sys.stderr.write(f"ERROR - startup failed: {exc}\n")
        raise SystemExit(1)
    print(f"GenX test server on 127.0.0.1:{args.port} profile={args.profile}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        try:
            server.server_close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
