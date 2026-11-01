from __future__ import annotations

import argparse
import base64
import json
import math
import textwrap
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from html import escape
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "diagrams"
OUT.mkdir(parents=True, exist_ok=True)

WIDTH = 1536
HEIGHT = 1024
GIF_FRAME_DURATION_MS = 1000
IMAGE_MASTER_WIDTH = 1536
IMAGE_MASTER_HEIGHT = 1024

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
    "danger": "#ff7188",
}

FONT_STACK = 'Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'


def clean_generated_text(value: str) -> str:
    return "\n".join(line.rstrip() for line in value.splitlines()) + "\n"


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
    color: str = "mint"


@dataclass(frozen=True)
class Edge:
    id: str
    source: str
    target: str
    label: str = ""
    kind: str = "data"


@dataclass(frozen=True)
class Step:
    title: str
    caption: str
    nodes: tuple[str, ...]
    edges: tuple[str, ...]


@dataclass(frozen=True)
class Diagram:
    slug: str
    title: str
    subtitle: str
    nodes: tuple[Node, ...]
    edges: tuple[Edge, ...]
    steps: tuple[Step, ...]


@dataclass(frozen=True)
class ImageFirstConfig:
    master: Path
    hotspots: dict[str, tuple[int, int, int]]
    route_overrides: dict[str, tuple[tuple[int, int], ...]]


def n(id_: str, title: str, subtitle: str, detail: str, x: int, y: int, w: int, h: int, color: str = "mint") -> Node:
    return Node(id_, title, subtitle, detail, x, y, w, h, color)


def e(id_: str, source: str, target: str, label: str = "", kind: str = "data") -> Edge:
    return Edge(id_, source, target, label, kind)


