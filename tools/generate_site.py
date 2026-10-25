from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
CURRENT_DATE = "October 24, 2026"

NAV = (
    ("home", "Overview", "index.html"),
    ("platform", "Platform", "platform.html"),
    ("studio", "Studio", "studio.html"),
    ("runtime", "Runtime", "runtime.html"),
    ("governance", "Governance", "governance.html"),
    ("solutions", "Solutions", "solutions.html"),
    ("architecture", "Architecture", "architecture.html"),
)


def header() -> str:
    links = "".join(
        f'<a href="{href}" data-nav-page="{key}">{label}</a>'
        for key, label, href in NAV
    )
    return f"""
    <a class="skip-link" href="#main-content">Skip to content</a>
    <header class="site-header">
      <div class="nav-shell">
        <a class="brand" href="index.html" aria-label="ContextWeaver home">
          <span class="brand-mark" aria-hidden="true"></span>
          <span class="brand-copy"><strong>ContextWeaver</strong><span>by BrainzBytes</span></span>
        </a>
        <nav class="primary-nav" data-primary-nav aria-label="Primary navigation">{links}</nav>
        <div class="nav-actions">
          <button class="icon-button" type="button" data-theme-toggle aria-label="Change color theme">☀</button>
          <button class="menu-button" type="button" data-menu-toggle aria-label="Open navigation" aria-expanded="false">☰</button>
        </div>
      </div>
    </header>
    """


def footer() -> str:
    return f"""
    <footer class="site-footer">
      <div class="container footer-grid">
        <div>
          <a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true"></span><span class="brand-copy"><strong>ContextWeaver</strong><span>Governed capability platform</span></span></a>
          <p style="margin-top:16px">Turn specifications, enterprise information, Agents, MCPs, Workflows, models, policy, and infrastructure into governed, deployable Services with evidence attached.</p>
        </div>
        <div><h3>Explore</h3><div class="footer-links"><a href="platform.html">Platform model</a><a href="studio.html">Agent/MCP Studio</a><a href="runtime.html">Dynamic runtime</a></div></div>
        <div><h3>Trust</h3><div class="footer-links"><a href="governance.html">Governance</a><a href="architecture.html">Architecture</a><a href="architecture.html#downloads">Diagram downloads</a></div></div>
        <div><h3>Adopt</h3><div class="footer-links"><a href="solutions.html#individual">Individuals</a><a href="solutions.html#small-business">Small business</a><a href="solutions.html#enterprise">Enterprise</a></div></div>
      </div>
      <div class="container footer-bottom">
        <span>© 2026 BrainzBytes. ContextWeaver product architecture.</span>
        <span>Architecture refreshed {CURRENT_DATE}. Compliance and deployment outcomes remain customer-specific.</span>
      </div>
    </footer>
    """


def page(name: str, title: str, description: str, content: str) -> str:
    return dedent(f"""\
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width,initial-scale=1">
      <meta name="description" content="{description}">
      <meta name="theme-color" content="#07110f">
      <title>{title}</title>
      <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
      <link rel="stylesheet" href="assets/css/site.css?v=20261025-2">
    </head>
    <body data-page="{name}">
      {header()}
      <main id="main-content">
        {content}
      </main>
      {footer()}
      <script src="assets/js/site.js?v=20261025-2"></script>
    </body>
    </html>
    """).lstrip()


def diagram(name: str, title: str, note: str) -> str:
    return f"""
    <div class="diagram-shell" data-reveal>
      <div class="diagram-toolbar">
        <strong>{title}</strong>
        <a href="diagrams/{name}.html" target="_blank" rel="noopener">Open full screen ↗</a>
        <a href="diagrams/{name}.svg">Static SVG</a>
        <a href="diagrams/{name}.gif">Animated GIF</a>
      </div>
      <iframe class="diagram-frame" src="diagrams/{name}.html" title="{title}" loading="lazy"></iframe>
    </div>
    <p class="diagram-note">{note}</p>
    """


