#!/usr/bin/env python3
"""
Minimal GenX reference test server (RFC-001). Standard library only.

Implements just enough of the GenX skeleton to execute the live conformance
tier: Jobs lifecycle with idempotency (L-01..L-05, L-07, L-14, L-15),
ServerInfoV3 negotiation (L-06), provenance echo for the `analysis` job type,
versioned ontology terms (L-08, L-09), append-only lot ledgers (L-10, L-11),
and model registration with digest-bound inference (L-12..L-15). In-memory
state, no persistence, no authentication (Bearer tokens are accepted and
ignored).

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

Idempotency: same key + byte-identical body replays the existing job (200);
same key + different body is rejected with 409 (evidence for the RFC-001 §8
requires-decision on the conflict status code).
"""

import argparse
import copy
import json
import re
import sys
import threading
import time
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

TERM_ID_RE = re.compile(r"^[^:/]+:[^:/]+:[^:/]+$")
MODEL_ID_RE = re.compile(r"^[^:/]+:model:[^:/]+$")
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
    return json.dumps(doc, sort_keys=True, separators=(",", ":"))


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


class Store:
    def __init__(self, ttl_days=7, delay=1.0):
        self.lock = threading.Lock()
        self.jobs = {}
        self.idempotency = {}  # key -> {"body": canonical, "jobDbId": str}
        self.counter = 0
        self.ttl = timedelta(days=ttl_days)
        self.delay = delay
        self.variables = {}  # (variableDbId, version) -> term, insertion ordered
        self.variable_order = []
        self.ledger = {}  # seedLotDbId -> [entries in position order]
        self.ledger_keys = {}  # idempotencyKey -> {"lot": ..., "entryDbId": ..., "body": canonical}
        self.ledger_counter = 0
        self.models = {}  # (modelDbId, modelVersion) -> artifact, insertion ordered
        self.model_order = []
        past = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.jobs["JOB_EXPIRED"] = {
            "jobDbId": "JOB_EXPIRED",
            "jobType": "germplasm_search",
            "status": "EXPIRED",
            "createdAt": past,
            "updatedAt": past,
            "expiresAt": past,
        }

    def create(self, job_type, parameters, key):
        with self.lock:
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

    def get(self, job_id):
        with self.lock:
            job = self.jobs.get(job_id)
            return copy.deepcopy(job) if job else None

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
        for prefix in ("/brapi/v3", "/brapi/v2"):
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
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except Exception:
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
        if self._route() == "/variables":
            return self._var_list()
        if self._route().startswith("/variables/"):
            return self._var_get()
        if "/ledger" in self._route():
            parts = self._route().strip("/").split("/")
            if len(parts) == 3 and parts[0] == "seedlots" and parts[2] == "ledger":
                return self._ledger_list(parts[1])
        if self._route() == "/models":
            return self._model_list()
        if self._route().startswith("/models/"):
            return self._model_get()
        return self._send_text(404, f"unknown path {self.path}")

    def do_POST(self):
        if self.server.profile == "v21":
            return self._send_text(404, f"unknown path {self.path}")
        if self._route() == "/jobs":
            return self._job_submit()
        if self._route() == "/variables":
            return self._var_publish()
        if "/ledger" in self._route():
            parts = self._route().strip("/").split("/")
            if len(parts) == 3 and parts[0] == "seedlots" and parts[2] == "ledger":
                return self._ledger_append(parts[1])
        if self._route() == "/models":
            return self._model_publish()
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
                {"name": "jobs", "versions": ["1.0"],
                 "methods": ["GET", "POST", "DELETE"],
                 "scopes": ["jobs.submit", "jobs.read"]},
                {"name": "provenanceEnvelope", "versions": ["1.0"],
                 "methods": ["GET", "POST"], "scopes": []},
                {"name": "ontologyTerms", "versions": ["1.0"],
                 "methods": ["GET", "POST"], "scopes": ["ontology.write"]},
                {"name": "lotLedger", "versions": ["1.0"],
                 "methods": ["GET", "POST"],
                 "scopes": ["seedlots.ledger.append", "seedlots.ledger.read"]},
                {"name": "modelRegistry", "versions": ["1.0"],
                 "methods": ["GET", "POST"],
                 "scopes": ["models.register", "models.read", "jobs.infer"]},
            ],
            "authProfiles": [{"name": "none", "scopes": []}],
        }))

    def _job_list(self):
        store = self.server.store
        with store.lock:
            jobs = sorted(store.jobs.values(), key=lambda j: j["jobDbId"])
        return self._send_json(200, envelope(
            data=jobs,
            pagination={"totalCount": len(jobs), "pageSize": len(jobs),
                        "totalPages": 1, "currentPage": 0},
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
        with store.lock:
            seen = store.idempotency.get(key) if key else None
            if seen:
                if seen["body"] == canon:
                    return self._send_json(200, envelope(
                        result=store.jobs[seen["jobDbId"]],
                        status=[{"message": "Replayed existing job",
                                 "messageType": "INFO"}],
                    ))
                return self._send_text(409, "idempotency key already used with a different body")
        job = store.create(job_type, body.get("parameters") or {}, key)
        if key:
            with store.lock:
                store.idempotency[key] = {"body": canon, "jobDbId": job["jobDbId"]}
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

    # -- ontology terms -----------------------------------------------

    def _query(self):
        return {k: v[0] for k, v in parse_qs(urlparse(self.path).query).items()}

    def _var_publish(self):
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
            existing = store.variables.get(key)
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
            store.variables[key] = term
            store.variable_order.append(key)
        return self._send_json(200, envelope(
            result=term,
            status=[{"message": "Term version published", "messageType": "INFO"}],
        ))

    def _var_list(self):
        store = self.server.store
        query = self._query()
        with store.lock:
            terms = [store.variables[k] for k in store.variable_order]
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

    def _var_id(self):
        return self._route().split("/variables/", 1)[1].split("/")[0]

    def _var_get(self):
        store = self.server.store
        vid = self._var_id()
        version = self._query().get("version")
        with store.lock:
            if version:
                term = store.variables.get((vid, version))
            else:
                term = None
                for key in reversed(store.variable_order):
                    if key[0] == vid:
                        term = store.variables[key]
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


def main():
    parser = argparse.ArgumentParser(description="GenX reference test server")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--profile", choices=("genx", "v21"), default="genx")
    parser.add_argument("--ttl-days", type=int, default=7)
    parser.add_argument("--delay", type=float, default=1.0,
                        help="seconds from submit to completion")
    args = parser.parse_args()

    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    server.store = Store(ttl_days=args.ttl_days, delay=args.delay)
    server.profile = args.profile
    print(f"GenX test server on 127.0.0.1:{args.port} profile={args.profile}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
