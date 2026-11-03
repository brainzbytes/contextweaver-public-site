from __future__ import annotations

import argparse
from pathlib import Path

import generate_diagrams as diagrams


ROOT = Path(__file__).resolve().parents[1]
SPATIAL = ROOT / "assets" / "media" / "spatial"
SPATIAL.mkdir(parents=True, exist_ok=True)


def node(id_: str, title: str, subtitle: str, x: int, y: int, color: str = "mint") -> diagrams.Node:
    return diagrams.n(id_, title, subtitle, subtitle, x, y, 150, 100, color)


def edge(id_: str, source: str, target: str, label: str = "", kind: str = "data") -> diagrams.Edge:
    return diagrams.e(id_, source, target, label, kind)


def static_step() -> tuple[diagrams.Step, ...]:
    return (diagrams.Step("Architecture", "Static architecture master.", (), ()),)


STATIC_SPATIAL_DIAGRAMS = (
    diagrams.Diagram(
        "layered-governed-architecture",
        "Layered Governed Architecture",
        "Experience channels compose governed capabilities across Cerebro, Weave, and Loom.",
        (
            node("portal", "Portal", "Experience channel", 40, 100),
            node("ide", "IDE", "Developer channel", 260, 100),
            node("api", "API", "Programmatic channel", 480, 100),
            node("assistant", "Assistant", "Conversational channel", 700, 100),
            node("intent", "Intent", "Bounded request", 40, 340),
            node("identity", "Identity", "Principal and authority", 220, 340),
            node("compiler", "Compiler", "Typed execution plan", 400, 340),
            node("policy", "Policy", "Rules and guardrails", 580, 340),
            node("registry", "Registry", "Approved versions", 760, 340),
            node("approval", "Approval Gate", "Independent review", 940, 340, "amber"),
            node("workflows", "Workflows", "Durable coordination", 40, 620),
            node("agents", "Agents", "Specialist reasoning", 190, 620),
            node("mcp", "MCP", "Tools and resources", 340, 620),
            node("evidence", "Evidence", "Receipts and traces", 490, 620),
            node("kubernetes", "Kubernetes", "Portable runtime", 640, 620),
            node("models", "Models + Knowledge", "LLMs · Vector DB · Graph", 790, 620),
            node("systems", "Enterprise Systems", "ERP · CRM · Apps", 940, 620),
            node("infrastructure", "Infrastructure", "Compute · Storage · Cloud", 1090, 620),
        ),
        (
            edge("l1", "portal", "intent", "intent"),
            edge("l2", "ide", "compiler"),
            edge("l3", "api", "policy", kind="governance"),
            edge("l4", "assistant", "intent"),
            edge("l5", "intent", "identity", kind="governance"),
            edge("l6", "identity", "policy", kind="governance"),
            edge("l7", "compiler", "registry"),
            edge("l8", "policy", "approval", kind="approval"),
            edge("l9", "registry", "workflows"),
            edge("l10", "workflows", "agents"),
            edge("l11", "workflows", "mcp"),
            edge("l12", "agents", "evidence", kind="evidence"),
            edge("l13", "mcp", "systems"),
            edge("l14", "kubernetes", "infrastructure"),
            edge("l15", "models", "agents"),
            edge("l16", "evidence", "portal", "evidence", "evidence"),
        ),
        static_step(),
    ),
    diagrams.Diagram(
        "governed-platform-city",
        "Governed Platform",
        "Cerebro governs, Weave composes, and Loom runs across enterprise and cloud systems.",
        (
            node("salesforce", "Salesforce", "Enterprise system", 40, 100),
            node("sap", "SAP", "Enterprise system", 190, 100),
            node("servicenow", "ServiceNow", "Enterprise system", 340, 100),
            node("m365", "Microsoft 365", "Enterprise system", 490, 100),
            node("aws", "AWS", "Cloud platform", 640, 100),
            node("snowflake", "Snowflake", "Data platform", 790, 100),
            node("databases", "Databases", "Enterprise data", 940, 100),
            node("solutions", "Solutions", "User-facing compositions", 40, 340),
            node("services", "Services", "Reusable contracts", 240, 340),
            node("cerebro", "Cerebro Control Plane", "Intent · Identity · Policy · Registry", 440, 340),
            node("workflows", "Workflows", "Durable coordination", 640, 340),
            node("approval", "Human Approval", "Independent decision", 840, 340, "amber"),
            node("loom", "Loom Foundation", "Portable substrate", 40, 620),
            node("evidence", "Evidence Fabric", "Receipts and traces", 240, 620),
            node("knowledge", "Knowledge + Models", "RAG · Memory · Models", 440, 620),
            node("mcp", "MCP Gateways", "Tools and resources", 640, 620),
            node("agents", "Agents", "Specialist execution", 840, 620),
            node("history", "Run History", "Status and observability", 1040, 620),
        ),
        (
            edge("p1", "salesforce", "solutions"),
            edge("p2", "sap", "solutions"),
            edge("p3", "servicenow", "services"),
            edge("p4", "m365", "services"),
            edge("p5", "solutions", "cerebro"),
            edge("p6", "services", "cerebro"),
            edge("p7", "cerebro", "workflows"),
            edge("p8", "cerebro", "approval", kind="approval"),
            edge("p9", "workflows", "agents"),
            edge("p10", "agents", "mcp"),
            edge("p11", "knowledge", "agents"),
            edge("p12", "loom", "workflows"),
            edge("p13", "mcp", "aws"),
            edge("p14", "mcp", "snowflake"),
            edge("p15", "mcp", "databases"),
            edge("p16", "workflows", "evidence", kind="evidence"),
            edge("p17", "evidence", "history", kind="evidence"),
        ),
        static_step(),
    ),
    diagrams.Diagram(
        "governed-call-flow",
        "Governed Call Flow",
        "Every request carries identity, policy, state, and proof.",
        (
            node("channel", "User / Channel", "Request and purpose", 40, 100),
            node("solution", "Solution API", "Published action", 240, 100),
            node("identity", "Identity + Intent", "Principal and bounded request", 440, 100),
            node("policy", "Policy Decision", "Authorize reachable graph", 640, 100, "amber"),
            node("compiler", "Workflow Compiler", "Typed execution plan", 40, 340),
            node("coordinator", "Run Coordinator", "Durable state", 240, 340),
            node("agent", "Agent Runtime", "Specialist reasoning", 440, 340),
            node("mcp", "MCP Gateway", "Tools and credentials", 640, 340),
            node("system", "Enterprise System", "Consequential side effect", 40, 620),
            node("approval", "Human Approval", "Review · approve · deny", 240, 620, "amber"),
            node("evidence", "Evidence Store", "Logs · state · proof", 440, 620),
            node("outcome", "Outcome", "Approved and provable", 640, 620),
        ),
        (
            edge("c1", "channel", "solution"),
            edge("c2", "solution", "identity"),
            edge("c3", "identity", "policy", kind="governance"),
            edge("c4", "policy", "compiler", kind="approval"),
            edge("c5", "compiler", "coordinator"),
            edge("c6", "coordinator", "agent"),
            edge("c7", "coordinator", "mcp"),
            edge("c8", "agent", "system"),
            edge("c9", "mcp", "system"),
            edge("c10", "system", "approval", kind="approval"),
            edge("c11", "approval", "evidence", kind="evidence"),
            edge("c12", "evidence", "outcome", kind="success"),
            edge("c13", "outcome", "channel", "evidence return", "evidence"),
        ),
        static_step(),
    ),
    diagrams.Diagram(
        "governed-sequence-ladder",
        "Governed Sequence",
        "The sequence preserves identity, authorization, parallel work, approval, evidence, and outcome.",
        (
            node("s1", "1 · Submit intent", "Channel → Cerebro", 40, 100),
            node("s2", "2 · Resolve identity", "Cerebro", 240, 100),
            node("s3", "3 · Authorize plan", "Cerebro → Coordinator", 440, 100, "amber"),
            node("s4", "4 · Dispatch workflow", "Coordinator → Agent", 640, 100),
            node("s5", "5 · Invoke Agent", "Parallel execution", 40, 340),
            node("s6", "6 · Request MCP tool", "Agent → MCP Gateway", 240, 340),
            node("s7", "7 · Approval required", "Governed wait", 440, 340, "amber"),
            node("s8", "8 · Execute side effect", "MCP → Enterprise System", 640, 340),
            node("s9", "9 · Return receipt", "Enterprise System → Agent", 40, 620),
            node("s10", "10 · Persist evidence", "Agent → Evidence", 240, 620),
            node("s11", "11 · Return outcome", "Cerebro → Channel", 440, 620),
            node("participants", "Participants", "Channel · Cerebro · Coordinator · Agent · MCP · System", 640, 620),
        ),
        tuple(
            edge(f"q{index}", f"s{index}", f"s{index + 1}", kind="approval" if index in {3, 7} else "data")
            for index in range(1, 11)
        ),
        static_step(),
    ),
    diagrams.Diagram(
        "durable-saga-flow",
        "Durable Saga Flow",
        "Parallel work, governed waits, safe recovery, and complete evidence.",
        (
            node("identity", "Identity", "Who can do what", 40, 100),
            node("policy", "Policy", "Rules and guardrails", 260, 100),
            node("governance", "Governance", "Compliance · audit · controls", 480, 100),
            node("intent", "1 · Intent", "User request", 40, 340),
            node("compile", "2 · Compile Plan", "Tasks and dependencies", 190, 340),
            node("start", "3 · Start Run", "Initialize Saga", 340, 340),
            node("readiness", "4A · Readiness Agent", "Validate · prepare · check", 490, 340),
            node("risk", "4B · Risk Agent", "Analyze · mitigate · guard", 640, 340),
            node("fetch", "4C · MCP Data Fetch", "Retrieve · transform · enrich", 790, 340),
            node("synthesis", "5 · Synthesis Agent", "Merge · reason · decide", 940, 340),
            node("approval", "6 · Human Approval", "Review · approve · deny", 1090, 340, "amber"),
            node("action", "7 · Enterprise Action", "Execute · integrate · commit", 1240, 340),
            node("evidence", "8 · Evidence + Outcome", "Logs · artifacts · results", 1390, 340),
            node("checkpoint", "Checkpoint", "Save progress", 40, 620),
            node("queue", "Queue", "Pending work", 240, 620),
            node("receipt", "Receipt", "Immutable record", 440, 620),
            node("history", "Run History", "Trace · search · audit", 640, 620),
            node("retry", "Retry", "Backoff and retry", 840, 620, "amber"),
            node("compensation", "Compensation", "Undo · revert · restore", 1040, 620, "danger"),
        ),
        (
            edge("d1", "identity", "policy", kind="governance"),
            edge("d2", "policy", "governance", kind="governance"),
            edge("d3", "intent", "compile"),
            edge("d4", "compile", "start"),
            edge("d5", "start", "readiness"),
            edge("d6", "start", "risk"),
            edge("d7", "start", "fetch"),
            edge("d8", "readiness", "synthesis"),
            edge("d9", "risk", "synthesis"),
            edge("d10", "fetch", "synthesis"),
            edge("d11", "synthesis", "approval", kind="approval"),
            edge("d12", "approval", "action", kind="approval"),
            edge("d13", "action", "evidence", kind="success"),
            edge("d14", "fetch", "retry", kind="approval"),
            edge("d15", "fetch", "compensation", kind="failure"),
            edge("d16", "compensation", "synthesis", "rejoin", "evidence"),
            edge("d17", "start", "checkpoint", kind="evidence"),
            edge("d18", "checkpoint", "queue", kind="evidence"),
            edge("d19", "queue", "receipt", kind="evidence"),
            edge("d20", "receipt", "history", kind="evidence"),
        ),
        static_step(),
    ),
)


def write_static_spatial(diagram: diagrams.Diagram, *, skip_raster: bool) -> None:
    png_path = SPATIAL / f"{diagram.slug}.png"
    svg_path = SPATIAL / f"{diagram.slug}.svg"
    if not png_path.exists():
        raise FileNotFoundError(f"Approved spatial master is missing: {png_path}")
    diagrams.write_static_svg(diagram)
    generated_svg = diagrams.OUT / f"{diagram.slug}.svg"
    svg_path.write_bytes(generated_svg.read_bytes())


def main(*, skip_raster: bool = False) -> None:
    intent_svg = diagrams.OUT / "intent-to-evidence.svg"
    (SPATIAL / "intent-to-evidence.svg").write_bytes(intent_svg.read_bytes())
    for diagram in STATIC_SPATIAL_DIAGRAMS:
        write_static_spatial(diagram, skip_raster=skip_raster)
    diagrams.write_drawio(
        STATIC_SPATIAL_DIAGRAMS,
        diagrams.OUT / "contextweaver-spatial-visuals.drawio",
    )
    print(f"Generated {len(STATIC_SPATIAL_DIAGRAMS)} standardized spatial architecture masters.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-raster", action="store_true")
    main(skip_raster=parser.parse_args().skip_raster)