HOME = """
<section class="container hero">
  <div>
    <p class="eyebrow">The governed service factory</p>
    <h1>Turn any approved idea into a <em>working Service.</em></h1>
    <p class="lede">ContextWeaver brings specifications, enterprise knowledge, Agents, MCP tools, Workflows, models, policy, and cloud infrastructure into one governed lifecycle—from creation and dry run to deployment, execution, recovery, and evidence.</p>
    <div class="hero-actions">
      <a class="button primary" href="studio.html">Explore Agent/MCP Studio <span aria-hidden="true">→</span></a>
      <a class="button" href="architecture.html">Explore the architecture</a>
    </div>
    <div class="pills" style="margin-top:24px">
      <span class="pill">No-code GUI</span><span class="pill">VS Code + CLI</span><span class="pill">Jupyter</span><span class="pill">OpenAPI + MCP + A2A</span><span class="pill">Kubernetes + GitOps</span>
    </div>
  </div>
  <div class="hero-visual" aria-label="ContextWeaver product model">
    <div class="orbit-ring" aria-hidden="true"></div>
    <div class="orbit"><div><strong>Service</strong><span>Governed outcome</span></div></div>
    <div class="orbit-node n1"><b>Create</b><small>Studio + code</small></div>
    <div class="orbit-node n2"><b>Govern</b><small>Policy + approval</small></div>
    <div class="orbit-node n3"><b>Operate</b><small>Evidence + SLO</small></div>
    <div class="orbit-node n4"><b>Compose</b><small>Agents + MCPs</small></div>
  </div>
</section>
<div class="container trust-strip" aria-label="Supported creation inputs">
  <span>Specifications & RFCs</span><span>OpenAPI & AsyncAPI</span><span>Wikis & enterprise data</span><span>Agents & MCP servers</span><span>Models & solution packs</span>
</div>

<section class="container section">
  <div class="section-head">
    <div><p class="section-kicker">One product, complete lifecycle</p><h2>More than an AI answer. A governed business outcome.</h2></div>
    <p>A ContextWeaver run can return a typed result, citations, approvals, policy decisions, tool receipts, artifacts, retries, compensation evidence, metrics, logs, traces, and a durable audit trail.</p>
  </div>
  <div class="grid four">
    <article class="card mint" data-reveal><div class="meta">01 · Understand</div><h3>Make intent explicit</h3><p>Classify purpose, risk, data, entities, required capabilities, ambiguity, and approval needs before protected work begins.</p></article>
    <article class="card violet" data-reveal><div class="meta">02 · Compile</div><h3>Freeze an authorized plan</h3><p>Resolve exact compatible capability versions, validate typed contracts, bind data fields, and pin one immutable execution plan.</p></article>
    <article class="card amber" data-reveal><div class="meta">03 · Execute</div><h3>Coordinate durable work</h3><p>Run Agents in parallel, pause without wasting compute, call tools through governed gateways, retry safely, and compensate when required.</p></article>
    <article class="card coral" data-reveal><div class="meta">04 · Prove</div><h3>Attach evidence</h3><p>Preserve lineage, citations, policy and approval decisions, release digests, side-effect receipts, telemetry, and evaluation results.</p></article>
  </div>
</section>

<section class="container section compact">
  <div class="section-head">
    <div><p class="section-kicker">Interactive product map</p><h2>From raw material to trusted Service.</h2></div>
    <p>Use the controls, click any component, or open the full-screen version. The animation follows creation, admission, deployment, discovery, execution, and evidence.</p>
  </div>
  {service_factory}
</section>

<section class="container section">
  <div class="section-head">
    <div><p class="section-kicker">A platform for every scale</p><h2>Start with one useful tool. Grow without rebuilding the foundation.</h2></div>
    <p>The same contracts support a personal assistant, a small-business process, a multi-team enterprise platform, or an isolated sovereign deployment.</p>
  </div>
  <div class="grid three">
    <article class="card mint" data-reveal><div class="meta">Individual</div><h3>Build personal leverage</h3><p>Create a private research, planning, coding, or administration Service from your own approved sources and tools.</p><ul><li>Guided Studio experience</li><li>Personal workspaces and memory</li><li>Clear approvals before side effects</li></ul><a class="card-link" href="solutions.html#individual">See the individual path →</a></article>
    <article class="card amber" data-reveal><div class="meta">Small business</div><h3>Package repeatable operations</h3><p>Turn informal know-how into shared workflows for sales, support, finance, delivery, and back-office work.</p><ul><li>Reusable Service templates</li><li>Shared connectors and policies</li><li>Traceable outcomes without a platform team</li></ul><a class="card-link" href="solutions.html#small-business">See the business path →</a></article>
    <article class="card violet" data-reveal><div class="meta">Enterprise</div><h3>Govern an ecosystem</h3><p>Operate many tenants, capability publishers, model providers, data products, risk tiers, regions, and deployment profiles.</p><ul><li>Separation of duties</li><li>Immutable supply chain and evidence</li><li>Dedicated, sovereign, or disconnected profiles</li></ul><a class="card-link" href="solutions.html#enterprise">See the enterprise path →</a></article>
  </div>
</section>

<section class="container section compact">
  <div class="band" data-reveal>
    <p class="section-kicker">The central promise</p>
    <h2>ContextWeaver lets customers build their own AI capabilities while the platform safely discovers, validates, compiles, approves, orchestrates, recovers, observes, and proves every outcome.</h2>
    <div class="button-row"><a class="button primary" href="platform.html">See how the platform works</a><a class="button" href="governance.html">See the trust model</a></div>
  </div>
</section>
"""

