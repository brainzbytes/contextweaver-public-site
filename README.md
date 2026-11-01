# ContextWeaver public site

Standalone generated product site for ContextWeaver. Human-authored narrative lives in `tools/generate_site.py`; reviewed current-product claims and their implementation evidence live in `content/source-truth.json`. Generated HTML is committed so reviews can inspect the exact artifact that will be published.

Repository: `brainzbytes/contextweaver-public-site`.

## Pages

The site contains 11 pages: Home, Overview, Platform, Studio, Runtime, Governance, Solutions, Architecture, Learning, Library, and Company. Architecture includes six complete diagram packages plus the four-page NextGen architecture atlas.

## Build and validate

```powershell
python -m pip install -r requirements.txt
.\scripts\build.ps1
python .\tests\validate_site.py
npm test
python .\tools\audit_source_truth.py
```

`audit_source_truth.py` compares the audited revisions in `content/source-truth.json` with sibling repositories under `nextgen`. A mismatch means implementation advanced and public claims must be reviewed before refreshing the ledger.

## Source-of-truth and publication model

1. Implementation repositories are authoritative for code, contracts, and operational behavior.
2. `content/source-truth.json` is the reviewed public fact ledger. Every fact names its evidence and audited repository revision.
3. `tools/generate_site.py` is the canonical public narrative and renders the ledger into the appropriate pages.
4. `tests/validate_site.py` fails if a ledger fact is missing from the generated site.
5. `.github/workflows/publish-pages.yml` rebuilds all pages and diagrams, runs Python and JavaScript validation, and fails if generated output differs from the commit.
6. Only a validated artifact from `main` is mirrored into
   `ajaypunreddy/brainzbytes`, the GitHub Pages publish target for
   `brainzbytes.com`.

The default generated sitemap targets `https://brainzbytes.com`.
`brainzbytes/contextweaver-public-site` is the only editable source for the
public site. The `ajaypunreddy/brainzbytes` repository is a generated publish
target and must not be edited manually because each successful publication
replaces its contents with the validated artifact.

The source repository requires the `BRAINZBYTES_DEPLOY_KEY` Actions secret,
whose public key is registered as a write-enabled deploy key on the publish
target. Pushes to `main` validate and publish automatically. Pull requests run
the complete validation without changing the public site.

## Editing rules

- Edit `tools/generate_site.py`, not generated HTML.
- Update `content/source-truth.json` only after reviewing implementation evidence.
- Preserve the distinction between **Implemented foundation**, **Active realization**, and **Target architecture**.
- Do not imply automatic certification, provider parity, or authority granted by a model.
- Keep Agents and MCPs as separate boundaries; Agents never possess provider credentials.
