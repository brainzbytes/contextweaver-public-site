from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import re
import textwrap
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


WIDTH = 1600
HEIGHT = 1100

BACKGROUND = "#020704"
PANEL = "#07130d"
PANEL_ALT = "#0b1d13"
PANEL_DEEP = "#041009"
TEXT = "#effaf1"
MUTED = "#8eaa96"
LINE = "#315446"
LIME = "#78f7a2"
GREEN = "#44df7d"
GREEN_DEEP = "#20d866"
AMBER = "#f0bf55"
RED = "#ff7188"

COLOR_MAP = {
    "#07111f": BACKGROUND,
    "#123c63": "#0d3a20",
    "#35266a": "#12301d",
    "#0b1a2c": PANEL,
    "#0c1b2d": "#06140c",
    "#0e2035": PANEL_ALT,
    "#10243a": "#123624",
    "#294866": LINE,
    "#35c8ff": GREEN,
    "#55d8ff": LIME,
    "#bfeeff": "#c9f8d6",
    "#a78bfa": GREEN_DEEP,
    "#44e0a1": LIME,
    "#ffc857": AMBER,
    "#ff668c": RED,
    "#f4f8ff": TEXT,
    "#9eb3c9": MUTED,
}

LANES = (
    (180, 145, 1220, 195),
    (120, 375, 1340, 195),
    (60, 605, 1460, 195),
)


def parse_style(value: str) -> dict[str, str]:
    style: dict[str, str] = {}
    for item in (value or "").split(";"):
        if not item:
            continue
        if "=" in item:
            key, item_value = item.split("=", 1)
            style[key] = item_value
        else:
            style[item] = "1"
    return style


def format_style(style: dict[str, str]) -> str:
    return ";".join(
        key if value == "1" and key in {"text", "ellipse", "rhombus"} else f"{key}={value}"
        for key, value in style.items()
    ) + ";"


def replace_colors(value: str) -> str:
    for old, new in COLOR_MAP.items():
        value = re.sub(re.escape(old), new, value, flags=re.IGNORECASE)
    return value


def geometry(cell: ET.Element) -> ET.Element:
    geom = cell.find("mxGeometry")
    if geom is None:
        geom = ET.SubElement(cell, "mxGeometry", {"as": "geometry"})
    return geom


def set_geometry(
    cell: ET.Element, x: float, y: float, width: float, height: float
) -> None:
    geom = geometry(cell)
    geom.set("x", f"{x:g}")
    geom.set("y", f"{y:g}")
    geom.set("width", f"{width:g}")
    geom.set("height", f"{height:g}")


def semantic_kind(style: dict[str, str]) -> str:
    color = style.get("strokeColor", "").lower()
    if color in {AMBER.lower(), "#ffc857"}:
        return "amber"
    if color in {RED.lower(), "#ff668c"}:
        return "red"
    return "green"


def card_style(kind: str) -> dict[str, str]:
    stroke = {"amber": AMBER, "red": RED}.get(kind, LIME)
    fill = {"amber": "#201707", "red": "#24080d"}.get(kind, "#06140c")
    gradient = {"amber": "#3b2808", "red": "#42101a"}.get(kind, "#123624")
    return {
        "shape": "cube",
        "size": "12",
        "direction": "south",
        "boundedLbl": "1",
        "whiteSpace": "wrap",
        "html": "1",
        "fillColor": fill,
        "gradientColor": gradient,
        "gradientDirection": "north",
        "strokeColor": stroke,
        "strokeWidth": "2",
        "fontColor": TEXT,
        "fontSize": "13",
        "shadow": "1",
        "spacingTop": "12",
        "spacingRight": "12",
        "align": "center",
        "verticalAlign": "middle",
    }


