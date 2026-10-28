from __future__ import annotations

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
    "library.html",
    "company.html",
)
DIAGRAMS = (
    "service-factory",
    "platform-planes",
    "capability-lifecycle",
    "governed-run",
    "scale-path",
)
ATLAS = "contextweaver-nextgen-architecture"


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


def main() -> None:
    for page in PAGES:
        validate_page(ROOT / page)
    for slug in DIAGRAMS:
        validate_diagram(slug)
    validate_drawio()
    validate_atlas()
    git_config = (ROOT / ".git" / "config").read_text(encoding="utf-8")
    assert_true("[remote " not in git_config, "A Git remote was configured before approval")
    print(f"Validated {len(PAGES)} pages and {len(DIAGRAMS)} complete diagram deliverables.")


if __name__ == "__main__":
    main()
