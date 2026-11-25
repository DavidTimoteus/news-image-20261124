#!/usr/bin/env python3
"""Render the v4 front page for make.fun news-image-20261124 — broadsheet redesign.

v4 (25 Nov 2026): total rebuild of the content after the Round 3 audit
(rank 2009/14.561 — 8 of 13 featured stories in v3 had the wrong date).
All 38 stories verified to Tuesday 24 Nov 2026 against named outlets.
Lead is hard news (Riyadh PIF tower); Sanofi $41bn moves to a middle card.
Cards use the Round 3 winners' pattern: full-width art panel on top with
a number callout banner inside the art, headline + body below.

Editorial broadsheet language (after rank 1 @gentle-koala-36, 851.588):
cream paper + ink + one muted red; serif masthead and headlines; hairline
rules; no boxes, no navy bands, no colour chips. 1024x1024, Pillow only.
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
    "EUROPE": (51, 87, 122), "EAST ASIA": (107, 78, 142),
    "SOUTH ASIA": (62, 122, 122), "SE ASIA": (78, 122, 78),
    "MIDDLE EAST": (140, 47, 47), "NORTH AMERICA": (138, 109, 47),
    "AFRICA": (96, 122, 62), "OCEANIA": (70, 110, 140),
    "LATIN AMERICA": (150, 90, 40), "GLOBAL": (90, 90, 90),
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


# --- story data: 38 stories, all happened / first reported Tue 24 Nov 2026 ---
# (facts, dates and labels verified against named outlets; see V4_SPEC.md)
HEROES = [
    dict(n=1, city="RIYADH", tag="WAR \u00b7 DRONE", label="CONFIRMED",
         region="MIDDLE EAST", art="riyadh",
         head="Houthi drone hits Riyadh's tallest tower",
         body="A Houthi drone hits the PIF Tower in the financial district \u2014 the second strike on the tower in five days; 11 hurt.",
         src="Saudi Civil Defence \u00b7 Reuters"),
    dict(n=2, city="SHANGHAI", tag="POLITICS \u00b7 PURGE", label="OFFICIAL",
         region="EAST ASIA", art="shanghai",
         head="China probes Shanghai party chief",
         body="Chen Jining, 62, is under investigation for 'serious violations' \u2014 the fourth Politburo member probed since 2025.",
         src="Xinhua \u00b7 Reuters"),
    dict(n=3, city="HORMUZ", tag="WAR \u00b7 SHIPPING", label="CLAIM",
         region="MIDDLE EAST", art="hormuz2",
         head="Three ships hit in Hormuz; Brent jumps",
         body="UKMTO: three ships hit by projectiles, crews safe; Iran's Guards claim a fourth tanker hit a mine. Brent $91.40.",
         src="UKMTO \u00b7 Reuters"),
]

CARDS = [
    dict(n=4, city="NEW YORK", tag="COURTS \u00b7 TECH", label="CONFIRMED",
         region="NORTH AMERICA", art="court",
         head="US jury finds Huawei guilty",
         body="Guilty on 10 of 12 \u2014 fraud, sanctions, trade secrets; racketeering cleared.",
         src="Reuters \u00b7 CNN"),
    dict(n=5, city="ZAPORIZHZHIA", tag="WAR", label="CONFIRMED",
         region="EUROPE", art="apartment",
         head="Russian raid kills 2 in Zaporizhzhia",
         body="Night raid kills 2, wounds 40+, incl. four children; a five-storey block is hit.",
         src="AP \u00b7 Reuters"),
    dict(n=6, city="PARIS", tag="PHARMA \u00b7 DEALS", label="CONFIRMED",
         region="EUROPE", art="sanofi_card",
         head="Sanofi buys Insmed for $41bn",
         body="Sanofi buys Insmed, $41bn cash at $175/share \u2014 biggest deal in 20 years.",
         src="Sanofi \u00b7 Bloomberg"),
    dict(n=7, city="LAUSANNE", tag="SPORT \u00b7 COURT", label="OFFICIAL",
         region="AFRICA", art="trophy",
         head="CAS hands Senegal back AFCON title",
         body="Top court restores Senegal's 1\u20130 final win, voiding CAF's 3\u20130 forfeit to Morocco.",
         src="CAS \u00b7 Reuters"),
    dict(n=8, city="SERANG", tag="DISASTER", label="REPORTED",
         region="SE ASIA", art="fire2",
         head="Factory fire: death toll hits 26",
         body="Toll confirmed Tuesday after the Saturday blaze; 8 missing, probe under way.",
         src="AP \u00b7 Reuters"),
    dict(n=9, city="HANOI", tag="DISASTER", label="CONFIRMED",
         region="SE ASIA", art="blast",
         head="Gas blast kills 6 in Hanoi eatery",
         body="Gas blast flattens hotpot eatery; 6 dead, 10+ hurt, houses damaged.",
         src="AP \u00b7 Reuters"),
    dict(n=10, city="NEPAL", tag="DISASTER", label="CONFIRMED",
         region="SOUTH ASIA", art="quake2",
         head="Nepal quake, 5.6, near China border",
         body="A 5.6 quake strikes near the China border at 07:17; checks under way.",
         src="The Hindu \u00b7 EMSC"),
    dict(n=11, city="RAS AL KHAIMAH", tag="DISASTER", label="CONFIRMED",
         region="MIDDLE EAST", art="bus",
         head="Bus crash kills 13 in the UAE",
         body="A bus carrying 41 hits a parked truck on Al Watan Road; 13 dead, 14 hurt.",
         src="RAK Police \u00b7 Gulf Business"),
    dict(n=12, city="NEW YORK", tag="MARKETS", label="CONFIRMED",
         region="NORTH AMERICA", art="dow",
         head="Dow closes above 50,000 at last",
         body="First close above 50,000 \u2014 50,018 \u2014 as Nvidia gives back 5.9% and chips slide.",
         src="Investopedia \u00b7 Barron's"),
    dict(n=13, city="KOUROU", tag="SPACE", label="CONFIRMED",
         region="LATIN AMERICA", art="rocket",
         head="Ariane 6 lofts 36 Amazon satellites",
         body="Lift-off at 11:14 UTC from French Guiana \u2014 the 10th Ariane 6 flight, a day late.",
         src="Spaceflight Now \u00b7 AIAA"),
]

ALSO = [
    (14, "UK: warns Ukraine suppliers of sabotage", "MoD"),
    (15, "Slovakia: MPs end postal votes from abroad", "AP"),
    (16, "France: Nahel officer sent to murder trial", "AFP"),
    (17, "Turkey: helicopter crash kills 5", "AA"),
    (18, "Yemen: UK sanctions Houthi leaders", "gov.uk"),
    (19, "DR Congo: rebels say advance halted", "Al Jazeera"),
    (20, "Ethiopia: Alamata war-crimes probe urged", "Amnesty"),
    (21, "Cameroon: separatist denies war crimes", "AFP"),
    (22, "China: Pakistani named to Shenzhou-24 crew", "HKFP"),
    (23, "India: bus crash kills 4 children", "Tribune"),
    (24, "Australia: Wong backs the US alliance", "AAP"),
    (25, "Vanuatu: MPs back A$500m Australia pact", "AAP"),
    (26, "US: confidence index 103.3", "Conf. Board"),
    (27, "Brazil: Bolsonaro still in intensive care", "hospital"),
    (28, "Cartagena: about 25 held hostage in store", "Reuters"),
    (29, "UNAIDS: 1.2m new HIV infections in 2025", "AFP"),
    (30, "Champions League: Real Madrid 5-1 PSV", "UEFA"),
    (31, "Iraq takes over Kurdish-held oilfields", "Reuters"),
    (32, "Mexico to try 'El Chapo Isidro' at home", "Reuters"),
    (33, "Gaza: strikes kill 7; WHO warns of meningitis", "WHO"),
    (34, "EU caps Chinese car imports at 350,000 a year", "Reuters"),
    (35, "S. Africa cities tighten water curbs", "Africanews"),
    (36, "Borno school enrolment nearly doubles", "Al Jazeera"),
    (37, "Solomons to drop China pact for Australia", "SMH \u00b7 Reuters"),
    (38, "England thrash Australia in T20, Gold Coast", "Reuters"),
]

NUMBERS = [
    ("11", "hurt in Riyadh strike"),
    ("10 of 12", "counts: Huawei guilty"),
    ("50,018", "Dow's first 50,000 close"),
    ("$41bn", "Sanofi buys Insmed"),
    ("5,258", "England heat deaths, record"),
    ("36", "Amazon satellites lofted"),
]

TIMELINE = [
    ("01:00", "Hanoi blast"),
    ("01:32", "Nepal quake"),
    ("06:30", "Sanofi $41bn deal"),
    ("11:14", "Ariane 6 launch"),
    ("14:50", "Serang toll: 26"),
    ("21:00", "Dow 50,018"),
]

# display name, count — sums to 38 (Turkey counted EUROPE, T20 Gold Coast OCEANIA)
REGIONS = [
    ("EUROPE", 8), ("E. ASIA", 2), ("MIDDLE EAST", 6), ("N. AMERICA", 4),
    ("AFRICA", 6), ("S. ASIA", 2), ("SE ASIA", 2), ("OCEANIA", 4),
    ("LAT. AM.", 3), ("GLOBAL", 1),
]

PIN_REGION = {
    1: "MIDDLE EAST", 2: "EAST ASIA", 3: "MIDDLE EAST",
    4: "NORTH AMERICA", 5: "EUROPE", 6: "EUROPE", 7: "AFRICA",
    8: "SE ASIA", 9: "SE ASIA", 10: "SOUTH ASIA", 11: "MIDDLE EAST",
    12: "NORTH AMERICA", 13: "LATIN AMERICA",
}
# lon/lat of the 13 featured stories (true city coords; map is schematic).
PINS = {
    1: (47, 25), 2: (121, 31), 3: (56, 26), 4: (-74, 41), 5: (35, 48),
    6: (2, 49), 7: (-17, 15), 8: (106, -6), 9: (106, 21), 10: (84, 28),
    11: (56, 25), 12: (-74, 41), 13: (-53, 5),
}
# px nudges so all 13 dots (11px) stay visually separate, no leader lines.
# Computed from projected positions: 1/3/11 Gulf cluster spread apart,
# 4/12 (both New York) split diagonally, 5 nudged off 3, 2 off the PACIFIC label.
PIN_NUDGE = {1: (-10, 6), 2: (-2, -8), 3: (-8, -10), 4: (-8, -7),
             5: (-6, -4), 6: (0, 0), 7: (0, 0), 8: (0, 0), 9: (-4, 3),
             10: (0, 0), 11: (10, 6), 12: (8, 7), 13: (0, 0)}

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

# --- flat drawing helpers ---

def _star4(d, cx, cy, r, fill):
    d.polygon([(cx, cy - r), (cx + r * 0.30, cy - r * 0.30), (cx + r, cy),
               (cx + r * 0.30, cy + r * 0.30), (cx, cy + r),
               (cx - r * 0.30, cy + r * 0.30), (cx - r, cy),
               (cx - r * 0.30, cy - r * 0.30)], fill=fill)


def _flame(d, cx, base, s, fill):
    d.polygon([(cx - s * 0.45, base), (cx - s * 0.18, base - s * 0.55),
               (cx, base - s * 0.30), (cx + s * 0.16, base - s * 0.75),
               (cx + s * 0.45, base)], fill=fill)


def _callout(d, x, y, text, fnt, fill=RED):
    tw = int(d.textlength(text, font=fnt)) + 12
    d.rectangle([x, y, x + tw, y + 20], fill=(255, 255, 255),
                outline=HAIR, width=1)
    d.text((x + 6, y + 4), text, font=fnt, fill=fill)
    return tw


def _banner(d, x, y, text, fill=RED):
    """White-box number callout inside an art panel (bottom/top corner)."""
    return _callout(d, x, y, text, sans_b(9), fill=fill)


def _panel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=LINE, width=1)


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


# --- reused small icons, redrawn inside card panels ---

def icon_fire(d, x, y, s, col):
    # factory silhouette, sawtooth roof + chimney + flame
    d.polygon([(x + 3, y + s - 3), (x + 3, y + s * 0.52),
               (x + s * 0.30, y + s * 0.30), (x + s * 0.48, y + s * 0.52),
               (x + s * 0.68, y + s * 0.30), (x + s - 3, y + s * 0.52),
               (x + s - 3, y + s - 3)], fill=col)
    d.rectangle([x + s * 0.72, y + 2, x + s * 0.84, y + s * 0.52], fill=col)
    _flame(d, x + s * 0.78, y + 4, s * 0.34, RED)


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


# --- hero art: flat, outlined, dense (no empty field >40%) ---

def hero_sanofi(d, x, y, w, h):
    # data panel, not a scene: giant number + rising bar chart
    _panel(d, x, y, w, h)
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


def hero_riyadh(d, x, y, w, h):
    # PIF Tower skyline, KAFD: dark slabs, lit windows, impact mark + smoke
    _panel(d, x, y, w, h)
    base = y + h
    bcol = (96, 96, 98)
    # background slabs (left to right)
    slabs = [(8, 52, 58), (66, 68, 56), (130, 44, 62), (240, 50, 74)]
    for bx, bh, bw in slabs:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=bcol,
                    outline=INK, width=1)
        for wy in range(base - bh + 8, base - 6, 10):
            for wx in range(x + bx + 6, x + bx + bw - 5, 12):
                d.rectangle([wx, wy, wx + 4, wy + 4], fill=(238, 226, 170))
    # PIF Tower: tall dark slab, centre-right, grid windows
    tx0, tx1 = x + 176, x + 232
    d.rectangle([tx0, y + 6, tx1, base], fill=(58, 58, 64), outline=INK,
                width=2)
    for wy in range(y + 12, base - 6, 9):
        for wx in range(tx0 + 6, tx1 - 5, 11):
            d.rectangle([wx, wy, wx + 4, wy + 5], fill=(238, 226, 170))
    # impact mark mid-tower + thin smoke drifting up-left
    d.ellipse([tx0 + 8, y + 40, tx0 + 34, y + 58], fill=(30, 30, 32))
    d.ellipse([tx0 - 2, y + 30, tx0 + 12, y + 40], fill=(150, 148, 142))
    d.ellipse([tx0 - 12, y + 20, tx0 + 2, y + 30], fill=(178, 176, 170))
    d.ellipse([tx0 - 20, y + 12, tx0 - 8, y + 20], fill=(200, 198, 192))
    # ground line
    d.line([(x, base - 1), (x + w, base - 1)], fill=INK, width=1)
    # callouts
    _callout(d, x + 8, y + 8, "2ND STRIKE IN 5 DAYS", sans_b(8), fill=INK)
    _lw = d.textlength("PIF TOWER \u00b7 KAFD", font=sans_b(8))
    d.text((x + w - 8 - _lw, y + 8), "PIF TOWER \u00b7 KAFD", font=sans_b(8),
           fill=GREY)
    tw = int(d.textlength("11 HURT", font=sans_b(11))) + 12
    _callout(d, x + w - 8 - tw, y + h - 28, "11 HURT", sans_b(11))


def hero_shanghai(d, x, y, w, h):
    # Shanghai skyline under a big magnifier
    _panel(d, x, y, w, h)
    base = y + h
    bcol = (92, 92, 104)
    # skyline slabs
    slabs = [(8, 46, 44), (56, 60, 40), (100, 38, 48), (152, 52, 44),
             (200, 66, 40), (244, 44, 38), (286, 58, 32)]
    for bx, bh, bw in slabs:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=bcol,
                    outline=INK, width=1)
        for wy in range(base - bh + 7, base - 5, 9):
            for wx in range(x + bx + 5, x + bx + bw - 4, 10):
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(238, 226, 170))
    # Oriental Pearl-style tower: spire + two spheres, centre-left
    px = x + 118
    d.line([(px, y + 10), (px, y + 62)], fill=INK, width=2)
    d.ellipse([px - 9, y + 16, px + 9, y + 34], fill=RED, outline=INK,
              width=1)
    d.ellipse([px - 6, y + 40, px + 6, y + 52], fill=RED, outline=INK,
              width=1)
    d.line([(x, base - 1), (x + w, base - 1)], fill=INK, width=1)
    # magnifier over the right-hand towers
    cx, cy, r = x + w * 0.60, y + 38, 27
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    d.line([(cx + r * 0.7, cy + r * 0.7), (cx + r * 1.5, cy + r * 1.5)],
           fill=INK, width=4)
    # callouts
    _callout(d, x + 8, y + 8, "4TH POLITBURO MEMBER", sans_b(8), fill=INK)
    d.text((x + w - 58, y + 8), "SHANGHAI", font=sans_b(8), fill=GREY)
    tw = int(d.textlength("UNDER PROBE", font=sans_b(11))) + 12
    _callout(d, x + w - 8 - tw, y + h - 28, "UNDER PROBE", sans_b(11))


def hero_hormuz2(d, x, y, w, h):
    # schematic Strait of Hormuz: Iran coast (top), Oman (bottom right),
    # 4 tankers, 2 projectile bursts, dashed route, 2 callouts
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=LINE, width=1)
    d.polygon([(x, y), (x + w, y), (x + w, y + 24),
               (x + w * 0.60, y + 34), (x + w * 0.28, y + 22), (x, y + 30)],
              fill=LAND, outline=LAND_LINE)
    d.polygon([(x + w * 0.68, y + h), (x + w, y + h), (x + w, y + 60),
               (x + w * 0.80, y + 56), (x + w * 0.70, y + 72)],
              fill=LAND, outline=LAND_LINE)
    dashed(d, (x + 8, y + h - 16), (x + w - 8, y + 46), GREY)
    # small waves
    for wx, wy in ((0.18, 78), (0.55, 82), (0.88, 70), (0.40, 88)):
        d.line([(x + w * wx, y + wy), (x + w * wx + 14, y + wy)], fill=GREY,
               width=1)
    _tanker(d, x + w * 0.20, y + 58, 13)
    _tanker(d, x + w * 0.42, y + 50, 13)
    _tanker(d, x + w * 0.62, y + 62, 13)
    _tanker(d, x + w * 0.84, y + 52, 13)
    _star4(d, x + w * 0.31, y + 42, 6, RED)
    _star4(d, x + w * 0.72, y + 40, 6, RED)
    _mine(d, x + w * 0.52, y + 76, 5)
    _callout(d, x + 8, y + 8, "3 SHIPS HIT", sans_b(10))
    d.text((x + 8, y + 32), "4TH TANKER CLAIMED", font=sans(8), fill=INK)
    d.text((x + 150, y + 8), "IRAN", font=sans_b(8), fill=GREY)
    d.text((x + w - 52, y + h - 14), "OMAN", font=sans_b(8), fill=GREY)
    d.text((x + w * 0.36, y + h - 14), "STRAIT OF HORMUZ", font=sans_b(8),
           fill=GREY)
    tw = int(d.textlength("BRENT $91.40", font=sans_b(9))) + 12
    _callout(d, x + w - 8 - tw, y + h - 28, "BRENT $91.40", sans_b(9),
             fill=INK)


HERO_ART = {"riyadh": hero_riyadh, "shanghai": hero_shanghai,
            "hormuz2": hero_hormuz2, "sanofi": hero_sanofi}


# --- card art: full-width panel (w x 62) with number callout banner ---

def art_court(d, x, y, w, h):
    _panel(d, x, y, w, h)
    col = (90, 90, 100)
    # courthouse: pediment + 3 columns + steps, left two-thirds
    d.polygon([(x + 18, y + 24), (x + 114, y + 24), (x + 66, y + 8)],
              fill=col, outline=INK, width=1)
    for cx in (28, 58, 88):
        d.rectangle([x + cx, y + 26, x + cx + 10, y + 48], fill=col,
                    outline=INK, width=1)
    d.rectangle([x + 62, y + 36, x + 70, y + 48], fill=INK)
    for i, sy in enumerate((50, 54, 58)):
        d.rectangle([x + 14, y + sy, x + 118, y + sy + 3], fill=col,
                    outline=INK, width=1)
    tw = int(d.textlength("GUILTY 10 OF 12", font=sans_b(9))) + 12
    _banner(d, x + w - 8 - tw, y + 6, "GUILTY 10 OF 12")


def art_apartment(d, x, y, w, h):
    _panel(d, x, y, w, h)
    # 5-storey block, damaged top, crack + smoke
    bx0, by0, bw = x + 14, y + 6, 84
    d.polygon([(bx0, by0 + 6), (bx0 + 20, by0), (bx0 + 44, by0 + 5),
               (bx0 + bw, by0 + 2), (bx0 + bw, y + h - 4),
               (bx0, y + h - 4)], fill=(120, 110, 100), outline=INK,
              width=1)
    for r in range(5):
        for c in range(4):
            wx, wy = bx0 + 8 + c * 19, by0 + 12 + r * 9
            d.rectangle([wx, wy, wx + 10, wy + 6],
                        fill=INK if (r + c) % 3 else (238, 226, 170))
    d.line([(bx0 + 44, by0 + 4), (bx0 + 38, by0 + 22), (bx0 + 50, by0 + 34),
            (bx0 + 42, y + h - 8)], fill=RED, width=2)
    d.ellipse([bx0 + 8, by0 - 2, bx0 + 22, by0 + 8], fill=(178, 176, 170))
    d.ellipse([bx0 + 24, by0 - 6, bx0 + 34, by0 + 2], fill=(200, 198, 192))
    tw = int(d.textlength("2 KILLED \u00b7 40+ HURT", font=sans_b(9))) + 12
    _banner(d, x + w - 8 - tw, y + h - 28, "2 KILLED \u00b7 40+ HURT")


def art_sanofi_card(d, x, y, w, h):
    _panel(d, x, y, w, h)
    # big capsule pill (two halves) + small rising chart
    px0, py0, pw, ph = x + 12, y + 18, 96, 26
    d.rounded_rectangle([px0, py0, px0 + pw, py0 + ph], radius=13,
                        fill=(252, 250, 242), outline=INK, width=2)
    d.rectangle([px0 + 2, py0 + 2, px0 + pw // 2, py0 + ph - 2],
                fill=RED)
    d.rounded_rectangle([px0, py0, px0 + pw, py0 + ph], radius=13,
                        outline=INK, width=2)
    d.line([(px0 + pw // 2, py0 + 2), (px0 + pw // 2, py0 + ph - 2)],
           fill=INK, width=1)
    d.rectangle([px0 + 10, py0 + 6, px0 + 30, py0 + 10], fill=(255, 255, 255))
    # rising chart, right
    bars = [8, 14, 20]
    for i, bh in enumerate(bars):
        d.rectangle([x + 126 + i * 14, y + 34 - bh, x + 126 + i * 14 + 9,
                     y + 34], fill=REGION["EUROPE"])
    d.line([(x + 124, y + 36), (x + 168, y + 12)], fill=RED, width=2)
    d.polygon([(x + 168, y + 12), (x + 160, y + 12), (x + 168, y + 20)],
              fill=RED)
    _banner(d, x + w - 8 - 47, y + h - 28, "$41BN")


def art_trophy(d, x, y, w, h):
    _panel(d, x, y, w, h)
    gold = (150, 120, 50)
    # trophy cup + stem + base, left
    d.polygon([(x + 28, y + 12), (x + 72, y + 12), (x + 66, y + 34),
               (x + 34, y + 34)], fill=gold, outline=INK, width=1)
    d.ellipse([x + 20, y + 14, x + 32, y + 28], outline=INK, width=2)
    d.ellipse([x + 68, y + 14, x + 80, y + 28], outline=INK, width=2)
    d.rectangle([x + 46, y + 34, x + 54, y + 46], fill=gold, outline=INK,
                width=1)
    d.rectangle([x + 36, y + 46, x + 64, y + 52], fill=gold, outline=INK,
                width=1)
    # Senegal flag: green-yellow-red vertical thirds, right of cup
    fx, fy = x + 92, y + 14
    d.line([(fx, fy + 26), (fx, fy - 2)], fill=INK, width=2)
    d.rectangle([fx + 2, fy, fx + 14, fy + 24], fill=(40, 110, 70),
                outline=INK, width=1)
    d.rectangle([fx + 14, fy, fx + 26, fy + 24], fill=(220, 190, 60),
                outline=INK, width=1)
    d.rectangle([fx + 26, fy, fx + 38, fy + 24], fill=(170, 50, 50),
                outline=INK, width=1)
    tw = int(d.textlength("TITLE RESTORED", font=sans_b(9))) + 12
    _banner(d, x + w - 8 - tw, y + h - 28, "TITLE RESTORED")


def art_fire2(d, x, y, w, h):
    _panel(d, x, y, w, h)
    icon_fire(d, x + 12, y + 4, 54, (140, 47, 47))
    d.ellipse([x + 84, y + 8, x + 96, y + 18], fill=(178, 176, 170))
    d.ellipse([x + 98, y + 4, x + 106, y + 12], fill=(200, 198, 192))
    tw = int(d.textlength("26 DEAD", font=sans_b(9))) + 12
    _banner(d, x + w - 8 - tw, y + h - 28, "26 DEAD")


def art_blast(d, x, y, w, h):
    _panel(d, x, y, w, h)
    # leaning 2-storey building + rubble + dust
    d.polygon([(x + 16, y + 22), (x + 92, y + 12), (x + 98, y + 50),
               (x + 16, y + 56)], fill=(110, 105, 95), outline=INK,
              width=1)
    for wx, wy in ((26, 28), (48, 25), (70, 22), (30, 40), (54, 37),
                   (76, 34)):
        d.rectangle([x + wx, y + wy, x + wx + 10, y + wy + 7], fill=INK)
    d.line([(x + 50, y + 14), (x + 56, y + 30), (x + 48, y + 44)],
           fill=RED, width=2)
    for rx, ry, rs in ((104, 48, 8), (116, 50, 6), (126, 52, 5)):
        d.polygon([(x + rx, y + ry), (x + rx + rs, y + ry - rs),
                   (x + rx + 2 * rs, y + ry)], fill=(140, 134, 124),
                  outline=INK, width=1)
    d.ellipse([x + 108, y + 20, x + 120, y + 30], fill=(200, 198, 192))
    d.ellipse([x + 122, y + 26, x + 130, y + 34], fill=(178, 176, 170))
    tw = int(d.textlength("6 KILLED", font=sans_b(9))) + 12
    _banner(d, x + w - 8 - tw, y + h - 28, "6 KILLED")


def art_quake2(d, x, y, w, h):
    _panel(d, x, y, w, h)
    icon_quake(d, x + 12, y + 4, 54, (120, 90, 60))
    # seismograph strip across the lower right
    pts = [(x + 82, y + 46), (x + 92, y + 46), (x + 97, y + 34),
           (x + 102, y + 52), (x + 107, y + 40), (x + 112, y + 50),
           (x + 117, y + 36), (x + 122, y + 54), (x + 127, y + 44),
           (x + 132, y + 46), (x + 178, y + 46)]
    d.line(pts, fill=RED, width=2)
    tw = int(d.textlength("5.6", font=sans_b(9))) + 12
    _banner(d, x + w - 8 - tw, y + 6, "5.6")


def art_bus(d, x, y, w, h):
    _panel(d, x, y, w, h)
    # road strip
    d.rectangle([x, y + 46, x + w, y + 58], fill=(190, 185, 175))
    for rx in range(x + 6, x + w - 6, 18):
        d.line([(rx, y + 52), (rx + 9, y + 52)], fill=(255, 255, 255),
               width=2)
    # bus (left) + parked truck (right)
    d.rectangle([x + 12, y + 18, x + 108, y + 46], fill=(138, 109, 47),
                outline=INK, width=1)
    for wx in (20, 40, 60, 80):
        d.rectangle([x + wx, y + 23, x + wx + 14, y + 33],
                    fill=(252, 250, 242), outline=INK, width=1)
    d.rectangle([x + 128, y + 24, x + 176, y + 46], fill=(90, 90, 90),
                outline=INK, width=1)
    d.rectangle([x + 160, y + 28, x + 172, y + 36],
                fill=(252, 250, 242), outline=INK, width=1)
    for wx in (28, 88, 140, 166):
        d.ellipse([x + wx, y + 42, x + wx + 10, y + 52], fill=INK)
    tw = int(d.textlength("13 DEAD", font=sans_b(9))) + 12
    _banner(d, x + w - 8 - tw, y + 6, "13 DEAD")


def art_dow(d, x, y, w, h):
    # big number + chart line, no small banner (number IS the callout)
    _panel(d, x, y, w, h)
    d.text((x + 8, y + 4), "50,018", font=serif_black(26), fill=INK)
    pts = [(x + 8, y + 44), (x + 45, y + 34), (x + 80, y + 40),
           (x + 115, y + 28), (x + 150, y + 34), (x + 182, y + 24)]
    d.line(pts, fill=REGION["EUROPE"], width=2)
    d.polygon([(x + 182, y + 24), (x + 174, y + 22), (x + 180, y + 31)],
              fill=REGION["EUROPE"])
    d.text((x + 8, y + h - 12), "DOW FIRST CLOSE ABOVE 50,000",
           font=sans_b(8), fill=GREY)
    _nw = d.textlength("NVIDIA \u22125.9%", font=sans_b(8))
    d.text((x + w - 8 - _nw, y + 6), "NVIDIA \u22125.9%", font=sans_b(8),
           fill=RED)


def art_rocket(d, x, y, w, h):
    _panel(d, x, y, w, h)
    # rocket upright, left; 3 small satellites, right
    rx = x + 44
    d.polygon([(rx - 8, y + 12), (rx + 8, y + 12), (rx, y + 2)],
              fill=RED, outline=INK, width=1)
    d.rectangle([rx - 8, y + 12, rx + 8, y + 40], fill=(210, 208, 200),
                outline=INK, width=1)
    d.polygon([(rx - 8, y + 32), (rx - 16, y + 44), (rx - 8, y + 40)],
              fill=RED, outline=INK, width=1)
    d.polygon([(rx + 8, y + 32), (rx + 16, y + 44), (rx + 8, y + 40)],
              fill=RED, outline=INK, width=1)
    _flame(d, rx, y + 56, 16, RED)
    d.ellipse([rx - 12, y + 52, rx - 2, y + 60], fill=(200, 198, 192))
    d.ellipse([rx + 4, y + 54, rx + 14, y + 60], fill=(178, 176, 170))
    for sx, sy in ((112, 12), (142, 24), (168, 10)):
        d.rectangle([x + sx, y + sy, x + sx + 10, y + sy + 8],
                    fill=(51, 87, 122), outline=INK, width=1)
        d.rectangle([x + sx - 8, y + sy + 1, x + sx, y + sy + 7],
                    fill=(120, 140, 170), outline=INK, width=1)
        d.rectangle([x + sx + 10, y + sy + 1, x + sx + 18, y + sy + 7],
                    fill=(120, 140, 170), outline=INK, width=1)
    _star4(d, x + 96, y + 44, 4, RED)
    tw = int(d.textlength("36 SATELLITES", font=sans_b(9))) + 12
    _banner(d, x + w - 8 - tw, y + h - 28, "36 SATELLITES")


def art_flag(d, x, y, w, h):
    # kept for CARD_ART completeness (v4 has no flag card); flag + podium
    _panel(d, x, y, w, h)
    icon_flag(d, x + 12, y + 4, 54, (78, 122, 78))
    d.rectangle([x + 84, y + 40, x + 160, y + 46], fill=(120, 110, 100),
                outline=INK, width=1)
    d.text((x + 92, y + 48), "DEC 16", font=sans_b(9), fill=INK)
    tw = int(d.textlength("DEC 16", font=sans_b(9))) + 12
    _banner(d, x + w - 8 - tw, y + 6, "DEC 16")


CARD_ART = {"court": art_court, "apartment": art_apartment,
            "sanofi_card": art_sanofi_card, "trophy": art_trophy,
            "fire2": art_fire2, "blast": art_blast, "quake2": art_quake2,
            "bus": art_bus, "dow": art_dow, "rocket": art_rocket,
            "flag": art_flag}


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
        d.ellipse([px - 5.5, py - 5.5, px + 5.5, py + 5.5], fill=col,
                  outline=(255, 255, 255), width=1)
        t = str(n)
        tw = d.textlength(t, font=sans_b(7))
        d.text((px - tw / 2, py - 4), t, font=sans_b(7),
               fill=(255, 255, 255))

# --- cards: no boxes, thin region rule on top, art panel, serif headline ---

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
    # full-width art panel with number callout banner inside
    CARD_ART[s["art"]](d, x, y + 28, w, 62)
    hf = serif_b(14)
    lines = wrap(d, s["head"], hf, w)[:2]
    yy = text_block(d, x, y + 94, lines, hf, INK, leading=16)
    blines = wrap(d, s["body"], sans(9), w)[:2]
    yy = text_block(d, x, yy + 3, blines, sans(9), (60, 58, 52),
                    leading=11)
    d.text((x, yy + 3), s["src"], font=sans(8), fill=GREY)


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

    # count line, small caps, centred (shrink to 9pt if it overflows)
    cnt = "38 STORIES, ALL FROM TUESDAY 24 NOV \u00b7 " + " \u00b7 ".join(
        f"{n} {c}" for n, c in REGIONS)
    f_cnt = sans_b(10)
    if d.textlength(cnt, font=f_cnt) > CW:
        f_cnt = sans_b(9)
    centred(d, W // 2, 104, cnt, f_cnt, INK)
    hline(d, M, W - M, 120)

    # sub-headline: italic serif, red diamonds between items
    parts = ["Houthi drone hits Riyadh tower",
             "China probes Shanghai party chief",
             "US jury finds Huawei guilty"]
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
        fnum = serif_black(32)
        if d.textlength(num, font=fnum) > cw - 16:
            fnum = serif_black(28)
        d.text((cx0 + 8, 158), num, font=fnum, fill=INK)
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

    # map + also-on list (25 items, 2 columns: 14-26 / 27-38)
    my = 844
    draw_map(d, M, my, 336, 108)
    lx = M + 352
    col_w = (W - M - lx - 10) // 2
    for i, (n, head, src) in enumerate(ALSO):
        col = i // 13
        row = i % 13
        ax = lx + col * (col_w + 10)
        ay = 840 + row * 9
        d.text((ax, ay), str(n), font=sans_b(8), fill=RED)
        d.text((ax + 20, ay), head, font=sans(8), fill=INK)
        sw = d.textlength(src, font=sans(8))
        d.text((ax + col_w - sw, ay + 1), src, font=sans(8), fill=GREY)

    # DATE CHECK: thin red rule, flowing text with named dates
    dy = 958
    d.line([(M, dy), (W - M, dy)], fill=RED, width=1)
    d.text((M, dy + 5), "DATE CHECK", font=sans_b(10), fill=RED)
    dc = ("Every story here happened or was first reported Tue 24 Nov 2026. "
          "Left out \u2014 Nvidia's +31% jump (Mon 23 Nov; Tue: shares fell 5.9%) "
          "\u00b7 EU's 22nd sanctions (Mon 23 Nov) \u00b7 Medvedev nuclear warning "
          "(Mon 23 Nov) \u00b7 UK's Rohingya sanctions (Mon 23 Nov) \u00b7 AWACS for "
          "Poland (decided Mon 23 Nov) \u00b7 Merkury sinking (Sun 22 Nov; UNSMIL "
          "probe call Mon 23 Nov) \u00b7 COP31 collapse (Sun 22 Nov) \u00b7 Serang "
          "fire itself (Sat 21 Nov; Tue's news: toll of 26) \u00b7 Huang "
          "reinstated (Mon 23 Nov). Not yet \u2014 Shenzhen-24 launch (Wed 25 Nov) "
          "\u00b7 Solomons\u2013Australia treaty signing (Wed 25 Nov).")
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
            "wires \u00b7 ONGOING still unfolding \u00b7 v4 \u00b7 38 stories",
            sans(8), GREY)

    img.save(OUT, format="PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    render()