def badge_style(kind: str) -> dict[str, str]:
    stroke = {"amber": AMBER, "red": RED}.get(kind, LIME)
    fill = {"amber": "#2a1d08", "red": "#2a0a10"}.get(kind, "#071b0f")
    return {
        "rounded": "1",
        "arcSize": "50",
        "whiteSpace": "wrap",
        "html": "1",
        "fillColor": fill,
        "strokeColor": stroke,
        "strokeWidth": "1.5",
        "fontColor": TEXT,
        "fontSize": "10",
        "fontStyle": "1",
        "align": "center",
        "verticalAlign": "middle",
        "shadow": "1",
    }


def transform_page(diagram: ET.Element) -> None:
    model = diagram.find("mxGraphModel")
    root = model.find("root") if model is not None else None
    if model is None or root is None:
        raise ValueError(f"{diagram.get('name')} has no graph model")
    model.set("pageWidth", str(WIDTH))
    model.set("pageHeight", str(HEIGHT))
    model.set("background", BACKGROUND)
    cells = {
        cell.get("id"): cell
        for cell in root.findall("mxCell")
        if cell.get("id")
    }

    background = cells.get("page-background")
    if background is not None:
        set_geometry(background, 0, 0, WIDTH, HEIGHT)
        background.set(
            "style",
            "rounded=0;fillColor=#020704;strokeColor=#020704;",
        )

    for orb_id, x, y, width, height, fill, opacity in (
        ("ambient-orb-left", -120, 30, 500, 500, "#0d3a20", "18"),
        ("ambient-orb-right", 1280, 520, 440, 440, "#12301d", "16"),
    ):
        orb = cells.get(orb_id)
        if orb is not None:
            set_geometry(orb, x, y, width, height)
            orb.set(
                "style",
                f"ellipse;fillColor={fill};strokeColor=none;opacity={opacity};",
            )

    text_updates = {
        "eyebrow": (70, 20, 620, 28, LIME, 18),
        "title": (70, 48, 1040, 50, TEXT, 34),
        "subtitle": (70, 98, 1180, 34, MUTED, 16),
        "legend-title": (88, 854, 480, 28, LIME, 15),
    }
    for cell_id, (x, y, width, height, color, size) in text_updates.items():
        cell = cells.get(cell_id)
        if cell is None:
            continue
        set_geometry(cell, x, y, width, height)
        cell.set(
            "style",
            "text;html=1;strokeColor=none;fillColor=none;whiteSpace=wrap;"
            f"fontSize={size};fontColor={color};align=left;verticalAlign=middle;"
            "fontStyle=1;",
        )

    story = cells.get("story-pill")
    if story is not None:
        set_geometry(story, 1225, 54, 305, 38)
        story.set(
            "style",
            "rounded=1;arcSize=50;whiteSpace=wrap;html=1;fillColor=#07130d;"
            "strokeColor=#44df7d;strokeWidth=1.5;fontColor=#c9f8d6;"
            "fontSize=12;fontStyle=1;align=center;verticalAlign=middle;",
        )

    for lane_index, (x, y, width, height) in enumerate(LANES, 1):
        lane = cells.get(f"lane-{lane_index}")
        if lane is None:
            continue
        set_geometry(lane, x, y, width, height)
        lane.set(
            "style",
            "shape=parallelogram;perimeter=parallelogramPerimeter;fixedSize=1;"
            "size=0.055;whiteSpace=wrap;html=1;fillColor=#0b1d13;"
            "gradientColor=#041009;gradientDirection=south;strokeColor=#315446;"
            "strokeWidth=2;fontColor=#8eaa96;fontSize=13;fontStyle=1;"
            "align=left;verticalAlign=top;spacingLeft=42;spacingTop=13;shadow=1;",
        )
        children = [
            cell
            for cell in root.findall("mxCell")
            if cell.get("vertex") == "1"
            and cell.get("parent") == lane.get("id")
            and not cell.get("id", "").endswith("-badge")
        ]
        children.sort(
            key=lambda cell: float(geometry(cell).get("x", "0") or 0)
        )
        count = len(children)
        if not count:
            continue
        margin = 48.0
        gap = 26.0
        card_width = (width - margin * 2 - gap * (count - 1)) / count
        for index, card in enumerate(children):
            old_style = parse_style(card.get("style", ""))
            kind = semantic_kind(old_style)
            card_x = margin + index * (card_width + gap)
            card_progress = card_x / max(1.0, width - card_width)
            card_y = 30.0 + card_progress * 54.0
            set_geometry(card, card_x, card_y, card_width, 112)
            card.set("style", format_style(card_style(kind)))
            card.set("value", replace_colors(card.get("value", "")))
            badge = cells.get(f"{card.get('id')}-badge")
            if badge is not None:
                set_geometry(badge, card_x + 12, card_y + 6, 88, 24)
                badge.set("style", format_style(badge_style(kind)))
                badge.set("value", replace_colors(badge.get("value", "")))

    legend_bg = cells.get("legend-bg")
    if legend_bg is not None:
        set_geometry(legend_bg, 60, 840, 1480, 210)
        legend_bg.set(
            "style",
            "shape=parallelogram;perimeter=parallelogramPerimeter;fixedSize=1;"
            "size=0.035;whiteSpace=wrap;html=1;fillColor=#07130d;"
            "gradientColor=#041009;gradientDirection=south;strokeColor=#315446;"
            "strokeWidth=1.5;shadow=1;",
        )
    for index in range(1, 4):
        card = cells.get(f"legend-card-{index}")
        if card is None:
            continue
        x = 88 + (index - 1) * 474
        set_geometry(card, x, 895, 442, 120)
        style = parse_style(card.get("style", ""))
        kind = semantic_kind(style)
        stroke = {"amber": AMBER, "red": RED}.get(kind, GREEN)
        card.set(
            "style",
            "rounded=1;arcSize=12;whiteSpace=wrap;html=1;fillColor=#0b1d13;"
            f"strokeColor={stroke};strokeWidth=1.5;fontColor={TEXT};fontSize=13;"
            "align=left;verticalAlign=middle;spacingLeft=16;spacingRight=16;"
            "shadow=1;",
        )
        card.set("value", replace_colors(card.get("value", "")))

    for cell in root.findall("mxCell"):
        cell.set("value", replace_colors(cell.get("value", "")))
        if cell.get("edge") == "1":
            style = parse_style(replace_colors(cell.get("style", "")))
            kind = semantic_kind(style)
            style.update(
                {
                    "edgeStyle": "orthogonalEdgeStyle",
                    "rounded": "1",
                    "orthogonalLoop": "1",
                    "jettySize": "auto",
                    "html": "1",
                    "endArrow": "block",
                    "endFill": "1",
                    "strokeColor": {
                        "amber": AMBER,
                        "red": RED,
                    }.get(kind, GREEN),
                    "strokeWidth": "2.5",
                    "fontColor": TEXT,
                    "fontSize": "11",
                    "labelBackgroundColor": BACKGROUND,
                }
            )
            cell.set("style", format_style(style))
        elif cell.get("style"):
            cell.set("style", replace_colors(cell.get("style", "")))


