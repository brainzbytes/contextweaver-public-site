import json
import os
from pathlib import Path
from textwrap import dedent

from atlas_assets import atlas_asset_version

ROOT = Path(__file__).resolve().parents[1]
ATLAS_ASSET_VERSION = atlas_asset_version(ROOT)
CURRENT_DATE = "November 1, 2026"
PUBLIC_SITE_URL = os.environ.get(
    "PUBLIC_SITE_URL",
    "https://brainzbytes.com",
).rstrip("/")
SOURCE_TRUTH = json.loads((ROOT / "content" / "source-truth.json").read_text(encoding="utf-8"))
FACTS = {fact["id"]: fact for fact in SOURCE_TRUTH["facts"]}


def standalone_page(filename: str) -> str:
    return (ROOT / "content" / "pages" / filename).read_text(encoding="utf-8")


NAV = (
    ("landing", "Home", "index.html"),
    ("overview", "Overview", "overview.html"),
    ("platform", "Platform", "platform.html"),
    ("studio", "Studio", "studio.html"),
    ("runtime", "Runtime", "runtime.html"),
    ("governance", "Governance", "governance.html"),
    ("solutions", "Solutions", "solutions.html"),
    ("architecture", "Architecture", "architecture.html"),
    ("learning", "Learn", "learning.html"),
    ("company", "Company", "company.html"),
)


def brand_lockup(compact: bool = False) -> str:
    modifier = " brand-lockup--compact" if compact else ""
    return f"""
      <span class="brand-lockup{modifier}" aria-hidden="true">
        <span class="brand-lockup__marks">
          <img src="assets/brand/brainzbytes-b4.svg" alt="" width="38" height="38">
          <span class="brand-lockup__bridge"></span>
          <img src="assets/brand/contextweaver-c1.svg" alt="" width="38" height="38">
        </span>
        <span class="brand-lockup__copy">
          <strong>BrainzBytes</strong>
          <span>ContextWeaver</span>
        </span>
      </span>
    """


def header() -> str:
    links = "".join(
        f'<a href="{href}" data-nav-page="{key}">{label}</a>'
        for key, label, href in NAV
    )
    return f"""
    <a class="skip-link" href="#main-content">Skip to content</a>
    <header class="site-header">
      <div class="nav-shell">
        <a class="brand" href="index.html" aria-label="ContextWeaver home">{brand_lockup(compact=True)}</a>
        <nav class="primary-nav" data-primary-nav aria-label="Primary navigation">{links}</nav>
        <div class="nav-actions">
          <button class="icon-button" type="button" data-theme-toggle aria-label="Change dark contrast theme">◑</button>
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
          <a class="brand" href="index.html" aria-label="ContextWeaver home">{brand_lockup(compact=True)}</a>
          <p style="margin-top:16px">Turn approved intent into user-facing Solutions assembled from governed Services, Workflows, Agents, MCP capabilities, knowledge, models, policy, and portable infrastructure—with evidence attached.</p>
        </div>
        <div><h3>Explore</h3><div class="footer-links"><a href="platform.html">Platform model</a><a href="studio.html">Studio and creation contexts</a><a href="runtime.html">Dynamic runtime</a></div></div>
        <div><h3>Trust</h3><div class="footer-links"><a href="governance.html">Governance</a><a href="architecture.html">Architecture</a><a href="learning.html">Learning</a></div></div>
        <div><h3>Company</h3><div class="footer-links"><a href="company.html#about">About BrainzBytes</a><a href="company.html#about">Founder</a><a href="company.html#company-paths">Careers · planned</a></div></div>
      </div>
      <div class="container footer-bottom">
        <span>© 2026 BrainzBytes. ContextWeaver product architecture.</span>
        <span>Reference architecture only. Compliance and deployment outcomes remain customer-specific.</span>
      </div>
    </footer>
    """


def page(name: str, title: str, description: str, content: str) -> str:
    spatial_dialog = """
      <dialog class="spatial-modal" data-spatial-modal aria-label="Expanded spatial view">
        <div class="spatial-modal-frame">
          <div class="spatial-modal-bar">
            <strong data-spatial-modal-title>ContextWeaver spatial view</strong>
            <button class="spatial-modal-close" type="button" data-spatial-close aria-label="Close expanded spatial view">← Back to page</button>
          </div>
          <div class="spatial-modal-content">
            <img data-spatial-modal-image alt="">
            <iframe data-spatial-modal-frame title="Expanded ContextWeaver spatial view" sandbox="allow-scripts allow-same-origin"></iframe>
          </div>
        </div>
      </dialog>
    """ if 'class="spatial-visual' in content or "data-spatial-open" in content else ""
    intro = ""
    if name == "landing":
        intro = f"""
      <section class="site-intro" data-site-intro hidden aria-label="BrainzBytes and ContextWeaver overview">
        <div class="site-intro__backdrop"></div>
        <div class="site-intro__shell">
          <div class="site-intro__utility">
            <span class="site-intro__status"><i></i> Narrated story</span>
            <button class="button compact" type="button" data-intro-skip>Skip intro</button>
          </div>
          <div class="site-intro__stage">
            <iframe
              data-intro-frame
              data-src="assets/brand/brainzbytes-contextweaver-overview.html?embedded=1&amp;intro=1&amp;v=20261104-1"
              title="BrainzBytes and ContextWeaver narrated company overview"
              loading="eager"
              allow="autoplay"
              sandbox="allow-scripts allow-same-origin"
            ></iframe>
          </div>
          <div class="site-intro__footer">
            <p>Music opens the story for 10 seconds, then the narrated ContextWeaver journey begins automatically. If a browser blocks sound, the first interaction quietly enables it.</p>
            <button class="button primary" type="button" data-intro-enter>Enter ContextWeaver</button>
          </div>
        </div>
      </section>
      <noscript>
        <section class="noscript-intro">
          <img src="assets/brand/brainzbytes-contextweaver-overview.png" alt="BrainzBytes and ContextWeaver company overview">
          <p>BrainzBytes builds ContextWeaver: governed AI Solutions composed through Cerebros, Loom, and Weave.</p>
        </section>
      </noscript>
        """
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
      <link rel="stylesheet" href="assets/css/site.css?v=20261104-3">
    </head>
    <body data-page="{name}">
      {intro}
      {header()}
      <main id="main-content">
        {content}
      </main>
      {spatial_dialog}
      {footer()}
      <script src="assets/js/site.js?v=20261104-2"></script>
    </body>
    </html>
    """).lstrip()


def diagram(name: str, title: str, note: str) -> str:
    asset_version = "20261103-9" if name == "service-factory" else "20261103-2"
    return f"""
    <div class="diagram-shell" data-reveal>
      <div class="diagram-toolbar">
        <strong>{title}</strong>
      </div>
      <iframe class="diagram-frame" src="diagrams/{name}.html?v={asset_version}" title="{title}" loading="lazy"></iframe>
    </div>
    <p class="diagram-note">{note}</p>
    """


def spatial_visual(
    image: str,
    eyebrow: str,
    title: str,
    description: str,
    *,
    alt: str,
    wide: bool = False,
) -> str:
    wide_class = " spatial-visual-wide" if wide else ""
    return f"""
    <figure class="spatial-visual{wide_class}" data-reveal>
      <button class="spatial-visual-stage spatial-visual-trigger" type="button" data-spatial-open data-spatial-type="image" data-spatial-src="assets/media/spatial/{image}?v=20261103-2" data-spatial-title="{title}" aria-label="Open large view: {title}">
        <img src="assets/media/spatial/{image}?v=20261103-2" alt="{alt}" loading="lazy">
        <span class="spatial-visual-expand" aria-hidden="true">Expand ↗</span>
      </button>
      <figcaption>
        <span>{eyebrow}</span>
        <strong>{title}</strong>
        <p>{description}</p>
      </figcaption>
    </figure>
    """


def fact_cards(*fact_ids: str) -> str:
    cards = []
    for fact_id in fact_ids:
        fact = FACTS[fact_id]
        status_class = "mint" if fact["status"] == "Implemented foundation" else "amber"
        cards.append(
            f'<article class="card {status_class}" data-fact-id="{fact_id}" data-reveal>'
            f'<div class="meta">{fact["status"]}</div>'
            f'<h3>{fact["title"]}</h3><p>{fact["summary"]}</p></article>'
        )
    return "".join(cards)


LANDING = """
<section class="landing-replay container" aria-label="Company overview">
  <div class="landing-replay__visual" aria-hidden="true">
    <img src="assets/brand/brainzbytes-contextweaver-overview.png" alt="">
    <span class="landing-replay__pulse"></span>
  </div>
  <div class="landing-replay__copy">
    <p class="eyebrow">BrainzBytes × ContextWeaver</p>
    <h2>Replay the company and product story.</h2>
    <p>See how ContextWeaver uses Cerebros as its brain, Loom as its architecture, and Weave to orchestrate governed AI Solutions.</p>
  </div>
  <button class="button landing-replay__button" type="button" data-intro-replay><span aria-hidden="true">▶</span> Replay overview</button>
</section>

<section class="container landing-intro">
  <div class="landing-intro-grid">
    <div>
      <p class="eyebrow">The governed AI solution operating platform</p>
      <h1>From business intent to an <em>approved production Solution.</em></h1>
      <p class="lede">ContextWeaver turns approved ideas into governed, user-facing Solutions through reusable capabilities, durable orchestration, independent approval, evidence, outcome, and run history.</p>
    </div>
    <div class="landing-actions">
      <a class="button primary" href="overview.html">Start with the Overview <span aria-hidden="true">→</span></a>
      <a class="button" href="studio.html">Explore Studio</a>
    </div>
  </div>
</section>

<section class="container landing-next">
  <div class="section-head">
    <div><p class="section-kicker">Continue deeper</p><h2>Move from the visual promise into the product details.</h2></div>
    <p>The Overview is the first detailed chapter. From there, explore the platform model, the unified Studio and its creation contexts, runtime, governance, Solutions, and complete architecture.</p>
  </div>
  <div class="grid three">
    <article class="card mint" data-reveal><div class="meta">Start here</div><h3>Overview</h3><p>Understand the complete lifecycle, product promise, supported inputs, evidence, and adoption path.</p><a class="card-link" href="overview.html">Open Overview →</a></article>
    <article class="card sky" data-reveal><div class="meta">Build</div><h3>Workspace and Studio</h3><p>See how one Studio moves across MCP, Agent, Workflow, Service, and Solution contexts using guided and developer experiences.</p><a class="card-link" href="studio.html">Explore Studio →</a></article>
    <article class="card violet" data-reveal><div class="meta">Understand</div><h3>Architecture</h3><p>Inspect the planes, trust boundaries, lifecycle, governed runtime, deployment profiles, and editable diagrams.</p><a class="card-link" href="architecture.html">Explore Architecture →</a></article>
  </div>
</section>
"""


HOME = """
<section class="container hero">
  <div>
    <p class="eyebrow">The governed solution operating platform</p>
    <h1>Turn any approved idea into a <em>working Solution.</em></h1>
    <p class="lede">ContextWeaver composes user-facing Solutions from reusable Services, Workflows, Agents, MCP capabilities, enterprise knowledge, models, policy, and portable infrastructure—then governs the lifecycle from creation and dry run to deployment, execution, recovery, and evidence.</p>
    <div class="hero-actions">
      <a class="button primary" href="studio.html">Explore Studio <span aria-hidden="true">→</span></a>
      <a class="button" href="architecture.html">Explore the architecture</a>
    </div>
    <div class="pills" style="margin-top:24px">
      <span class="pill">No-code GUI</span><span class="pill">VS Code + CLI</span><span class="pill">Jupyter</span><span class="pill">OpenAPI + MCP + A2A</span><span class="pill">Kubernetes + GitOps</span>
    </div>
  </div>
  {intent_to_evidence}
</section>
<div class="container trust-strip" aria-label="Supported creation inputs">
  <span>Specifications & RFCs</span><span>OpenAPI & AsyncAPI</span><span>Wikis & enterprise data</span><span>MCPs, Agents & Workflows</span><span>Services & solution packs</span>
</div>