PLATFORM = """
<section class="container hero" style="min-height:610px">
  <div>
    <p class="eyebrow">Product architecture</p>
    <h1>Three systems. One <em>governed fabric.</em></h1>
    <p class="lede"><strong>Cerebro</strong> understands and governs. <strong>Weave</strong> packages reusable Services, Workflows, Agents, MCPs, RAG profiles, models, and policies. <strong>Loom</strong> provides the portable Kubernetes, GitOps, data, messaging, identity, secrets, and observability foundation.</p>
  </div>
  <div class="grid" style="align-self:center">
    <article class="card mint"><div class="meta">Cerebro</div><h3>Think, govern, compile, orchestrate, prove.</h3><p>The experience and control plane that turns an authenticated intent into an authorized immutable execution plan and durable outcome.</p></article>
    <article class="card amber"><div class="meta">Weave</div><h3>Compose reusable capability building blocks.</h3><p>The governed catalog of Service definitions, Workflow graphs, Agents, MCP tools, data products, models, policies, and solution packs.</p></article>
    <article class="card violet"><div class="meta">Loom</div><h3>Run on a portable operational substrate.</h3><p>Kubernetes, Helm, OCI, GitOps, databases, queues, object stores, search, identity, secrets, telemetry, and provider adapters.</p></article>
  </div>
</section>

<section class="container section compact">
  <div class="section-head"><div><p class="section-kicker">Eight coordinated planes</p><h2>Stable product semantics above replaceable infrastructure.</h2></div><p>Cloud services implement platform contracts. They do not redefine identity, policy, Workflow, transaction, evidence, or lifecycle semantics.</p></div>
  {platform_planes}
</section>

<section class="container section">
  <div class="section-head"><div><p class="section-kicker">The planes</p><h2>Each layer has a precise responsibility and boundary.</h2></div><p>Separation makes the system easier to operate, replace, scale, audit, and reason about than a single unrestricted “AI application.”</p></div>
  <div class="grid four">
    <article class="card violet" data-reveal><div class="meta">01</div><h3>Experience</h3><p>Portal, admin, Studio, workspaces, research, run history, approvals, topology, and operations.</p></article>
    <article class="card amber" data-reveal><div class="meta">02</div><h3>Governance</h3><p>Identity context, entitlements, policy, admission, trust, approvals, audit, and separation of duties.</p></article>
    <article class="card sky" data-reveal><div class="meta">03</div><h3>Registry & composition</h3><p>Catalogs, schemas, alias resolution, compatibility, lifecycle, and immutable Workflow compilation.</p></article>
    <article class="card coral" data-reveal><div class="meta">04</div><h3>Agents & MCP</h3><p>Constrained reasoning, tool brokering, sandboxing, capability evaluation, and human authority.</p></article>
    <article class="card mint" data-reveal><div class="meta">05</div><h3>Workflow runtime</h3><p>Coordinator, task workers, queues, inbox/outbox, checkpoints, waits, Saga journal, and Finalizer.</p></article>
    <article class="card sky" data-reveal><div class="meta">06</div><h3>RAG, memory & models</h3><p>Governed sources, atomic generations, authorized retrieval, bounded memory, aliases, and providers.</p></article>
    <article class="card amber" data-reveal><div class="meta">07</div><h3>Evidence & operations</h3><p>Metrics, logs, traces, evaluations, cost, receipts, SLOs, alerts, and immutable audit export.</p></article>
    <article class="card violet" data-reveal><div class="meta">08</div><h3>Infrastructure</h3><p>Kubernetes, PostgreSQL, event bus, object storage, search, secrets, networking, and recovery.</p></article>
  </div>
</section>

<section class="container section compact">
  <div class="quote" data-reveal">Models can propose. They cannot grant themselves authority. The compiler and policy plane decide what is admissible; the runtime executes only the pinned plan.</div>
</section>

<section class="container section">
  <div class="section-head"><div><p class="section-kicker">Cloud neutral by contract</p><h2>Deploy where your risk, cost, data, and sovereignty require.</h2></div><p>The control plane uses portable specifications, OCI artifacts, Kubernetes APIs, Helm, GitOps, OpenTelemetry, and provider adapters.</p></div>
  <div class="grid four">
    <article class="card mint"><div class="meta">Azure</div><h3>AKS profile</h3><p>Azure identity, Key Vault, Blob, PostgreSQL/Cosmos adapters, AI Search, Azure OpenAI, and native networking.</p></article>
    <article class="card amber"><div class="meta">AWS</div><h3>EKS profile</h3><p>IAM, Secrets Manager, S3, PostgreSQL/Dynamo adapters, OpenSearch, Bedrock, and VPC integrations.</p></article>
    <article class="card sky"><div class="meta">Google Cloud</div><h3>GKE profile</h3><p>Workload Identity, Secret Manager, Cloud Storage, PostgreSQL, search/vector adapters, and Vertex AI.</p></article>
    <article class="card violet"><div class="meta">Private / sovereign</div><h3>Kubernetes profile</h3><p>Private clusters, OpenBao or native secrets, S3-compatible storage, PostgreSQL, Qdrant/OpenSearch, and local model endpoints.</p></article>
  </div>
</section>
"""

