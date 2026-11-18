#!/usr/bin/env bun
import { jcsCanonicalize } from "./jcs.ts";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";

const corpusPath = new URL("../../Specification/BrAPI-GenX/Conformance/digest-vectors.json", import.meta.url);
const corpus = JSON.parse(readFileSync(corpusPath, "utf8")) as any;

const failures: string[] = [];
let structuredCount = 0;
let rejectionCount = 0;

for (const v of corpus.structuredJsonVectors) {
  try {
    const canonical = jcsCanonicalize(new TextEncoder().encode(v.inputJson));
    const canonicalText = new TextDecoder().decode(canonical);
    if (canonicalText !== v.expectedCanonicalUtf8) {
      failures.push(v.id + ": canonical mismatch: got " + JSON.stringify(canonicalText));
    }
    const sha = createHash("sha256").update(canonical).digest("hex");
    if (sha !== v.expectedSha256) {
      failures.push(v.id + ": sha256 mismatch: got " + sha);
    }
    structuredCount++;
  } catch (e) {
    failures.push(v.id + ": unexpected error: " + String(e));
  }
}

for (const v of corpus.rejectionVectors) {
  try {
    jcsCanonicalize(new TextEncoder().encode(v.inputJson));
    failures.push(v.id + ": expected rejection but accepted");
  } catch (e) {
    rejectionCount++;
  }
}

function expectThrow(fn: () => void, label: string): void {
  try { fn(); failures.push(label + ": expected throw"); }
  catch { /* ok */ }
}
expectThrow(() => jcsCanonicalize(new TextEncoder().encode('{"a":1,"a":2}')), "dup-top");
expectThrow(() => jcsCanonicalize(new TextEncoder().encode('{"o":{"a":1,"a":2}}')), "dup-nested");
expectThrow(() => jcsCanonicalize(new TextEncoder().encode('{"v":9007199254740992}')), "unsafe-int");
expectThrow(() => jcsCanonicalize(new TextEncoder().encode('{"v":"\\ud800"}')), "lone-surrogate");
expectThrow(() => jcsCanonicalize(new TextEncoder().encode('{"v":NaN}')), "nan");
expectThrow(() => jcsCanonicalize(new Uint8Array([0xff, 0xfe])), "bad-utf8");

console.log("dup-unmask check:", new TextDecoder().decode(jcsCanonicalize(new TextEncoder().encode('{"a":1,"a\\u0061":2}'))));

if (failures.length) {
  console.error("FAIL jcs ts");
  failures.forEach((f) => console.error(" - " + f));
  process.exit(1);
}
console.log("PASS jcs ts: " + structuredCount + " structured, " + rejectionCount + " rejection");