<section id="intent-outcome-examples" class="container section outcome-overview" aria-labelledby="outcome-overview-title">
  <div class="section-head">
    <div><p class="section-kicker">See the product through familiar moments</p><h2 id="outcome-overview-title">Start with a story people already understand.</h2></div>
    <p>Choose a real-world goal and see how ContextWeaver turns it into a trusted result—without making the reader learn the platform before the value becomes clear.</p>
  </div>

  <div class="outcome-primer" data-reveal>
    <div>
      <span class="outcome-primer__label">The experience in one sentence</span>
      <h3>Ask for the result. ContextWeaver handles the governed journey.</h3>
      <p>Identity, knowledge, policy, approvals, reusable capabilities, execution, and evidence work together behind one clear experience.</p>
    </div>
    <ul class="outcome-primer__flow" aria-label="The shared intent-to-outcome path">
      <li><span aria-hidden="true"></span><b>Ask</b><small>Describe the result</small></li>
      <li><span aria-hidden="true"></span><b>Understand</b><small>Gather trusted context</small></li>
      <li><span aria-hidden="true"></span><b>Plan</b><small>Compose the right path</small></li>
      <li><span aria-hidden="true"></span><b>Authorize</b><small>Apply policy and approval</small></li>
      <li><span aria-hidden="true"></span><b>Execute</b><small>Coordinate durable work</small></li>
      <li><span aria-hidden="true"></span><b>Prove</b><small>Attach evidence</small></li>
      <li><span aria-hidden="true"></span><b>Improve</b><small>Learn from outcomes</small></li>
    </ul>
  </div>

  <div class="outcome-workspace">
    <aside class="outcome-story-rail" aria-label="Choose a real-world story">
      <div class="outcome-story-rail__head">
        <span>Explore by outcome</span>
        <h3>Choose a familiar goal</h3>
        <p>Each story follows the same governed path from a person’s request to a proven result.</p>
      </div>
      <div class="outcome-tabs" role="tablist" aria-orientation="vertical" aria-label="Real-world ContextWeaver examples">
        <button class="outcome-tab active" id="outcome-tab-travel" type="button" role="tab" aria-selected="true" aria-controls="outcome-travel" data-outcome-tab="outcome-travel"><span>Travel</span><strong>Book a flight</strong><small>Request to confirmed trip</small><i aria-hidden="true">→</i></button>
        <button class="outcome-tab" id="outcome-tab-developer" type="button" role="tab" aria-selected="false" aria-controls="outcome-developer" data-outcome-tab="outcome-developer"><span>Software delivery</span><strong>Spec to pull request</strong><small>Requirement to review-ready code</small><i aria-hidden="true">→</i></button>
        <button class="outcome-tab" id="outcome-tab-crm" type="button" role="tab" aria-selected="false" aria-controls="outcome-crm" data-outcome-tab="outcome-crm"><span>Revenue</span><strong>CRM and sales</strong><small>Account insight to approved renewal</small><i aria-hidden="true">→</i></button>
        <button class="outcome-tab" id="outcome-tab-service" type="button" role="tab" aria-selected="false" aria-controls="outcome-service" data-outcome-tab="outcome-service"><span>Customer care</span><strong>Customer service</strong><small>Billing issue to proven resolution</small><i aria-hidden="true">→</i></button>
      </div>
      <div class="outcome-story-rail__promise">
        <span aria-hidden="true">✓</span>
        <p><b>Same trust model.</b> Identity, policy, approvals, durable execution, evidence, and observability follow every story.</p>
      </div>
    </aside>

    <div class="outcome-stage">
    <article class="outcome-panel active" id="outcome-travel" role="tabpanel" aria-labelledby="outcome-tab-travel">
      <header class="outcome-panel__head">
        <div><span>Travel story</span><h3>“Book me a policy-compliant flight to Seattle next Tuesday and send me the itinerary.”</h3></div>
        <div class="outcome-result"><span>Outcome</span><strong>A confirmed trip—not a list of links.</strong><p>The traveler receives an approved itinerary, booking reference, calendar entry, and notification. The business receives the policy, approval, payment, and booking evidence.</p></div>
      </header>
      <nav class="outcome-detail-nav" aria-label="Travel story sections"><a class="active" href="#outcome-travel">Overview</a><a href="#outcome-travel-journey">Journey</a><a href="#outcome-travel-blocks">What powers it</a><a href="#outcome-travel-trust">Guardrails and evidence</a></nav>
      <div class="outcome-building-blocks" id="outcome-travel-blocks" aria-label="Travel solution building blocks">
        <section><span>Solution</span><b>Business Travel Assistant</b><p>The final experience the traveler opens and uses.</p></section>
        <section><span>Services</span><b>Trip planning · Booking · Payment · Notification</b><p>Reusable business outcomes with typed inputs and results.</p></section>
        <section><span>Workflows</span><b>Search → compare → approve → reserve → pay → confirm</b><p>Durable steps that can wait, retry, or compensate safely.</p></section>
        <section><span>Agents</span><b>Travel planner · Policy specialist</b><p>Bounded reasoning specialists that interpret choices and propose a plan.</p></section>
        <section><span>MCP capabilities</span><b>Airline · expense policy · traveler profile · payment · calendar · email</b><p>Governed access to the systems that can read data or take action.</p></section>
      </div>
      <ul class="outcome-journey" id="outcome-travel-journey" aria-label="How the travel story unfolds">
        <li><span aria-hidden="true"></span><div><b>Ask</b><p>The traveler states dates, destination, preferences, and the desired result in ordinary language.</p></div></li>
        <li><span aria-hidden="true"></span><div><b>Understand</b><p>Identity, role, traveler profile, loyalty numbers, company travel policy, budget, calendar, and purpose are gathered from approved sources.</p></div></li>
        <li><span aria-hidden="true"></span><div><b>Plan</b><p>The Travel Agent compares viable flights and proposes an exact itinerary using approved airline and policy capabilities.</p></div></li>
        <li><span aria-hidden="true"></span><div><b>Authorize</b><p>Policy checks cabin, price, route, and purpose. An out-of-policy choice pauses for the traveler or manager to approve.</p></div></li>
        <li><span aria-hidden="true"></span><div><b>Execute</b><p>The Workflow reserves the seat, brokers a scoped payment credential, confirms the booking, writes the calendar event, and sends the itinerary.</p></div></li>
        <li><span aria-hidden="true"></span><div><b>Prove</b><p>The result includes the selected fare, policy decision, approval, booking locator, payment receipt reference, messages sent, and complete run history.</p></div></li>
        <li><span aria-hidden="true"></span><div><b>Improve</b><p>Latency, failures, retries, price changes, traveler feedback, and provider reliability help improve future runs without silently changing authority.</p></div></li>
      </ul>
      <div class="outcome-proof" id="outcome-travel-trust">
        <section><span>Guardrails a person can understand</span><ul><li>The Agent can recommend a flight; it cannot invent permission to buy it.</li><li>Payment credentials stay in a trusted gateway and are never exposed to the Agent.</li><li>Price or itinerary changes beyond the approved scope require a new decision.</li><li>A failed booking can release the reservation or reverse the charge through compensation.</li></ul></section>
        <section><span>What is gathered as evidence</span><ul><li>Who asked, for what purpose, and under which role</li><li>Options considered, citations, policy rules, and the chosen plan</li><li>Approval and entitlement decisions</li><li>Tool receipts, booking and payment references, logs, metrics, and traces</li></ul></section>
      </div>
    </article>

    <article class="outcome-panel" id="outcome-developer" role="tabpanel" aria-labelledby="outcome-tab-developer" hidden>
      <header class="outcome-panel__head">
        <div><span>Software delivery story</span><h3>“Implement this approved specification, add tests, commit it, and open a pull request.”</h3></div>
        <div class="outcome-result"><span>Outcome</span><strong>A reviewable pull request tied back to the specification.</strong><p>The developer receives code, tests, build results, a commit, and a PR. Reviewers receive traceability from each requirement to the changed files and validation evidence.</p></div>
      </header>
      <nav class="outcome-detail-nav" aria-label="Software delivery story sections"><a class="active" href="#outcome-developer">Overview</a><a href="#outcome-developer-journey">Journey</a><a href="#outcome-developer-blocks">What powers it</a><a href="#outcome-developer-trust">Guardrails and evidence</a></nav>
      <div class="outcome-building-blocks" id="outcome-developer-blocks" aria-label="Software delivery solution building blocks">
        <section><span>Solution</span><b>Governed Software Delivery Assistant</b><p>The developer experience from approved specification to review.</p></section>
        <section><span>Services</span><b>Change implementation · Validation · Pull-request delivery</b><p>Reusable contracts for producing and reviewing a software change.</p></section>
        <section><span>Workflows</span><b>Analyze → branch → edit → test → scan → commit → open PR</b><p>A durable delivery path with explicit gates and recovery.</p></section>
        <section><span>Agents</span><b>Spec analyst · Coding Agent · Test Agent · Review Agent</b><p>Specialists with separate responsibilities and bounded tools.</p></section>
        <section><span>MCP capabilities</span><b>Specification · repository · work items · CI · security scanner · artifact registry</b><p>Least-privilege access to engineering systems.</p></section>
      </div>
      <ul class="outcome-journey" id="outcome-developer-journey" aria-label="How the software delivery story unfolds">
        <li><span aria-hidden="true"></span><div><b>Ask</b><p>The developer selects an approved specification and asks for a complete, review-ready implementation.</p></div></li>
        <li><span aria-hidden="true"></span><div><b>Understand</b><p>The platform gathers repository instructions, architecture, code owners, work items, dependency rules, test conventions, and protected-branch policy.</p></div></li>
        <li><span aria-hidden="true"></span><div><b>Plan</b><p>The Spec Analyst maps requirements to components. The Coding and Test Agents propose file changes, tests, and validation commands.</p></div></li>
        <li><span aria-hidden="true"></span><div><b>Authorize</b><p>Policy verifies repository access, allowed tools, branch scope, change risk, data classification, and whether a human must approve execution.</p></div></li>
        <li><span aria-hidden="true"></span><div><b>Execute</b><p>The Workflow creates a branch, edits only permitted files, runs tests and scans, records results, commits with traceability, and opens the PR.</p></div></li>
        <li><span aria-hidden="true"></span><div><b>Prove</b><p>The PR links requirements, code changes, test output, security findings, model and capability versions, approvals, and the immutable execution plan.</p></div></li>
        <li><span aria-hidden="true"></span><div><b>Improve</b><p>Review feedback, escaped defects, flaky tests, build time, and acceptance results improve evaluation and planning—not branch protection or approval rules.</p></div></li>
      </ul>
      <div class="outcome-proof" id="outcome-developer-trust">
        <section><span>Guardrails a person can understand</span><ul><li>The Coding Agent works only in the approved repository, branch, and file scope.</li><li>Protected branches remain protected; the platform opens a PR but does not autonomously merge it.</li><li>Code generation and independent review use separate identities and evidence.</li><li>Secret scanning, dependency checks, tests, and required reviewers still apply.</li></ul></section>
        <section><span>What is gathered as evidence</span><ul><li>Specification revision and requirement-to-code mapping</li><li>Repository digest, branch, changed files, prompts, and capability versions</li><li>Test, lint, build, security, and policy results</li><li>Commit SHA, PR link, reviewer decisions, logs, metrics, and traces</li></ul></section>
      </div>
    </article>

    <article class="outcome-panel" id="outcome-crm" role="tabpanel" aria-labelledby="outcome-tab-crm" hidden>
      <header class="outcome-panel__head">
        <div><span>Revenue story</span><h3>“Prepare Acme’s renewal, propose the right offer, update the CRM, and schedule the follow-up.”</h3></div>
        <div class="outcome-result"><span>Outcome</span><strong>A prepared renewal with approved next actions.</strong><p>The account owner receives a concise account brief, recommended offer, updated opportunity, drafted outreach, and scheduled follow-up—without losing control of pricing or customer communication.</p></div>
      </header>
      <nav class="outcome-detail-nav" aria-label="Revenue story sections"><a class="active" href="#outcome-crm">Overview</a><a href="#outcome-crm-journey">Journey</a><a href="#outcome-crm-blocks">What powers it</a><a href="#outcome-crm-trust">Guardrails and evidence</a></nav>
      <div class="outcome-building-blocks" id="outcome-crm-blocks" aria-label="CRM solution building blocks">
        <section><span>Solution</span><b>Account Growth Assistant</b><p>The seller-facing workspace for renewals and customer growth.</p></section>
        <section><span>Services</span><b>Account insight · Offer preparation · CRM update · Outreach</b><p>Reusable outcomes shared across sales Solutions.</p></section>
        <section><span>Workflows</span><b>Gather → assess → recommend → approve → update → communicate</b><p>A repeatable process that keeps pricing and outreach governed.</p></section>
        <section><span>Agents</span><b>Account Analyst · Offer Agent · Compliance Reviewer</b><p>Specialists that summarize, reason, and recommend within policy.</p></section>
        <section><span>MCP capabilities</span><b>CRM · product usage · support history · pricing · contracts · calendar · email</b><p>Identity-aware access to customer and commercial systems.</p></section>
      </div>
      <ul class="outcome-journey" id="outcome-crm-journey" aria-label="How the revenue story unfolds">
        <li><span aria-hidden="true"></span><div><b>Ask</b><p>The account owner requests a renewal plan for a named customer and target date.</p></div></li>
        <li><span aria-hidden="true"></span><div><b>Understand</b><p>The platform gathers the customer record, contract, usage, open issues, previous commitments, renewal policy, pricing authority, and communication history.</p></div></li>
        <li><span aria-hidden="true"></span><div><b>Plan</b><p>The Account Analyst summarizes health and risks. The Offer Agent proposes the next-best action, package, and outreach sequence with cited reasons.</p></div></li>
        <li><span aria-hidden="true"></span><div><b>Authorize</b><p>Discount, data-use, legal, territory, and communication policies determine what the seller can approve and what must go to finance, legal, or management.</p></div></li>
        <li><span aria-hidden="true"></span><div><b>Execute</b><p>The Workflow updates the opportunity, creates tasks, prepares the quote, drafts the email, and schedules the meeting. Sending or discounting waits for required approval.</p></div></li>
        <li><span aria-hidden="true"></span><div><b>Prove</b><p>The account record shows source data, cited insights, policy decisions, approved offer, CRM changes, communications, and the resulting customer response.</p></div></li>
        <li><span aria-hidden="true"></span><div><b>Improve</b><p>Conversion, response, forecast accuracy, discount effectiveness, stale data, and customer feedback improve recommendations and operational health.</p></div></li>
      </ul>
      <div class="outcome-proof" id="outcome-crm-trust">
        <section><span>Guardrails a person can understand</span><ul><li>The Agent may recommend a discount but cannot exceed the seller’s authority.</li><li>Customer data is filtered by identity, role, account ownership, and purpose.</li><li>External messages remain drafts until the appropriate person approves sending.</li><li>Every CRM change records the old value, new value, reason, and actor.</li></ul></section>
        <section><span>What is gathered as evidence</span><ul><li>Customer sources, timestamps, citations, and data-access decisions</li><li>Account-health calculation and offer rationale</li><li>Discount, legal, and communication approvals</li><li>CRM mutations, quote versions, messages, outcomes, logs, metrics, and traces</li></ul></section>
      </div>
    </article>

    <article class="outcome-panel" id="outcome-service" role="tabpanel" aria-labelledby="outcome-tab-service" hidden>
      <header class="outcome-panel__head">
        <div><span>Customer care story</span><h3>“This customer was charged twice. Verify it, fix it, and explain what happened.”</h3></div>
        <div class="outcome-result"><span>Outcome</span><strong>A resolved case with a clear explanation and proof.</strong><p>The customer receives an accurate response and, when authorized, a refund. The service team receives a complete case history, policy basis, financial receipt, and operational signals.</p></div>
      </header>
      <nav class="outcome-detail-nav" aria-label="Customer care story sections"><a class="active" href="#outcome-service">Overview</a><a href="#outcome-service-journey">Journey</a><a href="#outcome-service-blocks">What powers it</a><a href="#outcome-service-trust">Guardrails and evidence</a></nav>
      <div class="outcome-building-blocks" id="outcome-service-blocks" aria-label="Customer service solution building blocks">
        <section><span>Solution</span><b>Customer Resolution Console</b><p>The agent-facing experience for understanding and resolving cases.</p></section>
        <section><span>Services</span><b>Case triage · Billing investigation · Refund · Customer notification</b><p>Reusable resolution outcomes with controlled side effects.</p></section>
        <section><span>Workflows</span><b>Classify → verify → investigate → approve → resolve → notify → close</b><p>A durable case path that can pause for people or external systems.</p></section>
        <section><span>Agents</span><b>Case Triage Agent · Billing Specialist · Response Agent</b><p>Specialists that reason over the case without owning financial authority.</p></section>
        <section><span>MCP capabilities</span><b>Ticketing · CRM · orders · billing · payment · policy knowledge · messaging</b><p>Governed connections to customer and transaction systems.</p></section>
      </div>
      <ul class="outcome-journey" id="outcome-service-journey" aria-label="How the customer care story unfolds">
        <li><span aria-hidden="true"></span><div><b>Ask</b><p>A customer or service representative reports the duplicate charge and asks for resolution.</p></div></li>
        <li><span aria-hidden="true"></span><div><b>Understand</b><p>The platform gathers the authenticated customer, case history, order, invoice, payment events, refund policy, communication preference, and agent authority.</p></div></li>
        <li><span aria-hidden="true"></span><div><b>Plan</b><p>The Billing Specialist compares the order and payment timeline, determines whether the charge is duplicate, and proposes the permitted remedy.</p></div></li>
        <li><span aria-hidden="true"></span><div><b>Authorize</b><p>Policy checks refund amount, transaction age, fraud signals, customer identity, service-agent limits, and whether supervisor approval is required.</p></div></li>
        <li><span aria-hidden="true"></span><div><b>Execute</b><p>The Workflow issues the authorized refund, updates the ticket and CRM, sends the explanation, and schedules follow-up if settlement is delayed.</p></div></li>
        <li><span aria-hidden="true"></span><div><b>Prove</b><p>The closed case includes the payment comparison, policy applied, approval, refund receipt, customer message, timestamps, and full run history.</p></div></li>
        <li><span aria-hidden="true"></span><div><b>Improve</b><p>Repeat incidents, refund latency, escalation rate, customer sentiment, and payment-provider errors become observable signals for product and operations teams.</p></div></li>
      </ul>
      <div class="outcome-proof" id="outcome-service-trust">
        <section><span>Guardrails a person can understand</span><ul><li>The Agent can diagnose and recommend; only policy-authorized capabilities can issue money.</li><li>Customer identity and account ownership are verified before private data is exposed.</li><li>High-value or suspicious refunds pause for independent approval.</li><li>Messages cite verified transaction facts instead of inventing an explanation.</li></ul></section>
        <section><span>What is gathered as evidence</span><ul><li>Customer, case, order, invoice, and payment-event lineage</li><li>Diagnosis, policy version, authority, and approval decision</li><li>Refund transaction and downstream update receipts</li><li>Customer communication, settlement status, logs, metrics, traces, and outcome</li></ul></section>
      </div>
    </article>
    </div>
  </div>

  <div class="outcome-shared" data-reveal>
    <div><span>What stays the same in every example</span><h3>The domain changes. The trust model does not.</h3></div>
    <div class="outcome-shared__grid">
      <p><b>Identity follows the request.</b> The platform knows who is acting, for what purpose, and under which role and entitlements.</p>
      <p><b>Models propose; policy authorizes.</b> An Agent can reason about a plan, but it cannot grant itself access, credentials, approval, or authority.</p>
      <p><b>Work survives interruption.</b> Durable Workflows can wait for approval, retry transient failures, resume, or compensate completed steps.</p>
      <p><b>Every important step leaves proof.</b> Plans, citations, decisions, approvals, receipts, artifacts, metrics, logs, traces, and outcomes remain connected.</p>
    </div>
  </div>
</section>

<section id="reading-path" class="container section reader-journey" aria-labelledby="reader-journey-title">
  <div class="section-head">
    <div><p class="section-kicker">Your reading path</p><h2 id="reader-journey-title">Start with the promise. Go as deep as you need.</h2></div>
    <p>Each chapter answers one question and hands the reader to the next. Product evaluators can follow the full path; specialists can jump directly to their concern.</p>
  </div>
  <nav class="reader-path" aria-label="ContextWeaver reading journey">
    <a class="reader-step active" href="#reading-path"><span>01</span><b>Understand</b><small>What is the product?</small></a>
    <a class="reader-step" href="studio.html?from=journey"><span>02</span><b>Create</b><small>How is it built?</small></a>
    <a class="reader-step" href="runtime.html?from=journey#scenarios"><span>03</span><b>Experience</b><small>What happens in a run?</small></a>
    <a class="reader-step" href="governance.html?from=journey"><span>04</span><b>Trust</b><small>Who has authority?</small></a>
    <a class="reader-step" href="solutions.html?from=journey#consumer"><span>05</span><b>Use</b><small>How do people enter?</small></a>
    <a class="reader-step" href="architecture.html?from=journey"><span>06</span><b>Inspect</b><small>How does it fit together?</small></a>
    <a class="reader-step" href="learning.html?from=journey"><span>07</span><b>Learn</b><small>Explore every concept</small></a>
  </nav>
</section>

<section class="container section">
  <div class="section-head">
    <div><p class="section-kicker">One product, complete lifecycle</p><h2>More than an AI answer. A governed business outcome.</h2></div>
    <p>A ContextWeaver run can return a typed result, citations, approvals, policy decisions, tool receipts, artifacts, retries, compensation evidence, metrics, logs, traces, and a durable audit trail.</p>
  </div>
  <div class="grid four">
    <article class="card mint" data-reveal><div class="meta">Understand</div><h3>Make intent explicit</h3><p>Classify purpose, risk, data, entities, required capabilities, ambiguity, and approval needs before protected work begins.</p></article>
    <article class="card mint" data-reveal><div class="meta">Compile</div><h3>Freeze an authorized plan</h3><p>Resolve exact compatible capability versions, validate typed contracts, bind data fields, and pin one immutable execution plan.</p></article>
    <article class="card mint" data-reveal><div class="meta">Execute</div><h3>Coordinate durable work</h3><p>Run Agents in parallel, pause without wasting compute, call tools through governed gateways, retry safely, and compensate when required.</p></article>
    <article class="card mint" data-reveal><div class="meta">Prove</div><h3>Attach evidence</h3><p>Preserve lineage, citations, policy and approval decisions, release digests, side-effect receipts, telemetry, and evaluation results.</p></article>
  </div>