STUDIO = """
<section class="container hero" style="min-height:640px">
  <div>
    <p class="eyebrow">Agent + MCP Studio</p>
    <h1>Extend the platform <em>from inside the platform.</em></h1>
    <p class="lede">A guided GUI for non-programmers and a complete engineering path for developers. Start with a requirement, Swagger/OpenAPI file, RFC, wiki, product documentation, existing MCP server, code repository, or blank canvas.</p>
    <div class="hero-actions"><a class="button primary" href="#create">See the creation flow</a><a class="button" href="architecture.html#capability-lifecycle">See lifecycle architecture</a></div>
  </div>
  <div class="grid" style="align-self:center">
    <article class="card mint"><div class="meta">GUI</div><h3>Guided creation</h3><p>Describe the outcome, select sources and tools, review generated contracts, simulate, and submit through governance.</p></article>
    <article class="card sky"><div class="meta">Developer</div><h3>VS Code, CLI, SDK</h3><p>Author portable specs, schemas, tests, tool implementations, deployment overlays, and evaluation fixtures.</p></article>
    <article class="card violet"><div class="meta">Research</div><h3>Jupyter workspaces</h3><p>Explore approved data and models, validate retrieval, experiment with scoring, and convert work into governed assets.</p></article>
  </div>
</section>

<section id="create" class="container section compact">
  <div class="section-head"><div><p class="section-kicker">Create, dry run, publish</p><h2>One workspace for the complete capability lifecycle.</h2></div><p>Everything generated remains inspectable and editable: specifications, schemas, prompts, code, tests, policies, configuration references, Helm overlays, dashboards, and evidence.</p></div>
  {capability_lifecycle}
</section>

<section class="container section">
  <div class="section-head"><div><p class="section-kicker">What can be created</p><h2>Four asset types, designed to work together.</h2></div><p>The Studio makes the distinction clear so a tool is not confused with an Agent, and a Workflow is not mistaken for an unrestricted chat chain.</p></div>
  <div class="grid four">
    <article class="card sky" data-reveal><div class="meta">Specification</div><h3>The contract</h3><p>Identity, owner, inputs, outputs, errors, side effects, data classes, dependencies, SLOs, tests, support, and lifecycle.</p></article>
    <article class="card violet" data-reveal><div class="meta">Agent</div><h3>The reasoning capability</h3><p>A bounded task specialist with typed inputs and outputs, approved model envelopes, skills, evaluations, and resource limits.</p></article>
    <article class="card mint" data-reveal><div class="meta">MCP</div><h3>The tool capability</h3><p>A governed integration exposing tools, resources, and prompts with schemas, delegated identity, side-effect classes, receipts, and compensation.</p></article>
    <article class="card amber" data-reveal><div class="meta">Service + Workflow</div><h3>The customer outcome</h3><p>An executable product that composes typed steps, parallel work, decisions, waits, approvals, callbacks, retries, and finalization.</p></article>
  </div>
</section>

<section class="container section">
  <div class="section-head"><div><p class="section-kicker">Studio workspace</p><h2>Designed for hundreds of capabilities, not a handful of cards.</h2></div><p>Separate Agent and MCP catalogs support search, ownership, lifecycle, risk, health, version, environment, dependency, and entitlement filters.</p></div>
  <div class="grid two">
    <article class="card mint"><div class="meta">Agent catalog</div><h3>Find the right specialist</h3><ul><li>Search by capability, owner, domain, trust, region, model envelope, and evaluation</li><li>Compare exact versions, schemas, SLOs, support, and consumers</li><li>Inspect Agent Cards, dependencies, dashboards, and recent runs</li><li>Create, clone, modify, deprecate, drain, or retire through governed actions</li></ul></article>
    <article class="card violet"><div class="meta">MCP catalog</div><h3>Find the right tool boundary</h3><ul><li>Search by tool, provider, side-effect class, data scope, credential profile, and region</li><li>Inspect schemas, transports, rate limits, idempotency, receipts, and compensation</li><li>See every Service, Workflow, and Agent consumer before an update or removal</li><li>Test through a safe sandbox without exposing provider credentials to the Agent</li></ul></article>
  </div>
</section>

<section class="container section compact">
  <div class="band">
    <p class="section-kicker">Inputs to a new capability</p>
    <h2>Start from OpenAPI, AsyncAPI, MCP, source code, an RFC, product documentation, a wiki, a data product, an industry pack, or simply a described outcome.</h2>
    <div class="pills" style="margin-top:22px"><span class="pill">Import</span><span class="pill">Discover</span><span class="pill">Generate</span><span class="pill">Edit</span><span class="pill">Validate</span><span class="pill">Simulate</span><span class="pill">Scan</span><span class="pill">Approve</span><span class="pill">Publish</span><span class="pill">Deploy</span><span class="pill">Observe</span><span class="pill">Improve</span></div>
  </div>
</section>
"""

RUNTIME = """
<section class="container hero" style="min-height:650px">
  <div>
    <p class="eyebrow">Governed dynamic execution</p>
    <h1>Dynamic enough to adapt. <em>Bounded enough to trust.</em></h1>
    <p class="lede">ContextWeaver can select an approved Service or compose a constrained plan from admitted capabilities. The model may help propose the graph; identity, schemas, policy, compatibility, approvals, and the compiler determine whether it can run.</p>
    <div class="hero-actions"><a class="button primary" href="#flow">Walk through a run</a><a class="button" href="governance.html">Review the safeguards</a></div>
  </div>
  <div class="quote">Dependencies control when work may run. Schemas, explicit bindings, and field policy control what data each step receives.</div>
</section>

<section id="flow" class="container section compact">
  <div class="section-head"><div><p class="section-kicker">Prompt to proved outcome</p><h2>A run is a state machine, not a stream of hopeful messages.</h2></div><p>Click components and step through the active path. The diagram distinguishes identity and policy, authorized data, Agent reasoning, MCP side effects, approval, durable execution, and evidence.</p></div>
  {governed_run}
</section>

<section class="container section">
  <div class="section-head"><div><p class="section-kicker">Run lifecycle</p><h2>The simple view of a rigorous execution model.</h2></div><p>The full design contains more granular authorization, retrieval, binding, checkpoint, disclosure, and audit states; users see a comprehensible progression.</p></div>
  <div class="steps">
    <article class="step"><div><h3>Receive and scrutinize intent</h3><p>Resolve identity, tenant, roles, relationships, device, purpose, risk, classification, entities, ambiguity, and candidate outcomes.</p></div></article>
    <article class="step"><div><h3>Select or constrained-compose</h3><p>Choose an approved Service, ask a clarifying question, or propose a graph from only admitted capabilities and control nodes.</p></div></article>
    <article class="step"><div><h3>Compile and authorize the complete graph</h3><p>Validate schemas, field bindings, dependencies, fallback sets, budgets, RAG scopes, model envelopes, tool risk, and approvals.</p></div></article>
    <article class="step"><div><h3>Freeze the immutable plan</h3><p>Pin exact Service, Workflow, Agent, MCP, model, policy, schema, source, index, and configuration versions.</p></div></article>
    <article class="step"><div><h3>Commit the durable run</h3><p>Persist state, the plan, first tasks or approval request, and transactional outbox before returning acceptance.</p></div></article>
    <article class="step"><div><h3>Execute typed work</h3><p>Dispatch through persistent commands; run ready Agents in parallel; use bounded context; checkpoint accepted artifacts.</p></div></article>
    <article class="step"><div><h3>Invoke tools under delegated authority</h3><p>The MCP gateway validates the exact call, performs just-in-time token exchange, keeps credentials outside the Agent, and records receipts.</p></div></article>
    <article class="step"><div><h3>Finalize, disclose, and prove</h3><p>Validate one canonical result, apply disclosure policy and approval, render approved formats, persist evidence, and reauthorize delivery.</p></div></article>
  </div>
</section>

<section class="container section">
  <div class="section-head"><div><p class="section-kicker">Resilience by design</p><h2>Long-running work can wait, retry, resume, and compensate.</h2></div><p>Durability is a product contract rather than a best-effort property hidden inside an Agent loop.</p></div>
  <div class="grid three">
    <article class="card mint"><div class="meta">Durable waits</div><h3>Release compute while waiting</h3><p>Human approval, timer, callback, or external event state is persisted. The run resumes from authoritative state rather than holding an open process.</p></article>
    <article class="card amber"><div class="meta">At-least-once safety</div><h3>Replay without repeating side effects</h3><p>Inbox/outbox, leases, idempotency keys, accepted artifact hashes, and provider receipts let another worker safely continue after failure.</p></article>
    <article class="card coral"><div class="meta">Saga compensation</div><h3>Handle partial business failure</h3><p>Each side effect declares whether and how it can be compensated. Failed plans reverse approved actions or escalate explicit non-compensable state.</p></article>
  </div>
</section>
"""

