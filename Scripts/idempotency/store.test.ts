import { test, expect, beforeAll, afterEach } from "bun:test";
import { PostgresIdempotencyStore } from "./store";

const DSN = process.env.GENX_IDEMPOTENCY_DSN || "postgresql://postgres:postgres@localhost/brapi_genx_idempotency";

function uuid(): string {
  return crypto.randomUUID();
}

function ident() {
  return {
    tenantId: uuid(),
    clientId: uuid(),
    principalId: uuid(),
    operationId: "genxSubmitAsyncJob",
    idempotencyKey: "key-" + uuid(),
  };
}

let store: PostgresIdempotencyStore;
beforeAll(async () => {
  store = new PostgresIdempotencyStore(DSN, 7 * 86400000, 30 * 86400000, 2);
  await store.migrate();
  await store.purge();
});

test("new claim and complete", async () => {
  const i = ident();
  const { disposition } = await store.claim(i, "fp1");
  expect(disposition).toBe("acquired");
  await store.complete(i, "fp1", 202, { jobDbId: "JOB_0001" });
  const rec = await store.get(i);
  expect(rec?.status).toBe("completed");
  expect(rec?.responseBody).toEqual({ jobDbId: "JOB_0001" });
});

test("replay same fingerprint", async () => {
  const i = ident();
  await store.claim(i, "fp1");
  await store.complete(i, "fp1", 200, { ok: true });
  const { disposition } = await store.claim(i, "fp1");
  expect(disposition).toBe("replay");
});

test("conflict different fingerprint", async () => {
  const i = ident();
  await store.claim(i, "fp1");
  await store.complete(i, "fp1", 200, { ok: true });
  const { disposition } = await store.claim(i, "fp2");
  expect(disposition).toBe("conflict");
});

test("concurrent reservation only one acquired", async () => {
  const i = ident();
  const barrier = { n: 0 };
  const run = async () => {
    const r = await store.claim(i, "fp1");
    return r.disposition;
  };
  const [a, b] = await Promise.all([run(), run()]);
  const sorted = [a, b].sort();
  expect(sorted).toEqual(["acquired", "in_progress"]);
});

test("lease expiry recovery", async () => {
  const i = ident();
  const r1 = await store.claim(i, "fp1", "jcs-rfc8785:v1", "procA");
  expect(r1.disposition).toBe("acquired");
  await new Promise((res) => setTimeout(res, 2500));
  const r2 = await store.claim(i, "fp1", "jcs-rfc8785:v1", "procB");
  expect(r2.disposition).toBe("acquired");
  expect(r2.record.leaseOwner).toBe("procB");
});

test("tenant isolation", async () => {
  const i = ident();
  await store.claim(i, "fp1");
  await store.complete(i, "fp1", 200, { secret: "A" });
  const i2 = { ...i, tenantId: uuid() };
  const { disposition } = await store.claim(i2, "fp1");
  expect(disposition).toBe("acquired");
});

test("failure semantics retryable", async () => {
  const i = ident();
  await store.claim(i, "fp1");
  const r = await store.fail(i, true, "business", { msg: "boom" });
  expect(r.status).toBe("retryable_failure");
  const c = await store.claim(i, "fp1");
  expect(c.disposition).toBe("acquired");
});

test("fingerprint profile persisted", async () => {
  const i = ident();
  await store.claim(i, "fp1");
  await store.complete(i, "fp1", 200, { ok: true });
  const rec = await store.get(i);
  expect(rec?.canonicalizationProfile).toBe("jcs-rfc8785:v1");
  expect(rec?.fingerprintAlgorithm).toBe("sha256");
});
