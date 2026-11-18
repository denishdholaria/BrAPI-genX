#!/usr/bin/env bun
import { jcsCanonicalize, JCSError, DuplicatePropertyError, NonFiniteNumberError, LoneSurrogateError, UnsafeIntegerError } from "./jcs.ts";
import { createHash } from "node:crypto";

const rawMode = Bun.argv.includes("--raw");

const chunks: Uint8Array[] = [];
for await (const chunk of Bun.stdin.stream()) chunks.push(chunk);
const input = new Uint8Array(chunks.reduce((n, c) => n + c.length, 0));
let off = 0;
for (const c of chunks) { input.set(c, off); off += c.length; }

try {
  if (rawMode) {
    const sha = createHash("sha256").update(input).digest("hex");
    process.stdout.write(JSON.stringify({ ok: true, sha256: sha }) + "\n");
    process.exit(0);
  }
  const canonical = jcsCanonicalize(input);
  const sha = createHash("sha256").update(canonical).digest("hex");
  const out = {
    ok: true,
    canonicalBase64: Buffer.from(canonical).toString("base64"),
    canonicalUtf8: new TextDecoder().decode(canonical),
    sha256: sha,
  };
  process.stdout.write(JSON.stringify(out) + "\n");
} catch (e) {
  const err = e as Error;
  let category = "invalid-input";
  if (e instanceof DuplicatePropertyError) category = "duplicate-property";
  else if (e instanceof NonFiniteNumberError) category = "non-finite";
  else if (e instanceof LoneSurrogateError) category = "lone-surrogate";
  else if (e instanceof UnsafeIntegerError) category = "unsafe-integer";
  else if (e instanceof JCSError) category = "jcs-error";
  process.stdout.write(JSON.stringify({ ok: false, error: err.message, category }) + "\n");
  process.exit(1);
}
