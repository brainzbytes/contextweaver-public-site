(() => {
  const root = document.documentElement;
  const storedTheme = localStorage.getItem("cw-theme");
  const preferred = matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
  root.dataset.theme = storedTheme || preferred;

  const themeButton = document.querySelector("[data-theme-toggle]");
  const updateThemeButton = () => {
    if (!themeButton) return;
    const isLight = root.dataset.theme === "light";
    themeButton.textContent = isLight ? "☾" : "☀";
    themeButton.setAttribute("aria-label", isLight ? "Use dark theme" : "Use light theme");
  };
  themeButton?.addEventListener("click", () => {
    root.dataset.theme = root.dataset.theme === "light" ? "dark" : "light";
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
})();