DIAGRAMS = (
    Diagram(
        "intent-to-evidence",
        "Intent to Evidence",
        "One governed path turns an authenticated request into a proven, reusable outcome.",
        (
            n("intent", "Intent", "Authenticated request", "A person or delegated client submits a bounded request with current identity, tenant, purpose, and authority.", 40, 400, 120, 90, "mint"),
            n("solution", "Solution", "User-facing composition", "The requested experience resolves a published Solution action without inventing a separate runtime primitive.", 190, 400, 120, 90, "mint"),
            n("service", "Service", "Reusable executable contract", "The Solution action resolves an approved reusable Service and its eligible Workflow contracts.", 340, 400, 120, 90, "mint"),
            n("cerebro", "Cerebro", "Compile · identity · policy", "Cerebro normalizes intent, resolves identity and entitlement, selects exact versions, and authorizes the complete reachable graph.", 625, 360, 190, 140, "mint"),
            n("workflow", "Workflow", "Durable coordination", "A typed Workflow coordinates state, waits, retries, parallel branches, approvals, and compensation.", 840, 400, 120, 90, "mint"),
            n("agents", "Agents", "Bounded reasoning", "Specialist Agents perform bounded reasoning over only the context and tools approved for their task.", 975, 345, 120, 90, "mint"),
            n("mcp", "MCP", "Governed capabilities", "MCP gateways invoke approved capabilities with scoped credentials that are never exposed to Agents.", 975, 490, 120, 90, "mint"),
            n("systems", "Enterprise systems", "Approved side effects", "Enterprise systems receive schema-valid, policy-authorized operations through governed capability gateways.", 1115, 400, 135, 90, "mint"),
            n("approval", "Approval gate", "Independent authority", "Consequential actions pause for an independent decision bound to the exact action hash.", 1135, 315, 105, 90, "amber"),
            n("evidence", "Evidence", "Receipts · lineage · evaluation", "The run binds artifacts, citations, policy decisions, approvals, provider receipts, logs, traces, and evaluations.", 1260, 400, 120, 90, "mint"),
            n("outcome", "Outcome", "Useful · approved · provable", "The canonical result returns through the Solution experience with the evidence needed to operate, audit, and improve it.", 1400, 400, 110, 90, "mint"),
            n("history", "Run history", "Operate and learn", "Evidence-backed run history supports investigation, regression analysis, lifecycle decisions, and continuous improvement.", 40, 185, 145, 100, "mint"),
        ),
        (
            e("i1", "intent", "solution", "resolve"),
            e("i2", "solution", "service", "select"),
            e("i3", "service", "cerebro", "compile", "governance"),
            e("i4", "cerebro", "workflow", "immutable plan", "governance"),
            e("i5", "workflow", "agents", "parallel task"),
            e("i6", "workflow", "mcp", "capability call"),
            e("i7", "agents", "systems", "typed artifact"),
            e("i8", "mcp", "systems", "approved operation"),
            e("i9", "systems", "approval", "consequential action", "waiting"),
            e("i10", "systems", "evidence", "receipts", "evidence"),
            e("i11", "evidence", "outcome", "prove", "success"),
            e("i12", "outcome", "history", "operate + learn", "evidence"),
        ),
        (
            Step("Start with authenticated intent", "A person or delegated client enters through an approved channel with identity, tenant, purpose, and current authority attached.", ("intent", "solution"), ("i1",)),
            Step("Resolve the reusable contract", "The Solution action selects an approved Service instead of hiding execution inside a one-off prompt or experience.", ("solution", "service"), ("i2",)),
            Step("Compile and authorize the graph", "Cerebro validates intent, identity, entitlement, exact versions, data scope, tools, side effects, and policy before dispatch.", ("service", "cerebro"), ("i3",)),
            Step("Create an immutable execution plan", "The approved Service resolves a durable Workflow with pinned capabilities, budgets, policy decisions, and evidence requirements.", ("cerebro", "workflow"), ("i4",)),
            Step("Run reasoning and capabilities in parallel", "Bounded Agents and MCP gateways execute their typed branches without giving provider credentials to Agents.", ("workflow", "agents", "mcp"), ("i5", "i6")),
            Step("Reach enterprise systems safely", "Typed Agent artifacts and authorized MCP operations converge at enterprise systems through governed boundaries.", ("agents", "mcp", "systems"), ("i7", "i8")),
            Step("Pause for independent approval", "Consequential work waits durably for an approver who is distinct from the requester and sees the exact proposed action.", ("systems", "approval"), ("i9",)),
            Step("Bind evidence to the result", "Receipts, lineage, citations, policy, approvals, logs, traces, and evaluation become part of the canonical run record.", ("systems", "evidence"), ("i10",)),
            Step("Return a proven outcome", "The user-facing Solution receives a useful approved outcome with proof attached rather than a bare model response.", ("evidence", "outcome"), ("i11",)),
            Step("Operate, investigate, and improve", "Run history closes the lifecycle with evidence-driven operations, regression investigation, and governed improvement.", ("outcome", "history"), ("i12",)),
        ),
    ),
    Diagram(
        "service-factory",
        "Universal Solution and Capability Factory",
        "Approved inputs become reusable capabilities and Services that compose into governed, user-facing Solutions.",
        (
            n("inputs", "Product inputs", "Specs · APIs · wiki · data · code", "Start from a described outcome, RFC, OpenAPI or AsyncAPI document, existing MCP server, repository, enterprise source, data product, or industry pack.", 36, 145, 180, 110, "sky"),
            n("studio", "Unified Studio", "MCP · Agent · Workflow · Service · Solution", "Guide non-programmers through five governed contexts while preserving complete specifications, schemas, dependency graphs, code, tests, configuration references, and deployment assets for engineers.", 260, 145, 190, 110, "mint"),
            n("contracts", "Typed contracts", "MCP · Agent · Workflow · Service · Solution", "Normalize identity, ownership, inputs, outputs, errors, side effects, dependencies, policies, data classes, SLOs, experience actions, evaluations, and support.", 494, 145, 180, 110, "violet"),
            n("admission", "Admission pipeline", "Test · scan · SBOM · sign · approve", "Validate behavior and compatibility; scan package, code, dependencies, image, secrets, malware, and licenses; bind provenance and independent approval.", 718, 145, 190, 110, "amber"),
            n("registry", "Immutable Registry", "Candidate · canary · active", "Publish exact versioned contracts and release digests. Discovery is filtered by identity, policy, trust, lifecycle, compatibility, health, region, and residency.", 952, 145, 210, 110, "coral"),
            n("operator", "Capability Operator", "Kubernetes · Helm · GitOps", "Reconcile only an approved desired state into isolated runtime identity, network, quota, configuration, probes, queues, observability, and digest-pinned workloads.", 82, 355, 205, 110, "mint"),
            n("discovery", "Runtime discovery", "Attest · inspect · qualify", "Compare the live descriptor to the signed release, discover Agent or MCP operations, evaluate synthetic and canary traffic, and promote the logical alias.", 337, 355, 205, 110, "sky"),
            n("compose", "Solution + Service resolution", "Experience action · compile · authorize", "Resolve a published Solution action to an approved reusable Service and Workflow, or constrained-compose only admitted capabilities. Validate bindings, policy, approval, budgets, fallbacks, and the complete graph.", 592, 355, 205, 110, "violet"),
            n("execute", "Governed Service Run", "Agents · MCPs · RAG · humans", "Commit an immutable plan, dispatch typed work, run parallel branches, wait durably, invoke tools through gateways, retry safely, and compensate when required.", 847, 355, 205, 110, "amber"),
            n("outcome", "Solution result + proof", "Experience · citations · receipts · evidence", "Present the typed result through the Solution experience with lineage, approvals, policy decisions, release identity, tool receipts, artifacts, metrics, logs, traces, evaluations, and audit references.", 486, 548, 228, 112, "mint"),
        ),
        (
            e("f1", "inputs", "studio", "ingest"),
            e("f2", "studio", "contracts", "generate + edit"),
            e("f3", "contracts", "admission", "validate", "governance"),
            e("f4", "admission", "registry", "admit", "governance"),
            e("f5", "registry", "operator", "approved release", "success"),
            e("f6", "operator", "discovery", "live runtime"),
            e("f7", "discovery", "registry", "promote", "success"),
            e("f8", "registry", "compose", "discover"),
            e("f9", "compose", "execute", "immutable plan", "governance"),
            e("f10", "execute", "outcome", "finalize", "success"),
            e("f11", "outcome", "registry", "health + learning", "evidence"),
        ),
        (
            Step("Bring approved raw material", "Import or describe the desired outcome and the information, systems, and standards it may use.", ("inputs", "studio"), ("f1",)),
            Step("Create inspectable assets", "The Studio produces editable contracts and implementation assets rather than hiding behavior inside a prompt.", ("studio", "contracts"), ("f2",)),
            Step("Prove the release", "Tests, security scanning, SBOM, provenance, compatibility, policy, and human approval bind one immutable release.", ("contracts", "admission", "registry"), ("f3", "f4")),
            Step("Deploy through governed desired state", "The Capability Operator creates only the identity, network, secrets, resources, and runtime declared by the approved profile.", ("registry", "operator", "discovery"), ("f5", "f6")),
            Step("Attest and publish discovery", "The live runtime must match the signed release and pass qualification before its logical capability alias becomes active.", ("discovery", "registry"), ("f7",)),
            Step("Resolve the Solution action", "Cerebro maps the user-facing experience action to an approved Service, resolves exact compatible capabilities, validates the graph, and freezes an immutable execution plan.", ("registry", "compose", "execute"), ("f8", "f9")),
            Step("Return an evidence-backed Solution result", "The durable Service Run finalizes a stable result and the Solution presents the proof needed to understand, operate, audit, and improve it.", ("execute", "outcome", "registry"), ("f10", "f11")),
        ),
    ),
    Diagram(
        "generic-agent-runtime",
        "Generic Agent Runtime",
        "One platform image becomes multiple isolated logical Agents through immutable, profile-bound deployments.",
        (
            n("registry", "Immutable AgentCards", "Profile + schemas + digest", "Registry validates the exact logical Agent identity, skill contracts, policy budgets, queues, MCP allowlist, and generic runtime compatibility.", 42, 85, 210, 105, "mint"),
            n("compiler", "Workflow Compiler", "Resolve + pin exact profile", "The compiled plan pins Agent version, profile digest, skill version, executor type, command queue, and runtime range.", 328, 85, 210, 105, "mint"),
            n("coordinator", "Run Coordinator", "Authorize + dispatch", "The coordinator emits a grant-bound command with exact Agent and skill identity, purpose, principal, trace, input digest, and permitted actions.", 614, 85, 210, 105, "mint"),
            n("rabbit", "RabbitMQ", "Durable command delivery", "Manual acknowledgement, redelivery, competing consumers, and dedicated logical Agent queues preserve work across pod loss.", 900, 85, 210, 105, "mint"),
            n("image", "Generic runtime image", "cw-generic-agent-runtime:0.2.0", "One hardened platform image provides profile verification, durable PostgreSQL claims and leases, policy checks, receipts, metrics, cancellation, and graceful drain.", 477, 250, 245, 105, "mint"),
            n("risk", "Risk Agent", "Generic image + Risk profile", "Independent namespace, ServiceAccount, NetworkPolicy, queue, HPA, metrics, rollout, and deterministic hello-risk-v1 executor.", 50, 360, 185, 105, "mint"),
            n("readiness", "Readiness Agent", "Generic image + Readiness profile", "The same image mounts a different immutable profile and runs the deterministic hello-readiness-v1 executor.", 50, 525, 185, 105, "mint"),
            n("synthesis", "Synthesis Agent", "Generic image + Synthesis profile", "Consumes compatible Risk and Readiness results, requires hello.publish permission before recommending approval, and never performs publication.", 430, 445, 205, 110, "mint"),
            n("approval", "Human approval", "Expected action hash", "The durable Workflow pauses and requires a human decision before any publication side effect is released.", 710, 445, 205, 110, "amber"),
            n("publisher", "Publisher MCP", "Separate approved side effect", "The Publisher remains outside every Agent profile and publishes idempotently only after approval.", 990, 445, 180, 110, "mint"),
        ),
        (
            e("g1", "registry", "compiler", "resolve"),
            e("g2", "compiler", "coordinator", "immutable plan", "governance"),
            e("g3", "coordinator", "rabbit", "profile-bound command"),
            e("g4", "rabbit", "image", "deliver"),
            e("g5", "image", "risk", "mount Risk profile"),
            e("g6", "image", "readiness", "mount Readiness profile"),
            e("g6b", "image", "synthesis", "mount Synthesis profile"),
            e("g7", "risk", "synthesis", "typed risk result"),
            e("g8", "readiness", "synthesis", "typed readiness result"),
            e("g9", "synthesis", "approval", "recommendation", "governance"),
            e("g10", "approval", "publisher", "approved action", "governance"),
            e("g11", "publisher", "coordinator", "receipt", "success"),
        ),
        (
            Step("Resolve the immutable logical Agent", "Registry accepts only an AgentCard whose embedded profile, schemas, queue, budgets, and digest agree.", ("registry", "compiler"), ("g1",)),
            Step("Compile and authorize exact identity", "Compiler pins the profile and skill; Coordinator grants one purpose-bound execution and dispatches it durably.", ("compiler", "coordinator", "rabbit"), ("g2", "g3")),
            Step("Run one hardened image", "The shared image verifies the command and profile, then each deployment keeps independent identity, networking, queue, scaling, and state.", ("rabbit", "image", "risk", "readiness", "synthesis"), ("g4", "g5", "g6", "g6b")),
            Step("Execute Risk and Readiness in parallel", "Deterministic parity rules run independently and return typed evidence-backed results.", ("risk", "readiness", "synthesis"), ("g7", "g8")),
            Step("Synthesize without publishing", "Synthesis combines compatible inputs and can recommend approval only when hello.publish is permitted.", ("synthesis", "approval"), ("g9",)),
            Step("Keep side effects behind HITL", "A human approves the expected action hash before the separate Publisher MCP performs the idempotent side effect.", ("approval", "publisher", "coordinator"), ("g10", "g11")),
        ),
    ),
    Diagram(
        "platform-planes",
        "Eight Platform Planes",
        "Cerebro, Weave, and Loom coordinate stable governance and execution contracts above replaceable infrastructure.",
        (
            n("experience", "1 · Experience", "My Solutions · Studio · delegated clients", "One authenticated entry point presents consumer, builder, operator, or delegated headless experiences according to entitlement. Users receive governed Solution actions, never cluster-admin credentials.", 62, 92, 250, 95, "violet"),
            n("governance", "2 · Governance", "Identity · policy · approval · audit", "Every protected action requires verified identity, tenant, purpose, policy version, bounded authority, and correlation.", 350, 92, 250, 95, "amber"),
            n("registry", "3 · Registry", "Catalog · schemas · compiler · lifecycle", "Resolve exact compatible versions and compile immutable plans. Discovery never bypasses trust, lifecycle, health, region, residency, or entitlement.", 638, 92, 250, 95, "sky"),
            n("capabilities", "4 · Agents + MCP", "Reasoning · tools · sandbox · evaluation", "Agents reason under bounded identity. MCP calls are schema-validated, policy-mediated, rate-limited, audited, and executed without giving credentials to Agents.", 926, 92, 220, 95, "coral"),
            n("workflow", "5 · Workflow runtime", "Coordinator · queues · checkpoints · Saga", "Execute durable plans with persistent commands, inbox/outbox, idempotency, retries, approvals, callbacks, checkpoints, and compensation.", 62, 282, 250, 95, "mint"),
            n("knowledge", "6 · RAG + memory + models", "Sources · retrieval · context · aliases", "Authorized retrieval and governed continuity respect source authority, ACLs, purpose, classification, residency, freshness, retention, and immutable generation pins.", 350, 282, 250, 95, "sky"),
            n("evidence", "7 · Evidence", "Metrics · logs · traces · evaluations", "Correlate infrastructure, model, retrieval, policy, Workflow, tool, cost, quality, and business signals without placing secrets or private payloads in telemetry.", 638, 282, 250, 95, "amber"),
            n("infrastructure", "8 · Infrastructure", "Kubernetes · data · event bus · secrets", "Portable provider implementations for compute, persistence, messaging, object storage, search, identity, secrets, networking, telemetry, backup, and recovery.", 926, 282, 220, 95, "violet"),
            n("cerebro", "Cerebro", "Understand · govern · compile · orchestrate · prove", "The product experience and control plane spanning intent, identity, policy, composition, durable execution, evidence, and operations.", 150, 500, 270, 105, "mint"),
            n("weave", "Weave", "Solutions · Services · Workflows · Agents · MCPs", "The reusable governed solution and capability fabric: experience contracts, typed runtime contracts, policies, models, retrieval profiles, data products, and industry packs.", 465, 500, 270, 105, "amber"),
            n("loom", "Loom", "Portable operational substrate", "The cloud-neutral Kubernetes, OCI, Helm, GitOps, data, messaging, secrets, identity, networking, and observability foundation.", 780, 500, 270, 105, "violet"),
        ),
        (
            e("p1", "experience", "governance", "identity + action", "governance"),
            e("p2", "governance", "registry", "eligibility", "governance"),
            e("p3", "registry", "capabilities", "resolution"),
            e("p4", "capabilities", "workflow", "typed work"),
            e("p5", "workflow", "knowledge", "authorized context"),
            e("p6", "knowledge", "evidence", "lineage", "evidence"),
            e("p7", "evidence", "infrastructure", "operate", "evidence"),
            e("p8", "cerebro", "experience", "experience"),
            e("p9", "cerebro", "governance", "control", "governance"),
            e("p10", "weave", "registry", "catalog"),
            e("p11", "weave", "capabilities", "capabilities"),
            e("p12", "weave", "workflow", "composition"),
            e("p13", "loom", "workflow", "runtime"),
            e("p14", "loom", "knowledge", "data"),
            e("p15", "loom", "infrastructure", "providers"),
        ),
        (
            Step("Experience starts with a governed Solution action", "Consumers use My Solutions, builders use Studio, and delegated clients use identity-filtered discovery—not direct infrastructure credentials.", ("experience", "governance"), ("p1",)),
            Step("Governance limits the eligible universe", "Identity, tenant, purpose, entitlement, risk, region, lifecycle, and policy filter what can even be discovered or composed.", ("governance", "registry"), ("p2",)),
            Step("Registry and composition pin exact capability identity", "Schemas, versions, compatibility, trust, health, and lifecycle resolve before Agents or tools can be invoked.", ("registry", "capabilities"), ("p3",)),
            Step("The runtime coordinates typed durable work", "Capabilities execute behind constrained identities while Workflows manage dependencies, waits, retries, callbacks, and compensation.", ("capabilities", "workflow", "knowledge"), ("p4", "p5")),
            Step("Evidence and infrastructure close the operating loop", "Every outcome connects to lineage, evaluations, receipts, telemetry, SLOs, provider health, cost, recovery, and audit.", ("knowledge", "evidence", "infrastructure"), ("p6", "p7")),
            Step("Cerebro, Weave, and Loom span the planes", "Cerebro provides the control plane, Weave the reusable governed assets, and Loom the portable operational foundation.", ("cerebro", "weave", "loom", "experience", "governance", "registry", "capabilities", "workflow", "knowledge", "infrastructure"), ("p8", "p9", "p10", "p11", "p12", "p13", "p14", "p15")),
        ),
    ),
    Diagram(
        "capability-lifecycle",
        "Agent and MCP Capability Lifecycle",
        "A capability becomes usable only after specification, conformance, supply-chain evidence, admission, deployment, attestation, qualification, and Registry convergence.",
        (
            n("author", "Author", "GUI · VS Code · CLI · SDK", "Create the Agent or MCP behavior, portable specification, schemas, evaluation fixtures, metrics, ownership, support, runbook, and deployment profile.", 38, 112, 170, 102, "sky"),
            n("conformance", "Conformance", "Contracts · malformed I/O · resilience", "Validate discovery, schemas, side effects, idempotency, compensation, duplicate delivery, timeout, restart, cancellation, safety, and recovery.", 242, 112, 175, 102, "mint"),
            n("supply", "Supply chain", "Build · scan · SBOM · provenance", "Create digest-pinned image, chart, package, and evidence. Scan code, dependencies, image, secrets, malware, licenses, and generated content.", 451, 112, 175, 102, "amber"),
            n("approval", "Policy + approval", "Risk · data · authority · environment", "Apply publisher trust, tenant scope, external authority, side-effect risk, data classification, region, environment, and separation of duties.", 660, 112, 175, 102, "coral"),
            n("registry", "Release Registry", "Candidate release authority", "Store one immutable release record binding the specification, image, chart, package, policy profile, and complete admission evidence.", 869, 112, 175, 102, "violet"),
            n("operator", "Capability Operator", "Desired state · Kubernetes · Helm", "Verify the admitted release again; create namespace, identity, network, queues, configuration references, resources, probes, telemetry, and digest-pinned runtime.", 974, 318, 188, 110, "mint"),
            n("runtime", "Restricted runtime", "Agent or MCP workspace", "Run non-root with bounded identity, deny-default networking, minimum resources, approved egress, no arbitrary Kubernetes API, and no inline credentials.", 742, 318, 188, 110, "sky"),
            n("attest", "Runtime attestation", "Descriptor · health · schemas", "Discover the live service identity, Agent Card or MCP capabilities, schemas, versions, health, capacity, metrics, support, and lifecycle metadata.", 510, 318, 188, 110, "amber"),
            n("canary", "Qualification", "Synthetic · canary · evaluation", "Compare the live descriptor to the signed release; test quality, safety, reliability, latency, drift, rollback, and alert coverage.", 278, 318, 188, 110, "coral"),
            n("active", "Active capability", "Discoverable logical alias", "Promote only a healthy, entitled, compatible version. Registry events update Cerebro, protocol gateways, configuration, UI, observability, and solution catalogs.", 46, 318, 188, 110, "mint"),
            n("operate", "Operate and improve", "Observe · evaluate · update · drain", "Pin versions into runs, collect evidence, detect drift, release a new immutable version, canary, roll forward, quarantine, drain, roll back safely, or retire.", 394, 540, 412, 112, "violet"),
        ),
        (
            e("c1", "author", "conformance", "test"),
            e("c2", "conformance", "supply", "prove"),
            e("c3", "supply", "approval", "submit", "governance"),
            e("c4", "approval", "registry", "admit", "governance"),
            e("c5", "registry", "operator", "release", "success"),
            e("c6", "operator", "runtime", "reconcile", "success"),
            e("c7", "runtime", "attest", "discover"),
            e("c8", "attest", "canary", "verify", "governance"),
            e("c9", "canary", "active", "promote", "success"),
            e("c10", "active", "operate", "resolve + observe"),
            e("c11", "operate", "registry", "new version / lifecycle", "evidence"),
        ),
        (
            Step("Author a portable capability", "The publisher creates behavior and evidence-ready contracts in the GUI or engineering toolchain.", ("author", "conformance"), ("c1",)),
            Step("Prove behavior and build integrity", "Conformance and supply-chain gates bind tests, scans, SBOM, provenance, and immutable artifacts.", ("conformance", "supply"), ("c2",)),
            Step("Require policy and independent authority", "Risk, data, side effects, tenant scope, environment, and publisher trust determine admission and approval.", ("supply", "approval", "registry"), ("c3", "c4")),
            Step("Deploy only the admitted release", "The Capability Operator is the only component permitted to materialize runtime desired state.", ("registry", "operator", "runtime"), ("c5", "c6")),
            Step("Attest the live service", "The platform validates the runtime identity, descriptors, schemas, health, metrics, and support metadata against the signed release.", ("runtime", "attest"), ("c7",)),
            Step("Qualify before active discovery", "Synthetic and canary evidence must remain healthy before the Registry promotes a logical capability alias.", ("attest", "canary", "active"), ("c8", "c9")),
            Step("Operate through the same lifecycle", "Runs pin the active version; updates, drift, quarantine, drain, rollback, and retirement all flow through the Registry-authoritative control plane.", ("active", "operate", "registry"), ("c10", "c11")),
        ),
    ),
    Diagram(
        "governed-run",
        "Solution Action to Governed Service Run",
        "Intent becomes an approved, executed, evidence-backed outcome.",
        (
            n("enterprise", "Enterprise Input", "Identity · request · purpose", "A bounded enterprise request enters through an approved Solution channel with current user, tenant, purpose, and authority context.", 40, 100, 175, 105, "mint"),
            n("workspace", "Collaborative Workspace", "People · context · review", "People refine the request together while shared context, ownership, and review remain explicit.", 255, 100, 175, 105, "mint"),
            n("studio", "Studio", "Design · compose · validate", "Studio converts the agreed intent into a typed, inspectable Service and Workflow design.", 470, 100, 175, 105, "mint"),
            n("compiler", "Intent Compiler", "Intent · entities · risk", "The compiler produces a typed execution intent and validates constructability without assigning unauthorized privilege.", 685, 100, 175, 105, "mint"),
            n("identity", "Identity", "User · tenant · delegation", "Identity resolves the current principal, tenant, groups, roles, delegation, session, and effective authority.", 900, 100, 175, 105, "mint"),
            n("policy", "Policy Approval", "Graph · risk · decision", "Policy evaluates the complete reachable graph and pauses consequential operations for independent approval.", 65, 330, 190, 110, "amber"),
            n("workflow", "Workflow", "DAG · state · barriers", "A durable Workflow coordinates typed nodes, conditions, waits, retries, and compensation.", 300, 330, 190, 110, "mint"),
            n("agents", "Agents", "Specialists · artifacts", "Specialist Agents receive bounded tasks and return schema-valid immutable artifacts.", 535, 330, 190, 110, "mint"),
            n("mcp", "MCP", "Tools · credentials · receipts", "MCP resolves approved tools, performs scoped token exchange, and records provider receipts without exposing credentials to Agents.", 770, 330, 190, 110, "mint"),
            n("orchestrator", "Durable Orchestrator", "Queue · checkpoints · Saga", "The orchestrator persists commands, events, leases, checkpoints, approvals, retries, and compensation evidence.", 1005, 330, 155, 110, "mint"),
            n("evidence", "Evidence", "Lineage · policy · telemetry", "Evidence preserves the plan, artifacts, citations, approvals, receipts, metrics, logs, traces, and cost needed to reproduce the outcome.", 665, 555, 255, 105, "mint"),
            n("outcome", "Outcome", "Approved · useful · provable", "The governed result returns to the user with its evidence, policy decision, state, and reproducible proof intact.", 960, 555, 190, 105, "mint"),
        ),
        (
            e("r1", "enterprise", "workspace", kind="success"),
            e("r2", "workspace", "studio", kind="success"),
            e("r3", "studio", "compiler", kind="success"),
            e("r4", "compiler", "identity", kind="success"),
            e("r5", "identity", "policy", kind="governance"),
            e("r6", "workflow", "agents", kind="success"),
            e("r7", "workflow", "mcp", kind="success"),
            e("r8", "agents", "orchestrator", kind="success"),
            e("r9", "mcp", "orchestrator", kind="success"),
            e("r10", "policy", "workflow", kind="governance"),
            e("r11", "policy", "orchestrator", kind="governance"),
            e("r12", "orchestrator", "evidence", kind="success"),
            e("r13", "evidence", "outcome", kind="success"),
            e("r14", "outcome", "enterprise", kind="evidence"),
        ),
        (
            Step("Capture enterprise intent", "Enterprise input enters a collaborative workspace where people refine the bounded request and its purpose.", ("enterprise", "workspace"), ("r1",)),
            Step("Design the governed solution", "Studio turns the agreed request into typed, inspectable Service and Workflow contracts.", ("workspace", "studio"), ("r2",)),
            Step("Compile intent and resolve identity", "The intent compiler validates the request and resolves the current principal, tenant, delegation, and authority.", ("studio", "compiler", "identity"), ("r3", "r4")),
            Step("Authorize the complete graph", "Policy evaluates the whole reachable graph and holds consequential operations for independent approval.", ("identity", "policy"), ("r5",)),
            Step("Execute durably", "Workflow fans out to specialist Agents and MCP tools, then converges through the durable orchestrator with approved policy context.", ("workflow", "agents", "mcp", "policy", "orchestrator"), ("r10", "r6", "r7", "r8", "r9", "r11")),
            Step("Return evidence with the outcome", "The orchestrator emits evidence, and the evidence-backed canonical outcome returns to the experience layer with logs, state, and proof.", ("orchestrator", "evidence", "outcome", "enterprise"), ("r12", "r13", "r14")),
        ),
    ),
    Diagram(
        "scale-path",
        "Individual to Sovereign Enterprise",
        "The same Solution, Service, Workflow, Agent, and MCP contracts scale through progressively stronger sharing, isolation, governance, operations, and assurance.",
        (
            n("individual", "Individual", "Personal Solutions and private sources", "Guided consumer experiences, personal sources, explicit confirmation before side effects, local or hosted execution, personal workspaces, and understandable run evidence.", 42, 145, 185, 115, "mint"),
            n("team", "Team", "Shared capabilities and knowledge", "Group entitlements, shared catalogs, team-owned sources, reusable Workflows, owner/support metadata, quality thresholds, and role-based approvals.", 274, 145, 185, 115, "sky"),
            n("business", "Small business", "Repeatable operating Solutions", "Business-owned Solution templates, reusable Services, common connectors, customer and financial boundaries, operational dashboards, exception handling, and accountable outcomes.", 506, 145, 185, 115, "amber"),
            n("enterprise", "Enterprise", "Multi-tenant governed ecosystem", "Publisher trust, separation of duties, risk tiers, lifecycle admission, model and data governance, broad observability, cost attribution, and dedicated profiles.", 738, 145, 185, 115, "violet"),
            n("sovereign", "Sovereign / regulated", "Dedicated, restricted, or disconnected", "Dedicated identity realms, keys, namespaces, data planes, queues, search generations, model endpoints, evidence stores, backups, regions, and offline operations.", 970, 145, 185, 115, "coral"),
            n("contracts", "Stable product contracts", "Solutions · Services · Workflows · Agents · MCPs", "The product model remains stable across scale: experience and runtime contracts, exact versions, policy context, evidence, ownership, lifecycle, and support.", 126, 388, 300, 108, "mint"),
            n("profiles", "Progressive deployment profiles", "Shared · dedicated · sovereign · edge", "Assurance increases by replacing shared resources with dedicated or restricted implementations without forking the platform semantics.", 450, 388, 300, 108, "amber"),
            n("packs", "Solution and control packs", "Industry · jurisdiction · data · policy", "Signed packs contribute vocabulary, schemas, policies, evaluations, solution templates, dashboards, controls, and shared-responsibility guidance.", 774, 388, 300, 108, "violet"),
            n("outcomes", "Outcome", "One useful Solution to a governed ecosystem", "Customers can start with one consumer-ready Solution, preserve reusable Service and capability investment, and add governance and isolation as risk and organizational complexity increase.", 360, 570, 480, 90, "mint"),
        ),
        (
            e("s1", "individual", "team", "share"),
            e("s2", "team", "business", "standardize"),
            e("s3", "business", "enterprise", "govern"),
            e("s4", "enterprise", "sovereign", "isolate", "governance"),
            e("s5", "individual", "contracts", "same asset model"),
            e("s6", "business", "profiles", "profile"),
            e("s7", "sovereign", "packs", "controls", "governance"),
            e("s8", "contracts", "outcomes", "preserve investment", "success"),
            e("s9", "profiles", "outcomes", "scale operations", "success"),
            e("s10", "packs", "outcomes", "adapt domain", "success"),
        ),
        (
            Step("Begin with one person and one useful outcome", "Use guided creation, private approved sources, bounded tools, explicit confirmation, and clear run evidence.", ("individual", "contracts"), ("s5",)),
            Step("Share within a team", "Add group ownership, shared catalogs, source scopes, support routes, quality thresholds, and role-based approval.", ("individual", "team", "contracts"), ("s1", "s5")),
            Step("Turn know-how into small-business operations", "Package repeatable customer, finance, support, sales, delivery, and administration processes as user-facing Solutions backed by reusable Services.", ("team", "business", "profiles"), ("s2", "s6")),
            Step("Operate an enterprise capability ecosystem", "Add multi-tenant identity, publisher trust, separation of duties, lifecycle admission, cost attribution, broad observability, and dedicated profiles.", ("business", "enterprise", "profiles", "packs"), ("s3", "s6")),
            Step("Meet sovereign and regulated constraints", "Use dedicated or disconnected identity, keys, networks, data, models, evidence, regions, recovery, and operating procedures.", ("enterprise", "sovereign", "packs"), ("s4", "s7")),
            Step("Preserve the same product investment", "Solutions, Services, Workflows, Agents, MCPs, policies, packs, and evidence retain stable contracts while deployment and assurance become stronger.", ("contracts", "profiles", "packs", "outcomes"), ("s8", "s9", "s10")),
        ),
    ),
)


