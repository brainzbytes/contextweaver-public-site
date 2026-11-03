from __future__ import annotations

import argparse
import base64
import html
import json
from pathlib import Path

from PIL import Image, ImageDraw


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
  <linearGradient id="front" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#10291A"/><stop offset="1" stop-color="#06120B"/></linearGradient>
  <linearGradient id="amberFront" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#382B0D"/><stop offset="1" stop-color="#120D03"/></linearGradient>
  <filter id="glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="shadow" x="-50%" y="-50%" width="220%" height="240%"><feGaussianBlur stdDeviation="14"/></filter>
  <pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse" patternTransform="skewX(-24)"><path d="M48 0H0V48" fill="none" stroke="#173623" stroke-width="1"/></pattern>
  <marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="4" orient="auto"><path d="M0 0L11 4L0 8Z" fill="{LIME}"/></marker>
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
    .route{{fill:none;stroke:{LIME};stroke-width:4;stroke-linecap:round;stroke-linejoin:round;marker-end:url(#arrow);filter:url(#glow)}}
  </style>
</defs>
<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bg)"/><rect y="105" width="{WIDTH}" height="{HEIGHT-105}" fill="url(#grid)" opacity=".28"/>
"""


def platform(x: int, y: int, width: int, depth: int, label: str) -> str:
    p1 = (x, y)
    p2 = (x + width, y + 104)
    p3 = (x + width + depth, y + 48)
    p4 = (x + depth, y - 56)
    top = " ".join(f"{px},{py}" for px, py in (p1, p2, p3, p4))
    bottom = " ".join(
        f"{px},{py}" for px, py in ((p1[0], p1[1] + 18), (p2[0], p2[1] + 18), (p3[0], p3[1] + 66), (p4[0], p4[1] + 66))
    )
    return f"""<g>
<polygon points="{bottom}" fill="#020704" stroke="#16733B" stroke-width="2" opacity=".9"/>
<polygon points="{top}" fill="url(#plane)" stroke="{GREEN}" stroke-width="2" opacity=".96" filter="url(#glow)"/>
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
) -> tuple[str, tuple[int, int, int, int]]:
    top_dx, top_dy, side = 18, -13, 18
    front_fill = "url(#amberFront)" if accent == AMBER else "url(#front)"
    svg = f"""<g id="{ident}">
<ellipse cx="{x+width/2+14}" cy="{y+height+18}" rx="{width*.55}" ry="17" fill="{accent}" opacity=".18" filter="url(#shadow)"/>
<polygon points="{x},{y} {x+top_dx},{y+top_dy} {x+width+top_dx},{y+top_dy} {x+width},{y}" fill="#163B22" stroke="{accent}" stroke-width="2"/>
<polygon points="{x+width},{y} {x+width+side},{y+top_dy} {x+width+side},{y+height+top_dy} {x+width},{y+height}" fill="#06100A" stroke="{accent}" stroke-width="2"/>
<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="13" fill="{front_fill}" stroke="{accent}" stroke-width="2.5" filter="url(#glow)"/>
<circle cx="{x+18}" cy="{y+18}" r="17" fill="{LIME}" stroke="#E8FFB8" stroke-width="2" filter="url(#glow)"/><text x="{x+18}" y="{y+24}" class="number">{number}</text>
<text x="{x+width/2}" y="{y+height/2-2}" class="block-title">{html.escape(title)}</text>
<text x="{x+width/2}" y="{y+height/2+25}" class="block-copy">{html.escape(copy)}</text>
</g>"""
    return svg, (x - 8, y - 22, width + 36, height + 43)


def route(points: list[tuple[int, int]]) -> tuple[str, list[tuple[int, int]]]:
    d = "M" + " L".join(f"{x} {y}" for x, y in points)
    return f'<path d="{d}" class="route"/>', points


def overview_svg() -> tuple[str, list[tuple[int, int, int, int]], list[list[tuple[int, int]]]]:
    out = [svg_header("BrainzBytes and ContextWeaver", "A three-quarter architectural view of governed composition, execution, and evidence.")]
    out.append('<text x="70" y="70" class="eyebrow">CONTEXTWEAVER BY BRAINZBYTES</text>')
    out.append('<text x="70" y="125" class="title">Build governed AI systems from intent to evidence</text>')
    out.append('<text x="70" y="160" class="subtitle">Compose once. Govern every action. Deploy on any Kubernetes platform.</text>')
    out.extend(
        [
            platform(85, 300, 1120, 220, "COMPOSE + GOVERN"),
            platform(155, 565, 1120, 220, "ORCHESTRATE + EXECUTE"),
            platform(225, 830, 1120, 220, "INTELLIGENCE + EVIDENCE"),
        ]
    )
    specs = [
        ("intent", 1, 165, 220, 220, 105, "Intent", "Goals + constraints", GREEN),
        ("governance", 2, 440, 250, 220, 105, "Governance", "Identity + policy", AMBER),
        ("studio", 3, 715, 280, 220, 105, "Agent + MCP Studio", "Build + validate", GREEN),
        ("registry", 4, 990, 310, 220, 105, "Registry", "Signed releases", GREEN),
        ("orchestrator", 5, 235, 485, 220, 105, "Orchestrator", "Plan + reconcile", GREEN),
        ("runtime", 6, 510, 515, 220, 105, "Agents + MCP", "Bounded execution", GREEN),
        ("mesh", 7, 785, 545, 220, 105, "Event Mesh", "Commands + retries", AMBER),
        ("services", 8, 1060, 575, 220, 105, "Live Services", "Scale + replace", GREEN),
        ("cerebros", 9, 305, 750, 220, 105, "Cerebros", "Understand + reason", GREEN),
        ("weave", 10, 580, 780, 220, 105, "Weave", "Durable workflows", GREEN),
        ("loom", 11, 855, 810, 220, 105, "Loom", "Portable foundation", GREEN),
        ("evidence", 12, 1130, 840, 220, 105, "Evidence", "Receipts + replay", AMBER),
    ]
    boxes = []
    for spec in specs:
        cell, box = block(*spec)
        out.append(cell)
        boxes.append(box)
    paths = [
        [(385, 273), (440, 280)],
        [(660, 303), (715, 310)],
        [(935, 333), (990, 340)],
        [(1100, 415), (1100, 455), (345, 455), (345, 485)],
        [(455, 538), (510, 545)],
        [(730, 568), (785, 575)],
        [(1005, 598), (1060, 605)],
        [(1170, 680), (1170, 720), (415, 720), (415, 750)],
        [(525, 803), (580, 810)],
        [(800, 833), (855, 840)],
        [(1075, 863), (1130, 870)],
    ]
    route_points = []
    for pts in paths:
        cell, saved = route(pts)
        out.append(cell)
        route_points.append(saved)
    out.append('<text x="70" y="965" class="subtitle">CEREBROS understands  ·  WEAVE coordinates  ·  LOOM runs portably  ·  EVIDENCE proves every material action</text>')
    out.append("</svg>")
    return "".join(out), boxes, route_points


def intent_svg() -> tuple[str, list[tuple[int, int, int, int]], list[list[tuple[int, int]]]]:
    out = [svg_header("Intent to governed evidence", "Seven governed stages arranged across three receding architectural planes.")]
    out.append('<text x="70" y="70" class="eyebrow">CONTEXTWEAVER GOVERNED RUN</text>')
    out.append('<text x="70" y="125" class="title">Intent to governed evidence</text>')
    out.append('<text x="70" y="160" class="subtitle">One durable, authorized path from request to proof.</text>')
    out.extend(
        [
            platform(105, 335, 990, 235, "ADMIT"),
            platform(210, 600, 900, 235, "EXECUTE"),
            platform(315, 850, 790, 235, "VERIFY + DELIVER"),
        ]
    )
    specs = [
        ("intent", 1, 185, 245, 230, 112, "Intent", "Request + purpose", GREEN),
        ("resolve", 2, 495, 278, 230, 112, "Resolve", "Service + workflow", GREEN),
        ("authorize", 3, 805, 311, 230, 112, "Authorize", "Identity + policy", AMBER),
        ("commit", 4, 315, 510, 260, 112, "Commit", "Plan + task + outbox", GREEN),
        ("execute", 5, 685, 550, 260, 112, "Execute", "Agents + MCP + RAG", GREEN),
        ("verify", 6, 440, 760, 270, 112, "Verify", "Approval + contracts", AMBER),
        ("deliver", 7, 850, 805, 270, 112, "Deliver", "Result + evidence", GREEN),
    ]
    boxes = []
    for spec in specs:
        cell, box = block(*spec)
        out.append(cell)
        boxes.append(box)
    paths = [
        [(415, 301), (495, 315)],
        [(725, 334), (805, 348)],
        [(920, 423), (920, 465), (445, 465), (445, 510)],
        [(575, 566), (685, 590)],
        [(815, 662), (815, 715), (575, 715), (575, 760)],
        [(710, 816), (850, 850)],
    ]
    route_points = []
    for pts in paths:
        cell, saved = route(pts)
        out.append(cell)
        route_points.append(saved)
    out.append('<rect x="1130" y="235" width="360" height="178" rx="20" fill="#07150D" stroke="#2D7A45" stroke-width="2"/>')
    out.append('<text x="1160" y="275" class="plane-label">APPLIES AT EVERY STAGE</text>')
    for index, label in enumerate(("IDENTITY + ENTITLEMENTS", "DURABLE STATE + OUTBOX", "AUDIT + TELEMETRY", "RECEIPTS + REPLAY")):
        out.append(f'<text x="1160" y="{310+index*28}" class="side-copy">{label}</text>')
    out.append("</svg>")
    return "".join(out), boxes, route_points


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
    audio_init = (
        """const jazz=byId("jazz");let audioStarted=false,musicEnabled=true,narrationEnabled=true,narratorVoice=null,voiceLoadPromise=null;jazz.volume=.2;
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
  if(!audioStarted||!narrationEnabled||!("speechSynthesis" in window))return;
  clearTimeout(timer);speechSynthesis.cancel();const voice=await waitForNarrator(),utterance=new SpeechSynthesisUtterance(stage.title+". "+stage.caption);
  if(voice)utterance.voice=voice;utterance.lang=voice?.lang||"en-US";utterance.rate=.96;utterance.pitch=1.02;
  utterance.onstart=()=>{jazz.volume=musicEnabled?.07:0};utterance.onend=()=>{jazz.volume=musicEnabled?.2:0;timer=setTimeout(advance,900)};utterance.onerror=()=>{jazz.volume=musicEnabled?.2:0;schedule()};
  speechSynthesis.resume();speechSynthesis.speak(utterance)
}"""
        if audio_file
        else "function speak(){}"
    )
    audio_handlers = (
        'async function beginAudio(){audioStarted=true;byId("audioGate").hidden=true;if("speechSynthesis" in window)speechSynthesis.resume();'
        'if(musicEnabled){try{await jazz.play()}catch{musicEnabled=false;byId("music").textContent="Music off"}}speak(stages[index]);return true};'
        'window.unlockIntroAudio=()=>beginAudio();window.isIntroAudioUnlocked=()=>audioStarted;'
        'byId("beginStory").onclick=beginAudio;'
        'byId("music").onclick=async()=>{musicEnabled=!musicEnabled;byId("music").ariaPressed=String(musicEnabled);'
        'byId("music").textContent=musicEnabled?"Music on":"Music off";if(musicEnabled){audioStarted=true;byId("audioGate").hidden=true;'
        'try{await jazz.play()}catch{musicEnabled=false}}else jazz.pause()};'
        'byId("narration").onclick=()=>{narrationEnabled=!narrationEnabled;byId("narration").ariaPressed=String(narrationEnabled);'
        'byId("narration").textContent=narrationEnabled?"Narration on":"Narration off";if(narrationEnabled){audioStarted=true;'
        'byId("audioGate").hidden=true;speak(stages[index])}else speechSynthesis.cancel()};'
        'addEventListener("pointerdown",event=>{if(!event.target.closest("button,a")&&!audioStarted)beginAudio()},{capture:true});'
        'addEventListener("pagehide",()=>{speechSynthesis.cancel();jazz.pause()});'
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
.player{{width:min(1320px,100%);border:1px solid var(--line);border-radius:24px;overflow:hidden;background:var(--panel);box-shadow:0 24px 80px #0009}}
.topbar{{display:flex;align-items:center;justify-content:space-between;gap:18px;padding:13px 17px;border-bottom:1px solid var(--line)}}.topbar strong{{font-size:13px}}.topbar div{{display:flex;gap:12px}}.topbar span{{color:var(--muted);font-size:10px;font-weight:800;letter-spacing:.12em;text-transform:uppercase}}
.canvas{{position:relative;aspect-ratio:8/5;background:#020704;overflow:hidden}}.canvas>img{{display:block;width:100%;height:100%;object-fit:contain}}
.overlay{{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}}.focus{{fill:#a8ff3e12;stroke:var(--lime);stroke-width:5;vector-effect:non-scaling-stroke;filter:url(#glow)}}.route{{fill:none;stroke:var(--lime);stroke-width:6;stroke-linecap:round;stroke-linejoin:round;vector-effect:non-scaling-stroke;stroke-dasharray:14 11;filter:url(#glow);animation:flow 1.1s linear infinite}}
@keyframes flow{{to{{stroke-dashoffset:-50}}}}.caption{{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:18px;align-items:center;min-height:108px;padding:16px 18px;border-top:1px solid var(--line);background:linear-gradient(135deg,var(--surface),var(--panel))}}.caption-label{{margin:0 0 5px;color:var(--lime);font-size:9px;font-weight:900;letter-spacing:.16em;text-transform:uppercase}}.caption h1{{margin:0;font-size:clamp(17px,2vw,25px)}}.caption p:last-child{{margin:6px 0 0;color:var(--muted);font-size:12px;line-height:1.45}}
.audio-gate{{position:absolute;inset:0;display:grid;place-items:center;background:linear-gradient(#050b0812,#050b08b8)}}.audio-gate[hidden]{{display:none}}.audio-gate button{{display:grid;gap:4px;min-width:210px;padding:14px 18px;border:1px solid var(--lime);border-radius:12px;background:#102c1d;color:var(--ink);font-weight:850;cursor:pointer}}.audio-gate small{{color:#b8cabd;font-size:10px}}
.controls{{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:6px}}.controls button{{min-height:35px;padding:0 11px;border:1px solid #315b3b;border-radius:8px;background:#0c1810;color:#d4e4d7;font-size:10px;font-weight:800;cursor:pointer}}.controls button:hover,.controls button:focus-visible{{border-color:var(--lime);color:var(--ink);outline:none}}.controls .primary{{border-color:var(--lime);background:var(--lime);color:#061008}}
.progress{{display:grid;grid-template-columns:repeat({len(stages)},1fr);gap:4px;padding:0 18px 14px}}.progress button{{height:4px;padding:0;border:0;border-radius:99px;background:#244a2d;cursor:pointer}}.progress button.active{{background:var(--lime);box-shadow:0 0 12px #a8ff3e88}}
body.embedded{{padding:0}}body.embedded .player{{width:100%;border:0;border-radius:0;box-shadow:none}}body.popout{{padding:24px}}
@media(max-width:760px){{.caption{{grid-template-columns:1fr}}.controls{{justify-content:flex-start}}.controls button{{flex:1 1 auto}}.topbar span{{display:none}}}}
@media(prefers-reduced-motion:reduce){{*,*::before,*::after{{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}}}
</style></head><body>
<main class="player" aria-label="{html.escape(title)}">
<header class="topbar"><strong>{html.escape(title)}</strong><div><span id="voiceName"></span><span id="stageCount">01 / {len(stages):02d}</span></div></header>
<section class="canvas"><img src="{svg_name}" alt="{html.escape(subtitle)}"><svg class="overlay" viewBox="0 0 {WIDTH} {HEIGHT}" aria-hidden="true"><defs><filter id="glow"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><g id="focusLayer"></g><g id="routeLayer"></g></svg>{audio_gate}</section>
<section class="caption" aria-live="polite"><div><p class="caption-label" id="stageLabel"></p><h1 id="stageTitle"></h1><p id="stageCaption"></p></div><div class="controls"><button id="previous">Previous</button><button id="playPause" class="primary">Pause</button><button id="next">Next</button><button id="reset">Reset</button>{audio_controls}<button id="popout">Pop out</button></div></section>
<nav class="progress" id="progress" aria-label="Animation stages"></nav>{audio_element}</main>
<script>
const stages={data};const params=new URLSearchParams(location.search),embedded=params.get("embedded")==="1",popout=params.get("popout")==="1";const introMode=params.get("intro")==="1";document.body.classList.toggle("embedded",embedded);document.body.classList.toggle("popout",popout);
const byId=id=>document.getElementById(id),focusLayer=byId("focusLayer"),routeLayer=byId("routeLayer"),progress=byId("progress");let index=0,playing=true,timer=0;{audio_init}
stages.forEach((s,i)=>{{const b=document.createElement("button");b.type="button";b.ariaLabel=`Open stage ${{i+1}}: ${{s.label}}`;b.onclick=()=>{{index=i;render()}};progress.append(b)}});
function node(name,attrs){{const n=document.createElementNS("http://www.w3.org/2000/svg",name);Object.entries(attrs).forEach(([k,v])=>n.setAttribute(k,v));return n}}
function completeIntro(){{playing=false;clearTimeout(timer);if("speechSynthesis" in window)speechSynthesis.cancel();if(typeof jazz!=="undefined")jazz.pause();if(window.parent!==window)window.parent.postMessage({{type:"brainzbytes-intro-complete"}},location.origin)}}
function advance(){{if(!playing)return;if(index===stages.length-1){{if(introMode)completeIntro();else{{index=0;render()}}}}else{{index+=1;render(true)}}}}
function schedule(){{clearTimeout(timer);if(playing)timer=setTimeout(advance,4200)}}
function render(announce=false){{const s=stages[index];focusLayer.replaceChildren();routeLayer.replaceChildren();const [x,y,w,h]=s.box;focusLayer.append(node("rect",{{x,y,width:w,height:h,rx:20,class:"focus"}}));if(s.route.length){{const d="M"+s.route.map(p=>p.join(" ")).join(" L");routeLayer.append(node("path",{{d,class:"route"}}))}}byId("stageLabel").textContent=`${{String(index+1).padStart(2,"0")}} · ${{s.label}}`;byId("stageTitle").textContent=s.title;byId("stageCaption").textContent=s.caption;byId("stageCount").textContent=`${{String(index+1).padStart(2,"0")}} / ${{String(stages.length).padStart(2,"0")}}`;[...progress.children].forEach((b,i)=>b.classList.toggle("active",i===index));byId("playPause").textContent=playing?"Pause":"Play";if(announce)speak(s);else schedule()}}
function showOpening(){{index=0;playing=true;render()}}
function tryIntroMusic(){{if(typeof jazz!=="undefined")jazz.play().catch(()=>{{if(byId("audioGate"))byId("audioGate").hidden=false}})}}
byId("previous").onclick=()=>{{index=(index-1+stages.length)%stages.length;render(true)}};byId("next").onclick=()=>{{index=(index+1)%stages.length;render(true)}};byId("playPause").onclick=()=>{{playing=!playing;render()}};byId("reset").onclick=()=>{{index=0;playing=false;render()}};
{audio_handlers}
byId("popout").textContent=popout?"Back":"Pop out";byId("popout").onclick=()=>{{if(popout){{window.close();setTimeout(()=>{{if(history.length>1)history.back();else location.href="{standalone_fallback}"}},80)}}else window.open("{standalone_fallback}?popout=1","contextweaver-animation","popup,width=1380,height=960,noopener")}};
addEventListener("keydown",e=>{{if(["INPUT","TEXTAREA","BUTTON"].includes(document.activeElement?.tagName))return;if(e.key===" "){{e.preventDefault();byId("playPause").click()}}if(e.key==="ArrowLeft")byId("previous").click();if(e.key==="ArrowRight")byId("next").click();if(e.key==="Home")byId("reset").click();if(e.key==="Escape"&&popout)byId("popout").click()}});
showOpening();
tryIntroMusic();
</script></body></html>"""


def write_visuals(skip_raster: bool = False) -> None:
    BRAND.mkdir(parents=True, exist_ok=True)
    DIAGRAMS.mkdir(parents=True, exist_ok=True)

    overview, overview_boxes, overview_routes = overview_svg()
    overview_svg_path = BRAND / "brainzbytes-contextweaver-overview.svg"
    overview_png_path = BRAND / "brainzbytes-contextweaver-overview.png"
    overview_svg_path.write_text(overview, encoding="utf-8")
    (BRAND / "brainzbytes-contextweaver-overview.drawio").write_text(
        drawio(overview, "BrainzBytes ContextWeaver overview", overview_boxes, overview_routes), encoding="utf-8"
    )
    if not skip_raster:
        render_png(overview_svg_path, overview_png_path)
        (BRAND / "contextweaver-weaving.png").write_bytes(overview_png_path.read_bytes())
        gif_from_master(overview_png_path, BRAND / "brainzbytes-contextweaver-overview.gif", overview_boxes[:10], overview_routes)
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
        {"label": "Evidence", "title": "Every material action returns proof.", "caption": "Receipts, traces, approvals, audits, and replay complete the governed feedback loop."},
    ]
    (BRAND / "brainzbytes-contextweaver-overview.html").write_text(
        player_html(
            "BrainzBytes × ContextWeaver",
            "Three angled architectural planes show composition, execution, intelligence, and evidence.",
            "brainzbytes-contextweaver-overview.svg",
            overview_stages,
            overview_boxes[:10],
            overview_routes,
            "brainzbytes-contextweaver-overview.html",
            "brainzbytes-jazz-loop.wav",
        ),
        encoding="utf-8",
    )

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
            "intent-to-evidence-flow.svg",
            intent_stages,
            intent_boxes,
            intent_routes,
            "intent-to-evidence-flow.html",
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-raster", action="store_true")
    write_visuals(parser.parse_args().skip_raster)
