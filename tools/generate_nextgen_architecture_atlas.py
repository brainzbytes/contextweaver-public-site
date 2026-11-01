from __future__ import annotations

import argparse
from dataclasses import dataclass
from html import escape as html_escape
from pathlib import Path
from textwrap import wrap
from xml.sax.saxutils import escape as xml_escape

from PIL import Image, ImageDraw, ImageFont


OUT = Path(__file__).resolve().parents[1] / "diagrams"
GIF_FRAME_DURATION_MS = 1000

COLORS = {
    "bg": "#07110f",
    "panel": "#10231e",
    "panel2": "#152d26",
    "text": "#f4f8f2",
    "muted": "#a8bbb3",
    "line": "#38544a",
    "mint": "#70e6b1",
    "amber": "#ffc76a",
    "coral": "#7fb98d",
    "violet": "#9bcf9f",
    "sky": "#52b788",
    "red": "#ff6f69",
}


@dataclass(frozen=True)
class Node:
    id: str
    title: str
    subtitle: str
    detail: str
    x: int
    y: int
    w: int
    h: int
    color: str
    group: str


@dataclass(frozen=True)
class Edge:
    id: str
    source: str
    target: str
    label: str
    kind: str = "data"


NODES = [
    Node("people", "Users + channels", "Consumers | builders | operators | delegated clients | events",
         "One authenticated entry point presents My Solutions, Studio, operations, APIs, events, and delegated assistant channels according to current entitlement. Users never need direct infrastructure credentials.",
         45, 95, 235, 82, "sky", "access"),
    Node("workspace", "Collaborative Workspaces", "Plain language | code | notebooks | documents | data",
         "A shared place to explore intent, specifications, code, documents, data, and AI assistance before anything is promoted.",
         325, 95, 260, 82, "mint", "experience"),
    Node("studios", "Five Studio contexts", "MCP | Agent | Workflow | Service | Solution",
         "Purpose-built contexts create distinct typed assets and complete Solution compositions rather than hiding every behavior inside one unrestricted prompt.",
         625, 95, 260, 82, "mint", "experience"),
    Node("operations", "Operations + approvals", "Run history | topology | evidence | human decisions",
         "Operators, risk owners, and approvers inspect health, evidence, pending decisions, failures, retries, and release status.",
         925, 95, 260, 82, "amber", "experience"),
    Node("inputs", "Enterprise inputs", "Specs | OpenAPI | MCP | repositories | wikis | data",
         "ContextWeaver can start from a described outcome or approved enterprise material, including specifications, APIs, MCP servers, code, knowledge, and data products.",
         45, 235, 235, 105, "sky", "access"),
    Node("intent", "Intent + contract compiler", "Normalize requirements into typed assets and graphs",
         "Cerebro converts desired outcomes into explicit Solution, Service, Workflow, Agent, MCP, data, model, policy, experience, and evidence contracts.",
         325, 235, 260, 105, "mint", "cerebro"),
    Node("identity", "Identity + entitlements", "Tenant | user | role | groups | purpose | delegation",
         "Every protected action carries verified identity, tenant, purpose, delegated authority, and entitlement context.",
         625, 235, 260, 105, "violet", "cerebro"),
    Node("policy", "Policy + approval", "Risk | side effects | separation of duties | admission",
         "Policy constrains discovery and execution, requires approval where needed, prevents self-approval, and records every decision.",
         925, 235, 260, 105, "amber", "cerebro"),
    Node("registry", "Registry + lifecycle", "Schemas | versions | compatibility | trust | promotion",
         "Only immutable, compatible, healthy, entitled, region-appropriate, and lifecycle-eligible releases can be discovered.",
         1225, 235, 230, 105, "coral", "cerebro"),
    Node("solutions", "Solutions", "User-facing compositions | experience lifecycle",
         "Solutions are the final consumer-facing experiences and complete dependency graphs assembled from reusable Services and lower-level governed capabilities.",
         325, 405, 145, 92, "mint", "weave"),
    Node("services", "Services", "Reusable executable contracts",
         "Services expose stable intent-to-outcome contracts pinned to approved Workflows, with typed inputs, outputs, policy, ownership, SLOs, and lifecycle.",
         485, 405, 145, 92, "mint", "weave"),
    Node("workflows", "Workflows", "Durable graphs | waits | retries",
         "Workflows are typed state machines with checkpoints, approvals, callbacks, idempotency, retries, and compensation.",
         645, 405, 145, 92, "mint", "weave"),
    Node("agents", "Agents", "Bounded reasoning | goals | evaluations",
         "Agents reason within a constrained plan, model envelope, data scope, tool allow-list, budget, and evaluation policy.",
         805, 405, 145, 92, "coral", "weave"),
    Node("mcp", "MCP capabilities", "Tools | resources | prompts | adapters",
         "MCP servers broker tool access with validated schemas, delegated identity, rate limits, audit, receipts, and compensation metadata.",
         965, 405, 160, 92, "sky", "weave"),
    Node("knowledge", "RAG + data products", "Authorized retrieval | citations | lineage",
         "Retrieval respects source authority, ACLs, purpose, classification, residency, freshness, retention, and immutable generation pins.",
         1140, 405, 160, 92, "sky", "weave"),
    Node("models", "Models + memory", "Provider aliases | routing | bounded continuity",
         "Model providers are replaceable behind governed aliases, while memory is scoped, retained, and authorized independently.",
         1315, 405, 140, 92, "violet", "weave"),
    Node("dryrun", "Safe Dry Run Lab", "No real side effects | mocks | faults | comparison",
         "Designs are rehearsed with mocked side effects, deterministic fixtures, fault injection, evaluation, and evidence before promotion.",
         325, 555, 260, 100, "amber", "runtime"),
    Node("plan", "Immutable execution plan", "Exact versions | policies | budgets | fallbacks",
         "Cerebro resolves the complete compatible graph, validates all bindings, and freezes exact versions before execution.",
         625, 555, 260, 100, "violet", "runtime"),
    Node("orchestrator", "Durable orchestrator", "Commands | queues | checkpoints | Saga",
         "The runtime persists commands and state, coordinates parallel work, handles waits and retries, and compensates safely.",
         925, 555, 260, 100, "mint", "runtime"),
    Node("evidence", "Evidence + evaluation", "Logs | metrics | traces | receipts | quality | cost",
         "Every run returns correlated operational, policy, model, retrieval, tool, approval, business, quality, and cost evidence.",
         1225, 555, 230, 100, "amber", "runtime"),
    Node("operator", "Capability Operator", "MCPEngine CRDs | Helm | GitOps | reconciliation",
         "The cloud-neutral operator reconciles approved desired state into isolated Kubernetes workloads and reports status without cloud-provider coupling.",
         325, 725, 260, 105, "mint", "loom"),
    Node("kubernetes", "Portable Kubernetes runtime", "Namespaces | identity | network | quotas | probes",
         "AKS, EKS, GKE, k3s, private cloud, and edge clusters host the same capability contracts and OCI artifacts.",
         625, 725, 260, 105, "violet", "loom"),
    Node("data", "State + knowledge substrate", "Database | event bus | object store | search | cache",
         "Portable provider adapters supply durable state, queues, eventing, object storage, vector or lexical search, and caching.",
         925, 725, 260, 105, "sky", "loom"),
    Node("observe", "Operations foundation", "Secrets | observability | backup | recovery | FinOps",
         "Loom provides secrets, identity, networking, telemetry, backup, recovery, cost controls, and deployment profiles.",
         1225, 725, 230, 105, "amber", "loom"),
    Node("external", "External systems", "SaaS | APIs | databases | enterprise tools | humans",
         "Adapters connect to external tools and services while keeping provider credentials outside Agents and preserving policy and evidence.",
         45, 555, 235, 105, "coral", "external"),
    Node("clouds", "Any deployment profile", "Azure | AWS | Google | private | sovereign | edge",
         "The control plane contracts remain stable while provider-specific infrastructure, assurance, residency, and qualification vary by profile.",
         45, 725, 235, 105, "violet", "external"),
]