def node_map(diagram: Diagram) -> dict[str, Node]:
    return {node.id: node for node in diagram.nodes}


def center(node: Node) -> tuple[float, float]:
    return node.x + node.w / 2, node.y + node.h / 2


def edge_path(edge: Edge, nodes: dict[str, Node]) -> str:
    source = nodes[edge.source]
    target = nodes[edge.target]
    sx, sy = center(source)
    tx, ty = center(target)
    dx = tx - sx
    dy = ty - sy
    if abs(dx) >= abs(dy):
        sx = source.x + source.w if dx > 0 else source.x
        tx = target.x if dx > 0 else target.x + target.w
        mid = (sx + tx) / 2
        return f"M {sx:.1f} {sy:.1f} L {mid:.1f} {sy:.1f} L {mid:.1f} {ty:.1f} L {tx:.1f} {ty:.1f}"
    sy = source.y + source.h if dy > 0 else source.y
    ty = target.y if dy > 0 else target.y + target.h
    mid = (sy + ty) / 2
    return f"M {sx:.1f} {sy:.1f} L {sx:.1f} {mid:.1f} L {tx:.1f} {mid:.1f} L {tx:.1f} {ty:.1f}"


def text_lines(text: str, max_chars: int) -> list[str]:
    return textwrap.wrap(text, width=max_chars, break_long_words=False, break_on_hyphens=False) or [""]


SCENE_LAYERS = (
    ("EXPERIENCE", "Channels and Solutions", 172, 320),
    ("CEREBRO", "Intent, Identity, Policy, Registry, Compiler", 430, 575),
    ("WEAVE + LOOM", "Workflows, Agents, MCP, Evidence, Kubernetes", 680, 830),
)

GOVERNED_RUN_LAYOUT = {
    "enterprise": (92, 350, 112, 150),
    "workspace": (218, 366, 112, 150),
    "studio": (344, 382, 112, 150),
    "compiler": (470, 398, 112, 150),
    "identity": (596, 414, 112, 150),
    "policy": (722, 430, 112, 150),
    "workflow": (848, 446, 112, 150),
    "agents": (974, 374, 112, 132),
    "mcp": (974, 532, 112, 132),
    "orchestrator": (1100, 462, 112, 150),
    "evidence": (1226, 478, 112, 150),
    "outcome": (1352, 494, 104, 150),
}

GOVERNED_EDGE_PATHS = {
    "r1": "M 204 425 L 218 441",
    "r2": "M 330 441 L 344 457",
    "r3": "M 456 457 L 470 473",
    "r4": "M 582 473 L 596 489",
    "r5": "M 708 489 L 722 505",
    "r10": "M 834 505 L 848 521",
    "r6": "M 960 506 C 972 500 968 452 974 440",
    "r7": "M 960 536 C 972 542 968 584 974 598",
    "r8": "M 1086 440 C 1094 444 1092 510 1100 522",
    "r9": "M 1086 598 C 1094 590 1092 544 1100 538",
    "r11": "M 778 580 C 846 668 1028 690 1156 612",
    "r12": "M 1212 537 L 1226 553",
    "r13": "M 1338 553 L 1352 569",
}


def scene_nodes(diagram: Diagram) -> tuple[Node, ...]:
    if diagram.slug == "governed-run":
        return tuple(
            Node(
                node.id,
                node.title,
                node.subtitle,
                node.detail,
                *GOVERNED_RUN_LAYOUT[node.id],
                node.color,
            )
            for node in diagram.nodes
        )
    bands = (
        [node for node in diagram.nodes if node.y < 280],
        [node for node in diagram.nodes if 280 <= node.y < 520],
        [node for node in diagram.nodes if node.y >= 520],
    )
    visual_nodes: list[Node] = []
    for band_index, band in enumerate(bands):
        ordered = sorted(band, key=lambda item: (item.x, item.y))
        if not ordered:
            continue
        count = len(ordered)
        columns = min(4, count)
        rows = (count + columns - 1) // columns
        gap_x = 38
        gap_y = 14
        available = 970
        card_width = min(222, int((available - gap_x * (columns - 1)) / columns))
        card_height = 108 if rows == 1 else 84
        total_width = columns * card_width + gap_x * (columns - 1)
        start_x = 330 + (available - total_width) // 2
        start_y = SCENE_LAYERS[band_index][2] + 48 - ((rows - 1) * (card_height + gap_y)) // 2
        for index, node in enumerate(ordered):
            row = index // columns
            column = index % columns
            row_count = min(columns, count - row * columns)
            row_width = row_count * card_width + gap_x * (row_count - 1)
            row_start_x = 330 + (available - row_width) // 2
            visual_nodes.append(
                Node(
                    node.id,
                    node.title,
                    node.subtitle,
                    node.detail,
                    row_start_x + column * (card_width + gap_x),
                    start_y + row * (card_height + gap_y),
                    card_width,
                    card_height,
                    node.color,
                )
            )
    return tuple(visual_nodes)


def svg_governed_decks() -> str:
    face = "M 62 431 L 212 300 L 1482 500 L 1301 714 L 58 508 Z"
    return (
        '<g class="glass-deck governed-runway governed-slab deck-1">'
        f'<path class="deck-shadow" d="{face}" transform="translate(0 45)"/>'
        f'<path class="deck-depth" d="{face}" transform="translate(0 26)"/>'
        f'<path class="deck-face" d="{face}"/>'
        '<path class="deck-grid" d="M 86 414 L 1328 612 M 114 390 L 1360 586 M 143 365 L 1392 560 '
        'M 173 339 L 1422 534 M 194 317 L 1450 514 M 180 482 L 350 323 M 430 568 L 596 361 '
        'M 684 610 L 842 400 M 938 651 L 1085 440 M 1190 692 L 1334 478"/>'
        '<path class="deck-shine" d="M 62 431 L 212 300 L 1482 500"/>'
        '<path class="runway-rail runway-rail-a" d="M 83 456 L 218 333 L 1451 525"/>'
        '<path class="runway-rail runway-rail-b" d="M 79 493 L 1294 686 L 1454 510"/>'
        '<g class="branch-plinth"><path d="M 951 405 L 1014 351 L 1160 374 L 1089 447 Z"/>'
        '<path d="M 951 563 L 1014 509 L 1160 532 L 1089 605 Z"/></g>'
        '</g>'
    )


def svg_decks(*, governed: bool = False) -> str:
    if governed:
        return svg_governed_decks()
    decks = []
    for index, (label, subtitle, top, bottom) in enumerate(SCENE_LAYERS, start=1):
        decks.append(
            f'<g class="glass-deck deck-{index}">'
            f'<path class="deck-shadow" d="M 354 {top + 65} L 1128 {top - 2} L 1368 {top + 108} '
            f'L 1288 {bottom + 8} L 388 {bottom + 59} L 260 {bottom - 10} Z"/>'
            f'<path class="deck-depth" d="M 260 {bottom - 10} L 388 {bottom + 59} L 1288 {bottom + 8} '
            f'L 1368 {top + 108} L 1368 {top + 127} L 1294 {bottom + 30} L 384 {bottom + 82} L 260 {bottom + 8} Z"/>'
            f'<path class="deck-face" d="M 354 {top + 55} L 1128 {top - 12} L 1368 {top + 98} '
            f'L 1288 {bottom - 2} L 388 {bottom + 49} L 260 {bottom - 20} Z"/>'
            f'<path class="deck-grid" d="M 318 {top + 89} L 1328 {top + 71} M 300 {top + 130} L 1336 {top + 117} '
            f'M 282 {top + 169} L 1312 {top + 161} M 430 {top + 44} L 438 {bottom + 43} '
            f'M 660 {top + 24} L 672 {bottom + 30} M 890 {top + 4} L 906 {bottom + 17} '
            f'M 1120 {top - 8} L 1140 {bottom + 4}"/>'
            f'<path class="deck-shine" d="M 354 {top + 55} L 1128 {top - 12} L 1364 {top + 97}"/>'
            f'<text class="layer-title" x="70" y="{top + 88}">{label}</text>'
            f'<text class="layer-subtitle" x="70" y="{top + 115}">{subtitle}</text>'
            f'<path class="layer-rule" d="M 50 {top + 57} V {top + 119}"/>'
            f'</g>'
        )
    return "".join(decks)


def svg_icon(node: Node) -> str:
    label = f"{node.id} {node.title}".lower()
    cx = node.x + node.w / 2
    cy = node.y + 25
    if "workspace" in label:
        shape = f'<circle cx="{cx}" cy="{cy - 8}" r="5"/><circle cx="{cx - 13}" cy="{cy - 4}" r="4"/><circle cx="{cx + 13}" cy="{cy - 4}" r="4"/><path d="M {cx - 10} {cy + 13} c 1 -9 6 -13 10 -13 s 9 4 10 13 M {cx - 21} {cy + 11} c 1 -7 5 -10 9 -10 M {cx + 21} {cy + 11} c -1 -7 -5 -10 -9 -10"/>'
    elif "compiler" in label:
        shape = f'<path d="M {cx - 10} {cy - 4} c -8 -8 2 -18 9 -11 c 5 -8 16 -2 13 6 c 8 1 9 13 1 16 c 1 8 -10 12 -15 5 c -7 6 -16 -2 -11 -9 c -6 -2 -5 -10 3 -11 z M {cx - 3} {cy - 11} v 22 M {cx + 5} {cy - 10} v 20"/>'
    elif "workflow" in label:
        shape = f'<circle cx="{cx}" cy="{cy - 11}" r="4"/><circle cx="{cx - 13}" cy="{cy + 10}" r="4"/><circle cx="{cx + 13}" cy="{cy + 10}" r="4"/><path d="M {cx} {cy - 7} v 7 M {cx} {cy} l -13 6 M {cx} {cy} l 13 6"/>'
    elif "agents" in label:
        shape = f'<rect x="{cx - 11}" y="{cy - 9}" width="22" height="17" rx="5"/><path d="M {cx} {cy - 14} v 5 M {cx - 5} {cy - 1} h 1 M {cx + 4} {cy - 1} h 1 M {cx - 16} {cy - 4} h 5 M {cx + 11} {cy - 4} h 5"/>'
    elif node.id == "mcp":
        shape = f'<ellipse cx="{cx}" cy="{cy - 9}" rx="10" ry="5"/><path d="M {cx - 10} {cy - 9} v 18 c 0 3 20 3 20 0 v-18 M {cx - 10} {cy} c 0 3 20 3 20 0"/>'
    elif any(word in label for word in ("policy", "approval", "authorize", "identity", "governance")):
        shape = f'<path d="M {cx} {cy - 12} l 11 5 v 8 c 0 8 -5 13 -11 16 c -6 -3 -11 -8 -11 -16 v-8 z"/><path d="M {cx - 5} {cy + 1} l 4 4 l 7 -8"/>'
    elif any(word in label for word in ("evidence", "outcome", "final", "result", "registry", "contract")):
        shape = f'<rect x="{cx - 10}" y="{cy - 13}" width="20" height="27" rx="2"/><path d="M {cx - 5} {cy - 5} h 10 M {cx - 5} {cy + 1} h 10 M {cx - 5} {cy + 7} h 7"/>'
    elif any(word in label for word in ("mcp", "tool", "runtime", "operator", "orchestrator", "infrastructure")):
        shape = f'<circle cx="{cx}" cy="{cy}" r="8"/><circle cx="{cx}" cy="{cy}" r="3"/><path d="M {cx} {cy - 14} v 5 M {cx} {cy + 9} v 5 M {cx - 14} {cy} h 5 M {cx + 9} {cy} h 5 M {cx - 10} {cy - 10} l 4 4 M {cx + 6} {cy + 6} l 4 4 M {cx + 10} {cy - 10} l -4 4 M {cx - 6} {cy + 6} l -4 4"/>'
    elif any(word in label for word in ("studio", "code", "compile", "developer")):
        shape = f'<path d="M {cx - 12} {cy - 8} l -7 8 l 7 8 M {cx + 12} {cy - 8} l 7 8 l -7 8 M {cx + 4} {cy - 12} l -8 24"/>'
    elif any(word in label for word in ("agent", "people", "user", "team", "human", "enterprise")):
        shape = f'<circle cx="{cx}" cy="{cy - 7}" r="6"/><path d="M {cx - 13} {cy + 13} c 1 -9 7 -13 13 -13 s 12 4 13 13"/>'
    else:
        shape = f'<circle cx="{cx}" cy="{cy}" r="12"/><path d="M {cx - 8} {cy} h 16 M {cx} {cy - 8} v 16"/>'
    return f'<g class="node-icon">{shape}</g>'


def svg_node(node: Node, interactive: bool = False, substantial: bool = False) -> str:
    title_lines = text_lines(node.title, max(14, int(node.w / 10)))
    subtitle_lines = text_lines(node.subtitle, max(18, int(node.w / 8)))
    compact = node.h < 100
    icon_y = node.y + (21 if compact else 27)
    title_y = node.y + (48 if compact else 61)
    title_markup = "".join(
        f'<tspan x="{node.x + node.w / 2}" dy="{0 if i == 0 else 16}">{escape(line)}</tspan>'
        for i, line in enumerate(title_lines[:2])
    )
    subtitle_y = title_y + min(len(title_lines), 2) * 14 + 4
    subtitle_markup = "".join(
        f'<tspan x="{node.x + node.w / 2}" dy="{0 if i == 0 else 14}">{escape(line)}</tspan>'
        for i, line in enumerate(subtitle_lines[:1 if compact else 2])
    )
    attrs = (
        f' role="button" tabindex="0" aria-label="{escape(node.title)}" data-node-id="{node.id}"'
        if interactive else ""
    )
    echo_markup = "" if substantial else (
        f'<rect class="node-echo node-echo-back" x="{node.x - 12}" y="{node.y + 8}" width="{node.w}" height="{node.h}" rx="15"/>'
        f'<rect class="node-echo" x="{node.x - 6}" y="{node.y + 4}" width="{node.w}" height="{node.h}" rx="15"/>'
    )
    depth = 18 if substantial else 12
    node_class = " governed-node" if substantial else ""
    radius = 22 if substantial else 15
    return f"""
    <g id="node-{node.id}" class="node node-{node.color}{node_class}"{attrs}>
      {echo_markup}
      <path class="node-depth" d="M {node.x + 10} {node.y + node.h} L {node.x + node.w} {node.y + node.h} L {node.x + node.w - 11} {node.y + node.h + depth} L {node.x + 21} {node.y + node.h + depth} Z"/>
      <rect class="node-face" x="{node.x}" y="{node.y}" width="{node.w}" height="{node.h}" rx="{radius}"/>
      <path class="node-shine" d="M {node.x + 16} {node.y + 7} H {node.x + node.w - 16}"/>
      <g transform="translate(0 {icon_y - (node.y + 25)})">{svg_icon(node)}</g>
      <text class="node-title" x="{node.x + node.w / 2}" y="{title_y}">{title_markup}</text>
      <text class="node-subtitle" x="{node.x + node.w / 2}" y="{subtitle_y}">{subtitle_markup}</text>
      <g class="node-step"><circle cx="{node.x + node.w - 15}" cy="{node.y + 15}" r="13"/><text class="node-step-number" x="{node.x + node.w - 15}" y="{node.y + 19}"></text></g>
    </g>"""


