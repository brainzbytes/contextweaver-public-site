# ContextWeaver public site

This repository is the standalone public product site for BrainzBytes
ContextWeaver.

## Content rules

- Preserve the distinction between implemented foundations, active
  realization, and target architecture.
- Do not imply automatic regulatory certification or guaranteed compliance.
- Keep the central product hierarchy consistent: MCPs expose governed
  capabilities; Agents provide bounded reasoning; Workflows coordinate
  durable work; Services expose reusable executable intent-to-outcome
  contracts; Solutions are the final user-facing compositions and lifecycle
  experiences assembled from those reusable assets.
- Do not describe Solutions as a separate runtime primitive. Solution actions
  resolve reusable Services and use the existing governed Service Run API.
- Preserve one authenticated entry point with entitlement-shaped Builder,
  Consumer (`/my-solutions`), and delegated headless experiences.
- Treat Agents and MCP servers as different capability boundaries.
- Models may propose plans but cannot authorize capabilities, tools, data,
  credentials, endpoints, or policy.
- Preserve credential non-possession: trusted gateways broker scoped
  credentials; Agents never receive provider secrets.

## Implementation rules

- Keep the site framework-free and self-contained.
- Use shared styles in `assets/css/site.css` and behavior in
  `assets/js/site.js`.
- Edit page source in `tools/generate_site.py`; edit diagram source in
  `tools/generate_diagrams.py`; regenerate outputs before committing.
- Every diagram change must update interactive HTML, static SVG, GIF, and the
  multi-page Draw.io source from the shared model.
- Maintain keyboard access, readable paused states, alt text, high contrast,
  and `prefers-reduced-motion` behavior.
- GIF frames remain 1,000 ms unless a task explicitly requests otherwise.

## Validation

```powershell
py -3 -m pip install -r requirements.txt
.\scripts\build.ps1
py -3 tests\validate_site.py
```
