#!/usr/bin/env bun
/**
 * Second GenX reference test server (RFC-001 core + RFC-004 inference).
 * TypeScript/Bun, written black-box from the RFC text — not ported from the
 * Python reference server. Exists to prove the spec interoperates across
 * runtimes, especially digest canonicalization (D-02 evidence).
 *
 * Subset: ServerInfoV3 (+v21 profile), Jobs lifecycle, minimal model
 * registry, inference with genuinely computed inputsDigest. Terms, ledger,
 * matrices, packages, telemetry deliberately excluded (patterns proven).
 *
 * Canonical JSON here: recursively sorted keys, compact separators, UTF-8.
 * Agreement with the Python server holds for ASCII payloads; non-ASCII
 * escaping differs (Python ensure_ascii) — an honest D-02 boundary.
 *
 * Usage:
 *   bun Scripts/genx_test_server_ts.ts --port 18082 --delay 0.4
 *   bun Scripts/genx_test_server_ts.ts --port 18083 --profile v21
 */

import { createHash } from "node:crypto";
import { jcsCanonicalize, parseStrictJson } from "./jcs-canonicalization/jcs.ts";

const args: Record<string, string> = {};
for (let i = 2; i < Bun.argv.length; i += 2) {
  args[Bun.argv[i].replace(/^--/, "")] = Bun.argv[i + 1];
}
const PORT = parseInt(args.port ?? "18082", 10);
const PROFILE = args.profile ?? "genx";
const DELAY = parseFloat(args.delay ?? "1.0");

const SUPPORTED_JOB_TYPES = ["germplasm_search", "analysis", "inference"];
const TERMINAL = new Set(["COMPLETED", "FAILED", "CANCELLED", "EXPIRED"]);
const MODEL_ID_RE = /^[^:/]+:model:[^:/]+$/;
const DIGEST_RE = /^[0-9a-f]{64}$/;

const GERMPLASM = [
  { germplasmDbId: "GERM01", germplasmName: "Germ 01" },
  { germplasmDbId: "GERM02", germplasmName: "Germ 02" },
  { germplasmDbId: "GERM03", germplasmName: "Germ 03" },
];

function utcnow(): string {
  return new Date().toISOString().replace(/\.\d+Z$/, "Z");
}

function canonical(value: unknown): string {
  if (value === undefined) value = null;
  const bytes = new TextEncoder().encode(JSON.stringify(value));
  return new TextDecoder().decode(jcsCanonicalize(bytes));
}

function sha256hex(text: string): string {
  return createHash("sha256").update(text, "utf8").digest("hex");
}

function json(code: number, doc: unknown): Response {
  return new Response(JSON.stringify(doc), {
    status: code,
    headers: { "Content-Type": "application/json" },
  });
}

function text(code: number, message: string): Response {
  return new Response(`ERROR - ${utcnow()} - ${message}\n`, {
    status: code,
    headers: { "Content-Type": "text/plain" },
  });
}

interface Job {
  jobDbId: string;
  jobType: string;
  status: string;
  progress?: number;
  createdAt: string;
  updatedAt: string;
  expiresAt: string;
  idempotencyKey?: string;
  result?: unknown;
}

const jobs = new Map<string, Job>();
const idempotency = new Map<string, { body: string; jobDbId: string }>();
const models = new Map<string, Record<string, unknown>>();
const modelOrder: Array<[string, string]> = [];
let jobCounter = 0;

const past = new Date(Date.now() - 86400000).toISOString().replace(/\.\d+Z$/, "Z");
jobs.set("JOB_EXPIRED", {
  jobDbId: "JOB_EXPIRED",
  jobType: "germplasm_search",
  status: "EXPIRED",
  createdAt: past,
  updatedAt: past,
  expiresAt: past,
});

function resolveModel(id: string, version?: string): Record<string, unknown> | null {
  if (version) return (models.get(`${id} ${version}`) as Record<string, unknown>) ?? null;
  for (let i = modelOrder.length - 1; i >= 0; i--) {
    if (modelOrder[i][0] === id) return models.get(`${id} ${modelOrder[i][1]}`) ?? null;
  }
  return null;
}

function buildResult(jobType: string, params: Record<string, unknown>): unknown {
  if (jobType === "germplasm_search") {
    const names = new Set((params.germplasmNames as string[]) ?? []);
    const ids = new Set((params.germplasmDbIds as string[]) ?? []);
    return {
      data: GERMPLASM.filter(
        (g) => (!names.size && !ids.size) || names.has(g.germplasmName) || ids.has(g.germplasmDbId),
      ),
    };
  }
  if (jobType === "analysis") {
    const obs = params.observation;
    return { data: obs !== undefined ? [obs] : [] };
  }
  if (jobType === "inference") {
    const model = resolveModel(params.modelDbId as string, params.modelVersion as string | undefined);
    if (!model || model.status === "revoked") return null;
    const inputs = params.inputs;
    return {
      data: [
        {
          modelDbId: model.modelDbId,
          modelVersion: model.modelVersion,
          inputsDigest: sha256hex(canonical(inputs)),
          outputs: { echo: inputs },
          uncertainty: { type: "echo_stub", value: 0.0 },
        },
      ],
    };
  }
  return { data: [] };
}