</section>

<section class="container section compact">
  <div class="section-head">
    <div><p class="section-kicker">Interactive product map</p><h2>From raw material to a trusted Solution.</h2></div>
    <p>Use the controls, click any component, or open the full-screen version. The animation follows creation, admission, deployment, discovery, execution, and evidence.</p>
  </div>
  {service_factory}
</section>

<section class="container section">
  <div class="section-head">
    <div><p class="section-kicker">A platform for every scale</p><h2>Start with one useful tool. Grow without rebuilding the foundation.</h2></div>
    <p>The same hierarchy supports a personal Solution, a small-business experience, a multi-team enterprise platform, or an isolated sovereign deployment without turning every outcome into a one-off application.</p>
  </div>
  <div class="grid three">
    <article class="card mint" data-reveal><div class="meta">Individual</div><h3>Build personal leverage</h3><p>Use a private research, planning, coding, or administration Solution assembled from approved sources, capabilities, and reusable Services.</p><ul><li>My Solutions consumer entry</li><li>Personal workspaces and memory</li><li>Clear approvals before side effects</li></ul><a class="card-link" href="solutions.html#individual">See the individual path →</a></article>
    <article class="card amber" data-reveal><div class="meta">Small business</div><h3>Package repeatable operations</h3><p>Turn informal know-how into shared Solutions for sales, support, finance, delivery, and back-office work.</p><ul><li>Reusable Service contracts</li><li>Shared connectors and policies</li><li>Traceable outcomes without a platform team</li></ul><a class="card-link" href="solutions.html#small-business">See the business path →</a></article>
    <article class="card violet" data-reveal><div class="meta">Enterprise</div><h3>Govern an ecosystem</h3><p>Operate many tenants, capability publishers, model providers, data products, risk tiers, regions, and deployment profiles.</p><ul><li>Separation of duties</li><li>Immutable supply chain and evidence</li><li>Dedicated, sovereign, or disconnected profiles</li></ul><a class="card-link" href="solutions.html#enterprise">See the enterprise path →</a></article>
  </div>
</section>

<section class="container section compact">
  <div class="band" data-reveal>
    <p class="section-kicker">The central promise</p>
    <h2>ContextWeaver lets customers build their own AI capabilities while the platform safely discovers, validates, compiles, approves, orchestrates, recovers, observes, and proves every outcome.</h2>
    <div class="button-row"><a class="button primary" href="studio.html">Next: create a capability →</a><a class="button" href="platform.html">See the platform model</a></div>
  </div>
</section>
"""

PLATFORM = """
<section class="container hero" style="min-height:610px">
  <div>
    <p class="eyebrow">Product architecture</p>
    <h1>Three systems. One <em>governed fabric.</em></h1>
    <p class="lede"><strong>Cerebro</strong> understands and governs. <strong>Weave</strong> composes user-facing Solutions from reusable Services, Workflows, Agents, MCPs, RAG profiles, models, and policies. <strong>Loom</strong> provides the portable Kubernetes, GitOps, data, messaging, identity, secrets, and observability foundation.</p>
  </div>
  {platform_city}
</section>

<section class="container section compact">
  <div class="section-head"><div><p class="section-kicker">Eight coordinated planes</p><h2>Stable product semantics above replaceable infrastructure.</h2></div><p>Cloud services implement platform contracts. They do not redefine identity, policy, Workflow, transaction, evidence, or lifecycle semantics.</p></div>
  {platform_planes}
</section>

<section class="container section">
  <div class="section-head"><div><p class="section-kicker">The planes</p><h2>Each layer has a precise responsibility and boundary.</h2></div><p>Separation makes the system easier to operate, replace, scale, audit, and reason about than a single unrestricted “AI application.”</p></div>
  <div class="grid four">
    <article class="card violet" data-reveal><div class="meta">01</div><h3>Experience</h3><p>One authenticated entry point presents Builder/Admin Studio, Consumer My Solutions, or delegated headless access according to entitlement.</p></article>
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
  <div class="plain-language" data-reveal>
    <div><p class="section-kicker">Plain-language model</p><h2>Think of the platform as a governed factory.</h2></div>
    <p><strong>Cerebro</strong> is the control room, <strong>Weave</strong> is the approved parts catalog, and <strong>Loom</strong> is the factory floor. Models can suggest an assembly plan, but they cannot approve their own parts, issue themselves credentials, or bypass the safety gates.</p>
  </div>
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

<section class="container section compact">
  <div class="chapter-next">
    <div><p class="section-kicker">Next chapter</p><h2>See how capabilities are created, inspected, rehearsed, and promoted.</h2><p>Move from the platform model into the guided and developer creation experience.</p></div>
    <a class="button primary" href="studio.html">Open Studio →</a>
  </div>
</section>
"""

STUDIO = """
<section class="container hero" style="min-height:640px">
  <div>
    <p class="eyebrow">Unified capability Studio</p>
    <h1>Move from one intent to <em>five governed contexts.</em></h1>
    <p class="lede">MCPs, Agents, Workflows, Services, and Solutions now share one tabbed workspace. A guided GUI supports non-programmers while typed drafts, schemas, dependency graphs, code, and review remain available to engineers.</p>
    <div class="hero-actions"><a class="button primary" href="#create">See the creation flow</a><a class="button" href="architecture.html#capability-lifecycle">See lifecycle architecture</a></div>
  </div>
  {layered_architecture}
</section>

<section class="container section compact">
  <div class="section-head"><div><p class="section-kicker">Current realization</p><h2>The authoring workspace is connected to real Registry contracts.</h2></div><p>AI interpretation proposes normalized intent and exact references from governed context. Deterministic compilation validates the result; authoring does not publish, deploy, execute, grant authority, or apply side effects.</p></div>
  <div class="grid three">{studio_facts}</div>
</section>

<section id="create" class="container section compact">
  <div class="section-head"><div><p class="section-kicker">Create, dry run, publish</p><h2>One workspace for the complete capability lifecycle.</h2></div><p>Everything generated remains inspectable and editable: specifications, schemas, prompts, code, tests, policies, configuration references, Helm overlays, dashboards, and evidence.</p></div>
  {capability_lifecycle}
</section>

<section class="container section">
  <div class="section-head"><div><p class="section-kicker">What can be created</p><h2>Four reusable runtime artifact types—and the Solution that composes them.</h2></div><p>The Studio makes each responsibility explicit: an MCP is not an Agent, a Workflow is not a Service, and a reusable Service is not the complete user-facing Solution.</p></div>
  <div class="grid four">
    <article class="card sky" data-reveal><div class="meta">MCP capability</div><h3>The governed tool boundary</h3><p>Exposes tools, resources, and prompts with typed schemas, delegated identity, side-effect classes, receipts, idempotency, and compensation metadata.</p></article>
    <article class="card violet" data-reveal><div class="meta">Agent</div><h3>The bounded reasoning specialist</h3><p>Uses an approved model, knowledge, instructions, budgets, and MCP allow-list to produce a typed result for one defined responsibility.</p></article>
    <article class="card amber" data-reveal><div class="meta">Workflow</div><h3>The durable coordination graph</h3><p>Orders Agent and capability work through typed steps, branches, parallel joins, waits, approvals, callbacks, retries, checkpoints, and compensation.</p></article>
    <article class="card mint" data-reveal><div class="meta">Service</div><h3>The reusable executable contract</h3><p>Publishes a stable intent-to-outcome contract pinned to one or more approved Workflows, with inputs, outputs, policies, SLOs, and lifecycle.</p></article>
    <article class="card coral" data-reveal><div class="meta">Solution</div><h3>The final user-facing composition</h3><p>Packages the complete dependency graph, experience contract, presentation, lifecycle, and one or more Services into what a consumer actually discovers and uses.</p></article>
  </div>
</section>

<section class="container section compact">
  <div class="plain-language" data-reveal>
    <div><p class="section-kicker">Plain-language model</p><h2>A workshop with an inspection window.</h2></div>
    <p>The Studio does not hide what it generates. It is closer to a workshop where every drawing, part, test, safety check, and release package remains visible. Non-programmers get guidance; engineers can open the exact specifications, schemas, code, policies, and deployment assets.</p>
  </div>
</section>

<section class="container section">
  <div class="section-head"><div><p class="section-kicker">Studio workspace</p><h2>Designed for hundreds of capabilities and complete Solutions.</h2></div><p>Catalogs make reusable components discoverable; the Solution context assembles their complete dependency graph and consumer experience without copying those components.</p></div>
  <div class="grid three">
    <article class="card mint"><div class="meta">Agent catalog</div><h3>Find the right specialist</h3><ul><li>Search by capability, owner, domain, trust, region, model envelope, and evaluation</li><li>Compare exact versions, schemas, SLOs, support, and consumers</li><li>Inspect Agent Cards, dependencies, dashboards, and recent runs</li><li>Create, clone, modify, deprecate, drain, or retire through governed actions</li></ul></article>
    <article class="card violet"><div class="meta">MCP catalog</div><h3>Find the right tool boundary</h3><ul><li>Search by tool, provider, side-effect class, data scope, credential profile, and region</li><li>Inspect schemas, transports, rate limits, idempotency, receipts, and compensation</li><li>See every Service, Workflow, and Agent consumer before an update or removal</li><li>Test through a safe sandbox without exposing provider credentials to the Agent</li></ul></article>
    <article class="card amber"><div class="meta">Solution context</div><h3>Assemble the complete experience</h3><ul><li>Select immutable MCP, Agent, Workflow, and Service versions instead of cloning them</li><li>Inspect the complete dependency graph, experience contract, entry actions, policies, and lifecycle</li><li>Qualify and publish a consumer-ready Solution without executing it during authoring</li><li>Expose the published experience through My Solutions and delegated channels</li></ul></article>
  </div>
</section>

<section class="container section compact">
  <div class="band">
    <p class="section-kicker">Inputs to a new capability</p>
    <h2>Start from OpenAPI, AsyncAPI, MCP, source code, an RFC, product documentation, a wiki, a data product, an industry pack, or simply a described outcome.</h2>
    <div class="pills" style="margin-top:22px"><span class="pill">Import</span><span class="pill">Discover</span><span class="pill">Generate</span><span class="pill">Edit</span><span class="pill">Validate</span><span class="pill">Simulate</span><span class="pill">Scan</span><span class="pill">Approve</span><span class="pill">Publish</span><span class="pill">Deploy</span><span class="pill">Observe</span><span class="pill">Improve</span></div>
  </div>
</section>

<section class="container section compact">
  <div class="chapter-next">
    <div><p class="section-kicker">Next chapter</p><h2>Follow three Solution outcomes through a governed Service Run.</h2><p>See how a user action resolves an approved Service, admitted capabilities, approvals, durable execution, and evidence.</p></div>
    <a class="button primary" href="runtime.html#scenarios">See it run →</a>
  </div>
</section>
"""

RUNTIME = """
<section class="container hero" style="min-height:650px">
  <div>
    <p class="eyebrow">Governed dynamic execution</p>
    <h1>Dynamic enough to adapt. <em>Bounded enough to trust.</em></h1>
    <p class="lede">A user launches a Solution action defined by its Service Experience Contract. ContextWeaver resolves the approved Service and Workflow, or constrained-composes a plan from admitted capabilities; identity, schemas, policy, compatibility, approvals, and the compiler determine whether it can run.</p>
    <div class="hero-actions"><a class="button primary" href="#flow">Walk through a run</a><a class="button" href="#run-history">Inspect run history</a><a class="button" href="governance.html">Review the safeguards</a></div>
  </div>
  {governed_call_flow}
</section>

<section class="container section compact">
  <div class="section-head"><div><p class="section-kicker">Solution to runtime</p><h2>The user sees a Solution. The platform executes a governed Service Run.</h2></div><p>This separation lets product teams evolve presentation and lifecycle independently while the runtime reuses stable, typed, observable execution contracts.</p></div>
  <div class="steps">
    <article class="step"><div><h3>Discover the Solution</h3><p>The consumer portal or delegated client returns only Solutions permitted for the authenticated user, tenant, purpose, and current entitlement state.</p></div></article>
    <article class="step"><div><h3>Choose an experience action</h3><p>The published Service Experience Contract defines the title, description, fields, actions, progress, approvals, result views, and evidence links presented to the user.</p></div></article>
    <article class="step"><div><h3>Resolve the reusable Service</h3><p>The selected action maps to a stable Service contract pinned to an approved Workflow and exact reusable capability versions.</p></div></article>
    <article class="step"><div><h3>Execute and return evidence</h3><p>The existing Service Run API performs durable governed execution; the Solution experience presents status, approvals, results, history, citations, receipts, and trace links.</p></div></article>
  </div>
</section>

<section id="flow" class="container section compact">
  <div class="section-head"><div><p class="section-kicker">Prompt to proved outcome</p><h2>A run is a state machine, not a stream of hopeful messages.</h2></div><p>Click components and step through the active path. The diagram distinguishes identity and policy, authorized data, Agent reasoning, MCP side effects, approval, durable execution, and evidence.</p></div>
  {governed_run}
</section>

<section class="container section compact">
  <div class="section-head"><div><p class="section-kicker">Three runtime views</p><h2>Read the same run by route, message order, or durable recovery.</h2></div><p>Each technical view preserves a different invariant: the service path, exact participant timing, or the state and compensation model behind long-running work.</p></div>
  <div class="spatial-gallery spatial-gallery-three">
    {governed_call_flow}
    {governed_sequence_ladder}
    {durable_saga_flow}
  </div>
</section>

<section id="generic-agent-runtime" class="container section compact">
  <div class="section-head"><div><p class="section-kicker">Profile-bound Agents</p><h2>One hardened image. Many isolated logical Agents.</h2></div><p>Role, schemas, executor, MCP access, budgets, queues, and runtime compatibility are injected through immutable profiles. Each logical Agent retains independent identity, networking, scaling, rollout, and rollback.</p></div>
  {generic_agent_runtime}
</section>

<section class="container section compact">
  <div class="section-head"><div><p class="section-kicker">Current runtime realization</p><h2>Composition, delegation, retrieval, and approval now share one evidence model.</h2></div><p>Plans are exact-version and digest pinned. Agents receive only authorized MCP bindings, retrieval returns citations and receipts, and policy-required dynamic plans cannot execute before approval of the exact immutable plan.</p></div>
  <div class="grid three">{runtime_facts}</div>
</section>

