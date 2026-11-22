// Ghost Catcher — entry program for the make.fun bounty
// "The agent builds a game from one prompt" (Node 22, standard library only).
//
// The entry itself is the X post: the house reads the post (its video, then
// its text) straight from X and scores it on views + 10x interactions.
// This program does one small job: it hands POST.json, which holds the
// post's address, over to the output folder so the gate can find it.
//
// Before copying, it checks that POST.json actually holds a real X post URL
// and that the file is small enough for the gate (at most 16384 bytes).
// A placeholder ("TO_BE_POSTED") or a link to somewhere that is not an X
// post would make the entry unreadable to the grader, so the program
// refuses to copy those and exits with a clear error instead of silently
// handing in a dead link.
//
// Run it locally the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import {
  copyFileSync,
  existsSync,
  mkdirSync,
  readFileSync,
  statSync,
} from "node:fs";
import { join } from "node:path";

const repoDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const source = join(repoDir, "POST.json");
const target = join(outputDir, "POST.json");

// A real X post URL looks like https://x.com/<user>/status/<digits>.
// Anything else — a placeholder, a link to another site, a malformed
// address — cannot be graded, so it is rejected here.
const X_POST_URL = /^https:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/[A-Za-z0-9_]+\/status\/\d+$/;
const MAX_POST_BYTES = 16384;

function fail(message: string): never {
  console.error(`POST.json validation failed: ${message}`);
  process.exit(1);
}

if (!existsSync(source)) {
  fail(`no POST.json found in ${repoDir}`);
}

const size = statSync(source).size;
if (size > MAX_POST_BYTES) {
  fail(`POST.json is ${size} bytes, over the ${MAX_POST_BYTES} byte cap`);
}

let parsed: unknown;
try {
  parsed = JSON.parse(readFileSync(source, "utf8"));
} catch (err) {
  fail(`POST.json is not valid JSON: ${(err as Error).message}`);
}

if (typeof parsed !== "object" || parsed === null || Array.isArray(parsed)) {
  fail("POST.json must be a JSON object with a url field");
}
const url = (parsed as Record<string, unknown>).url;
if (typeof url !== "string" || !X_POST_URL.test(url)) {
  fail(`url is not an X post address: ${JSON.stringify(url)}`);
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(source, target);
console.log(`POST.json copied to ${target}: ${url}`);
