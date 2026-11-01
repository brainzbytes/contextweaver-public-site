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


def svg_icon(node: Node) -> str:
    label = f"{node.id} {node.title}".lower()
    cx = node.x + node.w / 2
    cy = node.y + 23
    if any(word in label for word in ("policy", "approval", "identity", "entitlement")):
        shape = f'<path d="M {cx} {cy - 11} l 10 4 v 8 c 0 7 -4 11 -10 14 c -6 -3 -10 -7 -10 -14 v-8 z"/><path d="M {cx - 4} {cy + 1} l 3 3 l 6 -7"/>'
    elif any(word in label for word in ("evidence", "registry", "solution", "service")):
        shape = f'<rect x="{cx - 9}" y="{cy - 12}" width="18" height="24" rx="2"/><path d="M {cx - 4} {cy - 4} h 8 M {cx - 4} {cy + 1} h 8 M {cx - 4} {cy + 6} h 6"/>'
    elif any(word in label for word in ("mcp", "operator", "orchestrator", "runtime", "operations")):
        shape = f'<circle cx="{cx}" cy="{cy}" r="7"/><circle cx="{cx}" cy="{cy}" r="2.5"/><path d="M {cx} {cy - 12} v 4 M {cx} {cy + 8} v 4 M {cx - 12} {cy} h 4 M {cx + 8} {cy} h 4"/>'
    elif any(word in label for word in ("studio", "compiler", "workflow", "plan")):
        shape = f'<path d="M {cx - 10} {cy - 7} l -6 7 l 6 7 M {cx + 10} {cy - 7} l 6 7 l -6 7 M {cx + 3} {cy - 10} l -6 20"/>'
    elif any(word in label for word in ("user", "people", "workspace", "agent", "human")):
        shape = f'<circle cx="{cx}" cy="{cy - 6}" r="5"/><path d="M {cx - 11} {cy + 11} c 1 -8 6 -11 11 -11 s 10 3 11 11"/>'
    else:
        shape = f'<circle cx="{cx}" cy="{cy}" r="10"/><path d="M {cx - 6} {cy} h 12 M {cx} {cy - 6} v 12"/>'
    return f'<g class="node-icon">{shape}</g>'


def rounded_zone_markup(label: str, x: int, y: int, w: int, h: int, color: str) -> str:
    label_width = min(w - 52, max(220, int(len(label) * 6.3 + 34)))
    face = (
        f"M {x + 30} {y} H {x + w - 26} "
        f"Q {x + w - 8} {y} {x + w - 4} {y + 16} "
        f"L {x + w - 17} {y + h - 17} "
        f"Q {x + w - 20} {y + h} {x + w - 38} {y + h} "
        f"H {x + 24} Q {x + 5} {y + h} {x + 2} {y + h - 17} "
        f"L {x + 14} {y + 17} Q {x + 16} {y} {x + 30} {y} Z"
    )
    depth = (
        f"M {x + 2} {y + h - 17} Q {x + 5} {y + h} {x + 24} {y + h} "
        f"H {x + w - 38} Q {x + w - 20} {y + h} {x + w - 17} {y + h - 17} "
        f"L {x + w - 20} {y + h + 16} Q {x + w - 24} {y + h + 30} {x + w - 42} {y + h + 31} "
        f"L {x + 22} {y + h + 31} Q {x + 4} {y + h + 29} {x} {y + h + 15} Z"
    )
    shadow = (
        f"M {x + 22} {y + h + 18} H {x + w - 30} "
        f"Q {x + w - 12} {y + h + 18} {x + w - 18} {y + h + 36} "
        f"H {x + 18} Q {x} {y + h + 34} {x + 6} {y + h + 20} Z"
    )
    return (
        f'<g class="zone zone-{color}">'
        f'<path class="zone-shadow" d="{shadow}"/>'
        f'<path class="zone-depth" d="{depth}"/>'
        f'<path class="zone-face" d="{face}"/>'
        f'<path class="zone-grid" d="M {x + 45} {y + 17} H {x + w - 38} M {x + 28} {y + h / 2:.1f} H {x + w - 34} '
        f'M {x + w * .28:.1f} {y + 10} L {x + w * .27:.1f} {y + h - 10} M {x + w * .53:.1f} {y + 7} L {x + w * .52:.1f} {y + h - 8} '
        f'M {x + w * .78:.1f} {y + 5} L {x + w * .77:.1f} {y + h - 6}"/>'
        f'<path class="zone-shine" d="M {x + 31} {y + 8} H {x + w - 34}"/>'
        f'<rect class="zone-label-plate" x="{x + 18}" y="{y + 3}" width="{label_width}" height="18" rx="8"/>'
        f'<text x="{x + 28}" y="{y + 16}">{xml_escape(label)}</text></g>'
    )


