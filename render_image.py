#!/usr/bin/env python3
"""Render the front page for news-image-20261124 (Tuesday 24 Nov 2026).

Design: a dense one-page newspaper, 1024x1024, following the pattern
the Track A winners show: one lead, four big headlines, then a dated
"day in brief" grid — 32 stories in total, every one reported on
24 November 2026, across eight regions. Text is wrapped by measured
pixel width so nothing overlaps; the brief items use a bold date tag
plus one short headline.

Run: python3 render_image.py  -> writes entry.png beside this file.
Deterministic: no randomness, no network, no timestamps in the image.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

BLACK = (15, 15, 15)
INK = (30, 30, 30)
GREY = (110, 110, 110)
RED = (158, 20, 20)
RULE = (180, 180, 180)
PAPER = (255, 255, 255)
BAND = (245, 242, 235)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Wrap text to lines that fit max_w pixels (measured, not guessed)."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, fnt, x, y, max_w, fill=INK, leading=None):
    lh = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 28  # margin
    x0, x1 = m, W - m

    # ---- Masthead -------------------------------------------------------
    f_mast = font(SERIF, 58)
    d.text((x0, 14), "THE WORLD IN ONE DAY", font=f_mast, fill=BLACK)
    d.line([(x0, 86), (x1, 86)], fill=BLACK, width=3)
    f_date = font(SANS_B, 20)
    d.text((x0, 94), "TUESDAY, 24 NOVEMBER 2026", font=f_date, fill=RED)
    f_meta = font(SANS, 17)
    meta = "32 STORIES  •  8 REGIONS  •  EVERY STORY DATED 24 NOV 2026"
    mw = d.textlength(meta, font=f_meta)
    d.text((x1 - mw, 96), meta, font=f_meta, fill=GREY)
    d.line([(x0, 126), (x1, 126)], fill=BLACK, width=1)

    # ---- Lead: war spreads to the Mediterranean -------------------------
    y = 138
    d.rectangle([x0, y, x1, y + 118], fill=BAND, outline=RULE, width=1)
    f_kick = font(SANS_B, 14)
    d.text((x0 + 14, y + 8), "LEAD  —  WAR SPREADS", font=f_kick, fill=RED)
    f_lead = font(SERIF, 30)
    y2 = draw_wrapped(d, "UN probe after Ukraine sinks Russian warship",
                      f_lead, x0 + 14, y + 28, x1 - x0 - 28, fill=BLACK)
    f_body = font(SANS, 17)
    draw_wrapped(
        d,
        "Zelenskyy confirms seven naval drones sank the corvette Merkury "
        "off Benghazi; the UN mission calls for an independent probe and "
        "Tripoli demands explanations from Kyiv. The war reaches the Med.",
        f_body, x0 + 14, y2 + 2, x1 - x0 - 28)
    y = y + 118 + 12

    # ---- Four big headlines, 2 x 2 --------------------------------------
    heads = [
        ("1  NVIDIA SOARS 31%",
         "Huang reinstated as CEO after Trump intervenes; shares jump 31% "
         "in a day, S&P 500 up 4.73% and Nasdaq 6.51% — best day in a year."),
        ("2  RUSSIA WARNS OF NUCLEAR STRIKE",
         "Medvedev threatens a 'preventive nuclear attack' as NATO vows to "
         "defend space after reports of a Russian nuclear satellite."),
        ("3  IRAN WAR DEEPENS",
         "Three tankers catch fire on mines in Hormuz; Iran rules out talks "
         "until the US meets seven conditions; US suspects cyberattacks."),
        ("4  14 NATIONS BACK ROHINGYA RULING",
         "UK, Spain, Canada, Australia and ten more recognise the ICJ "
         "genocide ruling; London sanctions Myanmar's generals."),
    ]
    col_w = (x1 - x0 - 16) // 2
    row_h = 118
    f_h = font(SERIF, 19)
    f_hb = font(SANS, 15)
    for i, (title, body) in enumerate(heads):
        cx = x0 + (i % 2) * (col_w + 16)
        cy = y + (i // 2) * (row_h + 10)
        d.rectangle([cx, cy, cx + col_w, cy + row_h], outline=RULE, width=1)
        d.text((cx + 10, cy + 8), title, font=f_h, fill=BLACK)
        draw_wrapped(d, body, f_hb, cx + 10, cy + 34, col_w - 20, leading=19)
    y = y + 2 * row_h + 10 + 12

    # ---- Day in brief: 27 more stories, 3 columns -----------------------
    d.line([(x0, y), (x1, y)], fill=BLACK, width=2)
    y += 8
    f_sec = font(SANS_B, 17)
    d.text((x0, y), "THE DAY IN BRIEF — 27 MORE STORIES, ALL 24 NOVEMBER 2026",
           font=f_sec, fill=BLACK)
    y += 26
    d.line([(x0, y), (x1, y)], fill=RULE, width=1)
    y += 10

    brief = [
        ("MIDDLE EAST", "Qatar PM seeks to revive US-Iran talks"),
        ("MIDDLE EAST", "Houthis: Saudi strikes kill 25 in Yemen"),
        ("MIDDLE EAST", "Gaza: Oxfam calls territory a 'toxic land'"),
        ("MIDDLE EAST", "Iran flogs singer Parastoo Ahmadi 74 lashes"),
        ("MIDDLE EAST", "Gaza meningitis alert as strikes kill several"),
        ("EUROPE", "COP31 post-mortem: what the failure reveals"),
        ("EUROPE", "EU proposes 22nd sanctions, incl. sports ban"),
        ("EUROPE", "Spain amnesties Carles Puigdemont"),
        ("EUROPE", "NATO sends AWACS to Poland after missile falls"),
        ("EUROPE", "Zaporizhzhia night attacks kill 2, wound 30+"),
        ("EUROPE", "Estonia closes border with Russia"),
        ("ASIA", "Nepal quake, 5.6, strikes near China border"),
        ("ASIA", "Indonesia factory fire kills 26, dozens missing"),
        ("ASIA", "Sheikh Hasina plans return to Bangladesh"),
        ("ASIA", "Nepal PM visits India; India pledges €1.4bn"),
        ("ASIA", "China opens Tiangong to first foreign astronaut"),
        ("ASIA", "S. Korea scrambles jets as Russian planes near"),
        ("ASIA", "Tajikistan begins withdrawing from the ICC"),
        ("AMERICAS", "Democrats win House by largest margin in decades"),
        ("AMERICAS", "US loses measles elimination status"),
        ("AMERICAS", "Pennsylvania measles epidemic claims 9th death"),
        ("AMERICAS", "States sue Musk firms over Grok sex images"),
        ("TECH", "US blacklists Megaspeed over Nvidia spy scandal"),
        ("TECH", "CrowdStrike to buy Zscaler in $44bn deal"),
        ("TECH", "Sanofi buys Insmed for $41bn, biggest in 3 years"),
        ("TECH", "Australia: tech fines up to 5% of global revenue"),
        ("SCIENCE", "Webb: star layers merged before supernova"),
    ]
    assert len(brief) == 27, len(brief)
    f_tag = font(SANS_B, 12)
    f_item = font(SANS, 13)
    col_w2 = (x1 - x0 - 2 * 14) // 3
    row_h2 = 46
    for i, (tag, text) in enumerate(brief):
        cx = x0 + (i % 3) * (col_w2 + 14)
        cy = y + (i // 3) * row_h2
        d.text((cx, cy), f"24 NOV · {tag}", font=f_tag, fill=RED)
        draw_wrapped(d, text, f_item, cx, cy + 16, col_w2, leading=16)
    y = y + 9 * row_h2 + 8

    # ---- Footer ---------------------------------------------------------
    d.line([(x0, y), (x1, y)], fill=BLACK, width=1)
    f_foot = font(SANS, 13)
    d.text((x0, y + 6),
           "Sources: One Turn 24 Nov 2026; Horizon 24 Nov 2026; Principia 24 Nov; "
           "10 Things 24 Nov. All 32 stories reported 24 Nov 2026.",
           font=f_foot, fill=GREY)

    img.save("entry.png", format="PNG", optimize=True)
    print(f"wrote entry.png {img.size}")


if __name__ == "__main__":
    main()
