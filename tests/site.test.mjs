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
  const diagrams = ["intent-to-evidence", "service-factory", "generic-agent-runtime", "platform-planes", "capability-lifecycle", "governed-run", "scale-path"];
  for (const name of diagrams) {
    for (const extension of ["html", "svg", "gif"]) {
      await access(join(root, "diagrams", `${name}.${extension}`));
    }
  }
  await access(join(root, "diagrams", "contextweaver-public-architecture.drawio"));
  for (const extension of ["html", "svg", "png", "gif", "drawio"]) {
    await access(join(root, "diagrams", `contextweaver-spatial-architecture.${extension}`));
  }
  for (const image of [
    "intent-to-evidence.png",
    "layered-governed-architecture.png",
    "governed-platform-city.png",
    "governed-call-flow.png",
    "governed-sequence-ladder.png",
    "durable-saga-flow.png",
  ]) {
    await access(join(root, "assets", "media", "spatial", image));
  }
});

test("architecture players preserve approved static masters with semantic overlays", async () => {
  const expected = {
    "intent-to-evidence": ["Authenticated request", "Evidence", "edge-i12"],
    "service-factory": ["Product inputs", "Solution result + proof", "edge-f11"],
    "generic-agent-runtime": ["Generic runtime image", "Publisher MCP", "edge-g11"],
    "platform-planes": ["Eight Platform Planes", "Cerebro", "Loom"],
    "capability-lifecycle": ["Release Registry", "Operate and improve", "edge-c11"],
    "governed-run": ["Enterprise Input", "Workflow", "edge-r14"],
    "scale-path": ["Individual", "Sovereign / regulated", "Outcome"],
  };
  for (const [name, markers] of Object.entries(expected)) {
    const html = await readFile(join(root, "diagrams", `${name}.html`), "utf8");
    assert.match(html, /id="audio"[^>]*aria-pressed="false"/);
    assert.match(html, /id="popout"[^>]*>Pop out ↗<\/button>/);
    assert.match(html, /url\.searchParams\.set\("popout","1"\)/);
    assert.match(html, /e\.key==="Escape"&&isPopout/);
    assert.match(html, /Back · Esc/);
    assert.match(html, /SpeechSynthesisUtterance/);
    assert.match(html, /viewBox="0 0 1536 1024"/);
    assert.match(html, new RegExp(`class="architecture diagram-${name} image-first-diagram"`));
    assert.match(html, /href="data:image\/png;base64,/);
    assert.match(html, /The approved static composition remains unchanged/);
    assert.match(html, /class="image-overlay-edges"/);
    assert.match(html, /class="image-overlay-hotspots"/);
    assert.match(html, /class="node image-hotspot [^"]+"/);
    assert.match(html, /class="edge image-overlay-edge [^"]+"/);
    assert.match(html, /\.image-hotspot\.active \.hotspot-ring/);
    assert.doesNotMatch(html, /edge-label/);
    for (const marker of markers) assert.match(html, new RegExp(marker.replace(/[+]/g, "\\+")));
  }
});

test("nextgen atlas uses rounded 3d trays and a grouped Studio module", async () => {
  const html = await readFile(join(root, "diagrams", "contextweaver-nextgen-architecture.html"), "utf8");
  const svg = await readFile(join(root, "diagrams", "contextweaver-nextgen-architecture.svg"), "utf8");

  for (const output of [html, svg]) {
    assert.match(output, /class="zone-depth"/);
    assert.match(output, /class="node-side"/);
    assert.match(output, /class="[^"]*\bstudio-module\b[^"]*"/);
    assert.match(output, /class="studio-backplate"/);
    assert.match(output, /class="studio-tray-depth"/);
    assert.match(output, />STUDIO<\/text>/);
    for (const context of ["MCP", "AGENT", "FLOW", "SERVICE", "SOLUTION"]) {
      assert.match(output, new RegExp(`>${context}<\\/text>`));
    }
    assert.doesNotMatch(output, /class="node-echo/);
  }
});

test("repository publishing metadata is explicit", async () => {
  const readme = await readFile(join(root, "README.md"), "utf8");
  assert.match(readme, /brainzbytes\/contextweaver-public-site/);
});

test("spatial diagrams preserve the complete source image", async () => {
  const css = await readFile(join(root, "assets", "css", "site.css"), "utf8");
  assert.match(css, /\.spatial-visual-stage\s*\{[^}]*aspect-ratio:\s*3\s*\/\s*2/s);
  assert.match(css, /\.spatial-visual img\s*\{[^}]*object-fit:\s*contain/s);
  assert.doesNotMatch(css, /\.hero\s*>\s*\.spatial-visual\s+\.spatial-visual-stage\s*\{[^}]*aspect-ratio:\s*1\.14\s*\/\s*1/s);
});

test("spatial architecture uses compact, stage-specific emphasis", async () => {
  const html = await readFile(join(root, "diagrams", "contextweaver-spatial-architecture.html"), "utf8");
  const css = await readFile(join(root, "assets", "css", "site.css"), "utf8");
  assert.match(html, /class="core" id="core"/);
  assert.match(html, /classList\.toggle\("active",step\.core===true\)/);
  assert.match(html, /\.core\{[^}]*visibility:hidden[^}]*opacity:0/s);
  assert.match(html, /\.core\.active\{[^}]*visibility:visible/s);
  assert.match(html, /"core": true/);
  assert.match(html, /"core": false/);
  assert.match(css, /\.architecture-atlas-shell\s*\{[^}]*max-width:\s*1360px/s);
  assert.match(css, /\.architecture-spatial-frame\s*\{[^}]*min-height:\s*720px/s);
});

test("product hierarchy and consumer journey remain explicit", async () => {
  const landing = await readFile(join(root, "index.html"), "utf8");
  const siteJs = await readFile(join(root, "assets", "js", "site.js"), "utf8");
  const siteCss = await readFile(join(root, "assets", "css", "site.css"), "utf8");
  const overview = await readFile(join(root, "overview.html"), "utf8");
  const studio = await readFile(join(root, "studio.html"), "utf8");
  const runtime = await readFile(join(root, "runtime.html"), "utf8");
  const solutions = await readFile(join(root, "solutions.html"), "utf8");
  const architecture = await readFile(join(root, "architecture.html"), "utf8");
  const story = await readFile(join(root, "diagrams", "intent-to-evidence.html"), "utf8");
  const companyIntro = await readFile(join(root, "assets", "brand", "brainzbytes-contextweaver-overview.html"), "utf8");

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
  for (const runDetail of [
    "Run history and evidence",
    "Journey timeline",
    "Run Explorer",
    "Investigate regression",
    "Accepted output",
    "Dry-run comparison",
    "tool and policy receipts",
    "Evidence bundle",
  ]) {
    assert.match(runtime, new RegExp(runDetail, "i"));
  }
  assert.match(solutions, /Service is the reusable executable contract\. Solution is the complete user experience\./);
  for (const example of [
    "Business travel Solution",
    "Employee onboarding Solution",
    "Customer incident recovery Solution",
    "Insurance claim Solution",
    "Software release Solution",
  ]) {
    assert.match(solutions, new RegExp(example));
  }
  for (const relationship of [
    "One Solution can compose many Services",
    "One Service can support many Solutions",
    "One Service can select one or more approved Workflows",
    "One typed Workflow can support multiple Services",
  ]) {
    assert.match(solutions, new RegExp(relationship));
  }
  assert.match(solutions, /\/my-solutions/);
  assert.match(solutions, /delegated/i);
  assert.match(solutions, /Open run-history deep dive/);
  assert.match(solutions, /Open creation and dry runs/);
  assert.match(architecture, /five Studio contexts/);
  for (const spatialView of [
    "intent-to-evidence.png",
    "layered-governed-architecture.png",
    "governed-platform-city.png",
    "contextweaver-spatial-architecture.html",
  ]) {
    assert.match(architecture, new RegExp(spatialView.replace(/[.]/g, "\\.")));
  }
  assert.doesNotMatch(architecture, /architecture-block-view/);
  assert.match(story, /user-facing Solution/);
  assert.match(landing, /data-site-intro/);
  assert.match(landing, /data-src="assets\/brand\/brainzbytes-contextweaver-overview\.html\?embedded=1&amp;intro=1"/);
  assert.match(landing, /data-intro-skip/);
  assert.match(landing, /data-intro-enter/);
  assert.match(landing, /data-intro-replay/);
  assert.match(landing, /assets\/brand\/brainzbytes-b4\.svg/);
  assert.match(landing, /assets\/brand\/contextweaver-c1\.svg/);
  assert.match(landing, /sandbox="allow-scripts allow-same-origin"/);
  assert.match(landing, /assets\/css\/site\.css\?v=20261101-21/);
  assert.match(landing, /assets\/js\/site\.js\?v=20261101-18/);
  assert.match(siteJs, /contextweaver-company-intro-seen/);
  assert.match(siteJs, /brainzbytes-intro-complete/);
  assert.match(siteJs, /event\.key === "Escape"/);
  assert.match(siteJs, /prefers-reduced-motion: reduce/);
  assert.match(siteCss, /\.site-intro\[hidden\]\s*\{\s*display:\s*none;\s*\}/);
  assert.match(companyIntro, /Enable jazz \+ female narration/);
  assert.match(companyIntro, /beginAudio\(\);\s*<\/script>/);
  assert.match(companyIntro, /const introMode=params\.get\("intro"\)==="1"/);
  assert.match(companyIntro, /brainzbytes-intro-complete/);
  assert.match(companyIntro, /class="logo-portal"/);
  assert.match(companyIntro, /class="logo-plate"/);
  assert.match(companyIntro, /Microsoft Ava/);
  assert.match(companyIntro, /utterance\.onend=.*advance/s);
  assert.doesNotMatch(companyIntro, /setTimeout\([^)]*7600/);
  const introMarkup = landing.match(/<section class="site-intro"[\s\S]*?<\/section>/)?.[0] ?? "";
  assert.doesNotMatch(introMarkup, /site-intro__header/);
  assert.doesNotMatch(introMarkup, /brand-lockup/);
  assert.doesNotMatch(landing, /contextweaver-ai-factory\.(?:gif|png)/);

  const combined = [overview, studio, runtime, solutions, architecture, story].join("\n");
  for (const stale of [
    "working Service",
    "Four creation Studios",
    "ContextWeaver Studios",
    "Agent Studio",
    "MCP Studio",
    "Service Studio",
    "Workflow Studio",
    "Solution Studio",
    "Workspaces and Studios",
    "User-facing governed outcomes",
    "one useful Service",
    "Generated production service",
  ]) {
    assert.doesNotMatch(combined, new RegExp(stale), `stale product meaning remains: ${stale}`);
  }
});