GOVERNANCE = """
<section class="container hero" style="min-height:650px">
  <div>
    <p class="eyebrow">Governance built into execution</p>
    <h1>Authority is explicit. <em>Evidence is automatic.</em></h1>
    <p class="lede">Every protected human and workload action carries verified identity, tenant, purpose, policy version, correlation, and bounded authority. No prompt, model, Agent, tool, or generated package can expand its own privileges.</p>
  </div>
  <div class="grid" style="align-self:center">
    <article class="card violet"><div class="meta">Identity</div><h3>Who is acting?</h3><p>User, workload, tenant, role, group, relationship, device, session, delegation, and current revocation state.</p></article>
    <article class="card amber"><div class="meta">Policy</div><h3>What is permitted?</h3><p>Purpose, environment, region, data class, model, source, capability, operation, arguments, risk, and disclosure.</p></article>
    <article class="card mint"><div class="meta">Evidence</div><h3>What actually happened?</h3><p>Decision IDs, plan and artifact hashes, release digests, approvals, citations, receipts, evaluations, metrics, logs, and traces.</p></article>
  </div>
</section>

<section class="container section compact">
  <div class="section-head"><div><p class="section-kicker">Control model</p><h2>Five layers around every consequential tool call.</h2></div><p>Identity is resolved before the call, authority is checked at use time, credentials remain in the trusted gateway, and the result is minimized before returning to the Agent.</p></div>
  <div class="grid four">
    <article class="card sky"><div class="meta">01</div><h3>Authenticate</h3><p>OIDC, MFA, workload identity, current tenant and subject context.</p></article>
    <article class="card violet"><div class="meta">02</div><h3>Inject identity</h3><p>Bounded user, role, group, purpose, plan, node, delegation, and correlation context.</p></article>
    <article class="card amber"><div class="meta">03</div><h3>Broker credentials</h3><p>Just-in-time scoped exchange. Agents never receive provider tokens, cloud keys, connector secrets, or database credentials.</p></article>
    <article class="card coral"><div class="meta">04</div><h3>Evaluate policy</h3><p>Exact service, tool, operation, arguments, data, read/write risk, region, side effect, approval, and budget.</p></article>
    <article class="card mint"><div class="meta">05</div><h3>Validate and audit</h3><p>Schema-check inputs and outputs; minimize fields; attach provenance; record receipt, decision, latency, and result class.</p></article>
  </div>
</section>

<section class="container section">
  <div class="section-head"><div><p class="section-kicker">Non-negotiable safeguards</p><h2>Human authority remains human.</h2></div><p>These controls apply to platform engines and illustrate how ContextWeaver policy can encode customer-specific hard blocks.</p></div>
  <div class="grid three">
    <article class="card coral"><div class="meta">Hard block</div><h3>No autonomous high-severity acknowledgment</h3><p>Severity 0, 1, and 2 incidents cannot be automatically acknowledged by an Agent.</p></article>
    <article class="card coral"><div class="meta">Hard block</div><h3>No autonomous merge or production rollback</h3><p>Code merge and production rollback retain explicit independent human authority.</p></article>
    <article class="card coral"><div class="meta">Hard block</div><h3>No unreviewed sensitive communication or security change</h3><p>Customer communications and authentication or cryptography changes require qualified review.</p></article>
    <article class="card amber"><div class="meta">Separation of duty</div><h3>No self-approval</h3><p>The submitting or executing identity cannot approve its own restricted production action.</p></article>
    <article class="card amber"><div class="meta">Promotion</div><h3>Review before Enforce</h3><p>Engines begin in advisory Review mode. Promotion requires passing metrics, at least two clean evaluation weeks, and human approval.</p></article>
    <article class="card amber"><div class="meta">Auto-pause</div><h3>Stop after repeated evaluation failure</h3><p>Two consecutive evaluation failures automatically pause enforcement until review and recovery.</p></article>
  </div>
</section>

<section class="container section">
  <div class="section-head"><div><p class="section-kicker">Lifecycle governance</p><h2>Admission happens before deployment—and continues afterward.</h2></div><p>Capabilities are not trusted forever because one build passed. Runtime identity, canary health, evaluation, drift, support, and lifecycle remain part of eligibility.</p></div>
  <div class="steps">
    <article class="step"><div><h3>Validate the specification</h3><p>Strict identities, owners, versions, schemas, side effects, idempotency, compensation, dependencies, credential and resilience profiles.</p></div></article>
    <article class="step"><div><h3>Inspect the supply chain</h3><p>Trusted publisher, signatures, immutable digests, SBOM, dependencies, images, malware, secrets, licenses, provenance, and reproducibility.</p></div></article>
    <article class="step"><div><h3>Prove isolation and safety</h3><p>Restricted runtime, deny-default network, bounded identity, resource quota, malformed I/O, adversarial, duplicate, retry, restart, timeout, and recovery tests.</p></div></article>
    <article class="step"><div><h3>Approve by risk</h3><p>Data class, external authority, side effects, environment, tenant scope, residency, and human-authority requirements determine the decision path.</p></div></article>
    <article class="step"><div><h3>Qualify the live runtime</h3><p>Compare the live descriptor to the signed release; use synthetic and canary traffic; continuously evaluate health, quality, safety, SLO, and drift.</p></div></article>
    <article class="step"><div><h3>Drain and retire safely</h3><p>Block new resolution, preserve pinned work, revoke routes and authority, retain evidence, and remove resources according to retention policy.</p></div></article>
  </div>
</section>

<section class="container section compact">
  <div class="section-head"><div><p class="section-kicker">Architecture maturity</p><h2>Clear status instead of inflated claims.</h2></div><p>The product story distinguishes proven foundations, active implementation, and complete target architecture. Regulatory certification is never implied automatically.</p></div>
  <div class="status-grid">
    <article class="status implemented"><b>Implemented foundations</b><p>Persistent Registry and contracts, configuration discovery, platform UI foundations, governed identity patterns, durable execution slices, and current application capabilities.</p></article>
    <article class="status progress"><b>Active realization</b><p>Complete Agent/MCP admission, signed bundles, operator-owned deployment, isolated runtime profiles, full canary automation, drift correction, and lifecycle convergence.</p></article>
    <article class="status target"><b>Target architecture</b><p>Universal cross-industry packs, broad provider parity, complete disconnected profiles, exhaustive assurance automation, and production qualification by deployment profile.</p></article>
  </div>
</section>
"""

