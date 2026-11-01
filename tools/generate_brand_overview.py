from __future__ import annotations

import argparse
import html
import math
import textwrap
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "brand"
WIDTH, HEIGHT = 1200, 675

BG = "#020705"
SURFACE = "#07140d"
SURFACE_2 = "#0b1e14"
LINE = "#28543a"
TEXT = "#f4fff5"
MUTED = "#a8c2af"
LIME = "#7cff8f"
GREEN = "#35d06f"
AMBER = "#ffbd59"


@dataclass(frozen=True)
class Node:
    key: str
    x: int
    y: int
    w: int
    h: int
    eyebrow: str
    title: str
    subtitle: str
    accent: str = GREEN


NODES = (
    Node("intent", 38, 176, 154, 130, "01 · INTENT", "Approved request", "A goal enters with identity, context, and constraints."),
    Node("studio", 222, 176, 178, 130, "02 · STUDIO", "Compose the path", "Choose Services, Workflows, Agents, and capabilities."),
    Node("weave", 438, 168, 258, 138, "05 · WEAVE", "Coordinate the outcome", "Durable orchestration turns approved intent into accountable execution.", LIME),
    Node("services", 734, 176, 188, 130, "07 · SERVICES", "Execute capabilities", "Typed contracts connect tools, systems, and people."),
    Node("solution", 952, 176, 210, 130, "09 · SOLUTION", "Deliver the experience", "A complete user-facing outcome with evidence attached.", LIME),
    Node("cerebros", 222, 344, 218, 130, "04 · CEREBROS", "Reason within bounds", "Specialists interpret context and propose the next safe action."),
    Node("loom", 490, 344, 218, 130, "06 · LOOM", "Shape the architecture", "Reusable patterns keep every capability composable and portable."),
    Node("runtime", 758, 344, 218, 130, "08 · RUNTIME", "Govern every run", "Policy, approvals, retries, and state remain visible."),
    Node("knowledge", 38, 526, 330, 108, "CONTEXT PLANE", "Knowledge + models", "Grounded retrieval, approved models, and reusable memory."),
    Node("policy", 435, 526, 330, 108, "03 · TRUST PLANE", "Identity + policy", "Least privilege, consent, isolation, and human control.", AMBER),
    Node("evidence", 832, 526, 330, 108, "10 · EVIDENCE", "Observe + improve", "Receipts, traces, evaluations, and learning close the loop.", LIME),
)

NODE_BY_KEY = {node.key: node for node in NODES}
EDGES = (
    ("intent", "studio"),
    ("studio", "weave"),
    ("weave", "services"),
    ("services", "solution"),
    ("studio", "cerebros"),
    ("cerebros", "weave"),
    ("weave", "loom"),
    ("loom", "runtime"),
    ("runtime", "services"),
    ("solution", "evidence"),
    ("knowledge", "cerebros"),
    ("policy", "weave"),
    ("runtime", "evidence"),
)
STAGES = ("intent", "policy", "studio", "cerebros", "weave", "loom", "services", "runtime", "solution", "evidence")


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = ("segoeuib.ttf", "arialbd.ttf") if bold else ("segoeui.ttf", "arial.ttf")
    for name in names:
        path = Path("C:/Windows/Fonts") / name
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def wrap(text: str, width: int) -> list[str]:
    return textwrap.wrap(text, width=width, break_long_words=False, break_on_hyphens=False)


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int, fill: str, outline: str, width: int = 1) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def center(node: Node) -> tuple[int, int]:
    return node.x + node.w // 2, node.y + node.h // 2


def edge_points(source: Node, target: Node) -> list[tuple[int, int]]:
    sx, sy = center(source)
    tx, ty = center(target)
    if abs(tx - sx) >= abs(ty - sy):
        start = (source.x + source.w if tx > sx else source.x, sy)
        end = (target.x if tx > sx else target.x + target.w, ty)
        mid = (start[0] + end[0]) // 2
        return [start, (mid, start[1]), (mid, end[1]), end]
    start = (sx, source.y + source.h if ty > sy else source.y)
    end = (tx, target.y if ty > sy else target.y + target.h)
    mid = (start[1] + end[1]) // 2
    return [start, (start[0], mid), (end[0], mid), end]


def arrow(draw: ImageDraw.ImageDraw, points: list[tuple[int, int]], color: str, width: int = 3) -> None:
    draw.line(points, fill=color, width=width, joint="curve")
    x2, y2 = points[-1]
    x1, y1 = points[-2]
    angle = math.atan2(y2 - y1, x2 - x1)
    size = 8
    left = (x2 - size * math.cos(angle - .55), y2 - size * math.sin(angle - .55))
    right = (x2 - size * math.cos(angle + .55), y2 - size * math.sin(angle + .55))
    draw.polygon([(x2, y2), left, right], fill=color)