def studio_module_markup(node: Node) -> str:
    x, y, w, h = node.x, node.y, node.w, node.h
    tile_labels = ("MCP", "AGENT", "FLOW", "SERVICE", "SOLUTION")
    tile_width = 42
    gap = 6
    start_x = x + 13
    tiles = []
    for index, label in enumerate(tile_labels):
        tx = start_x + index * (tile_width + gap)
        tiles.append(
            f'<g class="studio-tile">'
            f'<path class="studio-tile-side" d="M {tx + tile_width - 5} {y + 43} L {tx + tile_width + 2} {y + 48} '
            f'V {y + 75} L {tx + tile_width - 5} {y + 79} Z"/>'
            f'<rect x="{tx}" y="{y + 39}" width="{tile_width}" height="36" rx="8"/>'
            f'<text x="{tx + tile_width / 2:.1f}" y="{y + 61}">{label}</text>'
            f'</g>'
        )
    return (
        f'<g id="node-{node.id}" class="node node-{node.color} studio-module" data-node-id="{node.id}" '
        f'role="button" tabindex="0" aria-label="{xml_escape(node.title)}">'
        f'<rect class="studio-shadow" x="{x - 4}" y="{y + 16}" width="{w + 8}" height="{h - 4}" rx="18"/>'
        f'<path class="studio-tray-depth" d="M {x + 18} {y + h - 8} H {x + w - 10} L {x + w - 20} {y + h + 7} H {x + 28} Z"/>'
        f'<rect class="studio-tray" x="{x}" y="{y + 8}" width="{w}" height="{h - 12}" rx="18"/>'
        f'<rect class="studio-backplate" x="{x + 35}" y="{y}" width="{w - 70}" height="48" rx="12"/>'
        f'<text class="studio-heading" x="{x + w / 2:.1f}" y="{y + 25}">STUDIO</text>'
        f'{"".join(tiles)}'
        f'<g class="node-step"><circle cx="{x + w - 14}" cy="{y + 14}" r="12"/><text class="node-step-number" x="{x + w - 14}" y="{y + 18}"></text></g>'
        f'</g>'
    )