EDGES = [
    Edge("e1", "people", "workspace", "intent and collaboration"),
    Edge("e2", "workspace", "studios", "design"),
    Edge("e3", "inputs", "intent", "ingest"),
    Edge("e4", "studios", "intent", "typed assets"),
    Edge("e5", "intent", "identity", "authorize", "governance"),
    Edge("e6", "identity", "policy", "eligible actions", "governance"),
    Edge("e7", "policy", "registry", "admit and promote", "governance"),
    Edge("e8", "registry", "solutions", "published Solutions", "success"),
    Edge("e9", "solutions", "services", "experience actions"),
    Edge("e9b", "services", "workflows", "execute"),
    Edge("e10", "workflows", "agents", "delegate"),
    Edge("e11", "agents", "mcp", "tool boundary"),
    Edge("e12", "agents", "knowledge", "authorized context"),
    Edge("e13", "agents", "models", "model alias"),
    Edge("e14", "mcp", "external", "side effects and receipts"),
    Edge("e15", "studios", "dryrun", "rehearse", "waiting"),
    Edge("e16", "dryrun", "policy", "evidence for approval", "evidence"),
    Edge("e17", "registry", "operator", "approved desired state", "success"),
    Edge("e18", "solutions", "plan", "launch Service Run"),
    Edge("e19", "plan", "orchestrator", "commit plan", "governance"),
    Edge("e20", "orchestrator", "workflows", "typed work"),
    Edge("e21", "orchestrator", "evidence", "traces and outcomes", "evidence"),
    Edge("e22", "evidence", "operations", "operate and improve", "evidence"),
    Edge("e23", "operator", "kubernetes", "reconcile"),
    Edge("e24", "kubernetes", "data", "state and events"),
    Edge("e25", "data", "observe", "telemetry and recovery", "evidence"),
    Edge("e26", "clouds", "kubernetes", "deployment profile"),
    Edge("e27", "people", "solutions", "discover and use"),
]


