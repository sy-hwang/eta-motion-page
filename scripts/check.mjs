// Check deployable files, local resources and anchor targets without dependencies.
import { readFile, stat, readdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../site/", import.meta.url));
const html = await readFile(path.join(root, "index.html"), "utf8");
const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]);
const errors = [];
if (new Set(ids).size !== ids.length) errors.push("Duplicate HTML ids");
for (const [, value] of html.matchAll(/\b(?:src|href|poster)="([^"]+)"/g)) {
  if (value.startsWith("#")) {
    if (value.length > 1 && !ids.includes(value.slice(1))) errors.push(`Missing anchor: ${value}`);
  } else if (!/^[a-z][a-z\d+.-]*:/i.test(value)) {
    try { await stat(path.join(root, value)); } catch { errors.push(`Missing local resource: ${value}`); }
  }
}
for (const [, attributes] of html.matchAll(/<img\b([^>]+)>/g)) if (!/\balt="/.test(attributes)) errors.push("Image missing alt text");
let total = 0;
async function checkFiles(directory) {
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const filename = path.join(directory, entry.name);
    if (entry.isDirectory()) await checkFiles(filename);
    else {
      const info = await stat(filename);
      total += info.size;
      if (info.size > 100 * 1024 * 1024) errors.push(`File exceeds 100 MiB: ${filename}`);
    }
  }
}
await checkFiles(root);
if (errors.length) { console.error(errors.join("\n")); process.exitCode = 1; }
else console.log(`OK: local assets, anchors, unique IDs, image descriptions, file sizes. Site size: ${(total / 1024 / 1024).toFixed(2)} MiB.`);
