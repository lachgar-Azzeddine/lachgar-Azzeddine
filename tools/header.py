"""Draws the GitHub profile header from a real power trace.

Usage: python3 header.py <trace.json> <fonts dir> <out dir>
Writes header-light.svg and header-dark.svg.
"""
import json
import math
import sys

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

trace_file, fonts, out = sys.argv[1:4]
trace = json.load(open(trace_file))

W, H = 1200, 440
LEFT, RIGHT = 48, 1152
TOP, BOTTOM = 236, 392


def instance(path, **axes):
    return instancer.instantiateVariableFont(TTFont(path), axes)


display = instance(f"{fonts}/Archivo.ttf", wght=850, wdth=125)
text_font = instance(f"{fonts}/Archivo.ttf", wght=430, wdth=100)
mono = instance(f"{fonts}/JetBrainsMono.ttf", wght=500)
mono_bold = instance(f"{fonts}/JetBrainsMono.ttf", wght=700)


def text(font, s, size, x, y, tracking=0.0, anchor="start"):
    """Returns (svg path data, width) of s set in font at size, baseline at y."""
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    upm = font["head"].unitsPerEm
    scale = size / upm
    hmtx = font["hmtx"]
    advance = 0.0
    names = []
    for ch in s:
        name = cmap.get(ord(ch), ".notdef")
        names.append(name)
        advance += hmtx[name][0] * scale + tracking
    advance -= tracking
    if anchor == "end":
        x -= advance
    elif anchor == "middle":
        x -= advance / 2
    pen = SVGPathPen(gs, ntos=lambda v: f"{v:.1f}")
    cursor = x
    for name in names:
        gs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, cursor, y)))
        cursor += hmtx[name][0] * scale + tracking
    return pen.getCommands(), advance


total = trace["total"]
tenant = trace["tenant"]
n = len(total)
MAX = 5.5


def px(i):
    return LEFT + (RIGHT - LEFT) * i / (n - 1)


def py(v):
    return BOTTOM - math.sqrt(max(v, 0) / MAX) * (BOTTOM - TOP)


line = "M" + " L".join(f"{px(i):.1f},{py(v):.1f}" for i, v in enumerate(total))
area = line + f" L{RIGHT:.1f},{BOTTOM} L{LEFT:.1f},{BOTTOM} Z"

segments, cur = [], []
for i, v in enumerate(tenant):
    if v is None:
        if cur:
            segments.append(cur)
        cur = []
    else:
        cur.append(f"{px(i):.1f},{py(v):.1f}")
if cur:
    segments.append(cur)
tenant_d = " ".join("M" + " L".join(s) for s in segments if len(s) > 1)

off = [i for i, v in enumerate(tenant) if v is None]
band_x0, band_x1 = px(off[0] - 1), px(off[-1] + 1)

name_d, name_w = text(display, "Azzeddine Lachgar", 86, LEFT - 3, 150, tracking=-2.2)
sub_d, _ = text(text_font, "DevOps engineer. I build Kubernetes platforms that know what they cost.", 25, LEFT, 196)
rec_d, rec_w = text(mono_bold, "REC", 12, LEFT + 16, 52, tracking=1.4)
eyebrow_d, _ = text(mono, "POWER OF MY PLATFORM · 40 H · REAL DATA", 12, LEFT + 16 + rec_w + 14, 52, tracking=1.2)
label_d, label_w = text(mono_bold, "over budget → put to sleep", 12.5, band_x0 - 10, TOP - 10, anchor="end")
label2_d, _ = text(mono, "by a controller I wrote", 12.5, band_x0 - 10, TOP + 8, anchor="end")

ticks = []
for v in (0.5, 1, 2, 5):
    d, _ = text(mono, f"{v:g} W", 10.5, LEFT + 4, py(v) - 5)
    ticks.append((d, py(v)))


def when(i):
    import datetime

    t = datetime.datetime.fromtimestamp(trace["start"] + i * trace["step"], datetime.UTC)
    return t.strftime("%d %b %H:%M")


