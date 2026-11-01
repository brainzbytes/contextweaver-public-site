from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    "index.html",
    "overview.html",
    "platform.html",
    "studio.html",
    "runtime.html",
    "governance.html",
    "solutions.html",
    "architecture.html",
    "learning.html",
    "library.html",
    "company.html",
)
DIAGRAMS = (
    "intent-to-evidence",
    "service-factory",
    "generic-agent-runtime",
    "platform-planes",
    "capability-lifecycle",
    "governed-run",
    "scale-path",
)
ATLAS = "contextweaver-nextgen-architecture"
SPATIAL = "contextweaver-spatial-architecture"
SPATIAL_IMAGES = (
    "intent-to-evidence.png",
    "layered-governed-architecture.png",
    "governed-platform-city.png",
    "governed-call-flow.png",
    "governed-sequence-ladder.png",
    "durable-saga-flow.png",
)
SOURCE_TRUTH = ROOT / "content" / "source-truth.json"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []
        self.ids: list[str] = []
        self.images_without_alt: list[str] = []
        self.main_count = 0
        self.title_count = 0
        self.description_count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "main":
            self.main_count += 1
        if tag == "meta" and values.get("name") == "description":
            self.description_count += 1
        if "id" in values and values["id"]:
            self.ids.append(values["id"])
        if tag == "img" and "alt" not in values:
            self.images_without_alt.append(values.get("src", "(unknown)"))
        for name in ("href", "src"):
            if values.get(name):
                self.references.append(values[name])

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_data(self, data: str) -> None:
        if self.get_starttag_text() and data.strip():
            pass


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_page(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(text)
    assert_true(text.lower().startswith("<!doctype html>"), f"{path.name}: missing doctype")
    assert_true(bool(re.search(r"<title>[^<]+</title>", text, re.I)), f"{path.name}: missing title")
    assert_true(parser.description_count == 1, f"{path.name}: expected one meta description")
    assert_true(parser.main_count == 1, f"{path.name}: expected one main landmark")
    assert_true(not parser.images_without_alt, f"{path.name}: images missing alt: {parser.images_without_alt}")
    assert_true(len(parser.ids) == len(set(parser.ids)), f"{path.name}: duplicate IDs")
    for reference in parser.references:
        parsed = urlsplit(reference)
        if parsed.scheme or reference.startswith(("#", "mailto:", "data:")):
            continue
        target = (path.parent / parsed.path).resolve()
        assert_true(target.exists(), f"{path.name}: broken local reference {reference}")


def validate_diagram(slug: str) -> None:
    html_path = ROOT / "diagrams" / f"{slug}.html"
    svg_path = ROOT / "diagrams" / f"{slug}.svg"
    gif_path = ROOT / "diagrams" / f"{slug}.gif"
    for path in (html_path, svg_path, gif_path):
        assert_true(path.exists() and path.stat().st_size > 500, f"{slug}: missing or empty {path.suffix}")
    validate_page(html_path)
    ET.parse(svg_path)
    with Image.open(gif_path) as image:
        assert_true(getattr(image, "n_frames", 1) >= 6, f"{slug}: GIF needs at least six meaningful stages")
        for frame in range(image.n_frames):
            image.seek(frame)
            assert_true(image.info.get("duration") == 1000, f"{slug}: frame {frame} is not 1,000 ms")


def validate_drawio() -> None:
    path = ROOT / "diagrams" / "contextweaver-public-architecture.drawio"
    tree = ET.parse(path)
    pages = tree.getroot().findall("diagram")
    assert_true(len(pages) == len(DIAGRAMS), "Draw.io page count does not match diagrams")
    for page in pages:
        cells = page.findall("./mxGraphModel/root/mxCell")
        ids = {cell.get("id") for cell in cells}
        assert_true({"0", "1"}.issubset(ids), f"Draw.io page {page.get('name')} lacks root cells")


def validate_atlas() -> None:
    html_path = ROOT / "diagrams" / f"{ATLAS}.html"
    svg_path = ROOT / "diagrams" / f"{ATLAS}.svg"
    png_path = ROOT / "diagrams" / f"{ATLAS}.png"
    gif_path = ROOT / "diagrams" / f"{ATLAS}.gif"
    drawio_path = ROOT / "diagrams" / f"{ATLAS}.drawio"
    for path in (html_path, svg_path, png_path, gif_path, drawio_path):
        assert_true(path.exists() and path.stat().st_size > 500, f"{ATLAS}: missing or empty {path.suffix}")
    validate_page(html_path)
    ET.parse(svg_path)
    atlas_pages = ET.parse(drawio_path).getroot().findall("diagram")
    assert_true(len(atlas_pages) == 4, "NextGen atlas Draw.io must contain four pages")
    with Image.open(png_path) as image:
        assert_true(image.size == (1600, 960), "NextGen atlas PNG must be 1600x960")
    with Image.open(gif_path) as image:
        assert_true(image.size == (1200, 720), "NextGen atlas GIF must be 1200x720")
        assert_true(image.n_frames == 8, "NextGen atlas GIF must contain eight stages")
        for frame in range(image.n_frames):
            image.seek(frame)
            assert_true(image.info.get("duration") == 1000, f"NextGen atlas frame {frame} is not 1,000 ms")


def validate_spatial_architecture() -> None:
    html_path = ROOT / "diagrams" / f"{SPATIAL}.html"
    svg_path = ROOT / "diagrams" / f"{SPATIAL}.svg"
    png_path = ROOT / "diagrams" / f"{SPATIAL}.png"
    gif_path = ROOT / "diagrams" / f"{SPATIAL}.gif"
    drawio_path = ROOT / "diagrams" / f"{SPATIAL}.drawio"
    for path in (html_path, svg_path, png_path, gif_path, drawio_path):
        assert_true(path.exists() and path.stat().st_size > 500, f"{SPATIAL}: missing or empty {path.suffix}")
    validate_page(html_path)
    ET.parse(svg_path)
    drawio_pages = ET.parse(drawio_path).getroot().findall("diagram")
    assert_true(len(drawio_pages) == 1, "Spatial architecture Draw.io must contain one page")
    cells = drawio_pages[0].findall("./mxGraphModel/root/mxCell")
    assert_true({"0", "1"}.issubset({cell.get("id") for cell in cells}), "Spatial Draw.io lacks root cells")
    with Image.open(png_path) as image:
        assert_true(image.size == (1400, 840), "Spatial architecture PNG must be 1400x840")
    with Image.open(gif_path) as image:
        assert_true(image.size == (1200, 720), "Spatial architecture GIF must be 1200x720")
        assert_true(image.n_frames == 8, "Spatial architecture GIF must contain eight stages")
        for frame in range(image.n_frames):
            image.seek(frame)
            assert_true(image.info.get("duration") == 1000, f"Spatial architecture frame {frame} is not 1,000 ms")
    for image_name in SPATIAL_IMAGES:
        image_path = ROOT / "assets" / "media" / "spatial" / image_name
        assert_true(image_path.exists() and image_path.stat().st_size > 10_000, f"Missing spatial image {image_name}")


def validate_brand_overview() -> None:
    brand = ROOT / "assets" / "brand"
    html_path = brand / "brainzbytes-contextweaver-overview.html"
    svg_path = brand / "brainzbytes-contextweaver-overview.svg"
    png_path = brand / "brainzbytes-contextweaver-overview.png"
    gif_path = brand / "brainzbytes-contextweaver-overview.gif"
    drawio_path = brand / "brainzbytes-contextweaver-overview.drawio"
    for path in (html_path, svg_path, png_path, gif_path, drawio_path):
        assert_true(path.exists() and path.stat().st_size > 500, f"Brand overview missing or empty: {path.name}")
    validate_page(html_path)
    ET.parse(svg_path)
    drawio_pages = ET.parse(drawio_path).getroot().findall("diagram")
    assert_true(len(drawio_pages) == 1, "Brand overview Draw.io must contain one editable page")
    with Image.open(png_path) as image:
        assert_true(image.size == (1200, 675), "Brand overview PNG must be 1200x675")
    with Image.open(gif_path) as image:
        assert_true(image.size == (960, 540), "Brand overview GIF must be 960x540")
        assert_true(image.n_frames == 10, "Brand overview GIF must contain ten semantic stages")
        for frame in range(image.n_frames):
            image.seek(frame)
            assert_true(image.info.get("duration") == 1000, f"Brand overview frame {frame} is not 1,000 ms")


def validate_source_truth() -> None:
    ledger = json.loads(SOURCE_TRUTH.read_text(encoding="utf-8"))
    assert_true(ledger.get("schemaVersion") == 1, "Source-truth schema version must be 1")
    assert_true(
        re.fullmatch(r"\d{4}-\d{2}-\d{2}", ledger.get("auditedAt", "")) is not None,
        "Source-truth audit date must use YYYY-MM-DD",
    )
    facts = ledger.get("facts", [])
    fact_ids = [fact.get("id", "") for fact in facts]
    assert_true(facts and len(fact_ids) == len(set(fact_ids)), "Source-truth fact IDs must be unique")
    for repository, revision in ledger.get("sources", {}).items():
        assert_true(repository and re.fullmatch(r"[0-9a-f]{40}", revision) is not None, f"Invalid revision for {repository}")
    rendered = "\n".join((ROOT / page).read_text(encoding="utf-8") for page in PAGES)
    for fact in facts:
        fact_id = fact["id"]
        assert_true(fact.get("title") and fact.get("summary"), f"{fact_id}: missing public claim")
        assert_true(fact.get("evidence"), f"{fact_id}: missing evidence reference")
        assert_true(
            f'data-fact-id="{fact_id}"' in rendered,
            f"{fact_id}: source-truth fact is not rendered on any public page",
        )


def validate_product_semantics() -> None:
    overview = (ROOT / "overview.html").read_text(encoding="utf-8")
    studio = (ROOT / "studio.html").read_text(encoding="utf-8")
    runtime = (ROOT / "runtime.html").read_text(encoding="utf-8")
    solutions = (ROOT / "solutions.html").read_text(encoding="utf-8")
    architecture = (ROOT / "architecture.html").read_text(encoding="utf-8")
    atlas = (ROOT / "diagrams" / f"{ATLAS}.html").read_text(encoding="utf-8")
    story = (ROOT / "diagrams" / "intent-to-evidence.html").read_text(encoding="utf-8")

    assert_true("working Solution" in overview, "Overview must promise a working Solution")
    for concept in (
        "MCP capability",
        "bounded reasoning specialist",
        "durable coordination graph",
        "reusable executable contract",
        "final user-facing composition",
    ):
        assert_true(concept in studio, f"Studio must define {concept}")
    for term in ("Service Experience Contract", "Service Run"):
        assert_true(term in runtime and term in solutions, f"Runtime and Solutions must preserve {term}")
    for run_detail in (
        "Run history and evidence",
        "Journey timeline",
        "Run Explorer",
        "Investigate regression",
        "Accepted output",
        "Dry-run comparison",
        "tool and policy receipts",
        "Evidence bundle",
    ):
        assert_true(run_detail.lower() in runtime.lower(), f"Runtime must explain {run_detail}")
    assert_true("/my-solutions" in solutions, "Solutions must document the consumer landing route")
    assert_true("delegated" in solutions.lower(), "Solutions must document delegated external access")
    assert_true("Open run-history deep dive" in solutions, "Solutions must link to the run-history deep dive")
    assert_true("Open creation and dry runs" in solutions, "Solutions must link to Studio dry runs")
    assert_true(
        "Service is the reusable executable contract. Solution is the complete user experience." in solutions,
        "Solutions must keep Service and Solution responsibilities distinct",
    )
    for example in (
        "Business travel Solution",
        "Employee onboarding Solution",
        "Customer incident recovery Solution",
        "Insurance claim Solution",
        "Software release Solution",
    ):
        assert_true(example in solutions, f"Solutions must include the {example} example")
    for relationship in (
        "One Solution can compose many Services",
        "One Service can support many Solutions",
        "One Service can select one or more approved Workflows",
        "One typed Workflow can support multiple Services",
    ):
        assert_true(relationship in solutions, f"Solutions must explain: {relationship}")
    assert_true("five Studio contexts" in architecture, "Architecture must include all five Studio contexts")
    for spatial_view in (
        "intent-to-evidence.png",
        "layered-governed-architecture.png",
        "governed-platform-city.png",
        f"{SPATIAL}.html",
    ):
        assert_true(spatial_view in architecture, f"Architecture must include spatial view {spatial_view}")
    assert_true("architecture-block-view" not in architecture, "Retired flat architecture blocks remain")
    rendered = "\n".join((ROOT / page).read_text(encoding="utf-8") for page in PAGES)
    for image_name in SPATIAL_IMAGES:
        assert_true(image_name in rendered, f"Approved spatial image is not used: {image_name}")
    assert_true("Solutions" in atlas and "Reusable executable contracts" in atlas, "Atlas must model Solutions and Services")
    assert_true("user-facing Solution" in story, "Intent-to-evidence story must return through the user-facing Solution")

    combined = "\n".join((ROOT / page).read_text(encoding="utf-8") for page in PAGES) + atlas + story
    for stale in (
        "working Service",
        "Four creation Studios",
        "ContextWeaver Studios",
        "Agent Studio",
        "MCP Studio",
        "Service Studio",
        "Workflow Studio",
        "Solution Studio",
        "Workspaces and Studios",
        "User-facing governed outcomes",
        "one useful Service",
        "Generated production service",
    ):
        assert_true(stale not in combined, f"Stale product meaning remains: {stale}")


def main() -> None:
    for page in PAGES:
        validate_page(ROOT / page)
    for slug in DIAGRAMS:
        validate_diagram(slug)
    validate_drawio()
    validate_atlas()
    validate_spatial_architecture()
    validate_brand_overview()
    validate_source_truth()
    validate_product_semantics()
    print(
        f"Validated {len(PAGES)} pages, {len(DIAGRAMS)} complete diagram deliverables, "
        "and the public source-truth ledger."
    )


if __name__ == "__main__":
    main()