def absolute_boxes(cells: dict[str, ET.Element]) -> dict[str, tuple[float, float, float, float]]:
    cache: dict[str, tuple[float, float, float, float]] = {}

    def resolve(cell_id: str, visiting: set[str] | None = None) -> tuple[float, float, float, float]:
        if cell_id in cache:
            return cache[cell_id]
        if cell_id not in cells:
            return 0, 0, 0, 0
        visiting = visiting or set()
        if cell_id in visiting:
            return 0, 0, 0, 0
        visiting.add(cell_id)
        cell = cells[cell_id]
        geom = geometry(cell)
        x = float(geom.get("x", "0") or 0)
        y = float(geom.get("y", "0") or 0)
        width = float(geom.get("width", "0") or 0)
        height = float(geom.get("height", "0") or 0)
        parent = cell.get("parent")
        if parent and parent in cells and parent not in {"0", "1"}:
            px, py, _, _ = resolve(parent, visiting)
            x += px
            y += py
        cache[cell_id] = x, y, width, height
        return cache[cell_id]

    for cell_id in cells:
        resolve(cell_id)
    return cache


def clean_lines(value: str) -> list[str]:
    value = re.sub(r"(?i)<br\s*/?>", "\n", value or "")
    value = re.sub(r"<[^>]+>", "", value)
    value = html.unescape(value)
    return [line.strip() for line in value.splitlines() if line.strip()]


