(() => {
  const root = document.documentElement;
  const storedTheme = localStorage.getItem("cw-theme");
  root.dataset.theme = storedTheme === "deep" ? "deep" : "dark";

  const themeButton = document.querySelector("[data-theme-toggle]");
  const updateThemeButton = () => {
    if (!themeButton) return;
    const isDeep = root.dataset.theme === "deep";
    themeButton.textContent = isDeep ? "◐" : "◑";
    themeButton.setAttribute("aria-label", isDeep ? "Use standard dark theme" : "Use high-contrast dark theme");
  };
  themeButton?.addEventListener("click", () => {
    root.dataset.theme = root.dataset.theme === "deep" ? "dark" : "deep";
    localStorage.setItem("cw-theme", root.dataset.theme);
    updateThemeButton();
  });
  updateThemeButton();

  const menuButton = document.querySelector("[data-menu-toggle]");
  const nav = document.querySelector("[data-primary-nav]");
  menuButton?.addEventListener("click", () => {
    const open = nav?.classList.toggle("open") ?? false;
    menuButton.setAttribute("aria-expanded", String(open));
  });
  nav?.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => {
    nav.classList.remove("open");
    menuButton?.setAttribute("aria-expanded", "false");
  }));

  const scenarioTabs = [...document.querySelectorAll("[data-scenario]")];
  const selectScenario = (tab) => {
    const panelId = tab.dataset.scenario;
    scenarioTabs.forEach((item) => {
      const selected = item === tab;
      item.classList.toggle("active", selected);
      item.setAttribute("aria-selected", String(selected));
      item.tabIndex = selected ? 0 : -1;
    });
    document.querySelectorAll(".scenario-panel").forEach((panel) => {
      const selected = panel.id === panelId;
      panel.classList.toggle("active", selected);
      panel.hidden = !selected;
    });
  };
  scenarioTabs.forEach((tab, index) => {
    tab.addEventListener("click", () => selectScenario(tab));
    tab.addEventListener("keydown", (event) => {
      if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
      event.preventDefault();
      let next = index;
      if (event.key === "ArrowLeft") next = (index - 1 + scenarioTabs.length) % scenarioTabs.length;
      if (event.key === "ArrowRight") next = (index + 1) % scenarioTabs.length;
      if (event.key === "Home") next = 0;
      if (event.key === "End") next = scenarioTabs.length - 1;
      scenarioTabs[next].focus();
      selectScenario(scenarioTabs[next]);
    });
  });

  const page = document.body.dataset.page;
  document.querySelectorAll("[data-nav-page]").forEach((link) => {
    if (link.dataset.navPage === page) link.setAttribute("aria-current", "page");
  });
  if (page === "architecture" && !location.hash) {
    history.scrollRestoration = "manual";
    const showFactoryFirst = () => window.scrollTo(0, 0);
    showFactoryFirst();
    requestAnimationFrame(showFactoryFirst);
    window.addEventListener("pageshow", showFactoryFirst, { once: true });
  }

  const intro = document.querySelector("[data-site-intro]");
  const introFrame = intro?.querySelector("[data-intro-frame]");
  const introSkip = intro?.querySelector("[data-intro-skip]");
  const introEnter = intro?.querySelector("[data-intro-enter]");
  const introReplayButtons = [...document.querySelectorAll("[data-intro-replay]")];
  const introStorageKey = "contextweaver-company-intro-seen";
  let introReturnFocus = null;
  let introAudioUnlocked = false;

  const readIntroSeen = () => {
    try {
      return sessionStorage.getItem(introStorageKey) === "1";
    } catch {
      return false;
    }
  };

  const rememberIntro = () => {
    try {
      sessionStorage.setItem(introStorageKey, "1");
    } catch {
      // The intro remains usable when browser storage is unavailable.
    }
  };

  const removeForcedIntroQuery = () => {
    const url = new URL(location.href);
    if (!url.searchParams.has("intro")) return;
    url.searchParams.delete("intro");
    history.replaceState(history.state, "", `${url.pathname}${url.search}${url.hash}`);
  };

  const closeIntro = () => {
    if (!intro || intro.hidden) return;
    rememberIntro();
    removeForcedIntroQuery();
    intro.classList.add("is-leaving");
    intro.classList.remove("is-active");
    document.body.classList.remove("site-intro-open");
    window.setTimeout(() => {
      intro.hidden = true;
      intro.classList.remove("is-leaving");
      if (introFrame) introFrame.removeAttribute("src");
      introReturnFocus?.focus();
    }, 460);
  };

  const openIntro = (trigger = null) => {
    if (!intro || !introFrame) return;
    introReturnFocus = trigger;
    introAudioUnlocked = false;
    intro.hidden = false;
    introFrame.src = introFrame.dataset.src || "";
    document.body.classList.add("site-intro-open");
    requestAnimationFrame(() => {
      intro.classList.add("is-active");
      introSkip?.focus({ preventScroll: true });
    });
  };

  introSkip?.addEventListener("click", closeIntro);
  introEnter?.addEventListener("click", closeIntro);
  introReplayButtons.forEach((button) => button.addEventListener("click", () => openIntro(button)));
  window.addEventListener("message", (event) => {
    if (
      event.origin === location.origin
      && event.source === introFrame?.contentWindow
      && event.data?.type === "brainzbytes-intro-complete"
    ) {
      closeIntro();
    }
  });
  const unlockIntroAudio = () => {
    if (!intro || intro.hidden || introAudioUnlocked) return false;
    const frameWindow = introFrame?.contentWindow;
    if (!frameWindow?.unlockIntroAudio) return false;
    introAudioUnlocked = true;
    frameWindow.unlockIntroAudio();
    return true;
  };
  document.addEventListener("pointerdown", (event) => {
    if (event.target.closest("[data-intro-skip], [data-intro-enter]")) return;
    unlockIntroAudio();
  }, { capture: true });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && intro && !intro.hidden) {
      event.preventDefault();
      closeIntro();
      return;
    }
    if (intro && !intro.hidden && !introAudioUnlocked && !event.ctrlKey && !event.altKey && !event.metaKey) {
      if (unlockIntroAudio()) {
        event.preventDefault();
      }
    }
  });

  const forceIntro = new URLSearchParams(location.search).get("intro") === "1";
  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (intro && (forceIntro || (!readIntroSeen() && !reduceMotion))) {
    window.setTimeout(() => openIntro(), 0);
  }

  if (new URLSearchParams(location.search).get("from") === "journey") {
    const returnLink = document.createElement("a");
    returnLink.className = "journey-return";
    returnLink.href = "overview.html#reading-path";
    returnLink.innerHTML = '<span aria-hidden="true">←</span><span><b>Reading path</b><small>Return to all six chapters</small></span>';
    returnLink.addEventListener("click", (event) => {
      try {
        const previous = new URL(document.referrer);
        if (previous.origin === location.origin && previous.pathname.endsWith("/overview.html")) {
          event.preventDefault();
          history.back();
        }
      } catch {
        // The normal link remains the fallback when there is no usable referrer.
      }
    });
    document.body.append(returnLink);
  }

  const reveal = document.querySelectorAll("[data-reveal]");
  if (matchMedia("(prefers-reduced-motion: reduce)").matches || !("IntersectionObserver" in window)) {
    reveal.forEach((item) => item.classList.add("visible"));
  } else {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.12 });
    reveal.forEach((item) => observer.observe(item));
  }

  document.querySelectorAll("[data-copy-link]").forEach((button) => {
    button.addEventListener("click", async () => {
      await navigator.clipboard.writeText(button.dataset.copyLink || location.href);
      const original = button.textContent;
      button.textContent = "Copied";
      setTimeout(() => { button.textContent = original; }, 1200);
    });
  });

  const autoHeightFrames = [...document.querySelectorAll("iframe[data-auto-height]")];
  window.addEventListener("message", (event) => {
    if (event.origin !== location.origin || !event.data || typeof event.data !== "object") return;
    const frame = autoHeightFrames.find((item) => (
      item.contentWindow === event.source && item.dataset.autoHeight === event.data.type
    ));
    const height = Number(event.data.height);
    if (!frame || !Number.isFinite(height) || height < 300 || height > 5000) return;
    frame.style.height = `${Math.ceil(height)}px`;
    frame.style.minHeight = "0";
  });

  const storyLaunch = document.querySelector("[data-story-launch]");
  storyLaunch?.addEventListener("click", () => {
    const source = storyLaunch.dataset.storySrc;
    if (!source) return;
    const frame = document.createElement("iframe");
    frame.className = "landing-cinematic-frame";
    frame.title = "Interactive ContextWeaver intent-to-evidence product story";
    frame.setAttribute("sandbox", "allow-scripts allow-same-origin allow-popups");
    frame.setAttribute("allow", "autoplay");
    storyLaunch.replaceWith(frame);
    frame.src = source;
    frame.focus();
  }, { once: true });

  const experienceDialog = document.querySelector("[data-experience-modal]");
  const experienceFrame = experienceDialog?.querySelector("[data-experience-frame]");
  let experienceTrigger = null;

  const closeExperience = () => {
    if (!experienceDialog?.open) return;
    experienceDialog.close();
  };

  document.querySelectorAll("[data-experience-open]").forEach((link) => {
    link.addEventListener("click", (event) => {
      if (!experienceDialog?.showModal) return;
      event.preventDefault();
      experienceTrigger = link;
      if (experienceFrame && !experienceFrame.src) {
        experienceFrame.src = experienceFrame.dataset.src;
      }
      experienceDialog.showModal();
      document.body.classList.add("experience-open");
    });
  });

  experienceDialog?.querySelector("[data-experience-close]")?.addEventListener("click", closeExperience);
  experienceDialog?.addEventListener("click", (event) => {
    if (event.target === experienceDialog) closeExperience();
  });
  experienceDialog?.addEventListener("close", () => {
    document.body.classList.remove("experience-open");
    experienceTrigger?.focus();
  });
  experienceFrame?.addEventListener("load", () => {
    experienceFrame.contentWindow?.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeExperience();
    });
  });

  const spatialDialog = document.querySelector("[data-spatial-modal]");
  const spatialDialogTitle = spatialDialog?.querySelector("[data-spatial-modal-title]");
  const spatialDialogImage = spatialDialog?.querySelector("[data-spatial-modal-image]");
  const spatialDialogFrame = spatialDialog?.querySelector("[data-spatial-modal-frame]");
  let spatialTrigger = null;

  const closeSpatialView = () => {
    if (!spatialDialog?.open) return;
    spatialDialog.close();
  };

  document.querySelectorAll("[data-spatial-open]").forEach((trigger) => {
    trigger.addEventListener("click", () => {
      if (!spatialDialog?.showModal) return;
      spatialTrigger = trigger;
      const mode = trigger.dataset.spatialType === "iframe" ? "iframe" : "image";
      const title = trigger.dataset.spatialTitle || "ContextWeaver spatial view";
      const source = trigger.dataset.spatialSrc || "";
      spatialDialog.dataset.spatialMode = mode;
      if (spatialDialogTitle) spatialDialogTitle.textContent = title;
      if (mode === "image" && spatialDialogImage) {
        spatialDialogImage.src = source;
        spatialDialogImage.alt = trigger.querySelector("img")?.alt || title;
      }
      if (mode === "iframe" && spatialDialogFrame) {
        spatialDialogFrame.src = source;
        spatialDialogFrame.title = `Expanded ${title}`;
      }
      spatialDialog.showModal();
      document.body.classList.add("spatial-modal-open");
    });
  });

  spatialDialog?.querySelector("[data-spatial-close]")?.addEventListener("click", closeSpatialView);
  spatialDialog?.addEventListener("click", (event) => {
    if (event.target === spatialDialog) closeSpatialView();
  });
  spatialDialog?.addEventListener("close", () => {
    document.body.classList.remove("spatial-modal-open");
    if (spatialDialogFrame) spatialDialogFrame.src = "";
    if (spatialDialogImage) spatialDialogImage.removeAttribute("src");
    spatialTrigger?.focus();
  });
  spatialDialogFrame?.addEventListener("load", () => {
    spatialDialogFrame.contentWindow?.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeSpatialView();
    });
  });

  const learningAtlas = document.querySelector("[data-learning-atlas]");
  if (learningAtlas) {
    const goals = {
      understand: {
        label: "Understand",
        title: "From AI basics to one governed result",
        copy: "Learn why language models need enterprise knowledge, bounded Agents, approved capabilities, durable Workflows, policy, and evidence before they can produce trusted business outcomes.",
        guide: "ContextWeaver essentials for a new learner",
        items: ["AI, LLM, and RAG in plain language", "Agent, MCP, Workflow, Service, and Solution", "One governed journey with evidence"],
      },
      explain: {
        label: "Explain",
        title: "Tell the ContextWeaver product story clearly",
        copy: "Move from the customer problem to the product model, differentiators, proof points, trust story, public architecture, and claims that must not be made.",
        guide: "ContextWeaver product narrative for marketing",
        items: ["Category, audience, and core customer problem", "Cerebro, Weave, Loom, and the reuse model", "Approved proof points and claim boundaries"],
      },
      sell: {
        label: "Sell",
        title: "Connect customer pain to governed outcomes",
        copy: "Use discovery questions, qualification signals, use-case patterns, business value, deployment choices, demo flows, objections, and clear non-fit guidance.",
        guide: "ContextWeaver discovery and solution guide",
        items: ["Customer pains and qualification questions", "Outcome-led use cases and demo paths", "Objections, deployment choices, and non-fit signals"],
      },
      build: {
        label: "Build",
        title: "Create, test, publish, and operate a capability",
        copy: "Follow the governed builder lifecycle across Studios, source control, typed contracts, evaluation, immutable publication, deployment, runtime evidence, and safe retirement.",
        guide: "ContextWeaver builder handbook",
        items: ["Agent, MCP, Workflow, Service, and Solution contracts", "Tests, evaluation, policy, and publication", "Deployment, observability, and lifecycle"],
      },
      architect: {
        label: "Architect",
        title: "Traverse every boundary, dependency, and tradeoff",
        copy: "Inspect product planes, identity, authorization, data ownership, synchronous and asynchronous traffic, Kubernetes trust boundaries, portability, scaling, HA, and disaster recovery.",
        guide: "ContextWeaver architecture deep dive",
        items: ["Planes, contracts, trust boundaries, and identity", "Data, queues, storage, gateways, and runtime flow", "Portability, scale, resilience, and target architecture"],
      },
      operate: {
        label: "Operate",
        title: "Run, diagnose, recover, and improve the platform",
        copy: "Learn the cluster, service startup order, dependencies, health signals, dashboards, alerts, failure modes, incident flows, backup, restore, and disaster-recovery sequence.",
        guide: "ContextWeaver operator and SRE runbook",
        items: ["Cluster, namespaces, services, and dependencies", "Logs, metrics, traces, alerts, and diagnosis", "Shutdown, startup, backup, restore, and recovery"],
      },
    };
    const depthTimes = { essentials: "15 minutes", practitioner: "60 minutes", deep: "Complete deep dive" };
    const routeTitle = learningAtlas.querySelector("[data-learning-route-title]");
    const routeCopy = learningAtlas.querySelector("[data-learning-route-copy]");
    const routeTime = learningAtlas.querySelector("[data-learning-route-time]");
    const goalLabel = learningAtlas.querySelector("[data-learning-goal-label]");
    const guideTitle = learningAtlas.querySelector("[data-learning-guide-title]");
    const guideList = learningAtlas.querySelector("[data-learning-guide-list]");
    let selectedGoal = "understand";
    let selectedDepth = "essentials";
    let selectedLesson = "ai";

    const renderLearningSelection = () => {
      const goal = goals[selectedGoal];
      if (!goal) return;
      if (routeTitle) routeTitle.textContent = goal.title;
      if (routeCopy) routeCopy.textContent = goal.copy;
      if (routeTime) routeTime.textContent = depthTimes[selectedDepth] || depthTimes.essentials;
      if (goalLabel) goalLabel.textContent = goal.label;
      if (guideTitle) guideTitle.textContent = goal.guide;
      if (guideList) guideList.innerHTML = goal.items.map((item) => `<li>${item}</li>`).join("");
      const url = new URL(location.href);
      url.searchParams.set("goal", selectedGoal);
      url.searchParams.set("depth", selectedDepth);
      history.replaceState({}, "", url);
    };

    const requestedGoal = new URLSearchParams(location.search).get("goal");
    const requestedDepth = new URLSearchParams(location.search).get("depth");
    if (requestedGoal && goals[requestedGoal]) selectedGoal = requestedGoal;
    if (requestedDepth && depthTimes[requestedDepth]) selectedDepth = requestedDepth;

    const lessons = {
      ai: {
        label: "Lesson 01 · Foundation",
        mark: "AI",
        title: "What are AI and large language models?",
        copy: "A language model predicts useful language from learned patterns. It can explain, summarize, and draft—but it does not know enterprise truth or hold authority to act.",
        definition: "A probabilistic language engine that turns instructions and context into generated text, code, classifications, or structured output.",
        why: ["Makes complex knowledge easier to use", "Accelerates analysis and drafting", "Still requires grounding, validation, and control"],
        concepts: [
          ["Model", "A trained system that recognizes patterns and generates likely outputs."],
          ["Prompt", "The instruction, context, constraints, and examples sent to the model."],
          ["Inference", "The moment a trained model calculates a response."],
          ["Guardrail", "A control that constrains, validates, or blocks unsafe output."],
        ],
        flow: [["1", "Ask", "A user or system supplies intent."], ["2", "Contextualize", "Relevant instructions and knowledge are added."], ["3", "Generate", "The model predicts an output."], ["4", "Validate", "Policy and evidence determine what can be used."]],
        takeaway: "A model produces possibilities. A governed platform decides what is trusted, permitted, and recorded.",
        href: "overview.html",
        link: "Explore the platform view",
      },
      rag: {
        label: "Lesson 02 · Knowledge",
        mark: "RAG",
        title: "How does retrieval-augmented generation ground an answer?",
        copy: "RAG retrieves relevant, authorized knowledge before generation so a response can be current, scoped, and linked back to its sources.",
        definition: "A pattern that searches approved knowledge, assembles a context pack, and asks a model to answer from that evidence rather than model memory alone.",
        why: ["Uses enterprise-specific and current information", "Preserves citations and source ownership", "Applies access control before content reaches the model"],
        concepts: [
          ["Ingestion", "Extract, normalize, classify, and index source content."],
          ["Embedding", "A numeric representation used to compare semantic meaning."],
          ["Retrieval", "Find the best authorized chunks using keyword, vector, or hybrid search."],
          ["Citation", "A durable link from an answer back to supporting evidence."],
        ],
        flow: [["1", "Ingest", "Approved sources become searchable chunks."], ["2", "Retrieve", "The query finds authorized relevant evidence."], ["3", "Augment", "Evidence is packed into the model context."], ["4", "Answer", "The response includes citations and confidence."]],
        takeaway: "RAG does not make a model the source of truth; it connects the model to sources that remain authoritative.",
        href: "platform.html",
        link: "Explore knowledge services",
      },
      agents: {
        label: "Lesson 03 · Reasoning",
        mark: "AG",
        title: "What makes an AI Agent different from a chatbot?",
        copy: "An Agent is a bounded specialist that can inspect context, choose an approved next step, use permitted capabilities, and stop under explicit conditions.",
        definition: "A role-driven reasoning component with typed inputs and outputs, approved knowledge and tools, budgets, policy boundaries, and observable stop conditions.",
        why: ["Applies specialist reasoning consistently", "Can coordinate multiple safe steps", "Keeps autonomy bounded by contracts and policy"],
        concepts: [
          ["Role", "The narrow responsibility and expertise the Agent is allowed to exercise."],
          ["Plan", "A proposed sequence of steps, not unchecked authority to execute."],
          ["Tool", "A typed capability the Agent may request through a governed boundary."],
          ["Stop condition", "A limit, completion rule, approval gate, or escalation trigger."],
        ],
        flow: [["1", "Observe", "Read the authorized task and context."], ["2", "Plan", "Choose the next permitted action."], ["3", "Act", "Invoke a typed capability through policy."], ["4", "Inspect", "Validate evidence, stop, retry, or escalate."]],
        takeaway: "An Agent reasons inside a contract; identity, policy, credentials, and durable state remain outside it.",
        href: "#agent-learning",
        link: "Open the Agent deep dive",
      },
      mcp: {
        label: "Lesson 04 · Capabilities",
        mark: "MCP",
        title: "How does MCP connect models to real capabilities?",
        copy: "Model Context Protocol standardizes how clients discover and invoke tools, resources, and prompts without embedding every integration into the Agent.",
        definition: "A protocol boundary that publishes typed capabilities while ContextWeaver adds identity, policy, credential brokering, auditing, and dependency scope.",
        why: ["Makes integrations discoverable and reusable", "Separates reasoning from system-specific code", "Creates a consistent place to enforce least privilege"],
        concepts: [
          ["Tool", "A typed operation that may read data or create a side effect."],
          ["Resource", "Context exposed for controlled reading."],
          ["Prompt", "A reusable, versioned interaction template."],
          ["Server", "The isolated capability provider that owns its implementation."],
        ],
        flow: [["1", "Discover", "The client reads available capabilities."], ["2", "Authorize", "Identity and policy determine allowed scope."], ["3", "Invoke", "Validated arguments reach the selected server."], ["4", "Receipt", "Result, timing, and evidence return to the run."]],
        takeaway: "MCP standardizes capability access; governance determines who may use which capability and under what conditions.",
        href: "platform.html",
        link: "Explore MCP boundaries",
      },
      workflows: {
        label: "Lesson 05 · Coordination",
        mark: "WF",
        title: "Why do governed AI systems need durable Workflows?",
        copy: "Workflows own sequence, state, retries, waits, approvals, compensation, and recovery so a long-running outcome does not depend on one request or Agent.",
        definition: "A deterministic, versioned orchestration contract that coordinates services, Agents, human decisions, and side effects across durable checkpoints.",
        why: ["Survives process and infrastructure failure", "Makes approvals and retries explicit", "Separates deterministic coordination from probabilistic reasoning"],
        concepts: [
          ["Checkpoint", "Persisted progress from which a run can safely continue."],
          ["Retry", "A bounded repeat with backoff and idempotency rules."],
          ["Approval", "A durable human decision linked to identity and evidence."],
          ["Compensation", "A defined action that addresses a partial or failed side effect."],
        ],
        flow: [["1", "Compile", "Intent becomes an immutable execution plan."], ["2", "Dispatch", "Typed work goes to the right participant."], ["3", "Checkpoint", "Progress and evidence are committed."], ["4", "Finalize", "Outcome and complete run history are published."]],
        takeaway: "Agents decide within steps; Workflows own the reliable journey across steps.",
        href: "runtime.html",
        link: "Explore the runtime",
      },
      services: {
        label: "Lesson 06 · Reuse",
        mark: "SV",
        title: "What is a ContextWeaver Service?",
        copy: "A Service publishes a stable business capability that hides the changing combination of Workflow, Agents, knowledge, MCP dependencies, policy, and evidence behind it.",
        definition: "A reusable, versioned intent-to-outcome contract that can be composed into multiple Solutions without duplicating its internal implementation.",
        why: ["Encourages reuse across products and teams", "Keeps consumers independent of internal changes", "Attaches ownership, entitlement, policy, and SLOs"],
        concepts: [
          ["Contract", "The stable typed request, result, errors, and guarantees."],
          ["Composition", "The internal assets resolved to fulfill the contract."],
          ["Entitlement", "The rules defining who may discover and invoke the Service."],
          ["Lifecycle", "Versioning, evaluation, publication, deployment, and retirement."],
        ],
        flow: [["1", "Request", "A Solution invokes the Service contract."], ["2", "Resolve", "The registry selects an entitled version."], ["3", "Execute", "Workflow and capabilities produce the outcome."], ["4", "Return", "A typed result and evidence receipt are delivered."]],
        takeaway: "A Service is the reusable product boundary; its Workflow, Agents, and tools are implementation details.",
        href: "platform.html",
        link: "Explore platform contracts",
      },
      solutions: {
        label: "Lesson 07 · Experience",
        mark: "SO",
        title: "How do reusable capabilities become a complete Solution?",
        copy: "A Solution combines user experience, entitlement, data boundaries, and one or more Services into a complete outcome for a specific audience.",
        definition: "The user-facing composition that presents an approved experience while resolving reusable Services through governed APIs.",
        why: ["Focuses the platform on real user outcomes", "Reuses capabilities without exposing internals", "Keeps audience, access, and experience explicit"],
        concepts: [
          ["Audience", "The people or systems entitled to use the experience."],
          ["Experience", "The interface, interaction pattern, and status feedback."],
          ["Service Run API", "The stable boundary used to request reusable outcomes."],
          ["Outcome", "The result a user receives, including evidence and next actions."],
        ],
        flow: [["1", "Express intent", "The user starts from a goal, not infrastructure."], ["2", "Authorize", "Identity and entitlement are evaluated."], ["3", "Compose", "Required Services fulfill the request."], ["4", "Present", "The Solution returns status, result, and proof."]],
        takeaway: "Solutions are where users experience value; Services are how the platform safely reuses the machinery behind it.",
        href: "solutions.html",
        link: "Explore Solutions",
      },
      contextweaver: {
        label: "Lesson 08 · Platform",
        mark: "CW",
        title: "How do Cerebro, Weave, and Loom work together?",
        copy: "ContextWeaver separates discovery and reasoning, durable orchestration, and portable capability deployment while connecting them through typed contracts and evidence.",
        definition: "A governed AI platform that turns approved intent into reusable, observable outcomes through three cooperating product planes.",
        why: ["Keeps authoring, runtime, and deployment concerns separate", "Supports portable Kubernetes-based operation", "Makes governance and evidence part of every layer"],
        concepts: [
          ["Cerebro", "Discover, design, evaluate, govern, and operate AI assets."],
          ["Weave", "Compile intent and coordinate durable governed execution."],
          ["Loom", "Package, deploy, discover, and operate portable capabilities."],
          ["Context", "Identity, knowledge, policy, history, and evidence woven into each run."],
        ],
        flow: [["1", "Design", "Cerebro creates governed assets and contracts."], ["2", "Publish", "Immutable versions enter registries."], ["3", "Run", "Weave coordinates authorized execution."], ["4", "Operate", "Loom deploys capabilities and returns evidence."]],
        takeaway: "ContextWeaver is not one model or Agent; it is the operating system that connects intelligence to governed execution.",
        href: "architecture.html",
        link: "Open the architecture",
      },
      evidence: {
        label: "Lesson 09 · Trust",
        mark: "EV",
        title: "What turns an AI output into a verified result?",
        copy: "A verified result carries the citations, tool receipts, policy decisions, approvals, evaluations, logs, traces, and history needed to understand how it was produced.",
        definition: "An outcome whose source context, execution path, authority, side effects, quality checks, and human decisions remain reviewable after the run.",
        why: ["Supports audit and human review", "Makes failures diagnosable and recoverable", "Creates feedback for evaluation and improvement"],
        concepts: [
          ["Citation", "Evidence linking a claim to an authorized source."],
          ["Receipt", "A signed record of a capability request and result."],
          ["Trace", "The connected timing and dependency path across a run."],
          ["Evaluation", "A repeatable measurement of quality, safety, and policy adherence."],
        ],
        flow: [["1", "Capture", "Each boundary records identity and correlation."], ["2", "Attach", "Sources, decisions, and side effects become evidence."], ["3", "Evaluate", "Quality and policy checks score the outcome."], ["4", "Preserve", "Reports and history support review and learning."]],
        takeaway: "Trust is not a label added to an answer; it is the evidence preserved across the entire run.",
        href: "governance.html",
        link: "Explore governance and proof",
      },
    };
    const lessonButtons = [...learningAtlas.querySelectorAll("[data-learning-step]")];
    const lessonLabel = learningAtlas.querySelector("[data-learning-step-label]");
    const lessonTitle = learningAtlas.querySelector("[data-learning-step-title]");
    const lessonCopy = learningAtlas.querySelector("[data-learning-step-copy]");
    const lessonMark = learningAtlas.querySelector("[data-learning-step-mark]");
    const lessonDefinition = learningAtlas.querySelector("[data-learning-step-definition]");
    const lessonWhy = learningAtlas.querySelector("[data-learning-step-why]");
    const lessonConcepts = learningAtlas.querySelector("[data-learning-step-concepts]");
    const lessonFlow = learningAtlas.querySelector("[data-learning-step-flow]");
    const lessonTakeaway = learningAtlas.querySelector("[data-learning-step-takeaway]");
    const lessonLink = learningAtlas.querySelector("[data-learning-step-link]");
    const renderLesson = () => {
      const lesson = lessons[selectedLesson];
      if (!lesson) return;
      if (lessonLabel) lessonLabel.textContent = lesson.label;
      if (lessonTitle) lessonTitle.textContent = lesson.title;
      if (lessonCopy) lessonCopy.textContent = lesson.copy;
      if (lessonMark) lessonMark.textContent = lesson.mark;
      if (lessonDefinition) lessonDefinition.textContent = lesson.definition;
      if (lessonWhy) lessonWhy.innerHTML = lesson.why.map((item) => `<li>${item}</li>`).join("");
      if (lessonConcepts) lessonConcepts.innerHTML = lesson.concepts.map(([title, copy], index) => `<article><span>${String(index + 1).padStart(2, "0")}</span><b>${title}</b><p>${copy}</p></article>`).join("");
      if (lessonFlow) lessonFlow.innerHTML = lesson.flow.map(([number, title, copy], index) => `<article><span>${number}</span><b>${title}</b><p>${copy}</p></article>${index < lesson.flow.length - 1 ? '<i aria-hidden="true">→</i>' : ""}`).join("");
      if (lessonTakeaway) lessonTakeaway.textContent = lesson.takeaway;
      if (lessonLink) lessonLink.href = lesson.href;
      if (lessonLink) lessonLink.firstChild.textContent = `${lesson.link} `;
      lessonButtons.forEach((button) => {
        const active = button.dataset.learningStep === selectedLesson;
        button.classList.toggle("active", active);
        button.setAttribute("aria-pressed", String(active));
      });
      const url = new URL(location.href);
      url.searchParams.set("lesson", selectedLesson);
      history.replaceState({}, "", url);
    };
    const requestedLesson = new URLSearchParams(location.search).get("lesson");
    if (requestedLesson && lessons[requestedLesson]) selectedLesson = requestedLesson;
    lessonButtons.forEach((button) => button.addEventListener("click", () => {
      selectedLesson = button.dataset.learningStep;
      renderLesson();
    }));

    const goalButtons = [...learningAtlas.querySelectorAll("[data-learning-goal]")];
    goalButtons.forEach((button) => {
      const selected = button.dataset.learningGoal === selectedGoal;
      button.classList.toggle("active", selected);
      button.setAttribute("aria-pressed", String(selected));
      button.addEventListener("click", () => {
        selectedGoal = button.dataset.learningGoal;
        goalButtons.forEach((item) => {
          const active = item === button;
          item.classList.toggle("active", active);
          item.setAttribute("aria-pressed", String(active));
        });
        renderLearningSelection();
      });
    });

    const depthButtons = [...learningAtlas.querySelectorAll("[data-learning-depth]")];
    depthButtons.forEach((button) => {
      const selected = button.dataset.learningDepth === selectedDepth;
      button.classList.toggle("active", selected);
      button.setAttribute("aria-pressed", String(selected));
      button.addEventListener("click", () => {
        selectedDepth = button.dataset.learningDepth;
        depthButtons.forEach((item) => {
          const active = item === button;
          item.classList.toggle("active", active);
          item.setAttribute("aria-pressed", String(active));
        });
        renderLearningSelection();
      });
    });

    const jargonButton = learningAtlas.querySelector("[data-learning-jargon]");
    jargonButton?.addEventListener("click", () => {
      const active = !document.body.classList.contains("learning-jargon-on");
      document.body.classList.toggle("learning-jargon-on", active);
      jargonButton.setAttribute("aria-pressed", String(active));
      jargonButton.textContent = active ? "Jargon explanations on" : "Explain jargon inline";
    });
    learningAtlas.querySelectorAll("[data-learning-jargon-term]").forEach((button) => {
      button.addEventListener("click", () => {
        const expanded = button.dataset.expanded === "true";
        button.dataset.expanded = String(!expanded);
        button.textContent = expanded
          ? "What is a typed contract?"
          : "Typed contract: a validated input/output schema that makes expectations explicit.";
      });
    });

    const filters = [...learningAtlas.querySelectorAll("[data-component-filter]")];
    const componentCards = [...learningAtlas.querySelectorAll("[data-component-domain]")];
    filters.forEach((button) => button.addEventListener("click", () => {
      const filter = button.dataset.componentFilter;
      filters.forEach((item) => {
        const active = item === button;
        item.classList.toggle("active", active);
        item.setAttribute("aria-pressed", String(active));
      });
      componentCards.forEach((card) => {
        const domains = (card.dataset.componentDomain || "").split(" ");
        card.hidden = filter !== "all" && !domains.includes(filter);
      });
    }));

    const lensContent = {
      business: ["Why it matters", "Turn repeatable expertise into a governed capability.", "An Agent can apply a specialist role consistently while the platform preserves ownership, limits, approvals, and evidence. It augments a process; it does not become an unaccountable digital employee.", ["Good fit", "Research, classify, compare, recommend, draft"], ["Needs control", "Side effects, sensitive data, high-risk decisions"], ["ContextWeaver adds", "Identity, policy, MCP boundaries, approval, evidence"]],
      sales: ["Customer conversation", "Lead with the process problem, not autonomous AI.", "Qualify where expertise is repetitive, information is fragmented, tools are disconnected, and accountability matters. Show one bounded journey and its evidence rather than promising a general digital employee.", ["Ask", "Where does work stall or require manual coordination?"], ["Demonstrate", "A governed result with citations, approval, and receipts"], ["Avoid", "Claims of unlimited autonomy or automatic compliance"]],
      engineering: ["Implementation model", "A typed runtime profile around a model and approved dependencies.", "The Agent receives validated state, a profile, model alias, budgets, and allowlisted MCP references. It emits typed output and evidence. It does not own credentials, deployment authority, or unrestricted network access.", ["Inputs", "Schema, identity context, task state, context pack"], ["Runtime", "Bounded loop, timeout, retries, token and cost budgets"], ["Outputs", "Typed result, citations, receipts, diagnostics"]],
      architecture: ["Boundary and tradeoff", "Separate probabilistic reasoning from deterministic authority.", "Agents optimize reasoning flexibility. Workflows own order and durable control; MCP servers own capability interfaces; gateways and policy services own authorization and credentials; the Registry owns immutable identity.", ["Boundary", "Agent is not Workflow, MCP, or policy engine"], ["Scale", "Profile-bound generic runtimes and isolated queues"], ["Tradeoff", "More contracts, but safer reuse and independent evolution"]],
      operations: ["Runtime operations", "Operate the profile, queue, and evidence—not hidden reasoning.", "Monitor queue depth, execution latency, model errors, retries, budget exhaustion, output validation, and dependency health. Roll back an immutable profile or model alias without rewriting the Workflow.", ["Health", "Readiness, queue lag, model and MCP dependencies"], ["Failure", "Timeout, invalid output, unavailable provider, budget breach"], ["Recovery", "Retry safely, requeue, pause, quarantine, or roll back"]],
    };
    const lensTabs = [...learningAtlas.querySelectorAll("[data-learning-lens]")];
    const lensPanel = learningAtlas.querySelector("[data-learning-lens-panel]");
    const renderLens = (name) => {
      const content = lensContent[name];
      if (!content || !lensPanel) return;
      lensPanel.innerHTML = `<div><span class="learning-panel-kicker">${content[0]}</span><h3>${content[1]}</h3><p>${content[2]}</p></div><div class="learning-agent-loop" aria-label="Bounded Agent loop"><span>Observe</span><i>→</i><span>Plan</span><i>→</i><span>Act</span><i>→</i><span>Inspect</span><i>→</i><b>Stop</b></div><div class="learning-panel-grid"><article><span>${content[3][0]}</span><b>${content[3][1]}</b></article><article><span>${content[4][0]}</span><b>${content[4][1]}</b></article><article><span>${content[5][0]}</span><b>${content[5][1]}</b></article></div>`;
    };
    lensTabs.forEach((tab, index) => {
      tab.addEventListener("click", () => {
        lensTabs.forEach((item) => {
          const active = item === tab;
          item.classList.toggle("active", active);
          item.setAttribute("aria-selected", String(active));
          item.tabIndex = active ? 0 : -1;
        });
        renderLens(tab.dataset.learningLens);
      });
      tab.addEventListener("keydown", (event) => {
        if (!["ArrowLeft", "ArrowRight"].includes(event.key)) return;
        event.preventDefault();
        const direction = event.key === "ArrowRight" ? 1 : -1;
        const next = lensTabs[(index + direction + lensTabs.length) % lensTabs.length];
        next.click();
        next.focus();
      });
    });

    const generateButton = learningAtlas.querySelector("[data-learning-generate]");
    generateButton?.addEventListener("click", () => {
      const goal = goals[selectedGoal];
      const lessonSections = Object.values(lessons).map((lesson) => [
        `## ${lesson.label}: ${lesson.title}`,
        "",
        lesson.copy,
        "",
        `**What it is:** ${lesson.definition}`,
        "",
        "**Why it matters:**",
        ...lesson.why.map((item) => `- ${item}`),
        "",
        "**Core concepts:**",
        ...lesson.concepts.map(([title, copy]) => `- **${title}:** ${copy}`),
        "",
        "**How it works:**",
        ...lesson.flow.map(([number, title, copy]) => `${number}. **${title}:** ${copy}`),
        "",
        `> **Key takeaway:** ${lesson.takeaway}`,
        "",
      ].join("\n"));
      const guide = [
        `# ${goal.guide}`,
        "",
        `**Goal:** ${goal.label}`,
        `**Depth:** ${depthTimes[selectedDepth] || depthTimes.essentials}`,
        "",
        goal.copy,
        "",
        "## Recommended modules",
        "",
        ...goal.items.map((item) => `- ${item}`),
        "",
        ...lessonSections,
      ].join("\n");
      const blobUrl = URL.createObjectURL(new Blob([guide], { type: "text/markdown;charset=utf-8" }));
      const download = document.createElement("a");
      download.href = blobUrl;
      download.download = `contextweaver-${selectedGoal}-${selectedDepth}-guide.md`;
      download.click();
      window.setTimeout(() => URL.revokeObjectURL(blobUrl), 1000);
      generateButton.textContent = "Guide downloaded";
      generateButton.setAttribute("aria-live", "polite");
      window.setTimeout(() => { generateButton.innerHTML = 'Download my guide <span aria-hidden="true">↓</span>'; }, 1800);
    });
    renderLearningSelection();
    renderLesson();
  }
})();