SOLUTIONS = """
<section class="container hero" style="min-height:660px">
  <div>
    <p class="eyebrow">One platform, many outcomes</p>
    <h1>Personal productivity to <em>enterprise operating model.</em></h1>
    <p class="lede">ContextWeaver scales the control plane around the customer. It does not force an individual to operate an enterprise stack, or force an enterprise to replace governance with a consumer chatbot.</p>
    <div class="hero-actions"><a class="button primary" href="#individual">Choose your starting point</a><a class="button" href="studio.html">See what you can build</a></div>
  </div>
  <div class="card mint"><div class="meta">A reusable pattern</div><h3>Core + profile + pack + tenant controls</h3><p>Platform core, deployment profile, jurisdiction and regulatory profile, industry ontology and policy pack, data/connectivity pack, solution templates, and tenant-specific configuration.</p><div class="pills" style="margin-top:18px"><span class="pill">Same contracts</span><span class="pill">Different assurance</span><span class="pill">Progressive isolation</span></div></div>
</section>

<section class="container section compact">
  <div class="section-head"><div><p class="section-kicker">Scale path</p><h2>Capability and governance grow together.</h2></div><p>Use the animation to see how identity, sharing, policy, evidence, isolation, and lifecycle controls evolve while the Service, Workflow, Agent, and MCP contracts stay stable.</p></div>
  {scale_path}
</section>

<section id="individual" class="container section">
  <div class="section-head"><div><p class="section-kicker">Individual</p><h2>Turn your own information and tools into reliable personal Services.</h2></div><p>Begin with guided templates and human confirmation. Keep sources, memory, credentials, and outcomes bounded to the person and purpose.</p></div>
  <div class="grid three">
    <article class="card mint"><h3>Research companion</h3><p>Register approved personal sources, retrieve with citations, compare evidence, and produce a traceable report.</p></article>
    <article class="card sky"><h3>Personal operations</h3><p>Plan travel, track commitments, prepare documents, summarize projects, or coordinate tasks with explicit approval before side effects.</p></article>
    <article class="card violet"><h3>Developer copilot</h3><p>Use code, documentation, repository context, test tools, and deployment workflows without exposing credentials to reasoning components.</p></article>
  </div>
</section>

<section id="small-business" class="container section">
  <div class="section-head"><div><p class="section-kicker">Small business</p><h2>Package how the business works, not just how one person prompts.</h2></div><p>Shared Services convert repeatable know-how into accountable workflows with ownership, permissions, quality checks, and operational visibility.</p></div>
  <div class="grid three">
    <article class="card amber"><h3>Customer operations</h3><p>Intake, classify, draft, approve, communicate, schedule, and preserve customer and service evidence.</p></article>
    <article class="card mint"><h3>Sales and finance</h3><p>Research, quote, invoice, reconcile, collect approvals, and invoke payment or accounting tools through bounded authority.</p></article>
    <article class="card sky"><h3>Delivery and support</h3><p>Turn requests into tasks, route specialists, track dependencies, manage exceptions, and produce a customer-ready outcome.</p></article>
  </div>
</section>

<section id="enterprise" class="container section">
  <div class="section-head"><div><p class="section-kicker">Enterprise</p><h2>Operate a governed capability ecosystem across teams, clouds, and risk tiers.</h2></div><p>Enterprises gain common contracts and evidence while preserving domain ownership, provider choice, data boundaries, and independent human authority.</p></div>
  <div class="grid four">
    <article class="card violet"><h3>Multi-tenant identity</h3><p>Role, attribute, relationship, purpose, environment, and delegated authority carried end to end.</p></article>
    <article class="card coral"><h3>Risk-tiered lifecycle</h3><p>Publisher trust, admission gates, independent approval, canary qualification, evaluation, drift, quarantine, and retirement.</p></article>
    <article class="card amber"><h3>Progressive isolation</h3><p>Shared SaaS, dedicated data plane, dedicated cluster/account, sovereign region, private datacenter, disconnected, or edge.</p></article>
    <article class="card mint"><h3>Attributable operations</h3><p>Quality, reliability, cost, usage, policy, model, data, tool, and business outcome by tenant and capability.</p></article>
  </div>
</section>

<section class="container section">
  <div class="section-head"><div><p class="section-kicker">Representative industry packs</p><h2>Adapt vocabulary and controls without forking the platform.</h2></div><p>Industry and regulatory packs supply ontologies, policy, data mappings, solution templates, evaluations, dashboards, evidence collectors, deployment guidance, and shared-responsibility boundaries.</p></div>
  <div class="grid four">
    <article class="card coral"><div class="meta">Healthcare & life sciences</div><h3>Provenance and qualified review</h3><p>PHI boundaries, consent, de-identification, scientific or clinical lineage, records retention, and FHIR/laboratory adapters.</p></article>
    <article class="card mint"><div class="meta">Banking & payments</div><h3>Integrity and dual control</h3><p>Transaction evidence, fraud and AML workflows, PCI boundaries, explainability, model risk, and immutable financial receipts.</p></article>
    <article class="card violet"><div class="meta">Government & defense</div><h3>Sovereignty and mission isolation</h3><p>Clearance boundaries, restricted regions, disconnected operation, records schedules, and higher-assurance deployment profiles.</p></article>
    <article class="card amber"><div class="meta">Telecom</div><h3>Multi-vendor service operations</h3><p>Inventory, topology, change control, outage workflows, TM Forum-aligned adapters, and customer communication evidence.</p></article>
    <article class="card sky"><div class="meta">Manufacturing & energy</div><h3>Safety and edge operations</h3><p>Plant and OT isolation, maintenance evidence, asset lineage, safety approval, edge execution, and industrial-control boundaries.</p></article>
    <article class="card coral"><div class="meta">Insurance</div><h3>Case evidence and fairness</h3><p>Underwriting and claims evidence, explainability, document lineage, adjuster authority, and jurisdiction-specific retention.</p></article>
    <article class="card mint"><div class="meta">Retail & consumer</div><h3>Consent and supply chain</h3><p>Privacy, personalization boundaries, PCI isolation, consumer rights, fraud, fulfillment, and supplier integration.</p></article>
    <article class="card violet"><div class="meta">Enterprise technology</div><h3>Software and production operations</h3><p>Code intelligence, incident response, dependency risk, spec review, release governance, developer automation, and SRE.</p></article>
  </div>
</section>
"""