<section id="run-history" class="container section">
  <div class="section-head"><div><p class="section-kicker">Run history and evidence</p><h2>Inspect the journey—not just the final answer.</h2></div><p>The consumer sees a clear progression and result. Builders, approvers, and operators can drill into the immutable plan, Workflow nodes, approvals, retries, tool calls, evidence, and recovery decisions behind it.</p></div>
  <div class="run-explorer" data-reveal aria-label="Illustrative ContextWeaver Run Explorer product view">
    <div class="run-explorer-bar">
      <div class="run-explorer-brand"><span class="run-explorer-mark">CW</span><div><small>ContextWeaver</small><strong>Run Explorer</strong></div></div>
      <div class="run-explorer-path"><span>Production health</span><b>/</b><strong>Run SR-2847</strong></div>
      <span class="run-status complete"><i></i> Completed with approval</span>
    </div>
    <div class="run-explorer-tabs" aria-label="Run Explorer sections">
      <span>Summary</span><span class="active">Journey</span><span>Evidence</span><span>Artifacts</span>
    </div>
    <div class="run-explorer-body">
      <aside class="run-journey" aria-label="Run journey">
        <div class="run-id"><small>Service run</small><strong>Investigate production regression</strong><span>8m 42s · 12 steps · Risk: medium</span></div>
        <ol>
          <li class="done"><i>✓</i><div><strong>Intent received</strong><span>10:32:08 · User request</span></div></li>
          <li class="done"><i>✓</i><div><strong>Capabilities admitted</strong><span>10:32:09 · 6 approved</span></div></li>
          <li class="done"><i>✓</i><div><strong>Dry run evaluated</strong><span>10:32:12 · 4 checks passed</span></div></li>
          <li class="done"><i>✓</i><div><strong>Plan approved</strong><span>10:34:21 · Independent reviewer</span></div></li>
          <li class="active"><i>5</i><div><strong>Investigate regression</strong><span>10:34:23 · Agent step</span></div></li>
          <li class="done"><i>✓</i><div><strong>Result delivered</strong><span>10:40:50 · Evidence attached</span></div></li>
        </ol>
      </aside>
      <div class="run-step-detail" aria-label="Selected workflow step details">
        <div class="run-step-heading">
          <div><small>Workflow node 5 of 12</small><h3>Investigate regression</h3><p>Compare release changes with the observed error spike using only admitted telemetry and repository evidence.</p></div>
          <span class="run-status complete"><i></i> Succeeded</span>
        </div>
        <div class="run-detail-grid">
          <article><span>Bounded specialist</span><strong>Production diagnosis Agent</strong><small>Profile v3.8 · Model envelope approved</small></article>
          <article><span>Duration</span><strong>2m 18s</strong><small>Within 5-minute budget</small></article>
          <article><span>Accepted artifact</span><strong>Diagnosis report</strong><small>SHA-256 · immutable version</small></article>
        </div>
        <div class="run-result">
          <div class="run-result-head"><span>Accepted output</span><strong>Confidence 94%</strong></div>
          <h4>Release 2026.11.01 introduced a retry-path regression.</h4>
          <p>Error growth begins seven minutes after ring deployment and correlates with a changed timeout branch. No evidence indicates data loss. Rollback remains a separately approved human action.</p>
          <div class="run-citations"><span>[1] Release diff</span><span>[2] Trace cohort</span><span>[3] Error budget</span><span>[4] Runbook</span></div>
        </div>
        <div class="run-receipt-row">
          <span><i>✓</i> Typed input validated</span>
          <span><i>✓</i> 3 tool receipts</span>
          <span><i>✓</i> Policy decision PD-8821</span>
          <span><i>✓</i> No credentials disclosed</span>
        </div>
      </div>
      <aside class="run-evidence" aria-label="Evidence summary">
        <div><small>Authority</small><strong>Delegated read-only</strong><span>Production operator</span></div>
        <div><small>Approval</small><strong>Maya Chen</strong><span>Separation of duty verified</span></div>
        <div><small>MCP operations</small><strong>3 completed</strong><span>Logs · Traces · Repository</span></div>
        <div><small>Evidence</small><strong>18 records</strong><span>Citations, receipts, metrics, traces</span></div>
        <button type="button">Export evidence bundle</button>
      </aside>
    </div>
    <p class="run-explorer-note">Illustrative product view — exact fields and controls vary by Solution, Service, role, and policy profile.</p>
  </div>
  <div class="grid four">
    <article class="card mint"><div class="meta">Run summary</div><h3>Who asked for what—and what happened?</h3><p>Solution, action, Service, initiator, delegated client, purpose, status, risk, start and finish time, current owner, and final outcome.</p></article>
    <article class="card amber"><div class="meta">Journey timeline</div><h3>Follow every meaningful state transition.</h3><p>Intent received, capabilities admitted, dry run completed, plan approved, work dispatched, waits entered, retries or compensation applied, and result delivered.</p></article>
    <article class="card coral"><div class="meta">Step evidence</div><h3>Open any Workflow node.</h3><p>Inspect the Agent or control step, typed inputs and outputs, source citations, model and prompt version, MCP operation, latency, retries, and accepted artifact hash.</p></article>
    <article class="card sky"><div class="meta">Authority and receipts</div><h3>See why each protected action was allowed.</h3><p>Policy decision, approver, separation of duties, delegated identity, credential-broker event, tool and policy receipts, disclosure decision, logs, metrics, and traces.</p></article>
  </div>
  <div class="grid two solution-example-grid">
    <article class="card mint"><div class="meta">Dry-run comparison</div><h3>Compare rehearsal with production.</h3><p>See mocked side effects, sample or protected-data boundaries, estimated cost and latency, expected approvals, quality and safety evaluation, failure injection, retry, rollback, and the exact version promoted after review.</p></article>
    <article class="card amber"><div class="meta">Evidence bundle</div><h3>Export the proof with the outcome.</h3><p>Preserve the immutable plan digest, component versions, approvals, citations, provider receipts, artifacts, policy decisions, evaluations, run timeline, trace links, and retention classification.</p></article>
  </div>
</section>

<section id="scenarios" class="container section scenario-section">
  <div class="section-head">
    <div><p class="section-kicker">See it run</p><h2>Three outcomes. One governed execution pattern.</h2></div>
    <p>These illustrative journeys make the architecture concrete. Exact connectors and side effects depend on the admitted capabilities in a customer deployment.</p>
  </div>
  <div class="scenario-tabs" role="tablist" aria-label="Illustrative ContextWeaver scenarios">
    <button class="scenario-tab active" id="scenario-tab-incident" role="tab" aria-selected="true" aria-controls="scenario-incident" data-scenario="scenario-incident">Production incident</button>
    <button class="scenario-tab" id="scenario-tab-sales" role="tab" aria-selected="false" aria-controls="scenario-sales" data-scenario="scenario-sales">Customer renewal</button>
    <button class="scenario-tab" id="scenario-tab-travel" role="tab" aria-selected="false" aria-controls="scenario-travel" data-scenario="scenario-travel">Travel coordination</button>
  </div>
  <div class="scenario-stage">
    <article class="scenario-panel active" id="scenario-incident" role="tabpanel" aria-labelledby="scenario-tab-incident">
      <div class="scenario-heading"><div><span class="status-badge illustrative">Illustrative</span><h3>Investigate a production regression</h3></div><p>An SRE asks for an evidence-backed assessment without giving an Agent unrestricted production authority.</p></div>
      <ol class="scenario-flow">
        <li><b>Intent</b><span>“Explain the error spike after the latest release and prepare the safest next action.”</span></li>
        <li><b>Admit</b><span>Resolve the incident, telemetry, repository, release, and runbook capabilities allowed for this operator.</span></li>
        <li><b>Dry run</b><span>Show proposed queries, data scopes, parallel investigations, budgets, and any action that would need approval.</span></li>
        <li><b>Authorize</b><span>Policy permits read-only investigation and draft preparation; rollback or incident acknowledgment remains human-controlled.</span></li>
        <li><b>Execute</b><span>Agents inspect logs, traces, recent changes, and known patterns in parallel while durable state preserves progress.</span></li>
        <li><b>Prove</b><span>Return the diagnosis, confidence, citations, tool receipts, policy decisions, and a separately reviewable remediation plan.</span></li>
      </ol>
    </article>
    <article class="scenario-panel" id="scenario-sales" role="tabpanel" aria-labelledby="scenario-tab-sales" hidden>
      <div class="scenario-heading"><div><span class="status-badge illustrative">Illustrative</span><h3>Prepare a customer renewal brief</h3></div><p>An account team needs a current, source-backed view without mixing customer data or sending unreviewed communication.</p></div>
      <ol class="scenario-flow">
        <li><b>Intent</b><span>“Prepare the renewal brief, identify open commitments, and draft the customer follow-up.”</span></li>
        <li><b>Admit</b><span>Resolve approved CRM, support, contract, product, and document sources for the user, account, and purpose.</span></li>
        <li><b>Dry run</b><span>Preview the fields to retrieve, the comparison logic, and the proposed communication before protected work begins.</span></li>
        <li><b>Authorize</b><span>Policy filters account data, excludes unrelated customers, and requires an account owner to approve external communication.</span></li>
        <li><b>Execute</b><span>Workers assemble history, commitments, risks, usage evidence, and recommended actions into a typed brief.</span></li>
        <li><b>Prove</b><span>Deliver citations, freshness, missing-data warnings, approval state, and a draft that cannot be sent autonomously.</span></li>
      </ol>
    </article>
    <article class="scenario-panel" id="scenario-travel" role="tabpanel" aria-labelledby="scenario-tab-travel" hidden>
      <div class="scenario-heading"><div><span class="status-badge target">Profile-dependent</span><h3>Coordinate a policy-compliant trip</h3></div><p>A traveler wants an itinerary assembled across providers while retaining explicit approval for booking and payment.</p></div>
      <ol class="scenario-flow">
        <li><b>Intent</b><span>“Plan the trip within company policy, compare practical options, and prepare it for approval.”</span></li>
        <li><b>Admit</b><span>Resolve travel policy, calendar, approved search providers, expense limits, identity, and regional constraints.</span></li>
        <li><b>Dry run</b><span>Present candidate providers, data shared with each one, estimated cost, timing, and proposed booking actions.</span></li>
        <li><b>Authorize</b><span>Policy removes disallowed options and requires the traveler or delegated approver before any external commitment.</span></li>
        <li><b>Execute</b><span>Search tasks run in parallel; a Workflow joins the results, applies preferences, and pauses durably for approval.</span></li>
        <li><b>Prove</b><span>Return the itinerary, comparison evidence, approval record, and provider receipts when configured connectors perform a booking.</span></li>
      </ol>
    </article>
  </div>
</section>

<section class="container section compact">
  <div class="plain-language" data-reveal>
    <div><p class="section-kicker">Plain-language model</p><h2>A relay race with signed handoffs.</h2></div>
    <p>A Workflow is not one Agent improvising from start to finish. Each specialist receives only the baton it needs, passes a typed result to the next stage, and records the handoff. Checkpoints let the race pause for approval or resume with another worker after failure.</p>
  </div>
</section>

<section class="container section">
  <div class="section-head"><div><p class="section-kicker">Run lifecycle</p><h2>The simple view of a rigorous execution model.</h2></div><p>The full design contains more granular authorization, retrieval, binding, checkpoint, disclosure, and audit states; users see a comprehensible progression.</p></div>
  <div class="steps">
    <article class="step"><div><h3>Receive and scrutinize intent</h3><p>Resolve identity, tenant, roles, relationships, device, purpose, risk, classification, entities, ambiguity, and candidate outcomes.</p></div></article>
    <article class="step"><div><h3>Resolve the Solution action</h3><p>Map the selected experience action to an approved Service, ask a clarifying question, or propose a graph from only admitted capabilities and control nodes.</p></div></article>
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

<section class="container section compact">
  <div class="chapter-next">
    <div><p class="section-kicker">Next chapter</p><h2>Understand the authority, credential, policy, and evidence boundaries.</h2><p>The scenarios become trustworthy only when the runtime cannot expand its own permissions.</p></div>
    <a class="button primary" href="governance.html">Open the trust model →</a>
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
  {governed_call_flow}
</section>

<section class="container section compact">
  <div class="section-head"><div><p class="section-kicker">Current control realization</p><h2>Authority is bound to identity, resource, purpose, and side effect.</h2></div><p>Interactive roles do not imply side-effect authority. External clients receive identity-filtered discovery, provider credentials remain platform-owned, and each permitted action is bound to exact policy and entitlement evidence.</p></div>
  <div class="grid three">{governance_facts}</div>
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
  <div class="plain-language" data-reveal>
    <div><p class="section-kicker">Plain-language model</p><h2>A guarded service counter—not a key handoff.</h2></div>
    <p>When an Agent needs an external system, the trusted gateway checks the exact request, uses a narrowly scoped credential on its behalf, and returns only the permitted result. The Agent never walks away holding the provider credential.</p>
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

<section class="container section compact">
  <div class="chapter-next">
    <div><p class="section-kicker">Next chapter</p><h2>See how the same contracts scale across people, teams, industries, and isolation profiles.</h2><p>Governance grows with the operating model without changing the core capability language.</p></div>
    <a class="button primary" href="solutions.html">Explore adoption paths →</a>
  </div>
</section>
"""

SOLUTIONS = """
<section class="container hero" style="min-height:660px">
  <div>
    <p class="eyebrow">The user-facing product layer</p>
    <h1>Solutions are what people <em>discover, launch, and trust.</em></h1>
    <p class="lede">A ContextWeaver Solution is the final user-facing composition: a complete experience, dependency graph, lifecycle, and set of reusable Services assembled from governed Workflows, Agents, MCP capabilities, knowledge, models, and policy.</p>
    <div class="hero-actions"><a class="button primary" href="#examples">See intent-to-outcome examples</a><a class="button" href="#concepts">Understand the hierarchy</a></div>
  </div>
  {intent_to_evidence}
</section>

<section class="container section compact">
  <div class="section-head"><div><p class="section-kicker">Current realization</p><h2>The product now has an explicit Solution layer and consumer entry point.</h2></div><p>These reviewed facts distinguish implemented foundations from target architecture and connect the authoring model to how a regular user or external assistant actually uses the platform.</p></div>
  <div class="grid three">{solution_facts}</div>
</section>

<section id="concepts" class="container section">
  <div class="section-head"><div><p class="section-kicker">Conceptual model</p><h2>Five concepts. Five different responsibilities.</h2></div><p>Service is the reusable executable contract. Solution is the complete user experience. Each layer adds meaning without erasing the layer beneath it.</p></div>
  <div class="grid four">
    <article class="card sky"><div class="meta">01 · MCP capability</div><h3>A governed way to reach a tool or source</h3><p>Defines tools, resources, prompts, schemas, delegated identity, side-effect risk, receipts, rate limits, idempotency, and compensation. It does not decide the business goal.</p></article>
    <article class="card violet"><div class="meta">02 · Agent</div><h3>A bounded reasoning specialist</h3><p>Uses an approved model, instructions, knowledge, skills, and MCP allow-list to perform one typed responsibility. It does not own end-to-end durable coordination.</p></article>
    <article class="card amber"><div class="meta">03 · Workflow</div><h3>A durable coordination graph</h3><p>Sequences and joins typed work across Agents, MCPs, waits, approvals, events, retries, checkpoints, and compensation. It defines how work progresses and recovers.</p></article>
    <article class="card mint"><div class="meta">04 · Service</div><h3>A reusable executable intent-to-outcome contract</h3><p>Publishes stable inputs, outputs, policies, SLOs, ownership, lifecycle, and one or more approved Workflows. It is the unit launched through the Service Run API.</p></article>
    <article class="card coral"><div class="meta">05 · Solution</div><h3>The final user-facing composition</h3><p>Combines one or more Services with the complete dependency graph, presentation, entry actions, lifecycle, entitlement, and Service Experience Contract that a consumer sees.</p></article>
  </div>
</section>

<section class="container section compact">
  <div class="plain-language" data-reveal>
    <div><p class="section-kicker">Plain-language model</p><h2>A restaurant, not a pile of kitchen equipment.</h2></div>
    <p>MCP capabilities are the appliances and supplier interfaces. Agents are skilled specialists. Workflows are the coordinated kitchen process. Services are reusable menu-item contracts the kitchen can reliably produce. The Solution is the complete restaurant experience the customer discovers, orders from, follows, and evaluates.</p>
  </div>
</section>

<section id="examples" class="container section">
  <div class="section-head"><div><p class="section-kicker">Five illustrative examples</p><h2>A Solution carries a person from intent to outcome.</h2></div><p>The user asks for an outcome, not a Workflow or MCP. The Solution presents the experience, composes reusable Services, and lets each Service select approved Workflows, Agents, and MCP capabilities behind a stable contract.</p></div>
  <article class="card mint solution-example-feature" data-reveal>
    <div class="meta">Example 01 · Business travel Solution</div>
    <h3>“Arrange an approved trip to Seattle and keep me informed.”</h3>
    <p>The traveler sees one guided experience. ContextWeaver preserves the reusable execution layers beneath it.</p>
    <div class="intent-chain" aria-label="Business travel intent-to-outcome chain">
      <div><span>01 · Intent</span><strong>Arrange the trip</strong><small>Dates, purpose, preferences, budget</small></div>
      <div><span>02 · Solution</span><strong>Business Travel</strong><small>Forms, actions, progress, approvals</small></div>
      <div><span>03 · Services</span><strong>Plan, approve, pay, notify</strong><small>Four reusable executable contracts</small></div>
      <div><span>04 · Workflows</span><strong>Search, compare, approve, book</strong><small>Waits, retries, recovery, receipts</small></div>
      <div><span>05 · Agents + MCPs</span><strong>Reason and act</strong><small>Travel specialist, policy, booking, payment</small></div>
      <div><span>06 · Outcome</span><strong>Approved booked itinerary</strong><small>Confirmation, receipts, evidence, history</small></div>
    </div>
  </article>
  <div class="grid two solution-example-grid">
    <article class="card amber" data-reveal><div class="meta">Example 02 · Employee onboarding Solution</div><h3>“Have this employee ready for Monday.”</h3><ul><li><strong>Services:</strong> worker verification, access provisioning, equipment fulfillment, training, notification</li><li><strong>Workflows:</strong> validate identity, obtain manager approval, provision in parallel, escalate blockers</li><li><strong>Outcome:</strong> a ready employee with approvals, exceptions, ownership, and evidence</li></ul></article>
    <article class="card coral" data-reveal><div class="meta">Example 03 · Customer incident recovery Solution</div><h3>“Restore service and keep the customer informed.”</h3><ul><li><strong>Services:</strong> incident triage, production change, customer communication, post-incident review</li><li><strong>Workflows:</strong> enrich and diagnose, approve a change, canary and rollback, publish updates</li><li><strong>Outcome:</strong> restored service, controlled change, customer timeline, and traceable evidence</li></ul></article>
    <article class="card mint" data-reveal><div class="meta">Example 04 · Insurance claim Solution</div><h3>“Assess this claim and settle it fairly.”</h3><ul><li><strong>Services:</strong> document intake, coverage decision, fraud review, settlement payment, notification</li><li><strong>Workflows:</strong> extract and validate, collect missing evidence, route adjuster approval, issue payment</li><li><strong>Outcome:</strong> an explained decision, approved settlement, payment receipt, and complete case history</li></ul></article>
    <article class="card sky" data-reveal><div class="meta">Example 05 · Software release Solution</div><h3>“Release this change safely to production.”</h3><ul><li><strong>Services:</strong> specification review, change validation, release promotion, stakeholder communication</li><li><strong>Workflows:</strong> build and test, risk approval, staged rings, health checks, automatic pause or rollback</li><li><strong>Outcome:</strong> a qualified release with approval, rollout status, rollback posture, and evidence</li></ul></article>
  </div>
</section>