def svg_markup() -> str:
    group_parts = []
    for label, x, y, w, h, color in GROUPS:
        group_parts.append(rounded_zone_markup(label, x, y, w, h, color))
    edge_parts = []
    for edge in EDGES:
        d, lx, ly = edge_path(edge)
        edge_parts.append(
            f'<g id="edge-{edge.id}" class="edge edge-{edge.kind}" data-edge-id="{edge.id}">'
            f'<path class="edge-route" d="{d}" marker-end="url(#arrow)"/>'
            f'<circle class="flow-pulse" r="4"><animateMotion dur="1.8s" repeatCount="indefinite" path="{d}"/></circle>'
            f'<text x="{lx:.1f}" y="{ly:.1f}">{xml_escape(edge.label)}</text></g>'
        )
    node_parts = []
    for node in NODES:
        if node.id == "studios":
            node_parts.append(studio_module_markup(node))
            continue
        lines = wrap(node.subtitle, width=max(18, node.w // 13))[:2]
        subtitle = "".join(
            f'<tspan x="{node.x + node.w / 2:.1f}" dy="{0 if i == 0 else 14}">{xml_escape(line)}</tspan>'
            for i, line in enumerate(lines)
        )
        node_parts.append(
            f'<g id="node-{node.id}" class="node node-{node.color}" data-node-id="{node.id}" '
            f'role="button" tabindex="0" aria-label="{xml_escape(node.title)}">'
            f'<rect class="node-shadow" x="{node.x - 4}" y="{node.y + 8}" width="{node.w + 8}" height="{node.h}" rx="18"/>'
            f'<path class="node-side" d="M {node.x + node.w - 10} {node.y + 12} L {node.x + node.w + 2} {node.y + 20} '
            f'V {node.y + node.h - 10} Q {node.x + node.w + 2} {node.y + node.h} {node.x + node.w - 10} {node.y + node.h + 8} Z"/>'
            f'<path class="node-depth" d="M {node.x + 18} {node.y + node.h - 8} H {node.x + node.w - 10} '
            f'L {node.x + node.w - 20} {node.y + node.h + 10} H {node.x + 28} Z"/>'
            f'<rect class="node-face" x="{node.x}" y="{node.y}" width="{node.w - 10}" height="{node.h - 8}" rx="17"/>'
            f'<path class="node-shine" d="M {node.x + 16} {node.y + 7} H {node.x + node.w - 16}"/>'
            f'{svg_icon(node)}'
            f'<text class="node-title" x="{node.x + (node.w - 10) / 2:.1f}" y="{node.y + 50}">{xml_escape(node.title)}</text>'
            f'<text class="node-subtitle" x="{node.x + (node.w - 10) / 2:.1f}" y="{node.y + 69}">{subtitle}</text>'
            f'<g class="node-step"><circle cx="{node.x + node.w - 14}" cy="{node.y + 14}" r="12"/><text class="node-step-number" x="{node.x + node.w - 14}" y="{node.y + 18}"></text></g>'
            f'</g>'
        )
    return f"""<svg class="architecture" viewBox="0 0 1500 880" role="img" aria-labelledby="diagram-title diagram-desc">
<title id="diagram-title">ContextWeaver NextGen architecture atlas</title>
<desc id="diagram-desc">Current ContextWeaver architecture from collaborative Workspaces and four Studios through Cerebro governance, Weave capabilities, durable runtime, evidence, Capability Operator, and cloud-neutral Loom infrastructure.</desc>
<defs>
  <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="context-stroke"/></marker>
  <filter id="glow"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="zone-glow" x="-20%" y="-30%" width="140%" height="180%"><feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#70e6b1" flood-opacity=".2"/><feDropShadow dx="0" dy="12" stdDeviation="10" flood-color="#000000" flood-opacity=".65"/></filter>
  <filter id="card-shadow" x="-30%" y="-30%" width="160%" height="180%"><feDropShadow dx="0" dy="9" stdDeviation="8" flood-color="#000000" flood-opacity=".58"/></filter>
  <linearGradient id="glass-face" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#173f2e" stop-opacity=".96"/><stop offset=".48" stop-color="#10261d" stop-opacity=".94"/><stop offset="1" stop-color="#07110d" stop-opacity=".98"/></linearGradient>
  <linearGradient id="zone-face" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#173429" stop-opacity=".5"/><stop offset=".55" stop-color="#0a1812" stop-opacity=".72"/><stop offset="1" stop-color="#07110d" stop-opacity=".9"/></linearGradient>
  <linearGradient id="zone-mint" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#174936" stop-opacity=".76"/><stop offset=".58" stop-color="#0b251a" stop-opacity=".82"/><stop offset="1" stop-color="#07110d" stop-opacity=".94"/></linearGradient>
  <linearGradient id="zone-forest" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#123522" stop-opacity=".78"/><stop offset=".58" stop-color="#091c12" stop-opacity=".86"/><stop offset="1" stop-color="#050d08" stop-opacity=".96"/></linearGradient>
  <linearGradient id="zone-moss" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#263d1c" stop-opacity=".72"/><stop offset=".58" stop-color="#142511" stop-opacity=".84"/><stop offset="1" stop-color="#071008" stop-opacity=".96"/></linearGradient>
  <linearGradient id="zone-amber" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a3015" stop-opacity=".68"/><stop offset=".58" stop-color="#211b0d" stop-opacity=".82"/><stop offset="1" stop-color="#0d0b06" stop-opacity=".96"/></linearGradient>
  <pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse"><path d="M50 0H0V50" fill="none" stroke="#38544a" stroke-width="1" opacity=".23"/></pattern>
</defs>
<rect width="1500" height="880" fill="#07110f"/><rect y="70" width="1500" height="810" fill="url(#grid)" opacity=".72"/>
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
.zone{filter:url(#zone-glow)}.zone-shadow{fill:#000;opacity:.58}.zone-face{fill:url(#zone-face);stroke:#70e6b1;stroke-width:1.6}.zone-depth{fill:#030d09;stroke:#70e6b1;stroke-width:1.1}.zone-grid{fill:none;stroke:#70e6b1;stroke-width:.65;opacity:.1}.zone-shine{fill:none;stroke:#b4ffda;stroke-width:1.2;opacity:.62}.zone-label-plate{fill:#07110f;fill-opacity:.94;stroke:#70e6b1;stroke-width:.75}.zone text{fill:#d8fff0;font:800 10px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;letter-spacing:1.2px}
.zone-mint .zone-face{fill:url(#zone-mint);stroke:#70e6b1}.zone-violet .zone-face{fill:url(#zone-forest);stroke:#9bcf9f}.zone-sky .zone-face{fill:url(#zone-moss);stroke:#52b788}.zone-amber .zone-face{fill:url(#zone-amber);stroke:#ffc76a}
.node{filter:url(#card-shadow)}.node-shadow{fill:#000;opacity:.54}.node-face{fill:url(#glass-face);stroke:#70e6b1;stroke-width:2}.node-side{fill:#06130d;stroke:#70e6b1;stroke-width:1.1}.node-depth{fill:#030806;stroke:#70e6b1;stroke-width:1.2}.node-shine{fill:none;stroke:#b4ffda;stroke-width:1.1;opacity:.66}.node-mint .node-face{stroke:#70e6b1}.node-amber .node-face{stroke:#ffc76a}.node-coral .node-face{stroke:#7fb98d}.node-violet .node-face{stroke:#9bcf9f}.node-sky .node-face{stroke:#52b788}
.studio-shadow{fill:#000;opacity:.58}.studio-tray{fill:url(#glass-face);stroke:#70e6b1;stroke-width:2}.studio-tray-depth{fill:#030806;stroke:#70e6b1;stroke-width:1.2}.studio-backplate{fill:#123c2b;fill-opacity:.95;stroke:#8af5bd;stroke-width:1.6}.studio-heading{fill:#e8fff4;font:900 11px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;letter-spacing:2px;text-anchor:middle}.studio-tile rect{fill:#0b2118;stroke:#70e6b1;stroke-width:1.2}.studio-tile-side{fill:#030806;stroke:#4aa979;stroke-width:.8}.studio-tile text{fill:#d8fff0;font:800 5.5px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;text-anchor:middle}
.node-icon{fill:none;stroke:#d8fff0;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}.node-title{fill:#f4f8f2;font:700 12px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;text-anchor:middle}.node-subtitle{fill:#a8cbbd;font:8px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;text-anchor:middle}
.node-step{opacity:0}.node-step circle{fill:#07110f;stroke:#70e6b1;stroke-width:2}.node-step text{fill:#70e6b1;font:800 10px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;text-anchor:middle}
.edge{opacity:.32}.edge .edge-route{fill:none;stroke:#52b788;stroke-width:2}.flow-pulse{fill:#70e6b1;opacity:0;filter:url(#glow)}.edge text{fill:#a8bbb3;font:8px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;text-anchor:middle;paint-order:stroke;stroke:#07110f;stroke-width:4}
.edge-governance .edge-route{stroke:#ffc76a;stroke-dasharray:8 6}.edge-governance .flow-pulse,.edge-waiting .flow-pulse{fill:#ffc76a}.edge-success .edge-route{stroke:#70e6b1}.edge-evidence .edge-route{stroke:#d8fff0;stroke-dasharray:3 7}.edge-evidence .flow-pulse{fill:#d8fff0}.edge-waiting .edge-route{stroke:#ffc76a;stroke-dasharray:10 7}
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
*{{box-sizing:border-box}}html{{color-scheme:dark}}body{{min-width:320px;margin:0;overflow-x:hidden;color:var(--text);background:var(--bg);font:14px/1.5 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
.shell{{display:grid;grid-template-rows:auto minmax(0,1fr) auto;width:min(1600px,100%);min-height:100dvh;margin:auto;border:1px solid var(--line);background:linear-gradient(180deg,#0b1c15,#050b08);box-shadow:0 34px 100px #0009;overflow:hidden}}
.storybar{{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:center;gap:24px;min-height:92px;padding:14px 20px;border-bottom:1px solid var(--line);background:#091710eb;backdrop-filter:blur(20px)}}
.storybar>div,.detailbar>div{{min-width:0}}.stage-count{{color:var(--mint);font-size:9px;font-weight:900;letter-spacing:.15em;text-transform:uppercase}}.stage-title{{display:block;margin-top:4px;font:700 clamp(18px,2vw,29px)/1.08 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;letter-spacing:-.025em}}.stage-caption{{display:block;max-width:1080px;margin-top:6px;overflow-wrap:anywhere;color:var(--muted);font-size:11px}}
.canvas{{position:relative;min-height:620px;overflow:auto;background:radial-gradient(circle at 55% 42%,#173f2e44 0,transparent 40%),var(--bg)}}.architecture{{display:block;min-width:1120px;width:100%;height:auto}}
.diagram-title{{fill:#f4f8f2;font:700 25px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}.diagram-subtitle{{fill:#a8bbb3;font:12px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
.zone{{filter:url(#zone-glow)}}.zone-shadow{{fill:#000;opacity:.58}}.zone-face{{fill:url(#zone-face);stroke:#70e6b1;stroke-width:1.6}}.zone-depth{{fill:#030d09;stroke:#70e6b1;stroke-width:1.1}}.zone-grid{{fill:none;stroke:#70e6b1;stroke-width:.65;opacity:.1}}.zone-shine{{fill:none;stroke:#b4ffda;stroke-width:1.2;opacity:.62}}.zone-label-plate{{fill:#07110f;fill-opacity:.94;stroke:#70e6b1;stroke-width:.75}}.zone text{{fill:#d8fff0;font:800 10px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;letter-spacing:1.2px}}
.zone-mint .zone-face{{fill:url(#zone-mint);stroke:#70e6b1}}.zone-violet .zone-face{{fill:url(#zone-forest);stroke:#9bcf9f}}.zone-sky .zone-face{{fill:url(#zone-moss);stroke:#52b788}}.zone-amber .zone-face{{fill:url(#zone-amber);stroke:#ffc76a}}
.node{{cursor:pointer;filter:url(#card-shadow);transition:opacity .35s}}.node-shadow{{fill:#000;opacity:.54}}.node-face{{fill:url(#glass-face);stroke:#70e6b1;stroke-width:2;transition:.3s}}.node-side{{fill:#06130d;stroke:#70e6b1;stroke-width:1.1;transition:.3s}}.node-depth{{fill:#030806;stroke:#70e6b1;stroke-width:1.2;transition:.3s}}.node-shine{{fill:none;stroke:#b4ffda;stroke-width:1.1;opacity:.66}}.node-mint .node-face{{stroke:#70e6b1}}.node-amber .node-face{{stroke:#ffc76a}}.node-coral .node-face{{stroke:#7fb98d}}.node-violet .node-face{{stroke:#9bcf9f}}.node-sky .node-face{{stroke:#52b788}}
.studio-shadow{{fill:#000;opacity:.58}}.studio-tray{{fill:url(#glass-face);stroke:#70e6b1;stroke-width:2;transition:.3s}}.studio-tray-depth{{fill:#030806;stroke:#70e6b1;stroke-width:1.2;transition:.3s}}.studio-backplate{{fill:#123c2b;fill-opacity:.95;stroke:#8af5bd;stroke-width:1.6;transition:.3s}}.studio-heading{{fill:#e8fff4;font:900 11px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;letter-spacing:2px;text-anchor:middle}}.studio-tile rect{{fill:#0b2118;stroke:#70e6b1;stroke-width:1.2;transition:.3s}}.studio-tile-side{{fill:#030806;stroke:#4aa979;stroke-width:.8}}.studio-tile text{{fill:#d8fff0;font:800 5.5px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;text-anchor:middle}}
.node-icon{{fill:none;stroke:#d8fff0;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}}.node-title{{fill:#f4f8f2;font:700 12px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;text-anchor:middle}}.node-subtitle{{fill:#a8cbbd;font:8px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;text-anchor:middle}}
.node-step{{opacity:0}}.node-step circle{{fill:#07110f;stroke:#70e6b1;stroke-width:2}}.node-step text{{fill:#70e6b1;font:800 10px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;text-anchor:middle}}
.node:hover .node-face,.node.selected .node-face,.node:hover .studio-tray,.node.selected .studio-tray{{stroke-width:4}}.node.active .node-face,.node.active .studio-tray{{stroke-width:5;filter:url(#glow)}}.node.active .node-depth,.node.active .node-side,.node.active .studio-tray-depth{{stroke:var(--mint)}}.node.active .studio-backplate,.node.active .studio-tile rect{{stroke:#b4ffda;filter:url(#glow)}}.node.active .node-step{{opacity:1}}.node.complete{{opacity:.72}}.node.dim{{opacity:.42}}
.edge{{opacity:.24;transition:opacity .35s}}.edge .edge-route{{fill:none;stroke:#52b788;stroke-width:2}}.flow-pulse{{fill:#70e6b1;opacity:0;filter:url(#glow)}}.edge text{{fill:#a8bbb3;font:8px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;text-anchor:middle;paint-order:stroke;stroke:#07110f;stroke-width:4}}
.edge-governance .edge-route{{stroke:#ffc76a;stroke-dasharray:8 6}}.edge-governance .flow-pulse,.edge-waiting .flow-pulse{{fill:#ffc76a}}.edge-success .edge-route{{stroke:#70e6b1}}.edge-evidence .edge-route{{stroke:#d8fff0;stroke-dasharray:3 7}}.edge-evidence .flow-pulse{{fill:#d8fff0}}.edge-waiting .edge-route{{stroke:#ffc76a;stroke-dasharray:10 7}}
.edge.complete{{opacity:.52}}.edge.dim{{opacity:.14}}.edge.active{{opacity:1}}.edge.active .edge-route{{stroke-width:5;stroke-dasharray:14 9;animation:flow .8s linear infinite;filter:url(#glow)}}.edge.active .flow-pulse{{opacity:1}}.edge-governance.active .edge-route{{stroke:var(--amber)}}.edge-evidence.active .edge-route{{stroke:#d8fff0;stroke-dasharray:3 8}}@keyframes flow{{to{{stroke-dashoffset:-23}}}}
.trust-label{{fill:#ffc76a;font:700 10px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
.controls{{display:flex;gap:7px}}button{{min-height:39px;padding:0 13px;border:1px solid var(--line);border-radius:9px;color:var(--text);background:var(--panel);cursor:pointer;font:800 10px Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}button:hover{{border-color:var(--mint)}}button:focus-visible,.node:focus-visible{{outline:3px solid var(--mint);outline-offset:3px}}button.primary{{color:#07110f;background:var(--mint)}}
.detailbar{{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:center;gap:24px;min-height:88px;padding:13px 20px;border-top:1px solid var(--line);background:#07110d}}.detailbar b{{display:block;font:700 15px/1.2 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}.detailbar em{{display:block;margin:3px 0;color:var(--amber);font-size:9px;font-style:normal;font-weight:800}}.detailbar p{{margin:0;color:#c8d6d0;font-size:10px}}.legend{{display:flex;flex-wrap:wrap;gap:12px;margin-top:7px;color:var(--muted);font-size:8px}}.legend span::before{{content:"";display:inline-block;width:10px;height:3px;margin-right:5px;vertical-align:middle;background:var(--mint)}}.legend .gov::before{{background:var(--amber)}}.legend .success::before{{background:var(--mint)}}.legend .evidence::before{{background:#d8fff0}}
.dots{{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:7px}}.dot{{width:11px;height:11px;min-height:0;padding:0;border:0;border-radius:50%;background:var(--line)}}.dot.complete{{background:#456e5d}}.dot.active{{background:var(--mint);box-shadow:0 0 10px var(--mint)}}
html.embedded .shell{{min-height:0;border:0;box-shadow:none}}html.embedded .canvas{{overflow:hidden}}html.embedded .architecture{{min-width:0;width:100%}}
@media(max-width:980px){{.shell{{min-height:auto}}.storybar{{grid-template-columns:1fr}}.controls{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));width:100%}}.controls button{{min-width:0;padding-inline:8px}}.detailbar{{grid-template-columns:1fr}}.dots{{justify-content:flex-start}}.canvas{{min-height:0;overflow:hidden}}.architecture{{min-width:0;width:100%}}}}
@media(max-width:620px){{.shell{{border-width:0}}.storybar,.detailbar{{padding:14px}}.controls{{grid-template-columns:repeat(2,minmax(0,1fr))}}.stage-title{{font-size:18px}}.stage-caption{{font-size:10px}}}}
@media(prefers-reduced-motion:reduce){{*{{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}}}
</style></head><body><main class="shell" aria-live="polite">
<header class="storybar"><div><span class="stage-count" id="stage-count"></span><strong class="stage-title" id="stage-title"></strong><span class="stage-caption" id="stage-caption"></span></div><div class="controls"><button id="prev">Previous</button><button id="play" class="primary">Pause</button><button id="next">Next</button><button id="reset">Reset</button></div></header>
<section class="canvas">{svg_markup()}</section>
<footer class="detailbar"><div><b id="detail-title">Select a component</b><em id="detail-subtitle">Click any glass architecture block</em><p id="detail-copy">Walk the lifecycle or inspect a component. Only the current route moves; completed stages remain subtly visible.</p><div class="legend"><span>Intent / execution</span><span class="gov">Governance / approval</span><span class="success">Promotion / success</span><span class="evidence">Evidence return</span></div></div><div class="dots" id="dots"></div></footer>
</main>
<script>
const nodes={json.dumps(node_data)};const steps={json.dumps(STAGES)};
let current=0,playing=!matchMedia("(prefers-reduced-motion: reduce)").matches,timer;
const $=id=>document.getElementById(id),nodeEls=[...document.querySelectorAll(".node")],edgeEls=[...document.querySelectorAll(".edge")];
function inspect(id){{const d=nodes[id];if(!d)return;nodeEls.forEach(el=>el.classList.toggle("selected",el.dataset.nodeId===id));$("detail-title").textContent=d.title;$("detail-subtitle").textContent=d.subtitle;$("detail-copy").textContent=d.detail;}}
nodeEls.forEach(el=>{{el.addEventListener("click",()=>{{playing=false;$("play").textContent="Play";stop();inspect(el.dataset.nodeId)}});el.addEventListener("keydown",ev=>{{if(ev.key==="Enter"||ev.key===" "){{ev.preventDefault();el.click()}}}})}});
steps.forEach((_,i)=>{{const b=document.createElement("button");b.className="dot";b.setAttribute("aria-label",`Show stage ${{i+1}}`);b.onclick=()=>{{current=i;render();restart()}};$("dots").appendChild(b)}});
function render(){{const s=steps[current],done=steps.slice(0,current),doneNodes=new Set(done.flatMap(step=>step.nodes)),doneEdges=new Set(done.flatMap(step=>step.edges));nodeEls.forEach(el=>{{const id=el.dataset.nodeId,active=s.nodes.includes(id),complete=doneNodes.has(id)&&!active;el.classList.toggle("active",active);el.classList.toggle("complete",complete);el.classList.toggle("dim",!active&&!complete);el.classList.remove("selected");const number=el.querySelector(".node-step-number");if(number)number.textContent=active?String(s.nodes.indexOf(id)+1):""}});edgeEls.forEach(el=>{{const id=el.dataset.edgeId,active=s.edges.includes(id),complete=doneEdges.has(id)&&!active;el.classList.toggle("active",active);el.classList.toggle("complete",complete);el.classList.toggle("dim",!active&&!complete)}});$("stage-count").textContent=`Current flow · stage ${{current+1}} of ${{steps.length}}`;$("stage-title").textContent=s.title;$("stage-caption").textContent=s.caption;[...$("dots").children].forEach((d,i)=>{{d.classList.toggle("active",i===current);d.classList.toggle("complete",i<current)}});if(s.nodes.length)inspect(s.nodes[s.nodes.length-1]);}}
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
    zone_fills = {
        "mint": "#123b2b",
        "violet": "#0e291b",
        "sky": "#1c3018",
        "amber": "#302711",
    }
    for label, x, y, w, h, color in GROUPS:
        box = (int(x * sx), int(y * sy), int((x + w) * sx), int((y + h) * sy))
        depth = max(10, int(16 * sy))
        radius = max(12, int(22 * sy))
        draw.rounded_rectangle(
            (box[0] + 4, box[1] + depth + 8, box[2] - 4, box[3] + depth + 8),
            radius=radius,
            fill="#010503",
        )
        draw.rounded_rectangle(
            (box[0], box[1] + depth, box[2], box[3] + depth),
            radius=radius,
            fill="#030806",
            outline=COLORS["line"],
            width=2,
        )
        draw.rounded_rectangle(
            box,
            radius=radius,
            fill=zone_fills[color],
            outline=COLORS[color],
            width=2,
        )
        draw.line((box[0] + depth * 2, box[1] + 7, box[2] - depth * 2, box[1] + 7), fill="#315f4c", width=1)
        label_width = min(box[2] - box[0] - 40, max(180, int(len(label) * 5.5 + 28)))
        label_plate = (box[0] + 10, box[1] + 2, box[0] + 10 + label_width, box[1] + 20)
        draw.rounded_rectangle(label_plate, radius=8, fill=COLORS["bg"], outline=COLORS[color], width=1)
        draw.text((box[0] + 20, box[1] + 6), label, fill=COLORS["text"], font=font(8, True))
    by_id = {n.id: n for n in NODES}
    for edge in EDGES:
        source, target = by_id[edge.source], by_id[edge.target]
        sx0, sy0 = center(source)
        tx0, ty0 = center(target)
        semantic_color = COLORS["amber"] if edge.kind in {"governance", "waiting"} else "#d8fff0" if edge.kind == "evidence" else COLORS["mint"]
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
        depth = max(7, int(9 * sy))
        if node.id == "studios":
            radius = max(10, int(16 * sy))
            draw.rounded_rectangle(
                (box[0] - 4, box[1] + depth + 5, box[2] + 4, box[3] + depth),
                radius=radius,
                fill="#010503",
            )
            draw.rounded_rectangle(
                (box[0], box[1] + depth, box[2], box[3]),
                radius=radius,
                fill=COLORS["panel"],
                outline=COLORS["mint"],
                width=5 if active else 2,
            )
            plate = (
                box[0] + int(35 * sx),
                box[1],
                box[2] - int(35 * sx),
                box[1] + int(48 * sy),
            )
            draw.rounded_rectangle(
                plate,
                radius=max(7, int(12 * sy)),
                fill="#123c2b",
                outline="#8af5bd",
                width=3 if active else 2,
            )
            studio_label = "STUDIO"
            studio_font = font(10, True)
            studio_width = draw.textbbox((0, 0), studio_label, font=studio_font)[2]
            draw.text(((plate[0] + plate[2] - studio_width) / 2, plate[1] + 7), studio_label,
                      fill="#e8fff4", font=studio_font)
            tile_labels = ("MCP", "AGT", "FLOW", "SVC", "SOL")
            tile_width = int(42 * sx)
            tile_gap = int(6 * sx)
            tile_x = box[0] + int(13 * sx)
            tile_y = box[1] + int(39 * sy)
            tile_bottom = box[1] + int(75 * sy)
            for label in tile_labels:
                tile_box = (tile_x, tile_y, tile_x + tile_width, tile_bottom)
                draw.rounded_rectangle(
                    tile_box,
                    radius=max(5, int(8 * sy)),
                    fill="#0b2118",
                    outline="#b4ffda" if active else COLORS["mint"],
                    width=2,
                )
                label_font = font(6, True)
                label_width = draw.textbbox((0, 0), label, font=label_font)[2]
                draw.text(((tile_box[0] + tile_box[2] - label_width) / 2, tile_box[1] + 9),
                          label, fill="#d8fff0", font=label_font)
                tile_x += tile_width + tile_gap
            continue
        front = (box[0], box[1], box[2] - depth, box[3] - depth)
        draw.rounded_rectangle(
            (box[0] - 4, box[1] + 7, box[2] + 3, box[3] + depth),
            radius=max(10, int(17 * sy)),
            fill="#010503",
        )
        draw.polygon(
            [(front[2] - 2, front[1] + depth), (box[2], front[1] + depth * 2),
             (box[2], box[3] - depth), (front[2] - 2, box[3])],
            fill="#06130d",
            outline=COLORS[node.color] if active else COLORS["line"],
        )
        draw.polygon(
            [(front[0] + depth, front[3]), (front[2], front[3]), (box[2] - depth, box[3]), (box[0] + depth * 2, box[3])],
            fill="#030806",
            outline=COLORS[node.color] if active else COLORS["line"],
        )
        draw.rounded_rectangle(front, radius=13, fill=COLORS["panel2"] if active else COLORS["panel"],
                               outline=COLORS[node.color], width=5 if active else 2)
        draw.line((front[0] + 14, front[1] + 7, front[2] - 14, front[1] + 7), fill="#4b8a6e", width=1)
        tw = draw.textbbox((0, 0), node.title, font=font(12, True))[2]
        draw.text(((front[0] + front[2] - tw) / 2, front[1] + 18), node.title, fill=COLORS["text"], font=font(12, True))
        subtitle_lines = wrap(node.subtitle, width=max(18, node.w // 13))[:2]
        for index, line in enumerate(subtitle_lines):
            lw = draw.textbbox((0, 0), line, font=font(8))[2]
            draw.text(((front[0] + front[2] - lw) / 2, front[1] + 43 + index * 12), line, fill=COLORS["muted"], font=font(8))
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
                f'style="rounded=1;whiteSpace=wrap;html=1;shadow=1;glass=1;fillColor={COLORS["panel"]};gradientColor={COLORS["panel2"]};gradientDirection=north;strokeColor={stroke};'
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