ARCHITECTURE = """
<section class="container hero" style="min-height:590px">
  <div>
    <p class="eyebrow">Architecture explorer</p>
    <h1>Inspect the whole system. <em>Then zoom into the flow.</em></h1>
    <p class="lede">The diagrams below share one semantic model and ship in four formats: clickable interactive HTML, editable Draw.io, static SVG, and presentation-ready animated GIF.</p>
    <div class="hero-actions"><a class="button primary" href="#explore">Explore diagrams</a><a class="button" href="diagrams/contextweaver-public-architecture.drawio">Download editable Draw.io</a></div>
  </div>
  <div class="card amber"><div class="meta">Diagram semantics</div><h3>Motion communicates meaning.</h3><ul><li>Solid pulse: active request or data</li><li>Dashed pulse: identity, policy, or authorization</li><li>Green: validated output or success</li><li>Amber: approval, waiting, retry, or compensation</li><li>Red: denial or failed validation</li><li>Parallel pulses: concurrent Agent work</li></ul></div>
</section>

<section id="explore" class="container section compact">
  <div class="section-head"><div><p class="section-kicker">Interactive diagrams</p><h2>Clickable, controllable, and readable without animation.</h2></div><p>Every player supports Play, Pause, Next, Previous, Reset, stage selection, component inspection, keyboard focus, reduced motion, and a textual explanation.</p></div>
  <div style="display:grid;gap:50px">
    <section id="service-factory">{service_factory}</section>
    <section id="platform-planes">{platform_planes}</section>
    <section id="capability-lifecycle">{capability_lifecycle}</section>
    <section id="governed-run">{governed_run}</section>
    <section id="scale-path">{scale_path}</section>
  </div>
</section>

<section id="downloads" class="container section">
  <div class="section-head"><div><p class="section-kicker">Portable assets</p><h2>Use the architecture in reviews, proposals, presentations, and implementation planning.</h2></div><p>The editable source contains one Draw.io page per diagram. Static SVG works for print and documentation; GIF works when an interactive player is unavailable.</p></div>
  <div class="grid four">
    <article class="card mint"><div class="meta">Editable</div><h3>Draw.io source</h3><p>Four pages with semantic colors, orthogonal connectors, grouped boundaries, and stable component names.</p><a class="card-link" href="diagrams/contextweaver-public-architecture.drawio">Download .drawio →</a></article>
    <article class="card sky"><div class="meta">Interactive</div><h3>HTML + SVG players</h3><p>Deterministic stages, component details, manual controls, accessible captions, and reduced-motion behavior.</p><a class="card-link" href="diagrams/service-factory.html">Open a player →</a></article>
    <article class="card violet"><div class="meta">Documentation</div><h3>Static SVG</h3><p>Responsive vector fallback with all components and labels visible when animation or scripting is unavailable.</p><a class="card-link" href="diagrams/governed-run.svg">Open SVG →</a></article>
    <article class="card amber"><div class="meta">Presentation</div><h3>Animated GIF</h3><p>Meaningful stages at one second per frame, optimized for readability rather than decorative speed.</p><a class="card-link" href="diagrams/capability-lifecycle.gif">Open GIF →</a></article>
  </div>
</section>

<section class="container section compact">
  <div class="section-head"><div><p class="section-kicker">Product truth</p><h2>Architecture is a contract and direction—not a claim that every box is production-qualified today.</h2></div><p>The website intentionally distinguishes implemented foundations, active realization, and target architecture. Readiness must be demonstrated for the exact release, deployment profile, risk tier, cloud, region, and customer control environment.</p></div>
</section>
"""