def wrap_lines(lines: list[str], width: float, font_size: float, max_lines: int) -> list[str]:
    chars = max(10, int(width / max(font_size * 0.54, 1)))
    wrapped: list[str] = []
    for line in lines:
        wrapped.extend(
            textwrap.wrap(
                line,
                width=chars,
                break_long_words=False,
                break_on_hyphens=False,
            )
            or [""]
        )
    if len(wrapped) > max_lines:
        wrapped = wrapped[:max_lines]
        wrapped[-1] = wrapped[-1].rstrip(" .") + "…"
    return wrapped


def text_svg(
    lines: list[str],
    x: float,
    y: float,
    width: float,
    height: float,
    color: str,
    font_size: float,
    *,
    align: str = "center",
    bold_first: bool = False,
    max_lines: int = 5,
) -> str:
    if not lines:
        return ""
    wrapped = wrap_lines(lines, width, font_size, max_lines)
    line_height = font_size * 1.28
    total_height = line_height * len(wrapped)
    start_y = y + max(line_height, (height - total_height) / 2 + line_height * 0.8)
    anchor = "start" if align == "left" else "middle"
    text_x = x if align == "left" else x + width / 2
    tspans = []
    for index, line in enumerate(wrapped):
        weight = "800" if bold_first and index == 0 else "500"
        size = font_size + 2 if bold_first and index == 0 else font_size
        line_color = TEXT if bold_first and index == 0 else color
        tspans.append(
            f'<tspan x="{text_x:.1f}" y="{start_y + index * line_height:.1f}" '
            f'font-size="{size:.1f}" font-weight="{weight}" fill="{line_color}">'
            f"{html.escape(line)}</tspan>"
        )
    return (
        f'<text text-anchor="{anchor}" font-family="Inter,Segoe UI,Arial,sans-serif">'
        + "".join(tspans)
        + "</text>"
    )


def edge_points(
    source_box: tuple[float, float, float, float],
    target_box: tuple[float, float, float, float],
) -> list[tuple[float, float]]:
    sx, sy, sw, sh = source_box
    tx, ty, tw, th = target_box
    scx, scy = sx + sw / 2, sy + sh / 2
    tcx, tcy = tx + tw / 2, ty + th / 2
    if abs(tcy - scy) > abs(tcx - scx):
        start = (scx, sy + sh if tcy >= scy else sy)
        end = (tcx, ty if tcy >= scy else ty + th)
        mid = (start[1] + end[1]) / 2
        return [start, (start[0], mid), (end[0], mid), end]
    start = (sx + sw if tcx >= scx else sx, scy)
    end = (tx if tcx >= scx else tx + tw, tcy)
    return [start, end]