axis = []
for k, i in enumerate((0, n // 2, n - 1)):
    label = when(i) + (" UTC" if i == n - 1 else "")
    d, _ = text(mono, label, 11, px(i) if k else LEFT, BOTTOM + 26, anchor=("start", "middle", "end")[k])
    axis.append(d)

last_x, last_y = px(n - 1), py(total[-1])

THEMES = {
    "light": dict(paper="#f6f5f1", grid="#e7e4dc", major="#d8d4ca", ink="#111418", muted="#6b7079",
                  charge="#ff5a1f", charge_soft="rgba(255,90,31,0.10)", asleep="rgba(17,20,24,0.07)", asleep_line="#8a8f98"),
    "dark": dict(paper="#0d0f13", grid="#171a20", major="#22262d", ink="#eeece6", muted="#9a9fa8",
                 charge="#ff6a33", charge_soft="rgba(255,106,51,0.13)", asleep="rgba(238,236,230,0.06)", asleep_line="#5b6069"),
}

for theme, c in THEMES.items():
    ticks_svg = "\n".join(
        f'<path d="{d}" fill="{c["muted"]}"/><line x1="{LEFT}" x2="{RIGHT}" y1="{y:.1f}" y2="{y:.1f}" stroke="{c["major"]}" stroke-width="1" stroke-dasharray="2 4"/>'
        for d, y in ticks
    )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Azzeddine Lachgar. DevOps engineer. I build Kubernetes platforms that know what they cost. Behind the name, 40 hours of real power data from his platform, with the moment a tenant went over its energy budget and was put to sleep.">
<title>Azzeddine Lachgar</title>
<defs>
  <pattern id="minor" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="{c["grid"]}" stroke-width="1"/></pattern>
  <pattern id="major" width="100" height="100" patternUnits="userSpaceOnUse"><path d="M100 0H0V100" fill="none" stroke="{c["major"]}" stroke-width="1"/></pattern>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="14"/></clipPath>
</defs>
<style>
  .trace {{ stroke-dasharray: 1; stroke-dashoffset: 1; animation: draw 3.2s cubic-bezier(.45,.05,.25,1) .3s forwards; }}
  .area {{ opacity: 0; animation: show .9s ease 3s forwards; }}
  .tenant {{ opacity: 0; animation: show .9s ease 2.4s forwards; }}
  .event {{ opacity: 0; animation: show .7s ease 1.9s forwards; }}
  .pen {{ opacity: 0; animation: show .3s ease 3.4s forwards, pulse 1.8s ease-in-out 3.7s infinite; transform-origin: {last_x:.1f}px {last_y:.1f}px; }}
  .rec {{ animation: blink 1.6s steps(2, start) infinite; }}
  @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
  @keyframes show {{ to {{ opacity: 1; }} }}
  @keyframes pulse {{ 50% {{ transform: scale(1.7); opacity: .55; }} }}
  @keyframes blink {{ to {{ visibility: hidden; }} }}
  @media (prefers-reduced-motion: reduce) {{
    .trace {{ animation: none; stroke-dashoffset: 0; }}
    .area, .tenant, .event, .pen {{ animation: none; opacity: 1; }}
    .rec {{ animation: none; }}
  }}
</style>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="{c["paper"]}"/>
  <rect width="{W}" height="{H}" fill="url(#minor)"/>
  <rect width="{W}" height="{H}" fill="url(#major)"/>

  <circle class="rec" cx="{LEFT + 5}" cy="48" r="5" fill="{c["charge"]}"/>
  <path d="{rec_d}" fill="{c["charge"]}"/>
  <path d="{eyebrow_d}" fill="{c["muted"]}"/>
  <path d="{name_d}" fill="{c["ink"]}"/>
  <path d="{sub_d}" fill="{c["muted"]}"/>

  {ticks_svg}

  <g class="event">
    <rect x="{band_x0:.1f}" y="{TOP - 30}" width="{band_x1 - band_x0:.1f}" height="{BOTTOM - TOP + 30}" fill="{c["asleep"]}"/>
    <line x1="{band_x0:.1f}" x2="{band_x0:.1f}" y1="{TOP - 30}" y2="{BOTTOM}" stroke="{c["ink"]}" stroke-width="1.5"/>
    <path d="{label_d}" fill="{c["ink"]}"/>
    <path d="{label2_d}" fill="{c["muted"]}"/>
  </g>

  <path class="area" d="{area}" fill="{c["charge_soft"]}"/>
  <path class="tenant" d="{tenant_d}" fill="none" stroke="{c["asleep_line"]}" stroke-width="1.3" stroke-dasharray="4 4"/>
  <path class="trace" d="{line}" pathLength="1" fill="none" stroke="{c["charge"]}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>
  <circle class="pen" cx="{last_x:.1f}" cy="{last_y:.1f}" r="5" fill="{c["charge"]}"/>

  <line x1="{LEFT}" x2="{RIGHT}" y1="{BOTTOM}" y2="{BOTTOM}" stroke="{c["ink"]}" stroke-width="1"/>
  {"".join(f'<path d="{d}" fill="{c["muted"]}"/>' for d in axis)}
</g>
</svg>
"""
    open(f"{out}/header-{theme}.svg", "w").write(svg)
    print(theme, len(svg) // 1024, "KB")
