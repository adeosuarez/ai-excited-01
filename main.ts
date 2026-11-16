// make.fun entry: ai-excited-01
// Copies pre-made entry.png into the output directory (default /output).
// Deterministic, stdlib only, no network.

const fs = require("fs");
const path = require("path");

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";

fs.mkdirSync(outDir, { recursive: true });

const src = path.join(__dirname, "entry.png");

// Basic sanity checks before shipping the copy.
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

if (!fs.existsSync(src)) {
  throw new Error(`missing source image: ${src}`);
}

const data = fs.readFileSync(src);
if (data.length === 0) {
  throw new Error("entry.png is empty (0 bytes)");
}
if (data.length <= 8) {
  throw new Error("entry.png too short to be a PNG");
}
if (data.length > 1024 * 1024) {
  throw new Error(`entry.png exceeds 1 MiB limit (${data.length} bytes)`);
}
if (!data.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error("entry.png is not a valid PNG (bad signature)");
}

const dest = path.join(outDir, "entry.png");
fs.copyFileSync(src, dest);

console.log(`copied ${src} -> ${dest}`);