def polygon_points(points: list[tuple[float, float]]) -> str:
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def render_page(diagram: ET.Element) -> str:
    model = diagram.find("mxGraphModel")
    root = model.find("root") if model is not None else None
    if model is None or root is None:
        raise ValueError(f"{diagram.get('name')} has no graph model")
    cells = {
        cell.get("id"): cell
        for cell in root.findall("mxCell")
        if cell.get("id")
    }
    boxes = absolute_boxes(cells)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="{html.escape(diagram.get("name", "Architecture"))}">',
        "<defs>",
        '<radialGradient id="ambient-left"><stop stop-color="#20d866" stop-opacity=".18"/>'
        '<stop offset="1" stop-color="#20d866" stop-opacity="0"/></radialGradient>',
        '<radialGradient id="ambient-right"><stop stop-color="#78f7a2" stop-opacity=".12"/>'
        '<stop offset="1" stop-color="#78f7a2" stop-opacity="0"/></radialGradient>',
        '<linearGradient id="platform-fill" x1="0" y1="0" x2="1" y2="1">'
        '<stop stop-color="#0b2415"/><stop offset="1" stop-color="#041009"/></linearGradient>',
        '<linearGradient id="card-green" x1="0" y1="0" x2="0" y2="1">'
        '<stop stop-color="#0d4829"/><stop offset=".58" stop-color="#09331f"/>'
        '<stop offset="1" stop-color="#04170e"/></linearGradient>',
        '<linearGradient id="card-amber" x1="0" y1="0" x2="0" y2="1">'
        '<stop stop-color="#53390c"/><stop offset=".58" stop-color="#38260a"/>'
        '<stop offset="1" stop-color="#1f1607"/></linearGradient>',
        '<linearGradient id="card-red" x1="0" y1="0" x2="0" y2="1">'
        '<stop stop-color="#571521"/><stop offset=".58" stop-color="#3b0f18"/>'
        '<stop offset="1" stop-color="#21080d"/></linearGradient>',
        '<filter id="shadow" x="-20%" y="-30%" width="150%" height="180%">'
        '<feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#000" flood-opacity=".65"/>'
        "</filter>",
        '<filter id="glow-green" x="-40%" y="-60%" width="180%" height="220%">'
        '<feDropShadow dx="0" dy="0" stdDeviation="5" flood-color="#78f7a2" flood-opacity=".45"/>'
        "</filter>",
        '<filter id="glow-amber" x="-40%" y="-60%" width="180%" height="220%">'
        '<feDropShadow dx="0" dy="0" stdDeviation="5" flood-color="#f0bf55" flood-opacity=".42"/>'
        "</filter>",
        '<filter id="glow-red" x="-40%" y="-60%" width="180%" height="220%">'
        '<feDropShadow dx="0" dy="0" stdDeviation="5" flood-color="#ff7188" flood-opacity=".42"/>'
        "</filter>",
        '<marker id="arrow-green" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">'
        '<path d="M0 0L9 3.5L0 7Z" fill="#44df7d"/></marker>',
        '<marker id="arrow-amber" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">'
        '<path d="M0 0L9 3.5L0 7Z" fill="#f0bf55"/></marker>',
        '<marker id="arrow-red" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">'
        '<path d="M0 0L9 3.5L0 7Z" fill="#ff7188"/></marker>',
        "</defs>",
        "<style>"
        ".flow{stroke-dasharray:14 10}"
        "</style>",
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{BACKGROUND}"/>',
        '<ellipse cx="100" cy="190" rx="310" ry="310" fill="url(#ambient-left)"/>',
        '<ellipse cx="1510" cy="690" rx="300" ry="300" fill="url(#ambient-right)"/>',
    ]

    for cell in root.findall("mxCell"):
        cell_id = cell.get("id", "")
        if cell.get("vertex") != "1" or re.fullmatch(r"lane-\d+", cell_id) is None:
            continue
        x, y, width, _ = boxes[cell_id]
        depth = 18.0
        platform = [
            (x, y + 126.0),
            (x + width - 90.0, y + 184.0),
            (x + width, y + 126.0),
            (x + 90.0, y + 68.0),
        ]
        front = [
            platform[0],
            platform[1],
            (platform[1][0], platform[1][1] + depth),
            (platform[0][0], platform[0][1] + depth),
        ]
        side = [
            platform[1],
            platform[2],
            (platform[2][0], platform[2][1] + depth),
            (platform[1][0], platform[1][1] + depth),
        ]
        lines = clean_lines(cell.get("value", ""))
        parts.append(
            f'<g filter="url(#shadow)"><polygon points="{polygon_points(front)}" fill="#020905" '
            f'stroke="{LINE}" stroke-width="2"/><polygon points="{polygon_points(side)}" '
            f'fill="#06140c" stroke="{LINE}" stroke-width="2"/><polygon '
            f'points="{polygon_points(platform)}" fill="url(#platform-fill)" '
            f'stroke="{LINE}" stroke-width="2"/></g>'
        )
        parts.append(
            text_svg(lines[:1], x + 102, y + 44, width - 204, 28, MUTED, 13, align="left", max_lines=1)
        )

    for cell in root.findall("mxCell"):
        if cell.get("edge") != "1":
            continue
        source = cell.get("source")
        target = cell.get("target")
        if source not in boxes or target not in boxes:
            continue
        style = parse_style(cell.get("style", ""))
        kind = semantic_kind(style)
        stroke = {"amber": AMBER, "red": RED}.get(kind, GREEN)
        marker = {"amber": "arrow-amber", "red": "arrow-red"}.get(kind, "arrow-green")
        points = edge_points(boxes[source], boxes[target])
        parts.append(
            f'<polyline class="flow" points="{polygon_points(points)}" fill="none" '
            f'stroke="{stroke}" stroke-width="2.5" stroke-linecap="round" '
            f'stroke-linejoin="round" marker-end="url(#{marker})" opacity=".88"/>'
        )
        label_lines = clean_lines(cell.get("value", ""))
        if label_lines:
            middle = points[len(points) // 2]
            label = " · ".join(label_lines)
            label_width = min(230, max(90, len(label) * 6.5))
            parts.append(
                f'<rect x="{middle[0] - label_width / 2:.1f}" y="{middle[1] - 13:.1f}" '
                f'width="{label_width:.1f}" height="26" rx="8" fill="{BACKGROUND}" '
                f'stroke="{stroke}" stroke-opacity=".42"/>'
            )
            parts.append(
                text_svg(
                    [label],
                    middle[0] - label_width / 2 + 7,
                    middle[1] - 13,
                    label_width - 14,
                    26,
                    TEXT,
                    10,
                    max_lines=1,
                )
            )

    for cell in root.findall("mxCell"):
        if cell.get("vertex") != "1":
            continue
        cell_id = cell.get("id", "")
        if cell_id in {"page-background", "ambient-orb-left", "ambient-orb-right"}:
            continue
        x, y, width, height = boxes[cell_id]
        style = parse_style(cell.get("style", ""))
        lines = clean_lines(cell.get("value", ""))
        if re.fullmatch(r"lane-\d+", cell_id):
            continue
        if cell_id == "legend-bg":
            inset = 28
            points = [(x + inset, y), (x + width, y), (x + width - inset, y + height), (x, y + height)]
            parts.append(
                f'<polygon points="{polygon_points(points)}" fill="{PANEL}" stroke="{LINE}" '
                'stroke-width="1.5" filter="url(#shadow)"/>'
            )
            continue
        if style.get("shape") == "cube":
            kind = semantic_kind(style)
            stroke = {"amber": AMBER, "red": RED}.get(kind, LIME)
            gradient = {"amber": "card-amber", "red": "card-red"}.get(kind, "card-green")
            glow = {"amber": "glow-amber", "red": "glow-red"}.get(kind, "glow-green")
            depth = min(16, width * 0.055)
            front_width = width - depth
            front_height = height - depth
            top = [(x, y + depth), (x + depth, y), (x + width, y), (x + front_width, y + depth)]
            side = [
                (x + front_width, y + depth),
                (x + width, y),
                (x + width, y + front_height),
                (x + front_width, y + height),
            ]
            parts.append(
                f'<g filter="url(#{glow})"><polygon points="{polygon_points(top)}" '
                f'fill="{stroke}" fill-opacity=".12" stroke="{stroke}" stroke-width="1.6"/>'
                f'<polygon points="{polygon_points(side)}" fill="{stroke}" fill-opacity=".08" '
                f'stroke="{stroke}" stroke-width="1.6"/><rect x="{x:.1f}" y="{y + depth:.1f}" '
                f'width="{front_width:.1f}" height="{front_height:.1f}" rx="10" '
                f'fill="url(#{gradient})" stroke="{stroke}" stroke-width="2"/></g>'
            )
            parts.append(
                text_svg(
                    lines,
                    x + 16,
                    y + depth + 9,
                    max(0, front_width - 32),
                    max(0, front_height - 18),
                    MUTED,
                    11.5,
                    bold_first=True,
                    max_lines=5,
                )
            )
            continue
        if cell_id.endswith("-badge"):
            kind = semantic_kind(style)
            stroke = {"amber": AMBER, "red": RED}.get(kind, LIME)
            parts.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" '
                f'rx="{height / 2:.1f}" fill="{PANEL_DEEP}" stroke="{stroke}" stroke-width="1.5"/>'
            )
            parts.append(
                text_svg(lines, x + 7, y, width - 14, height, TEXT, 9.5, max_lines=1)
            )
            continue
        if style.get("text") == "1" or "text" in style:
            font_size = float(style.get("fontSize", "14") or 14)
            color = style.get("fontColor", TEXT)
            parts.append(
                text_svg(
                    lines,
                    x,
                    y,
                    width,
                    height,
                    color,
                    font_size,
                    align=style.get("align", "center"),
                    bold_first=style.get("fontStyle") in {"1", "3"},
                    max_lines=3,
                )
            )
            continue
        kind = semantic_kind(style)
        stroke = {"amber": AMBER, "red": RED}.get(kind, GREEN)
        parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" '
            f'rx="12" fill="{PANEL_ALT}" stroke="{stroke}" stroke-width="1.5" filter="url(#shadow)"/>'
        )
        parts.append(
            text_svg(
                lines,
                x + 16,
                y + 8,
                width - 32,
                height - 16,
                MUTED,
                11.5,
                align="left" if cell_id.startswith("legend-card-") else "center",
                bold_first=True,
                max_lines=5,
            )
        )
    parts.append("</svg>")
    return "".join(parts)