<section class="container section compact">
  <div class="section-head"><div><p class="section-kicker">Reuse without duplication</p><h2>The layers are many-to-many—governed by typed contracts.</h2></div><p>Solutions package context and experience; they do not copy the assets below them. Approved versions are referenced, composed, and independently evolved.</p></div>
  <div class="grid four">
    <article class="card mint"><div class="meta">Solution → Service</div><h3>One Solution can compose many Services.</h3><p>Business Travel combines planning, approval, payment, and notification Services into one experience.</p></article>
    <article class="card amber"><div class="meta">Service → Solution</div><h3>One Service can support many Solutions.</h3><p>The same Notification Service can serve travel, onboarding, incident, claims, and release Solutions.</p></article>
    <article class="card coral"><div class="meta">Service → Workflow</div><h3>One Service can select one or more approved Workflows.</h3><p>A Payment Service may use standard charge, high-risk approval, refund, and recovery Workflows under one stable contract.</p></article>
    <article class="card sky"><div class="meta">Workflow → Service</div><h3>One typed Workflow can support multiple Services.</h3><p>A generic human-approval Workflow can coordinate travel approval, access grants, production changes, claim settlement, and release promotion.</p></article>
  </div>
  <div class="posture-table-wrap reuse-map" data-reveal>
    <table class="posture-table">
      <thead><tr><th>Reusable asset</th><th>Where it appears</th><th>What remains stable</th></tr></thead>
      <tbody>
        <tr><th>Notification Service</th><td>All five example Solutions</td><td>Message request, delivery status, channel policy, receipts, and audit evidence</td></tr>
        <tr><th>Payment Service</th><td>Business Travel and Insurance Claim Solutions</td><td>Authorize, charge, refund, reconcile, and return a financial receipt</td></tr>
        <tr><th>Human Approval Workflow</th><td>Travel Approval, Access Provisioning, Production Change, Claims Settlement, and Release Promotion Services</td><td>Assignee rules, separation of duties, wait, timeout, escalation, decision, and evidence</td></tr>
        <tr><th>Evidence Packaging Workflow</th><td>Travel Receipt, Post-Incident Review, Claims Decision, and Release Evidence Services</td><td>Collect lineage, approvals, citations, receipts, summaries, and immutable references</td></tr>
        <tr><th>Identity and directory MCP capabilities</th><td>Employee Onboarding, Incident Recovery, and Software Release Solutions</td><td>Governed access to users, groups, roles, ownership, and entitlements without owning the business outcome</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section id="consumer" class="container section">
  <div class="section-head"><div><p class="section-kicker">One authentication entry point</p><h2>The same platform presents the right experience for each user.</h2></div><p>Entitlements determine presentation after sign-in. Consumer users do not need to navigate internal MCPs, Agents, Workflows, or cluster resources, while builders and operators retain the detailed controls they need.</p></div>
  <div class="grid three">
    <article class="card mint"><div class="meta">Consumer</div><h3>My Solutions</h3><p>Consumer-only users land on <strong>/my-solutions</strong>, discover permitted Solutions, launch experience actions, provide inputs, approve when required, and inspect status, results, history, citations, and receipts.</p></article>
    <article class="card amber"><div class="meta">Builder / Admin</div><h3>Studio and operations</h3><p>Authorized builders move through MCP, Agent, Workflow, Service, and Solution contexts in one Studio. Operators manage identity, policy, publication, runtime health, evidence, and lifecycle.</p></article>
    <article class="card violet"><div class="meta">Headless / delegated</div><h3>Copilot, Claude, API, or event</h3><p>External assistants discover and invoke only the Solutions and actions allowed for the represented user. Delegated identity is preserved end to end; provider credentials remain platform-owned.</p></article>
  </div>
</section>

<section class="container section compact">
  <div class="section-head"><div><p class="section-kicker">Consumer journey</p><h2>From sign-in to evidence-backed result.</h2></div><p>The user journey stays simple because the platform preserves the complexity and proof beneath it.</p></div>
  <div class="steps">
    <article class="step"><div><h3>Sign in once</h3><p>ContextWeaver resolves tenant, user, role, groups, relationships, purpose, session, device, and current entitlement state.</p></div></article>
    <article class="step"><div><h3>Open My Solutions</h3><p>The portal returns only published Solutions currently permitted for this user and context.</p></div></article>
    <article class="step"><div><h3>Choose an experience action</h3><p>The Service Experience Contract renders approved fields, guidance, progress, approval points, result views, and evidence links.</p></div></article>
    <article class="step"><div><h3>Launch the Service Run</h3><p>The action maps to a reusable Service and approved Workflow. The runtime freezes exact capability, policy, source, model, and configuration versions.</p></div></article>
    <article class="step"><div><h3>Follow progress and approve</h3><p>Durable state survives waits and failures. Human authority is requested explicitly when policy requires it.</p></div></article>
    <article class="step"><div><h3>Receive the result and proof</h3><p>The Solution presents the outcome with appropriate citations, receipts, approvals, lineage, run history, and trace links.</p></div></article>
  </div>
</section>

<section id="journey-map" class="container section compact">
  <div class="section-head"><div><p class="section-kicker">Continue the journey</p><h2>Each page opens a different layer of the actual product experience.</h2></div><p>Start with the user-facing Solution, then move into authoring, rehearsal, execution, run history, evidence, and architecture without losing the same intent-to-outcome thread.</p></div>
  <div class="grid three">
    <article class="card mint"><div class="meta">Create and rehearse</div><h3>Studio</h3><p>See how MCPs, Agents, Workflows, Services, and Solutions are authored, inspected, safely simulated, compared, approved, and promoted.</p><a class="card-link" href="studio.html#create">Open creation and dry runs →</a></article>
    <article class="card amber"><div class="meta">Follow real journeys</div><h3>Runtime scenarios</h3><p>Walk through production incident, customer renewal, and travel examples from intent through admission, dry run, authorization, execution, and proof.</p><a class="card-link" href="runtime.html#scenarios">Open execution scenarios →</a></article>
    <article class="card coral"><div class="meta">Inspect a run</div><h3>Run history and evidence</h3><p>See the journey timeline, immutable plan, Workflow steps, approvals, retries, tool receipts, citations, traces, and exported evidence bundle.</p><a class="card-link" href="runtime.html#run-history">Open run-history deep dive →</a></article>
    <article class="card sky"><div class="meta">Understand authority</div><h3>Governance and evidence</h3><p>Inspect identity, delegated authority, policy decisions, credential brokering, human approval, audit records, and lifecycle controls.</p><a class="card-link" href="governance.html">Open the trust model →</a></article>
    <article class="card mint"><div class="meta">Inspect every boundary</div><h3>Architecture atlas</h3><p>See how the experience, control, capability, runtime, evidence, operations, and infrastructure layers connect.</p><a class="card-link" href="architecture.html#governed-run">Open architecture deep dive →</a></article>
    <article class="card amber"><div class="meta">Watch end to end</div><h3>Interactive intent-to-evidence story</h3><p>Move through the ten-stage governed path from authenticated intent and reusable contracts to durable execution, evidence, outcome, and operations.</p><a class="card-link" href="diagrams/intent-to-evidence.html?popout=1" target="_blank" rel="noopener noreferrer">Open the visual journey ↗</a></article>
  </div>
</section>

<section id="external-assistants" class="container section">
  <div class="section-head"><div><p class="section-kicker">External assistants on behalf of a user</p><h2>Delegation changes the channel—not the authority model.</h2></div><p>A Copilot, Claude client, IDE extension, or another approved assistant does not receive a master key or bypass the consumer model.</p></div>
  <div class="grid four">
    <article class="card sky"><div class="meta">Discover</div><h3>Identity-filtered catalog</h3><p>The capability gateway returns only Solutions, Services, and actions allowed for the represented user, tenant, purpose, and channel.</p></article>
    <article class="card violet"><div class="meta">Delegate</div><h3>Bound user context</h3><p>Short-lived delegated context carries the user, client, scope, purpose, correlation, and revocation state into each protected request.</p></article>
    <article class="card amber"><div class="meta">Invoke</div><h3>Same policy and runtime</h3><p>The gateway reauthorizes the exact action and arguments, then launches the same governed Service Run used by the portal.</p></article>
    <article class="card mint"><div class="meta">Return</div><h3>Minimized result and evidence</h3><p>The assistant receives only the permitted result and references. Connector, cloud, model-provider, and database credentials never enter its context.</p></article>
  </div>
</section>

<section class="container section compact">
  <div class="section-head"><div><p class="section-kicker">Scale path</p><h2>Capability and governance grow together.</h2></div><p>Use the animation to see how identity, sharing, policy, evidence, isolation, and lifecycle controls evolve while the Service, Workflow, Agent, and MCP contracts stay stable.</p></div>
  {scale_path}
</section>

<section id="individual" class="container section">
  <div class="section-head"><div><p class="section-kicker">Individual</p><h2>Use reliable personal Solutions without operating the platform.</h2></div><p>Begin with guided Solution experiences and human confirmation. Keep sources, memory, credentials, Services, and outcomes bounded to the person and purpose.</p></div>
  <div class="grid three">
    <article class="card mint"><h3>Research companion</h3><p>Register approved personal sources, retrieve with citations, compare evidence, and produce a traceable report.</p></article>
    <article class="card sky"><h3>Personal operations</h3><p>Plan travel, track commitments, prepare documents, summarize projects, or coordinate tasks with explicit approval before side effects.</p></article>
    <article class="card violet"><h3>Developer copilot</h3><p>Use code, documentation, repository context, test tools, and deployment workflows without exposing credentials to reasoning components.</p></article>
  </div>
</section>

<section id="small-business" class="container section">
  <div class="section-head"><div><p class="section-kicker">Small business</p><h2>Package how the business works, not just how one person prompts.</h2></div><p>Shared Solutions present complete operating experiences while reusable Services convert repeatable know-how into accountable execution with ownership, permissions, quality checks, and visibility.</p></div>
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

<section class="container section compact">
  <div class="chapter-next">
    <div><p class="section-kicker">Next chapter</p><h2>Inspect the complete platform and its trust boundaries.</h2><p>Move from representative outcomes into the master architecture, lifecycle diagrams, and deployment posture.</p></div>
    <a class="button primary" href="architecture.html">Open the architecture atlas →</a>
  </div>
</section>
"""

ARCHITECTURE = """
<section id="platform-plane-architecture" class="container architecture-atlas-hero">
  <div class="architecture-spatial-hero">
    <div class="architecture-atlas-intro">
      <p class="eyebrow">Master architecture</p>
      <h1>See the Eight Platform Planes. <em>Then inspect every governed layer.</em></h1>
      <p class="lede">This is the approved top-level ContextWeaver architecture: Experience, Governance, Registry, Agents + MCP, Workflow runtime, RAG + memory + models, Evidence, and Infrastructure are coordinated by Cerebro, Weave, and Loom.</p>
      <div class="hero-actions">
        <a class="button primary" href="#interactive-platform-architecture">Open interactive architecture</a>
        <a class="button" href="diagrams/platform-planes.svg">Download architecture SVG</a>
      </div>
    </div>
    <figure class="spatial-visual" data-reveal>
      <button class="spatial-visual-stage spatial-visual-trigger" type="button" data-spatial-open data-spatial-type="image" data-spatial-src="assets/media/platform-planes-static-master.png?v=20261103-2" data-spatial-title="Eight Platform Planes" aria-label="Open large view: Eight Platform Planes">
        <img src="assets/media/platform-planes-static-master.png?v=20261103-2" alt="Eight Platform Planes with Experience, Governance, Registry, Agents and MCP, Workflow runtime, RAG memory and models, Evidence, Infrastructure, Cerebro, Weave, and Loom on three angled rectangular slabs." loading="eager">
        <span class="spatial-visual-expand" aria-hidden="true">Expand ↗</span>
      </button>
      <figcaption>
        <span>Approved master architecture</span>
        <strong>Eight platform planes coordinated by Cerebro, Weave, and Loom</strong>
        <p>The eleven components preserve the approved platform hierarchy, trust boundaries, and portable infrastructure relationship without changing the architecture model.</p>
      </figcaption>
    </figure>
  </div>
</section>

<section id="interactive-platform-architecture" class="container section compact">
  <div class="section-head">
    <div><p class="section-kicker">Interactive platform architecture</p><h2>Inspect every approved plane and platform component.</h2></div>
    <p>Use Play, Pause, Previous, Next, Reset, stage selection, or component inspection to explore the same eleven-component model shown above.</p>
  </div>
  <div class="diagram-shell architecture-atlas-shell" data-reveal>
    <div class="diagram-toolbar">
      <strong>Eight Platform Planes</strong>
      <button class="diagram-toolbar-action" type="button" data-spatial-open data-spatial-type="iframe" data-spatial-src="diagrams/platform-planes.html?popout=1&amp;v=20261103-2" data-spatial-title="Eight Platform Planes">Expand view ↗</button>
    </div>
    <iframe class="diagram-frame architecture-spatial-frame" src="diagrams/platform-planes.html?v=20261103-2" title="Eight Platform Planes" loading="eager" sandbox="allow-scripts allow-same-origin"></iframe>
  </div>
  <p class="diagram-note">Motion follows the active route only. Labels, captions, line styles, and stage controls keep the approved architecture readable when animation is paused or reduced.</p>
  <noscript><p class="diagram-note">JavaScript is required for the interactive player. <a href="diagrams/platform-planes.svg">Open the static platform architecture.</a></p></noscript>
</section>

<section id="technical-architecture-atlas" class="container section compact">
  <div class="section-head">
    <div><p class="section-kicker">19-page technical atlas</p><h2>Inspect every architecture concern in the same rendered-glass perspective.</h2></div>
    <p>Move through layered architecture, deployment, identity, durable execution, RAG, recovery, authorization, operations, and an OpenTelemetry run trace explorer without switching visual systems.</p>
  </div>
  <div class="diagram-shell architecture-atlas-shell" data-reveal>
    <div class="diagram-toolbar">
      <strong>ContextWeaver NextGen Architecture</strong>
      <a class="diagram-toolbar-action" href="diagrams/contextweaver-nextgen-atlas.html?popout=1&amp;v=__ATLAS_ASSET_VERSION__" target="_blank" rel="noopener noreferrer">Open dedicated viewer ↗</a>
    </div>
    <iframe class="diagram-frame architecture-spatial-frame" src="diagrams/contextweaver-nextgen-atlas.html?embedded=1&amp;v=__ATLAS_ASSET_VERSION__" title="ContextWeaver 19-page rendered-glass technical architecture atlas" loading="lazy" sandbox="allow-scripts allow-same-origin allow-downloads"></iframe>
  </div>
  <p class="diagram-note">All 19 pages use photoreal rendered-glass masters with exact semantic overlays. The trace explorer follows W3C context across browser, gateway, policy, workflow, Agent, MCP, model/RAG, queues, stores, and external side effects.</p>
</section>

<section class="container section compact architecture-explorer-intro">
  <div class="section-head">
    <div><p class="section-kicker">Detailed architecture explorers</p><h2>Zoom from the master architecture into one concern at a time.</h2></div>
    <p>The diagrams below preserve the same product semantics and focus separately on capability lifecycle, governed runtime, and scale.</p>
  </div>
  <div class="card amber"><div class="meta">Diagram semantics</div><h3>Motion communicates meaning.</h3><ul><li>Solid pulse: active request or data</li><li>Dashed pulse: identity, policy, or authorization</li><li>Green: validated output or success</li><li>Amber: approval, waiting, retry, or compensation</li><li>Red: denial or failed validation</li><li>Parallel pulses: concurrent Agent work</li></ul></div>
</section>

<section id="explore" class="container section compact">
  <div class="section-head"><div><p class="section-kicker">Interactive diagrams</p><h2>Clickable, controllable, and readable without animation.</h2></div><p>Every player supports Play, Pause, Next, Previous, Reset, stage selection, component inspection, keyboard focus, reduced motion, and a textual explanation.</p></div>
  <div style="display:grid;gap:50px">
    <section id="intent-to-evidence-flow">
      <div class="diagram-shell" data-reveal>
        <div class="diagram-toolbar">
          <strong>Intent to Governed Evidence</strong>
          <a class="diagram-toolbar-action" href="diagrams/intent-to-evidence-flow.html?popout=1&amp;v=20261103-11" target="_blank" rel="noopener noreferrer">Expand view ↗</a>
        </div>
        <iframe class="diagram-frame" src="diagrams/intent-to-evidence-flow.html?embedded=1&amp;v=20261103-11" title="Intent to governed evidence" loading="lazy" sandbox="allow-scripts allow-same-origin"></iframe>
      </div>
      <p class="diagram-note">Seven governed stages move across three receding architectural planes from authenticated intent to a reviewable, replayable result.</p>
    </section>
    <section id="capability-lifecycle">{capability_lifecycle}</section>
    <section id="governed-run">{governed_run}</section>
    <section id="scale-path">{scale_path}</section>
  </div>
</section>

