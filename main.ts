// one-day-news-agent1 — make.fun news-image-20261121 (Agent 1 entry).
//
// The entry image is drawn by gen.py and stored next to this file as
// entry.png. This program only copies that image into the output
// directory the grader provides, so both runs write identical bytes.
//
// Usage (outside the grader): MAKEFUN_OUTPUT_DIR=out node main.ts
// The image is resolved from this file's own directory, never from the
// process working directory, so it works from any cwd. MAKEFUN_OUTPUT_DIR
// is used as-is: never joined onto the repository path.

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const source = new URL("./entry.png", import.meta.url);

mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, "entry.png"));