STAGES = [
    {
        "title": "Start with people, intent, and approved enterprise material",
        "caption": "Business users, builders, operators, APIs, and events enter through governed channels and collaborative Workspaces.",
        "nodes": ["people", "workspace", "inputs"],
        "edges": ["e1", "e3"],
    },
    {
        "title": "Create distinct assets in purpose-built Studios",
        "caption": "MCP, Agent, Workflow, Service, and Solution contexts produce inspectable typed contracts, complete dependency graphs, implementation assets, tests, and configuration references.",
        "nodes": ["workspace", "studios", "intent"],
        "edges": ["e2", "e4"],
    },
    {
        "title": "Rehearse safely before real execution",
        "caption": "The Safe Dry Run Lab mocks side effects, injects failures, evaluates quality and cost, and produces evidence without changing production systems.",
        "nodes": ["studios", "dryrun", "policy"],
        "edges": ["e15", "e16"],
    },
    {
        "title": "Govern and promote one immutable version",
        "caption": "Identity, entitlements, policy, separation of duties, compatibility, evidence, and approval determine what may enter the Registry.",
        "nodes": ["intent", "identity", "policy", "registry"],
        "edges": ["e5", "e6", "e7"],
    },
    {
        "title": "Compose user-facing Solutions from reusable capabilities",
        "caption": "Solutions define the experience and complete graph; reusable Services execute approved Workflows over Agents, MCP capabilities, governed knowledge, models, and memory.",
        "nodes": ["people", "solutions", "services", "workflows", "agents", "mcp", "knowledge", "models"],
        "edges": ["e8", "e9", "e9b", "e10", "e11", "e12", "e13", "e27"],
    },
    {
        "title": "Compile and execute a durable authorized plan",
        "caption": "Each request resolves exact compatible versions, freezes policy and budget, persists execution state, coordinates parallel work, and handles waits or compensation.",
        "nodes": ["solutions", "services", "plan", "orchestrator", "workflows", "agents"],
        "edges": ["e18", "e19", "e20"],
    },
    {
        "title": "Broker tools, external services, and human authority",
        "caption": "MCP gateways invoke external systems under delegated identity while credentials remain outside Agents and every side effect returns a receipt.",
        "nodes": ["agents", "mcp", "external", "operations"],
        "edges": ["e11", "e14"],
    },
    {
        "title": "Operate with evidence on any cloud",
        "caption": "The Capability Operator reconciles approved desired state into Kubernetes; state, search, events, secrets, telemetry, backup, recovery, and evidence close the lifecycle.",
        "nodes": ["registry", "operator", "kubernetes", "data", "observe", "clouds", "evidence", "operations"],
        "edges": ["e17", "e21", "e22", "e23", "e24", "e25", "e26"],
    },
]


GROUPS = [
    ("EXPERIENCE - Workspaces, Studios, operations", 305, 72, 900, 125, "mint"),
    ("CEREBRO - Understand, govern, compile, orchestrate, prove", 305, 207, 1168, 155, "violet"),
    ("WEAVE - Reusable governed capability fabric", 305, 377, 1168, 142, "sky"),
    ("RUNTIME - Rehearse, execute durably, collect evidence", 305, 527, 1168, 150, "amber"),
    ("LOOM - Portable operational foundation", 305, 697, 1168, 155, "violet"),
]


def center(node: Node) -> tuple[float, float]:
    return node.x + node.w / 2, node.y + node.h / 2


def edge_path(edge: Edge) -> tuple[str, float, float]:
    by_id = {n.id: n for n in NODES}
    source = by_id[edge.source]
    target = by_id[edge.target]
    sx, sy = center(source)
    tx, ty = center(target)
    if abs(tx - sx) >= abs(ty - sy):
        start_x = source.x + source.w if tx > sx else source.x
        end_x = target.x if tx > sx else target.x + target.w
        mid_x = (start_x + end_x) / 2
        d = f"M {start_x} {sy} L {mid_x} {sy} L {mid_x} {ty} L {end_x} {ty}"
        return d, mid_x, (sy + ty) / 2 - 7
    start_y = source.y + source.h if ty > sy else source.y
    end_y = target.y if ty > sy else target.y + target.h
    mid_y = (start_y + end_y) / 2
    d = f"M {sx} {start_y} L {sx} {mid_y} L {tx} {mid_y} L {tx} {end_y}"
    return d, (sx + tx) / 2, mid_y - 7