function runJob(jobId: string, jobType: string, params: Record<string, unknown>): void {
  setTimeout(() => {
    const job = jobs.get(jobId);
    if (!job || TERMINAL.has(job.status)) return;
    job.status = "RUNNING";
    job.updatedAt = utcnow();
    setTimeout(() => {
      const live = jobs.get(jobId);
      if (!live || TERMINAL.has(live.status)) return;
      const result = buildResult(jobType, params);
      if (result === null) {
        live.status = "FAILED";
      } else {
        live.status = "COMPLETED";
        live.result = result;
      }
      live.updatedAt = utcnow();
    }, (DELAY * 1000) / 2);
  }, (DELAY * 1000) / 2);
}

function stripPrefix(path: string): string {
  for (const prefix of ["/genx/v1", "/brapi/v2"]) {
    if (path === prefix || path.startsWith(prefix + "/")) return path.slice(prefix.length) || "/";
  }
  return path;
}

async function readBody(req: Request): Promise<{ ok: boolean; value: unknown }> {
  const textBody = await req.text();
  if (!textBody) return { ok: true, value: {} };
  try {
    const value = parseStrictJson(new TextEncoder().encode(textBody));
    return { ok: true, value };
  } catch {
    return { ok: false, value: null };
  }
}

const server = Bun.serve({
  port: PORT,
  hostname: "127.0.0.1",
  async fetch(req) {
    const url = new URL(req.url);
    const route = stripPrefix(url.pathname);
    const method = req.method;
    console.error(`${utcnow()} ${method} ${url.pathname}`);

    if (PROFILE === "v21" && route !== "/serverinfo") {
      return text(404, `unknown path ${url.pathname}`);
    }

    if (method === "GET" && route === "/serverinfo") {
      if (PROFILE === "v21") {
        return json(200, {
          metadata: { pagination: {}, status: [], datafiles: [] },
          result: {
            serverName: "GenX V2.1-only Test Server",
            organizationName: "The Institute",
            calls: [
              { service: "germplasm/{germplasmDbId}/pedigree", versions: ["2.0", "2.1"], methods: ["GET"] },
              { service: "germplasm-search", versions: ["2.0", "2.1"], methods: ["POST"] },
            ],
          },
        });
      }
      return json(200, {
        metadata: { pagination: {}, status: [], datafiles: [] },
        result: {
          serverName: "GenX Conformance Test Server (TS)",
          organizationName: "The Institute",
          organizationURL: "institute.org/home",
          contactEmail: "contact@institute.org",
          documentationURL: "institute.org/server",
          location: "local",
          calls: [
            { service: "germplasm/{germplasmDbId}/pedigree", versions: ["2.0", "2.1"], methods: ["GET"] },
          ],
          brapiVersions: ["2.1", "3.0-draft"],
          capabilities: [
            { name: "jobs", versions: ["1.0"], methods: ["GET", "POST", "DELETE"], scopes: ["jobs.submit", "jobs.read"] },
            { name: "provenanceEnvelope", versions: ["1.0"], methods: ["GET", "POST"], scopes: [] },
            { name: "modelRegistry", versions: ["1.0"], methods: ["GET", "POST"], scopes: ["models.register", "models.read", "jobs.infer"] },
          ],
          authProfiles: [{ name: "none", scopes: [] }],
        },
      });
    }

    if (method === "GET" && route === "/jobs") {
      const all = [...jobs.values()].sort((a, b) => (a.jobDbId < b.jobDbId ? -1 : 1));
      return json(200, {
        metadata: {
          pagination: { totalCount: all.length, pageSize: all.length, totalPages: 1, currentPage: 0 },
          status: [],
          datafiles: [],
        },
        result: { data: all },
      });
    }

    if (method === "POST" && route === "/jobs") {
      const parsed = await readBody(req);
      if (!parsed.ok) return text(400, "malformed JSON request object");
      const body = parsed.value as Record<string, unknown>;
      const jobType = body.jobType as string;
      if (!SUPPORTED_JOB_TYPES.includes(jobType)) return text(400, `unknown jobType '${jobType}'`);
      const warnings: Array<Record<string, string>> = [];
      if (jobType === "inference") {
        const params = (body.parameters as Record<string, unknown>) ?? {};
        const model = resolveModel(params.modelDbId as string, params.modelVersion as string | undefined);
        if (!model) return text(400, `unknown model '${params.modelDbId}'`);
        if (model.status === "revoked") return text(400, `model '${model.modelDbId}' is revoked`);
        if (model.status === "deprecated") {
          warnings.push({ message: `model '${model.modelDbId}' is deprecated`, messageType: "WARNING" });
        }
      }
      const key = req.headers.get("idempotency-key") ?? (body.idempotencyKey as string | undefined);
      const canon = canonical(body);
      const seen = key ? idempotency.get(key) : undefined;
      if (seen) {
        if (seen.body === canon) {
          const existing = jobs.get(seen.jobDbId);
          return json(200, {
            metadata: { pagination: {}, status: [{ message: "Replayed existing job", messageType: "INFO" }], datafiles: [] },
            result: existing,
          });
        }
        return text(409, "idempotency key already used with a different body");
      }
      jobCounter += 1;
      const now = utcnow();
      const job: Job = {
        jobDbId: `JOB_${String(jobCounter).padStart(4, "0")}`,
        jobType,
        status: "SUBMITTED",
        createdAt: now,
        updatedAt: now,
        expiresAt: new Date(Date.now() + 7 * 86400000).toISOString().replace(/\.\d+Z$/, "Z"),
        ...(key ? { idempotencyKey: key } : {}),
      };
      jobs.set(job.jobDbId, job);
      if (key) idempotency.set(key, { body: canon, jobDbId: job.jobDbId });
      runJob(job.jobDbId, jobType, (body.parameters as Record<string, unknown>) ?? {});
      return json(202, {
        metadata: {
          pagination: {},
          status: [{ message: "Job accepted", messageType: "INFO" }, ...warnings],
          datafiles: [],
        },
        result: job,
      });
    }

    if (route.startsWith("/jobs/")) {
      const id = route.split("/jobs/")[1].split("/")[0];
      if (method === "GET") {
        const job = jobs.get(id);
        if (!job) return text(404, `unknown job '${id}'`);
        if (job.status === "EXPIRED") {
          const { result: _omit, ...slim } = job;
          void _omit;
          return json(200, { metadata: { pagination: {}, status: [], datafiles: [] }, result: slim });
        }
        return json(200, { metadata: { pagination: {}, status: [], datafiles: [] }, result: job });
      }
      if (method === "DELETE") {
        const job = jobs.get(id);
        if (!job) return text(404, `unknown job '${id}'`);
        if (TERMINAL.has(job.status)) return text(400, `job ${job.jobDbId} is terminal (${job.status})`);
        job.status = "CANCELLED";
        job.updatedAt = utcnow();
        return json(200, { metadata: { pagination: {}, status: [], datafiles: [] }, result: job });
      }
    }

    if (method === "POST" && route === "/models") {
      const parsed = await readBody(req);
      if (!parsed.ok) return text(400, "malformed JSON request object");
      const body = parsed.value as Record<string, unknown>;
      const mid = (body.modelDbId as string) ?? "";
      const version = (body.modelVersion as string) ?? "";
      if (!MODEL_ID_RE.test(mid)) return text(400, `modelDbId '${mid}' is not namespaced`);
      if (!version) return text(400, "missing model version");
      if (!DIGEST_RE.test((body.artifactDigest as string) ?? "")) {
        return text(400, "artifactDigest must be SHA-256 hex");
      }
      const artifact = { status: "active", ...body };
      if (!["active", "deprecated", "revoked"].includes(artifact.status as string)) {
        return text(400, `unknown status '${artifact.status}'`);
      }
      const mapKey = `${mid} ${version}`;
      const existing = models.get(mapKey);
      if (existing) {
        if (canonical(existing) === canonical(artifact)) {
          return json(200, {
            metadata: { pagination: {}, status: [{ message: "Replayed existing model version", messageType: "INFO" }], datafiles: [] },
            result: existing,
          });
        }
        return text(409, `model ${mid} version ${version} already registered with a different body`);
      }
      models.set(mapKey, artifact as Record<string, unknown>);
      modelOrder.push([mid, version]);
      return json(200, {
        metadata: { pagination: {}, status: [{ message: "Model version registered", messageType: "INFO" }], datafiles: [] },
        result: artifact,
      });
    }

    if (method === "GET" && route === "/models") {
      let list = modelOrder.map(([m, v]) => models.get(`${m} ${v}`));
      const statusFilter = url.searchParams.get("status");
      const idFilter = url.searchParams.get("modelDbId");
      if (statusFilter) list = list.filter((m) => m?.status === statusFilter);
      if (idFilter) list = list.filter((m) => m?.modelDbId === idFilter);
      return json(200, {
        metadata: {
          pagination: { totalCount: list.length, pageSize: list.length, totalPages: 1, currentPage: 0 },
          status: [],
          datafiles: [],
        },
        result: { data: list },
      });
    }

    if (method === "GET" && route.startsWith("/models/")) {
      const mid = route.split("/models/")[1].split("/")[0];
      const version = url.searchParams.get("version") ?? undefined;
      const artifact = resolveModel(mid, version);
      if (!artifact) return text(404, `unknown model '${mid}'`);
      return json(200, { metadata: { pagination: {}, status: [], datafiles: [] }, result: artifact });
    }

    return text(404, `unknown path ${url.pathname}`);
  },
});

console.log(`GenX test server (TS) on 127.0.0.1:${PORT} profile=${PROFILE}`);