GOVERNED_NODE_NUMBERS = {
    "enterprise": "1",
    "workspace": "2",
    "studio": "3",
    "compiler": "4",
    "identity": "5",
    "policy": "6",
    "workflow": "7",
    "agents": "8",
    "mcp": "9",
    "orchestrator": "10",
    "evidence": "11",
    "outcome": "12",
}


def svg_governed_node(node: Node, interactive: bool = False) -> str:
    title_lines = text_lines(node.title, 13)
    subtitle_lines = text_lines(node.subtitle, 18)
    attrs = (
        f' role="button" tabindex="0" aria-label="{escape(node.title)}" data-node-id="{node.id}"'
        if interactive else ""
    )
    title_y = node.y + 82
    title_markup = "".join(
        f'<tspan x="{node.x + node.w / 2}" dy="{0 if index == 0 else 18}">{escape(line)}</tspan>'
        for index, line in enumerate(title_lines[:2])
    )
    subtitle_y = title_y + min(len(title_lines), 2) * 18 + 12
    subtitle_markup = "".join(
        f'<tspan x="{node.x + node.w / 2}" dy="{0 if index == 0 else 12}">{escape(line)}</tspan>'
        for index, line in enumerate(subtitle_lines[:2])
    )
    x, y, w, h = node.x, node.y, node.w, node.h
    return f"""
    <g id="node-{node.id}" class="node node-{node.color} governed-node governed-cuboid"{attrs}>
      <rect class="cuboid-echo cuboid-echo-back" x="{x - 16}" y="{y + 16}" width="{w}" height="{h}" rx="17"/>
      <rect class="cuboid-echo" x="{x - 8}" y="{y + 8}" width="{w}" height="{h}" rx="17"/>
      <path class="node-plinth" d="M {x - 13} {y + h - 7} L {x + w + 9} {y + h - 7} L {x + w + 22} {y + h + 14} L {x - 2} {y + h + 14} Z"/>
      <path class="node-top" d="M {x + 8} {y + 5} L {x + 23} {y - 13} L {x + w - 9} {y - 13} L {x + w + 8} {y + 5} Z"/>
      <path class="node-side" d="M {x + w - 1} {y + 10} L {x + w + 10} {y + 1} L {x + w + 10} {y + h - 13} L {x + w - 1} {y + h} Z"/>
      <rect class="node-face" x="{x}" y="{y}" width="{w}" height="{h}" rx="18"/>
      <path class="node-shine" d="M {x + 15} {y + 7} H {x + w - 15}"/>
      <g transform="translate(0 17)">{svg_icon(node)}</g>
      <text class="node-title" x="{x + w / 2}" y="{title_y}">{title_markup}</text>
      <text class="node-subtitle" x="{x + w / 2}" y="{subtitle_y}">{subtitle_markup}</text>
      <g class="cuboid-number"><circle cx="{x + 8}" cy="{y - 15}" r="16"/><text x="{x + 8}" y="{y - 9}">{GOVERNED_NODE_NUMBERS[node.id]}</text></g>
      <g class="node-step"><circle cx="{x + w - 15}" cy="{y + 15}" r="13"/><text class="node-step-number" x="{x + w - 15}" y="{y + 19}"></text></g>
    </g>"""


def svg_scene_accents(diagram: Diagram) -> str:
    if diagram.slug != "governed-run":
        return """
          <g class="route-legend" transform="translate(58 914)">
            <circle cx="0" cy="0" r="6" class="legend-lime"/><text x="15" y="4">Data / Execution</text>
            <circle cx="180" cy="0" r="6" class="legend-amber"/><text x="195" y="4">Authorization / Approvals</text>
            <circle cx="430" cy="0" r="6" class="legend-white"/><text x="445" y="4">Evidence / State</text>
          </g>
        """
    return """
      <g class="control-routes">
        <path d="M 166 330 V 222 H 604 V 405" class="control-route"/>
        <circle cx="166" cy="330" r="5"/><circle cx="604" cy="405" r="5"/>
        <text x="226" y="209">IDENTITY</text><text class="control-copy" x="310" y="209">Access · permissions · roles</text>
        <path d="M 596 270 V 228 H 778 V 421" class="control-route"/>
        <circle cx="778" cy="421" r="5"/>
        <text x="626" y="215">POLICY</text><text class="control-copy" x="696" y="215">Governance · compliance · risk</text>
        <path d="M 778 228 H 1326 V 469" class="control-route"/>
        <circle cx="1326" cy="469" r="5"/>
        <text x="1158" y="215">STATE</text><text class="control-copy" x="1215" y="215">Context · session · memory</text>
      </g>
      <g class="payload-card request-card" transform="translate(205 588)">
        <rect width="190" height="108" rx="12"/><text class="payload-title" x="18" y="27">REQUEST PAYLOAD</text>
        <text x="22" y="51">• userId</text><text x="22" y="68">• intent</text><text x="22" y="85">• context + metadata</text>
      </g>
      <g class="payload-card evidence-card" transform="translate(738 700)">
        <rect width="205" height="118" rx="12"/><text class="payload-title" x="18" y="28">EVIDENCE PAYLOAD</text>
        <text x="22" y="53">• execution logs + outputs</text><text x="22" y="72">• attestations + hashes</text>
        <text x="22" y="91">• approvals + receipts</text>
      </g>
      <g class="evidence-return">
        <path d="M 1404 644 V 748 Q 1404 780 1370 803 L 1230 886 Q 1198 904 1162 898 L 195 744 Q 155 737 155 699 V 514" class="return-glow"/>
        <path d="M 1404 644 V 748 Q 1404 780 1370 803 L 1230 886 Q 1198 904 1162 898 L 195 744 Q 155 737 155 699 V 514" class="return-route"/>
        <text x="520" y="818">EVIDENCE RETURN · LOGS · STATE · PROOF</text>
      </g>
      <g class="route-legend reference-legend" transform="translate(48 812)">
        <rect x="0" y="0" width="310" height="152" rx="16"/>
        <path d="M 24 34 H 104" class="legend-route legend-route-lime"/><text x="126" y="39">Request / response</text>
        <path d="M 24 72 H 104" class="legend-route legend-route-control"/><text x="126" y="77">Identity / policy route</text>
        <path d="M 104 110 H 24" class="legend-route legend-route-return"/><text x="126" y="115">Evidence return</text>
        <path d="M 24 134 H 104" class="legend-route legend-route-amber"/><text x="126" y="139">Human approval</text>
      </g>
    """


def svg_scene_beams(diagram: Diagram) -> str:
    return ""


GOVERNED_IMAGE_HOTSPOTS = {
    "enterprise": (159, 421, 58),
    "workspace": (279, 434, 58),
    "studio": (406, 444, 58),
    "compiler": (532, 457, 58),
    "identity": (661, 468, 58),
    "policy": (785, 480, 58),
    "workflow": (883, 496, 46),
    "agents": (997, 414, 52),
    "mcp": (999, 541, 52),
    "orchestrator": (1146, 504, 58),
    "evidence": (1295, 525, 58),
    "outcome": (1427, 537, 58),
}

GOVERNED_IMAGE_ROUTES = {
    "r1": "M 217 421 L 221 432",
    "r2": "M 337 434 L 348 444",
    "r3": "M 464 444 L 474 456",
    "r4": "M 590 457 L 603 468",
    "r5": "M 719 468 L 727 480",
    "r10": "M 843 480 L 849 496",
    "r6": "M 929 477 C 943 452 950 431 953 420",
    "r7": "M 929 513 C 941 523 945 533 947 541",
    "r8": "M 1049 414 C 1081 425 1099 458 1104 489",
    "r9": "M 1051 541 C 1079 535 1093 520 1105 510",
    "r11": "M 843 480 C 953 449 1052 458 1105 489",
    "r12": "M 1204 505 L 1237 521",
    "r13": "M 1353 526 L 1369 536",
    "r14": "M 1427 596 V 703 Q 1427 752 1377 781 L 1260 850 Q 1219 875 1170 866 L 208 711 Q 159 703 159 654 V 480",
}

GOVERNED_IMAGE_GIF_ROUTES = {
    "r1": [(217, 421), (221, 432)],
    "r2": [(337, 434), (348, 444)],
    "r3": [(464, 444), (474, 456)],
    "r4": [(590, 457), (603, 468)],
    "r5": [(719, 468), (727, 480)],
    "r10": [(843, 480), (849, 496)],
    "r6": [(929, 477), (943, 452), (950, 431), (953, 420)],
    "r7": [(929, 513), (941, 523), (945, 533), (947, 541)],
    "r8": [(1049, 414), (1081, 425), (1099, 458), (1104, 489)],
    "r9": [(1051, 541), (1079, 535), (1093, 520), (1105, 510)],
    "r11": [(843, 480), (953, 449), (1052, 458), (1105, 489)],
    "r12": [(1204, 505), (1237, 521)],
    "r13": [(1353, 526), (1369, 536)],
    "r14": [(1427, 596), (1427, 703), (1377, 781), (1260, 850), (1170, 866), (208, 711), (159, 654), (159, 480)],
}

IMAGE_FIRST_CONFIGS = {
    "intent-to-evidence": ImageFirstConfig(
        ROOT / "assets" / "media" / "spatial" / "intent-to-evidence.png",
        {
            "intent": (83, 503, 34), "solution": (247, 503, 34),
            "service": (414, 503, 34), "cerebro": (760, 502, 76),
            "workflow": (920, 550, 38), "agents": (1028, 496, 34),
            "mcp": (1028, 585, 34), "systems": (1168, 550, 38),
            "approval": (1238, 462, 36), "evidence": (1312, 550, 34),
            "outcome": (1455, 550, 34), "history": (868, 807, 48),
        },
        {
            "i7": ((1061, 496), (1103, 510), (1137, 536)),
            "i8": ((1061, 585), (1104, 572), (1137, 558)),
            "i9": ((1168, 512), (1178, 488), (1208, 470)),
            "i10": ((1206, 550), (1278, 550)),
            "i12": ((1455, 584), (1455, 970), (868, 970), (868, 855)),
        },
    ),
    "service-factory": ImageFirstConfig(
        ROOT / "assets" / "media" / "service-factory-static-master.png",
        {
            "inputs": (218, 309, 68), "studio": (498, 309, 68),
            "contracts": (766, 309, 68), "admission": (1035, 309, 68),
            "registry": (1300, 309, 68), "operator": (267, 644, 68),
            "discovery": (530, 644, 68), "compose": (784, 644, 68),
            "execute": (1056, 644, 68), "outcome": (1321, 644, 68),
        },
        {
            "f7": ((530, 539), (570, 510), (1300, 510), (1300, 414)),
            "f11": ((1321, 749), (1321, 839), (238, 839), (238, 764)),
        },
    ),
    "generic-agent-runtime": ImageFirstConfig(
        ROOT / "assets" / "media" / "generic-agent-runtime-static-master.png",
        {
            "registry": (386, 230, 66), "compiler": (707, 230, 66),
            "coordinator": (1028, 230, 66), "rabbit": (739, 380, 58),
            "image": (741, 516, 58), "risk": (430, 615, 66),
            "readiness": (1084, 615, 66), "synthesis": (741, 645, 62),
            "approval": (739, 802, 62), "publisher": (1081, 807, 66),
        },
        {
            "g11": ((1081, 911), (1081, 935), (1407, 935), (1407, 219), (1133, 219)),
        },
    ),
    "platform-planes": ImageFirstConfig(
        ROOT / "assets" / "media" / "platform-planes-static-master.png",
        {
            "experience": (292, 254, 70), "governance": (605, 254, 70),
            "registry": (923, 254, 70), "capabilities": (1237, 254, 70),
            "workflow": (292, 485, 70), "knowledge": (610, 485, 70),
            "evidence": (925, 485, 70), "infrastructure": (1248, 485, 70),
            "cerebro": (331, 738, 82), "weave": (773, 738, 82),
            "loom": (1210, 738, 82),
        },
        {},
    ),
    "capability-lifecycle": ImageFirstConfig(
        ROOT / "assets" / "media" / "capability-lifecycle-static-master.png",
        {
            "author": (311, 250, 66), "conformance": (558, 250, 66),
            "supply": (806, 250, 66), "approval": (1054, 250, 66),
            "registry": (1305, 250, 66), "operator": (1301, 504, 66),
            "runtime": (1050, 504, 66), "attest": (806, 504, 66),
            "canary": (558, 504, 66), "active": (312, 504, 66),
            "operate": (775, 742, 86),
        },
        {
            "c5": ((1410, 250), (1450, 250), (1450, 504), (1406, 504)),
            "c11": ((925, 742), (1450, 742), (1450, 363), (1405, 250)),
        },
    ),
    "governed-run": ImageFirstConfig(
        ROOT / "assets" / "media" / "governed-run-static-master.png",
        GOVERNED_IMAGE_HOTSPOTS,
        {edge_id: tuple(points) for edge_id, points in GOVERNED_IMAGE_GIF_ROUTES.items()},
    ),
    "scale-path": ImageFirstConfig(
        ROOT / "assets" / "media" / "scale-path-static-master.png",
        {
            "individual": (234, 281, 66), "team": (503, 281, 66),
            "business": (767, 281, 66), "enterprise": (1035, 281, 66),
            "sovereign": (1315, 281, 66), "contracts": (396, 553, 76),
            "profiles": (767, 553, 76), "packs": (1142, 553, 76),
            "outcomes": (768, 837, 90),
        },
        {},
    ),
}


def image_config(diagram: Diagram) -> ImageFirstConfig | None:
    return IMAGE_FIRST_CONFIGS.get(diagram.slug)


def image_master_data_uri(config: ImageFirstConfig) -> str:
    return "data:image/png;base64," + base64.b64encode(config.master.read_bytes()).decode("ascii")


def image_route_points(diagram: Diagram, edge: Edge, config: ImageFirstConfig) -> tuple[tuple[int, int], ...]:
    override = config.route_overrides.get(edge.id)
    if override:
        return override
    sx, sy, sr = config.hotspots[edge.source]
    tx, ty, tr = config.hotspots[edge.target]
    dx, dy = tx - sx, ty - sy
    distance = max(math.hypot(dx, dy), 1)
    return (
        (round(sx + dx * sr / distance), round(sy + dy * sr / distance)),
        (round(tx - dx * tr / distance), round(ty - dy * tr / distance)),
    )


def image_route_path(points: tuple[tuple[int, int], ...]) -> str:
    return "M " + " L ".join(f"{x} {y}" for x, y in points)


def svg_image_scene(diagram: Diagram, interactive: bool) -> str:
    config = IMAGE_FIRST_CONFIGS[diagram.slug]
    edge_markup = []
    for edge in diagram.edges:
        route = image_route_path(image_route_points(diagram, edge, config))
        edge_markup.append(
            f'<g id="edge-{edge.id}" class="edge image-overlay-edge edge-{edge.kind}" data-edge-id="{edge.id}">'
            f'<path class="edge-halo" d="{route}"/><path class="edge-route" d="{route}" marker-end="url(#overlay-arrow)"/>'
            f'<circle class="flow-pulse" r="6"><animateMotion dur="1.5s" repeatCount="indefinite" path="{route}"/></circle></g>'
        )
    hotspot_markup = []
    for node in diagram.nodes:
        x, y, radius = config.hotspots[node.id]
        attrs = (
            f' role="button" tabindex="0" aria-label="{escape(node.title)}" data-node-id="{node.id}"'
            if interactive else f' data-node-id="{node.id}"'
        )
        hotspot_markup.append(
            f'<g id="node-{node.id}" class="node image-hotspot node-{node.color}"{attrs}>'
            f'<circle class="hotspot-hit" cx="{x}" cy="{y}" r="{radius}"/>'
            f'<circle class="hotspot-ring" cx="{x}" cy="{y}" r="{radius + 6}"/>'
            f'<circle class="hotspot-pulse" cx="{x}" cy="{y}" r="{radius + 14}"/></g>'
        )
    return f"""
    <svg class="architecture diagram-{diagram.slug} image-first-diagram" viewBox="0 0 {IMAGE_MASTER_WIDTH} {IMAGE_MASTER_HEIGHT}" role="img" aria-labelledby="diagram-title diagram-desc">
      <title id="diagram-title">{escape(diagram.title)}</title>
      <desc id="diagram-desc">{escape(diagram.subtitle)} The approved static composition remains unchanged while transparent overlays indicate the active semantic route.</desc>
      <defs>
        <marker id="overlay-arrow" markerWidth="12" markerHeight="12" refX="10" refY="4" orient="auto">
          <path d="M0,0 L0,8 L11,4 z" fill="context-stroke"/>
        </marker>
        <filter id="glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      </defs>
      <image class="static-master" href="{image_master_data_uri(config)}" x="0" y="0" width="{IMAGE_MASTER_WIDTH}" height="{IMAGE_MASTER_HEIGHT}" preserveAspectRatio="xMidYMid meet"/>
      <g class="image-overlay-edges">{''.join(edge_markup)}</g>
      <g class="image-overlay-hotspots">{''.join(hotspot_markup)}</g>
    </svg>"""