def draw_node(draw: ImageDraw.ImageDraw, node: Node, active: bool = False) -> None:
    outline = node.accent if active else LINE
    rounded(draw, (node.x, node.y, node.x + node.w, node.y + node.h), 16, SURFACE_2 if active else SURFACE, outline, 3 if active else 1)
    draw.rounded_rectangle((node.x + 14, node.y + 13, node.x + 27, node.y + 26), radius=4, fill=node.accent)
    draw.text((node.x + 36, node.y + 13), node.eyebrow, fill=node.accent if active else MUTED, font=font(11, True))
    title_lines = wrap(node.title, max(14, int(node.w / 12)))
    draw.multiline_text((node.x + 14, node.y + 39), "\n".join(title_lines[:2]), fill=TEXT, font=font(18, True), spacing=2)
    subtitle_y = node.y + 66 + max(0, len(title_lines[:2]) - 1) * 18
    subtitle_lines = wrap(node.subtitle, max(22, int(node.w / 8.6)))
    draw.multiline_text((node.x + 14, subtitle_y), "\n".join(subtitle_lines[:3]), fill=MUTED, font=font(11), spacing=3)


def render(active: str | None = None) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    for x in range(0, WIDTH, 40):
        draw.line((x, 0, x, HEIGHT), fill="#07110c", width=1)
    for y in range(0, HEIGHT, 40):
        draw.line((0, y, WIDTH, y), fill="#07110c", width=1)
    draw.ellipse((-160, -180, 420, 300), fill="#06190f")
    draw.ellipse((880, 430, 1370, 860), fill="#05160d")
    draw.text((38, 30), "BUILD THE SYSTEM THAT FULFILLS THE INTENT", fill=TEXT, font=font(28, True))
    draw.text((38, 70), "BrainzBytes composes governed AI through ContextWeaver, Cerebros, Weave, and Loom.", fill=MUTED, font=font(15))
    rounded(draw, (38, 112, 1162, 154), 12, "#08180f", LINE)
    chips = ("IDENTITY", "POLICY", "APPROVALS", "ISOLATION", "AUDIT")
    chip_x = 57
    for index, chip in enumerate(chips):
        color = AMBER if chip == "APPROVALS" else LIME
        draw.ellipse((chip_x, 127, chip_x + 8, 135), fill=color)
        draw.text((chip_x + 15, 121), chip, fill=TEXT, font=font(11, True))
        chip_x += (155, 142, 170, 155, 0)[index]
    draw.text((1000, 121), "GOVERNED BY DEFAULT", fill=LIME, font=font(11, True))

    active_node = NODE_BY_KEY.get(active or "")
    if active_node:
        glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        glow_draw.rounded_rectangle(
            (active_node.x - 9, active_node.y - 9, active_node.x + active_node.w + 9, active_node.y + active_node.h + 9),
            radius=23,
            outline=active_node.accent,
            width=10,
        )
        image = Image.alpha_composite(image.convert("RGBA"), glow.filter(ImageFilter.GaussianBlur(12))).convert("RGB")
        draw = ImageDraw.Draw(image)

    for source_key, target_key in EDGES:
        color = "#376a49"
        if active and active in (source_key, target_key):
            color = NODE_BY_KEY[active].accent
        arrow(draw, edge_points(NODE_BY_KEY[source_key], NODE_BY_KEY[target_key]), color, 4 if color != "#376a49" else 2)

    for node in NODES:
        draw_node(draw, node, node.key == active)

    draw.text((38, 650), "INTENT → COMPOSITION → REASONING → ORCHESTRATION → SERVICE → SOLUTION → EVIDENCE", fill="#6f947a", font=font(10, True))
    return image


def svg_lines(x: int, y: int, lines: list[str], size: int, fill: str, weight: int = 400, line_height: int | None = None) -> str:
    height = line_height or int(size * 1.25)
    tspans = "".join(
        f'<tspan x="{x}" y="{y + index * height}">{html.escape(line)}</tspan>'
        for index, line in enumerate(lines)
    )
    return f'<text font-family="Inter,Segoe UI,Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}">{tspans}</text>'