def main() -> None:
    diagrams = {
        "service_factory": diagram(
            "service-factory",
            "Universal Service Factory",
            "The same path supports an imported API, manually authored Agent, generated MCP server, or complete cross-industry solution pack.",
        ),
        "platform_planes": diagram(
            "platform-planes",
            "Eight Platform Planes",
            "Click a plane to inspect its responsibilities, trust boundary, and relationship to the portable infrastructure layer.",
        ),
        "capability_lifecycle": diagram(
            "capability-lifecycle",
            "Agent and MCP Capability Lifecycle",
            "Deployment is not discovery: a capability becomes usable only after runtime attestation, Registry convergence, and qualification.",
        ),
        "governed_run": diagram(
            "governed-run",
            "Governed Dynamic Service Run",
            "The player shows identity and policy paths, parallel Agent work, MCP side effects, human approval, durable state, and final evidence.",
        ),
        "scale_path": diagram(
            "scale-path",
            "Individual to Sovereign Enterprise",
            "Stable capability contracts remain portable while governance, tenancy, isolation, deployment, and assurance become progressively stronger.",
        ),
    }

    pages = {
        "index.html": page(
            "home",
            "ContextWeaver — Turn any approved idea into a governed Service",
            "ContextWeaver creates governed Services from specifications, knowledge, Agents, MCP tools, Workflows, models, policy, and portable infrastructure.",
            HOME.format(**diagrams),
        ),
        "platform.html": page(
            "platform",
            "ContextWeaver Platform — Cerebro, Weave, and Loom",
            "Explore the ContextWeaver platform planes, product model, cloud-neutral contracts, durable runtime, and governed capability architecture.",
            PLATFORM.format(**diagrams),
        ),
        "studio.html": page(
            "studio",
            "ContextWeaver Agent and MCP Studio",
            "Create, validate, simulate, publish, deploy, modify, and govern Agents, MCP servers, Services, and Workflows from a GUI, VS Code, CLI, or Jupyter.",
            STUDIO.format(**diagrams),
        ),
        "runtime.html": page(
            "runtime",
            "ContextWeaver Runtime — Governed dynamic Service execution",
            "See how ContextWeaver turns intent into an authorized immutable plan, durable Agent and MCP execution, and an evidence-backed result.",
            RUNTIME.format(**diagrams),
        ),
        "governance.html": page(
            "governance",
            "ContextWeaver Governance, Security, and Evidence",
            "Review ContextWeaver identity, credential non-possession, policy, approval, admission, lifecycle, evidence, and safety controls.",
            GOVERNANCE.format(**diagrams),
        ),
        "solutions.html": page(
            "solutions",
            "ContextWeaver Solutions — Individual, Small Business, and Enterprise",
            "See how ContextWeaver scales from personal Services to small-business operations, enterprise platforms, and sovereign deployments.",
            SOLUTIONS.format(**diagrams),
        ),
        "architecture.html": page(
            "architecture",
            "ContextWeaver Interactive Architecture Explorer",
            "Explore clickable animated ContextWeaver architecture diagrams and download editable Draw.io, static SVG, and GIF assets.",
            ARCHITECTURE.format(**diagrams),
        ),
    }

    for filename, content in pages.items():
        (ROOT / filename).write_text(content, encoding="utf-8", newline="\n")

    sitemap = "\n".join(
        f"  <url><loc>https://brainzbytes.com/{filename}</loc></url>"
        for filename in pages
    )
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap}\n</urlset>\n',
        encoding="utf-8",
        newline="\n",
    )
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: https://brainzbytes.com/sitemap.xml\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Generated {len(pages)} site pages.")


if __name__ == "__main__":
    main()
