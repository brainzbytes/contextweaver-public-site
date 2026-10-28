---
name: validate-contextweaver-public-site
description: Rebuilds and validates every public page and synchronized architecture format.
---

# Validate the ContextWeaver public site

1. Install the pinned Python dependency:
   `py -3 -m pip install -r requirements.txt`
2. Regenerate pages and all diagram formats:
   `.\scripts\build.ps1`
3. Validate local links, accessibility structure, SVG XML, GIF timing, and
   Draw.io root cells:
   `py -3 tests\validate_site.py`
4. Start a local server with `py -3 -m http.server 4173`.
5. Inspect the seven pages at desktop and mobile widths and open each
   interactive diagram full screen.