<section id="cloud-posture" class="container section">
  <div class="section-head">
    <div><p class="section-kicker">Cloud and deployment posture</p><h2>Portable contracts. Honest qualification status.</h2></div>
    <p>ContextWeaver separates the cloud-neutral control-plane design from the qualification of a specific provider profile. “Target adapter” means the contract is designed; it does not claim production parity.</p>
  </div>
  <div class="posture-table-wrap" data-reveal>
    <table class="posture-table">
      <thead><tr><th>Capability</th><th>Azure</th><th>AWS</th><th>Google Cloud</th><th>Private / sovereign</th></tr></thead>
      <tbody>
        <tr><th>Kubernetes runtime</th><td>AKS</td><td>EKS target</td><td>GKE target</td><td>Conformant Kubernetes</td></tr>
        <tr><th>Workload identity</th><td>Active adapter</td><td>Target adapter</td><td>Target adapter</td><td>Profile-specific</td></tr>
        <tr><th>Secrets</th><td>Key Vault adapter</td><td>Secrets Manager target</td><td>Secret Manager target</td><td>Native / OpenBao target</td></tr>
        <tr><th>Object and durable state</th><td>Active realization</td><td>Target adapters</td><td>Target adapters</td><td>PostgreSQL + S3-compatible profile</td></tr>
        <tr><th>Search and retrieval</th><td>Active realization</td><td>OpenSearch target</td><td>Search/vector target</td><td>OpenSearch / Qdrant target</td></tr>
        <tr><th>Model providers</th><td>Azure OpenAI adapter</td><td>Bedrock target</td><td>Vertex AI target</td><td>OpenAI-compatible local target</td></tr>
        <tr><th>Observability</th><td colspan="4">OpenTelemetry, Prometheus, Grafana, logs, traces, metrics, and provider-specific export adapters</td></tr>
        <tr class="posture-status"><th>Current posture</th><td><span class="status-badge active">Active realization</span></td><td><span class="status-badge target">Target profile</span></td><td><span class="status-badge target">Target profile</span></td><td><span class="status-badge mixed">Profile-dependent</span></td></tr>
      </tbody>
    </table>
  </div>
</section>

<section class="container section compact">
  <div class="section-head"><div><p class="section-kicker">Current deployment baseline</p><h2>Identity, workspace data, and delivery are being qualified as one operational profile.</h2></div><p>The local and Azure realization now includes repaired Keycloak entry, governed MongoDB workspace access, and reusable immutable CI/CD with SBOM, provenance, rollout-safe updates, and rollback.</p></div>
  <div class="grid three">{architecture_facts}</div>
</section>

<section id="downloads" class="container section">
  <div class="section-head"><div><p class="section-kicker">Portable assets</p><h2>Use the architecture in reviews, proposals, presentations, and implementation planning.</h2></div><p>The editable source contains one Draw.io page per diagram. Static SVG works for print and documentation; GIF works when an interactive player is unavailable.</p></div>
  <div class="grid four">
    <article class="card mint"><div class="meta">Editable</div><h3>Draw.io source</h3><p>Four pages with semantic colors, orthogonal connectors, grouped boundaries, and stable component names.</p><a class="card-link" href="diagrams/contextweaver-public-architecture.drawio">Download .drawio →</a></article>
    <article class="card sky"><div class="meta">Interactive</div><h3>HTML + SVG players</h3><p>Deterministic stages, component details, manual controls, accessible captions, and reduced-motion behavior.</p><a class="card-link" href="diagrams/platform-planes.html">Open a player →</a></article>
    <article class="card violet"><div class="meta">Documentation</div><h3>Static SVG</h3><p>Responsive vector fallback with all components and labels visible when animation or scripting is unavailable.</p><a class="card-link" href="diagrams/governed-run.svg">Open SVG →</a></article>
    <article class="card amber"><div class="meta">Presentation</div><h3>Animated GIF</h3><p>Meaningful stages at one second per frame, optimized for readability rather than decorative speed.</p><a class="card-link" href="diagrams/capability-lifecycle.gif">Open GIF →</a></article>
  </div>
</section>

<section class="container section compact">
  <div class="section-head"><div><p class="section-kicker">Product truth</p><h2>Architecture is a contract and direction—not a claim that every box is production-qualified today.</h2></div><p>The website intentionally distinguishes implemented foundations, active realization, and target architecture. Readiness must be demonstrated for the exact release, deployment profile, risk tier, cloud, region, and customer control environment.</p></div>
</section>

<section class="container section compact">
  <div class="chapter-next">
    <div><p class="section-kicker">Final chapter</p><h2>Move from visual architecture into the technical reasoning behind it.</h2><p>Explore the curated briefs on security, identity, runtime resilience, RAG, observability, cloud neutrality, and deployment readiness.</p></div>
    <a class="button primary" href="learning.html">Open Learning →</a>
  </div>
</section>
""".replace("__ATLAS_ASSET_VERSION__", ATLAS_ASSET_VERSION)

LIBRARY = """
<section class="container hero library-hero">
  <div>
    <p class="eyebrow">Technical library</p>
    <h1>Go beyond the product story. <em>Inspect the reasoning.</em></h1>
    <p class="lede">This curated library distills the architecture, security, runtime, data, and readiness papers developed for ContextWeaver NextGen. Each brief begins with the decision it explains, then exposes the design principles and implementation questions behind it.</p>
    <div class="hero-actions"><a class="button primary" href="#briefs">Browse the briefs</a><a class="button" href="architecture.html">Return to the architecture</a></div>
  </div>
  <div class="library-compass" aria-label="Technical library categories">
    <a href="#foundation"><span>01</span><b>Foundation</b><small>Platform and delivery design</small></a>
    <a href="#trust"><span>02</span><b>Trust</b><small>Identity, credentials, sandboxing</small></a>
    <a href="#runtime-library"><span>03</span><b>Runtime</b><small>Lifecycle, resilience, observability</small></a>
    <a href="#data-readiness"><span>04</span><b>Data & readiness</b><small>RAG, storage, parity</small></a>
  </div>
</section>

<section class="container section compact">
  <div class="plain-language" data-reveal>
    <div><p class="section-kicker">How to use this page</p><h2>Read the decision first. Expand only where you need depth.</h2></div>
    <p>The briefs are not compliance claims or deployment certifications. They document architectural intent, active realization, and qualification questions that must be answered for a specific release and customer environment.</p>
  </div>
</section>

<section id="briefs" class="container section library-section">
  <div id="foundation" class="library-group">
    <div class="library-group-head"><div><p class="section-kicker">01 · Foundation</p><h2>What kind of platform is ContextWeaver?</h2></div><p>Start here for the product model, portable contracts, delivery system, and specification-first operating model.</p></div>
    <div class="library-grid">
      <details class="brief" open>
        <summary><span>Conceptual design</span><small>Reusable Enterprise Agentic AI Platform</small></summary>
        <div><p><strong>Decision:</strong> Treat MCPs, Agents, Workflows, Services, Solutions, policy, data, and evidence as governed platform assets rather than application-local code.</p><ul><li>Separates user-facing Solution experience from reusable Service execution and lower-level capabilities.</li><li>Uses typed contracts and immutable plans to prevent runtime authority expansion.</li><li>Lets individual and enterprise experiences share the same core semantics.</li></ul></div>
      </details>
      <details class="brief">
        <summary><span>Spec-driven AI platform</span><small>Governance and operations whitepaper</small></summary>
        <div><p><strong>Decision:</strong> Make specifications executable inputs to admission, generation, testing, deployment, evaluation, and retirement.</p><ul><li>Defines ownership, schemas, side effects, dependencies, SLOs, support, and lifecycle before deployment.</li><li>Turns governance into machine-verifiable gates instead of after-the-fact review.</li><li>Connects business intent to implementation and operational evidence.</li></ul></div>
      </details>
      <details class="brief">
        <summary><span>Cloud-neutral delivery</span><small>Infrastructure and deployment design</small></summary>
        <div><p><strong>Decision:</strong> Keep control-plane semantics provider-neutral while implementing cloud services through qualified adapters.</p><ul><li>Centers Kubernetes, OCI, Helm, GitOps, OpenTelemetry, and portable schemas.</li><li>Injects provider backends and secrets rather than embedding them into capability definitions.</li><li>Requires qualification per cloud, region, release, and deployment profile.</li></ul></div>
      </details>
    </div>
  </div>

  <div id="trust" class="library-group">
    <div class="library-group-head"><div><p class="section-kicker">02 · Trust</p><h2>How is authority kept outside the model?</h2></div><p>These briefs cover identity continuity, runtime authorization, credential non-possession, and constrained execution.</p></div>
    <div class="library-grid">
      <details class="brief">
        <summary><span>Credential non-possession</span><small>Delegated authority without secret exposure</small></summary>
        <div><p><strong>Decision:</strong> Agents request permitted operations; a trusted gateway obtains and uses credentials just in time.</p><ul><li>Provider tokens, cloud keys, and connector secrets never enter Agent context.</li><li>Policy evaluates the exact service, tool, arguments, purpose, data, and side effect.</li><li>Receipts preserve what was requested, authorized, executed, and returned.</li></ul></div>
      </details>
      <details class="brief">
        <summary><span>Continuous entitlement</span><small>Runtime authorization and revocation</small></summary>
        <div><p><strong>Decision:</strong> Admission-time permission is not enough; protected actions must be reauthorized at use and delivery time.</p><ul><li>Carries user, workload, tenant, role, purpose, delegation, plan, and node identity.</li><li>Rechecks current revocation, policy, environment, data scope, and risk.</li><li>Prevents a long-running Workflow from relying on stale authority.</li></ul></div>
      </details>
      <details class="brief">
        <summary><span>Agent sandbox security</span><small>Constrained reasoning intent</small></summary>
        <div><p><strong>Decision:</strong> Treat generated and third-party reasoning code as untrusted workload content.</p><ul><li>Use restricted runtime identity, deny-default networking, quotas, and bounded filesystems.</li><li>Expose capabilities through policy-controlled interfaces rather than ambient cluster access.</li><li>Test malformed I/O, prompt injection, duplicate delivery, timeout, and restart behavior.</li></ul></div>
      </details>
    </div>
  </div>

  <div id="runtime-library" class="library-group">
    <div class="library-group-head"><div><p class="section-kicker">03 · Runtime</p><h2>How does the system deploy, recover, and prove operation?</h2></div><p>Follow the capability from admission through discovery, durable execution, failure recovery, and operational evidence.</p></div>
    <div class="library-grid">
      <details class="brief">
        <summary><span>Dynamic Agent and MCP lifecycle</span><small>Admission, deployment, and discovery</small></summary>
        <div><p><strong>Decision:</strong> Deployment and discovery are separate lifecycle states.</p><ul><li>Validate specifications and supply chain before the operator creates runtime resources.</li><li>Attest the live descriptor and converge Registry state before making a capability selectable.</li><li>Support canary, pause, quarantine, drain, and retirement as governed transitions.</li></ul></div>
      </details>
      <details class="brief">
        <summary><span>Durable microservice resilience</span><small>Cross-pod work recovery</small></summary>
        <div><p><strong>Decision:</strong> Workflow progress belongs in durable state, not in the memory of a particular pod.</p><ul><li>Use commands, events, leases, checkpoints, inbox/outbox, and accepted artifact hashes.</li><li>Make retries safe with idempotency keys and provider receipts.</li><li>Represent compensation and non-compensable escalation explicitly.</li></ul></div>
      </details>
      <details class="brief">
        <summary><span>Observability standard</span><small>Solutions, Services, Workflows, Agents, and MCPs</small></summary>
        <div><p><strong>Decision:</strong> Observe the business and trust path, not only infrastructure health.</p><ul><li>Correlate intent, plan, node, model, source, policy, approval, tool call, receipt, and result.</li><li>Measure reliability, quality, safety, cost, latency, usage, and business outcome.</li><li>Preserve enough evidence to explain a run without exposing restricted content.</li></ul></div>
      </details>
    </div>
  </div>

  <div id="data-readiness" class="library-group">
    <div class="library-group-head"><div><p class="section-kicker">04 · Data and readiness</p><h2>How do retrieval and deployment become trustworthy?</h2></div><p>These briefs distinguish a useful demonstration from a version-safe, authorized, recoverable, and qualified production profile.</p></div>
    <div class="library-grid">
      <details class="brief">
        <summary><span>Governed, fresh, version-safe RAG</span><small>Ingestion and atomic generations</small></summary>
        <div><p><strong>Decision:</strong> Publish complete retrieval generations atomically instead of mutating a live index in place.</p><ul><li>Bind chunks to source versions, classifications, ownership, policy, and provenance.</li><li>Authorize retrieval before search and filter results before context construction.</li><li>Keep aliases movable while a run pins the exact accepted generation.</li></ul></div>
      </details>
      <details class="brief">
        <summary><span>RAG storage and search readiness</span><small>Infrastructure qualification</small></summary>
        <div><p><strong>Decision:</strong> Evaluate the full ingestion, storage, search, authorization, freshness, and recovery path.</p><ul><li>Test scale, rebuild, replay, deletion, retention, backup, restore, and regional behavior.</li><li>Validate lexical, vector, hybrid, reranking, citation, and access-filter quality.</li><li>Separate provider availability from application-level readiness.</li></ul></div>
      </details>
      <details class="brief">
        <summary><span>Parity and deployment readiness</span><small>Release and profile qualification</small></summary>
        <div><p><strong>Decision:</strong> Readiness is specific to a release and deployment profile, not a permanent platform label.</p><ul><li>Compare required contracts, adapters, controls, tests, SLOs, and recovery evidence.</li><li>Classify gaps as implemented foundation, active realization, or target architecture.</li><li>Avoid implying regulatory certification from architectural intent alone.</li></ul></div>
      </details>
    </div>
  </div>
</section>

<section id="builder" class="container section builder-section">
  <div class="founder-shell">
    <figure class="founder-photo">
      <img src="assets/media/ajay-punreddy-founder.webp" width="1024" height="1024" loading="lazy" alt="Ajay Punreddy outdoors in an alpine mountain landscape">
      <figcaption>
        <span>Beyond technology</span>
        <p>An avid sportsman and traveler who enjoys nature, memorable experiences, thoughtful design, and the finer things in life.</p>
      </figcaption>
    </figure>
    <div class="founder-copy">
      <p class="section-kicker">Meet the founder</p>
      <h2>Ajay Punreddy</h2>
      <p class="founder-role">Founder &amp; CEO, BrainzBytes · Systems architect · Inventor</p>
      <p>Ajay is a veteran systems architect and engineering leader with more than 28 years of experience building mission-critical infrastructure across networking, telecommunications, cloud platforms, Kubernetes, distributed systems, and enterprise AI. He founded BrainzBytes to address the security and orchestration challenges created when AI Agents begin using enterprise data and tools.</p>
      <p>His career spans firmware and Ethernet switching at Cabletron Systems; ATM and SONET at Bay Networks/Nortel and Synoptics; frame-relay and ATM switching at Cascade Communications; carrier-grade VoIP at Castle Networks; and unified communications architecture as a founding engineer at BlueNote Networks. At Aspect Software, he advanced to Technical Director and Software Architect, helping move enterprise contact-center platforms toward cloud-native Kubernetes, microservices, modern identity, and continuous delivery.</p>
      <p>His broader work includes video streaming at Verivue, mobile-core optimization at Affirmed Networks, and platform engineering at Microsoft. Those decades of systems work shape ContextWeaver's emphasis on explicit contracts, constrained authority, durable recovery, portable infrastructure, and evidence that can be inspected after every consequential run.</p>
      <div class="founder-stats" aria-label="Founder experience highlights">
        <div><strong>28+</strong><span>Years in systems engineering</span></div>
        <div><strong>5</strong><span>Patent and application entries</span></div>
        <div><strong>10+</strong><span>Infrastructure and platform domains</span></div>
      </div>
    </div>
  </div>

  <div class="founder-career" aria-label="Selected career organizations">
    <span>Cabletron Systems</span><span>Bay Networks / Nortel</span><span>Cascade / Lucent</span><span>Castle / Siemens</span><span>BlueNote / Aspect</span><span>Verivue</span><span>Affirmed Networks</span><span>Microsoft</span><span>BrainzBytes</span>
  </div>

  <div class="founder-lens">
    <div>
      <p class="section-kicker">The engineering lens</p>
      <h3>ContextWeaver reflects a career spent making complex systems dependable.</h3>
    </div>
    <div class="builder-principles">
      <div><span>01</span><b>Build for failure</b><small>Durable state, replay, idempotency, compensation.</small></div>
      <div><span>02</span><b>Keep authority explicit</b><small>Identity, policy, approval, delegated credentials.</small></div>
      <div><span>03</span><b>Make evidence a product output</b><small>Receipts, lineage, decisions, evaluations, telemetry.</small></div>
    </div>
  </div>

  <div class="founder-ip">
    <div class="library-group-head">
      <div><p class="section-kicker">Intellectual property</p><h2>Inventions across communications, operations, cloud platforms, and agentic AI.</h2></div>
      <p>Statuses below reflect the current BrainzBytes founder profile and distinguish granted work from applications still under examination or pending.</p>
    </div>
    <div class="patent-grid">
      <article class="patent-card granted"><span>Granted · US 9,883,037</span><h3>Staff Level Estimation for Multi-Skilled Agents</h3><p>Contact-center workforce optimization · Aspect Software · Granted January 2018.</p></article>
      <article class="patent-card granted"><span>Granted · US 9,374,393</span><h3>Dynamic Call-Progress Analysis &amp; Call Processing</h3><p>Real-time media-stream analysis for call routing · Aspect Software · Granted June 2016.</p></article>
      <article class="patent-card approved"><span>Approved · 413306-US-NP</span><h3>Deployment of Pod Cohorts</h3><p>Manifest-driven Kubernetes cohort lifecycle management · Microsoft · Filed June 2023.</p></article>
      <article class="patent-card examination"><span>In examination · US 18/626,203</span><h3>Continuation: Pod Cohort Deployment</h3><p>Continuation expanding the cohort-orchestration methods developed at Microsoft.</p></article>
      <article class="patent-card pending"><span>Pending · Application 99741331</span><h3>ContextWeaver: Enterprise MCP Orchestration</h3><p>Multi-user, identity-aware agentic AI with governed retrieval and MCP security boundaries · BrainzBytes.</p></article>
    </div>
  </div>
