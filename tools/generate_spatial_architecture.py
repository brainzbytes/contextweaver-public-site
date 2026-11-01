from __future__ import annotations

import argparse
import json
from html import escape as html_escape
from pathlib import Path
from textwrap import wrap
from xml.sax.saxutils import escape as xml_escape

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "diagrams"
SLUG = "contextweaver-spatial-architecture"
GIF_FRAME_DURATION_MS = 1000

COLORS = {
    "bg": "#050b08",
    "panel": "#0a1812",
    "panel2": "#10261d",
    "panel3": "#173429",
    "text": "#f4f8f2",
    "muted": "#9db2a8",
    "line": "#315446",
    "mint": "#70e6b1",
    "amber": "#ffc76a",
    "red": "#ff756d",
}

NODES = {
    "channels": {"title": "Channels", "sub": "Portal · IDE · API · assistants", "x": 9, "y": 18},
    "solutions": {"title": "Solutions", "sub": "User-facing intent to outcome", "x": 31, "y": 14},
    "services": {"title": "Services", "sub": "Reusable executable contracts", "x": 50, "y": 14},
    "workflows": {"title": "Workflows", "sub": "Durable coordination graphs", "x": 69, "y": 14},
    "agents": {"title": "Agents", "sub": "Bounded reasoning specialists", "x": 82, "y": 36},
    "mcp": {"title": "MCP gateway", "sub": "Governed tools and resources", "x": 82, "y": 56},
    "foundation": {"title": "Knowledge + models", "sub": "Data · memory · enterprise systems", "x": 81, "y": 78},
    "intent": {"title": "Intent + identity", "sub": "Purpose · tenant · delegation", "x": 28, "y": 42},
    "policy": {"title": "Policy + compiler", "sub": "Authorize · resolve · freeze plan", "x": 50, "y": 42},
    "coordinator": {"title": "Run coordinator", "sub": "State · queues · retries · Saga", "x": 51, "y": 65},
    "evidence": {"title": "Evidence fabric", "sub": "Receipts · citations · traces", "x": 31, "y": 79},
    "external": {"title": "External systems", "sub": "SaaS · APIs · humans · data", "x": 9, "y": 68},
    "loom": {"title": "Loom foundation", "sub": "Kubernetes · state · events · secrets", "x": 52, "y": 88},
}

EDGES = [
    ("product-1", "channels", "solutions"),
    ("product-2", "solutions", "services"),
    ("product-3", "services", "workflows"),
    ("product-4", "workflows", "agents"),
    ("product-5", "workflows", "mcp"),
    ("product-6", "agents", "foundation"),
    ("product-7", "mcp", "foundation"),
    ("govern-1", "channels", "intent"),
    ("govern-2", "intent", "policy"),
    ("govern-3", "policy", "coordinator"),
    ("run-1", "coordinator", "workflows"),
    ("run-2", "agents", "mcp"),
    ("run-3", "mcp", "external"),
    ("evidence-1", "external", "evidence"),
    ("evidence-2", "coordinator", "evidence"),
    ("evidence-3", "evidence", "solutions"),
    ("deploy-1", "policy", "loom"),
    ("deploy-2", "loom", "coordinator"),
    ("deploy-3", "loom", "foundation"),
]