def write_svg() -> None:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title description">',
        '<title id="title">BrainzBytes and ContextWeaver governed AI architecture</title>',
        '<desc id="description">Intent moves through Studio, Cerebros, Weave, Loom, governed runtime, reusable Services, and a user-facing Solution with evidence attached.</desc>',
        "<defs>",
        '<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#07110c" stroke-width="1"/></pattern>',
        '<radialGradient id="glowA"><stop stop-color="#123a22"/><stop offset="1" stop-color="#020705" stop-opacity="0"/></radialGradient>',
        '<marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#376a49"/></marker>',
        "</defs>",
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{BG}"/><rect width="{WIDTH}" height="{HEIGHT}" fill="url(#grid)"/>',
        '<circle cx="80" cy="20" r="310" fill="url(#glowA)" opacity=".58"/>',
        svg_lines(38, 54, ["BUILD THE SYSTEM THAT FULFILLS THE INTENT"], 28, TEXT, 800),
        svg_lines(38, 88, ["BrainzBytes composes governed AI through ContextWeaver, Cerebros, Weave, and Loom."], 15, MUTED),
        '<rect x="38" y="112" width="1124" height="42" rx="12" fill="#08180f" stroke="#28543a"/>',
    ]
    chip_x = 57
    for index, chip in enumerate(("IDENTITY", "POLICY", "APPROVALS", "ISOLATION", "AUDIT")):
        color = AMBER if chip == "APPROVALS" else LIME
        parts.append(f'<circle cx="{chip_x + 4}" cy="131" r="4" fill="{color}"/>')
        parts.append(svg_lines(chip_x + 15, 135, [chip], 11, TEXT, 700))
        chip_x += (155, 142, 170, 155, 0)[index]
    parts.append(svg_lines(1000, 135, ["GOVERNED BY DEFAULT"], 11, LIME, 700))
    for source_key, target_key in EDGES:
        points = edge_points(NODE_BY_KEY[source_key], NODE_BY_KEY[target_key])
        encoded = " ".join(f"{x},{y}" for x, y in points)
        parts.append(f'<polyline points="{encoded}" fill="none" stroke="#376a49" stroke-width="2" marker-end="url(#arrow)"/>')
    for node in NODES:
        parts.extend(
            [
                f'<g id="{node.key}" class="architecture-node">',
                f'<rect x="{node.x}" y="{node.y}" width="{node.w}" height="{node.h}" rx="16" fill="{SURFACE}" stroke="{LINE}"/>',
                f'<rect x="{node.x + 14}" y="{node.y + 13}" width="13" height="13" rx="4" fill="{node.accent}"/>',
                svg_lines(node.x + 36, node.y + 24, [node.eyebrow], 11, MUTED, 700),
                svg_lines(node.x + 14, node.y + 56, wrap(node.title, max(14, int(node.w / 12)))[:2], 18, TEXT, 700, 20),
                svg_lines(node.x + 14, node.y + 82, wrap(node.subtitle, max(22, int(node.w / 8.6)))[:3], 11, MUTED, 400, 14),
                "</g>",
            ]
        )
    parts.append(svg_lines(38, 660, ["INTENT → COMPOSITION → REASONING → ORCHESTRATION → SERVICE → SOLUTION → EVIDENCE"], 10, "#6f947a", 700))
    parts.append("</svg>")
    (OUT / "brainzbytes-contextweaver-overview.svg").write_text("".join(parts), encoding="utf-8")


def write_drawio() -> None:
    mxfile = ET.Element("mxfile", host="app.diagrams.net", modified="2026-11-01T00:00:00.000Z", agent="GitHub Copilot CLI", version="24.7.17")
    diagram = ET.SubElement(mxfile, "diagram", id="brand-overview", name="BrainzBytes ContextWeaver Overview")
    model = ET.SubElement(diagram, "mxGraphModel", dx="1200", dy="675", grid="1", gridSize="10", page="1", pageWidth=str(WIDTH), pageHeight=str(HEIGHT), background=BG)
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")
    for source_key, target_key in EDGES:
        cell = ET.SubElement(
            root,
            "mxCell",
            id=f"edge-{source_key}-{target_key}",
            style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;strokeColor=#376a49;strokeWidth=2;endArrow=block;endFill=1;",
            edge="1",
            parent="1",
            source=source_key,
            target=target_key,
        )
        ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})
    for node in NODES:
        value = f"<b>{html.escape(node.eyebrow)}</b><br><font style='font-size: 18px'><b>{html.escape(node.title)}</b></font><br>{html.escape(node.subtitle)}"
        cell = ET.SubElement(
            root,
            "mxCell",
            id=node.key,
            value=value,
            style=f"rounded=1;whiteSpace=wrap;html=1;fillColor={SURFACE};strokeColor={node.accent};fontColor={TEXT};fontFamily=Inter;spacing=12;verticalAlign=top;arcSize=14;",
            vertex="1",
            parent="1",
        )
        ET.SubElement(cell, "mxGeometry", x=str(node.x), y=str(node.y), width=str(node.w), height=str(node.h), **{"as": "geometry"})
    ET.indent(mxfile)
    ET.ElementTree(mxfile).write(OUT / "brainzbytes-contextweaver-overview.drawio", encoding="utf-8", xml_declaration=True)


def write_rasters() -> None:
    base = render()
    base.save(OUT / "contextweaver-weaving.png", optimize=True)
    base.save(OUT / "brainzbytes-contextweaver-overview.png", optimize=True)
    frames = [render(stage).resize((960, 540), Image.Resampling.LANCZOS) for stage in STAGES]
    frames[0].save(
        OUT / "brainzbytes-contextweaver-overview.gif",
        save_all=True,
        append_images=frames[1:],
        duration=1000,
        loop=0,
        optimize=False,
        disposal=2,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-raster", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    write_svg()
    write_drawio()
    if not args.skip_raster:
        write_rasters()
    print("Generated BrainzBytes ContextWeaver overview assets")


if __name__ == "__main__":
    main()