def slug(value: str) -> str:
    return "-".join(
        part
        for part in "".join(
            character.lower() if character.isalnum() else " "
            for character in value
        ).split()
    )


def write_outputs(source: Path, output: Path, *, write_source: bool = False) -> None:
    tree = ET.parse(source)
    root = tree.getroot()
    root.set("modified", datetime.now(timezone.utc).replace(microsecond=0).isoformat())
    for diagram in root.findall("diagram"):
        transform_page(diagram)
    if write_source:
        ET.indent(tree, space="  ")
        tree.write(source, encoding="utf-8", xml_declaration=True)

    output.mkdir(parents=True, exist_ok=True)
    for generated in output.glob("*.svg"):
        generated.unlink()
    pages = []
    for index, diagram in enumerate(root.findall("diagram"), 1):
        filename = f"{index:02d}-{slug(diagram.get('name') or f'page-{index}')}.svg"
        (output / filename).write_text(render_page(diagram), encoding="utf-8")
        pages.append({"name": diagram.get("name") or f"Page {index}", "file": filename})
    source_bytes = source.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    source_hash = hashlib.sha256(source_bytes).hexdigest()
    manifest = {
        "source": source.name,
        "sourceSha256": source_hash,
        "exporter": "ContextWeaver deterministic angled SVG renderer",
        "orientation": "three-quarter perspective",
        "pages": pages,
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Rebuilt {len(pages)} angled architecture pages in {output}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--write-source",
        action="store_true",
        help="Persist the normalized angled geometry back to the Draw.io source.",
    )
    args = parser.parse_args()
    write_outputs(
        args.source.resolve(),
        args.output.resolve(),
        write_source=args.write_source,
    )


if __name__ == "__main__":
    main()
