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
    await access(join(root, "assets", "media", "spatial", image.replace(/\.png$/, ".svg")));
  }
  await access(join(root, "diagrams", "contextweaver-spatial-visuals.drawio"));
});

test("architecture players preserve approved image-first masters and semantic topology", async () => {
  const expected = {
    "intent-to-evidence": {
      nodes: ["intent", "solution", "service", "cerebro", "workflow", "agents", "mcp", "systems", "approval", "evidence", "outcome", "history"],
      edges: ["i1", "i2", "i3", "i4", "i5", "i6", "i7", "i8", "i9", "i10", "i11", "i12"],
    },
    "generic-agent-runtime": {
      nodes: ["registry", "compiler", "coordinator", "rabbit", "image", "risk", "readiness", "synthesis", "approval", "publisher"],
      edges: ["g1", "g2", "g3", "g4", "g5", "g6", "g6b", "g7", "g8", "g9", "g10", "g11"],
    },
    "platform-planes": {
      nodes: ["experience", "governance", "registry", "capabilities", "workflow", "knowledge", "evidence", "infrastructure", "cerebro", "weave", "loom"],
      edges: ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10", "p11", "p12", "p13", "p14", "p15"],
    },
    "capability-lifecycle": {
      nodes: ["author", "conformance", "supply", "approval", "registry", "operator", "runtime", "attest", "canary", "active", "operate"],
      edges: ["c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11"],
    },
    "governed-run": {
      nodes: ["enterprise", "workspace", "studio", "compiler", "identity", "policy", "workflow", "agents", "mcp", "orchestrator", "evidence", "outcome"],
      edges: ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10", "r11", "r12", "r13", "r14"],
    },
    "scale-path": {
      nodes: ["individual", "team", "business", "enterprise", "sovereign", "contracts", "profiles", "packs", "outcomes"],
      edges: ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"],
    },
    "service-factory": {
      nodes: ["inputs", "studio", "contracts", "admission", "registry", "operator", "discovery", "compose", "execute", "outcome"],
      edges: ["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11"],
    },
  };
  for (const [name, topology] of Object.entries(expected)) {
    const html = await readFile(join(root, "diagrams", `${name}.html`), "utf8");
    assert.match(html, /id="audio"[^>]*aria-pressed="false"/);
    assert.match(html, /id="popout"[^>]*>Pop out ↗<\/button>/);
    assert.match(html, /url\.searchParams\.set\("popout","1"\)/);
    assert.match(html, /e\.key==="Escape"&&isPopout/);
    assert.match(html, /Back · Esc/);
    assert.match(html, /SpeechSynthesisUtterance/);
    assert.match(html, /viewBox="0 0 1536 1024"/);
    assert.match(html, new RegExp(`<svg class="architecture diagram-${name} image-first-diagram"`));
    assert.match(html, /class="static-master" href="data:image\/png;base64,/);
    assert.match(html, /<g class="image-overlay-edges">/);
    assert.match(html, /<g class="image-overlay-hotspots">/);
    assert.match(html, /class="node image-hotspot node-[^"]+"/);
    assert.match(html, /class="edge image-overlay-edge edge-[^"]+"/);
    assert.match(html, /\.node\.active/);
    assert.match(html, /\.edge\.active/);
    assert.deepEqual([...html.matchAll(/data-node-id="([^"]+)"/g)].map((match) => match[1]), topology.nodes);
    assert.deepEqual([...html.matchAll(/data-edge-id="([^"]+)"/g)].map((match) => match[1]), topology.edges);
    const steps = JSON.parse(html.match(/const steps=(\[.*?\]);/s)[1]);
    for (const step of steps) {
      assert.ok(step.nodes.every((node) => topology.nodes.includes(node)), `${name} stage references an unknown node`);
      assert.ok(step.edges.every((edge) => topology.edges.includes(edge)), `${name} stage references an unknown edge`);
    }
  }
});

test("nextgen compatibility outputs use the rendered-glass atlas", async () => {
  const html = await readFile(join(root, "diagrams", "contextweaver-nextgen-architecture.html"), "utf8");
  const manifest = JSON.parse(await readFile(join(root, "diagrams", "contextweaver-nextgen-architecture", "manifest.json"), "utf8"));

  assert.match(html, /"OpenTelemetry Run Trace Explorer"/);
  assert.match(html, /"assetVersion"\s*:\s*"[a-f0-9]{12}"/);
  assert.doesNotMatch(html, /Editable \.drawio|Open current SVG|\.svg"/);
  assert.equal(manifest.pages.length, 19);
  for (const page of manifest.pages) {
    assert.match(page.file, /\.png$/);
    await access(join(root, "diagrams", "contextweaver-nextgen-architecture", page.file));
  }
  for (const extension of ["svg", "gif", "drawio"]) {
    await assert.rejects(access(join(root, "diagrams", `contextweaver-nextgen-architecture.${extension}`)));
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
  const company = await readFile(join(root, "company.html"), "utf8");
  const learning = await readFile(join(root, "learning.html"), "utf8");
  const libraryRedirect = await readFile(join(root, "library.html"), "utf8");
  const sitemap = await readFile(join(root, "sitemap.xml"), "utf8");
  const learningJs = await readFile(join(root, "learning.js"), "utf8");
  const learningCss = await readFile(join(root, "learning.css"), "utf8");
  const learningData = await readFile(join(root, "learning-data.js"), "utf8");
  const story = await readFile(join(root, "diagrams", "intent-to-evidence.html"), "utf8");
  const companyIntro = await readFile(join(root, "assets", "brand", "brainzbytes-contextweaver-overview.html"), "utf8");

  assert.match(overview, /working Solution/);
  for (const provider of ["Azure", "AWS", "Google Cloud"]) {
    assert.match(overview, new RegExp(provider));
    assert.match(story, new RegExp(provider));
  }
  assert.match(overview, /intent-to-evidence\.png\?v=20261103-2/);
  assert.match(architecture, /diagrams\/platform-planes\.html\?v=20261103-2/);
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
  for (const component of [
    "Experience",
    "Governance",
    "Registry",
    "Agents + MCP",
    "Workflow runtime",
    "RAG + memory + models",
    "Evidence",
    "Infrastructure",
    "Cerebro",
    "Weave",
    "Loom",
  ]) {
    assert.match(architecture, new RegExp(component.replace(/[+]/g, "\\+")));
  }
  assert.match(architecture, /assets\/media\/platform-planes-static-master\.png\?v=20261103-2/);
  assert.match(architecture, /diagrams\/platform-planes\.svg/);
  assert.doesNotMatch(architecture, /Universal Solution and Capability Factory/);
  assert.doesNotMatch(architecture, /assets\/media\/service-factory-static-master\.png/);
  assert.doesNotMatch(architecture, /diagrams\/service-factory\.html/);
  assert.doesNotMatch(architecture, /architecture-block-view/);
  assert.match(story, /user-facing Solution/);
  assert.match(landing, /data-site-intro/);
  assert.match(landing, /assets\/js\/site\.js\?v=20261102-4/);
  assert.match(landing, /data-src="assets\/brand\/brainzbytes-contextweaver-overview\.html\?embedded=1&amp;intro=1&amp;v=20261103-9"/);
  assert.match(landing, /data-intro-skip/);
  assert.match(landing, /data-intro-enter/);
  assert.match(landing, /data-intro-replay/);
  assert.match(landing, /assets\/brand\/brainzbytes-b4\.svg/);
  assert.match(landing, /assets\/brand\/contextweaver-c1\.svg/);
  assert.match(landing, /sandbox="allow-scripts allow-same-origin"/);
  assert.match(landing, /assets\/css\/site\.css\?v=20261102-4/);
  assert.doesNotMatch(landing, /assets\/js\/site\.js\?v=20261101-18/);
  assert.match(siteJs, /contextweaver-company-intro-seen/);
  assert.match(siteJs, /brainzbytes-intro-complete/);
  assert.match(siteJs, /event\.key === "Escape"/);
  assert.match(siteJs, /prefers-reduced-motion: reduce/);
  assert.match(siteCss, /\.site-intro\[hidden\]\s*\{\s*display:\s*none;\s*\}/);
  assert.match(companyIntro, /Start jazz \+ female narration/);
  assert.match(companyIntro, /showOpening\(\);\s*tryIntroMusic\(\);\s*<\/script>/);
  assert.match(companyIntro, /const introMode=params\.get\("intro"\)==="1"/);
  assert.match(companyIntro, /brainzbytes-intro-complete/);
  assert.match(companyIntro, /class="logo-portal"/);
  assert.match(companyIntro, /class="logo-plate"/);
  assert.match(companyIntro, /service-factory\.html\?portal=1&amp;v=20261103-9/);
  assert.match(companyIntro, /id="factoryPlane"/);
  assert.match(companyIntro, /contextweaver-factory-stage/);
  assert.match(companyIntro, /function showOpening\(\)[\s\S]*syncFactoryPlane\(0\)/);
  assert.doesNotMatch(companyIntro, /syncSpatialPlane/);
  assert.match(companyIntro, /narrationWatchdogDelay/);
  assert.match(companyIntro, /speechSynthesis\.resume\(\)/);
  assert.match(companyIntro, /englishVoices\.find\(voice=>voice\.default\)/);
  assert.match(companyIntro, /utterance\.lang=voice\?\.lang\|\|"en-US"/);
  assert.match(companyIntro, /const startGuard=setTimeout\(retry,1800\)/);
  assert.match(companyIntro, /setTimeout\(\(\)=>startUtterance\(\),120\)/);
  assert.match(companyIntro, /window\.unlockIntroAudio=\(\)=>beginAudio\(\)/);
  assert.match(companyIntro, /window\.isIntroAudioUnlocked=\(\)=>audioStarted/);
  assert.match(companyIntro, /function beginAudio\(\)[\s\S]*storyStarted=true[\s\S]*render\(true\)/);
  assert.match(companyIntro, /addEventListener\("pointerdown"[\s\S]*unlockFromGesture/);
  assert.match(companyIntro, /showOpening\(\);\s*tryIntroMusic\(\)/);
  assert.doesNotMatch(companyIntro, /showOpening\(\);\s*beginAudio\(\)/);
  assert.match(siteJs, /frameWindow\?\.unlockIntroAudio/);
  assert.match(siteJs, /document\.addEventListener\("pointerdown"[\s\S]*unlockIntroAudio/);
  assert.match(learning, /assets\/architecture\/contextweaver-intent-to-evidence\.png/);
  assert.match(learning, /class="atlas-hotspot[^"]*"[^>]*data-term="contextweaver"/);
  assert.match(learning, /id="glossary-grid"/);
  assert.match(learning, /id="lesson-dialog"/);
  assert.match(learning, /id="lesson-previous"/);
  assert.match(learning, /id="lesson-next"/);
  assert.match(learning, /Complete A–Z glossary/);
  assert.match(learning, /Latest capabilities connected to the master architecture/);
  assert.doesNotMatch(
    [landing, overview, studio, runtime, solutions, architecture, company, learning].join("\n"),
    /href="library\.html/,
  );
  assert.doesNotMatch(sitemap, /library\.html/);
  assert.match(libraryRedirect, /name="robots" content="noindex"/);
  assert.match(libraryRedirect, /url=learning\.html/);
  assert.match(learningJs, /window\.CW_LEARNING/);
  assert.match(learningJs, /localStorage\.setItem/);
  assert.match(learningJs, /history\.pushState/);
  assert.match(learningJs, /history\.replaceState/);
  assert.match(learningJs, /renderLessonNavigation/);
  assert.match(learningCss, /\.atlas-hotspot/);
  assert.match(learningCss, /\.lesson-dialog/);
  assert.match(learningCss, /\.glossary-grid/);
  assert.match(learningData, /Retrieval-Augmented Generation/);
  assert.match(learningData, /Agentic RAG/);
  assert.match(learningData, /Cross-Engine Dependency/);
  assert.match(learningData, /window\.CW_LEARNING/);
  assert.match(siteJs, /page === "architecture" && !location\.hash/);
  assert.match(siteJs, /history\.scrollRestoration = "manual"/);
  assert.doesNotMatch(companyIntro, /contextweaver-spatial-architecture\.html/);
  assert.match(architecture, /id="interactive-platform-architecture"/);
  assert.match(architecture, /platform-planes-static-master\.png\?v=20261103-2/);
  assert.match(architecture, /diagrams\/platform-planes\.html\?v=20261103-2/);
  assert.match(architecture, /id="technical-architecture-atlas"/);
  assert.match(architecture, /diagrams\/contextweaver-nextgen-atlas\.html\?embedded=1&amp;v=[a-f0-9]{12}/);
  assert.doesNotMatch(architecture, /contextweaver-nextgen-architecture\.(?:drawio|svg)/);
  assert.match(architecture, /diagrams\/intent-to-evidence-flow\.html\?embedded=1&amp;v=20261103-11/);
  assert.doesNotMatch(architecture, /experiences\/contextweaver-spatial-r3f/);
  assert.doesNotMatch(architecture, /id="high-level-views"/);
  const factory = await readFile(join(root, "diagrams", "service-factory.html"), "utf8");
  assert.match(factory, /body\.portal \.storybar,body\.portal \.detailbar\{display:none\}/);
  assert.match(factory, /const portalNodes=\["inputs","studio","contracts","admission","registry","operator","discovery","compose","execute","outcome"\]/);
  assert.match(factory, /contextweaver-factory-stage/);
  assert.match(factory, /event\.origin!==location\.origin/);
  assert.match(companyIntro, /Female narrator · \$\{preference\.label\}/);
  assert.match(companyIntro, /Microsoft Jenny[\s\S]*Microsoft Aria[\s\S]*Microsoft Ava/);
  assert.match(companyIntro, /await waitForNarrator\(\)/);
  assert.match(companyIntro, /"English narrator"[\s\S]*"Browser narrator"/);
  assert.doesNotMatch(companyIntro, /Female narrator unavailable/);
  assert.doesNotMatch(companyIntro, /voices\.find\(voice=>voice\.lang==="en-US"\)/);
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