def svg_markup() -> str:
    group_parts = []
    for label, x, y, w, h, color in GROUPS:
        group_parts.append(
            f'<g class="zone zone-{color}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20"/>'
            f'<text x="{x + 18}" y="{y + 24}">{xml_escape(label)}</text></g>'
        )
    edge_parts = []
    for edge in EDGES:
        d, lx, ly = edge_path(edge)
        edge_parts.append(
            f'<g id="edge-{edge.id}" class="edge edge-{edge.kind}" data-edge-id="{edge.id}">'
            f'<path d="{d}" marker-end="url(#arrow)"/><text x="{lx:.1f}" y="{ly:.1f}">{xml_escape(edge.label)}</text></g>'
        )
    node_parts = []
    for node in NODES:
        lines = wrap(node.subtitle, width=max(18, node.w // 13))[:2]
        subtitle = "".join(
            f'<tspan x="{node.x + node.w / 2:.1f}" dy="{0 if i == 0 else 14}">{xml_escape(line)}</tspan>'
            for i, line in enumerate(lines)
        )
        node_parts.append(
            f'<g id="node-{node.id}" class="node node-{node.color}" data-node-id="{node.id}" '
            f'role="button" tabindex="0" aria-label="{xml_escape(node.title)}">'
            f'<rect x="{node.x}" y="{node.y}" width="{node.w}" height="{node.h}" rx="15"/>'
            f'<text class="node-title" x="{node.x + node.w / 2:.1f}" y="{node.y + 34}">{xml_escape(node.title)}</text>'
            f'<text class="node-subtitle" x="{node.x + node.w / 2:.1f}" y="{node.y + 57}">{subtitle}</text>'
            f'</g>'
        )
    return f"""<svg class="architecture" viewBox="0 0 1500 880" role="img" aria-labelledby="diagram-title diagram-desc">
<title id="diagram-title">ContextWeaver NextGen architecture atlas</title>
<desc id="diagram-desc">Current ContextWeaver architecture from collaborative Workspaces and four Studios through Cerebro governance, Weave capabilities, durable runtime, evidence, Capability Operator, and cloud-neutral Loom infrastructure.</desc>
<defs>
  <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="context-stroke"/></marker>
  <filter id="glow"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse"><path d="M50 0H0V50" fill="none" stroke="#38544a" stroke-width="1" opacity=".23"/></pattern>
</defs>
<rect width="1500" height="880" fill="#07110f"/><rect width="1500" height="880" fill="url(#grid)"/>
<text class="diagram-title" x="45" y="42">ContextWeaver NextGen Architecture</text>
<text class="diagram-subtitle" x="45" y="65">Cerebro governs. Weave composes. Loom runs anywhere. Evidence follows every lifecycle stage.</text>
{''.join(group_parts)}
<g class="edges">{''.join(edge_parts)}</g>
<g class="nodes">{''.join(node_parts)}</g>
<text class="trust-label" x="1480" y="865" text-anchor="end">Identity | Policy | Approval | Audit | Evidence span every layer</text>
</svg>"""


def write_svg() -> None:
    svg = svg_markup()
    css = """
<style>
.diagram-title{fill:#f4f8f2;font:700 25px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}.diagram-subtitle{fill:#a8bbb3;font:12px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
.zone rect{fill:#10231e;fill-opacity:.35;stroke:#38544a;stroke-width:1.5}.zone text{fill:#a8bbb3;font:800 10px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;letter-spacing:1.2px}
.zone-mint rect{stroke:#70e6b1}.zone-violet rect{stroke:#9bcf9f}.zone-sky rect{stroke:#52b788}.zone-amber rect{stroke:#ffc76a}
.node rect{fill:#10231e;stroke:#38544a;stroke-width:2}.node-mint rect{stroke:#70e6b1}.node-amber rect{stroke:#ffc76a}.node-coral rect{stroke:#7fb98d}.node-violet rect{stroke:#9bcf9f}.node-sky rect{stroke:#52b788}
.node-title{fill:#f4f8f2;font:700 13px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;text-anchor:middle}.node-subtitle{fill:#a8bbb3;font:9px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;text-anchor:middle}
.edge{opacity:.32}.edge path{fill:none;stroke:#52b788;stroke-width:2}.edge text{fill:#a8bbb3;font:8px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;text-anchor:middle;paint-order:stroke;stroke:#07110f;stroke-width:4}
.edge-governance path{stroke:#9bcf9f;stroke-dasharray:8 6}.edge-success path{stroke:#70e6b1}.edge-evidence path{stroke:#ffc76a;stroke-dasharray:5 5}.edge-waiting path{stroke:#ffc76a;stroke-dasharray:10 7}
.trust-label{fill:#ffc76a;font:700 10px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
</style>"""
    standalone = svg.replace("<defs>", f"<defs>{css}", 1)
    (OUT / "contextweaver-nextgen-architecture.svg").write_text(standalone, encoding="utf-8")


def write_html() -> None:
    node_data = {
        n.id: {"title": n.title, "subtitle": n.subtitle, "detail": n.detail, "group": n.group}
        for n in NODES
    }
    import json
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Explore the complete ContextWeaver NextGen architecture across Workspaces, Studios, Cerebro, Weave, durable runtime, evidence, and portable Loom infrastructure.">
<title>ContextWeaver NextGen Architecture Atlas</title>
<script>if(window.self!==window.top||new URLSearchParams(location.search).has("embed"))document.documentElement.classList.add("embedded");</script>
<style>
:root{{--bg:{COLORS['bg']};--panel:{COLORS['panel']};--panel2:{COLORS['panel2']};--text:{COLORS['text']};--muted:{COLORS['muted']};--line:{COLORS['line']};--mint:{COLORS['mint']};--amber:{COLORS['amber']};--coral:{COLORS['coral']};--violet:{COLORS['violet']};--sky:{COLORS['sky']}}}
*{{box-sizing:border-box}}body{{margin:0;color:var(--text);background:var(--bg);font:14px/1.5 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
.shell{{display:grid;grid-template-columns:minmax(0,1fr) 340px;min-height:100dvh}}.canvas{{position:relative;overflow:auto;border-right:1px solid var(--line)}}.architecture{{display:block;min-width:1120px;width:100%;height:auto}}
.diagram-title{{fill:#f4f8f2;font:700 25px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}.diagram-subtitle{{fill:#a8bbb3;font:12px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
.zone rect{{fill:#10231e;fill-opacity:.35;stroke:#38544a;stroke-width:1.5}}.zone text{{fill:#a8bbb3;font:800 10px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;letter-spacing:1.2px}}
.zone-mint rect{{stroke:#70e6b1}}.zone-violet rect{{stroke:#9bcf9f}}.zone-sky rect{{stroke:#52b788}}.zone-amber rect{{stroke:#ffc76a}}
.node{{cursor:pointer}}.node rect{{fill:#10231e;stroke:#38544a;stroke-width:2;transition:.25s}}.node-mint rect{{stroke:#70e6b1}}.node-amber rect{{stroke:#ffc76a}}.node-coral rect{{stroke:#7fb98d}}.node-violet rect{{stroke:#9bcf9f}}.node-sky rect{{stroke:#52b788}}
.node-title{{fill:#f4f8f2;font:700 13px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;text-anchor:middle}}.node-subtitle{{fill:#a8bbb3;font:9px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;text-anchor:middle}}
.node:hover rect,.node.selected rect{{stroke-width:4}}.node.active rect{{stroke-width:5;filter:url(#glow)}}.node.complete{{opacity:.58}}
.edge{{opacity:.18}}.edge path{{fill:none;stroke:#52b788;stroke-width:2}}.edge text{{fill:#a8bbb3;font:8px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;text-anchor:middle;paint-order:stroke;stroke:#07110f;stroke-width:4}}
.edge-governance path{{stroke:#9bcf9f;stroke-dasharray:8 6}}.edge-success path{{stroke:#70e6b1}}.edge-evidence path{{stroke:#ffc76a;stroke-dasharray:5 5}}.edge-waiting path{{stroke:#ffc76a;stroke-dasharray:10 7}}
.edge.active{{opacity:1}}.edge.active path{{stroke-width:5;stroke-dasharray:14 9;animation:flow .8s linear infinite;filter:url(#glow)}}@keyframes flow{{to{{stroke-dashoffset:-23}}}}
.trust-label{{fill:#ffc76a;font:700 10px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
.panel{{display:flex;flex-direction:column;min-width:0;background:linear-gradient(180deg,var(--panel2),var(--bg));position:sticky;top:0;height:100dvh}}
.panel-head{{padding:22px;border-bottom:1px solid var(--line)}}.eyebrow{{margin:0 0 7px;color:var(--mint);font-size:9px;font-weight:900;letter-spacing:.15em;text-transform:uppercase}}h1{{margin:0;font:700 26px/1.08 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}.panel-head p{{margin:9px 0 0;color:var(--muted);font-size:11px}}
.legend{{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-top:15px;color:var(--muted);font-size:9px}}.legend span::before{{content:"";display:inline-block;width:10px;height:3px;margin-right:6px;vertical-align:middle;background:var(--sky)}}.legend .gov::before{{background:var(--violet)}}.legend .success::before{{background:var(--mint)}}.legend .evidence::before{{background:var(--amber)}}
.detail{{min-height:225px;padding:22px;border-bottom:1px solid var(--line)}}.detail b{{display:block;font:700 20px/1.2 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}.detail em{{display:block;margin:7px 0 12px;color:var(--amber);font-size:10px;font-style:normal;font-weight:800}}.detail p{{margin:0;color:#c8d6d0;font-size:12px}}
.stage{{flex:1;padding:22px;overflow:auto}}.stage-count{{color:var(--mint);font-size:10px;font-weight:900;letter-spacing:.12em;text-transform:uppercase}}.stage h2{{margin:8px 0;font:700 22px/1.18 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}.stage p{{margin:0;color:var(--muted);font-size:12px}}
.controls{{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;padding:12px;border-top:1px solid var(--line)}}button{{min-height:40px;border:1px solid var(--line);border-radius:9px;color:var(--text);background:var(--panel);cursor:pointer;font:800 11px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}button:hover{{border-color:var(--mint)}}button.primary{{color:#07110f;background:var(--mint)}}
.dots{{display:flex;flex-wrap:wrap;gap:7px;padding:0 18px 17px}}.dot{{width:11px;height:11px;min-height:0;padding:0;border:0;border-radius:50%;background:var(--line)}}.dot.active{{background:var(--mint);box-shadow:0 0 10px var(--mint)}}
html.embedded .shell{{grid-template-columns:1fr;min-height:0}}
html.embedded .canvas{{overflow:hidden;border-right:0;border-bottom:1px solid var(--line)}}
html.embedded .architecture{{min-width:0;width:100%}}
html.embedded .panel{{position:relative;top:auto;height:auto;min-height:0;display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);grid-template-areas:"head detail" "stage stage" "controls dots";grid-template-rows:auto auto auto}}
html.embedded .panel-head{{grid-area:head}}html.embedded .detail{{grid-area:detail;min-height:0}}html.embedded .stage{{grid-area:stage;min-height:0;overflow:visible}}html.embedded .controls{{grid-area:controls}}html.embedded .dots{{grid-area:dots;align-items:center;padding:12px 18px}}
@media(max-width:980px){{.shell{{grid-template-columns:1fr}}.canvas{{border-right:0;border-bottom:1px solid var(--line)}}.panel{{position:relative;height:auto;min-height:520px}}.architecture{{min-width:0;width:100%}}html.embedded .panel{{grid-template-columns:1fr;grid-template-areas:"head" "detail" "stage" "controls" "dots"}}}}
@media(prefers-reduced-motion:reduce){{*{{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}}}
</style></head><body><main class="shell"><section class="canvas">{svg_markup()}</section>
<aside class="panel" aria-live="polite">
<div class="panel-head"><p class="eyebrow">Interactive architecture</p><h1>NextGen Architecture Atlas</h1><p>Inspired by the legacy Cerebro, Weave, and Loom diagrams, updated to the current governed capability lifecycle.</p>
<div class="legend"><span>Data / work</span><span class="gov">Governance</span><span class="success">Promotion / success</span><span class="evidence">Evidence / waiting</span></div></div>
<div class="detail"><b id="detail-title">Select a component</b><em id="detail-subtitle">Click any architecture block</em><p id="detail-copy">Use the controls to walk through the complete lifecycle or select a component for its current NextGen responsibility.</p></div>
<div class="stage"><span class="stage-count" id="stage-count"></span><h2 id="stage-title"></h2><p id="stage-caption"></p></div>
<div class="controls"><button id="prev">Previous</button><button id="play" class="primary">Pause</button><button id="next">Next</button><button id="reset">Reset</button></div><div class="dots" id="dots"></div>
</aside></main>
<script>
const nodes={json.dumps(node_data)};const steps={json.dumps(STAGES)};
let current=0,playing=!matchMedia("(prefers-reduced-motion: reduce)").matches,timer;
const $=id=>document.getElementById(id),nodeEls=[...document.querySelectorAll(".node")],edgeEls=[...document.querySelectorAll(".edge")];
function inspect(id){{const d=nodes[id];if(!d)return;nodeEls.forEach(el=>el.classList.toggle("selected",el.dataset.nodeId===id));$("detail-title").textContent=d.title;$("detail-subtitle").textContent=d.subtitle;$("detail-copy").textContent=d.detail;}}
nodeEls.forEach(el=>{{el.addEventListener("click",()=>{{playing=false;$("play").textContent="Play";stop();inspect(el.dataset.nodeId)}});el.addEventListener("keydown",ev=>{{if(ev.key==="Enter"||ev.key===" "){{ev.preventDefault();el.click()}}}})}});
steps.forEach((_,i)=>{{const b=document.createElement("button");b.className="dot";b.setAttribute("aria-label",`Show stage ${{i+1}}`);b.onclick=()=>{{current=i;render();restart()}};$("dots").appendChild(b)}});
function render(){{const s=steps[current];nodeEls.forEach(el=>{{el.classList.toggle("active",s.nodes.includes(el.dataset.nodeId));el.classList.remove("selected")}});edgeEls.forEach(el=>el.classList.toggle("active",s.edges.includes(el.dataset.edgeId)));$("stage-count").textContent=`Stage ${{current+1}} of ${{steps.length}}`;$("stage-title").textContent=s.title;$("stage-caption").textContent=s.caption;[...$("dots").children].forEach((d,i)=>d.classList.toggle("active",i===current));if(s.nodes.length)inspect(s.nodes[s.nodes.length-1]);}}
function advance(delta=1){{current=(current+delta+steps.length)%steps.length;render()}}function stop(){{clearInterval(timer)}}function restart(){{stop();if(playing)timer=setInterval(()=>advance(),5000)}}
$("prev").onclick=()=>{{advance(-1);restart()}};$("next").onclick=()=>{{advance();restart()}};$("reset").onclick=()=>{{current=0;render();restart()}};$("play").onclick=()=>{{playing=!playing;$("play").textContent=playing?"Pause":"Play";restart()}};
function reportHeight(){{if(!document.documentElement.classList.contains("embedded"))return;const shell=document.querySelector(".shell");parent.postMessage({{type:"contextweaver-atlas-height",height:Math.ceil(shell.getBoundingClientRect().height)}},"*")}}
if(document.documentElement.classList.contains("embedded")){{const shell=document.querySelector(".shell");new ResizeObserver(reportHeight).observe(shell);addEventListener("load",reportHeight);addEventListener("resize",reportHeight)}}
addEventListener("keydown",event=>{{if(event.key!=="Escape"||document.documentElement.classList.contains("embedded"))return;event.preventDefault();if(window.opener&&!window.opener.closed){{window.close();return}}if(history.length>1){{history.back();return}}location.href="../architecture.html#nextgen-atlas"}});
render();restart();
</script></body></html>"""
    (OUT / "contextweaver-nextgen-architecture.html").write_text(html, encoding="utf-8")


def font(size: int, bold: bool = False):
    candidates = [
        Path("C:/Windows/Fonts/Inter-Bold.ttf" if bold else "C:/Windows/Fonts/Inter-Regular.ttf"),
        Path("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def scaled_box(node: Node, scale_x: float, scale_y: float) -> tuple[int, int, int, int]:
    return (
        int(node.x * scale_x),
        int(node.y * scale_y),
        int((node.x + node.w) * scale_x),
        int((node.y + node.h) * scale_y),
    )


def render_image(active_nodes: set[str] | None = None, active_edges: set[str] | None = None,
                 title: str = "", caption: str = "",
                 size: tuple[int, int] = (1600, 960)) -> Image.Image:
    active_nodes = active_nodes or set()
    active_edges = active_edges or set()
    width, height = size
    diagram_height = int(height * 0.82)
    sx, sy = width / 1500, diagram_height / 880
    image = Image.new("RGB", size, COLORS["bg"])
    draw = ImageDraw.Draw(image)
    for x in range(0, width, 50):
        draw.line((x, 0, x, diagram_height), fill="#10231e", width=1)
    for y in range(0, diagram_height, 50):
        draw.line((0, y, width, y), fill="#10231e", width=1)
    draw.text((30, 18), "ContextWeaver NextGen Architecture", fill=COLORS["text"], font=font(26, True))
    draw.text((30, 50), "Cerebro governs. Weave composes. Loom runs anywhere. Evidence follows every stage.",
              fill=COLORS["muted"], font=font(13))
    for label, x, y, w, h, color in GROUPS:
        box = (int(x * sx), int(y * sy), int((x + w) * sx), int((y + h) * sy))
        draw.rounded_rectangle(box, radius=16, fill="#0b1814", outline=COLORS[color], width=2)
        draw.text((box[0] + 12, box[1] + 8), label, fill=COLORS["muted"], font=font(9, True))
    by_id = {n.id: n for n in NODES}
    for edge in EDGES:
        source, target = by_id[edge.source], by_id[edge.target]
        sx0, sy0 = center(source)
        tx0, ty0 = center(target)
        semantic_color = COLORS["violet"] if edge.kind == "governance" else COLORS["amber"] if edge.kind in {"evidence", "waiting"} else COLORS["mint"] if edge.kind == "success" else COLORS["sky"]
        edge_active = edge.id in active_edges
        color = semantic_color if edge_active or not active_edges else "#27413a"
        draw.line(
            (int(sx0 * sx), int(sy0 * sy), int(tx0 * sx), int(ty0 * sy)),
            fill=color,
            width=5 if edge_active else 2,
        )
    for node in NODES:
        box = scaled_box(node, sx, sy)
        active = node.id in active_nodes
        draw.rounded_rectangle(box, radius=13, fill=COLORS["panel2"] if active else COLORS["panel"],
                               outline=COLORS[node.color], width=5 if active else 2)
        tw = draw.textbbox((0, 0), node.title, font=font(12, True))[2]
        draw.text(((box[0] + box[2] - tw) / 2, box[1] + 18), node.title, fill=COLORS["text"], font=font(12, True))
        subtitle_lines = wrap(node.subtitle, width=max(18, node.w // 13))[:2]
        for index, line in enumerate(subtitle_lines):
            lw = draw.textbbox((0, 0), line, font=font(8))[2]
            draw.text(((box[0] + box[2] - lw) / 2, box[1] + 43 + index * 12), line, fill=COLORS["muted"], font=font(8))
    footer_y = diagram_height + 18
    if title:
        draw.text((30, footer_y), title, fill=COLORS["mint"], font=font(22, True))
        for index, line in enumerate(wrap(caption, width=115)[:2]):
            draw.text((30, footer_y + 32 + index * 20), line, fill=COLORS["muted"], font=font(13))
    else:
        draw.text((30, footer_y), "Current product model: Workspaces + Studios -> Cerebro -> Weave -> Runtime -> Loom",
                  fill=COLORS["mint"], font=font(20, True))
        draw.text((30, footer_y + 32), "Offline prototype for review. No website integration has been performed.",
                  fill=COLORS["muted"], font=font(13))
    return image


def write_images() -> None:
    static = render_image()
    static.save(OUT / "contextweaver-nextgen-architecture.png", optimize=True)
    frames = []
    for stage in STAGES:
        frames.append(
            render_image(
                set(stage["nodes"]),
                set(stage["edges"]),
                stage["title"],
                stage["caption"],
                (1200, 720),
            )
        )
    frames[0].save(
        OUT / "contextweaver-nextgen-architecture.gif",
        save_all=True,
        append_images=frames[1:],
        duration=GIF_FRAME_DURATION_MS,
        loop=0,
        optimize=False,
        disposal=2,
    )


PAGES = [
    (
        "Platform Atlas",
        [
            ("Access", "People, APIs, events", 70, 110, 210, 80, "sky"),
            ("Entry + Workspaces + Studios", "My Solutions | MCP, Agent, Workflow, Service, Solution", 330, 110, 300, 80, "mint"),
            ("Cerebro", "Intent, identity, policy, registry, orchestration, evidence", 630, 110, 360, 80, "violet"),
            ("Weave", "Solutions, Services, Workflows, Agents, MCPs, RAG, models, packs", 330, 270, 320, 90, "sky"),
            ("Durable Runtime", "Immutable plans, queues, approvals, retry, compensation", 680, 270, 310, 90, "amber"),
            ("Loom", "Capability Operator, Kubernetes, data, secrets, telemetry, recovery", 330, 450, 660, 100, "violet"),
            ("External systems", "SaaS, APIs, databases, human authorities", 1040, 270, 240, 90, "coral"),
            ("Any cloud", "Azure, AWS, Google, private, sovereign, edge", 1040, 450, 240, 100, "mint"),
        ],
        [(0, 1, "intent"), (1, 2, "typed assets"), (2, 3, "approved capabilities"), (3, 4, "compose"), (4, 6, "tools and evidence"), (2, 5, "desired state"), (5, 7, "deployment profile")],
    ),
    (
        "Build and Promote",
        [
            ("Approved inputs", "Intent, specs, APIs, MCP, code, data", 70, 160, 190, 85, "sky"),
            ("Workspace", "Explore and collaborate", 300, 160, 180, 85, "mint"),
            ("Five contexts", "Create assets + Solutions", 520, 160, 180, 85, "mint"),
            ("Safe Dry Run", "Mocks, faults, evaluation, no side effects", 740, 160, 210, 85, "amber"),
            ("Evidence review", "Quality, cost, policy, security, receipts", 990, 160, 210, 85, "amber"),
            ("Independent approval", "Separation of duties", 990, 330, 210, 85, "violet"),
            ("Immutable Registry", "Version, digest, schemas, compatibility", 740, 330, 210, 85, "coral"),
            ("Capability Operator", "Reconcile approved desired state", 490, 330, 210, 85, "mint"),
            ("Attest + qualify", "Runtime descriptor, synthetic and canary", 260, 330, 190, 85, "sky"),
            ("Active capability", "Discoverable by authorized Services and Solutions", 70, 330, 150, 85, "mint"),
        ],
        [(0, 1, ""), (1, 2, ""), (2, 3, ""), (3, 4, ""), (4, 5, ""), (5, 6, ""), (6, 7, ""), (7, 8, ""), (8, 9, "")],
    ),
    (
        "Governed Runtime",
        [
            ("Request or event", "Identity, tenant, purpose", 60, 150, 190, 85, "sky"),
            ("Policy gate", "Entitlements, risk, approvals", 300, 150, 190, 85, "violet"),
            ("Registry resolution", "Compatible active releases only", 540, 150, 210, 85, "coral"),
            ("Immutable plan", "Exact graph, versions, budget, fallbacks", 800, 150, 220, 85, "violet"),
            ("Durable orchestrator", "Queues, checkpoints, waits, Saga", 1070, 150, 220, 85, "mint"),
            ("Agent branch", "Bounded reasoning and models", 300, 340, 210, 85, "coral"),
            ("RAG branch", "Authorized context and citations", 560, 340, 210, 85, "sky"),
            ("MCP branch", "Tools, adapters, receipts", 820, 340, 210, 85, "sky"),
            ("Human authority", "Approve, reject, modify", 1080, 340, 210, 85, "amber"),
            ("Evidence-backed result", "Result, lineage, traces, receipts, audit", 560, 520, 470, 95, "mint"),
        ],
        [(0, 1, ""), (1, 2, ""), (2, 3, ""), (3, 4, ""), (4, 5, "parallel"), (4, 6, "parallel"), (4, 7, "parallel"), (4, 8, "when required"), (5, 9, ""), (6, 9, ""), (7, 9, ""), (8, 9, "")],
    ),
    (
        "Cloud Deployment",
        [
            ("Git + Registry", "Contracts, images, provenance, policy", 70, 130, 220, 90, "sky"),
            ("MCPEngine CRDs", "Cloud-neutral desired state", 350, 130, 220, 90, "violet"),
            ("Capability Operator", "Watch, reconcile, attest, status", 630, 130, 230, 90, "mint"),
            ("Helm + GitOps", "Versioned deployment profiles", 920, 130, 220, 90, "amber"),
            ("Kubernetes", "Namespaces, identity, network, quotas, probes", 350, 330, 300, 100, "violet"),
            ("Shared substrate", "Database, queues, object, search, cache", 700, 330, 300, 100, "sky"),
            ("Operations", "Secrets, telemetry, backup, recovery, FinOps", 1050, 330, 260, 100, "amber"),
            ("Azure", "AKS and provider adapters", 210, 530, 210, 85, "mint"),
            ("AWS / Google", "EKS, GKE and provider adapters", 540, 530, 230, 85, "mint"),
            ("Private / Sovereign / Edge", "Disconnected and regulated profiles", 890, 530, 270, 85, "mint"),
        ],
        [(0, 1, ""), (1, 2, ""), (2, 3, ""), (3, 4, ""), (4, 5, ""), (5, 6, ""), (4, 7, ""), (4, 8, ""), (4, 9, "")],
    ),
]


def write_drawio() -> None:
    modified = "2026-11-01T00:00:00Z"
    diagrams = []
    palette = {key: (COLORS[key], COLORS[key]) for key in ["mint", "amber", "coral", "violet", "sky"]}
    for page_index, (name, nodes, edges) in enumerate(PAGES, start=1):
        cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
        cells.append(
            f'<mxCell id="title" value="{xml_escape(name)}" style="text;html=1;strokeColor=none;fillColor=none;'
            f'fontSize=18;fontStyle=1;fontColor={COLORS["text"]};" vertex="1" parent="1">'
            f'<mxGeometry x="50" y="35" width="900" height="40" as="geometry"/></mxCell>'
        )
        for index, (title, subtitle, x, y, w, h, color) in enumerate(nodes):
            fill, stroke = palette[color]
            value = f'<b>{html_escape(title)}</b><br><font color="#a8bbb3">{html_escape(subtitle)}</font>'
            value_attr = xml_escape(value, {'"': '&quot;'})
            cells.append(
                f'<mxCell id="n{index}" value="{value_attr}" '
                f'style="rounded=1;whiteSpace=wrap;html=1;fillColor={COLORS["panel"]};strokeColor={stroke};'
                f'fontColor={COLORS["text"]};fontSize=12;strokeWidth=2;" vertex="1" parent="1">'
                f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
            )
        for edge_index, (source, target, label) in enumerate(edges):
            cells.append(
                f'<mxCell id="e{edge_index}" value="{xml_escape(label)}" '
                f'style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;'
                f'endArrow=block;endFill=1;strokeColor={COLORS["sky"]};fontColor={COLORS["muted"]};" '
                f'edge="1" source="n{source}" target="n{target}" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>'
            )
        model = (
            '<mxGraphModel dx="1600" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
            'arrows="1" fold="1" page="1" pageScale="1" pageWidth="1400" pageHeight="800" math="0" shadow="0" '
            f'background="{COLORS["bg"]}"><root>{"".join(cells)}</root></mxGraphModel>'
        )
        diagrams.append(f'<diagram id="page-{page_index}" name="{xml_escape(name)}">{model}</diagram>')
    xml = f'<mxfile host="Electron" modified="{modified}" version="26.0.0">{"".join(diagrams)}</mxfile>'
    (OUT / "contextweaver-nextgen-architecture.drawio").write_text(xml, encoding="utf-8")


def write_readme() -> None:
    content = """# ContextWeaver NextGen Architecture Atlas

Standalone offline prototype inspired by the legacy Cerebro, Weave, and Loom diagrams.

## Files

- `contextweaver-nextgen-architecture.html` - responsive interactive architecture with component inspection and lifecycle controls
- `contextweaver-nextgen-architecture.drawio` - editable four-page source: Platform Atlas, Build and Promote, Governed Runtime, Cloud Deployment
- `contextweaver-nextgen-architecture.svg` - static vector overview
- `contextweaver-nextgen-architecture.png` - static high-resolution preview
- `contextweaver-nextgen-architecture.gif` - eight-stage animation at 1,000 ms per frame

## Current NextGen concepts shown

- One authenticated entry point with Consumer My Solutions, Builder/Admin Studio, and delegated headless access
- Collaborative Workspaces and MCP, Agent, Workflow, Service, and Solution Studio contexts
- Safe Dry Run Lab and evidence review before side effects
- Cerebro intent compilation, identity, entitlements, policy, approvals, Registry, orchestration, and evidence
- Weave Solutions, Services, Workflows, Agents, MCP capabilities, RAG/data products, models, memory, adapters, and solution packs
- Immutable execution plans, durable queues, checkpoints, retries, human approvals, and compensation
- Capability Operator, MCPEngine CRDs, Helm, GitOps, Kubernetes, state, search, events, secrets, telemetry, backup, and recovery
- Azure, AWS, Google Cloud, private, sovereign, and edge deployment profiles

No files in the public website repository were changed by this prototype.
"""
    (OUT / "README.md").write_text(content, encoding="utf-8")


def main(*, skip_raster: bool = False) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    write_svg()
    write_html()
    if not skip_raster:
        write_images()
    write_drawio()
    raster_status = "using committed PNG/GIF assets" if skip_raster else "with regenerated PNG/GIF assets"
    print(f"Generated architecture atlas in {OUT} {raster_status}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skip-raster",
        action="store_true",
        help="Keep committed PNG/GIF assets while regenerating deterministic text and vector outputs.",
    )
    main(skip_raster=parser.parse_args().skip_raster)