def svg_content(diagram: Diagram, interactive: bool = False) -> str:
    if image_config(diagram):
        return svg_image_scene(diagram, interactive)
    visual_nodes = scene_nodes(diagram)
    nodes = {node.id: node for node in visual_nodes}
    edges = []
    for edge in diagram.edges:
        route = GOVERNED_EDGE_PATHS[edge.id] if diagram.slug == "governed-run" else edge_path(edge, nodes)
        label_x = (center(nodes[edge.source])[0] + center(nodes[edge.target])[0]) / 2
        label_y = (center(nodes[edge.source])[1] + center(nodes[edge.target])[1]) / 2 - 8
        edges.append(
            f'<g id="edge-{edge.id}" class="edge edge-{edge.kind}" data-edge-id="{edge.id}">'
            f'<path class="edge-route" d="{route}" marker-end="url(#arrow)"/>'
            f'<circle class="flow-pulse" r="4"><animateMotion dur="1.8s" repeatCount="indefinite" path="{route}"/></circle>'
            + (f'<text x="{label_x:.1f}" y="{label_y:.1f}">{escape(edge.label)}</text>' if edge.label and diagram.slug != "governed-run" else "")
            + "</g>"
        )
    governed = diagram.slug == "governed-run"
    node_markup = "".join(
        svg_governed_node(node, interactive) if governed else svg_node(node, interactive)
        for node in visual_nodes
    )
    diagram_title_y = 68 if governed else 82
    diagram_subtitle_y = 110 if governed else 105
    title_markup = (
        f'<text class="diagram-title governed-main-title" x="{WIDTH / 2}" y="{diagram_title_y}">CONTEXTWEAVER — GOVERNED CALL FLOW</text>'
        f'<text class="diagram-subtitle governed-main-subtitle" x="{WIDTH / 2}" y="{diagram_subtitle_y}">Every request carries identity, policy, state, and proof</text>'
        if governed else
        f'<text class="brand-title" x="46" y="72"><tspan>CONTEXT</tspan><tspan class="brand-accent">WEAVER</tspan></text>'
        f'<text class="diagram-title" x="47" y="{diagram_title_y}">{escape(diagram.title.upper())}</text>'
        f'<text class="diagram-subtitle" x="47" y="{diagram_subtitle_y}">{escape(diagram.subtitle)}</text>'
    )
    return f"""
    <svg class="architecture diagram-{diagram.slug}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="diagram-title diagram-desc">
      <title id="diagram-title">{escape(diagram.title)}</title>
      <desc id="diagram-desc">{escape(diagram.subtitle)}</desc>
      <defs>
        <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
          <path d="M0,0 L0,6 L9,3 z" fill="context-stroke"/>
        </marker>
        <filter id="glow"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        <filter id="deck-glow" x="-20%" y="-30%" width="140%" height="180%"><feDropShadow dx="0" dy="0" stdDeviation="7" flood-color="#70e6b1" flood-opacity=".22"/><feDropShadow dx="0" dy="18" stdDeviation="14" flood-color="#000000" flood-opacity=".75"/></filter>
        <filter id="card-shadow" x="-30%" y="-30%" width="160%" height="180%"><feDropShadow dx="0" dy="9" stdDeviation="9" flood-color="#000000" flood-opacity=".58"/></filter>
        <linearGradient id="glass-face" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#173f2e" stop-opacity=".96"/><stop offset=".48" stop-color="#10261d" stop-opacity=".94"/><stop offset="1" stop-color="#07110d" stop-opacity=".98"/></linearGradient>
        <linearGradient id="deck-face" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#173429" stop-opacity=".48"/><stop offset=".58" stop-color="#0a1812" stop-opacity=".7"/><stop offset="1" stop-color="#07110d" stop-opacity=".9"/></linearGradient>
        <linearGradient id="deck-experience" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#174735" stop-opacity=".68"/><stop offset=".58" stop-color="#0b281d" stop-opacity=".84"/><stop offset="1" stop-color="#06130e" stop-opacity=".95"/></linearGradient>
        <linearGradient id="deck-cerebro" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#12382f" stop-opacity=".68"/><stop offset=".58" stop-color="#09231c" stop-opacity=".84"/><stop offset="1" stop-color="#05120e" stop-opacity=".95"/></linearGradient>
        <linearGradient id="deck-weave" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#283c23" stop-opacity=".66"/><stop offset=".58" stop-color="#172719" stop-opacity=".84"/><stop offset="1" stop-color="#09120b" stop-opacity=".96"/></linearGradient>
        <pattern id="perspective-grid" width="60" height="60" patternUnits="userSpaceOnUse"><path d="M60 0H0V60" fill="none" stroke="#315446" stroke-width="1" opacity=".22"/></pattern>
      </defs>
      <rect width="{WIDTH}" height="{HEIGHT}" fill="{COLORS['bg']}"/>
      <rect class="floor-grid" y="78" width="{WIDTH}" height="{HEIGHT - 78}" fill="url(#perspective-grid)"/>
      {title_markup}
      {svg_scene_beams(diagram)}
      <g class="decks">{svg_decks(governed=governed)}</g>
      <g class="edges">{''.join(edges)}</g>
      <g class="nodes">{node_markup}</g>
      {svg_scene_accents(diagram)}
    </svg>"""


SVG_STYLE = f"""
  .floor-grid {{ opacity:.58; }}
  .brand-title {{ fill:{COLORS['text']}; font:900 29px {FONT_STACK}; letter-spacing:2.4px; }}
  .brand-accent {{ fill:#b8ff6a; }}
  .diagram-title {{ fill:{COLORS['mint']}; font:800 15px {FONT_STACK}; letter-spacing:1.6px; }}
  .diagram-subtitle {{ fill:#b9d2c7; font:11px {FONT_STACK}; }}
  .diagram-governed-run .governed-main-title {{ fill:#f4f1e9; font-size:45px; font-weight:850; letter-spacing:2px; text-anchor:middle; }}
  .diagram-governed-run .governed-main-subtitle {{ fill:#a9aeb1; font-size:22px; font-weight:650; letter-spacing:1.5px; text-anchor:middle; }}
  .glass-deck {{ filter:url(#deck-glow); }}
  .glass-deck .deck-shadow {{ fill:#000; opacity:.62; }}
  .glass-deck .deck-face {{ fill:url(#deck-face); stroke:{COLORS['mint']}; stroke-width:1.6; opacity:.94; }}
  .glass-deck .deck-depth {{ fill:#03100b; stroke:{COLORS['mint']}; stroke-width:1.2; opacity:.9; }}
  .glass-deck .deck-grid {{ fill:none; stroke:#70e6b1; stroke-width:.75; opacity:.12; }}
  .glass-deck .deck-shine {{ fill:none; stroke:#a8ffd4; stroke-width:1.4; opacity:.66; }}
  .diagram-governed-run .governed-runway .deck-face {{ fill:url(#deck-experience); stroke:#4bd489; stroke-width:1.6; opacity:.58; }}
  .diagram-governed-run .governed-runway .deck-depth {{ fill:#06170f; stroke:#5bee92; stroke-width:1.5; opacity:.78; }}
  .diagram-governed-run .governed-runway .deck-grid {{ stroke:#4ccf88; opacity:.16; }}
  .runway-rail {{ fill:none; stroke:#7dff58; stroke-width:2.2; opacity:.35; filter:url(#glow); }}
  .branch-plinth path {{ fill:#0b281b; fill-opacity:.52; stroke:#57df91; stroke-width:1.2; }}
  .governed-slab .deck-shadow {{ opacity:.72; }}
  .governed-slab .deck-depth {{ stroke-width:1.8; }}
  .governed-slab .deck-face {{ stroke-width:2.3; }}
  .governed-slab .deck-grid {{ opacity:.09; }}
  .governed-slab .deck-shine {{ stroke-width:2.1; opacity:.78; }}
  .layer-plaque rect {{ fill:#04130d; fill-opacity:.92; stroke:#315b49; stroke-width:1.2; }}
  .layer-title {{ fill:{COLORS['text']}; font:800 20px {FONT_STACK}; letter-spacing:.7px; }}
  .layer-subtitle {{ fill:#a8cbbd; font:11px {FONT_STACK}; }}
  .layer-rule {{ fill:none; stroke:{COLORS['mint']}; stroke-width:4; filter:url(#glow); }}
  .node {{ filter:url(#card-shadow); }}
  .node-face {{ fill:url(#glass-face); stroke:{COLORS['mint']}; stroke-width:2.2; }}
  .node-echo {{ fill:#0b2a1d; fill-opacity:.58; stroke:#70e6b1; stroke-width:1; opacity:.72; }}
  .node-echo-back {{ opacity:.34; }}
  .node-depth {{ fill:#020a07; stroke:{COLORS['mint']}; stroke-width:1.2; }}
  .node-shine {{ fill:none; stroke:#b4ffda; stroke-width:1.3; opacity:.72; }}
  .node-mint .node-face {{ stroke:{COLORS['mint']}; }} .node-sky .node-face {{ stroke:{COLORS['sky']}; }}
  .node-amber .node-face {{ stroke:{COLORS['amber']}; }} .node-violet .node-face {{ stroke:{COLORS['violet']}; }}
  .node-coral .node-face {{ stroke:{COLORS['coral']}; }}
  .node-amber .node-depth,.node-amber .node-echo {{ stroke:{COLORS['amber']}; }}
  .governed-node .node-face {{ fill:url(#glass-face); stroke-width:2.8; }}
  .governed-node .node-depth {{ stroke-width:1.6; }}
  .governed-node .node-shine {{ stroke-width:1.6; opacity:.8; }}
  .governed-cuboid {{ filter:url(#card-shadow); }}
  .governed-cuboid .node-face {{ fill:url(#glass-face); stroke:#65e99d; stroke-width:2.2; }}
  .governed-cuboid .node-top {{ fill:#173b29; fill-opacity:.74; stroke:#72f2a7; stroke-width:1.5; }}
  .governed-cuboid .node-side {{ fill:#07160f; fill-opacity:.9; stroke:#4fcf88; stroke-width:1.2; }}
  .governed-cuboid .node-plinth {{ fill:#0b2519; fill-opacity:.74; stroke:#65e99d; stroke-width:1.2; }}
  .governed-cuboid .cuboid-echo {{ fill:#123a28; fill-opacity:.3; stroke:#4ecf87; stroke-width:1; }}
  .governed-cuboid .cuboid-echo-back {{ opacity:.45; }}
  .governed-cuboid.node-amber .node-face,.governed-cuboid.node-amber .node-top,.governed-cuboid.node-amber .node-side,.governed-cuboid.node-amber .node-plinth {{ stroke:#ffb938; }}
  .governed-cuboid.node-amber .node-face {{ fill:#3a2408; fill-opacity:.9; }}
  .governed-cuboid.node-amber .cuboid-echo {{ stroke:#ffb938; fill:#3b2306; }}
  .diagram-governed-run .node-title {{ font-size:14px; font-weight:850; }}
  .diagram-governed-run .node-subtitle {{ font-size:7px; }}
  .cuboid-number circle {{ fill:#07100b; stroke:#d9ff38; stroke-width:2.5; filter:url(#glow); }}
  .cuboid-number text {{ fill:#f1ffad; font:850 16px {FONT_STACK}; text-anchor:middle; }}
  .node-amber .cuboid-number circle {{ stroke:#ffb938; }} .node-amber .cuboid-number text {{ fill:#ffcb68; }}
  .node-icon {{ fill:none; stroke:#d8fff0; stroke-width:2.2; stroke-linecap:round; stroke-linejoin:round; }}
  .node-title {{ fill:{COLORS['text']}; font:750 13px {FONT_STACK}; text-anchor:middle; }}
  .node-subtitle {{ fill:#aed0c2; font:8px {FONT_STACK}; text-anchor:middle; }}
  .node-step {{ opacity:0; }} .node-step circle {{ fill:{COLORS['bg']}; stroke:{COLORS['mint']}; stroke-width:2; }}
  .node-step text {{ fill:{COLORS['mint']}; font:800 11px {FONT_STACK}; text-anchor:middle; }}
  .edge .edge-route {{ fill:none; stroke:{COLORS['mint']}; stroke-width:2.8; }}
  .flow-pulse {{ fill:{COLORS['mint']}; opacity:0; filter:url(#glow); }}
  .edge text {{ fill:{COLORS['muted']}; font:9px {FONT_STACK}; text-anchor:middle; paint-order:stroke; stroke:{COLORS['bg']}; stroke-width:4; }}
  .edge-governance .edge-route {{ stroke:{COLORS['amber']}; stroke-dasharray:8 6; }}
  .edge-governance .flow-pulse,.edge-waiting .flow-pulse {{ fill:{COLORS['amber']}; }}
  .edge-success .edge-route {{ stroke:{COLORS['mint']}; }} .edge-evidence .edge-route {{ stroke:#d8fff0; stroke-dasharray:3 7; }}
  .edge-evidence .flow-pulse {{ fill:#d8fff0; }}
  .edge-waiting .edge-route {{ stroke:{COLORS['amber']}; stroke-dasharray:10 7; }}
  .route-legend text {{ fill:#d4e2dc; font:11px {FONT_STACK}; }}
  .legend-lime {{ fill:{COLORS['mint']}; filter:url(#glow); }} .legend-amber {{ fill:{COLORS['amber']}; filter:url(#glow); }}
  .legend-white {{ fill:#e8fff5; filter:url(#glow); }}
  .reference-legend rect {{ fill:#03100c; fill-opacity:.9; stroke:#27c997; stroke-width:1; }}
  .reference-legend text {{ font-size:12px; }}
  .legend-route {{ fill:none; stroke-width:4; marker-end:url(#arrow); }}
  .legend-route-lime {{ stroke:#aaff2e; }} .legend-route-amber {{ stroke:{COLORS['amber']}; stroke-dasharray:8 6; }}
  .legend-route-control {{ stroke:#79e968; stroke-dasharray:8 7; }}
  .legend-route-return {{ stroke:#b9ff42; }}
  .step-markers circle {{ fill:#092116; stroke:#b8ff3d; stroke-width:3; filter:url(#glow); }}
  .step-markers text {{ fill:#eaffc9; font:800 18px {FONT_STACK}; text-anchor:middle; }}
  .step-markers .amber-marker circle {{ stroke:{COLORS['amber']}; }} .step-markers .amber-marker text {{ fill:{COLORS['amber']}; }}
  .step-markers .white-marker circle {{ stroke:#e8fff5; }} .step-markers .white-marker text {{ fill:#e8fff5; }}
  .outcome-route {{ fill:none; stroke:#e8fff5; stroke-width:3.2; stroke-dasharray:4 10; marker-end:url(#arrow); filter:url(#glow); }}
  .outcome-ring {{ fill:#092116; stroke:#b8ff3d; stroke-width:4; filter:url(#glow); }}
  .outcome-check {{ fill:none; stroke:#dfff8e; stroke-width:3; stroke-linecap:round; stroke-linejoin:round; }}
  .outcome-label {{ fill:{COLORS['text']}; font:800 21px {FONT_STACK}; letter-spacing:1.2px; text-anchor:end; }}
  .outcome-subtitle {{ fill:#a8cbbd; font:9px {FONT_STACK}; }}
  .vertical-beams .beam {{ fill:none; stroke-width:4; filter:url(#glow); }}
  .vertical-beams .beam-lime {{ stroke:#b8ff39; opacity:.72; }} .vertical-beams .beam-soft {{ stroke:#70e6b1; opacity:.28; }}
  .vertical-beams ellipse {{ fill:#b8ff39; opacity:.36; filter:url(#glow); }}
  .diagram-governed-run .node-step {{ display:none; }}
  .control-route {{ fill:none; stroke:#78e867; stroke-width:2.3; stroke-dasharray:8 7; }}
  .control-routes circle {{ fill:#78e867; filter:url(#glow); }}
  .control-routes text {{ fill:#8bf06d; font:800 15px {FONT_STACK}; }}
  .control-routes .control-copy {{ fill:#74c961; font-size:12px; font-weight:600; }}
  .payload-card rect {{ fill:#07140f; fill-opacity:.95; stroke:#52d890; stroke-width:1.3; }}
  .payload-card text {{ fill:#c8d8d0; font:10px {FONT_STACK}; }}
  .payload-card .payload-title {{ fill:#f1f4ef; font-size:14px; font-weight:800; }}
  .return-glow {{ fill:none; stroke:#b8ff39; stroke-width:13; opacity:.16; filter:url(#glow); }}
  .return-route {{ fill:none; stroke:#c9ff42; stroke-width:3.5; marker-end:url(#arrow); filter:url(#glow); }}
  .evidence-return text {{ fill:#a9ff43; font:800 13px {FONT_STACK}; letter-spacing:.8px; }}
  .image-first-diagram .static-master {{ pointer-events:none; }}
  .image-first-diagram .image-overlay-edge {{ opacity:0; transition:opacity .35s; }}
  .image-first-diagram .image-overlay-edge.complete {{ opacity:.16; }}
  .image-first-diagram .image-overlay-edge.active {{ opacity:1; }}
  .image-first-diagram .edge-halo {{ fill:none; stroke:#b8ff39; stroke-width:16; opacity:.18; filter:url(#glow); }}
  .image-first-diagram .edge-route {{ fill:none; stroke:#d4ff3f; stroke-width:5; stroke-linecap:round; stroke-linejoin:round; }}
  .image-first-diagram .edge-governance .edge-route,.image-first-diagram .edge-waiting .edge-route {{ stroke:#ffc76a; stroke-dasharray:11 8; }}
  .image-first-diagram .edge-evidence .edge-route {{ stroke:#e8fff5; stroke-dasharray:5 8; }}
  .image-first-diagram .flow-pulse {{ fill:#f1ff9c; opacity:0; filter:url(#glow); }}
  .image-first-diagram .active .flow-pulse {{ opacity:1; }}
  .image-hotspot {{ cursor:pointer; }}
  .image-hotspot .hotspot-hit {{ fill:#000; fill-opacity:.001; stroke:none; }}
  .image-hotspot .hotspot-ring,.image-hotspot .hotspot-pulse {{ fill:#b8ff39; fill-opacity:0; stroke:#d4ff3f; stroke-width:0; opacity:0; pointer-events:none; }}
  .image-hotspot.active .hotspot-ring,.image-hotspot.selected .hotspot-ring {{ fill-opacity:.09; stroke-width:4; opacity:1; filter:url(#glow); }}
  .image-hotspot.active .hotspot-pulse {{ stroke-width:2; opacity:.72; transform-box:fill-box; transform-origin:center; animation:hotspot-pulse 1.7s ease-out infinite; }}
  .image-hotspot.node-amber.active .hotspot-ring,.image-hotspot.node-amber.active .hotspot-pulse {{ fill:#ffc76a; stroke:#ffc76a; }}
  .image-hotspot:focus-visible .hotspot-ring {{ stroke-width:5; opacity:1; }}
  @keyframes hotspot-pulse {{ 0%{{transform:scale(.82);opacity:.8}} 100%{{transform:scale(1.22);opacity:0}} }}
"""


