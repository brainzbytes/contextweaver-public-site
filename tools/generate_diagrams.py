from __future__ import annotations

import argparse
import json
import textwrap
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from html import escape
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "diagrams"
OUT.mkdir(parents=True, exist_ok=True)

WIDTH = 1200
HEIGHT = 720
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
    "danger": "#ff7188",
}

FONT_STACK = 'Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'


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


def n(id_: str, title: str, subtitle: str, detail: str, x: int, y: int, w: int, h: int, color: str = "mint") -> Node:
    return Node(id_, title, subtitle, detail, x, y, w, h, color)


def e(id_: str, source: str, target: str, label: str = "", kind: str = "data") -> Edge:
    return Edge(id_, source, target, label, kind)


DIAGRAMS = (
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
        "A user-facing Solution action resolves a reusable Service while identity, policy, data, Agents, MCP tools, approvals, durable state, and evidence remain explicit.",
        (
            n("intent", "Solution action", "Experience contract · inputs · purpose", "Accept one published experience action and governed handles. Resolve the user, client, tenant, groups, roles, relationships, device, session, delegation, purpose, and current authority.", 40, 100, 175, 105, "sky"),
            n("understand", "Understand", "Intent · risk · entities · needs", "Produce a typed interpretation. Model output is advisory and cannot assign endpoints, credentials, scope, privilege, or policy.", 255, 100, 175, 105, "mint"),
            n("compile", "Resolve + compile", "Service · Workflow · bindings · budgets", "Map the Solution action to an eligible Service and approved Workflow, or constrained-compose approved nodes. Validate the DAG, schemas, conditions, barriers, fallbacks, data bindings, and report constructability.", 470, 100, 175, 105, "violet"),
            n("authorize", "Authorize", "Whole graph · use-time policy", "Enumerate every reachable capability, source, model, tool class, side effect, approval, disclosure, environment, and region before dispatch.", 685, 100, 175, 105, "amber"),
            n("plan", "Immutable plan", "Pins · hashes · envelopes · expiry", "Freeze exact versions, policy decisions, field projections, fallback sets, RAG scopes, model envelopes, budgets, approvals, expiry, and revocation epoch.", 900, 100, 225, 105, "coral"),
            n("rag", "Authorized context", "Sources · ACL/RLS · citations", "Retrieve only current, purpose-authorized, classification-aware, source-authoritative evidence with in-query access filters and immutable generation pins.", 65, 330, 190, 110, "sky"),
            n("agents", "Parallel Agents", "Typed tasks · accepted artifacts", "Dispatch ready nodes through durable commands. Each specialist sees only its typed task and authorized context and produces a validated immutable artifact.", 300, 330, 190, 110, "violet"),
            n("approval", "Human authority", "Review · decision · correction", "Pause durably for the exact action, proposal, evidence, assignment, expiry, and action hash. The requester cannot self-approve restricted actions.", 535, 330, 190, 110, "amber"),
            n("mcp", "MCP gateway", "Tool · identity · credentials · receipt", "Resolve the approved capability and exact tool, reauthorize arguments and side-effect risk, perform scoped token exchange, keep credentials out of the Agent, and validate the result.", 770, 330, 190, 110, "coral"),
            n("state", "Durable runtime", "Queue · inbox/outbox · checkpoints", "Persist authoritative run state, commands, events, leases, idempotency, artifacts, waits, callbacks, retries, Saga journal, and compensation evidence.", 1005, 330, 155, 110, "mint"),
            n("finalize", "Canonical outcome", "Validate · disclose · render", "Bind terminal artifacts and citations deterministically, validate one canonical result, apply disclosure policy, render approved formats, and reauthorize delivery.", 280, 555, 255, 105, "mint"),
            n("evidence", "Run evidence", "Lineage · receipts · policy · telemetry", "Preserve plan and release identity, artifacts, citations, decisions, approvals, provider receipts, compensation, evaluations, metrics, logs, traces, warnings, and cost.", 665, 555, 255, 105, "amber"),
        ),
        (
            e("r1", "intent", "understand", "classify"),
            e("r2", "understand", "compile", "select / compose"),
            e("r3", "compile", "authorize", "manifest", "governance"),
            e("r4", "authorize", "plan", "freeze", "governance"),
            e("r5", "plan", "rag", "authorized scopes", "governance"),
            e("r6", "plan", "state", "commit"),
            e("r7", "rag", "agents", "context + citations"),
            e("r8", "agents", "approval", "high-impact action", "waiting"),
            e("r9", "approval", "mcp", "approved operation", "success"),
            e("r10", "agents", "mcp", "tool intent"),
            e("r11", "mcp", "state", "receipt + result", "evidence"),
            e("r12", "state", "agents", "resume / retry"),
            e("r13", "agents", "finalize", "accepted artifacts", "success"),
            e("r14", "state", "finalize", "run state"),
            e("r15", "finalize", "evidence", "release", "success"),
            e("r16", "evidence", "state", "observe + improve", "evidence"),
        ),
        (
            Step("Resolve identity and typed intent", "The platform accepts a bounded request, resolves current authority, and treats model classification as advisory structured data.", ("intent", "understand"), ("r1",)),
            Step("Build and authorize the complete plan", "The compiler selects or constrained-composes eligible capabilities, validates every contract and binding, evaluates the whole graph, and freezes exact versions.", ("understand", "compile", "authorize", "plan"), ("r2", "r3", "r4")),
            Step("Commit durable state and authorized context", "The run, plan, first commands or approval, and outbox commit before acceptance; retrieval returns only policy-eligible current evidence.", ("plan", "state", "rag"), ("r5", "r6")),
            Step("Execute specialists in parallel", "Ready Agents receive typed tasks and bounded context, then return schema-valid immutable artifacts rather than unrestricted conversation history.", ("rag", "agents", "state"), ("r7", "r12")),
            Step("Hold consequential authority with a human", "A high-impact action waits durably for an independently assigned reviewer to decide the exact proposal and evidence hash.", ("agents", "approval"), ("r8",)),
            Step("Invoke tools without giving Agents credentials", "The MCP gateway reauthorizes the exact call, performs scoped token exchange, records the provider receipt, minimizes the result, and returns provenance.", ("approval", "mcp", "state"), ("r9", "r11")),
            Step("Finalize one stable outcome", "The Finalizer binds accepted artifacts and citations, validates the canonical result, applies disclosure policy, and renders only approved channels.", ("agents", "state", "finalize"), ("r13", "r14")),
            Step("Attach evidence and improve safely", "The result carries reproducible identity and evidence while metrics, traces, evaluations, and lifecycle signals improve future routing without rewriting history.", ("finalize", "evidence", "state"), ("r15", "r16")),
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


def svg_node(node: Node, interactive: bool = False) -> str:
    title_lines = text_lines(node.title, max(16, int(node.w / 10)))
    subtitle_lines = text_lines(node.subtitle, max(20, int(node.w / 8)))
    title_y = node.y + 31
    title_markup = "".join(
        f'<tspan x="{node.x + node.w / 2}" dy="{0 if i == 0 else 17}">{escape(line)}</tspan>'
        for i, line in enumerate(title_lines)
    )
    subtitle_y = title_y + len(title_lines) * 17 + 7
    subtitle_markup = "".join(
        f'<tspan x="{node.x + node.w / 2}" dy="{0 if i == 0 else 14}">{escape(line)}</tspan>'
        for i, line in enumerate(subtitle_lines[:3])
    )
    attrs = (
        f' role="button" tabindex="0" aria-label="{escape(node.title)}" data-node-id="{node.id}"'
        if interactive else ""
    )
    return f"""
    <g id="node-{node.id}" class="node node-{node.color}"{attrs}>
      <rect x="{node.x}" y="{node.y}" width="{node.w}" height="{node.h}" rx="16"/>
      <text class="node-title" x="{node.x + node.w / 2}" y="{title_y}">{title_markup}</text>
      <text class="node-subtitle" x="{node.x + node.w / 2}" y="{subtitle_y}">{subtitle_markup}</text>
    </g>"""


def svg_content(diagram: Diagram, interactive: bool = False) -> str:
    nodes = node_map(diagram)
    edges = []
    for edge in diagram.edges:
        label_x = (center(nodes[edge.source])[0] + center(nodes[edge.target])[0]) / 2
        label_y = (center(nodes[edge.source])[1] + center(nodes[edge.target])[1]) / 2 - 8
        edges.append(
            f'<g id="edge-{edge.id}" class="edge edge-{edge.kind}" data-edge-id="{edge.id}">'
            f'<path d="{edge_path(edge, nodes)}" marker-end="url(#arrow)"/>'
            + (f'<text x="{label_x:.1f}" y="{label_y:.1f}">{escape(edge.label)}</text>' if edge.label else "")
            + "</g>"
        )
    node_markup = "".join(svg_node(node, interactive) for node in diagram.nodes)
    return f"""
    <svg class="architecture" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="diagram-title diagram-desc">
      <title id="diagram-title">{escape(diagram.title)}</title>
      <desc id="diagram-desc">{escape(diagram.subtitle)}</desc>
      <defs>
        <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
          <path d="M0,0 L0,6 L9,3 z" fill="context-stroke"/>
        </marker>
        <filter id="glow"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      </defs>
      <rect width="{WIDTH}" height="{HEIGHT}" fill="{COLORS['bg']}"/>
      <g class="grid-lines" opacity=".22">
        {''.join(f'<path d="M {x} 0 V {HEIGHT}"/>' for x in range(0, WIDTH + 1, 60))}
        {''.join(f'<path d="M 0 {y} H {WIDTH}"/>' for y in range(0, HEIGHT + 1, 60))}
      </g>
      <text class="diagram-title" x="36" y="46">{escape(diagram.title)}</text>
      <text class="diagram-subtitle" x="36" y="72">{escape(diagram.subtitle)}</text>
      <g class="edges">{''.join(edges)}</g>
      <g class="nodes">{node_markup}</g>
    </svg>"""


SVG_STYLE = f"""
  .grid-lines path {{ stroke:{COLORS['line']}; stroke-width:1; }}
  .diagram-title {{ fill:{COLORS['text']}; font:700 24px {FONT_STACK}; }}
  .diagram-subtitle {{ fill:{COLORS['muted']}; font:12px {FONT_STACK}; }}
  .node rect {{ fill:{COLORS['panel']}; stroke:{COLORS['line']}; stroke-width:2; }}
  .node-mint rect {{ stroke:{COLORS['mint']}; }} .node-sky rect {{ stroke:{COLORS['sky']}; }}
  .node-amber rect {{ stroke:{COLORS['amber']}; }} .node-violet rect {{ stroke:{COLORS['violet']}; }}
  .node-coral rect {{ stroke:{COLORS['coral']}; }}
  .node-title {{ fill:{COLORS['text']}; font:700 14px {FONT_STACK}; text-anchor:middle; }}
  .node-subtitle {{ fill:{COLORS['muted']}; font:10px {FONT_STACK}; text-anchor:middle; }}
  .edge path {{ fill:none; stroke:{COLORS['line']}; stroke-width:2.5; }}
  .edge text {{ fill:{COLORS['muted']}; font:9px {FONT_STACK}; text-anchor:middle; paint-order:stroke; stroke:{COLORS['bg']}; stroke-width:4; }}
  .edge-governance path {{ stroke:{COLORS['violet']}; stroke-dasharray:8 6; }}
  .edge-success path {{ stroke:{COLORS['mint']}; }} .edge-evidence path {{ stroke:{COLORS['amber']}; stroke-dasharray:5 5; }}
  .edge-waiting path {{ stroke:{COLORS['amber']}; stroke-dasharray:10 7; }}
"""


def write_static_svg(diagram: Diagram) -> None:
    content = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}">'
        f"<style>{SVG_STYLE}</style>"
        + svg_content(diagram).replace(
            f'<svg class="architecture" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="diagram-title diagram-desc">',
            '<g role="img" aria-labelledby="diagram-title diagram-desc">',
            1,
        ).rsplit("</svg>", 1)[0]
        + "</g></svg>"
    )
    (OUT / f"{diagram.slug}.svg").write_text(content, encoding="utf-8", newline="\n")


