from __future__ import annotations

import argparse
import base64
import html
import io
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT / "assets" / "brand"
DIAGRAMS = ROOT / "diagrams"
WIDTH = 1600
HEIGHT = 1000
GIF_FRAME_DURATION_MS = 1000

INK = "#F4FFF5"
MUTED = "#9AAF9E"
LIME = "#A8FF3E"
GREEN = "#42F59E"
AMBER = "#F2B84B"
BG = "#030A06"
PANEL = "#07110C"
SURFACE = "#0C1A12"
LINE = "#1F5A35"


def svg_header(title: str, description: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">
<title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(description)}</desc>
<defs>
  <radialGradient id="bg" cx="18%" cy="4%" r="90%"><stop stop-color="#12351F"/><stop offset=".42" stop-color="{BG}"/><stop offset="1" stop-color="#010402"/></radialGradient>
  <linearGradient id="plane" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#0C2516"/><stop offset="1" stop-color="#041009"/></linearGradient>
  <linearGradient id="glassPlane" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#0A3B22"/><stop offset=".45" stop-color="#04170E"/><stop offset="1" stop-color="#010906"/></linearGradient>
  <linearGradient id="glassFascia" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#07502C"/><stop offset="1" stop-color="#010A06"/></linearGradient>
  <linearGradient id="front" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#10291A"/><stop offset="1" stop-color="#06120B"/></linearGradient>
  <linearGradient id="amberFront" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#382B0D"/><stop offset="1" stop-color="#120D03"/></linearGradient>
  <linearGradient id="glassFront" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#0E6A3C"/><stop offset=".18" stop-color="#073D24"/><stop offset=".72" stop-color="#03180F"/><stop offset="1" stop-color="#010906"/></linearGradient>
  <linearGradient id="amberGlassFront" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#805A0A"/><stop offset=".18" stop-color="#483008"/><stop offset=".72" stop-color="#1C1203"/><stop offset="1" stop-color="#080500"/></linearGradient>
  <filter id="glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="shadow" x="-50%" y="-50%" width="220%" height="240%"><feGaussianBlur stdDeviation="14"/></filter>
  <pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse" patternTransform="skewX(-24)"><path d="M48 0H0V48" fill="none" stroke="#173623" stroke-width="1"/></pattern>
  <marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="4" orient="auto"><path d="M0 0L11 4L0 8Z" fill="{GREEN}"/></marker>
  <style>
    text{{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
    .eyebrow{{font-size:16px;font-weight:850;letter-spacing:2.7px;fill:{LIME}}}
    .title{{font-size:48px;font-weight:900;letter-spacing:-1.4px;fill:{INK}}}
    .subtitle{{font-size:20px;fill:{MUTED}}}
    .plane-label{{font-size:13px;font-weight:850;letter-spacing:2px;fill:{GREEN}}}
    .block-title{{font-size:22px;font-weight:850;fill:{INK};text-anchor:middle}}
    .block-copy{{font-size:13px;fill:{MUTED};text-anchor:middle}}
    .side-copy{{font-size:13px;fill:{MUTED};text-anchor:start}}
    .number{{font-size:15px;font-weight:900;fill:#071009;text-anchor:middle}}
    .route{{fill:none;stroke:{GREEN};stroke-width:3;stroke-linecap:round;stroke-linejoin:round;marker-end:url(#arrow);opacity:.72}}
  </style>
</defs>
<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bg)"/><rect y="105" width="{WIDTH}" height="{HEIGHT-105}" fill="url(#grid)" opacity=".28"/>
"""


def platform(x: int, y: int, width: int, depth: int, label: str, dimensional: bool = False) -> str:
    p1 = (x, y)
    p2 = (x + width, y + 104)
    p3 = (x + width + depth, y + 48)
    p4 = (x + depth, y - 56)
    top = " ".join(f"{px},{py}" for px, py in (p1, p2, p3, p4))
    front = " ".join(
        f"{px},{py}" for px, py in (p1, p2, (p2[0], p2[1] + 30), (p1[0], p1[1] + 30))
    )
    side_face = " ".join(
        f"{px},{py}" for px, py in (p2, p3, (p3[0], p3[1] + 30), (p2[0], p2[1] + 30))
    )
    if dimensional:
        shadow = " ".join(f"{px},{py+44}" for px, py in (p1, p2, p3, p4))
        return f"""<g>
<polygon points="{shadow}" fill="#000" opacity=".8" filter="url(#shadow)"/>
<polygon points="{front}" fill="url(#glassFascia)" stroke="{GREEN}" stroke-width="3"/>
<polygon points="{side_face}" fill="#020C07" stroke="{GREEN}" stroke-width="2.5"/>
<polygon points="{top}" fill="url(#glassPlane)" stroke="{GREEN}" stroke-width="4"/>
<polyline points="{top} {p1[0]},{p1[1]}" fill="none" stroke="{GREEN}" stroke-width="15" opacity=".2" filter="url(#glow)"/>
<polyline points="{p1[0]+22},{p1[1]+4} {p2[0]-22},{p2[1]+100}" fill="none" stroke="#C9FFE0" stroke-width="2" opacity=".6"/>
<text x="{x+depth+24}" y="{y-24}" class="plane-label">{html.escape(label)}</text>
</g>"""
    return f"""<g>
<polygon points="{front}" fill="#020704" stroke="#16733B" stroke-width="2" opacity=".9"/>
<polygon points="{side_face}" fill="#020704" stroke="#16733B" stroke-width="2" opacity=".9"/>
<polygon points="{top}" fill="url(#plane)" stroke="{GREEN}" stroke-width="2" opacity=".96"/>
<text x="{x+depth+24}" y="{y-24}" class="plane-label">{html.escape(label)}</text>
</g>"""


def block(
    ident: str,
    number: int,
    x: int,
    y: int,
    width: int,
    height: int,
    title: str,
    copy: str,
    accent: str = GREEN,
    dimensional: bool = False,
) -> tuple[str, tuple[int, int, int, int]]:
    top_dx, top_dy, side = 18, -13, 18
    front_fill = "url(#amberFront)" if accent == AMBER else "url(#front)"
    if dimensional:
        front_fill = "url(#amberGlassFront)" if accent == AMBER else "url(#glassFront)"
        svg = f"""<g id="{ident}">
<ellipse cx="{x+width/2+14}" cy="{y+height+28}" rx="{width*.68}" ry="27" fill="{accent}" opacity=".5" filter="url(#shadow)"/>
<rect x="{x-18}" y="{y+18}" width="{width}" height="{height}" rx="15" fill="#03120B" stroke="{accent}" stroke-width="2" opacity=".82"/>
<rect x="{x-9}" y="{y+9}" width="{width}" height="{height}" rx="15" fill="#082719" stroke="{accent}" stroke-width="2" opacity=".92"/>
<polygon points="{x},{y} {x+28},{y-21} {x+width+28},{y-21} {x+width},{y}" fill="#164C2B" stroke="{accent}" stroke-width="3"/>
<polygon points="{x+width},{y} {x+width+28},{y-21} {x+width+28},{y+height-21} {x+width},{y+height}" fill="#03130C" stroke="{accent}" stroke-width="3"/>
<rect x="{x-5}" y="{y-5}" width="{width+10}" height="{height+10}" rx="18" fill="none" stroke="{accent}" stroke-width="18" opacity=".44" filter="url(#glow)"/>
<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="15" fill="{front_fill}" stroke="{accent}" stroke-width="4"/>
<rect x="{x+7}" y="{y+8}" width="{width-14}" height="{height-16}" rx="10" fill="#010A06" fill-opacity=".82" stroke="{accent}" stroke-opacity=".88" stroke-width="3"/>
<rect x="{x+13}" y="{y+14}" width="{width-26}" height="{height-28}" rx="7" fill="none" stroke="#DFFFF0" stroke-opacity=".55" stroke-width="2"/>
<path d="M{x+14} {y+9}H{x+width-18}" stroke="#F0FFF7" stroke-width="4" stroke-linecap="round" opacity=".94"/>
<path d="M{x+8} {y+16}V{y+height-18}" stroke="{accent}" stroke-width="4" opacity=".84"/>
<path d="M{x+width-8} {y+18}V{y+height-24}" stroke="#DFFFF0" stroke-width="2" opacity=".58"/>
<rect x="{x+8}" y="{y+height-2}" width="{width+13}" height="18" rx="8" fill="#0B3C23" stroke="{accent}" stroke-width="4" filter="url(#glow)"/>
<circle cx="{x+18}" cy="{y+18}" r="17" fill="{LIME}" stroke="#F0FFC8" stroke-width="2"/><text x="{x+18}" y="{y+24}" class="number">{number}</text>
<text x="{x+width/2}" y="{y+height/2-2}" class="block-title">{html.escape(title)}</text>
<text x="{x+width/2}" y="{y+height/2+25}" class="block-copy">{html.escape(copy)}</text>
</g>"""
        return svg, (x - 22, y - 28, width + 54, height + 62)
    svg = f"""<g id="{ident}">
<ellipse cx="{x+width/2+14}" cy="{y+height+18}" rx="{width*.55}" ry="17" fill="{accent}" opacity=".18" filter="url(#shadow)"/>
<polygon points="{x},{y} {x+top_dx},{y+top_dy} {x+width+top_dx},{y+top_dy} {x+width},{y}" fill="#163B22" stroke="{accent}" stroke-width="2"/>
<polygon points="{x+width},{y} {x+width+side},{y+top_dy} {x+width+side},{y+height+top_dy} {x+width},{y+height}" fill="#06100A" stroke="{accent}" stroke-width="2"/>
<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="13" fill="{front_fill}" stroke="{accent}" stroke-width="2.5"/>
<circle cx="{x+18}" cy="{y+18}" r="17" fill="{LIME}" stroke="#E8FFB8" stroke-width="2"/><text x="{x+18}" y="{y+24}" class="number">{number}</text>
<text x="{x+width/2}" y="{y+height/2-2}" class="block-title">{html.escape(title)}</text>
<text x="{x+width/2}" y="{y+height/2+25}" class="block-copy">{html.escape(copy)}</text>
</g>"""
    return svg, (x - 8, y - 22, width + 36, height + 43)


def route(points: list[tuple[int, int]]) -> tuple[str, list[tuple[int, int]]]:
    d = "M" + " L".join(f"{x} {y}" for x, y in points)
    return f'<path d="{d}" class="route"/>', points


def overview_svg() -> tuple[str, list[tuple[int, int, int, int]], list[list[tuple[int, int]]]]:
    master_path = ROOT / "assets" / "media" / "contextweaver-overview-glass-master.png"
    rendered = Image.open(master_path).convert("RGB")
    draw = ImageDraw.Draw(rendered)
    regular_path = Path("C:/Windows/Fonts/arial.ttf")
    bold_path = Path("C:/Windows/Fonts/arialbd.ttf")

    def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(str(bold_path if bold else regular_path), size)

    def centered(text: str, center_x: int, y: int, selected_font: ImageFont.FreeTypeFont, fill: str) -> None:
        box = draw.textbbox((0, 0), text, font=selected_font)
        draw.text((center_x - (box[2] - box[0]) / 2, y), text, font=selected_font, fill=fill)

    def icon(center_x: int, center_y: int, kind: int) -> None:
        ink = (240, 255, 247)
        width = 4
        if kind % 4 == 0:
            draw.ellipse((center_x - 17, center_y - 17, center_x + 17, center_y + 17), outline=ink, width=width)
            draw.ellipse((center_x - 7, center_y - 7, center_x + 7, center_y + 7), outline=ink, width=width)
            draw.line((center_x + 7, center_y - 7, center_x + 23, center_y - 23), fill=ink, width=width)
        elif kind % 4 == 1:
            draw.polygon(
                [(center_x, center_y - 21), (center_x + 19, center_y - 12), (center_x + 15, center_y + 12),
                 (center_x, center_y + 24), (center_x - 15, center_y + 12), (center_x - 19, center_y - 12)],
                outline=ink,
            )
            draw.line((center_x - 8, center_y, center_x - 1, center_y + 8, center_x + 12, center_y - 8), fill=ink, width=width)
        elif kind % 4 == 2:
            for dx, dy in ((-18, -12), (18, -12), (0, 17)):
                draw.ellipse((center_x + dx - 7, center_y + dy - 7, center_x + dx + 7, center_y + dy + 7), outline=ink, width=width)
            draw.line((center_x - 11, center_y - 8, center_x - 3, center_y + 10), fill=ink, width=width)
            draw.line((center_x + 11, center_y - 8, center_x + 3, center_y + 10), fill=ink, width=width)
        else:
            for offset in (-13, 0, 13):
                draw.rounded_rectangle(
                    (center_x - 23 + offset, center_y - 19 + offset // 3, center_x + 10 + offset, center_y + 14 + offset // 3),
                    radius=4,
                    outline=ink,
                    width=width,
                )

    cards = [
        (120, 151, 423, 316, "Intent", "Goals + constraints", False),
        (456, 151, 754, 316, "Governance", "Identity + policy", True),
        (784, 151, 1080, 316, "Agent + MCP Studio", "Build + validate", False),
        (1110, 151, 1411, 316, "Registry", "Signed releases", False),
        (120, 408, 423, 573, "Orchestrator", "Plan + reconcile", False),
        (456, 408, 754, 573, "Agents + MCP", "Bounded execution", False),
        (784, 408, 1080, 573, "Event Mesh", "Commands + retries", True),
        (1110, 408, 1411, 573, "Live Services", "Scale + replace", False),
        (120, 664, 423, 830, "Cerebros", "Understand + reason", False),
        (456, 664, 754, 830, "Weave", "Durable workflows", False),
        (784, 664, 1080, 830, "Loom", "Portable foundation", False),
        (1110, 664, 1411, 830, "Evidence", "Receipts + replay", True),
    ]
    centered("FROM INTENT TO GOVERNED EVIDENCE", 768, 26, font(42, True), "#F4FFF5")
    centered(
        "Compose once. Govern every action. Deploy on any Kubernetes platform.",
        768,
        78,
        font(20),
        "#A9C6B3",
    )
    for index, (x1, y1, x2, y2, title, copy, amber) in enumerate(cards, 1):
        cx = (x1 + x2) // 2
        badge = "#FFD42A" if amber else "#A8FF3E"
        draw.ellipse((x1 + 8, y1 + 6, x1 + 53, y1 + 51), fill="#061008", outline=badge, width=4)
        centered(str(index), x1 + 31, y1 + 12, font(25, True), badge)
        icon(cx, y1 + 53, index)
        centered(title, cx, y1 + 84, font(22 if len(title) < 17 else 19, True), "#F4FFF5")
        centered(copy, cx, y1 + 116, font(16), "#9FF2C9")

    boxes = [(x1, y1, x2 - x1, y2 - y1) for x1, y1, x2, y2, *_ in cards]
    routes = []
    for source, target in zip(boxes, boxes[1:]):
        sx, sy, sw, sh = source
        tx, ty, tw, th = target
        source_center = (sx + sw // 2, sy + sh // 2)
        target_center = (tx + tw // 2, ty + th // 2)
        if sy == ty:
            routes.append([(sx + sw, source_center[1]), (tx, target_center[1])])
        else:
            elbow_y = sy + sh + max(20, (ty - (sy + sh)) // 2)
            routes.append(
                [(source_center[0], sy + sh), (source_center[0], elbow_y), (target_center[0], elbow_y), (target_center[0], ty)]
            )

    rendered = rendered.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    x_scale = WIDTH / 1536
    y_scale = HEIGHT / 1024
    boxes = [(round(x * x_scale), round(y * y_scale), round(w * x_scale), round(h * y_scale)) for x, y, w, h in boxes]
    routes = [[(round(x * x_scale), round(y * y_scale)) for x, y in points] for points in routes]
    buffer = io.BytesIO()
    rendered.save(buffer, format="PNG", optimize=True)
    encoded = base64.b64encode(buffer.getvalue()).decode()
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" '
        'role="img" aria-labelledby="title desc">'
        '<title id="title">BrainzBytes and ContextWeaver</title>'
        '<desc id="desc">A luminous glass architecture from governed intent through execution to evidence.</desc>'
        f'<image href="data:image/png;base64,{encoded}" x="0" y="0" width="{WIDTH}" height="{HEIGHT}" '
        'preserveAspectRatio="xMidYMid meet"/></svg>'
    )
    return svg, boxes, routes


def intent_svg() -> tuple[str, list[tuple[int, int, int, int]], list[list[tuple[int, int]]]]:
    master_path = ROOT / "assets" / "media" / "intent-to-evidence-glass-master.png"
    encoded = base64.b64encode(master_path.read_bytes()).decode()
    boxes = [
        (330, 190, 250, 170),
        (605, 155, 250, 170),
        (875, 115, 245, 180),
        (535, 410, 280, 180),
        (870, 375, 300, 180),
        (560, 665, 285, 180),
        (885, 630, 305, 190),
    ]
    routes = [
        [(580, 275), (605, 262)],
        [(855, 245), (875, 230)],
        [(995, 295), (995, 335), (785, 400), (720, 410)],
        [(815, 500), (870, 475)],
        [(1015, 555), (1015, 605), (815, 665), (770, 680)],
        [(845, 750), (885, 725)],
    ]
    labels = [
        (455, 267, "1  INTENT", "Request + purpose"),
        (730, 232, "2  RESOLVE", "Service + workflow"),
        (997, 198, "3  AUTHORIZE", "Identity + policy"),
        (675, 485, "4  COMMIT", "Plan + task + outbox"),
        (1020, 450, "5  EXECUTE", "Agents + MCP + RAG"),
        (702, 738, "6  VERIFY", "Approval + contracts"),
        (1037, 703, "7  DELIVER", "Result + evidence"),
    ]
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" '
        'role="img" aria-labelledby="title desc">',
        '<title id="title">Intent to governed evidence</title>',
        '<desc id="desc">Seven governed stages rendered as physical dimensional glass across three receding platforms.</desc>',
        '<defs><filter id="textShadow" x="-30%" y="-50%" width="160%" height="200%">'
        '<feGaussianBlur in="SourceAlpha" stdDeviation="4"/><feOffset dy="2"/>'
        '<feComponentTransfer><feFuncA type="linear" slope=".9"/></feComponentTransfer>'
        '<feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>',
        f'<image href="data:image/png;base64,{encoded}" width="{WIDTH}" height="{HEIGHT}" preserveAspectRatio="none"/>',
        '<g font-family="Inter,Segoe UI,Arial,sans-serif" text-anchor="middle" filter="url(#textShadow)">',
    ]
    for x, y, title, copy in labels:
        out.append(f'<text x="{x}" y="{y}" fill="#F4FFF5" font-size="21" font-weight="850" letter-spacing=".8">{title}</text>')
        out.append(f'<text x="{x}" y="{y + 28}" fill="#BBD0C0" font-size="13" font-weight="650">{copy}</text>')
    out.extend(
        [
            '<text x="1305" y="135" fill="#F4FFF5" font-size="19" font-weight="850" letter-spacing=".8">GOVERNANCE PLANE</text>',
            '<text x="1305" y="164" fill="#BBD0C0" font-size="12.5" font-weight="650">Identity  •  Durable state  •  Telemetry</text>',
            '<text x="1305" y="187" fill="#BBD0C0" font-size="12.5" font-weight="650">Receipts  •  Evidence  •  Replay</text>',
            "</g></svg>",
        ]
    )
    return "".join(out), boxes, routes


def write_intent_visual(skip_raster: bool = False) -> None:
    intent, intent_boxes, intent_routes = intent_svg()
    intent_svg_path = DIAGRAMS / "intent-to-evidence-flow.svg"
    intent_png_path = DIAGRAMS / "intent-to-evidence-flow.png"
    intent_svg_path.write_text(intent, encoding="utf-8")
    (DIAGRAMS / "intent-to-evidence-flow.drawio").write_text(
        drawio(intent, "Intent to governed evidence", intent_boxes, intent_routes), encoding="utf-8"
    )
    if not skip_raster:
        render_png(intent_svg_path, intent_png_path)
        gif_from_master(intent_png_path, DIAGRAMS / "intent-to-evidence-flow.gif", intent_boxes, intent_routes)
    intent_stages = [
        {"label": "Intent enters", "title": "An authenticated request states purpose and constraints.", "caption": "Tenant context and an idempotency key establish the governed run boundary."},
        {"label": "Resolve", "title": "Intent selects an immutable service contract.", "caption": "The platform resolves the published Service and exact Workflow version."},
        {"label": "Authorize", "title": "The complete execution graph is authorized.", "caption": "Identity, tools, models, data, budgets, and fallback paths are checked before admission."},
        {"label": "Commit", "title": "Durable truth is committed before work begins.", "caption": "The run, immutable plan, first task, and outbox event commit together."},
        {"label": "Execute", "title": "Bounded workers execute durable attempts.", "caption": "Agents, MCP tools, RAG, approvals, and transformations run through leased work."},
        {"label": "Verify", "title": "Contracts and human decisions gate release.", "caption": "Citations, receipts, approvals, policy outcomes, and side effects are verified."},
        {"label": "Deliver", "title": "The canonical result remains reviewable and replayable.", "caption": "Evidence, metrics, logs, traces, receipts, and replayable events close the loop."},
    ]
    (DIAGRAMS / "intent-to-evidence-flow.html").write_text(
        player_html(
            "Intent to governed evidence",
            "Seven governed stages arranged across three receding architectural planes.",
            "intent-to-evidence-flow.svg?v=20261103-11",
            intent_stages,
            intent_boxes,
            intent_routes,
            "intent-to-evidence-flow.html",
        ),
        encoding="utf-8",
    )


def drawio(svg: str, name: str, boxes: list[tuple[int, int, int, int]], routes: list[list[tuple[int, int]]]) -> str:
    encoded = base64.b64encode(svg.encode()).decode()
    cells = [
        '<mxCell id="0"/>',
        '<mxCell id="1" parent="0"/>',
        '<mxCell id="master-layer" value="Angled architecture master (locked)" parent="0"/>',
        '<mxCell id="overlay-layer" value="Editable animation overlays" parent="0"/>',
        f'<mxCell id="title" value="{html.escape(name)}" style="text;html=1;strokeColor=none;fillColor=none;fontColor={INK};fontSize=18;fontStyle=1;opacity=0;" vertex="1" parent="overlay-layer"><mxGeometry x="30" y="20" width="700" height="30" as="geometry"/></mxCell>',
        f'<mxCell id="master" value="" style="shape=image;imageAspect=0;aspect=fixed;locked=1;image=data:image/svg+xml;base64,{encoded};" vertex="1" parent="master-layer"><mxGeometry x="0" y="0" width="{WIDTH}" height="{HEIGHT}" as="geometry"/></mxCell>',
    ]
    for index, (x, y, width, height) in enumerate(boxes, 1):
        cells.append(
            f'<mxCell id="hotspot-{index}" value="Stage {index}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor={LIME};strokeWidth=3;opacity=0;" vertex="1" parent="overlay-layer"><mxGeometry x="{x}" y="{y}" width="{width}" height="{height}" as="geometry"/></mxCell>'
        )
    for index, points in enumerate(routes, 1):
        source = points[0]
        target = points[-1]
        cells.append(
            f'<mxCell id="route-{index}" value="" style="edgeStyle=none;html=1;strokeColor={LIME};strokeWidth=4;endArrow=block;opacity=0;" edge="1" parent="overlay-layer"><mxGeometry relative="1" as="geometry"><mxPoint x="{source[0]}" y="{source[1]}" as="sourcePoint"/><mxPoint x="{target[0]}" y="{target[1]}" as="targetPoint"/></mxGeometry></mxCell>'
        )
    return (
        f'<mxfile host="Electron" modified="2026-11-02T00:00:00.000Z" version="26.0.0"><diagram id="{name}" name="{html.escape(name)}">'
        f'<mxGraphModel dx="1600" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{WIDTH}" pageHeight="{HEIGHT}" math="0" shadow="0"><root>'
        + "".join(cells)
        + "</root></mxGraphModel></diagram></mxfile>"
    )


def render_png(svg_path: Path, png_path: Path) -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=1)
        page.goto(svg_path.resolve().as_uri())
        page.screenshot(path=str(png_path), omit_background=False)
        browser.close()


def gif_from_master(
    png_path: Path,
    gif_path: Path,
    boxes: list[tuple[int, int, int, int]],
    routes: list[list[tuple[int, int]]],
) -> None:
    master = Image.open(png_path).convert("RGB")
    frames = []
    for index, box in enumerate(boxes):
        frame = master.copy()
        draw = ImageDraw.Draw(frame, "RGBA")
        x, y, width, height = box
        draw.rounded_rectangle((x, y, x + width, y + height), radius=18, fill=(168, 255, 62, 18), outline=(168, 255, 62, 255), width=6)
        if index > 0 and index - 1 < len(routes):
            draw.line(routes[index - 1], fill=(168, 255, 62, 255), width=7, joint="curve")
        frame.thumbnail((960, 600), Image.Resampling.LANCZOS)
        frames.append(frame)
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=GIF_FRAME_DURATION_MS,
        loop=0,
        optimize=True,
    )


def player_html(
    title: str,
    subtitle: str,
    svg_name: str,
    stages: list[dict[str, str]],
    boxes: list[tuple[int, int, int, int]],
    routes: list[list[tuple[int, int]]],
    standalone_fallback: str,
    audio_file: str | None = None,
) -> str:
    stage_data = []
    for index, stage in enumerate(stages):
        stage_data.append(
            {
                **stage,
                "box": boxes[index],
                "route": routes[index - 1] if index > 0 and index - 1 < len(routes) else [],
            }
        )
    data = json.dumps(stage_data, separators=(",", ":"))
    audio_gate = (
        '<div class="audio-gate" id="audioGate"><button type="button" id="beginStory">Start jazz + female narration'
        "<small>Or press any key to begin the narrated story</small></button></div>"
        if audio_file
        else ""
    )
    audio_controls = (
        '<button id="music" aria-pressed="true">Music on</button><button id="narration" aria-pressed="true">Narration on</button>'
        if audio_file
        else ""
    )
    audio_element = f'<audio id="jazz" src="{audio_file}" loop preload="auto"></audio>' if audio_file else ""
    canvas_content = (
        f'<section class="canvas" id="architectureCanvas"><img src="{svg_name}" alt="{html.escape(subtitle)}">'
        f'<svg class="overlay" viewBox="0 0 {WIDTH} {HEIGHT}" aria-hidden="true"><defs><filter id="glow">'
        '<feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/>'
        '<feMergeNode in="SourceGraphic"/></feMerge></filter></defs><g id="focusLayer"></g>'
        f'<g id="routeLayer"></g></svg>{audio_gate}</section>'
    )
    portal_css = """
.logo-portal{display:grid;grid-template-columns:104px minmax(0,1fr) 104px;border-bottom:1px solid var(--line);background:#020705}
.portal-screen{position:relative;min-width:0;overflow:hidden;background:#020705}.portal-screen .canvas{height:100%}
.portal-rail{position:relative;z-index:4;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;padding:12px 9px;background:linear-gradient(180deg,#0a2115,#06110b);border-color:#316b48;border-style:solid}
.portal-rail--brainz{border-width:0 1px 0 0}.portal-rail--context{border-width:0 0 0 1px}
.logo-plate{position:relative;display:grid;place-items:center;width:76px;height:76px;border:1px solid #68eda2;border-radius:22px;background:radial-gradient(circle at 28% 22%,#245c37 0,#102d1c 44%,#07110d 78%);box-shadow:inset 0 1px #ffffff24,0 18px 34px #0009}
.portal-rail--context .logo-plate{border-color:#f2b84b;background:radial-gradient(circle at 72% 20%,#5f481b 0,#273316 42%,#07110d 78%)}
.logo-plate::after{position:absolute;inset:8px;content:"";border:1px solid #ffffff18;border-radius:15px}.logo-plate img{position:relative;z-index:1;width:50px;height:50px}
.portal-name{text-align:center;line-height:1.12}.portal-name strong{display:block;font-size:11px}.portal-name span{display:block;margin-top:4px;color:var(--muted);font-size:8px;font-weight:800;letter-spacing:.12em;text-transform:uppercase}
.factory-plane{position:absolute;inset:0;width:100%;height:100%;border:0;background:#020705}.factory-plane[hidden]{display:none}
""" if audio_file else ""
    canvas_markup = (
        '<section class="logo-portal" aria-label="BrainzBytes and ContextWeaver illuminated logo portal">'
        '<aside class="portal-rail portal-rail--brainz"><div class="logo-plate"><img src="brainzbytes-b4.svg" alt="BrainzBytes"></div>'
        '<div class="portal-name"><strong>BrainzBytes</strong><span>AI company</span></div></aside>'
        f'<div class="portal-screen">{canvas_content}<iframe class="factory-plane" id="factoryPlane" '
        'src="../../diagrams/service-factory.html?portal=1&amp;v=20261103-9" title="Universal Solution and Capability Factory" '
        'sandbox="allow-scripts allow-same-origin" loading="eager" hidden></iframe></div>'
        '<aside class="portal-rail portal-rail--context"><div class="logo-plate"><img src="contextweaver-c1.svg" alt="ContextWeaver"></div>'
        '<div class="portal-name"><strong>ContextWeaver</strong><span>Governed AI</span></div></aside></section>'
        if audio_file
        else canvas_content
    )
    factory_init = (
        'const factoryPlane=byId("factoryPlane"),architectureCanvas=byId("architectureCanvas");'
        'function syncFactoryPlane(stageIndex=index){factoryPlane.contentWindow?.postMessage({type:"contextweaver-factory-stage",stage:Math.min(2,Math.floor(stageIndex/4))},location.origin)}'
        'factoryPlane.addEventListener("load",()=>syncFactoryPlane());'
        'function showFactoryPlane(){clearTimeout(timer);if(typeof stopSpeech==="function")stopSpeech();architectureCanvas.hidden=true;factoryPlane.hidden=false;syncFactoryPlane(index);timer=setTimeout(completeIntro,2200)}'
        if audio_file
        else 'function syncFactoryPlane(){}function showFactoryPlane(){completeIntro()}'
    )
    factory_render = "architectureCanvas.hidden=false;factoryPlane.hidden=true;syncFactoryPlane();" if audio_file else ""
    factory_opening = "architectureCanvas.hidden=false;factoryPlane.hidden=true;syncFactoryPlane(0);" if audio_file else ""
    intro_finish = "showFactoryPlane()" if audio_file else "completeIntro()"
    audio_init = (
        """const jazz=byId("jazz");let audioStarted=false,musicEnabled=true,narrationEnabled=true,storyStarted=false,narratorVoice=null,voiceLoadPromise=null,speechToken=0,speechKeepAlive=0;jazz.volume=.2;
const narratorPreferences=[
  {label:"Jenny",pattern:/Microsoft Jenny/i},{label:"Aria",pattern:/Microsoft Aria/i},
  {label:"Ava",pattern:/Microsoft Ava/i},{label:"Emma",pattern:/Microsoft Emma/i},
  {label:"Michelle",pattern:/Microsoft Michelle/i},{label:"Sonia",pattern:/Microsoft Sonia/i},
  {label:"Samantha",pattern:/Samantha/i},{label:"Zira",pattern:/Microsoft Zira/i},
  {label:"Google female",pattern:/Google (?:UK|US) English Female/i},{label:"Female voice",pattern:/\\bfemale\\b/i}
];
function chooseNarrator(){
  if(!("speechSynthesis" in window))return null;
  const voices=speechSynthesis.getVoices(),englishVoices=voices.filter(voice=>/^en(?:-|_)/i.test(voice.lang));
  const preference=narratorPreferences.find(({pattern})=>englishVoices.some(voice=>pattern.test(voice.name)));
  narratorVoice=preference?englishVoices.find(voice=>preference.pattern.test(voice.name)):
    englishVoices.find(voice=>voice.default)||englishVoices.find(voice=>voice.localService)||englishVoices[0]||voices.find(voice=>voice.default)||voices[0]||null;
  byId("voiceName").textContent=preference?`Female narrator · ${preference.label}`:narratorVoice?"English narrator":"Browser narrator";
  return narratorVoice;
}
chooseNarrator();
if("speechSynthesis" in window){speechSynthesis.addEventListener?.("voiceschanged",chooseNarrator);speechSynthesis.onvoiceschanged=chooseNarrator}
function waitForNarrator(){
  const selected=chooseNarrator();if(selected||!("speechSynthesis" in window))return Promise.resolve(selected);
  if(!voiceLoadPromise)voiceLoadPromise=new Promise(resolve=>{const started=performance.now();const poll=()=>{const voice=chooseNarrator();if(voice||performance.now()-started>=5000){voiceLoadPromise=null;resolve(voice);return}setTimeout(poll,60)};setTimeout(poll,60)});
  return voiceLoadPromise;
}
async function speak(stage){
  clearTimeout(timer);stopSpeech();
  if(!playing||!audioStarted||!narrationEnabled||!("speechSynthesis" in window)){scheduleFallback(stage);return}
  const token=++speechToken,voice=await waitForNarrator();
  if(token!==speechToken||!playing||!narrationEnabled)return;
  const startUtterance=(attempt=0)=>{
    if(token!==speechToken||!playing||!narrationEnabled)return;
    const utterance=new SpeechSynthesisUtterance(narrationText(stage));
    if(voice)utterance.voice=voice;utterance.lang=voice?.lang||"en-US";utterance.rate=.92;utterance.pitch=1.02;
    let started=false,retryScheduled=false;
    const retry=()=>{
      if(retryScheduled||started||token!==speechToken||!playing||!narrationEnabled)return;
      retryScheduled=true;clearTimeout(startGuard);speechSynthesis.cancel();
      if(attempt<2)setTimeout(()=>startUtterance(attempt+1),180);else scheduleFallback(stage)
    };
    const startGuard=setTimeout(retry,1800);
    utterance.onstart=()=>{if(token!==speechToken)return;started=true;clearTimeout(startGuard);jazz.volume=musicEnabled?.07:0;timer=setTimeout(()=>{if(token!==speechToken||!playing)return;speechToken+=1;clearInterval(speechKeepAlive);speechKeepAlive=0;speechSynthesis.cancel();jazz.volume=musicEnabled?.2:0;advance()},narrationWatchdogDelay(stage));speechKeepAlive=setInterval(()=>{if(token===speechToken&&speechSynthesis.paused)speechSynthesis.resume()},8000)};
    utterance.onend=()=>{if(token!==speechToken)return;clearTimeout(startGuard);clearTimeout(timer);clearInterval(speechKeepAlive);speechKeepAlive=0;jazz.volume=musicEnabled?.2:0;timer=setTimeout(advance,900)};
    utterance.onerror=()=>{if(token!==speechToken)return;if(!started){retry();return}clearTimeout(startGuard);clearTimeout(timer);clearInterval(speechKeepAlive);speechKeepAlive=0;jazz.volume=musicEnabled?.2:0;scheduleFallback(stage)};
    speechSynthesis.resume();speechSynthesis.speak(utterance)
  };
  setTimeout(()=>startUtterance(),120)
}
function narrationText(stage){return stage.title+". "+stage.caption}
function stopSpeech(){speechToken+=1;clearInterval(speechKeepAlive);speechKeepAlive=0;if("speechSynthesis" in window)speechSynthesis.cancel();jazz.volume=musicEnabled?.2:0}
function fallbackDelay(stage){return Math.max(6500,Math.min(10500,narrationText(stage).length*52))}
function narrationWatchdogDelay(stage){return Math.max(18000,Math.min(32000,narrationText(stage).length*95))}
function scheduleFallback(stage){clearTimeout(timer);if(playing)timer=setTimeout(advance,fallbackDelay(stage))}"""
        if audio_file
        else "function speak(){}"
    )
    audio_handlers = (
        'async function beginAudio(){if(audioStarted)return true;audioStarted=true;storyStarted=true;byId("audioGate").hidden=true;if("speechSynthesis" in window)speechSynthesis.resume();'
        'if(musicEnabled){try{await jazz.play()}catch{musicEnabled=false;byId("music").textContent="Music off"}}render(true);return true};'
        'function unlockFromGesture(event){if(audioStarted||event?.isTrusted===false)return false;beginAudio();return true};'
        'window.unlockIntroAudio=()=>beginAudio();window.isIntroAudioUnlocked=()=>audioStarted;'
        'byId("beginStory").onclick=beginAudio;'
        'byId("music").onclick=async()=>{musicEnabled=!musicEnabled;byId("music").ariaPressed=String(musicEnabled);'
        'byId("music").textContent=musicEnabled?"Music on":"Music off";if(musicEnabled){audioStarted=true;byId("audioGate").hidden=true;'
        'try{await jazz.play()}catch{musicEnabled=false}}else jazz.pause()};'
        'byId("narration").onclick=()=>{narrationEnabled=!narrationEnabled;byId("narration").ariaPressed=String(narrationEnabled);'
        'byId("narration").textContent=narrationEnabled?"Narration on":"Narration off";if(narrationEnabled){audioStarted=true;'
        'byId("audioGate").hidden=true;speak(stages[index])}else{stopSpeech();scheduleFallback(stages[index])}};'
        'addEventListener("pointerdown",event=>{if(!event.target.closest("button,a"))unlockFromGesture(event)},{capture:true});'
        'addEventListener("pagehide",()=>{clearTimeout(timer);stopSpeech();jazz.pause()});'
        if audio_file
        else ""
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{html.escape(subtitle)}"><meta name="theme-color" content="{BG}">
<title>{html.escape(title)} | BrainzBytes</title>
<style>
:root{{--bg:{BG};--panel:{PANEL};--surface:{SURFACE};--line:{LINE};--muted:{MUTED};--ink:{INK};--lime:{LIME}}}
*{{box-sizing:border-box}}html,body{{margin:0;min-height:100%;background:var(--bg);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
body{{display:grid;place-items:center;padding:18px;background:radial-gradient(circle at 12% 0,#17331f 0,transparent 32%),var(--bg)}}button{{font:inherit}}
.player{{width:min(1180px,100%);border:1px solid var(--line);border-radius:24px;overflow:hidden;background:var(--panel);box-shadow:0 24px 80px #0009}}
.topbar{{display:flex;align-items:center;justify-content:space-between;gap:18px;padding:13px 17px;border-bottom:1px solid var(--line)}}.topbar strong{{font-size:13px}}.topbar div{{display:flex;gap:12px}}.topbar span{{color:var(--muted);font-size:10px;font-weight:800;letter-spacing:.12em;text-transform:uppercase}}
.canvas{{position:relative;aspect-ratio:8/5;background:#020704;overflow:hidden}}.canvas>img{{display:block;width:100%;height:100%;object-fit:contain;transform:scale(.88);transform-origin:center}}
.overlay{{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;transform:scale(.88);transform-origin:center}}.focus{{fill:#a8ff3e12;stroke:var(--lime);stroke-width:5;vector-effect:non-scaling-stroke;filter:url(#glow)}}.route{{fill:none;stroke:var(--lime);stroke-width:6;stroke-linecap:round;stroke-linejoin:round;vector-effect:non-scaling-stroke;stroke-dasharray:14 11;filter:url(#glow);animation:flow 1.1s linear infinite}}
@keyframes flow{{to{{stroke-dashoffset:-50}}}}.caption{{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:18px;align-items:center;min-height:108px;padding:16px 18px;border-top:1px solid var(--line);background:linear-gradient(135deg,var(--surface),var(--panel))}}.caption-label{{margin:0 0 5px;color:var(--lime);font-size:9px;font-weight:900;letter-spacing:.16em;text-transform:uppercase}}.caption h1{{margin:0;font-size:clamp(17px,2vw,25px)}}.caption p:last-child{{margin:6px 0 0;color:var(--muted);font-size:12px;line-height:1.45}}
.audio-gate{{position:absolute;inset:0;display:grid;place-items:center;background:linear-gradient(#050b0812,#050b08b8)}}.audio-gate[hidden]{{display:none}}.audio-gate button{{display:grid;gap:4px;min-width:210px;padding:14px 18px;border:1px solid var(--lime);border-radius:12px;background:#102c1d;color:var(--ink);font-weight:850;cursor:pointer}}.audio-gate small{{color:#b8cabd;font-size:10px}}
.controls{{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:6px}}.controls button{{min-height:35px;padding:0 11px;border:1px solid #315b3b;border-radius:8px;background:#0c1810;color:#d4e4d7;font-size:10px;font-weight:800;cursor:pointer}}.controls button:hover,.controls button:focus-visible{{border-color:var(--lime);color:var(--ink);outline:none}}.controls .primary{{border-color:var(--lime);background:var(--lime);color:#061008}}
.progress{{display:grid;grid-template-columns:repeat({len(stages)},1fr);gap:4px;padding:0 18px 14px}}.progress button{{height:4px;padding:0;border:0;border-radius:99px;background:#244a2d;cursor:pointer}}.progress button.active{{background:var(--lime);box-shadow:0 0 12px #a8ff3e88}}
{portal_css}
body.embedded{{padding:0}}body.embedded .player{{width:100%;border:0;border-radius:0;box-shadow:none}}body.popout{{padding:24px}}
@media(max-width:760px){{.caption{{grid-template-columns:1fr}}.controls{{justify-content:flex-start}}.controls button{{flex:1 1 auto}}.topbar span{{display:none}}.logo-portal{{grid-template-columns:58px minmax(0,1fr) 58px}}.portal-rail{{padding:7px 4px}}.logo-plate{{width:44px;height:44px;border-radius:13px}}.logo-plate::after{{inset:5px;border-radius:9px}}.logo-plate img{{width:31px;height:31px}}.portal-name{{display:none}}}}
@media(prefers-reduced-motion:reduce){{*,*::before,*::after{{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}}}
</style></head><body>
<main class="player" aria-label="{html.escape(title)}">
<header class="topbar"><strong>{html.escape(title)}</strong><div><span id="voiceName"></span><span id="stageCount">01 / {len(stages):02d}</span></div></header>
{canvas_markup}
<section class="caption" aria-live="polite"><div><p class="caption-label" id="stageLabel"></p><h1 id="stageTitle"></h1><p id="stageCaption"></p></div><div class="controls"><button id="previous">Previous</button><button id="playPause" class="primary">Pause</button><button id="next">Next</button><button id="reset">Reset</button>{audio_controls}<button id="popout">Pop out</button></div></section>
<nav class="progress" id="progress" aria-label="Animation stages"></nav>{audio_element}</main>
<script>
const stages={data};const params=new URLSearchParams(location.search),embedded=params.get("embedded")==="1",popout=params.get("popout")==="1";const introMode=params.get("intro")==="1";document.body.classList.toggle("embedded",embedded);document.body.classList.toggle("popout",popout);
const byId=id=>document.getElementById(id),focusLayer=byId("focusLayer"),routeLayer=byId("routeLayer"),progress=byId("progress");let index=0,playing=true,timer=0;{factory_init}{audio_init}
stages.forEach((s,i)=>{{const b=document.createElement("button");b.type="button";b.ariaLabel=`Open stage ${{i+1}}: ${{s.label}}`;b.onclick=()=>{{index=i;render()}};progress.append(b)}});
function node(name,attrs){{const n=document.createElementNS("http://www.w3.org/2000/svg",name);Object.entries(attrs).forEach(([k,v])=>n.setAttribute(k,v));return n}}
function completeIntro(){{playing=false;clearTimeout(timer);if("speechSynthesis" in window)speechSynthesis.cancel();if(typeof jazz!=="undefined")jazz.pause();if(window.parent!==window)window.parent.postMessage({{type:"brainzbytes-intro-complete"}},location.origin)}}
function advance(){{if(!playing)return;if(index===stages.length-1){{if(introMode){intro_finish};else{{index=0;render()}}}}else{{index+=1;render(true)}}}}
function schedule(){{clearTimeout(timer);if(playing)timer=setTimeout(advance,4200)}}
function render(announce=false){{const s=stages[index];{factory_render}focusLayer.replaceChildren();routeLayer.replaceChildren();const [x,y,w,h]=s.box;focusLayer.append(node("rect",{{x,y,width:w,height:h,rx:20,class:"focus"}}));if(s.route.length){{const d="M"+s.route.map(p=>p.join(" ")).join(" L");routeLayer.append(node("path",{{d,class:"route"}}))}}byId("stageLabel").textContent=`${{String(index+1).padStart(2,"0")}} · ${{s.label}}`;byId("stageTitle").textContent=s.title;byId("stageCaption").textContent=s.caption;byId("stageCount").textContent=`${{String(index+1).padStart(2,"0")}} / ${{String(stages.length).padStart(2,"0")}}`;[...progress.children].forEach((b,i)=>b.classList.toggle("active",i===index));byId("playPause").textContent=playing?"Pause":"Play";if(announce)speak(s);else schedule()}}
function showOpening(){{index=0;playing=true;{factory_opening}render()}}
function tryIntroMusic(){{if(typeof jazz!=="undefined")jazz.play().catch(()=>{{if(byId("audioGate"))byId("audioGate").hidden=false}})}}
byId("previous").onclick=()=>{{index=(index-1+stages.length)%stages.length;render(true)}};byId("next").onclick=()=>{{index=(index+1)%stages.length;render(true)}};byId("playPause").onclick=()=>{{playing=!playing;render()}};byId("reset").onclick=()=>{{index=0;playing=false;render()}};
{audio_handlers}
byId("popout").textContent=popout?"Back":"Pop out";byId("popout").onclick=()=>{{if(popout){{window.close();setTimeout(()=>{{if(history.length>1)history.back();else location.href="{standalone_fallback}"}},80)}}else window.open("{standalone_fallback}?popout=1","contextweaver-animation","popup,width=1380,height=960,noopener")}};
addEventListener("keydown",e=>{{if(["INPUT","TEXTAREA","BUTTON"].includes(document.activeElement?.tagName))return;if(e.key===" "){{e.preventDefault();byId("playPause").click()}}if(e.key==="ArrowLeft")byId("previous").click();if(e.key==="ArrowRight")byId("next").click();if(e.key==="Home")byId("reset").click();if(e.key==="Escape"&&popout)byId("popout").click()}});
showOpening();
tryIntroMusic();
</script></body></html>"""


def write_visuals(skip_raster: bool = False, overview_only: bool = False, intent_only: bool = False) -> None:
    BRAND.mkdir(parents=True, exist_ok=True)
    DIAGRAMS.mkdir(parents=True, exist_ok=True)

    if skip_raster:
        required = [
            BRAND / "brainzbytes-contextweaver-overview.svg",
            BRAND / "brainzbytes-contextweaver-overview.drawio",
            BRAND / "brainzbytes-contextweaver-overview.html",
            BRAND / "brainzbytes-contextweaver-overview.png",
            BRAND / "brainzbytes-contextweaver-overview.gif",
            DIAGRAMS / "intent-to-evidence-flow.svg",
            DIAGRAMS / "intent-to-evidence-flow.drawio",
            DIAGRAMS / "intent-to-evidence-flow.html",
            DIAGRAMS / "intent-to-evidence-flow.png",
            DIAGRAMS / "intent-to-evidence-flow.gif",
        ]
        missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
        if missing:
            raise FileNotFoundError(
                "Committed rendered visual assets are missing: " + ", ".join(missing)
            )
        print("Using committed angled public visual assets.")
        return

    if intent_only:
        write_intent_visual(skip_raster)
        return

    overview, overview_boxes, overview_routes = overview_svg()
    overview_svg_path = BRAND / "brainzbytes-contextweaver-overview.svg"
    overview_png_path = BRAND / "brainzbytes-contextweaver-overview.png"
    overview_svg_path.write_text(overview, encoding="utf-8")
    (BRAND / "brainzbytes-contextweaver-overview.drawio").write_text(
        drawio(overview, "BrainzBytes ContextWeaver overview", overview_boxes, overview_routes), encoding="utf-8"
    )
    if not skip_raster:
        Image.open(io.BytesIO(base64.b64decode(overview.split("base64,", 1)[1].split('"', 1)[0]))).convert("RGB").save(
            overview_png_path, optimize=True
        )
        (BRAND / "contextweaver-weaving.png").write_bytes(overview_png_path.read_bytes())
        gif_from_master(overview_png_path, BRAND / "brainzbytes-contextweaver-overview.gif", overview_boxes, overview_routes)
    overview_stages = [
        {"label": "Governed intent", "title": "Every system begins with explicit purpose.", "caption": "Goals, constraints, tenant context, and identity enter as governed intent."},
        {"label": "Governance", "title": "Authority is evaluated before execution.", "caption": "Policy, entitlements, guardrails, budgets, and evidence requirements bind the run."},
        {"label": "Studio", "title": "Builders compose approved capabilities.", "caption": "Agents, MCP tools, knowledge, models, and APIs are assembled without rebuilding the platform."},
        {"label": "Registry", "title": "Only signed immutable releases may run.", "caption": "Versioned definitions and evidence create a stable supply chain from authoring to production."},
        {"label": "Orchestrator", "title": "The orchestrator plans and reconciles durable work.", "caption": "It resolves the graph, commits the plan, and coordinates recovery without granting itself authority."},
        {"label": "Agents and MCP", "title": "Bounded workers perform specialized actions.", "caption": "Agents reason while MCP capabilities execute narrow, policy-scoped operations."},
        {"label": "Event mesh", "title": "Commands, retries, and compensation move durably.", "caption": "The event mesh separates services while preserving correlation, leases, and replay."},
        {"label": "Live services", "title": "Approved compositions become scalable services.", "caption": "Portable runtime contracts support deployment, replacement, and migration across Kubernetes platforms."},
        {"label": "Cerebros", "title": "Cerebros understands context and intent.", "caption": "The reasoning plane retrieves evidence, plans bounded work, and interprets outcomes."},
        {"label": "Weave", "title": "Weave coordinates durable workflows.", "caption": "Versioned workflow state, retries, compensation, and human decisions remain explicit and recoverable."},
        {"label": "Loom", "title": "Loom supplies the portable runtime foundation.", "caption": "Kubernetes-native infrastructure keeps governed compositions deployable across environments and clouds."},
        {"label": "Evidence", "title": "Every material action returns proof.", "caption": "Receipts, traces, approvals, audits, and replay complete the governed feedback loop."},
    ]
    (BRAND / "brainzbytes-contextweaver-overview.html").write_text(
        player_html(
            "BrainzBytes × ContextWeaver",
            "Three angled architectural planes show composition, execution, intelligence, and evidence.",
            "brainzbytes-contextweaver-overview.svg?v=20261103-9",
            overview_stages,
            overview_boxes,
            overview_routes,
            "brainzbytes-contextweaver-overview.html",
            "brainzbytes-jazz-loop.wav",
        ),
        encoding="utf-8",
    )
    if overview_only:
        return

    write_intent_visual(skip_raster)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-raster", action="store_true")
    parser.add_argument("--overview-only", action="store_true")
    parser.add_argument("--intent-only", action="store_true")
    args = parser.parse_args()
    write_visuals(args.skip_raster, args.overview_only, args.intent_only)
