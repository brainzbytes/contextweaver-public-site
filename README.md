# ContextWeaver public site

This is a new, standalone public website for **BrainzBytes ContextWeaver**. It
is intentionally separate from the existing `brainzbytes` publishing target
and has no Git remote configured.

## Preview locally

```powershell
cd C:\Users\ajaypunreddy\nextgen\contextweaver-public-site
py -3 -m pip install -r requirements.txt
.\scripts\build.ps1
py -3 tests\validate_site.py
py -3 -m http.server 4173
```

Open `http://localhost:4173`.

## Site structure

- `index.html` — product promise and end-to-end service factory
- `platform.html` — Cerebro, Weave, Loom, and the eight platform planes
- `studio.html` — no-code and developer Agent/MCP creation
- `runtime.html` — governed dynamic service execution
- `governance.html` — security, policy, approval, evidence, and lifecycle
- `solutions.html` — individual, small-business, enterprise, and industry paths
- `architecture.html` — architecture explorer and downloadable diagrams
- `diagrams/` — five interactive HTML diagrams, static SVGs, GIFs, and one
  multi-page editable Draw.io source

## Design principles

- Progressive disclosure instead of dozens of disconnected pages.
- Clear distinction between current foundations and full target architecture.
- No claims of automatic regulatory certification.
- Accessible keyboard navigation, high contrast, reduced-motion support, and
  readable static fallbacks.
- No runtime framework, analytics tracker, third-party font, or CDN dependency.

## Rebuild

`tools/generate_site.py` owns the page content and
`tools/generate_diagrams.py` owns all diagram formats. Regenerate before
committing:

```powershell
py -3 -m pip install -r requirements.txt
.\scripts\build.ps1
py -3 tests\validate_site.py
```

The `package.json` scripts provide equivalent optional shortcuts in
environments where Node.js is available.