def write_interactive_html(diagram: Diagram) -> None:
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
*{{box-sizing:border-box}}body{{margin:0;color:var(--text);background:var(--bg);font:14px/1.5 {FONT_STACK}}}button{{font:inherit}}
.shell{{display:grid;grid-template-columns:minmax(0,1fr) 300px;min-height:720px}}.canvas{{position:relative;overflow:auto;border-right:1px solid var(--line)}}.architecture{{display:block;min-width:840px;width:100%;height:auto}}
{SVG_STYLE}
.node{{cursor:pointer}}.node rect,.edge path{{transition:.3s}}.node:hover rect,.node.selected rect{{stroke-width:4}}.node.active rect{{stroke-width:5;filter:url(#glow)}}.node.complete{{opacity:.66}}
.edge{{opacity:.24}}.edge.active{{opacity:1}}.edge.active path{{stroke-width:5;stroke-dasharray:14 9;animation:flow .75s linear infinite;filter:url(#glow)}}.edge-governance.active path{{stroke:var(--violet)}}.edge-success.active path{{stroke:var(--mint)}}.edge-waiting.active path,.edge-evidence.active path{{stroke:var(--amber)}}
@keyframes flow{{to{{stroke-dashoffset:-23}}}}
.panel{{display:flex;flex-direction:column;min-width:0;background:linear-gradient(180deg,var(--panel2),var(--bg))}}.panel-head{{padding:20px;border-bottom:1px solid var(--line)}}.eyebrow{{margin:0 0 7px;color:var(--mint);font-size:9px;font-weight:900;letter-spacing:.15em;text-transform:uppercase}}h1{{margin:0;font:700 25px/1.08 {FONT_STACK}}}.panel-head p{{margin:8px 0 0;color:var(--muted);font-size:11px}}
.detail{{min-height:210px;padding:20px;border-bottom:1px solid var(--line)}}.detail b{{display:block;font:700 19px/1.2 {FONT_STACK}}}.detail em{{display:block;margin:7px 0 12px;color:var(--amber);font-size:10px;font-style:normal;font-weight:800}}.detail p{{margin:0;color:#c8d6d0;font-size:12px}}
.stage{{flex:1;padding:20px}}.stage-count{{color:var(--mint);font-size:10px;font-weight:900;letter-spacing:.12em;text-transform:uppercase}}.stage h2{{margin:8px 0;font:700 21px/1.18 {FONT_STACK}}}.stage p{{margin:0;color:var(--muted);font-size:12px}}
.controls{{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;padding:12px;border-top:1px solid var(--line)}}.controls button{{min-height:39px;border:1px solid var(--line);border-radius:9px;color:var(--text);background:var(--panel);cursor:pointer;font-size:11px;font-weight:800}}.controls button:hover{{border-color:var(--mint)}}.controls .primary{{color:#07110f;background:var(--mint)}}
.dots{{display:flex;flex-wrap:wrap;gap:6px;padding:0 18px 16px}}.dot{{width:10px;height:10px;padding:0;border:0;border-radius:50%;background:var(--line);cursor:pointer}}.dot.active{{background:var(--mint);box-shadow:0 0 10px var(--mint)}}
@media(max-width:900px){{.shell{{grid-template-columns:1fr}}.canvas{{border-right:0;border-bottom:1px solid var(--line)}}.panel{{min-height:440px}}.architecture{{min-width:760px}}}}
@media(prefers-reduced-motion:reduce){{*{{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}}}
</style></head>
<body><main class="shell">
<section class="canvas">{svg_content(diagram, interactive=True)}</section>
<aside class="panel" aria-live="polite">
  <div class="panel-head"><p class="eyebrow">Interactive architecture</p><h1>{escape(diagram.title)}</h1><p>{escape(diagram.subtitle)}</p></div>
  <div class="detail"><b id="detail-title">Select a component</b><em id="detail-subtitle">Click or use the keyboard</em><p id="detail-copy">Every component remains readable while the animation is paused. Select a node for its responsibility and trust boundary.</p></div>
  <div class="stage"><span class="stage-count" id="stage-count"></span><h2 id="stage-title"></h2><p id="stage-caption"></p></div>
  <div class="controls"><button id="prev" type="button" aria-label="Previous stage">Previous</button><button id="play" class="primary" type="button">Pause</button><button id="next" type="button" aria-label="Next stage">Next</button><button id="reset" type="button">Reset</button></div>
  <div class="dots" id="dots" aria-label="Diagram stages"></div>
</aside></main>
<script>
const nodes={json.dumps(nodes_json, ensure_ascii=False)};
const steps={json.dumps(steps_json, ensure_ascii=False)};
let current=0,playing=!matchMedia("(prefers-reduced-motion: reduce)").matches,timer;
const $=id=>document.getElementById(id);
const nodeEls=[...document.querySelectorAll(".node")],edgeEls=[...document.querySelectorAll(".edge")];
function inspect(id){{const d=nodes[id];if(!d)return;nodeEls.forEach(el=>el.classList.toggle("selected",el.dataset.nodeId===id));$("detail-title").textContent=d.title;$("detail-subtitle").textContent=d.subtitle;$("detail-copy").textContent=d.detail;}}
nodeEls.forEach(el=>{{el.addEventListener("click",()=>{{playing=false;$("play").textContent="Play";stop();inspect(el.dataset.nodeId)}});el.addEventListener("keydown",ev=>{{if(ev.key==="Enter"||ev.key===" "){{ev.preventDefault();el.click()}}}})}});
steps.forEach((_,i)=>{{const b=document.createElement("button");b.className="dot";b.type="button";b.setAttribute("aria-label",`Show stage ${{i+1}}`);b.onclick=()=>{{current=i;render();restart()}};$("dots").appendChild(b)}});
function render(){{const s=steps[current];nodeEls.forEach(el=>{{el.classList.toggle("active",s.nodes.includes(el.dataset.nodeId));el.classList.remove("selected");}});edgeEls.forEach(el=>el.classList.toggle("active",s.edges.includes(el.dataset.edgeId)));$("stage-count").textContent=`Stage ${{current+1}} of ${{steps.length}}`;$("stage-title").textContent=s.title;$("stage-caption").textContent=s.caption;[...$("dots").children].forEach((d,i)=>d.classList.toggle("active",i===current));if(s.nodes.length)inspect(s.nodes[s.nodes.length-1]);}}
function advance(delta=1){{current=(current+delta+steps.length)%steps.length;render()}}function stop(){{clearInterval(timer)}}function restart(){{stop();if(playing)timer=setInterval(()=>advance(),4200)}}
$("prev").onclick=()=>{{advance(-1);restart()}};$("next").onclick=()=>{{advance();restart()}};$("reset").onclick=()=>{{current=0;render();restart()}};$("play").onclick=()=>{{playing=!playing;$("play").textContent=playing?"Pause":"Play";restart()}};
document.addEventListener("keydown",e=>{{if(e.target.closest(".node"))return;if(e.key==="ArrowRight")$("next").click();if(e.key==="ArrowLeft")$("prev").click();if(e.key===" "){{e.preventDefault();$("play").click()}}}});
$("play").textContent=playing?"Pause":"Play";render();restart();
</script></body></html>"""
    (OUT / f"{diagram.slug}.html").write_text(html, encoding="utf-8", newline="\n")


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


def write_gif(diagram: Diagram) -> None:
    title_font = load_font(22, True)
    subtitle_font = load_font(11)
    node_title_font = load_font(13, True)
    node_sub_font = load_font(9)
    caption_title = load_font(18, True)
    caption_font = load_font(11)
    nodes = node_map(diagram)
    frames: list[Image.Image] = []
    for index, step in enumerate(diagram.steps):
        image = Image.new("RGB", (WIDTH, HEIGHT + 90), COLORS["bg"])
        draw = ImageDraw.Draw(image)
        for x in range(0, WIDTH + 1, 60):
            draw.line((x, 0, x, HEIGHT), fill="#10231e", width=1)
        for y in range(0, HEIGHT + 1, 60):
            draw.line((0, y, WIDTH, y), fill="#10231e", width=1)
        draw.text((36, 28), diagram.title, font=title_font, fill=COLORS["text"])
        draw.text((36, 56), diagram.subtitle, font=subtitle_font, fill=COLORS["muted"])
        active_edges = set(step.edges)
        active_nodes = set(step.nodes)
        for edge in diagram.edges:
            color = COLORS["line"]
            line_width = 2
            if edge.id in active_edges:
                color = {
                    "governance": COLORS["violet"],
                    "success": COLORS["mint"],
                    "waiting": COLORS["amber"],
                    "evidence": COLORS["amber"],
                }.get(edge.kind, COLORS["sky"])
                line_width = 5
            draw_orthogonal(draw, nodes[edge.source], nodes[edge.target], color, line_width)
        for node in diagram.nodes:
            active = node.id in active_nodes
            stroke = COLORS[node.color] if active else COLORS["line"]
            fill = COLORS["panel2"] if active else COLORS["panel"]
            box = (node.x, node.y, node.x + node.w, node.y + node.h)
            draw.rounded_rectangle(box, radius=16, fill=fill, outline=stroke, width=5 if active else 2)
            draw_wrapped(draw, (node.x + 8, node.y + 8, node.x + node.w - 8, node.y + 55), node.title, node_title_font, COLORS["text"], max_lines=2)
            draw_wrapped(draw, (node.x + 8, node.y + 52, node.x + node.w - 8, node.y + node.h - 8), node.subtitle, node_sub_font, COLORS["muted"], max_lines=3)
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
    return f"rounded=1;whiteSpace=wrap;html=1;shadow=1;arcSize=16;fillColor={COLORS['panel']};strokeColor={stroke};strokeWidth=2;fontSize=14;fontFamily=Inter;fontColor={COLORS['text']};align=center;verticalAlign=middle;spacing=10;"


def write_drawio(diagrams: tuple[Diagram, ...]) -> None:
    mxfile = ET.Element("mxfile", host="app.diagrams.net", version="26.0.0")
    for diagram in diagrams:
        page = ET.SubElement(mxfile, "diagram", id=diagram.slug, name=diagram.title)
        model = ET.SubElement(page, "mxGraphModel", dx="1600", dy="1000", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth=str(WIDTH), pageHeight=str(HEIGHT))
        root = ET.SubElement(model, "root")
        ET.SubElement(root, "mxCell", id="0")
        ET.SubElement(root, "mxCell", id="1", parent="0")
        title = ET.SubElement(root, "mxCell", id=f"{diagram.slug}-title", value=f"<b>{escape(diagram.title)}</b><br>{escape(diagram.subtitle)}", style=f"text;html=1;strokeColor=none;fillColor=none;whiteSpace=wrap;fontSize=18;fontFamily=Inter;fontColor={COLORS['text']};align=left;verticalAlign=middle;", vertex="1", parent="1")
        ET.SubElement(title, "mxGeometry", x="35", y="20", width="1100", height="60", **{"as": "geometry"})
        for node in diagram.nodes:
            cell = ET.SubElement(root, "mxCell", id=f"{diagram.slug}-{node.id}", value=f"<b>{escape(node.title)}</b><br>{escape(node.subtitle)}", style=drawio_style(node), vertex="1", parent="1")
            ET.SubElement(cell, "mxGeometry", x=str(node.x), y=str(node.y), width=str(node.w), height=str(node.h), **{"as": "geometry"})
        for edge in diagram.edges:
            edge_color = {
                "governance": COLORS["violet"],
                "success": COLORS["mint"],
                "waiting": COLORS["amber"],
                "evidence": COLORS["amber"],
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
