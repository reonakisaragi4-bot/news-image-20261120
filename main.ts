// news-image-20261120 — one-image summary of Friday 20 November 2026
// world news. The poster is the entry.png beside this file; the program
// copies it to the grader's output directory. Node 22, stdlib only.
//
// The poster path is built from this file's own location, not from the
// working directory, because the grader runs `node /bot/main.ts` from an
// arbitrary cwd — a bare relative "entry.png" would fail there.
//
// Usage:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const source = join(here, 'entry.png');
const target = join(outDir, 'entry.png');

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

// The gate rejects a truncated image, so confirm the whole file landed.
const written = statSync(target).size;
const expected = statSync(source).size;
if (written !== expected) {
  throw new Error(`entry.png copy mismatch: ${written} != ${expected}`);
}
console.log(`wrote ${target} (${written} bytes)`);