def write_static_svg(diagram: Diagram) -> None:
    image_first = image_config(diagram) is not None
    svg_width = IMAGE_MASTER_WIDTH if image_first else WIDTH
    svg_height = IMAGE_MASTER_HEIGHT if image_first else HEIGHT
    content = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}">'
        f"<style>{SVG_STYLE}</style>"
        + svg_content(diagram).replace(
            f'<svg class="architecture diagram-{diagram.slug}'
            + (' image-first-diagram' if image_first else '')
            + f'" viewBox="0 0 {svg_width} {svg_height}" role="img" aria-labelledby="diagram-title diagram-desc">',
            '<g role="img" aria-labelledby="diagram-title diagram-desc">',
            1,
        ).rsplit("</svg>", 1)[0]
        + "</g></svg>"
    )
    (OUT / f"{diagram.slug}.svg").write_text(clean_generated_text(content), encoding="utf-8", newline="\n")


def write_interactive_html(diagram: Diagram) -> None:
    image_first = image_config(diagram) is not None
    nodes_json = {
        node.id: {"title": node.title, "subtitle": node.subtitle, "detail": node.detail}
        for node in diagram.nodes
    }
    steps_json = [
        {"title": step.title, "caption": step.caption, "nodes": step.nodes, "edges": step.edges}
        for step in diagram.steps
    ]
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{escape(diagram.subtitle)}">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<title>{escape(diagram.title)} — ContextWeaver</title>
<style>
:root{{--bg:{COLORS['bg']};--panel:{COLORS['panel']};--panel2:{COLORS['panel2']};--text:{COLORS['text']};--muted:{COLORS['muted']};--line:{COLORS['line']};--mint:{COLORS['mint']};--amber:{COLORS['amber']};--coral:{COLORS['coral']};--violet:{COLORS['violet']};--sky:{COLORS['sky']}}}
*{{box-sizing:border-box}}html{{color-scheme:dark}}body{{min-width:320px;margin:0;overflow-x:hidden;color:var(--text);background:var(--bg);font:14px/1.5 {FONT_STACK}}}button{{font:inherit}}
.experience{{display:grid;grid-template-rows:auto minmax(0,1fr) auto;width:min(1536px,100%);height:100vh;min-height:720px;margin:auto;border:1px solid var(--line);background:linear-gradient(180deg,#0b1c15,#050b08);box-shadow:0 34px 100px #0009;overflow:hidden}}
.storybar{{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:center;gap:22px;min-height:88px;padding:14px 18px;border-bottom:1px solid var(--line);background:#091710eb;backdrop-filter:blur(20px)}}
.storybar>div,.detailbar>div{{min-width:0}}.stage-count{{color:var(--mint);font-size:9px;font-weight:900;letter-spacing:.15em;text-transform:uppercase}}.stage-title{{display:block;margin-top:4px;font:700 clamp(18px,2vw,28px)/1.08 {FONT_STACK};letter-spacing:-.025em}}.stage-caption{{display:block;max-width:980px;margin-top:6px;overflow-wrap:anywhere;color:var(--muted);font-size:11px}}
.canvas{{position:relative;min-height:0;overflow:hidden;background:radial-gradient(circle at 52% 42%,#173f2e55 0,transparent 42%),var(--bg)}}.architecture{{display:block;min-width:900px;width:100%;height:100%;object-fit:contain}}
{SVG_STYLE}
.node{{cursor:pointer;transition:opacity .35s}}.node-face,.node-depth,.edge path{{transition:.35s}}.node:hover .node-face,.node.selected .node-face{{stroke-width:4}}.node.active .node-face{{stroke-width:5;filter:url(#glow)}}.node.active .node-depth{{stroke:var(--mint)}}.node.active .node-step{{opacity:1}}.node.complete{{opacity:.94}}.node.dim{{opacity:.82}}
.edge{{opacity:.42;transition:opacity .35s}}.edge.complete{{opacity:.7}}.edge.dim{{opacity:.32}}.edge.active{{opacity:1}}.edge.active .edge-route{{stroke-width:5;stroke-dasharray:15 9;animation:flow .75s linear infinite;filter:url(#glow)}}.edge.active .flow-pulse{{opacity:1}}.edge-governance.active .edge-route{{stroke:var(--amber)}}.edge-success.active .edge-route{{stroke:var(--mint)}}.edge-waiting.active .edge-route{{stroke:var(--amber)}}.edge-evidence.active .edge-route{{stroke:#d8fff0;stroke-dasharray:3 8}}
@keyframes flow{{to{{stroke-dashoffset:-23}}}}
.controls{{display:flex;gap:7px}}.controls button{{min-height:38px;padding:0 13px;border:1px solid var(--line);border-radius:9px;color:var(--text);background:var(--panel);cursor:pointer;font-size:10px;font-weight:850}}.controls button:hover{{border-color:var(--mint)}}.controls .primary,.controls button[aria-pressed="true"]{{color:#07110f;background:var(--mint)}}
.detailbar{{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:center;gap:22px;min-height:82px;padding:13px 18px;border-top:1px solid var(--line);background:#07110d}}.detailbar b{{display:block;font:700 15px/1.2 {FONT_STACK}}}.detailbar em{{display:block;margin:3px 0;color:var(--amber);font-size:9px;font-style:normal;font-weight:800}}.detailbar p{{margin:0;color:#c8d6d0;font-size:10px}}
.dots{{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:7px}}.dot{{width:10px;height:10px;min-height:0;padding:0;border:0;border-radius:50%;background:var(--line);cursor:pointer}}.dot.complete{{background:#456e5d}}.dot.active{{background:var(--mint);box-shadow:0 0 10px var(--mint)}}
.player-image-first .experience{{display:grid;grid-template-rows:auto minmax(0,1fr) auto;height:100vh;min-height:720px}}
.player-image-first .canvas{{width:100%;height:100%}}
.player-image-first .storybar{{grid-template-columns:minmax(0,1fr) auto}}
.player-image-first .stage-count{{font-size:9px}}.player-image-first .stage-title{{font-size:20px}}
.player-image-first .controls button{{min-height:38px;padding-inline:12px}}
.player-image-first .detailbar{{grid-template-columns:minmax(0,1fr) auto}}
@media(max-width:900px){{.storybar{{grid-template-columns:1fr}}.controls{{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));width:100%}}.controls button{{min-width:0;padding-inline:8px}}.detailbar{{grid-template-columns:1fr}}.dots{{justify-content:flex-start}}.canvas{{min-height:0;overflow:hidden}}.architecture{{min-width:0;width:100%}}}}
@media(max-width:900px){{.player-image-first .experience{{grid-template-rows:auto auto auto;height:auto;min-height:0}}.player-image-first .canvas{{height:auto;aspect-ratio:{IMAGE_MASTER_WIDTH}/{IMAGE_MASTER_HEIGHT}}}.player-image-first .storybar{{grid-template-columns:1fr}}.player-image-first .detailbar{{grid-template-columns:1fr}}}}
@media(max-width:620px){{.experience{{min-height:0;border-width:0}}.storybar,.detailbar{{padding:14px}}.controls{{grid-template-columns:repeat(2,minmax(0,1fr))}}.stage-title{{font-size:18px}}.stage-caption{{font-size:10px}}.architecture{{min-width:0}}}}
@media(prefers-reduced-motion:reduce){{*{{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}}}
</style></head>
<body class="player player-{diagram.slug}{' player-image-first' if image_first else ''}"><main class="experience" aria-live="polite">
<header class="storybar"><div><span class="stage-count" id="stage-count"></span><strong class="stage-title" id="stage-title"></strong><span class="stage-caption" id="stage-caption"></span></div>
<div class="controls"><button id="prev" type="button" aria-label="Previous stage">Previous</button><button id="play" class="primary" type="button">Pause</button><button id="next" type="button" aria-label="Next stage">Next</button><button id="audio" type="button" aria-pressed="false">Audio off</button><button id="reset" type="button">Reset</button><button id="popout" type="button" aria-label="Open animation in a dedicated window">Pop out ↗</button></div></header>
<section class="canvas">{svg_content(diagram, interactive=True)}</section>
<footer class="detailbar"><div><b id="detail-title">Select a component</b><em id="detail-subtitle">Click or use the keyboard</em><p id="detail-copy">Select any glass component to inspect its responsibility and trust boundary. Only the current semantic route moves.</p></div><div class="dots" id="dots" aria-label="Diagram stages"></div></footer>
</main>
<script>
const nodes={json.dumps(nodes_json, ensure_ascii=False)};
const steps={json.dumps(steps_json, ensure_ascii=False)};
let current=0,playing=!matchMedia("(prefers-reduced-motion: reduce)").matches,narration=false,timer;
const $=id=>document.getElementById(id);
const params=new URLSearchParams(location.search),isPopout=params.has("popout");
const nodeEls=[...document.querySelectorAll(".node")],edgeEls=[...document.querySelectorAll(".edge")];
function inspect(id){{const d=nodes[id];if(!d)return;nodeEls.forEach(el=>el.classList.toggle("selected",el.dataset.nodeId===id));$("detail-title").textContent=d.title;$("detail-subtitle").textContent=d.subtitle;$("detail-copy").textContent=d.detail;}}
nodeEls.forEach(el=>{{el.addEventListener("click",()=>{{playing=false;$("play").textContent="Play";stop();inspect(el.dataset.nodeId)}});el.addEventListener("keydown",ev=>{{if(ev.key==="Enter"||ev.key===" "){{ev.preventDefault();el.click()}}}})}});
steps.forEach((_,i)=>{{const b=document.createElement("button");b.className="dot";b.type="button";b.setAttribute("aria-label",`Show stage ${{i+1}}`);b.onclick=()=>{{current=i;render(true);restart()}};$("dots").appendChild(b)}});
function narrateStep(){{if(!narration||!("speechSynthesis" in window))return;window.speechSynthesis.cancel();const s=steps[current],utterance=new SpeechSynthesisUtterance(`${{s.title}}. ${{s.caption}}`);utterance.lang="en-US";utterance.rate=.95;window.speechSynthesis.speak(utterance);}}
function render(withNarration=false){{const s=steps[current],done=steps.slice(0,current),doneNodes=new Set(done.flatMap(step=>step.nodes)),doneEdges=new Set(done.flatMap(step=>step.edges));nodeEls.forEach(el=>{{const id=el.dataset.nodeId,active=s.nodes.includes(id),complete=doneNodes.has(id)&&!active;el.classList.toggle("active",active);el.classList.toggle("complete",complete);el.classList.toggle("dim",!active&&!complete);el.classList.remove("selected");const number=el.querySelector(".node-step-number");if(number)number.textContent=active?String(s.nodes.indexOf(id)+1):"";}});edgeEls.forEach(el=>{{const id=el.dataset.edgeId,active=s.edges.includes(id),complete=doneEdges.has(id)&&!active;el.classList.toggle("active",active);el.classList.toggle("complete",complete);el.classList.toggle("dim",!active&&!complete)}});$("stage-count").textContent=`Current flow · stage ${{current+1}} of ${{steps.length}}`;$("stage-title").textContent=s.title;$("stage-caption").textContent=s.caption;[...$("dots").children].forEach((d,i)=>{{d.classList.toggle("active",i===current);d.classList.toggle("complete",i<current)}});if(s.nodes.length)inspect(s.nodes[s.nodes.length-1]);if(withNarration)narrateStep();}}
function advance(delta=1){{current=(current+delta+steps.length)%steps.length;render(true)}}function stop(){{clearInterval(timer)}}function restart(){{stop();if(playing)timer=setInterval(()=>advance(),6000)}}
$("prev").onclick=()=>{{advance(-1);restart()}};$("next").onclick=()=>{{advance();restart()}};$("reset").onclick=()=>{{current=0;render(true);restart()}};$("play").onclick=()=>{{playing=!playing;$("play").textContent=playing?"Pause":"Play";if(!playing&&"speechSynthesis" in window)window.speechSynthesis.cancel();restart()}};
$("audio").onclick=()=>{{narration=!narration;$("audio").textContent=narration?"Audio on":"Audio off";$("audio").setAttribute("aria-pressed",String(narration));if(narration)narrateStep();else if("speechSynthesis" in window)window.speechSynthesis.cancel();}};if(!("speechSynthesis" in window)){{$("audio").disabled=true;$("audio").textContent="Audio unavailable";}}
function leavePopout(){{window.close();setTimeout(()=>{{if(history.length>1)history.back();else location.href="../architecture.html"}},80)}}
$("popout").textContent=isPopout?"Back · Esc":"Pop out ↗";
$("popout").setAttribute("aria-label",isPopout?"Close the dedicated animation view":"Open animation in a dedicated window");
$("popout").onclick=()=>{{if(isPopout){{leavePopout();return}}const url=new URL(location.href);url.searchParams.delete("embed");url.searchParams.delete("embedded");url.searchParams.set("popout","1");window.open(url.href,"_blank","noopener,noreferrer")}};
document.addEventListener("keydown",e=>{{if(e.key==="Escape"&&isPopout){{e.preventDefault();leavePopout();return}}if(e.target.closest(".node"))return;if(e.key==="ArrowRight")$("next").click();if(e.key==="ArrowLeft")$("prev").click();if(e.key===" "){{e.preventDefault();$("play").click()}}}});
$("play").textContent=playing?"Pause":"Play";render();restart();
</script></body></html>"""
    (OUT / f"{diagram.slug}.html").write_text(clean_generated_text(html), encoding="utf-8", newline="\n")


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = ["Inter-Bold.ttf", "seguisb.ttf", "arialbd.ttf"] if bold else ["Inter-Regular.ttf", "segoeui.ttf", "arial.ttf"]
    for name in names:
        path = Path("C:/Windows/Fonts") / name
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def draw_wrapped(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, font, fill: str, max_lines: int = 3, spacing: int = 4, anchor: str = "mm") -> None:
    x1, y1, x2, y2 = box
    width = max(12, int((x2 - x1) / max(font.size * 0.55, 1))) if hasattr(font, "size") else 22
    lines = textwrap.wrap(text, width=width, break_long_words=False)[:max_lines]
    draw.multiline_text(((x1 + x2) / 2, (y1 + y2) / 2), "\n".join(lines), font=font, fill=fill, anchor=anchor, align="center", spacing=spacing)


def draw_glass_decks(draw: ImageDraw.ImageDraw, governed: bool = False) -> None:
    label_font = load_font(20, True)
    subtitle_font = load_font(11)
    if governed:
        face_points = [(62, 431), (212, 300), (1482, 500), (1301, 714), (58, 508)]
        depth_points = [(x, y + 26) for x, y in face_points]
        shadow_points = [(x, y + 45) for x, y in face_points]
        draw.polygon(shadow_points, fill="#010402")
        draw.line(shadow_points + [shadow_points[0]], fill="#102118", width=2, joint="curve")
        draw.polygon(depth_points, fill="#06170f")
        draw.line(depth_points + [depth_points[0]], fill="#5bee92", width=2, joint="curve")
        draw.polygon(face_points, fill="#102a1d")
        draw.line(face_points + [face_points[0]], fill="#4bd489", width=3, joint="curve")
        for line in (
            [(86, 414), (1328, 612)], [(114, 390), (1360, 586)], [(143, 365), (1392, 560)],
            [(173, 339), (1422, 534)], [(194, 317), (1450, 514)], [(180, 482), (350, 323)],
            [(430, 568), (596, 361)], [(684, 610), (842, 400)], [(938, 651), (1085, 440)],
            [(1190, 692), (1334, 478)],
        ):
            draw.line(line, fill="#204f37", width=1)
        draw.line([(62, 431), (212, 300), (1482, 500)], fill="#9cffbd", width=2, joint="curve")
        draw.line([(83, 456), (218, 333), (1451, 525)], fill="#7dff58", width=2, joint="curve")
        draw.line([(79, 493), (1294, 686), (1454, 510)], fill="#7dff58", width=2, joint="curve")
        for points in (
            [(951, 405), (1014, 351), (1160, 374), (1089, 447)],
            [(951, 563), (1014, 509), (1160, 532), (1089, 605)],
        ):
            draw.polygon(points, fill="#0b281b", outline="#57df91")
        return
    governed_palette = (
        ("#06251a", "#123a2a", "#70e6b1"),
        ("#061d17", "#102f27", "#3fbf8a"),
        ("#111d11", "#263921", "#88b96a"),
    )
    for index, (label, subtitle, top, bottom) in enumerate(SCENE_LAYERS):
        depth_fill, face_fill, outline = governed_palette[index] if governed else ("#03100b", "#0a2419", COLORS["mint"])
        if governed:
            face_points = [
                (360, top + 44), (336, top + 55), (272, bottom - 29), (279, bottom - 10),
                (378, bottom + 43), (406, bottom + 48), (1278, bottom - 2),
                (1307, bottom - 13), (1354, top + 91), (1350, top + 74),
                (1142, top - 10), (1116, top - 13),
            ]
            depth_points = [(x, y + 24) for x, y in face_points]
            shadow_points = [(x, y + 38) for x, y in face_points]
            draw.polygon(shadow_points, fill="#020604")
            draw.line(shadow_points + [shadow_points[0]], fill="#0b1711", width=2, joint="curve")
            draw.polygon(depth_points, fill=depth_fill)
            draw.line(depth_points + [depth_points[0]], fill=outline, width=2, joint="curve")
            draw.polygon(face_points, fill=face_fill)
            draw.line(face_points + [face_points[0]], fill=outline, width=3, joint="curve")
            draw.line((360, top + 44, 336, top + 55, 272, bottom - 29), fill="#a8ffd4", width=2, joint="curve")
            draw.rounded_rectangle((49, top + 47, 287, top + 129), radius=20, fill="#04130d", outline="#315b49", width=1)
            draw.text((86, top + 62), label, font=label_font, fill=COLORS["text"])
            draw.text((86, top + 91), subtitle, font=subtitle_font, fill="#a8cbbd")
            draw.line((66, top + 65, 66, top + 111), fill=outline, width=4)
        else:
            draw.polygon(
                [(260, bottom - 10), (388, bottom + 59), (1288, bottom + 8), (1368, top + 108),
                 (1368, top + 127), (1294, bottom + 30), (384, bottom + 82), (260, bottom + 8)],
                fill=depth_fill,
                outline=outline,
            )
            draw.polygon(
                [(354, top + 55), (1128, top - 12), (1368, top + 98), (1288, bottom - 2),
                 (388, bottom + 49), (260, bottom - 20)],
                fill=face_fill,
                outline=outline,
            )
            draw.line((354, top + 55, 1128, top - 12, 1364, top + 97), fill="#a8ffd4", width=2)
            draw.text((70, top + 67), label, font=label_font, fill=COLORS["text"])
            draw.text((70, top + 96), subtitle, font=subtitle_font, fill="#a8cbbd")
            draw.line((50, top + 57, 50, top + 119), fill=outline, width=4)


def draw_orthogonal(draw: ImageDraw.ImageDraw, source: Node, target: Node, fill: str, width: int) -> None:
    sx, sy = center(source)
    tx, ty = center(target)
    if abs(tx - sx) >= abs(ty - sy):
        sx = source.x + source.w if tx > sx else source.x
        tx = target.x if tx > sx else target.x + target.w
        mid = (sx + tx) / 2
        points = [(sx, sy), (mid, sy), (mid, ty), (tx, ty)]
    else:
        sy = source.y + source.h if ty > sy else source.y
        ty = target.y if ty > sy else target.y + target.h
        mid = (sy + ty) / 2
        points = [(sx, sy), (sx, mid), (tx, mid), (tx, ty)]
    draw.line(points, fill=fill, width=width, joint="curve")
    if len(points) >= 2:
        x1, y1 = points[-2]
        x2, y2 = points[-1]
        if abs(x2 - x1) > abs(y2 - y1):
            sign = 1 if x2 > x1 else -1
            arrow = [(x2, y2), (x2 - sign * 10, y2 - 6), (x2 - sign * 10, y2 + 6)]
        else:
            sign = 1 if y2 > y1 else -1
            arrow = [(x2, y2), (x2 - 6, y2 - sign * 10), (x2 + 6, y2 - sign * 10)]
        draw.polygon(arrow, fill=fill)


GOVERNED_GIF_ROUTES = {
    "r1": [(204, 425), (218, 441)],
    "r2": [(330, 441), (344, 457)],
    "r3": [(456, 457), (470, 473)],
    "r4": [(582, 473), (596, 489)],
    "r5": [(708, 489), (722, 505)],
    "r10": [(834, 505), (848, 521)],
    "r6": [(960, 506), (972, 500), (968, 452), (974, 440)],
    "r7": [(960, 536), (972, 542), (968, 584), (974, 598)],
    "r8": [(1086, 440), (1094, 444), (1092, 510), (1100, 522)],
    "r9": [(1086, 598), (1094, 590), (1092, 544), (1100, 538)],
    "r11": [(778, 580), (846, 668), (1028, 690), (1156, 612)],
    "r12": [(1212, 537), (1226, 553)],
    "r13": [(1338, 553), (1352, 569)],
}


def draw_polyline_arrow(draw: ImageDraw.ImageDraw, points: list[tuple[int, int]], fill: str, width: int) -> None:
    draw.line(points, fill=fill, width=width, joint="curve")
    x1, y1 = points[-2]
    x2, y2 = points[-1]
    angle = math.atan2(y2 - y1, x2 - x1)
    size = 13 if width >= 4 else 10
    wing = 0.55
    arrow = [
        (x2, y2),
        (x2 - size * math.cos(angle - wing), y2 - size * math.sin(angle - wing)),
        (x2 - size * math.cos(angle + wing), y2 - size * math.sin(angle + wing)),
    ]
    draw.polygon(arrow, fill=fill)


def draw_governed_gif_accents(draw: ImageDraw.ImageDraw, active_edges: set[str]) -> None:
    route_color = "#78e867"
    draw.line([(166, 330), (166, 222), (604, 222), (604, 405)], fill=route_color, width=2, joint="curve")
    draw.line([(596, 270), (596, 228), (1326, 228), (1326, 469)], fill=route_color, width=2, joint="curve")
    label_font = load_font(14, True)
    small_font = load_font(10)
    draw.text((226, 190), "IDENTITY", font=label_font, fill="#8bf06d")
    draw.text((310, 194), "Access · permissions · roles", font=small_font, fill="#74c961")
    draw.text((626, 200), "POLICY", font=label_font, fill="#8bf06d")
    draw.text((696, 204), "Governance · compliance · risk", font=small_font, fill="#74c961")
    draw.text((1158, 200), "STATE", font=label_font, fill="#8bf06d")
    draw.text((1215, 204), "Context · session · memory", font=small_font, fill="#74c961")

    return_points = [(1404, 644), (1404, 748), (1370, 803), (1230, 886), (1162, 898), (195, 744), (155, 699), (155, 514)]
    draw.line(return_points, fill="#416b21", width=12, joint="curve")
    draw_polyline_arrow(draw, return_points, "#c9ff42", 4)
    draw.text((520, 818), "EVIDENCE RETURN · LOGS · STATE · PROOF", font=load_font(13, True), fill="#a9ff43")

    payload_title_font = load_font(14, True)
    payload_font = load_font(10)
    for box, title, lines in (
        ((205, 588, 395, 696), "REQUEST PAYLOAD", ("• userId", "• intent", "• context + metadata")),
        ((738, 700, 943, 818), "EVIDENCE PAYLOAD", ("• execution logs + outputs", "• attestations + hashes", "• approvals + receipts")),
    ):
        left, top, right, bottom = box
        draw.rounded_rectangle(box, radius=12, fill="#03100c", outline="#27c997", width=2)
        draw.text((left + 18, top + 15), title, font=payload_title_font, fill="#f4f1e9")
        for line_index, line in enumerate(lines):
            draw.text((left + 22, top + 47 + line_index * 18), line, font=payload_font, fill="#d8fff0")

    legend_font = load_font(11)
    draw.rounded_rectangle((48, 812, 358, 964), radius=16, fill="#03100c", outline="#27c997", width=1)
    for y, color, text in (
        (846, "#b8ff39", "Request / response"),
        (884, "#78e867", "Identity / policy route"),
        (922, "#c9ff42", "Evidence return"),
        (946, "#ffc76a", "Human approval"),
    ):
        draw.line((72, y, 152, y), fill=color, width=3)
        draw.text((174, y), text, font=legend_font, fill="#d4e2dc", anchor="lm")


def draw_governed_gif_icon(draw: ImageDraw.ImageDraw, node: Node) -> None:
    label = f"{node.id} {node.title}".lower()
    cx = int(node.x + node.w / 2)
    cy = node.y + 42
    color = "#d8fff0"
    width = 3
    if "workspace" in label:
        draw.ellipse((cx - 5, cy - 13, cx + 5, cy - 3), outline=color, width=width)
        draw.ellipse((cx - 19, cy - 9, cx - 11, cy - 1), outline=color, width=2)
        draw.ellipse((cx + 11, cy - 9, cx + 19, cy - 1), outline=color, width=2)
        draw.arc((cx - 11, cy - 3, cx + 11, cy + 21), 190, 350, fill=color, width=width)
        draw.arc((cx - 27, cy, cx - 9, cy + 18), 195, 315, fill=color, width=2)
        draw.arc((cx + 9, cy, cx + 27, cy + 18), 225, 345, fill=color, width=2)
    elif "compiler" in label:
        draw.ellipse((cx - 16, cy - 12, cx + 16, cy + 15), outline=color, width=width)
        draw.line((cx - 5, cy - 11, cx - 5, cy + 14), fill=color, width=2)
        draw.line((cx + 5, cy - 11, cx + 5, cy + 14), fill=color, width=2)
    elif "workflow" in label:
        for dx, dy in ((0, -12), (-15, 10), (15, 10)):
            draw.ellipse((cx + dx - 4, cy + dy - 4, cx + dx + 4, cy + dy + 4), outline=color, width=2)
        draw.line((cx, cy - 8, cx, cy), fill=color, width=2)
        draw.line((cx, cy, cx - 15, cy + 6), fill=color, width=2)
        draw.line((cx, cy, cx + 15, cy + 6), fill=color, width=2)
    elif "agents" in label:
        draw.rounded_rectangle((cx - 13, cy - 10, cx + 13, cy + 9), radius=5, outline=color, width=width)
        draw.line((cx, cy - 17, cx, cy - 10), fill=color, width=2)
        draw.ellipse((cx - 2, cy - 19, cx + 2, cy - 15), fill=color)
        draw.ellipse((cx - 7, cy - 3, cx - 4, cy), fill=color)
        draw.ellipse((cx + 4, cy - 3, cx + 7, cy), fill=color)
    elif node.id == "mcp":
        draw.ellipse((cx - 12, cy - 13, cx + 12, cy - 3), outline=color, width=2)
        draw.line((cx - 12, cy - 8, cx - 12, cy + 12), fill=color, width=2)
        draw.line((cx + 12, cy - 8, cx + 12, cy + 12), fill=color, width=2)
        draw.arc((cx - 12, cy + 4, cx + 12, cy + 15), 0, 180, fill=color, width=2)
        draw.arc((cx - 12, cy - 2, cx + 12, cy + 9), 0, 180, fill=color, width=2)
    elif any(word in label for word in ("policy", "approval", "identity")):
        points = [(cx, cy - 16), (cx + 13, cy - 10), (cx + 12, cy + 2), (cx, cy + 17), (cx - 12, cy + 2), (cx - 13, cy - 10)]
        draw.line(points + [points[0]], fill=color, width=width, joint="curve")
        draw.line((cx - 6, cy, cx - 1, cy + 5, cx + 8, cy - 6), fill=color, width=2, joint="curve")
    elif any(word in label for word in ("evidence", "outcome")):
        draw.rounded_rectangle((cx - 10, cy - 15, cx + 10, cy + 15), radius=2, outline=color, width=width)
        for offset, length in ((-7, 12), (0, 12), (7, 8)):
            draw.line((cx - 5, cy + offset, cx - 5 + length, cy + offset), fill=color, width=2)
    elif any(word in label for word in ("orchestrator", "runtime")):
        draw.ellipse((cx - 9, cy - 9, cx + 9, cy + 9), outline=color, width=2)
        draw.ellipse((cx - 3, cy - 3, cx + 3, cy + 3), outline=color, width=2)
        for dx, dy in ((0, -16), (0, 16), (-16, 0), (16, 0), (-11, -11), (11, 11), (11, -11), (-11, 11)):
            draw.line((cx + dx * 0.55, cy + dy * 0.55, cx + dx, cy + dy), fill=color, width=2)
    elif any(word in label for word in ("studio", "code")):
        draw.line((cx - 6, cy - 13, cx - 17, cy, cx - 6, cy + 13), fill=color, width=width, joint="curve")
        draw.line((cx + 6, cy - 13, cx + 17, cy, cx + 6, cy + 13), fill=color, width=width, joint="curve")
        draw.line((cx + 5, cy - 17, cx - 5, cy + 17), fill=color, width=2)
    else:
        draw.ellipse((cx - 7, cy - 15, cx + 7, cy - 1), outline=color, width=width)
        draw.arc((cx - 16, cy - 2, cx + 16, cy + 24), 185, 355, fill=color, width=width)


def write_image_first_gif(diagram: Diagram) -> None:
    config = IMAGE_FIRST_CONFIGS[diagram.slug]
    master = Image.open(config.master).convert("RGBA")
    caption_height = 104
    frame_size = (IMAGE_MASTER_WIDTH, IMAGE_MASTER_HEIGHT + caption_height)
    caption_title = load_font(24, True)
    caption_font = load_font(17)
    edge_kinds = {edge.id: edge.kind for edge in diagram.edges}
    frames: list[Image.Image] = []

    for index, step in enumerate(diagram.steps):
        frame = Image.new("RGBA", frame_size, (3, 11, 8, 255))
        frame.alpha_composite(master, (0, 0))
        overlay = Image.new("RGBA", master.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        for edge_id in step.edges:
            edge = next(item for item in diagram.edges if item.id == edge_id)
            points = image_route_points(diagram, edge, config)
            color = (255, 199, 106) if edge_kinds.get(edge_id) in {"governance", "waiting"} else (184, 255, 57)
            draw.line(points, fill=(*color, 42), width=20, joint="curve")
            draw.line(points, fill=(*color, 105), width=10, joint="curve")
            draw.line(points, fill=(*color, 245), width=4, joint="curve")
            x, y = points[-1]
            draw.polygon([(x, y), (x - 13, y - 8), (x - 13, y + 8)], fill=(*color, 245))

        for node_id in set(step.nodes):
            hotspot = config.hotspots.get(node_id)
            if not hotspot:
                continue
            x, y, radius = hotspot
            color = (255, 199, 106) if node_id == "policy" else (184, 255, 57)
            draw.ellipse(
                (x - radius - 13, y - radius - 13, x + radius + 13, y + radius + 13),
                outline=(*color, 46),
                width=11,
            )
            draw.ellipse(
                (x - radius - 5, y - radius - 5, x + radius + 5, y + radius + 5),
                outline=(*color, 230),
                width=4,
            )

        frame.alpha_composite(overlay, (0, 0))
        caption = ImageDraw.Draw(frame)
        caption.rectangle(
            (0, IMAGE_MASTER_HEIGHT, IMAGE_MASTER_WIDTH, frame_size[1]),
            fill=(3, 11, 8, 255),
        )
        caption.line(
            (0, IMAGE_MASTER_HEIGHT, IMAGE_MASTER_WIDTH, IMAGE_MASTER_HEIGHT),
            fill=(34, 80, 59, 255),
            width=2,
        )
        caption.text(
            (34, IMAGE_MASTER_HEIGHT + 16),
            f"{index + 1:02d}  {step.title}",
            font=caption_title,
            fill=(184, 255, 57, 255),
        )
        caption.text(
            (34, IMAGE_MASTER_HEIGHT + 57),
            textwrap.fill(step.caption, width=132),
            font=caption_font,
            fill=(205, 222, 213, 255),
        )
        frames.append(frame.convert("RGB"))

    frames[0].save(
        OUT / f"{diagram.slug}.gif",
        save_all=True,
        append_images=frames[1:],
        duration=GIF_FRAME_DURATION_MS,
        loop=0,
        disposal=2,
        optimize=True,
    )


def write_gif(diagram: Diagram) -> None:
    if image_config(diagram):
        write_image_first_gif(diagram)
        return

    brand_font = load_font(29, True)
    title_font = load_font(15, True)
    subtitle_font = load_font(11)
    node_title_font = load_font(13, True)
    node_sub_font = load_font(9)
    caption_title = load_font(18, True)
    caption_font = load_font(11)
    visual_nodes = scene_nodes(diagram)
    nodes = {node.id: node for node in visual_nodes}
    frames: list[Image.Image] = []
    for index, step in enumerate(diagram.steps):
        image = Image.new("RGB", (WIDTH, HEIGHT + 90), COLORS["bg"])
        draw = ImageDraw.Draw(image)
        for x in range(0, WIDTH + 1, 60):
            draw.line((x, 0, x, HEIGHT), fill="#10231e", width=1)
        for y in range(0, HEIGHT + 1, 60):
            draw.line((0, y, WIDTH, y), fill="#10231e", width=1)
        if diagram.slug == "governed-run":
            governed_brand = load_font(43, True)
            draw.text((WIDTH // 2, 28), "CONTEXTWEAVER — GOVERNED CALL FLOW", font=governed_brand, fill="#f4f1e9", anchor="ma")
            draw.text((WIDTH // 2, 86), "Every request carries identity, policy, state, and proof", font=load_font(21, True), fill="#a9aeb1", anchor="ma")
        else:
            draw.text((48, 24), "CONTEXTWEAVER", font=brand_font, fill=COLORS["text"])
            draw.text((50, 59), diagram.title.upper(), font=title_font, fill=COLORS["mint"])
            draw.text((50, 84), diagram.subtitle, font=subtitle_font, fill=COLORS["muted"])
        draw_glass_decks(draw, governed=diagram.slug == "governed-run")
        active_edges = set(step.edges)
        active_nodes = set(step.nodes)
        for edge in diagram.edges:
            color = COLORS["line"]
            line_width = 2
            if edge.id in active_edges:
                color = {
                    "governance": COLORS["amber"],
                    "success": COLORS["mint"],
                    "waiting": COLORS["amber"],
                    "evidence": "#d8fff0",
                }.get(edge.kind, COLORS["sky"])
                line_width = 5
            if diagram.slug == "governed-run":
                draw_polyline_arrow(draw, GOVERNED_GIF_ROUTES[edge.id], color, line_width)
            else:
                draw_orthogonal(draw, nodes[edge.source], nodes[edge.target], color, line_width)
        if diagram.slug == "governed-run":
            draw_governed_gif_accents(draw, active_edges)
        for node in visual_nodes:
            active = node.id in active_nodes
            stroke = COLORS[node.color] if active else "#568572"
            fill = COLORS["panel2"] if active else "#10271e"
            box = (node.x, node.y, node.x + node.w, node.y + node.h)
            if diagram.slug == "governed-run":
                x, y, w, h = node.x, node.y, node.w, node.h
                cube_stroke = "#ffc76a" if node.color == "amber" else "#70e6b1"
                if active:
                    cube_stroke = "#ffc76a" if node.color == "amber" else "#9dff71"
                draw.rounded_rectangle((x - 16, y + 16, x + w - 16, y + h + 16), radius=17, fill="#0a2418", outline="#315f47", width=1)
                draw.rounded_rectangle((x - 8, y + 8, x + w - 8, y + h + 8), radius=17, fill="#0c2f20", outline=cube_stroke, width=1)
                draw.polygon([(x - 13, y + h - 7), (x + w + 9, y + h - 7), (x + w + 22, y + h + 14), (x - 2, y + h + 14)], fill="#0b2519", outline=cube_stroke)
                draw.polygon([(x + 8, y + 5), (x + 23, y - 13), (x + w - 9, y - 13), (x + w + 8, y + 5)], fill="#173b29", outline=cube_stroke)
                draw.polygon([(x + w - 1, y + 10), (x + w + 10, y + 1), (x + w + 10, y + h - 13), (x + w - 1, y + h)], fill="#07160f", outline=cube_stroke)
                face_fill = "#3a2408" if node.color == "amber" else fill
                draw.rounded_rectangle(box, radius=18, fill=face_fill, outline=cube_stroke, width=5 if active else 3)
                draw.line((x + 15, y + 7, x + w - 15, y + 7), fill="#b4ffda", width=2)
                draw.ellipse((x - 8, y - 31, x + 24, y + 1), fill="#07100b", outline="#ffc76a" if node.color == "amber" else "#d9ff38", width=3)
                draw.text((x + 8, y - 15), GOVERNED_NODE_NUMBERS[node.id], font=load_font(15, True), fill="#ffcb68" if node.color == "amber" else "#f1ffad", anchor="mm")
            else:
                draw.rounded_rectangle(
                    (node.x - 10, node.y + 7, node.x + node.w - 10, node.y + node.h + 7),
                    radius=15,
                    fill="#082017",
                    outline=stroke,
                    width=1,
                )
                draw.rounded_rectangle(
                    (node.x - 5, node.y + 3, node.x + node.w - 5, node.y + node.h + 3),
                    radius=15,
                    fill="#0a2a1d",
                    outline=stroke,
                    width=1,
                )
                depth = 10
                draw.polygon(
                    [
                        (node.x + 10, node.y + node.h),
                        (node.x + node.w, node.y + node.h),
                        (node.x + node.w - 11, node.y + node.h + depth),
                        (node.x + 21, node.y + node.h + depth),
                    ],
                    fill="#030806",
                    outline=stroke,
                )
                draw.rounded_rectangle(box, radius=15, fill=fill, outline=stroke, width=5 if active else 2)
                draw.line((node.x + 16, node.y + 7, node.x + node.w - 16, node.y + 7), fill="#b4ffda", width=1)
            if diagram.slug == "governed-run":
                draw_governed_gif_icon(draw, node)
            else:
                draw.ellipse((node.x + node.w / 2 - 10, node.y + 11, node.x + node.w / 2 + 10, node.y + 31), outline="#d8fff0", width=2)
                draw.line((node.x + node.w / 2 - 5, node.y + 21, node.x + node.w / 2 + 5, node.y + 21), fill="#d8fff0", width=2)
                draw.line((node.x + node.w / 2, node.y + 16, node.x + node.w / 2, node.y + 26), fill="#d8fff0", width=2)
            compact = node.h < 100
            title_top = 62 if diagram.slug == "governed-run" else 34 if compact else 42
            title_bottom = 113 if diagram.slug == "governed-run" else 73
            subtitle_top = 112 if diagram.slug == "governed-run" else 66 if compact else 75
            draw_wrapped(draw, (node.x + 8, node.y + title_top, node.x + node.w - 8, node.y + title_bottom), node.title, node_title_font, COLORS["text"], max_lines=2)
            draw_wrapped(draw, (node.x + 8, node.y + subtitle_top, node.x + node.w - 8, node.y + node.h - 4), node.subtitle, node_sub_font, "#a8cbbd", max_lines=1 if compact else 2)
        if diagram.slug != "governed-run":
            legend_font = load_font(11)
            legend_items = ((58, COLORS["mint"], "Data / Execution"), (238, COLORS["amber"], "Authorization / Approvals"), (488, "#e8fff5", "Evidence / State"))
            for x, color, text in legend_items:
                draw.ellipse((x - 6, 908, x + 6, 920), fill=color)
                draw.text((x + 15, 906), text, font=legend_font, fill="#d4e2dc")
        draw.rectangle((0, HEIGHT, WIDTH, HEIGHT + 90), fill=COLORS["panel2"])
        draw.text((24, HEIGHT + 14), f"{index + 1}/{len(diagram.steps)}  {step.title}", font=caption_title, fill=COLORS["mint"])
        wrapped = textwrap.fill(step.caption, width=145)
        draw.text((24, HEIGHT + 43), wrapped, font=caption_font, fill=COLORS["text"])
        frames.append(image)
    frames[0].save(
        OUT / f"{diagram.slug}.gif",
        save_all=True,
        append_images=frames[1:],
        duration=GIF_FRAME_DURATION_MS,
        loop=0,
        optimize=True,
    )


def drawio_style(node: Node) -> str:
    stroke = COLORS[node.color]
    return f"rounded=1;whiteSpace=wrap;html=1;shadow=1;glass=1;arcSize=16;fillColor={COLORS['panel']};gradientColor={COLORS['panel2']};gradientDirection=north;strokeColor={stroke};strokeWidth=2;fontSize=14;fontFamily=Inter;fontColor={COLORS['text']};align=center;verticalAlign=middle;spacing=10;"


def write_drawio(diagrams: tuple[Diagram, ...]) -> None:
    mxfile = ET.Element("mxfile", host="app.diagrams.net", version="26.0.0")
    for diagram in diagrams:
        visual_nodes = scene_nodes(diagram)
        page = ET.SubElement(mxfile, "diagram", id=diagram.slug, name=diagram.title)
        config = image_config(diagram)
        page_width = IMAGE_MASTER_WIDTH if config else WIDTH
        page_height = IMAGE_MASTER_HEIGHT if config else HEIGHT
        model = ET.SubElement(page, "mxGraphModel", dx="1600", dy="1000", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth=str(page_width), pageHeight=str(page_height))
        root = ET.SubElement(model, "root")
        ET.SubElement(root, "mxCell", id="0")
        ET.SubElement(root, "mxCell", id="1", parent="0")
        if config:
            background = ET.SubElement(
                root,
                "mxCell",
                id=f"{diagram.slug}-approved-master",
                value="",
                style=f"shape=image;verticalLabelPosition=bottom;verticalAlign=top;imageAspect=0;aspect=fixed;image={image_master_data_uri(config)};",
                vertex="1",
                parent="1",
                locked="1",
            )
            ET.SubElement(
                background,
                "mxGeometry",
                x="0",
                y="0",
                width=str(IMAGE_MASTER_WIDTH),
                height=str(IMAGE_MASTER_HEIGHT),
                **{"as": "geometry"},
            )
            for node_id, (x, y, radius) in config.hotspots.items():
                hotspot = ET.SubElement(
                    root,
                    "mxCell",
                    id=f"{diagram.slug}-{node_id}",
                    value=escape(next((node.title for node in diagram.nodes if node.id == node_id), node_id.title())),
                    style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=none;strokeColor=#b8ff39;strokeWidth=2;dashed=1;opacity=28;fontColor=none;",
                    vertex="1",
                    parent="1",
                )
                ET.SubElement(
                    hotspot,
                    "mxGeometry",
                    x=str(x - radius),
                    y=str(y - radius),
                    width=str(radius * 2),
                    height=str(radius * 2),
                    **{"as": "geometry"},
                )
            for edge in diagram.edges:
                edge_color = COLORS["amber"] if edge.kind in {"governance", "waiting"} else "#b8ff39"
                route = ET.SubElement(
                    root,
                    "mxCell",
                    id=f"{diagram.slug}-{edge.id}",
                    value=escape(edge.label),
                    style=f"edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;endFill=1;strokeWidth=3;strokeColor={edge_color};dashed=1;opacity=34;fontSize=10;fontFamily=Inter;fontColor=#d4e2dc;",
                    edge="1",
                    parent="1",
                    source=f"{diagram.slug}-{edge.source}",
                    target=f"{diagram.slug}-{edge.target}",
                )
                ET.SubElement(route, "mxGeometry", relative="1", **{"as": "geometry"})
            continue
        title = ET.SubElement(root, "mxCell", id=f"{diagram.slug}-title", value=f"<b>{escape(diagram.title)}</b><br>{escape(diagram.subtitle)}", style=f"text;html=1;strokeColor=none;fillColor=none;whiteSpace=wrap;fontSize=18;fontFamily=Inter;fontColor={COLORS['text']};align=left;verticalAlign=middle;", vertex="1", parent="1")
        ET.SubElement(title, "mxGeometry", x="35", y="20", width="1100", height="60", **{"as": "geometry"})
        for node in visual_nodes:
            cell = ET.SubElement(root, "mxCell", id=f"{diagram.slug}-{node.id}", value=f"<b>{escape(node.title)}</b><br>{escape(node.subtitle)}", style=drawio_style(node), vertex="1", parent="1")
            ET.SubElement(cell, "mxGeometry", x=str(node.x), y=str(node.y), width=str(node.w), height=str(node.h), **{"as": "geometry"})
        for edge in diagram.edges:
            edge_color = {
                "governance": COLORS["amber"],
                "success": COLORS["mint"],
                "waiting": COLORS["amber"],
                "evidence": "#d8fff0",
            }.get(edge.kind, COLORS["sky"])
            dashed = "1" if edge.kind in {"governance", "waiting", "evidence"} else "0"
            cell = ET.SubElement(
                root,
                "mxCell",
                id=f"{diagram.slug}-{edge.id}",
                value=escape(edge.label),
                style=f"edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;endFill=1;strokeWidth=2;strokeColor={edge_color};dashed={dashed};fontSize=10;fontFamily=Inter;fontColor={COLORS['muted']};",
                edge="1",
                parent="1",
                source=f"{diagram.slug}-{edge.source}",
                target=f"{diagram.slug}-{edge.target}",
            )
            ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})
    ET.indent(mxfile, space="  ")
    tree = ET.ElementTree(mxfile)
    tree.write(OUT / "contextweaver-public-architecture.drawio", encoding="utf-8", xml_declaration=True)


def main(*, skip_raster: bool = False) -> None:
    for diagram in DIAGRAMS:
        write_static_svg(diagram)
        write_interactive_html(diagram)
        if not skip_raster:
            write_gif(diagram)
    write_drawio(DIAGRAMS)
    raster_status = "using committed GIF assets" if skip_raster else "with regenerated GIF assets"
    print(f"Generated {len(DIAGRAMS)} interactive diagrams {raster_status}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skip-raster",
        action="store_true",
        help="Keep committed GIF assets while regenerating deterministic text and vector outputs.",
    )
    main(skip_raster=parser.parse_args().skip_raster)
