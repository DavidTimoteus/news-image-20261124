#!/usr/bin/env python3
"""Render the v3 front page for make.fun news-image-20261124 — broadsheet redesign.

Editorial broadsheet language (after rank 1 @gentle-koala-36, 851.588):
cream paper + ink + one muted red; serif masthead and headlines; hairline
rules; no boxes, no navy bands, no colour chips; data maps as heroes;
small flat single-colour icons for cards. 1024x1024, Pillow only.
Deterministic: no randomness, no clock, no network.
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# --- palette: cream + ink + one red (mono-color discipline) ---
PAPER = (245, 240, 225)
PANEL = (252, 250, 242)
INK = (26, 26, 26)
RED = (166, 25, 46)          # the only accent; used sparingly
GREY = (96, 92, 84)
HAIR = (190, 182, 164)       # hairline rules
LINE = (203, 196, 178)
SEA = (221, 231, 234)
LAND = (230, 217, 184)
LAND_LINE = (185, 168, 127)
# muted region colours: only as 2px top rules, icon ink and map dots
REGION = {
    "EUROPE": (51, 87, 122), "ASIA": (107, 78, 142),
    "MIDDLE EAST": (140, 47, 47), "AMERICAS": (138, 109, 47),
    "AFRICA": (78, 122, 78), "OCEANIA": (62, 122, 122),
    "GLOBAL": (90, 90, 90),
}
# icon ink per card (single muted colour each)
ICON_COL = {
    "missile": (140, 47, 47), "scales": (51, 87, 122),
    "globe": (78, 122, 78), "eu": (138, 109, 47),
    "fire": (140, 47, 47), "awacs": (51, 87, 122),
    "quake": (120, 90, 60), "flag": (78, 122, 78),
    "talks": (62, 122, 122), "chip": (78, 122, 78),
}

F = "/usr/share/fonts/truetype"


def _font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(F + "/noto/NotoSerif-Regular.ttf", size)


def serif_black(size):
    return _font(F + "/noto/NotoSerif-Black.ttf", size)


def serif_b(size):
    return _font(F + "/noto/NotoSerif-Bold.ttf", size)


def serif(size):
    return _font(F + "/noto/NotoSerif-Regular.ttf", size)


def serif_i(size):
    return _font(F + "/noto/NotoSerif-Italic.ttf", size)


def sans_b(size):
    return _font(F + "/dejavu/DejaVuSans-Bold.ttf", size)


def sans(size):
    return _font(F + "/dejavu/DejaVuSans.ttf", size)


def wrap(d, text, fnt, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill, leading=None):
    lh = leading if leading is not None else int(fnt.size * 1.22)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def hline(d, x0, x1, y, width=1, fill=HAIR):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def dashed(d, p0, p1, fill, width=1, dash=5, gap=4):
    x0, y0 = p0
    x1, y1 = p1
    length = math.hypot(x1 - x0, y1 - y0)
    if length == 0:
        return
    ux, uy = (x1 - x0) / length, (y1 - y0) / length
    t = 0.0
    while t < length:
        t2 = min(t + dash, length)
        d.line([(x0 + ux * t, y0 + uy * t), (x0 + ux * t2, y0 + uy * t2)],
               fill=fill, width=width)
        t = t2 + gap


def centred(d, cx, y, text, fnt, fill):
    tw = d.textlength(text, font=fnt)
    d.text((cx - tw / 2, y), text, font=fnt, fill=fill)
    return tw


# --- story data: 35 stories, all happened / first reported Tue 24 Nov 2026 ---
# (facts, dates and labels unchanged from SOURCES.md; only the visual
# language changed. Lead is Sanofi: announced Paris Tue 24 Nov 06:30 UTC.)
HEROES = [
    dict(n=1, city="PARIS", tag="PHARMA \u00b7 DEALS", label="CONFIRMED",
         region="EUROPE", art="sanofi",
         head="Sanofi buys Insmed for $41bn",
         body="Sanofi buys Insmed for $41bn cash at $175 a share \u2014 its biggest deal in 20 years.",
         src="Principia \u00b7 Sanofi"),
    dict(n=2, city="HORMUZ", tag="WAR \u00b7 ENERGY", label="ONGOING",
         region="MIDDLE EAST", art="hormuz",
         head="Iran war deepens: tankers ablaze",
         body="Three tankers catch fire on mines in Hormuz; Iran rules out talks until the US meets seven conditions.",
         src="One Turn \u00b7 Horizon"),
    dict(n=3, city="BENGHAZI", tag="WAR \u00b7 SEA", label="CLAIM",
         region="AFRICA", art="merkury",
         head="UN probe after Ukraine sinks warship",
         body="Seven naval drones sank the corvette Merkury, Kyiv says; Libya demands a UN inquiry and answers.",
         src="One Turn \u00b7 Horizon \u00b7 Guardian"),
]

CARDS = [
    dict(n=4, city="MOSCOW", tag="WAR \u00b7 NUCLEAR", label="OFFICIAL",
         region="EUROPE", art="missile",
         head="Russia warns of preventive nuclear attack",
         body="Medvedev threatens a \u2018preventive nuclear attack\u2019; NATO vows a reply.",
         src="Principia \u00b7 10 Things"),
    dict(n=5, city="THE HAGUE", tag="JUSTICE", label="OFFICIAL",
         region="EUROPE", art="scales",
         head="14 nations back Rohingya ruling",
         body="UK, Spain, Canada and 11 more back the ICJ ruling; UK sanctions generals.",
         src="Horizon \u00b7 Principia"),
    dict(n=6, city="ANTALYA", tag="CLIMATE", label="REPORTED",
         region="EUROPE", art="globe",
         head="COP31 post-mortem: the failure",
         body="The first COP without a deal: no fossil fuels named, funding split.",
         src="iqmia \u00b7 Principia"),
    dict(n=7, city="BRUSSELS", tag="EUROPE \u00b7 SANCTIONS", label="OFFICIAL",
         region="EUROPE", art="eu",
         head="EU proposes 22nd sanctions package",
         body="Brussels proposes a 22nd round vs Russia, incl. a sports ban.",
         src="One Turn \u00b7 Horizon"),
    dict(n=8, city="SERANG", tag="DISASTER", label="REPORTED",
         region="ASIA", art="fire",
         head="Factory fire: death toll hits 26",
         body="Toll confirmed Tuesday after the Saturday blaze; 8 missing, probe under way.",
         src="One Turn \u00b7 AP"),
    dict(n=9, city="POLAND", tag="NATO \u00b7 DEFENCE", label="OFFICIAL",
         region="EUROPE", art="awacs",
         head="NATO sends AWACS to Poland",
         body="AWACS jets fly to Poland after a missile falls; defences on alert.",
         src="Horizon"),
    dict(n=10, city="NEPAL", tag="DISASTER", label="CONFIRMED",
         region="ASIA", art="quake",
         head="Nepal quake, 5.6, near China border",
         body="A 5.6 quake strikes near the China border at 07:17; checks under way.",
         src="Horizon \u00b7 The Hindu"),
    dict(n=11, city="DHAKA", tag="POLITICS", label="CLAIM",
         region="ASIA", art="flag",
         head="Sheikh Hasina plans return Dec 16",
         body="Hasina plans to return to Bangladesh on Dec 16, her party says.",
         src="One Turn"),
    dict(n=12, city="DOHA", tag="DIPLOMACY", label="REPORTED",
         region="MIDDLE EAST", art="talks",
         head="Qatar PM seeks to revive US\u2013Iran talks",
         body="Doha pushes to restart US\u2013Iran talks as the Hormuz war deepens.",
         src="One Turn"),
    dict(n=13, city="NEW YORK", tag="MARKETS \u00b7 TECH", label="CONFIRMED",
         region="AMERICAS", art="chip",
         head="Nvidia jumps 31% on Wall Street",
         body="Shares jump 31% in a day; S&P 500 up 4.73%, Nasdaq 6.51% \u2014 the best day in years.",
         src="One Turn \u00b7 Horizon"),
]

ALSO = [
    (14, "Houthis: Saudi strikes kill 25 in Yemen", "Horizon"),
    (15, "Gaza: Oxfam calls territory a \u201ctoxic land\u201d", "Horizon"),
    (16, "Iran flogs singer Parastoo Ahmadi 74 lashes", "Horizon"),
    (17, "Gaza meningitis alert as strikes kill several", "One Turn"),
    (18, "Spain amnesties Carles Puigdemont", "One Turn"),
    (19, "Estonia closes border with Russia", "Horizon"),
    (20, "Zaporizhzhia night attacks kill 2, wound 30+", "Horizon"),
    (21, "Nepal PM visits India; India pledges \u20ac1.4bn", "One Turn"),
    (22, "China opens Tiangong to foreign astronaut", "One Turn \u00b7 Horizon"),
    (23, "S. Korea scrambles jets as Russian planes near", "Horizon"),
    (24, "Tajikistan begins withdrawing from the ICC", "One Turn"),
    (25, "US loses measles elimination status after 25 years", "Principia"),
    (26, "Pennsylvania measles epidemic claims 9th death", "Horizon"),
    (27, "States sue Musk firms over Grok sex images", "Principia"),
    (28, "US blacklists Megaspeed over Nvidia spy case", "One Turn"),
    (29, "Australia: tech fines up to 5% of global revenue", "Principia"),
    (30, "Webb: star layers merged before supernova", "One Turn"),
    (31, "CrowdStrike\u2013Zscaler $44bn: shares slide 9%", "One Turn"),
    (32, "S. Africa cities tighten water curbs", "Africanews"),
    (33, "Borno school enrolment nearly doubles", "Al Jazeera"),
    (34, "Solomons to drop China pact for Australia", "SMH \u00b7 Reuters"),
    (35, "England thrash Australia in T20, Gold Coast", "Reuters"),
]

NUMBERS = [
    ("+31%", "Nvidia jump"),
    ("26", "Serang fire dead"),
    ("74", "lashes: Ahmadi"),
    ("$41bn", "Sanofi deal"),
    ("5.6", "Nepal quake"),
    ("14", "nations back ICJ"),
]

TIMELINE = [
    ("01:32", "Nepal quake"),
    ("03:41", "Quake reported"),
    ("06:30", "Sanofi $41bn deal"),
    ("09:09", "Insmed +14%"),
    ("14:50", "Serang toll: 26"),
    ("21:00", "Nvidia +31%"),
]

REGIONS = [
    ("EUROPE", 9), ("ASIA", 7), ("MIDDLE EAST", 6), ("AMERICAS", 6),
    ("AFRICA", 3), ("OCEANIA", 3), ("GLOBAL", 1),
]

PIN_REGION = {
    1: "EUROPE", 2: "MIDDLE EAST", 3: "AFRICA", 4: "EUROPE",
    5: "EUROPE", 6: "EUROPE", 7: "EUROPE", 8: "ASIA", 9: "EUROPE",
    10: "ASIA", 11: "ASIA", 12: "MIDDLE EAST", 13: "AMERICAS",
}
# lon/lat of the 13 featured stories (true city coords; map is schematic).
PINS = {
    1: (2, 49), 2: (56, 26), 3: (20, 32), 4: (37, 56), 5: (4, 52),
    6: (31, 37), 7: (4, 51), 8: (106, -6), 9: (19, 52), 10: (84, 28),
    11: (90, 24), 12: (51, 25), 13: (-74, 41),
}
# px nudges so the Europe / Gulf / Bengal clusters stay readable with
# 10px dots, no leader lines (schematic map; true cities named on cards)
PIN_NUDGE = {1: (-11, 7), 5: (7, -9), 7: (9, 7), 9: (-3, -5),
             4: (4, 0), 6: (0, 4), 2: (7, -5), 12: (-8, 5),
             10: (-5, -5), 11: (6, 5)}

CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-65, 60),
     (-55, 47), (-70, 42), (-80, 32), (-97, 26), (-105, 20), (-115, 30),
     (-125, 40), (-150, 60), (-168, 66)],
    [(-80, 10), (-60, 5), (-35, -8), (-40, -20), (-55, -35), (-70, -50),
     (-75, -30), (-80, -15), (-80, 10)],
    [(-10, 36), (0, 44), (10, 45), (20, 45), (28, 40), (30, 36), (23, 40),
     (18, 55), (10, 58), (5, 60), (-5, 58), (-10, 50), (-10, 36)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
     (43, 12), (51, 10), (40, -5), (35, -20), (20, -35), (15, -30),
     (12, -18), (9, 0), (-8, 5), (-17, 15)],
    [(30, 36), (40, 36), (48, 30), (57, 26), (60, 25), (66, 25), (72, 20),
     (77, 8), (80, 13), (88, 22), (92, 16), (97, 10), (100, 8), (103, 1),
     (104, 9), (109, 15), (106, 20), (108, 18), (114, 22), (120, 25),
     (122, 30), (127, 35), (130, 42), (135, 44), (140, 40), (142, 50),
     (158, 60), (170, 66), (178, 65), (170, 60), (160, 55), (150, 60),
     (140, 70), (130, 72), (110, 74), (100, 76), (80, 73), (70, 72),
     (60, 70), (50, 68), (45, 65), (40, 60), (35, 55), (30, 50), (30, 45),
     (30, 36)],
    [(113, -22), (114, -30), (115, -35), (125, -32), (130, -32), (135, -35),
     (140, -38), (145, -38), (150, -37), (153, -27), (150, -22), (146, -19),
     (142, -11), (136, -12), (132, -11), (126, -14), (122, -17), (118, -20),
     (113, -22)],
]

# --- flat single-colour icons (rank 1: small label-icons, not scenes) ---
# Each icon draws inside a s x s box at (x, y) in one muted colour.

def _star4(d, cx, cy, r, fill):
    d.polygon([(cx, cy - r), (cx + r * 0.30, cy - r * 0.30), (cx + r, cy),
               (cx + r * 0.30, cy + r * 0.30), (cx, cy + r),
               (cx - r * 0.30, cy + r * 0.30), (cx - r, cy),
               (cx - r * 0.30, cy - r * 0.30)], fill=fill)


def _flame(d, cx, base, s, fill):
    d.polygon([(cx - s * 0.45, base), (cx - s * 0.18, base - s * 0.55),
               (cx, base - s * 0.30), (cx + s * 0.16, base - s * 0.75),
               (cx + s * 0.45, base)], fill=fill)


def icon_missile(d, x, y, s, col):
    # proper missile, nose up-right: thick body, nose cone, tail fins, flame
    ux, uy = 0.7071, -0.7071
    nx, ny = uy, -ux  # normal
    cx, cy = x + s * 0.5, y + s * 0.52
    tail = (cx - ux * s * 0.34, cy - uy * s * 0.34)
    nose = (cx + ux * s * 0.40, cy + uy * s * 0.40)
    w = s * 0.075
    d.polygon([(tail[0] + nx * w, tail[1] + ny * w),
               (nose[0] - ux * s * 0.10 + nx * w, nose[1] - uy * s * 0.10 + ny * w),
               (nose[0] - ux * s * 0.10 - nx * w, nose[1] - uy * s * 0.10 - ny * w),
               (tail[0] - nx * w, tail[1] - ny * w)], fill=col)
    d.polygon([(nose[0] - ux * s * 0.10 + nx * w, nose[1] - uy * s * 0.10 + ny * w),
               nose,
               (nose[0] - ux * s * 0.10 - nx * w, nose[1] - uy * s * 0.10 - ny * w)],
              fill=col)
    # tail fins (two triangles, both sides of the body)
    f1 = (tail[0] + nx * w, tail[1] + ny * w)
    d.polygon([f1, (f1[0] - ux * s * 0.16 + nx * s * 0.22,
                    f1[1] - uy * s * 0.16 + ny * s * 0.22),
               (f1[0] - ux * s * 0.05, f1[1] - uy * s * 0.05)], fill=col)
    f2 = (tail[0] - nx * w, tail[1] - ny * w)
    d.polygon([f2, (f2[0] - ux * s * 0.16 - nx * s * 0.22,
                    f2[1] - uy * s * 0.16 - ny * s * 0.22),
               (f2[0] - ux * s * 0.05, f2[1] - uy * s * 0.05)], fill=col)
    # exhaust flame
    ft = (tail[0] - ux * s * 0.10, tail[1] - uy * s * 0.10)
    d.polygon([(ft[0] + nx * w * 0.7, ft[1] + ny * w * 0.7),
               (ft[0] - ux * s * 0.20, ft[1] - uy * s * 0.20),
               (ft[0] - nx * w * 0.7, ft[1] - ny * w * 0.7)], fill=RED)


def icon_scales(d, x, y, s, col):
    cx = x + s / 2
    d.line([(cx, y + 4), (cx, y + s - 8)], fill=col, width=2)
    d.line([(x + 4, y + 10), (x + s - 4, y + 10)], fill=col, width=2)
    d.line([(x + 4, y + s - 4), (x + s - 4, y + s - 4)], fill=col, width=2)
    for px in (x + 4, x + s - 4):
        d.line([(px, y + 10), (px, y + 16)], fill=col, width=1)
        d.pieslice([px - 8, y + 14, px + 8, y + 26], 0, 180, fill=col)


def icon_globe(d, x, y, s, col):
    cx, cy = x + s / 2, y + s / 2
    r = s * 0.38
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=2)
    d.ellipse([cx - r * 0.45, cy - r * 0.55, cx + r * 0.25, cy - r * 0.05],
              fill=col)
    d.ellipse([cx - r * 0.10, cy + r * 0.15, cx + r * 0.60, cy + r * 0.60],
              fill=col)
    # NO DEAL slash
    d.line([(cx - r * 0.75, cy + r * 0.75), (cx + r * 0.75, cy - r * 0.75)],
           fill=RED, width=3)


def icon_eu(d, x, y, s, col):
    cx, cy = x + s / 2, y + s / 2
    for k in range(8):
        a = math.pi / 4 * k - math.pi / 2
        _star4(d, cx + math.cos(a) * s * 0.34, cy + math.sin(a) * s * 0.34,
               s * 0.085, col)


def icon_fire(d, x, y, s, col):
    # factory silhouette, sawtooth roof + chimney + flame
    d.polygon([(x + 3, y + s - 3), (x + 3, y + s * 0.52),
               (x + s * 0.30, y + s * 0.30), (x + s * 0.48, y + s * 0.52),
               (x + s * 0.68, y + s * 0.30), (x + s - 3, y + s * 0.52),
               (x + s - 3, y + s - 3)], fill=col)
    d.rectangle([x + s * 0.72, y + 2, x + s * 0.84, y + s * 0.52], fill=col)
    _flame(d, x + s * 0.78, y + 4, s * 0.34, RED)


def icon_awacs(d, x, y, s, col):
    cy = y + s * 0.55
    # radar disc on a strut
    d.line([(x + s * 0.52, cy - s * 0.10), (x + s * 0.52, cy - s * 0.28)],
           fill=col, width=2)
    d.ellipse([x + s * 0.30, cy - s * 0.36, x + s * 0.74, cy - s * 0.24],
              fill=col)
    # slim fuselage + nose + tail fin + swept wing
    d.polygon([(x + 2, cy - 2), (x + s - 10, cy - 2), (x + s - 2, cy + 1),
               (x + s - 10, cy + 4), (x + 2, cy + 4)], fill=col)
    d.polygon([(x + 6, cy - 2), (x + 12, cy - s * 0.22),
               (x + 16, cy - s * 0.22), (x + 12, cy - 2)], fill=col)
    d.polygon([(x + s * 0.42, cy + 4), (x + s * 0.62, cy + s * 0.30),
               (x + s * 0.72, cy + s * 0.30), (x + s * 0.58, cy + 4)],
              fill=col)


def icon_quake(d, x, y, s, col):
    d.polygon([(x + 2, y + s - 3), (x + s * 0.50, y + 4),
               (x + s - 2, y + s - 3)], fill=col)
    d.polygon([(x + s * 0.38, y + 16), (x + s * 0.50, y + 4),
               (x + s * 0.62, y + 16)], fill=(252, 250, 242))
    d.line([(x + s * 0.50, y + 12), (x + s * 0.42, y + 22),
            (x + s * 0.56, y + 30), (x + s * 0.46, y + s - 6)],
           fill=RED, width=2)
    d.line([(x + 2, y + s - 6), (x + s - 2, y + s - 6)], fill=col, width=1)


def icon_flag(d, x, y, s, col):
    d.line([(x + 6, y + 2), (x + 6, y + s - 2)], fill=INK, width=2)
    d.rectangle([x + 8, y + 4, x + s - 2, y + s * 0.58], fill=col)
    d.ellipse([x + s * 0.42, y + s * 0.16, x + s * 0.66, y + s * 0.46],
              fill=RED)


def icon_talks(d, x, y, s, col):
    d.rounded_rectangle([x + 2, y + 4, x + s * 0.58, y + s * 0.52], radius=6,
                        outline=col, width=2)
    d.polygon([(x + 10, y + s * 0.52), (x + 16, y + s * 0.66),
               (x + 18, y + s * 0.52)], fill=col)
    d.rounded_rectangle([x + s * 0.42, y + s * 0.42, x + s - 2, y + s * 0.88],
                        radius=6, outline=col, width=2)
    d.polygon([(x + s - 16, y + s * 0.88), (x + s - 10, y + s - 2),
               (x + s - 8, y + s * 0.88)], fill=col)


def icon_chip(d, x, y, s, col):
    d.rectangle([x + 8, y + 8, x + s - 8, y + s - 8], outline=col, width=2)
    d.rectangle([x + s * 0.36, y + s * 0.36, x + s * 0.64, y + s * 0.64],
                fill=col)
    for k in range(3):
        px = x + 12 + k * 8
        d.line([(px, y + 2), (px, y + 8)], fill=col, width=2)
        d.line([(px, y + s - 8), (px, y + s - 2)], fill=col, width=2)
        py = y + 12 + k * 8
        d.line([(x + 2, py), (x + 8, py)], fill=col, width=2)
        d.line([(x + s - 8, py), (x + s - 2, py)], fill=col, width=2)
    d.line([(x + s * 0.55, y + s * 0.30), (x + s * 0.78, y + s * 0.07)],
           fill=RED, width=2)
    d.polygon([(x + s * 0.78, y + s * 0.07), (x + s * 0.66, y + s * 0.07),
               (x + s * 0.78, y + s * 0.19)], fill=RED)


ICONS = {
    "missile": icon_missile, "scales": icon_scales, "globe": icon_globe,
    "eu": icon_eu, "fire": icon_fire, "awacs": icon_awacs,
    "quake": icon_quake, "flag": icon_flag, "talks": icon_talks,
    "chip": icon_chip,
}


def _callout(d, x, y, text, fnt):
    tw = int(d.textlength(text, font=fnt)) + 12
    d.rectangle([x, y, x + tw, y + 20], fill=(255, 255, 255),
                outline=HAIR, width=1)
    d.text((x + 6, y + 4), text, font=fnt, fill=RED)
    return tw


def _tanker(d, cx, cy, s):
    d.rectangle([cx - s, cy - 2, cx + s, cy + 3], fill=INK)
    d.rectangle([cx + s * 0.3, cy - 6, cx + s * 0.7, cy - 2], fill=INK)
    _flame(d, cx, cy - 4, s * 0.9, RED)


def _mine(d, cx, cy, r):
    for k in range(8):
        a = math.pi / 4 * k
        d.line([(cx + math.cos(a) * r * 0.7, cy + math.sin(a) * r * 0.7),
                (cx + math.cos(a) * r * 1.5, cy + math.sin(a) * r * 1.5)],
               fill=INK, width=1)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=INK)


def hero_sanofi(d, x, y, w, h):
    # data panel, not a scene: giant number + rising bar chart
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=LINE, width=1)
    d.text((x + 12, y + 6), "$41bn", font=serif_black(40), fill=INK)
    d.text((x + 12, y + 52), "CASH AT $175 / SHARE", font=sans_b(9),
           fill=GREY)
    bx0 = x + w - 118
    bars = [14, 22, 30, 40]
    for i, bh in enumerate(bars):
        d.rectangle([bx0 + i * 26, y + h - 14 - bh, bx0 + i * 26 + 18,
                     y + h - 14], fill=REGION["EUROPE"])
    ax, ay = bx0 + 3 * 26 + 9, y + h - 14 - 46
    d.line([(bx0 - 4, y + h - 16), (ax, ay)], fill=RED, width=2)
    d.polygon([(ax, ay - 7), (ax + 8, ay + 2), (ax - 2, ay + 6)], fill=RED)
    d.text((bx0 - 6, y + 8), "INS +14%", font=sans_b(10), fill=RED)


def hero_hormuz(d, x, y, w, h):
    # schematic Strait of Hormuz: Iran coast (top), Oman (bottom right)
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=LINE, width=1)
    d.polygon([(x, y), (x + w, y), (x + w, y + 24),
               (x + w * 0.60, y + 34), (x + w * 0.28, y + 22), (x, y + 30)],
              fill=LAND, outline=LAND_LINE)
    d.polygon([(x + w * 0.68, y + h), (x + w, y + h), (x + w, y + 60),
               (x + w * 0.80, y + 56), (x + w * 0.70, y + 72)],
              fill=LAND, outline=LAND_LINE)
    dashed(d, (x + 8, y + h - 16), (x + w - 8, y + 46), GREY)
    _tanker(d, x + w * 0.30, y + 58, 13)
    _tanker(d, x + w * 0.52, y + 50, 13)
    _tanker(d, x + w * 0.72, y + 62, 13)
    _mine(d, x + w * 0.42, y + 74, 5)
    _mine(d, x + w * 0.86, y + 40, 5)
    _callout(d, x + 8, y + 8, "3 TANKERS ABLAZE", sans_b(10))
    d.text((x + 10, y + 34), "IRAN", font=sans_b(8), fill=GREY)
    d.text((x + w - 52, y + h - 14), "OMAN", font=sans_b(8), fill=GREY)
    d.text((x + w * 0.36, y + h - 14), "STRAIT OF HORMUZ", font=sans_b(8),
           fill=GREY)


def hero_merkury(d, x, y, w, h):
    # schematic Mediterranean / Libya coast
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=LINE, width=1)
    d.polygon([(x, y), (x + w, y), (x + w, y + 20), (x, y + 26)],
              fill=LAND, outline=LAND_LINE)
    d.polygon([(x, y + h), (x + w, y + h), (x + w, y + 66),
               (x + w * 0.72, y + 58), (x + w * 0.45, y + 70),
               (x + w * 0.20, y + 60), (x, y + 68)], fill=LAND,
              outline=LAND_LINE)
    sx, sy = x + w * 0.44, y + 44
    dashed(d, (x + w - 12, y + 8), (sx, sy), GREY)
    d.line([(sx - 8, sy - 8), (sx + 8, sy + 8)], fill=RED, width=3)
    d.line([(sx - 8, sy + 8), (sx + 8, sy - 8)], fill=RED, width=3)
    bx, by = x + w * 0.62, y + 74
    d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=RED,
              outline=(255, 255, 255), width=1)
    _callout(d, x + 8, y + 8, "7 DRONES", sans_b(10))
    d.text((x + w * 0.42, y + 4), "MEDITERRANEAN", font=sans_b(8),
           fill=GREY)
    d.text((x + 10, y + h - 14), "LIBYA", font=sans_b(8), fill=GREY)
    d.text((bx + 8, by - 4), "BENGHAZI", font=sans_b(8), fill=INK)


HERO_ART = {"sanofi": hero_sanofi, "hormuz": hero_hormuz,
            "merkury": hero_merkury}


# --- world map: beige land on paper, coloured dots, no leader lines ---
def draw_map(d, x, y, w, h):
    for poly in CONTINENTS:
        pts = [(x + (lon + 180) / 360 * w, y + (90 - lat) / 180 * h)
               for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    d.text((x + 4, y + int(h * 0.55)), "ATLANTIC", font=sans(8), fill=GREY)
    d.text((x + w - 48, y + int(h * 0.28)), "PACIFIC", font=sans(8),
           fill=GREY)
    for n, (lon, lat) in PINS.items():
        dx, dy = PIN_NUDGE.get(n, (0, 0))
        px = x + (lon + 180) / 360 * w + dx
        py = y + (90 - lat) / 180 * h + dy
        col = REGION[PIN_REGION[n]]
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=col,
                  outline=(255, 255, 255), width=1)
        t = str(n)
        tw = d.textlength(t, font=sans_b(7))
        d.text((px - tw / 2, py - 4), t, font=sans_b(7),
               fill=(255, 255, 255))

# --- cards: no boxes, thin region rule on top, flat icon, serif headline ---

def num_badge(d, x, y, n, r=9):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=INK)
    t = str(n)
    fnt = sans_b(10 if r >= 9 else 9)
    tw = d.textlength(t, font=fnt)
    d.text((x + r - tw / 2, y + r - 6), t, font=fnt, fill=(255, 255, 255))


def eyebrow(d, s, x, y, w, r=9):
    num_badge(d, x, y, s["n"], r=r)
    tx = x + 2 * r + 6
    # trust label on the right; shrink the tag until everything fits
    lt = s["label"]
    lw = d.textlength(lt, font=sans_b(8))
    avail = x + w - lw - 8 - tx
    d.text((tx, y + 2), s["city"], font=sans_b(10), fill=INK)
    cx = tx + d.textlength(s["city"], font=sans_b(10))
    tag = s["tag"]
    while tag and d.textlength(" \u00b7 " + tag, font=sans(9)) > avail - d.textlength(s["city"], font=sans_b(10)) - 4:
        parts = tag.split(" \u00b7 ")
        tag = " \u00b7 ".join(parts[:-1]) if len(parts) > 1 else ""
    if tag:
        d.text((cx + 4, y + 3), "\u00b7 " + tag, font=sans(9), fill=GREY)
    # trust label: muted small caps, not a colour chip
    d.text((x + w - lw, y + 3), lt, font=sans_b(8), fill=GREY)


def hero_card(d, s, x, y, w, h):
    HERO_ART[s["art"]](d, x, y, w, 96)
    eyebrow(d, s, x, y + 104, w, r=9)
    hf = serif_b(16)
    lines = wrap(d, s["head"], hf, w)[:2]
    yy = text_block(d, x, y + 128, lines, hf, INK, leading=18)
    blines = wrap(d, s["body"], sans(10), w)[:2]
    yy = text_block(d, x, yy + 3, blines, sans(10), (60, 58, 52),
                    leading=12)
    d.text((x, yy + 3), s["src"], font=sans(8), fill=GREY)


def story_card(d, s, x, y, w, h):
    col = REGION[s["region"]]
    d.rectangle([x, y, x + w, y + 2], fill=col)
    eyebrow(d, s, x, y + 8, w, r=8)
    # flat icon, left rail; headline + body to its right
    ix, iy = x, y + 32
    ICONS[s["art"]](d, ix, iy, 44, ICON_COL[s["art"]])
    tx = x + 50
    tw = w - 50
    hf = serif_b(14)
    lines = wrap(d, s["head"], hf, tw)[:3]
    yy = text_block(d, tx, iy + 1, lines, hf, INK, leading=16)
    blines = wrap(d, s["body"], sans(9), tw)[:3]
    yy = text_block(d, tx, yy + 3, blines, sans(9), (60, 58, 52),
                    leading=11)
    d.text((tx, yy + 3), s["src"], font=sans(8), fill=GREY)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 16
    CW = W - 2 * M  # 992

    # eyebrow: three parts, hairline below
    d.text((M, 10), "THE WORLD IN ONE DAY", font=sans_b(10), fill=INK)
    centred(d, W // 2, 10, "DAY 328 OF 2026", sans_b(10), RED)
    rt = "EVERY STORY DATED TUESDAY 24 NOV"
    d.text((W - M - d.textlength(rt, font=sans_b(10)), 10), rt,
           font=sans_b(10), fill=INK)
    hline(d, M, W - M, 27)

    # masthead, centred, serif black
    centred(d, W // 2, 32, "Tuesday 24 November 2026", serif_black(56),
            INK)
    hline(d, M, W - M, 98)

    # count line, small caps, centred
    cnt = "35 STORIES, ALL FROM TUESDAY 24 NOV \u00b7 " + " \u00b7 ".join(
        f"{n} {c}" for n, c in REGIONS)
    centred(d, W // 2, 104, cnt, sans_b(10), INK)
    hline(d, M, W - M, 120)

    # sub-headline: italic serif, red diamonds between items
    parts = ["Sanofi\u2019s $41bn deal", "UN probe over sunken warship",
             "Iran war deepens"]
    f_it = serif_i(17)
    widths = [d.textlength(p, font=f_it) for p in parts]
    dia = d.textlength(" \u25c6 ", font=sans_b(12))
    total = sum(widths) + 2 * dia
    cx = W // 2 - total / 2
    for i, p in enumerate(parts):
        d.text((cx, 126), p, font=f_it, fill=INK)
        cx += widths[i]
        if i < 2:
            d.text((cx, 128), " \u25c6 ", font=sans_b(12), fill=RED)
            cx += dia

    # Day in Numbers: giant serif numbers, hairlines
    hline(d, M, W - M, 152)
    cw = CW // 6
    for i, (num, lab) in enumerate(NUMBERS):
        cx0 = M + i * cw
        d.text((cx0 + 8, 158), num, font=serif_black(32), fill=INK)
        d.text((cx0 + 8, 194), lab, font=sans(9), fill=GREY)
        if i:
            d.line([(cx0, 158), (cx0, 206)], fill=HAIR, width=1)
    hline(d, M, W - M, 210)

    # timeline: quiet single row on paper (no dark band)
    ty = 217
    d.text((M, ty), "THE DAY IN UTC", font=sans_b(10), fill=INK)
    tx = M + int(d.textlength("THE DAY IN UTC", font=sans_b(10))) + 16
    each = (W - M - tx) // 6
    for t, ev in TIMELINE:
        d.text((tx, ty), t, font=sans_b(10), fill=RED)
        d.text((tx + 36, ty + 1), ev, font=sans(9), fill=(60, 58, 52))
        tx += each
    hline(d, M, W - M, 236)

    # heroes: 3 across, data panel on top, text below
    hy, hh = 244, 196
    hw = (CW - 14) // 3
    for i, s in enumerate(HEROES):
        hero_card(d, s, M + i * (hw + 7), hy, hw, hh)

    # cards: 5 + 5, hairline separators between columns
    cy1, chh = 448, 178
    cw5 = (CW - 40) // 5
    for row, cy in ((CARDS[:5], cy1), (CARDS[5:], cy1 + 186)):
        for i, s in enumerate(row):
            x = M + i * (cw5 + 10)
            story_card(d, s, x, cy, cw5, chh)
    for cy in (cy1, cy1 + 186):
        for i in range(1, 5):
            x = M + i * (cw5 + 10) - 5
            d.line([(x, cy + 4), (x, cy + chh - 4)], fill=HAIR, width=1)

    # section header
    sy = 818
    d.text((M, sy), "WHERE IT HAPPENED", font=sans_b(12), fill=INK)
    d.text((M + 148, sy + 2), "pins carry the story numbers", font=sans(9),
           fill=GREY)
    d.text((M + 352, sy), "ALSO ON TUESDAY 24 NOV", font=sans_b(12),
           fill=INK)
    hline(d, M, W - M, sy + 20)

    # map + also-on list
    my = 844
    draw_map(d, M, my, 336, 108)
    lx = M + 352
    col_w = (W - M - lx - 10) // 2
    for i, (n, head, src) in enumerate(ALSO):
        col = i // 11
        row = i % 11
        ax = lx + col * (col_w + 10)
        ay = my + row * 10
        d.text((ax, ay), str(n), font=sans_b(9), fill=RED)
        d.text((ax + 20, ay), head, font=sans(9), fill=INK)
        sw = d.textlength(src, font=sans(8))
        d.text((ax + col_w - sw, ay + 1), src, font=sans(8), fill=GREY)

    # DATE CHECK: thin red rule, flowing text with named dates
    dy = 958
    d.line([(M, dy), (W - M, dy)], fill=RED, width=1)
    d.text((M, dy + 5), "DATE CHECK", font=sans_b(10), fill=RED)
    dc = ("Every story here happened or was first reported Tue 24 Nov 2026. "
          "Left out \u2014 Democrats\u2019 House win (Sun 22 Nov) \u00b7 COP31 collapse "
          "(Sun 22 Nov) \u00b7 Merkury sinking (Sun 22 Nov; Tue\u2019s news: the UN probe) "
          "\u00b7 Serang fire (Sat 21 Nov; Tue\u2019s news: toll of 26) \u00b7 "
          "CrowdStrike\u2013Zscaler deal (Mon 23 Nov) \u00b7 Huang reinstated as Nvidia CEO "
          "(Mon 23 Nov; Tue\u2019s news: +31% jump).")
    lines = wrap(d, dc, sans(9), W - 2 * M - 96)
    text_block(d, M + 92, dy + 5, lines[:3], sans(9), INK, leading=11)

    # footer
    centred(d, W // 2, 998,
            "Every story here happened or was first reported on Tuesday "
            "24 November 2026, as the named outlets reported it. Maps and "
            "drawings are original vector art.",
            serif_i(9), GREY)
    centred(d, W // 2, 1010,
            "HOW SURE \u2014 CONFIRMED 2+ outlets \u00b7 OFFICIAL authority\u2019s "
            "words \u00b7 CLAIM one side\u2019s account \u00b7 REPORTED carried by "
            "wires \u00b7 ONGOING still unfolding \u00b7 v3 \u00b7 35 stories",
            sans(8), GREY)

    img.save(OUT, format="PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    render()
