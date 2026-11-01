import test from "node:test";
import assert from "node:assert/strict";
import { readFile, readdir, access } from "node:fs/promises";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const pages = [
  "index.html",
  "platform.html",
  "studio.html",
  "runtime.html",
  "governance.html",
  "solutions.html",
  "architecture.html",
];

test("all public pages have required structure and accessible images", async () => {
  for (const page of pages) {
    const html = await readFile(join(root, page), "utf8");
    assert.match(html, /<!doctype html>/i, `${page} is missing a doctype`);
    assert.match(html, /<title>[^<]+<\/title>/i, `${page} is missing a title`);
    assert.match(html, /<meta name="description"/i, `${page} is missing a description`);
    assert.match(html, /<main id="main-content"/i, `${page} is missing the main landmark`);
    assert.match(html, /assets\/css\/site\.css/, `${page} does not load shared CSS`);
    assert.match(html, /assets\/js\/site\.js/, `${page} does not load shared JavaScript`);
    for (const match of html.matchAll(/<img\b([^>]+)>/gi)) {
      assert.match(match[1], /\balt="[^"]*"/i, `${page} has an image without alt text`);
    }
  }
});

test("local links and embedded assets resolve", async () => {
  const files = [...pages];
  const diagramFiles = (await readdir(join(root, "diagrams")))
    .filter((name) => name.endsWith(".html"))
    .map((name) => join("diagrams", name));
  files.push(...diagramFiles);

  for (const source of files) {
    const html = await readFile(join(root, source), "utf8");
    const refs = [
      ...html.matchAll(/\b(?:href|src)="([^"]+)"/gi),
    ].map((match) => match[1])
      .filter((ref) => !ref.startsWith("#") && !ref.startsWith("http") && !ref.startsWith("mailto:") && !ref.startsWith("data:"));
    for (const ref of refs) {
      const clean = ref.split("#")[0].split("?")[0];
      if (!clean) continue;
      await access(join(root, dirname(source), clean));
    }
  }
});

test("diagram deliverables are complete", async () => {
  const diagrams = ["service-factory", "platform-planes", "capability-lifecycle", "governed-run", "scale-path"];
  for (const name of diagrams) {
    for (const extension of ["html", "svg", "gif"]) {
      await access(join(root, "diagrams", `${name}.${extension}`));
    }
  }
  await access(join(root, "diagrams", "contextweaver-public-architecture.drawio"));
});

test("repository publishing metadata is explicit", async () => {
  const readme = await readFile(join(root, "README.md"), "utf8");
  assert.match(readme, /brainzbytes\/contextweaver-public-site/);
});

test("product hierarchy and consumer journey remain explicit", async () => {
  const overview = await readFile(join(root, "overview.html"), "utf8");
  const studio = await readFile(join(root, "studio.html"), "utf8");
  const runtime = await readFile(join(root, "runtime.html"), "utf8");
  const solutions = await readFile(join(root, "solutions.html"), "utf8");
  const architecture = await readFile(join(root, "architecture.html"), "utf8");
  const story = await readFile(join(root, "experiences", "contextweaver-ai-factory-3d.html"), "utf8");

  assert.match(overview, /working Solution/);
  for (const concept of [
    "MCP capability",
    "bounded reasoning specialist",
    "durable coordination graph",
    "reusable executable contract",
    "final user-facing composition",
  ]) {
    assert.match(studio, new RegExp(concept));
  }
  assert.match(runtime, /Service Experience Contract/);
  assert.match(runtime, /Service Run/);
  assert.match(solutions, /Service is the reusable executable contract\. Solution is the complete user experience\./);
  assert.match(solutions, /\/my-solutions/);
  assert.match(solutions, /delegated/i);
  assert.match(architecture, /five Studio contexts/);
  assert.match(story, /Published user-facing Solution/);

  const combined = [overview, studio, runtime, solutions, architecture, story].join("\n");
  for (const stale of [
    "working Service",
    "Four creation Studios",
    "User-facing governed outcomes",
    "one useful Service",
    "Generated production service",
  ]) {
    assert.doesNotMatch(combined, new RegExp(stale), `stale product meaning remains: ${stale}`);
  }
});