</section>

<section class="container section compact">
  <div class="chapter-next">
    <div><p class="section-kicker">Put the pieces together</p><h2>Return to the architecture with the deeper decisions in view.</h2><p>The atlas connects these security, runtime, data, and deployment principles into one visual system.</p></div>
    <a class="button primary" href="architecture.html">Reopen the architecture atlas →</a>
  </div>
</section>
"""

# Keep the detailed founder profile single-sourced while presenting it on the
# dedicated Company page rather than inside the Technical Library.
_founder_start = LIBRARY.index('<section id="builder"')
_library_transition = LIBRARY.index(
    '<section class="container section compact">',
    _founder_start,
)
FOUNDER_PROFILE = LIBRARY[_founder_start:_library_transition].replace(
    'id="builder"',
    'id="about"',
    1,
)
LIBRARY = LIBRARY[:_founder_start] + LIBRARY[_library_transition:]

COMPANY = """
<section class="container hero company-hero">
  <div>
    <p class="eyebrow">BrainzBytes company</p>
    <h1>Engineering ambitious systems with <em>discipline, imagination, and evidence.</em></h1>
    <p class="lede">BrainzBytes is the company behind ContextWeaver. This space begins with the founder story and is designed to grow into Careers, company news, partnerships, and other corporate information without interrupting the product journey.</p>
    <div class="hero-actions"><a class="button primary" href="#about">Meet the founder</a><a class="button" href="overview.html">Explore ContextWeaver</a></div>
  </div>
  <nav id="company-paths" class="company-tabs" aria-label="Company sections">
    <a class="active" href="#about"><span>01</span><b>About</b><small>Company and founder</small></a>
    <span><span>02</span><b>Careers</b><small>Planned</small></span>
    <span><span>03</span><b>News</b><small>Planned</small></span>
    <span><span>04</span><b>Partners</b><small>Planned</small></span>
  </nav>
</section>
""" + FOUNDER_PROFILE + """
<section class="container section compact">
  <div class="chapter-next">
    <div><p class="section-kicker">Explore the work</p><h2>See how the engineering principles become a governed AI platform.</h2><p>Continue into the ContextWeaver overview or explore the complete Learning experience.</p></div>
    <div class="hero-actions"><a class="button primary" href="overview.html">Open the overview →</a><a class="button" href="learning.html">Learning</a></div>
  </div>
</section>
"""

LEARNING = """
<section class="learning-atlas" data-learning-atlas>
  <div class="container learning-hero">
    <div class="learning-hero-copy">
      <p class="eyebrow">Visual learning center</p>
      <h1>Pick a concept. <em>Learn it visually.</em></h1>
      <p class="learning-lede">Choose any topic to open one complete infographic: what it is, why it matters, the core concepts, the flow, and the key takeaway.</p>
      <div class="learning-actions">
        <a class="button primary" href="#visual-learning-cards">Choose a concept <span aria-hidden="true">↓</span></a>
        <a class="button" href="#learning-curriculum-title">Browse the full curriculum</a>
      </div>
      <div class="learning-proof" aria-label="Learning Atlas scope">
        <span><b>9</b> visual concepts</span>
        <span><b>8</b> curriculum areas</span>
        <span><b>48</b> platform services</span>
        <span><b>0</b> prerequisites</span>
      </div>
    </div>
    <div class="learning-orbit learning-overview-infographic" aria-label="How governed AI becomes a trusted outcome">
      <header>
        <span>Start anywhere</span>
        <h2>Choose what you want to understand.</h2>
        <p>Every item opens its complete visual lesson below.</p>
      </header>
      <div class="learning-infographic-flow">
        <button type="button" data-learning-step="ai" aria-controls="learning-lesson-board"><i>01</i><b>AI</b><small>Models and generation</small></button>
        <button type="button" data-learning-step="rag" aria-controls="learning-lesson-board"><i>02</i><b>RAG</b><small>Grounded knowledge</small></button>
        <button type="button" data-learning-step="agents" aria-controls="learning-lesson-board"><i>03</i><b>Agent</b><small>Bounded reasoning</small></button>
        <button type="button" data-learning-step="mcp" aria-controls="learning-lesson-board"><i>04</i><b>MCP</b><small>Governed capabilities</small></button>
        <button type="button" data-learning-step="workflows" aria-controls="learning-lesson-board"><i>05</i><b>Workflow</b><small>Durable coordination</small></button>
        <button type="button" data-learning-step="services" aria-controls="learning-lesson-board"><i>06</i><b>Service</b><small>Reusable contracts</small></button>
        <button type="button" data-learning-step="solutions" aria-controls="learning-lesson-board"><i>07</i><b>Solution</b><small>User-facing outcomes</small></button>
        <button type="button" data-learning-step="contextweaver" aria-controls="learning-lesson-board"><i>08</i><b>Platform</b><small>Cerebro, Weave, Loom</small></button>
        <button type="button" data-learning-step="evidence" aria-controls="learning-lesson-board"><i>09</i><b>Evidence</b><small>Trust and proof</small></button>
      </div>
      <footer class="learning-map-instruction"><strong>Select a topic</strong><span>Its visual explanation opens immediately below.</span></footer>
    </div>
  </div>

  <section id="visual-learning-cards" class="container learning-route" aria-labelledby="learning-route-title">
    <div class="learning-route-summary">
      <div>
        <p class="section-kicker">Choose one concept</p>
        <h2 id="learning-route-title">What do you want to learn?</h2>
        <p>Select a card. The complete visual explanation appears directly beneath the cards.</p>
      </div>
      <div class="learning-route-meta"><span>Click any card</span><span>9 visual lessons</span><span>Previous / Next included</span></div>
    </div>
    <div class="learning-lesson-grid" role="group" aria-label="Choose a visual concept card">
      <button class="learning-lesson-card active" type="button" data-learning-step="ai" aria-pressed="true" aria-controls="learning-lesson-board"><span class="learning-card-number">01</span><i>AI</i><b>AI and LLMs</b><small>What models can and cannot do</small><span class="learning-mini-diagram"><em>Prompt</em><u>→</u><em>Model</em><u>→</u><em>Validate</em></span></button>
      <button class="learning-lesson-card" type="button" data-learning-step="rag" aria-pressed="false" aria-controls="learning-lesson-board"><span class="learning-card-number">02</span><i>RAG</i><b>Grounded knowledge</b><small>Retrieve authorized context with citations</small><span class="learning-mini-diagram"><em>Sources</em><u>→</u><em>Retrieve</em><u>→</u><em>Cite</em></span></button>
      <button class="learning-lesson-card" type="button" data-learning-step="agents" aria-pressed="false" aria-controls="learning-lesson-board"><span class="learning-card-number">03</span><i>AG</i><b>AI Agents</b><small>Bounded reasoning with typed contracts</small><span class="learning-mini-diagram"><em>Observe</em><u>→</u><em>Act</em><u>→</u><em>Stop</em></span></button>
      <button class="learning-lesson-card" type="button" data-learning-step="mcp" aria-pressed="false" aria-controls="learning-lesson-board"><span class="learning-card-number">04</span><i>MCP</i><b>Model Context Protocol</b><small>Governed access to external capabilities</small><span class="learning-mini-diagram"><em>Discover</em><u>→</u><em>Allow</em><u>→</u><em>Invoke</em></span></button>
      <button class="learning-lesson-card" type="button" data-learning-step="workflows" aria-pressed="false" aria-controls="learning-lesson-board"><span class="learning-card-number">05</span><i>WF</i><b>Workflows</b><small>Durable coordination, retries, and approval</small><span class="learning-mini-diagram"><em>Plan</em><u>→</u><em>Save</em><u>→</u><em>Finish</em></span></button>
      <button class="learning-lesson-card" type="button" data-learning-step="services" aria-pressed="false" aria-controls="learning-lesson-board"><span class="learning-card-number">06</span><i>SV</i><b>Services</b><small>Stable reusable business contracts</small><span class="learning-mini-diagram"><em>Request</em><u>→</u><em>Run</em><u>→</u><em>Return</em></span></button>
      <button class="learning-lesson-card" type="button" data-learning-step="solutions" aria-pressed="false" aria-controls="learning-lesson-board"><span class="learning-card-number">07</span><i>SO</i><b>Solutions</b><small>Complete user-facing compositions</small><span class="learning-mini-diagram"><em>Intent</em><u>→</u><em>Services</em><u>→</u><em>Outcome</em></span></button>
      <button class="learning-lesson-card" type="button" data-learning-step="contextweaver" aria-pressed="false" aria-controls="learning-lesson-board"><span class="learning-card-number">08</span><i>CW</i><b>ContextWeaver</b><small>Cerebro, Weave, and Loom together</small><span class="learning-mini-diagram"><em>Cerebro</em><u>→</u><em>Weave</em><u>→</u><em>Loom</em></span></button>
      <button class="learning-lesson-card" type="button" data-learning-step="evidence" aria-pressed="false" aria-controls="learning-lesson-board"><span class="learning-card-number">09</span><i>EV</i><b>Verified result</b><small>Evidence, receipts, citations, and history</small><span class="learning-mini-diagram"><em>Capture</em><u>→</u><em>Score</em><u>→</u><em>Preserve</em></span></button>
    </div>
    <article id="learning-lesson-board" class="learning-lesson-board" data-learning-route-detail aria-live="polite" aria-atomic="true">
      <div class="learning-lesson-toolbar">
        <span data-learning-progress>Lesson 1 of 9</span>
        <div>
          <button type="button" data-learning-previous>← Previous</button>
          <button type="button" data-learning-next>Next lesson →</button>
        </div>
      </div>
      <header class="learning-board-head">
        <div><span data-learning-step-label>Lesson 01 · Foundation</span><h3 data-learning-step-title>What are AI and large language models?</h3><p data-learning-step-copy>A language model predicts useful language from learned patterns. It can explain, summarize, and draft—but it does not know enterprise truth or hold authority to act.</p></div>
        <div class="learning-board-mark" data-learning-step-mark aria-hidden="true">AI</div>
      </header>
      <div class="learning-board-pair">
        <section><span>What it is</span><p data-learning-step-definition>A probabilistic language engine that turns instructions and context into generated text, code, classifications, or structured output.</p></section>
        <section><span>Why it matters</span><ul data-learning-step-why><li>Makes complex knowledge easier to use</li><li>Accelerates analysis and drafting</li><li>Still requires grounding, validation, and control</li></ul></section>
      </div>
      <section class="learning-board-section">
        <span>Four core concepts</span>
        <div class="learning-concept-grid" data-learning-step-concepts></div>
      </section>
      <section class="learning-board-section">
        <span>How it works</span>
        <div class="learning-flow-cards" data-learning-step-flow></div>
      </section>
      <footer class="learning-board-takeaway"><div><span>Key takeaway</span><strong data-learning-step-takeaway>A model produces possibilities. A governed platform decides what is trusted, permitted, and recorded.</strong></div><a class="button compact" data-learning-step-link href="overview.html">Explore the platform view <span aria-hidden="true">→</span></a></footer>
    </article>
    <div class="learning-poster-gallery-head" hidden>
      <div><p class="section-kicker">Keep and revisit</p><h2>Every lesson as a complete visual learning card.</h2></div>
      <p>Scan the cards in order or jump directly to the concept you need. Each card uses the same learning pattern: definition, purpose, concepts, flow, and takeaway.</p>
    </div>
    <div class="learning-poster-gallery" data-learning-poster-gallery aria-label="Complete visual learning card collection" hidden></div>
  </section>

  <section id="agent-learning" class="container learning-deep-dive" aria-labelledby="agent-deep-dive-title" hidden>
    <div class="learning-deep-head">
      <div><p class="section-kicker">See progressive depth in action</p><h2 id="agent-deep-dive-title">What is an AI Agent?</h2></div>
      <span class="learning-status">Foundation concept</span>
    </div>
    <div class="learning-definition">
      <div class="learning-definition-mark" aria-hidden="true">A</div>
      <div><span>60-second explanation</span><p>An Agent is a specialist role that uses a model to decide the next safe step, but only within typed instructions, approved knowledge, permitted tools, budgets, and stop conditions.</p></div>
      <button type="button" data-learning-jargon-term="typed contract">What is a typed contract?</button>
    </div>
    <div class="learning-lens-layout">
      <div class="learning-lens-tabs" role="tablist" aria-label="Agent explanation lenses">
        <button class="active" type="button" role="tab" data-learning-lens="business" aria-selected="true">Business</button>
        <button type="button" role="tab" data-learning-lens="sales" aria-selected="false">Sales</button>
        <button type="button" role="tab" data-learning-lens="engineering" aria-selected="false">Engineering</button>
        <button type="button" role="tab" data-learning-lens="architecture" aria-selected="false">Architecture</button>
        <button type="button" role="tab" data-learning-lens="operations" aria-selected="false">Operations</button>
      </div>
      <div class="learning-lens-panel" data-learning-lens-panel>
        <div>
          <span class="learning-panel-kicker">Why it matters</span>
          <h3>Turn repeatable expertise into a governed capability.</h3>
          <p>An Agent can apply a specialist role consistently while the platform preserves ownership, limits, approvals, and evidence. It augments a process; it does not become an unaccountable digital employee.</p>
        </div>
        <div class="learning-agent-loop" aria-label="Bounded Agent loop">
          <span>Observe</span><i>→</i><span>Plan</span><i>→</i><span>Act</span><i>→</i><span>Inspect</span><i>→</i><b>Stop</b>
        </div>
        <div class="learning-panel-grid">
          <article><span>Good fit</span><b>Research, classify, compare, recommend, draft</b></article>
          <article><span>Needs control</span><b>Side effects, sensitive data, high-risk decisions</b></article>
          <article><span>ContextWeaver adds</span><b>Identity, policy, MCP boundaries, approval, evidence</b></article>
        </div>
      </div>
    </div>
  </section>

  <section class="container learning-curriculum" aria-labelledby="learning-curriculum-title">
    <div class="learning-curriculum-head">
      <div><p class="section-kicker">Complete platform curriculum</p><h2 id="learning-curriculum-title">Learn every concept the platform uses.</h2></div>
      <p>The curriculum starts with AI foundations, then follows knowledge, reasoning, orchestration, security, infrastructure, operations, and evidence. Every topic maps to a real ContextWeaver responsibility.</p>
    </div>
    <div class="learning-curriculum-grid">
      <article class="learning-curriculum-card"><span>01 · Intelligence</span><h3>AI and model foundations</h3><p>Understand the probabilistic systems behind generation before adding tools or autonomy.</p><ul><li>AI, machine learning, and deep learning</li><li>Neural networks and transformers</li><li>Tokens, context windows, and attention</li><li>Prompting and system instructions</li><li>Structured output and function calling</li><li>Multimodal models and inference</li><li>Hallucination, safety, and guardrails</li><li>Model evaluation and selection</li></ul></article>
      <article class="learning-curriculum-card"><span>02 · Knowledge</span><h3>RAG, search, and memory</h3><p>Learn how governed knowledge becomes searchable context without moving authority into the model.</p><ul><li>Source catalogs and ingestion</li><li>Parsing, normalization, and chunking</li><li>Embeddings and vector search</li><li>Keyword, semantic, and hybrid retrieval</li><li>Re-ranking and context packing</li><li>Citations and provenance</li><li>Session, working, and durable memory</li><li>Freshness, access, and deletion</li></ul></article>
      <article class="learning-curriculum-card"><span>03 · Reasoning</span><h3>Agents, tools, and MCP</h3><p>Move from conversation to bounded specialist reasoning with explicit capability boundaries.</p><ul><li>Agent roles and typed contracts</li><li>Planning, reflection, and stop conditions</li><li>Tools, resources, and prompts</li><li>Model Context Protocol servers</li><li>Plugins and capability packages</li><li>Multi-Agent delegation and routing</li><li>Budgets, timeouts, and approvals</li><li>Human-in-the-loop escalation</li></ul></article>
      <article class="learning-curriculum-card"><span>04 · Product model</span><h3>Workflows, Services, and Solutions</h3><p>See how reusable assets become reliable, user-facing outcomes.</p><ul><li>Immutable plans and Workflow compilation</li><li>Durable coordination and checkpoints</li><li>Retries, idempotency, and compensation</li><li>Saga and approval patterns</li><li>Service contracts and entitlements</li><li>Solution composition and experience</li><li>Registries, versions, and publication</li><li>Lifecycle, rollout, and retirement</li></ul></article>
      <article class="learning-curriculum-card"><span>05 · Trust</span><h3>Identity, security, and governance</h3><p>Understand how every request carries identity, authority, policy, and an auditable decision path.</p><ul><li>OIDC, OAuth 2.0, and Keycloak</li><li>Identity context and delegated authority</li><li>Token brokering and credential non-possession</li><li>Authentication and API gateways</li><li>Entitlement and policy decisions</li><li>Secrets and least privilege</li><li>Audit records and signed receipts</li><li>Evaluation, risk, and compliance</li></ul></article>
      <article class="learning-curriculum-card"><span>06 · Platform</span><h3>Data, messaging, and infrastructure</h3><p>Learn the cloud-neutral foundation that keeps state durable and capabilities portable.</p><ul><li>PostgreSQL and pgvector</li><li>RabbitMQ commands and events</li><li>Object and artifact storage</li><li>Valkey caching and coordination</li><li>Kubernetes namespaces and workloads</li><li>Cilium networking and policy</li><li>Helm, CRDs, and operators</li><li>Ingress, gateways, and service discovery</li></ul></article>
      <article class="learning-curriculum-card"><span>07 · Operations</span><h3>Observability and reliability</h3><p>Follow health, performance, failures, and recovery from one trace to the whole cluster.</p><ul><li>OpenTelemetry context propagation</li><li>Prometheus metrics and alerts</li><li>Loki logs and Tempo traces</li><li>Grafana dashboards and SLOs</li><li>Health, readiness, and dependency checks</li><li>Backups, restore, and disaster recovery</li><li>Shutdown, startup, and reconciliation</li><li>Capacity, scaling, and resilience</li></ul></article>
      <article class="learning-curriculum-card"><span>08 · Proof</span><h3>Evaluation, evidence, and improvement</h3><p>Turn each run into a result that can be reviewed, compared, reproduced, and improved.</p><ul><li>Offline and online evaluation</li><li>Golden datasets and scoring rubrics</li><li>Quality, safety, and policy thresholds</li><li>Prompt and model comparison</li><li>Citations, tool receipts, and approvals</li><li>Run history and report stores</li><li>Feedback and regression detection</li><li>Release gates and continuous learning</li></ul></article>
    </div>
  </section>

  <section class="container learning-service-catalog" aria-labelledby="learning-services-title">
    <div class="learning-curriculum-head">
      <div><p class="section-kicker">Platform service atlas</p><h2 id="learning-services-title">Know what every ContextWeaver service owns.</h2></div>
      <p>These cards map conceptual learning to the concrete services used by the platform. Names remain visible so architecture, code, operations, and learning use the same language.</p>
    </div>
    <div class="learning-service-grid">
      <article><span>Entry and identity</span><h3>Who is asking, and what may they do?</h3><p>API Gateway · Authentication Gateway · Identity Context · Entitlement Service · Token Broker · Policy Decision Service · Session Service</p></article>
      <article><span>Knowledge and intelligence</span><h3>Which context and model should be used?</h3><p>Source Catalog · RAG Ingestion · RAG Retrieval · Context Memory · Context Citation · Model Gateway · Intent Router</p></article>
      <article><span>Design and composition</span><h3>How does intent become an immutable plan?</h3><p>Solution Composer · Workflow Compiler · Registry Service · Configuration Service · Developer Portal · Admin Web</p></article>
      <article><span>Runtime and coordination</span><h3>How does work continue safely?</h3><p>Run Coordinator · Saga HITL · Finalizer · Notification Service · Audit Service · Report Store</p></article>
      <article><span>Capabilities and workspaces</span><h3>Where do tools and isolated work execute?</h3><p>Capability Operator · Capability Protocol Gateway · Artifact Gateway · Workspace API · Workspace Controller · Workspace Operations · Workspace Session Gateway</p></article>
      <article><span>Evidence and operations</span><h3>How is the platform observed and improved?</h3><p>Prometheus · Loki · Tempo · Grafana · Alloy · Kubernetes Events · evaluation cards · policy receipts · run reports</p></article>
    </div>
  </section>

  <section id="component-atlas" class="container component-atlas" aria-labelledby="component-atlas-title">
    <div class="component-atlas-head">
      <div><p class="section-kicker">Every component. No black boxes.</p><h2 id="component-atlas-title">Explore the platform by responsibility.</h2></div>
      <p>Each component page connects purpose, ownership, identity, data, protocols, dependencies, health, failure behavior, recovery, and implementation status.</p>
    </div>
    <div class="component-filter" role="group" aria-label="Filter platform components">
      <button class="active" type="button" data-component-filter="all" aria-pressed="true">All domains</button>
      <button type="button" data-component-filter="identity" aria-pressed="false">Identity</button>
      <button type="button" data-component-filter="data" aria-pressed="false">Data and messaging</button>
      <button type="button" data-component-filter="runtime" aria-pressed="false">Runtime</button>
      <button type="button" data-component-filter="cluster" aria-pressed="false">Cluster</button>
      <button type="button" data-component-filter="observe" aria-pressed="false">Observability</button>
    </div>
    <div class="component-grid">
      <article class="component-card" data-component-domain="identity"><div class="component-icon">ID</div><div class="component-title"><span>Identity provider</span><h3>Keycloak</h3></div><p>Authenticates users, publishes OIDC metadata, owns realms and clients, and supports delegated token exchange.</p><div class="component-tags"><span>Active · Kubernetes</span><span>OIDC / OAuth</span></div><a href="#keycloak-path">Open deep dive <span>→</span></a></article>
      <article class="component-card" data-component-domain="data"><div class="component-icon">SQL</div><div class="component-title"><span>Durable state</span><h3>PostgreSQL + pgvector</h3></div><p>Stores platform state, configuration revisions, run checkpoints, RAG generations, chunks, embeddings, inboxes, and outboxes.</p><div class="component-tags"><span>Active · Local and K8s</span><span>SQL / vector</span></div><a href="#data-path">Open deep dive <span>→</span></a></article>
      <article class="component-card" data-component-domain="data runtime"><div class="component-icon">MQ</div><div class="component-title"><span>Durable messaging</span><h3>RabbitMQ</h3></div><p>Moves signed commands, results, and events between isolated workers without coupling work to an HTTP request lifetime.</p><div class="component-tags"><span>Active foundation</span><span>AMQP</span></div><a href="#runtime-path">Open deep dive <span>→</span></a></article>
      <article class="component-card" data-component-domain="runtime"><div class="component-icon">RC</div><div class="component-title"><span>Orchestration</span><h3>Run Coordinator</h3></div><p>Commits durable run state, dispatches typed work, tracks checkpoints, applies retries, and drives finalization.</p><div class="component-tags"><span>Active realization</span><span>Workflow runtime</span></div><a href="#runtime-path">Open deep dive <span>→</span></a></article>
      <article class="component-card" data-component-domain="cluster"><div class="component-icon">K8S</div><div class="component-title"><span>Portable foundation</span><h3>Kubernetes + Cilium</h3></div><p>Provides workload lifecycle, namespace trust boundaries, service discovery, storage, policy enforcement, and recovery.</p><div class="component-tags"><span>Active · kind and AKS</span><span>Cloud-neutral</span></div><a href="#cluster-path">Open deep dive <span>→</span></a></article>
      <article class="component-card" data-component-domain="observe"><div class="component-icon">OBS</div><div class="component-title"><span>Evidence and health</span><h3>Prometheus · Loki · Tempo</h3></div><p>Collects metrics, logs, and traces through Alloy and presents operational evidence through Grafana.</p><div class="component-tags"><span>Active foundation</span><span>OpenTelemetry</span></div><a href="#observe-path">Open deep dive <span>→</span></a></article>
      <article class="component-card" data-component-domain="data"><div class="component-icon">OBJ</div><div class="component-title"><span>Artifacts and content</span><h3>Object storage</h3></div><p>Preserves private artifacts, source snapshots, extracted content, context packs, reports, and immutable evidence.</p><div class="component-tags"><span>MinIO / S3 contract</span><span>Encrypted storage</span></div><a href="#data-path">Open deep dive <span>→</span></a></article>
      <article class="component-card" data-component-domain="identity runtime"><div class="component-icon">GW</div><div class="component-title"><span>Capability boundary</span><h3>Authentication and token gateways</h3></div><p>Maintain principal context, broker scoped credentials, and keep provider secrets out of Agents and user-facing clients.</p><div class="component-tags"><span>Fail closed</span><span>Delegated authority</span></div><a href="#keycloak-path">Open deep dive <span>→</span></a></article>
    </div>
  </section>

  <section class="container learning-system-map" aria-labelledby="system-map-title">
    <div class="learning-system-copy">
      <p class="section-kicker">Follow one request end to end</p>
      <h2 id="system-map-title">From signed-in user to verified result.</h2>
      <p>Select any stage to learn who owns it, what data crosses the boundary, which identity is used, how it fails, and what evidence remains.</p>
      <div class="learning-map-legend"><span><i class="current"></i>Active foundation</span><span><i class="realizing"></i>Active realization</span><span><i class="target"></i>Target</span></div>
    </div>
    <div class="learning-flow" aria-label="Governed request flow">
      <div><span>01</span><b>User portal</b><small>Intent and identity</small></div><i>→</i>
      <div><span>02</span><b>Auth + policy</b><small>Scope and authority</small></div><i>→</i>
      <div><span>03</span><b>Compiler</b><small>Immutable plan</small></div><i>→</i>
      <div><span>04</span><b>Coordinator</b><small>Durable execution</small></div><i>→</i>
      <div><span>05</span><b>Agent + MCP</b><small>Bounded work</small></div><i>→</i>
      <div><span>06</span><b>Evidence</b><small>Verified result</small></div>
    </div>
  </section>

  <section class="container learning-guide" aria-labelledby="learning-guide-title">
    <div>
      <p class="section-kicker">Generate my guide</p>
      <h2 id="learning-guide-title">Your path, assembled from canonical material.</h2>
      <p>The guide keeps implementation-status labels, source links, diagrams, and the complete glossary. It never invents architecture or unsupported product claims.</p>
    </div>
    <div class="learning-guide-preview">
      <span>Guide preview</span>
      <strong data-learning-guide-title>ContextWeaver essentials for a new learner</strong>
      <ul data-learning-guide-list><li>AI, LLM, and RAG in plain language</li><li>Agent, MCP, Workflow, Service, and Solution</li><li>One governed journey with evidence</li></ul>
      <button class="button primary" type="button" data-learning-generate>Download my guide <span aria-hidden="true">↓</span></button>
    </div>
  </section>
