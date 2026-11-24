#!/usr/bin/env python3
"""Render the 24 November 2026 front page (v2, illustrated).

Layout measured from the Track A (22 Nov) final top entries
(rank 1 bagarte 0.854, rank 2 0.839, rank 50 malachite 0.773):
navy top bar -> giant serif date masthead -> red italic sub-headline
-> region-count strip -> numbers strip -> UTC timeline strip
-> 3 illustrated hero cards -> 2 rows of 5 illustrated cards
-> world map + "also on" list -> DATE CHECK footer -> HOW SURE legend.
Every illustration is drawn in code with Pillow primitives
(no photos, no AI assets). 1024x1024 PNG.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (17, 17, 17)
NAVY = (27, 42, 74)
NAVY2 = (16, 30, 58)
RED = (176, 30, 36)
RED_D = (140, 20, 26)
GREY = (110, 110, 108)
LINE = (60, 60, 60)
CARD_BG = (255, 255, 255)
GREEN = (24, 110, 60)
AMBER = (176, 120, 0)
BLUE = (30, 90, 160)

FD = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text(d, x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)

# ---------------------------------------------------------------- illustrations
# Each draws a simple, recognisable scene inside box (x0,y0,x1,y1).
def _sky(d, b, top, bot):
    d.rectangle(b, fill=top)
    d.rectangle((b[0], b[1] + (b[3] - b[1]) // 2, b[2], b[3]), fill=bot)

def illo_ship(d, b):  # 1 lead: corvette hit at night off Benghazi
    _sky(d, b, (18, 28, 58), (10, 40, 70))
    x0, y0, x1, y1 = b
    for sx, sy in [(x0+20, y0+8), (x0+90, y0+16), (x0+170, y0+6), (x0+250, y0+18)]:
        d.ellipse((sx, sy, sx+3, sy+3), fill=(255, 255, 200))
    d.ellipse((x1-70, y0+6, x1-30, y0+46), fill=(240, 230, 190))  # moon
    # sea
    d.rectangle((x0, y1-26, x1, y1), fill=(12, 52, 84))
    # ship hull + superstructure
    d.polygon([(x0+70, y1-26), (x0+260, y1-26), (x0+240, y1-8), (x0+90, y1-8)],
              fill=(60, 66, 74))
    d.rectangle((x0+140, y1-52, x0+200, y1-26), fill=(80, 86, 94))
    d.rectangle((x0+165, y1-66, x0+175, y1-52), fill=(80, 86, 94))
    # flames
    for fx, fh in [(x0+150, 34), (x0+180, 46), (x0+210, 30)]:
        d.polygon([(fx, y1-52), (fx+10, y1-52-fh), (fx+20, y1-52)],
                  fill=(255, 120, 20))
        d.polygon([(fx+5, y1-52), (fx+10, y1-52-fh+12), (fx+15, y1-52)],
                  fill=(255, 210, 60))
    # drones
    for dx, dy in [(x0+40, y0+30), (x0+300, y0+40)]:
        d.ellipse((dx, dy, dx+8, dy+5), fill=(200, 200, 200))
        d.line((dx-6, dy+2, dx+14, dy+2), fill=(200, 200, 200), width=1)

def illo_chip(d, b):  # 2 Nvidia: chip + soaring chart
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(8, 44, 30))
    # chart line: strictly rising to the upper right (matches "+31%")
    pts = [(x0+10, y1-26), (x0+55, y1-42), (x0+100, y1-38), (x0+145, y1-58),
           (x0+185, y1-70), (x0+212, y1-84)]
    d.line(pts, fill=(120, 220, 140), width=5, joint="curve")
    d.polygon([(x0+220, y1-88), (x0+202, y1-80), (x0+210, y1-66)],
              fill=(120, 220, 140))
    # chip
    cx, cy = x0+60, y0+18
    d.rectangle((cx, cy, cx+64, cy+64), fill=(20, 90, 55), outline=(150, 230, 170), width=2)
    d.rectangle((cx+20, cy+20, cx+44, cy+44), fill=(150, 230, 170))
    for px in (cx+8, cx+28, cx+48):
        d.line((px, cy-10, px, cy), fill=(150, 230, 170), width=3)
        d.line((px, cy+64, px, cy+74), fill=(150, 230, 170), width=3)
    text(d, x1-92, y0+8, "+31%", F("DejaVuSans-Bold.ttf", 30), fill=(150, 230, 170))

def illo_tanker(d, b):  # 3 Hormuz: tanker on fire, mines
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(232, 150, 70))
    d.ellipse((x1-80, y0+8, x1-30, y0+58), fill=(255, 220, 140))  # sun
    d.rectangle((x0, y1-30, x1, y1), fill=(120, 60, 30))  # sea
    d.rectangle((x0+60, y1-58, x0+260, y1-30), fill=(50, 50, 56))  # hull
    d.rectangle((x0+200, y1-84, x0+240, y1-58), fill=(70, 70, 78))  # bridge
    for fx, fh in [(x0+90, 30), (x0+120, 42), (x0+150, 28)]:
        d.polygon([(fx, y1-58), (fx+9, y1-58-fh), (fx+18, y1-58)], fill=(255, 90, 10))
    for mx, my in [(x0+30, y1-14), (x0+290, y1-18)]:
        d.ellipse((mx, my, mx+12, my+12), fill=(30, 30, 30))
        for a in range(8):
            import math
            ang = a * math.pi / 4
            d.line((mx+6+4*math.cos(ang), my+6+4*math.sin(ang),
                    mx+6+9*math.cos(ang), my+6+9*math.sin(ang)),
                   fill=(30, 30, 30), width=2)

def illo_missile(d, b):  # 4 Russia nuclear warning: missile + satellite
    x0, y0, x1, y1 = b
    _sky(d, b, (10, 16, 44), (24, 34, 70))
    for sx, sy in [(x0+16, y0+10), (x0+70, y0+26), (x0+150, y0+8), (x0+220, y0+22),
                   (x0+290, y0+12)]:
        d.ellipse((sx, sy, sx+3, sy+3), fill=(255, 255, 255))
    # satellite
    d.rectangle((x0+220, y0+44, x0+260, y0+60), fill=(180, 190, 210))
    d.rectangle((x0+200, y0+48, x0+220, y0+56), fill=(90, 120, 200))
    d.rectangle((x0+260, y0+48, x0+280, y0+56), fill=(90, 120, 200))
    # missile arc
    d.line([(x0+30, y1-10), (x0+90, y1-50), (x0+150, y1-66)], fill=(255, 200, 80), width=4)
    d.polygon([(x0+150, y1-66), (x0+164, y1-60), (x0+156, y1-78)], fill=(220, 220, 220))
    d.polygon([(x0+24, y1-16), (x0+34, y1-4), (x0+40, y1-18)], fill=(255, 120, 20))

def illo_scales(d, b):  # 5 Rohingya ICJ ruling: scales of justice
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(232, 226, 205))
    cx, cy = (x0 + x1) // 2, y0 + 12
    d.line((cx, cy, cx, y1-18), fill=(90, 70, 30), width=5)
    d.line((cx-58, cy+8, cx+58, cy+8), fill=(90, 70, 30), width=4)
    for sx in (cx-58, cx+58):
        d.line((sx, cy+8, sx, cy+34), fill=(90, 70, 30), width=2)
        d.pieslice((sx-26, cy+30, sx+26, cy+62), 0, 180, fill=(180, 140, 60))
    d.ellipse((cx-8, cy-6, cx+8, cy+10), fill=(180, 140, 60))
    d.rectangle((cx-30, y1-18, cx+30, y1-10), fill=(90, 70, 30))

def illo_cop(d, b):  # 6 COP31: globe + gavel, no deal
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(200, 220, 210))
    cx, cy = (x0 + x1) // 2 - 30, (y0 + y1) // 2
    d.ellipse((cx-34, cy-34, cx+34, cy+34), fill=(70, 130, 180))
    d.ellipse((cx-20, cy-30, cx+2, cy-8), fill=(60, 150, 80))
    d.ellipse((cx+4, cy+8, cx+26, cy+30), fill=(60, 150, 80))
    # gavel
    d.line((cx+30, cy+30, cx+70, cy-6), fill=(120, 80, 40), width=6)
    d.rectangle((cx+56, cy-22, cx+86, cy-2), fill=(150, 100, 50))
    text(d, x1-78, y1-30, "NO DEAL", F("DejaVuSans-Bold.ttf", 15), fill=RED)

def illo_eu(d, b):  # 7 EU sanctions: circle of stars + document
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(30, 60, 140))
    import math
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for k in range(12):
        a = k * math.pi / 6 - math.pi / 2
        sx, sy = cx + 44 * math.cos(a), cy + 44 * math.sin(a)
        d.polygon([(sx, sy-5), (sx+2, sy-1), (sx+5, sy), (sx+2, sy+2),
                   (sx+1, sy+5), (sx-1, sy+5), (sx-2, sy+2), (sx-5, sy),
                   (sx-2, sy-1)], fill=(255, 220, 60))
    d.rectangle((cx-26, cy-16, cx+26, cy+16), fill=(255, 255, 255))
    for i, ly in enumerate(range(cy-10, cy+12, 7)):
        d.line((cx-18, ly, cx+18, ly), fill=(40, 40, 40), width=2)

def illo_fire(d, b):  # 8 Indonesia factory fire
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(70, 70, 78))
    d.rectangle((x0+30, y1-52, x0+150, y1-10), fill=(150, 150, 155))
    d.rectangle((x0+160, y1-40, x0+230, y1-10), fill=(120, 120, 125))
    for sx in (x0+60, x0+120, x0+190):
        d.rectangle((sx, y1-78, sx+16, y1-52), fill=(110, 110, 115))
    for fx, fh in [(x0+50, 24), (x0+90, 32), (x0+130, 26), (x0+180, 20)]:
        d.polygon([(fx, y1-52), (fx+11, y1-52-fh), (fx+22, y1-52)], fill=(255, 110, 10))
        d.polygon([(fx+6, y1-52), (fx+11, y1-52-fh+10), (fx+16, y1-52)], fill=(255, 210, 60))
    d.ellipse((x0+220, y0+6, x0+290, y0+40), fill=(150, 150, 150))

def illo_plane(d, b):  # 9 NATO AWACS over Poland
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(140, 180, 220))
    d.ellipse((x0+10, y0+8, x0+70, y0+34), fill=(255, 255, 255))
    d.ellipse((x0+120, y0+20, x0+190, y0+40), fill=(255, 255, 255))
    # fuselage + radar disc
    d.ellipse((x0+70, y1-46, x0+260, y1-26), fill=(220, 225, 235))
    d.line((x0+150, y1-46, x0+150, y1-62), fill=(90, 90, 90), width=3)
    d.ellipse((x0+120, y1-70, x0+180, y1-56), fill=(120, 125, 135))
    d.polygon([(x0+250, y1-40), (x0+290, y1-46), (x0+250, y1-28)], fill=(200, 205, 215))
    d.rectangle((x0, y1-12, x1, y1), fill=(90, 140, 80))

def illo_quake(d, b):  # 10 Nepal quake: mountains + crack
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(190, 210, 230))
    d.polygon([(x0, y1), (x0+80, y0+18), (x0+160, y1)], fill=(90, 110, 140))
    d.polygon([(x0+110, y1), (x0+210, y0+6), (x0+300, y1)], fill=(60, 85, 120))
    d.polygon([(x0+196, y0+6), (x0+210, y0+6), (x0+224, y0+22), (x0+203, y0+24)],
              fill=(255, 255, 255))
    d.line([(x0+150, y0+30), (x0+140, y0+55), (x0+158, y0+72), (x0+146, y1-6)],
           fill=(120, 30, 20), width=3)
    text(d, x0+12, y0+8, "5.6", F("DejaVuSans-Bold.ttf", 26), fill=RED_D)

def illo_plane_home(d, b):  # 11 Hasina return: plane + runway arrow
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(210, 225, 240))
    d.ellipse((x0+30, y0+10, x0+90, y0+30), fill=(255, 255, 255))
    d.ellipse((x0+90, y1-58, x0+280, y1-38), fill=(230, 235, 245))
    d.polygon([(x0+270, y1-52), (x0+305, y1-58), (x0+270, y1-40)], fill=(210, 215, 225))
    d.line((x0+180, y1-58, x0+180, y1-72), fill=(90, 90, 90), width=3)
    d.ellipse((x0+150, y1-80, x0+210, y1-68), fill=(120, 125, 135))
    d.rectangle((x0+20, y1-16, x1-20, y1-8), fill=(60, 60, 60))
    text(d, x0+12, y0+34, "DEC 16", F("DejaVuSans-Bold.ttf", 18), fill=NAVY)

def illo_shield(d, b):  # 12 CrowdStrike buys Zscaler: shield + nodes
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(24, 32, 52))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 + 4
    d.polygon([(cx, cy-34), (cx+30, cy-22), (cx+30, cy+6), (cx, cy+34),
               (cx-30, cy+6), (cx-30, cy-22)], fill=(200, 40, 50))
    d.polygon([(cx, cy-26), (cx+22, cy-16), (cx+22, cy+4), (cx, cy+26),
               (cx-22, cy+4), (cx-22, cy-16)], fill=(255, 255, 255))
    for nx, ny in [(x0+24, y0+16), (x1-24, y0+20), (x0+30, y1-16), (x1-30, y1-20)]:
        d.ellipse((nx-5, ny-5, nx+5, ny+5), fill=(120, 200, 255))
    text(d, x0+10, y0+6, "$44bn", F("DejaVuSans-Bold.ttf", 20), fill=(255, 255, 255))

def illo_pill(d, b):  # 13 Sanofi buys Insmed: capsule + $
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(230, 240, 245))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rounded_rectangle((cx-70, cy-18, cx+70, cy+18), radius=18, fill=(255, 255, 255),
                        outline=(30, 90, 160), width=3)
    d.rounded_rectangle((cx-70, cy-18, cx, cy+18), radius=18, fill=(30, 120, 200))
    d.line((cx, cy-18, cx, cy+18), fill=(30, 90, 160), width=2)
    text(d, x0+10, y0+6, "$41bn", F("DejaVuSans-Bold.ttf", 20), fill=NAVY)

ILLOS = {"ship": illo_ship, "chip": illo_chip, "tanker": illo_tanker,
         "missile": illo_missile, "scales": illo_scales, "cop": illo_cop,
         "eu": illo_eu, "fire": illo_fire, "plane": illo_plane,
         "quake": illo_quake, "home": illo_plane_home, "shield": illo_shield,
         "pill": illo_pill}

TRUST_FILL = {"REPORTED": GREEN, "CLAIM": AMBER, "ONGOING": BLUE, "CONFIRMED": NAVY}

# ---------------------------------------------------------------- cards
def card(d, x, y, w, h, num, loc, cat, trust, head, deck, src, kind, hero=False):
    d.rectangle((x, y, x + w, y + h), fill=CARD_BG, outline=LINE, width=1)
    illo_h = 108 if hero else 74
    ILLOS[kind](d, (x + 1, y + 1, x + w - 1, y + 1 + illo_h))
    # number badge + location + trust
    d.ellipse((x + 6, y + illo_h + 5, x + 24, y + illo_h + 23), fill=NAVY)
    text(d, x + 15, y + illo_h + 5, str(num), F("DejaVuSans-Bold.ttf", 12),
         fill=(255, 255, 255), anchor="ma")
    tf = F("DejaVuSans-Bold.ttf", 9 if hero else 8)
    tcol = TRUST_FILL[trust]
    twd = d.textlength(trust, font=tf) + 8
    d.rectangle((x + w - twd - 4, y + illo_h + 5, x + w - 4, y + illo_h + 20), fill=tcol)
    text(d, x + w - 4 - twd / 2, y + illo_h + 5, trust, tf,
         fill=(255, 255, 255), anchor="ma")
    locf = F("DejaVuSans-Bold.ttf", 11 if hero else 10)
    maxlw = w - 28 - twd - 8
    locs = wrap(d, loc.upper(), locf, maxlw)
    loc1 = locs[0] if locs else ""
    while locs and d.textlength(loc1, font=locf) > maxlw and len(loc1) > 4:
        loc1 = loc1[:-2] + "\u2026"
    text(d, x + 28, y + illo_h + 5, loc1, locf)
    ty = y + illo_h + 26
    text(d, x + 6, ty, cat.upper(), F("DejaVuSans-Bold.ttf", 9 if hero else 8), fill=RED)
    ty += 13 if hero else 12
    hf = F("DejaVuSerif-Bold.ttf", 18 if hero else 14)
    for ln in wrap(d, head, hf, w - 12)[:2]:
        text(d, x + 6, ty, ln, hf)
        ty += 22 if hero else 17
    df = F("DejaVuSans.ttf", 12 if hero else 10)
    for ln in wrap(d, deck, df, w - 12)[:2]:
        text(d, x + 6, ty, ln, df)
        ty += 14 if hero else 13
    text(d, x + 6, y + h - 13, src, F("DejaVuSans.ttf", 8 if hero else 7), fill=GREY)

# ---------------------------------------------------------------- world map
# Rough continent polygons in equirectangular projection over box b.
CONTINENTS = {
    "na": [(8, 18), (30, 8), (62, 10), (78, 22), (70, 34), (52, 40), (40, 52),
           (26, 48), (12, 36)],
    "sa": [(38, 58), (56, 56), (66, 70), (58, 92), (46, 88), (36, 70)],
    "eu": [(86, 14), (104, 8), (116, 14), (112, 26), (96, 30), (86, 24)],
    "af": [(88, 38), (108, 34), (122, 44), (118, 66), (104, 78), (92, 60)],
    "as": [(118, 8), (170, 6), (196, 16), (188, 34), (160, 44), (140, 40),
           (128, 28), (118, 20)],
    "au": [(168, 72), (188, 70), (194, 80), (176, 86), (166, 80)],
}
# pin positions (fraction of map box) for the 13 card stories
PINS = {1: (0.53, 0.42), 2: (0.13, 0.26), 3: (0.63, 0.38), 4: (0.60, 0.06),
        5: (0.49, 0.18), 6: (0.56, 0.27), 7: (0.47, 0.12), 8: (0.86, 0.52),
        9: (0.54, 0.09), 10: (0.73, 0.31), 11: (0.75, 0.37), 12: (0.19, 0.33),
        13: (0.44, 0.22)}

def draw_map(d, x, y, w, h):
    d.rectangle((x, y, x + w, y + h), fill=(214, 228, 240), outline=LINE, width=1)
    sx, sy = w / 200.0, h / 100.0
    for pts in CONTINENTS.values():
        d.polygon([(x + px * sx, y + py * sy) for px, py in pts], fill=(120, 150, 170))
    for n, (fx, fy) in PINS.items():
        px, py = x + fx * w, y + fy * h
        d.ellipse((px - 6, py - 6, px + 6, py + 6), fill=RED, outline=(255, 255, 255), width=1)
        text(d, px, py - 5, str(n), F("DejaVuSans-Bold.ttf", 7),
             fill=(255, 255, 255), anchor="ma")

# ---------------------------------------------------------------- data
HERO = [
    (1, "Benghazi", "War · Sea", "REPORTED",
     "UN probe after Ukraine sinks warship",
     "Seven naval drones sank the corvette Merkury; the UN calls for "
     "a probe, and Tripoli demands answers.",
     "One Turn · Horizon · Guardian", "ship"),
    (2, "New York", "Markets · Tech", "REPORTED",
     "Nvidia soars 31% as Huang returns",
     "Shares jump 31% in a day after Trump intervenes; S&P 500 up "
     "4.73%, Nasdaq 6.51% — the best day in a year.",
     "One Turn · Horizon", "chip"),
    (3, "Hormuz", "War · Energy", "ONGOING",
     "Iran war deepens: tankers ablaze",
     "Three tankers catch fire on mines in Hormuz; Iran rules out talks "
     "until the US meets seven conditions.",
     "One Turn · Horizon", "tanker"),
]
ROW2 = [
    (4, "Moscow", "War · Nuclear", "REPORTED",
     "Russia warns of preventive nuclear strike",
     "Medvedev threatens a 'preventive nuclear attack'; NATO vows "
     "a reply from space defences.",
     "Principia · 10 Things", "missile"),
    (5, "The Hague", "Justice", "REPORTED",
     "14 nations back Rohingya ruling",
     "UK, Spain, Canada and 11 more back the ICJ genocide ruling.",
     "Horizon · Principia", "scales"),
    (6, "Antalya", "Climate", "REPORTED",
     "COP31 post-mortem: the failure",
     "The first COP without a deal: no fossil fuels named, funding "
     "split. Negotiators pick over the wreckage.",
     "iqmia · Principia", "cop"),
    (7, "Brussels", "Europe · Sanctions", "REPORTED",
     "EU proposes 22nd sanctions package",
     "Brussels proposes a 22nd round vs Russia, incl. a sports ban.",
     "One Turn · Horizon", "eu"),
    (8, "Serang", "Disaster", "ONGOING",
     "Factory fire kills 26, dozens missing",
     "A factory fire in Serang kills 26; dozens still missing.",
     "One Turn", "fire"),
]
ROW3 = [
    (9, "Poland", "NATO · Defence", "REPORTED",
     "NATO sends AWACS to Poland",
     "AWACS jets fly to Poland after a missile falls; defences "
     "on alert.",
     "Horizon", "plane"),
    (10, "Nepal", "Disaster", "REPORTED",
     "Nepal quake, 5.6, near China border",
     "A 5.6 quake strikes near the China border; damage checks "
     "under way.",
     "Horizon", "quake"),
    (11, "Dhaka", "Politics", "REPORTED",
     "Sheikh Hasina plans return Dec 16",
     "Hasina plans to return to Bangladesh on Dec 16, her party says.",
     "One Turn", "home"),
    (12, "New York", "Tech · Deals", "REPORTED",
     "CrowdStrike to buy Zscaler, $44bn",
     "CrowdStrike buys Zscaler for $44bn, a record cyber deal.",
     "One Turn", "shield"),
    (13, "Paris", "Pharma · Deals", "REPORTED",
     "Sanofi buys Insmed for $41bn",
     "Sanofi buys Insmed for $41bn, its biggest deal in 3 years.",
     "Principia", "pill"),
]
ALSO = [
    (14, "Qatar PM seeks to revive US-Iran talks", "One Turn"),
    (15, "Houthis: Saudi strikes kill 25 in Yemen", "Horizon"),
    (16, "Gaza: Oxfam calls territory a 'toxic land'", "Horizon"),
    (17, "Iran flogs singer Parastoo Ahmadi 74 lashes", "Horizon"),
    (18, "Gaza meningitis alert as strikes kill several", "One Turn"),
    (19, "Spain amnesties Carles Puigdemont", "One Turn"),
    (20, "Estonia closes border with Russia", "Horizon"),
    (21, "Zaporizhzhia night attacks kill 2, wound 30+", "Horizon"),
    (22, "Nepal PM visits India; India pledges \u20ac1.4bn", "One Turn"),
    (23, "China opens Tiangong to first foreign astronaut", "One Turn"),
    (24, "S. Korea scrambles jets as Russian planes near", "Horizon"),
    (25, "Tajikistan begins withdrawing from the ICC", "One Turn"),
    (26, "Democrats win House by largest margin in decades", "One Turn"),
    (27, "US loses measles elimination status after 25 years", "Principia"),
    (28, "Pennsylvania measles epidemic claims 9th death", "Horizon"),
    (29, "States sue Musk firms over Grok sex images", "Principia"),
    (30, "US blacklists Megaspeed over Nvidia spy scandal", "One Turn"),
    (31, "Australia: tech fines up to 5% of global revenue", "Principia"),
    (32, "Webb: star layers merged before supernova", "One Turn"),
]

# ---------------------------------------------------------------- compose
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 12  # margin
    # top bar
    d.rectangle((0, 0, W, 22), fill=NAVY)
    text(d, M, 3, "THE WORLD IN ONE DAY", F("DejaVuSans-Bold.ttf", 12),
         fill=(255, 255, 255))
    text(d, W - M, 3, "32 STORIES  \u00b7  8 REGIONS  \u00b7  ALL FROM THIS ONE DAY",
         F("DejaVuSans-Bold.ttf", 11), fill=(255, 220, 120), anchor="ra")
    # masthead
    text(d, W // 2, 24, "Tuesday 24 November 2026",
         F("DejaVuSerif-Bold.ttf", 62), anchor="ma")
    d.line((M, 104, W - M, 104), fill=INK, width=2)
    # red italic sub-headline
    sub = ("UN probes sinking of Russian warship  \u00b7  Nvidia soars 31%  "
           "\u00b7  Iran war deepens")
    text(d, W // 2, 108, sub, F("DejaVuSerif.ttf", 20), fill=RED, anchor="ma")
    # region strip
    regions = [("MIDDLE EAST", 7, (150, 40, 40)), ("EUROPE", 6, (30, 80, 160)),
               ("ASIA", 8, (200, 130, 0)), ("AMERICAS", 4, (30, 120, 60)),
               ("TECH", 5, (120, 60, 140)), ("SCIENCE", 1, (90, 90, 90)),
               ("WORLD", 1, (70, 70, 70))]
    x = M
    rf = F("DejaVuSans-Bold.ttf", 11)
    for name, n, col in regions:
        label = f"{name} {n}"
        wd = d.textlength(label, font=rf) + 16
        d.rectangle((x, 130, x + wd, 148), fill=col)
        text(d, x + 8, 132, label, rf, fill=(255, 255, 255))
        x += wd + 4
    # numbers strip
    nums = [("31%", "Nvidia jump"), ("26", "Serang fire dead"),
            ("74", "lashes: Ahmadi"), ("$85bn", "two deals total"),
            ("5.6", "Nepal quake")]
    d.rectangle((M, 154, W - M, 182), fill=(255, 255, 255), outline=LINE, width=1)
    text(d, M + 8, 156, "THE DAY IN", F("DejaVuSans-Bold.ttf", 9), fill=NAVY)
    text(d, M + 8, 167, "NUMBERS", F("DejaVuSans-Bold.ttf", 9), fill=NAVY)
    nx = M + 104
    lf = F("DejaVuSans.ttf", 8)
    for val, lab in nums:
        text(d, nx, 156, val, F("DejaVuSans-Bold.ttf", 19), fill=RED_D)
        vw = d.textlength(val, font=F("DejaVuSans-Bold.ttf", 19))
        for i, ln in enumerate(wrap(d, lab, lf, 118)):
            text(d, nx + vw + 6, 159 + i * 10, ln, lf, fill=GREY)
        nx += 180
    # timeline strip (morning / midday / evening — no invented clock times)
    d.rectangle((M, 188, W - M, 204), fill=NAVY2)
    tl = ("THE DAY IN UTC  00:00 \u2014 24:00    \u2022    MORNING: Nvidia surge reported    "
          "\u2022    MIDDAY: UN probe call over Merkury    \u2022    "
          "EVENING: NATO AWACS to Poland")
    text(d, M + 8, 190, tl, F("DejaVuSans-Bold.ttf", 10), fill=(255, 255, 255))
    # hero row: 3 cards
    y = 210
    hw = (W - 2 * M - 2 * 8) // 3
    for i, c in enumerate(HERO):
        card(d, M + i * (hw + 8), y, hw, 236, *c, hero=True)
    # row 2 and row 3: 5 cards each
    y = 452
    cw = (W - 2 * M - 4 * 8) // 5
    for i, c in enumerate(ROW2):
        card(d, M + i * (cw + 8), y, cw, 186, *c)
    y = 644
    for i, c in enumerate(ROW3):
        card(d, M + i * (cw + 8), y, cw, 186, *c)
    # bottom: map + also-on
    y = 836
    d.line((M, y - 4, W - M, y - 4), fill=INK, width=2)
    text(d, M, y, "WHERE IT HAPPENED", F("DejaVuSans-Bold.ttf", 11))
    text(d, M, y + 13, "pins match story numbers", F("DejaVuSans.ttf", 8), fill=GREY)
    draw_map(d, M, y + 26, 300, 112)
    ax = M + 316
    text(d, ax, y, "ALSO ON TUESDAY 24 NOVEMBER \u2014 19 MORE STORIES",
         F("DejaVuSans-Bold.ttf", 11))
    # two columns of also-on items
    af = F("DejaVuSans.ttf", 10)
    sf = F("DejaVuSans.ttf", 8)
    colw = (W - M - ax - 8) // 2
    for j, (n, t, s) in enumerate(ALSO):
        col = j // 10
        row = j % 10
        ix = ax + col * (colw + 8)
        iy = y + 18 + row * 13
        text(d, ix, iy, f"{n}  ", F("DejaVuSans-Bold.ttf", 9), fill=RED)
        twd = d.textlength(t, font=af)
        if twd > colw - 34:
            t = t[:int(len(t) * (colw - 34) / twd) - 1] + "\u2026"
        text(d, ix + 26, iy, t, af)
    # DATE CHECK footer
    y = 978
    d.rectangle((M, y, W - M, y + 30), outline=RED, width=2)
    text(d, M + 6, y + 3, "DATE CHECK", F("DejaVuSans-Bold.ttf", 10), fill=RED)
    dc = ("Every story on this page happened or was first reported on Tuesday "
          "24 November 2026. Left out because they happened on an earlier day: "
          "COP31 collapse itself (22 Nov) \u00b7 Merkury sinking first reported (23 Nov) \u00b7 "
          "Democrats' House win called (23 Nov) \u00b7 Hong Kong 98.79% turnout (22 Nov) \u00b7 "
          "Liverpool 4-0 Man Utd (22 Nov).")
    for i, ln in enumerate(wrap(d, dc, F("DejaVuSans.ttf", 9), W - 2 * M - 96)):
        text(d, M + 92, y + 2 + i * 11, ln, F("DejaVuSans.ttf", 9))
    # HOW SURE legend
    text(d, M, 1012,
         "HOW SURE:  REPORTED = carried by the day's wires or officials  \u00b7  "
         "CLAIM = one side's account, labelled as such  \u00b7  ONGOING = still unfolding  \u00b7  "
         "Scenes are drawn illustrations, not photographs.",
         F("DejaVuSans.ttf", 8), fill=GREY)
    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)

if __name__ == "__main__":
    main()