STEPS = [
    {
        "lens": "product",
        "title": "Enter through an entitled channel",
        "caption": "People and delegated clients begin with a governed Solution action rather than infrastructure access.",
        "nodes": ["channels", "solutions"],
        "edges": ["product-1"],
        "core": False,
    },
    {
        "lens": "product",
        "title": "Compose outcomes from reusable layers",
        "caption": "Solutions compose Services; Services select approved Workflows; Workflows coordinate Agents and MCP capabilities.",
        "nodes": ["solutions", "services", "workflows", "agents", "mcp", "foundation"],
        "edges": ["product-2", "product-3", "product-4", "product-5", "product-6", "product-7"],
        "core": False,
    },
    {
        "lens": "execution",
        "title": "Bind identity, purpose, and policy",
        "caption": "Cerebro narrows the eligible universe using tenant, user, purpose, delegation, policy, lifecycle, and approval.",
        "nodes": ["channels", "intent", "policy"],
        "edges": ["govern-1", "govern-2"],
        "core": True,
    },
    {
        "lens": "execution",
        "title": "Freeze and execute a durable plan",
        "caption": "The compiler pins exact versions and the coordinator persists state, dispatches typed work, retries, waits, and compensates.",
        "nodes": ["policy", "coordinator", "workflows", "agents", "mcp"],
        "edges": ["govern-3", "run-1", "run-2"],
        "core": True,
    },
    {
        "lens": "platform",
        "title": "Cerebro governs the complete lifecycle",
        "caption": "Intent, identity, policy, registry, compilation, orchestration, operations, and evidence remain explicit control-plane responsibilities.",
        "nodes": ["intent", "policy", "coordinator", "evidence"],
        "edges": ["govern-2", "govern-3", "evidence-2"],
        "core": True,
    },
    {
        "lens": "platform",
        "title": "Weave exposes governed capability fabric",
        "caption": "Solutions, Services, Workflows, Agents, MCP capabilities, knowledge, models, and adapters remain reusable and independently governed.",
        "nodes": ["solutions", "services", "workflows", "agents", "mcp", "foundation"],
        "edges": ["product-2", "product-3", "product-4", "product-5", "product-6", "product-7"],
        "core": False,
    },
    {
        "lens": "deployment",
        "title": "Loom runs the same contracts anywhere",
        "caption": "Kubernetes, state, events, secrets, networking, and observability are portable while provider implementations remain replaceable.",
        "nodes": ["loom", "coordinator", "foundation"],
        "edges": ["deploy-2", "deploy-3"],
        "core": False,
    },
    {
        "lens": "deployment",
        "title": "Evidence closes every external side effect",
        "caption": "MCP gateways broker enterprise systems without giving credentials to Agents, and every action returns correlated proof.",
        "nodes": ["mcp", "external", "evidence", "solutions", "loom"],
        "edges": ["run-3", "evidence-1", "evidence-3", "deploy-1"],
        "core": False,
    },
]


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/Inter-Bold.ttf" if bold else "C:/Windows/Fonts/Inter-Regular.ttf"),
        Path("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def edge_path(source: str, target: str) -> str:
    start = NODES[source]
    end = NODES[target]
    x1, y1 = start["x"] * 10, start["y"] * 6.2
    x2, y2 = end["x"] * 10, end["y"] * 6.2
    control = (x1 + x2) / 2
    return f"M{x1:.1f},{y1:.1f} C{control:.1f},{y1:.1f} {control:.1f},{y2:.1f} {x2:.1f},{y2:.1f}"


def svg_overlay() -> str:
    paths = []
    for edge_id, source, target in EDGES:
        paths.append(
            f'<path class="flow-edge" data-edge="{edge_id}" d="{edge_path(source, target)}" '
            'pathLength="100" marker-end="url(#arrow)"/>'
        )
    return (
        '<svg class="flow-map" viewBox="0 0 1000 620" aria-hidden="true">'
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">'
        '<path d="M0,0 L0,6 L8,3 z" fill="currentColor"/></marker>'
        '<filter id="glow"><feGaussianBlur stdDeviation="4" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
        f'{"".join(paths)}</svg>'
    )


def node_markup() -> str:
    items = []
    for node_id, node in NODES.items():
        items.append(
            f'<button class="spatial-node node-{node_id}" data-node="{node_id}" '
            f'style="--x:{node["x"]}%;--y:{node["y"]}%">'
            f'<span>{html_escape(node["title"])}</span><small>{html_escape(node["sub"])}</small></button>'
        )
    return "".join(items)


def write_html() -> None:
    html = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Interactive spatial view of the ContextWeaver product hierarchy, governed execution, platform planes, and deployment boundaries.">
<title>ContextWeaver Spatial Architecture</title>
<script>if(window.self!==window.top||new URLSearchParams(location.search).has("embedded"))document.documentElement.classList.add("embedded");</script>
<style>
:root{--bg:#050b08;--panel:#0a1812;--panel2:#10261d;--panel3:#173429;--text:#f4f8f2;--muted:#9db2a8;--line:#315446;--mint:#70e6b1;--amber:#ffc76a;--red:#ff756d}
*{box-sizing:border-box}html{color-scheme:dark}body{min-width:320px;margin:0;color:var(--text);background:var(--bg);font:14px/1.5 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;overflow-x:hidden}
button{font:inherit}.experience{width:min(1280px,calc(100% - 28px));margin:18px auto;border:1px solid var(--line);border-radius:26px;background:linear-gradient(180deg,#0b1c15,#050b08);box-shadow:0 34px 100px #0009;overflow:hidden}
.storybar{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:center;gap:22px;min-height:82px;padding:13px 18px;border-bottom:1px solid var(--line);background:#091710e8;backdrop-filter:blur(20px)}
.stage-index{color:var(--mint);font-size:9px;font-weight:900;letter-spacing:.16em;text-transform:uppercase}.stage-title{display:block;margin-top:4px;font-size:clamp(19px,2.1vw,30px);line-height:1.05;letter-spacing:-.03em}.stage-caption{display:block;max-width:940px;margin-top:7px;color:var(--muted);font-size:11px}
.controls{display:flex;gap:7px}.controls button,.lensbar button{min-height:38px;padding:0 13px;border:1px solid var(--line);border-radius:9px;color:var(--text);background:var(--panel);cursor:pointer;font-size:10px;font-weight:850}.controls button:hover,.lensbar button:hover{border-color:var(--mint)}.controls .primary{border-color:var(--mint);color:#04100b;background:var(--mint)}
.lensbar{display:flex;align-items:center;gap:9px;padding:11px 20px;border-bottom:1px solid var(--line);background:#07110d}.lensbar span{margin-right:auto;color:var(--muted);font-size:9px;font-weight:900;letter-spacing:.13em;text-transform:uppercase}.lensbar button.active{border-color:var(--mint);color:#04100b;background:var(--mint)}
.viewport{position:relative;height:min(500px,38vw);min-height:440px;overflow:hidden;perspective:1500px;background:radial-gradient(circle at 52% 46%,#1c493550 0,transparent 30%),linear-gradient(180deg,#08140f,#040806)}
.horizon{position:absolute;inset:0;opacity:.35;background:linear-gradient(#31544655 1px,transparent 1px),linear-gradient(90deg,#31544655 1px,transparent 1px);background-size:44px 44px;transform:perspective(760px) rotateX(65deg) scale(1.55) translateY(28%);transform-origin:center bottom;mask-image:linear-gradient(to bottom,transparent 0,#000 36%,#000)}
.orb{position:absolute;border-radius:50%;filter:blur(50px);pointer-events:none}.orb.a{width:380px;height:250px;left:34%;top:24%;background:#70e6b125}.orb.b{width:300px;height:220px;right:8%;top:35%;background:#70e6b115}.orb.c{width:240px;height:190px;left:5%;bottom:5%;background:#ffc76a12}
.world{position:absolute;inset:0;transform-style:preserve-3d;transition:transform 1s cubic-bezier(.2,.8,.2,1)}.world[data-lens="product"]{transform:rotateX(0) rotateY(-1deg) scale(1)}.world[data-lens="execution"]{transform:rotateX(1deg) rotateY(1.5deg) scale(1.02)}.world[data-lens="platform"]{transform:rotateX(2deg) rotateY(-2deg) scale(.98)}.world[data-lens="deployment"]{transform:rotateX(0) rotateY(2deg) scale(.97)}
.deck{position:absolute;left:50%;width:55%;height:30%;border:1px solid var(--line);border-radius:26px;background:linear-gradient(145deg,#143126cc,#091710d9);box-shadow:0 28px 70px #0008,inset 0 1px #70e6b122;transform-style:preserve-3d}.deck::after{position:absolute;inset:13px;border:1px solid #31544688;border-radius:18px;content:""}.deck span{position:absolute;left:22px;top:18px;color:#9db2a8;font-size:9px;font-weight:900;letter-spacing:.14em;text-transform:uppercase}
.deck.experience{top:8%;transform:translateX(-50%) perspective(900px) rotateX(63deg) rotateZ(-5deg) translateZ(15px)}.deck.control{top:35%;width:65%;transform:translateX(-50%) perspective(900px) rotateX(63deg) rotateZ(-5deg);background:linear-gradient(145deg,#173d2eeb,#0a1912e8)}.deck.runtime{top:62%;width:72%;transform:translateX(-50%) perspective(900px) rotateX(63deg) rotateZ(-5deg) translateZ(-18px)}
.core{position:absolute;left:50%;top:49%;z-index:8;width:112px;height:112px;display:grid;place-items:center;border:1px solid var(--line);border-radius:50%;visibility:hidden;color:var(--muted);background:radial-gradient(circle at 35% 30%,#17342955,#10261d 48%,#050b08 75%);box-shadow:none;opacity:0;filter:saturate(.35);transform:translate(-50%,-50%) translateZ(40px) scale(.7);transition:opacity .4s,filter .4s,transform .4s,box-shadow .4s,border-color .4s}
.core::before,.core::after{position:absolute;border:1px solid #70e6b166;border-radius:50%;content:"";opacity:0}.core::before{inset:-16px}.core::after{inset:-30px}.core.active{visibility:visible;border-color:#70e6b1aa;color:var(--text);box-shadow:0 0 0 9px #70e6b10a,0 0 48px #70e6b138;opacity:1;filter:none;transform:translate(-50%,-50%) translateZ(100px) scale(1)}.core.active::before,.core.active::after{opacity:1;animation:orbit 8s linear infinite}.core.active::after{animation-direction:reverse;animation-duration:12s}.core div{text-align:center}.core b{display:block;font-size:15px}.core small{color:var(--muted);font-size:7px;font-weight:900;letter-spacing:.12em;text-transform:uppercase}.core.active small{color:var(--mint)}
@keyframes orbit{to{transform:rotate(360deg)}}.flow-map{position:absolute;inset:0;z-index:5;width:100%;height:100%;overflow:visible;pointer-events:none}.flow-edge{fill:none;stroke:#315446;stroke-width:1.3;color:#315446;opacity:.24;transition:.35s}.flow-edge.active{stroke:var(--mint);stroke-width:3;color:var(--mint);opacity:1;stroke-dasharray:8 5;animation:flow .85s linear infinite;filter:url(#glow)}@keyframes flow{to{stroke-dashoffset:-26}}
.spatial-node{position:absolute;left:var(--x);top:var(--y);z-index:10;width:clamp(132px,13vw,198px);min-height:74px;display:grid;align-content:center;gap:4px;padding:13px 15px;border:1px solid var(--line);border-radius:14px;color:var(--text);background:linear-gradient(145deg,#10261df2,#07110df2);box-shadow:0 16px 34px #0008;transform:translate(-50%,-50%) translateZ(48px);transition:.45s cubic-bezier(.2,.8,.2,1);cursor:pointer;text-align:left}.spatial-node::before{position:absolute;left:12px;right:12px;bottom:-7px;height:8px;border-radius:0 0 9px 9px;background:#06100c;content:"";opacity:.8}.spatial-node span{font-size:12px;font-weight:850}.spatial-node small{color:var(--muted);font-size:8px;line-height:1.35}.spatial-node.active{z-index:14;border-color:var(--mint);background:linear-gradient(145deg,#173f2e,#0a1b14);box-shadow:0 20px 45px #0009,0 0 0 4px #70e6b118,0 0 32px #70e6b125;transform:translate(-50%,-55%) translateZ(95px) scale(1.05)}.spatial-node.dim{opacity:.25;filter:saturate(.4)}.spatial-node.selected{outline:2px solid var(--amber);outline-offset:3px}
.detailbar{display:grid;grid-template-columns:1fr auto;align-items:center;gap:20px;min-height:68px;padding:13px 20px;border-top:1px solid var(--line);background:#07110d}.detailbar p{margin:0;color:var(--muted);font-size:11px}.detailbar strong{color:var(--mint)}.dots{display:flex;gap:7px}.dot{width:10px;height:10px;min-height:0;padding:0;border:0;border-radius:50%;background:var(--line);cursor:pointer}.dot.active{background:var(--mint);box-shadow:0 0 10px var(--mint)}
html.embedded body{background:transparent}html.embedded .experience{width:min(1280px,100%);margin:0 auto;border:0;border-radius:0;box-shadow:none}
@media(max-width:980px){.storybar{grid-template-columns:1fr}.controls{flex-wrap:wrap}.lensbar{overflow-x:auto}.lensbar span{display:none}.viewport{height:560px;min-height:560px}.spatial-node{width:150px}.node-agents,.node-mcp,.node-foundation{left:84%}.node-channels,.node-external{left:12%}}
@media(max-width:620px){.experience{width:100%;margin:0;border-radius:0}.storybar{padding:15px}.controls button{flex:1}.lensbar{padding:10px 15px}.viewport{height:620px;min-height:620px}.deck{width:86%}.deck.control{width:94%}.deck.runtime{width:98%}.core{width:92px;height:92px}.spatial-node{width:128px;min-height:66px;padding:10px}.spatial-node span{font-size:10px}.spatial-node small{font-size:7px}.node-channels{--x:18%!important;--y:13%!important}.node-solutions{--x:52%!important;--y:10%!important}.node-services{--x:83%!important;--y:20%!important}.node-workflows{--x:79%!important;--y:34%!important}.node-agents{--x:81%!important;--y:49%!important}.node-mcp{--x:79%!important;--y:64%!important}.node-foundation{--x:74%!important;--y:82%!important}.node-intent{--x:23%!important;--y:31%!important}.node-policy{--x:45%!important;--y:43%!important}.node-coordinator{--x:47%!important;--y:61%!important}.node-evidence{--x:31%!important;--y:79%!important}.node-external{--x:16%!important;--y:61%!important}.node-loom{--x:48%!important;--y:92%!important}.flow-map{display:none}.detailbar{grid-template-columns:1fr}.dots{justify-content:center}}
@media(prefers-reduced-motion:reduce){*{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}
</style>
</head>
<body>
<main class="experience">
  <header class="storybar">
    <div><span class="stage-index" id="stage-index"></span><strong class="stage-title" id="stage-title"></strong><span class="stage-caption" id="stage-caption"></span></div>
    <div class="controls"><button id="prev">Previous</button><button id="play" class="primary">Pause</button><button id="next">Next</button><button id="reset">Reset</button></div>
  </header>
  <nav class="lensbar" aria-label="Architecture lenses"><span>Choose a lens</span><button data-lens="product">Product composition</button><button data-lens="execution">Governed execution</button><button data-lens="platform">Platform planes</button><button data-lens="deployment">Deployment + integration</button></nav>
  <section class="viewport" aria-label="Interactive ContextWeaver spatial architecture">
    <div class="horizon"></div><div class="orb a"></div><div class="orb b"></div><div class="orb c"></div>
    <div class="world" id="world" data-lens="product">
      <div class="deck experience"><span>Experience and product plane</span></div>
      <div class="deck control"><span>Cerebro control plane</span></div>
      <div class="deck runtime"><span>Weave runtime + Loom foundation</span></div>
      <div class="core" id="core"><div><small>Governed core</small><b>Cerebro</b></div></div>
      __SVG__
      __NODES__
    </div>
  </section>
  <footer class="detailbar"><p><strong id="detail-title">ContextWeaver</strong> <span id="detail-copy">Select any component to hold and inspect it. Motion shows only the currently active semantic route.</span></p><div class="dots" id="dots"></div></footer>
</main>
<script>
const steps=__STEPS__;const nodeData=__NODE_DATA__;let current=0;let playing=!matchMedia("(prefers-reduced-motion: reduce)").matches;let timer;
const $=id=>document.getElementById(id);const nodeEls=[...document.querySelectorAll(".spatial-node")];const edgeEls=[...document.querySelectorAll(".flow-edge")];const lensButtons=[...document.querySelectorAll("[data-lens]")];
steps.forEach((_,index)=>{const button=document.createElement("button");button.className="dot";button.setAttribute("aria-label",`Show stage ${index+1}`);button.onclick=()=>{current=index;render();restart()};$("dots").appendChild(button)});
function inspect(id){const node=nodeData[id];if(!node)return;nodeEls.forEach(el=>el.classList.toggle("selected",el.dataset.node===id));$("detail-title").textContent=node.title;$("detail-copy").textContent=node.sub}
nodeEls.forEach(el=>el.onclick=()=>{playing=false;$("play").textContent="Play";stop();inspect(el.dataset.node)});
function render(){const step=steps[current];$("world").dataset.lens=step.lens;$("stage-index").textContent=`${step.lens} lens · stage ${current+1} of ${steps.length}`;$("stage-title").textContent=step.title;$("stage-caption").textContent=step.caption;$("core").classList.toggle("active",step.core===true);nodeEls.forEach(el=>{const active=step.nodes.includes(el.dataset.node);el.classList.toggle("active",active);el.classList.toggle("dim",!active);el.classList.remove("selected")});edgeEls.forEach(el=>el.classList.toggle("active",step.edges.includes(el.dataset.edge)));lensButtons.forEach(button=>button.classList.toggle("active",button.dataset.lens===step.lens));[...$("dots").children].forEach((dot,index)=>dot.classList.toggle("active",index===current));inspect(step.nodes[step.nodes.length-1]);reportHeight()}
function advance(delta=1){current=(current+delta+steps.length)%steps.length;render()}function stop(){clearInterval(timer)}function restart(){stop();if(playing)timer=setInterval(()=>advance(),5200)}
lensButtons.forEach(button=>button.onclick=()=>{current=steps.findIndex(step=>step.lens===button.dataset.lens);render();restart()});$("prev").onclick=()=>{advance(-1);restart()};$("next").onclick=()=>{advance();restart()};$("reset").onclick=()=>{current=0;render();restart()};$("play").onclick=()=>{playing=!playing;$("play").textContent=playing?"Pause":"Play";restart()};
function reportHeight(){if(!document.documentElement.classList.contains("embedded"))return;parent.postMessage({type:"contextweaver-spatial-height",height:Math.ceil(document.querySelector(".experience").getBoundingClientRect().height)},"*")}
if(document.documentElement.classList.contains("embedded")){new ResizeObserver(reportHeight).observe(document.querySelector(".experience"));addEventListener("load",reportHeight);addEventListener("resize",reportHeight)}
render();restart();
</script>
</body></html>"""
    html = (
        html.replace("__SVG__", svg_overlay())
        .replace("__NODES__", node_markup())
        .replace("__STEPS__", json.dumps(STEPS))
        .replace("__NODE_DATA__", json.dumps(NODES))
    )
    (OUT / f"{SLUG}.html").write_text(html, encoding="utf-8")


def svg_node(node_id: str, node: dict[str, object]) -> str:
    x = float(node["x"]) * 14 - 92
    y = float(node["y"]) * 7.3 - 35
    return (
        f'<g id="{node_id}" class="node"><rect x="{x:.1f}" y="{y:.1f}" width="184" height="70" rx="14"/>'
        f'<text class="title" x="{x + 14:.1f}" y="{y + 27:.1f}">{xml_escape(str(node["title"]))}</text>'
        f'<text class="sub" x="{x + 14:.1f}" y="{y + 47:.1f}">{xml_escape(str(node["sub"]))}</text></g>'
    )


def write_svg() -> None:
    edges = []
    for _, source, target in EDGES:
        a, b = NODES[source], NODES[target]
        x1, y1 = float(a["x"]) * 14, float(a["y"]) * 7.3
        x2, y2 = float(b["x"]) * 14, float(b["y"]) * 7.3
        edges.append(f'<path d="M{x1:.1f},{y1:.1f} C{(x1+x2)/2:.1f},{y1:.1f} {(x1+x2)/2:.1f},{y2:.1f} {x2:.1f},{y2:.1f}"/>')
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 840" role="img" aria-labelledby="title desc">
<title id="title">ContextWeaver spatial architecture</title><desc id="desc">A spatial system map showing product composition, Cerebro governance, Weave runtime capabilities, Loom infrastructure, external systems, and evidence.</desc>
<defs><pattern id="grid" width="42" height="42" patternUnits="userSpaceOnUse"><path d="M42 0H0V42" fill="none" stroke="#315446" opacity=".18"/></pattern><filter id="glow"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<rect width="1400" height="840" fill="{COLORS["bg"]}"/><rect width="1400" height="840" fill="url(#grid)"/>
<text x="46" y="48" fill="{COLORS["text"]}" font-family="Inter,Segoe UI,sans-serif" font-size="27" font-weight="700">ContextWeaver Spatial Architecture</text>
<text x="46" y="73" fill="{COLORS["muted"]}" font-family="Inter,Segoe UI,sans-serif" font-size="12">Cerebro governs · Weave composes · Loom runs anywhere · Evidence follows every action</text>
<g opacity=".9"><path d="M280 120 L1130 120 L1260 245 L410 245 Z" fill="#10261d" stroke="#315446"/><path d="M205 325 L1175 325 L1300 470 L330 470 Z" fill="#173429" stroke="#70e6b1"/><path d="M145 555 L1210 555 L1340 720 L275 720 Z" fill="#0a1812" stroke="#315446"/></g>
<g class="edges" fill="none" stroke="{COLORS["line"]}" stroke-width="2" opacity=".55">{"".join(edges)}</g>
<g class="nodes">{"".join(svg_node(node_id, node) for node_id, node in NODES.items())}</g>
<style>.node rect{{fill:#0a1812;stroke:#315446;stroke-width:1.5}}.title{{fill:#f4f8f2;font:700 12px Inter,Segoe UI,sans-serif}}.sub{{fill:#9db2a8;font:8px Inter,Segoe UI,sans-serif}}</style></svg>"""
    (OUT / f"{SLUG}.svg").write_text(svg, encoding="utf-8")


def polygon_for_deck(y: int, left: int, right: int, depth: int) -> list[tuple[int, int]]:
    return [(left + 80, y), (right - 80, y), (right, y + depth), (left, y + depth)]


def node_box(node: dict[str, object], size: tuple[int, int]) -> tuple[int, int, int, int]:
    width, height = size
    x = int(float(node["x"]) / 100 * width)
    y = int(float(node["y"]) / 100 * (height - 110))
    w = 150 if width >= 1000 else 120
    h = 62 if width >= 1000 else 54
    return x - w // 2, y - h // 2, x + w // 2, y + h // 2


def render_frame(step: dict[str, object] | None, size: tuple[int, int]) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size, COLORS["bg"])
    draw = ImageDraw.Draw(image)
    for x in range(0, width, 42):
        draw.line((x, 0, x, height - 105), fill="#0c1d16", width=1)
    for y in range(0, height - 105, 42):
        draw.line((0, y, width, y), fill="#0c1d16", width=1)
    draw.text((28, 20), "ContextWeaver Spatial Architecture", fill=COLORS["text"], font=font(24, True))
    draw.text((28, 50), "Cerebro governs · Weave composes · Loom runs anywhere", fill=COLORS["muted"], font=font(11))
    scene_h = height - 110
    decks = [
        (int(scene_h * .16), int(width * .18), int(width * .82), int(scene_h * .12), "#10261d"),
        (int(scene_h * .40), int(width * .12), int(width * .88), int(scene_h * .14), "#173429"),
        (int(scene_h * .66), int(width * .08), int(width * .92), int(scene_h * .16), "#0a1812"),
    ]
    for y, left, right, depth, fill in decks:
        draw.polygon(polygon_for_deck(y, left, right, depth), fill=fill, outline=COLORS["line"])
    active_nodes = set(step["nodes"]) if step else set()
    active_edges = set(step["edges"]) if step else set()
    by_edge = {edge_id: (source, target) for edge_id, source, target in EDGES}
    for edge_id, (source, target) in by_edge.items():
        a = node_box(NODES[source], size)
        b = node_box(NODES[target], size)
        color = COLORS["mint"] if edge_id in active_edges else "#1e382e"
        draw.line(((a[0] + a[2]) // 2, (a[1] + a[3]) // 2, (b[0] + b[2]) // 2, (b[1] + b[3]) // 2), fill=color, width=4 if edge_id in active_edges else 2)
    for node_id, node in NODES.items():
        box = node_box(node, size)
        active = node_id in active_nodes
        draw.rounded_rectangle(box, radius=11, fill=COLORS["panel3"] if active else COLORS["panel"], outline=COLORS["mint"] if active else COLORS["line"], width=4 if active else 2)
        draw.text((box[0] + 10, box[1] + 12), str(node["title"]), fill=COLORS["text"], font=font(10 if width < 1000 else 12, True))
        sub = wrap(str(node["sub"]), width=25)[:2]
        for index, line in enumerate(sub):
            draw.text((box[0] + 10, box[1] + 32 + index * 11), line, fill=COLORS["muted"], font=font(7 if width < 1000 else 8))
    cx, cy = width // 2, int(scene_h * .49)
    core_active = bool(step and step.get("core"))
    if core_active:
        core_radius = 45
        draw.ellipse(
            (cx - core_radius, cy - core_radius, cx + core_radius, cy + core_radius),
            fill=COLORS["panel2"],
            outline=COLORS["mint"],
            width=3,
        )
        draw.text((cx - 30, cy - 10), "Cerebro", fill=COLORS["text"], font=font(15, True))
    if step:
        footer = height - 92
        draw.text((28, footer), str(step["title"]), fill=COLORS["mint"], font=font(19, True))
        for index, line in enumerate(wrap(str(step["caption"]), width=105)[:2]):
            draw.text((28, footer + 28 + index * 17), line, fill=COLORS["muted"], font=font(10))
    return image


def write_images() -> None:
    static = render_frame(None, (1400, 840))
    static.save(OUT / f"{SLUG}.png", optimize=True)
    frames = [render_frame(step, (1200, 720)) for step in STEPS]
    frames[0].save(
        OUT / f"{SLUG}.gif",
        save_all=True,
        append_images=frames[1:],
        duration=GIF_FRAME_DURATION_MS,
        loop=0,
        disposal=2,
        optimize=False,
    )


def write_drawio() -> None:
    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
    cells.append(
        f'<mxCell id="title" value="ContextWeaver Spatial Architecture" style="text;html=1;strokeColor=none;fillColor=none;fontSize=18;fontStyle=1;fontColor={COLORS["text"]};" vertex="1" parent="1"><mxGeometry x="50" y="30" width="900" height="40" as="geometry"/></mxCell>'
    )
    zones = [
        ("zone-experience", "EXPERIENCE + PRODUCT", 160, 90, 1080, 170, COLORS["panel2"]),
        ("zone-control", "CEREBRO CONTROL PLANE", 120, 295, 1160, 190, COLORS["panel3"]),
        ("zone-runtime", "WEAVE RUNTIME + LOOM FOUNDATION", 80, 525, 1240, 190, COLORS["panel"]),
    ]
    for zone_id, label, x, y, w, h, fill in zones:
        cells.append(
            f'<mxCell id="{zone_id}" value="{label}" style="swimlane;startSize=30;rounded=1;html=1;fillColor={fill};strokeColor={COLORS["line"]};fontColor={COLORS["muted"]};fontStyle=1;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
        )
    drawio_positions = {
        "channels": (190, 135), "solutions": (400, 125), "services": (610, 125), "workflows": (820, 125),
        "agents": (1040, 115), "mcp": (1040, 205), "foundation": (1030, 630), "intent": (200, 345),
        "policy": (470, 345), "coordinator": (740, 345), "evidence": (1010, 345), "external": (180, 610), "loom": (550, 610),
    }
    for node_id, node in NODES.items():
        x, y = drawio_positions[node_id]
        value = xml_escape(f'<b>{node["title"]}</b><br><font color="#9db2a8">{node["sub"]}</font>', {'"': '&quot;'})
        cells.append(
            f'<mxCell id="{node_id}" value="{value}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={COLORS["panel"]};strokeColor={COLORS["mint"]};fontColor={COLORS["text"]};fontSize=11;strokeWidth=2;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="170" height="68" as="geometry"/></mxCell>'
        )
    for edge_id, source, target in EDGES:
        cells.append(
            f'<mxCell id="{edge_id}" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;endFill=1;strokeColor={COLORS["line"]};" edge="1" source="{source}" target="{target}" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>'
        )
    model = (
        '<mxGraphModel dx="1400" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1400" pageHeight="800" math="0" shadow="0" '
        f'background="{COLORS["bg"]}"><root>{"".join(cells)}</root></mxGraphModel>'
    )
    xml = f'<mxfile host="Electron" modified="2026-11-01T16:00:00Z" version="26.0.0"><diagram id="spatial-architecture" name="Spatial Architecture">{model}</diagram></mxfile>'
    (OUT / f"{SLUG}.drawio").write_text(xml, encoding="utf-8")


def main(*, skip_raster: bool = False) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    write_html()
    write_svg()
    write_drawio()
    if not skip_raster:
        write_images()
    print(f"Generated spatial architecture experience in {OUT}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-raster", action="store_true")
    args = parser.parse_args()
    main(skip_raster=args.skip_raster)