</section>
"""


def main() -> None:
    diagrams = {
        "service_factory": diagram(
            "service-factory",
            "Universal Solution and Capability Factory",
            "The same path creates reusable MCPs, Agents, Workflows, and Services, then composes them into complete governed Solutions.",
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
            "Solution Action to Governed Service Run",
            "The player shows how a user-facing Solution action resolves a reusable Service, identity and policy paths, parallel Agent work, MCP side effects, human approval, durable state, and final evidence.",
        ),
        "generic_agent_runtime": diagram(
            "generic-agent-runtime",
            "Generic Agent Runtime",
            "Risk, Readiness, and Synthesis use one platform image with separate immutable profiles, queues, identities, scaling, and rollback.",
        ),
        "scale_path": diagram(
            "scale-path",
            "Individual to Sovereign Enterprise",
            "Stable capability contracts remain portable while governance, tenancy, isolation, deployment, and assurance become progressively stronger.",
        ),
        "current_facts": fact_cards(*FACTS),
        "studio_facts": fact_cards(
            "unified-studios",
            "solution-service-model",
            "connector-control-plane",
            "hello-world-qualification",
        ),
        "runtime_facts": fact_cards(
            "multi-agent-composition",
            "agent-tool-delegation",
            "profile-bound-agents",
            "rag-ingestion-safety",
            "retrieval-evidence",
            "durable-service-runs",
        ),
        "governance_facts": fact_cards(
            "policy-entitlements",
            "single-entry-experiences",
            "external-delegated-clients",
            "agent-tool-delegation",
        ),
        "solution_facts": fact_cards(
            "solution-service-model",
            "single-entry-experiences",
            "external-delegated-clients",
            "durable-service-runs",
        ),
        "architecture_facts": fact_cards(
            "reusable-cicd",
            "identity-and-workspaces",
            "external-delegated-clients",
        ),
        "intent_to_evidence": spatial_visual(
            "intent-to-evidence.png",
            "Intent → outcome → proof",
            "The complete governed product journey",
            "Identity, policy, reusable execution, approval, side effects, evidence, and Azure, AWS, or Google Cloud deployment targets remain visible from the first request to the final outcome.",
            alt="Isometric ContextWeaver intent-to-evidence architecture showing the governed journey from user intent through Solutions, Services, Workflows, Agents and MCP capabilities to an evidence-backed outcome on Azure, AWS, or Google Cloud.",
        ),
        "platform_city": spatial_visual(
            "governed-platform-city.png",
            "Governed platform city",
            "Cerebro at the center of a reusable capability ecosystem",
            "Product, runtime, trust, data, operations, and integration districts stay independently governed while working as one platform.",
            alt="Isometric ContextWeaver platform city with Cerebro at the center and governed districts for Studio, runtime, data, tools, operations, and evidence.",
        ),
        "layered_architecture": spatial_visual(
            "layered-governed-architecture.png",
            "Layered governed architecture",
            "Experience, control, runtime, and infrastructure stay distinct",
            "Requests move down through explicit trust boundaries; evidence and operational proof return through the same governed system.",
            alt="Layered isometric ContextWeaver architecture separating experience, Cerebro governance, Weave runtime, and Loom infrastructure planes.",
        ),
        "governed_call_flow": spatial_visual(
            "governed-call-flow.png",
            "Governed call flow",
            "The request route and evidence route are separate",
            "Identity and policy constrain the call above the primary execution path while receipts, citations, and outcome proof return below it.",
            alt="Isometric governed service call flow showing numbered request stages, identity and policy controls, Agent and MCP execution, and a separate evidence-return route.",
        ),
        "governed_sequence_ladder": spatial_visual(
            "governed-sequence-ladder.png",
            "Governed sequence ladder",
            "Exact participant timing without losing architectural depth",
            "Fixed lifelines, activations, approvals, waits, parallel work, and returns make runtime interaction reviewable message by message.",
            alt="Three-dimensional sequence ladder with fixed ContextWeaver participants, vertical lifelines, activations, message bridges, waits, approvals, parallel work, and returns.",
        ),
        "durable_saga_flow": spatial_visual(
            "durable-saga-flow.png",
            "Durable Saga flow",
            "Persistent state makes retry and recovery explicit",
            "Parallel work, joins, bounded retries, approval waits, compensation, queues, receipts, and run history are visible as one durable system.",
            alt="Isometric durable Saga workflow showing split and join paths, retry, approval, compensation, persistent state, queues, receipts, and run history.",
        ),
    }

    pages = {
        "index.html": page(
            "landing",
            "ContextWeaver — The governed AI solution operating platform",
            "Explore how ContextWeaver composes user-facing Solutions from reusable Services, Workflows, Agents, MCP capabilities, knowledge, policy, portable infrastructure, and evidence.",
            LANDING,
        ),
        "overview.html": page(
            "overview",
            "ContextWeaver — Turn any approved idea into a governed Solution",
            "ContextWeaver creates user-facing Solutions from reusable Services, Workflows, Agents, MCP capabilities, knowledge, models, policy, and portable infrastructure.",
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
            "ContextWeaver Studio — MCPs, Agents, Workflows, Services, and Solutions",
            "Create, validate, simulate, publish, deploy, modify, and govern MCPs, Agents, Workflows, reusable Services, and complete Solutions from a GUI, VS Code, CLI, or Jupyter.",
            STUDIO.format(**diagrams),
        ),
        "runtime.html": page(
            "runtime",
            "ContextWeaver Runtime — Solution actions and governed Service Runs",
            "See how a user-facing Solution action resolves a reusable Service, authorized immutable plan, durable Agent and MCP execution, and evidence-backed result.",
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
            "ContextWeaver Solutions — Consumer experiences built from governed Services",
            "Understand Solutions, Services, Workflows, Agents, and MCPs; follow the My Solutions consumer journey and delegated external-assistant access.",
            SOLUTIONS.format(**diagrams),
        ),
        "architecture.html": page(
            "architecture",
            "ContextWeaver Interactive Architecture Explorer",
            "Explore clickable animated ContextWeaver architecture diagrams and download editable Draw.io, static SVG, and GIF assets.",
            ARCHITECTURE.format(**diagrams),
        ),
        "learning.html": standalone_page("learning.html"),
        "library.html": standalone_page("library.html"),
        "company.html": page(
            "company",
            "BrainzBytes Company — About and Founder",
            "Meet BrainzBytes founder Ajay Punreddy and explore the experience, engineering principles, and intellectual property behind ContextWeaver.",
            COMPANY,
        ),
    }

    for filename, content in pages.items():
        (ROOT / filename).write_text(content, encoding="utf-8", newline="\n")

    sitemap = "\n".join(
        f"  <url><loc>{PUBLIC_SITE_URL}/{filename}</loc></url>"
        for filename in pages
        if filename != "library.html"
    )
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap}\n</urlset>\n',
        encoding="utf-8",
        newline="\n",
    )
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {PUBLIC_SITE_URL}/sitemap.xml\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Generated {len(pages)} site pages.")


if __name__ == "__main__":
    main()
