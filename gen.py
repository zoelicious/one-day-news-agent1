#!/usr/bin/env python3
"""Build entry.png for make.fun news-image-20261121 (Agent 1, hero Riyadh).

Draws a one-page cream newspaper in code (PIL only): masthead, date,
stat strip, region bar (sums to 35), 13 numbered illustrated panels
(3 heroes + 10 small), world map with pins 1-13, ALSO list 14-35,
THE VERDICT sidebar-strip, DATE CHECK box, footer + HOW WE CHECKED.
Deterministic: same bytes on every run.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024
CREAM = (247, 242, 231)
PAPER = (255, 253, 247)
INK = (26, 24, 22)
GRAY = (110, 105, 95)
RED = (176, 30, 36)
DARKRED = (140, 22, 28)
LINE = (180, 172, 155)
BLUE = (40, 90, 160)
GREEN = (35, 120, 60)
AMBER = (168, 108, 0)

F_SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
F_SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
F_SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center(d, y, text, fnt, fill, x0=0, x1=W):
    w = d.textlength(text, font=fnt)
    d.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)


def block(d, x, y, lines, fnt, fill, leading):
    for i, ln in enumerate(lines):
        d.text((x, y + i * leading), ln, font=fnt, fill=fill)
    return y + len(lines) * leading


# ---------------------------------------------------------------- stories
# (num, title, deck, source, verify, illu_key, illu_bg)
PANELS = [
    (1, "THREE MISSILES DOWN OVER RIYADH",
     "Saudi-led coalition downs three Houthi missiles over the capital \u2014 the third night of alerts; two blasts heard around 02:00; no casualties.",
     "REUTERS", "CONFIRMED", "riyadh", (28, 40, 68)),
    (2, "COP31 RUNS INTO OVERTIME",
     "The climate summit in Antalya enters day 13 with no deal; a third draft that omits fossil fuels splits nearly 200 nations.",
     "AP", "REPORTED", "cop31", (186, 214, 230)),
    (3, "PERU SHAKEN BY 6.7 QUAKE",
     "A magnitude 6.7 quake strikes Jun\u00edn at 00:09 UTC, 108 km deep; no deaths reported and no tsunami.",
     "USGS", "OFFICIAL", "peru", (232, 220, 198)),
    (4, "DOUBLE-TAP HITS KRYVYI RIH",
     "Russian strike kills 2 and injures 42 in a double-tap attack.",
     "REUTERS", "REPORTED", "kryvyi", (198, 204, 210)),
    (5, "ZELENSKY: BRIDGE \u2018WILL NOT STAY\u2019",
     "Kyiv leader tells NBC the Crimea bridge \u2018will not stay\u2019.",
     "NBC", "REPORTED", "bridge", (224, 227, 234)),
    (6, "IRAN CLAIMS US DRONE DOWNED",
     "Tehran claims its 58th MQ-9 kill over Hormuz; Washington has not confirmed it.",
     "AL JAZEERA", "CLAIM", "drone", (208, 220, 224)),
    (7, "IRAN: URANIUM STAYS AT HOME",
     "Tehran says its uranium stock stays in the country and seeks a \u2018fair solution\u2019.",
     "REUTERS", "REPORTED", "atom", (240, 230, 178)),
    (8, "TRUMP VOWS TAX ON DATA CENTRES",
     "Washington: a tax on foreign data centres is coming; no details yet.",
     "AP", "REPORTED", "servers", (214, 224, 234)),
    (9, "CHINA TO JAPAN: \u2018CORRECT\u2019 TAIWAN LINE",
     "Beijing tells Tokyo to \u2018correct\u2019 its Taiwan remarks; Japan says its stance is unchanged.",
     "AFP", "REPORTED", "flags", (235, 226, 214)),
    (10, "ALL 146 SAFE IN DAVAO LANDING",
     "Air Niugini 767 lands safely in Davao; all 146 aboard safe.",
     "REUTERS", "CONFIRMED", "plane", (184, 214, 234)),
    (11, "AUSTRALIA, CHINA TO TALK AI",
     "Canberra and Beijing agree to talk on AI as Albanese ends an 11-day trip.",
     "AP", "REPORTED", "chip", (220, 230, 224)),
    (12, "BITCOIN SLIPS BELOW $59,000",
     "Bitcoin at $58,983, down 3.9% in 24 hours.",
     "MARKET DATA", "REPORTED", "bitcoin", (240, 224, 178)),
    (13, "RUSSELL FASTEST IN WET VEGAS",
     "Russell fastest in wet practice, 1:34.041; Verstappen takes pole.",
     "F1", "OFFICIAL", "f1", (224, 224, 230)),
]

ALSO = [
    (14, "Rahul 124* \u2014 India 344/2, Wellington", "OCEANIA"),
    (15, "BepiColombo reaches Mercury", "ASIA"),
    (16, "Rutte in Warsaw for NATO talks", "EUROPE"),
    (17, "Bayelsa funeral boat sinks, \u22654 dead", "AFRICA"),
    (18, "Denmark expels Russian attach\u00e9", "EUROPE"),
    (19, "ATP Turin semi: Medvedev v Zverev", "EUROPE"),
    (20, "Israel strikes Gaza, 6 killed", "MIDDLE EAST"),
    (21, "Freight train derails in Sejong", "ASIA"),
    (22, "Houthis threaten Jeddah; Hodeidah hit", "MIDDLE EAST"),
    (23, "Vance: Iran strike is Trump\u2019s call", "AMERICAS"),
    (24, "Roundup settlement, $7.25bn", "AMERICAS"),
    (25, "Texas execution takes 63 minutes", "AMERICAS"),
    (26, "Palisades fire verdict, 12 dead", "AMERICAS"),
    (27, "Youth climate hearing, Vancouver", "AMERICAS"),
    (28, "Kim visits Pyongyang factory", "ASIA"),
    (29, "Taipei passes its budget", "ASIA"),
    (30, "Bangkok arsenic clean-up plan", "ASIA"),
    (31, "SCO forum opens in New Delhi", "ASIA"),
    (32, "Fresh sanctions on Myanmar", "ASIA"),
    (33, "Starc 7/58 in Ashes at Perth", "OCEANIA"),
    (34, "First US measles death of 2026", "AMERICAS"),
    (35, "Port Louis rating agency review", "AFRICA"),
]

# Region counts: panels + ALSO. Europe 5, Asia 10, Middle East 5,
# Africa 2, Americas 9, Oceania 3, Global 1 = 35 (COP31 = Asia/Antalya,
# Bitcoin = Global, BepiColombo = Asia/JAXA).
REGIONS = [("Europe", 5, (58, 110, 165)), ("Asia", 10, (198, 90, 40)),
           ("Middle East", 5, (30, 130, 90)), ("Africa", 2, (200, 150, 40)),
           ("Americas", 9, (150, 60, 90)), ("Oceania", 3, (40, 140, 160)),
           ("Global", 1, (120, 110, 120))]
assert sum(c for _, c, _ in REGIONS) == 35

# ---------------------------------------------------------------- illustrations
def illu_riyadh(d, x, y, w, h):
    d.ellipse([x + w - 34, y + 8, x + w - 14, y + 28], fill=(235, 230, 200))
    for bx in (x + 8, x + w // 2 - 14, x + w - 52):
        d.rectangle([bx, y + h - 26, bx + 34, y + h], fill=(16, 22, 40))
        d.rectangle([bx + 8, y + h - 36, bx + 26, y + h - 26], fill=(16, 22, 40))
    for sx, sy in ((x + 40, y + 22), (x + w // 2, y + 14), (x + w - 46, y + 30)):
        d.line([sx, y + h - 26, sx + 6, sy + 8], fill=(255, 210, 90), width=2)
        for dx, dy in ((0, 0), (7, 0), (3, 6), (3, -6), (0, 7)):
            d.line([sx + 6 + dx - 2, sy + 8 + dy, sx + 6 + dx + 2, sy + 8 + dy],
                   fill=(255, 220, 120), width=2)
        d.ellipse([sx + 2, sy + 4, sx + 10, sy + 12], fill=(255, 240, 160))


def illu_cop31(d, x, y, w, h):
    cx, cy, r = x + w // 2, y + h // 2 - 4, 26
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 175, 205),
              outline=(40, 90, 140), width=2)
    d.ellipse([cx - 10, cy - r, cx + 10, cy + r], outline=(40, 90, 140), width=1)
    d.line([cx - r, cy, cx + r, cy], fill=(40, 90, 140), width=1)
    d.line([cx - r + 6, cy - 14, cx + r - 6, cy - 14], fill=(40, 90, 140), width=1)
    d.line([cx - r + 6, cy + 14, cx + r - 6, cy + 14], fill=(40, 90, 140), width=1)
    cols = [(176, 30, 36), (40, 90, 160), (35, 120, 60), (200, 150, 40),
            (150, 60, 90), (60, 120, 140)]
    for i, c in enumerate(cols):
        fx = x + 14 + i * ((w - 28) // 6)
        d.rectangle([fx, y + h - 14, fx + 12, y + h - 4], fill=c)
    d.text((x + w - 46, y + 6), "DAY 13", font=font(F_SANS_B, 9), fill=RED)


def illu_peru(d, x, y, w, h):
    d.polygon([(x, y + h), (x + w // 4, y + 12), (x + w // 2, y + h)], fill=(150, 140, 125))
    d.polygon([(x + w // 2, y + h), (x + 3 * w // 4, y + 20), (x + w, y + h)], fill=(130, 120, 105))
    pts = [(x + 6, y + h - 18)]
    for i in range(1, 9):
        pts.append((x + 6 + i * (w - 12) // 8, y + h - 18 - (10 if i % 2 else -6)))
    d.line(pts, fill=(90, 60, 40), width=2, joint="curve")
    pts2 = [(x + 6, y + 22)]
    for i in range(1, 13):
        pts2.append((x + 6 + i * (w - 12) // 12, y + 22 + (8 if i % 3 == 0 else (-8 if i % 3 == 1 else 0))))
    d.line(pts2, fill=RED, width=2, joint="curve")


def illu_kryvyi(d, x, y, w, h):
    d.rectangle([x + 10, y + 22, x + 44, y + h], fill=(120, 122, 128))
    d.polygon([(x + 54, y + 30), (x + 88, y + 18), (x + 96, y + h), (x + 54, y + h)],
              fill=(96, 98, 104))
    d.rectangle([x + 104, y + 40, x + w - 12, y + h], fill=(140, 142, 148))
    for wy in (30, 48, 66):
        d.rectangle([x + 16, y + wy, x + 26, y + wy + 8], fill=(255, 220, 130))
        d.rectangle([x + 110, y + wy, x + 120, y + wy + 8], fill=(200, 210, 220))
    for i, (sx, sy, sr) in enumerate(((x + 62, y + 10, 9), (x + 76, y + 4, 12), (x + 92, y + 10, 8))):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(170, 168, 162))


def illu_bridge(d, x, y, w, h):
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(120, 175, 205))
    d.arc([x + 8, y + 8, x + w - 8, y + h + 6], 180, 360, fill=(90, 90, 95), width=3)
    for i in range(5):
        vx = x + 18 + i * ((w - 36) // 4)
        d.line([vx, y + 22, vx, y + h - 16], fill=(90, 90, 95), width=2)
    d.rectangle([x + w // 2 - 12, y + h - 34, x + w // 2 + 12, y + h - 16], fill=(120, 80, 50))
    d.line([x + w // 2, y + h - 44, x + w // 2, y + h - 34], fill=INK, width=2)
    d.ellipse([x + w // 2 - 4, y + h - 50, x + w // 2 + 4, y + h - 42], fill=INK)


def illu_drone(d, x, y, w, h):
    cx, cy = x + w // 2, y + h // 2
    for r in (34, 24, 14):
        d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(60, 140, 90), width=2)
    d.polygon([(cx - 26, cy), (cx - 6, cy - 6), (cx + 26, cy - 3), (cx + 6, cy + 4), (cx - 6, cy + 6)],
              fill=(90, 95, 100))
    d.line([cx + 22, cy - 3, cx + 34, cy - 10], fill=(90, 95, 100), width=3)
    d.line([cx - 30, cy - 12, cx - 8, cy + 12], fill=RED, width=3)
    d.line([cx - 8, cy - 12, cx - 30, cy + 12], fill=RED, width=3)


def illu_atom(d, x, y, w, h):
    cx, cy = x + w // 2, y + h // 2
    for ang in (0, 60, 120):
        d.ellipse([cx - 30, cy - 12, cx + 30, cy + 12], outline=(60, 60, 120), width=2)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
    d.rectangle([x + w - 34, y + h - 30, x + w - 12, y + h - 6], fill=(220, 180, 40),
                outline=INK, width=1)
    d.rectangle([x + w - 34, y + h - 30, x + w - 12, y + h - 24], fill=(180, 140, 20))


def illu_servers(d, x, y, w, h):
    for i in range(3):
        rx = x + 12 + i * ((w - 24) // 3)
        d.rectangle([rx, y + 10, rx + (w - 24) // 3 - 6, y + h - 10], fill=(50, 55, 65))
        for j in range(4):
            d.rectangle([rx + 5, y + 16 + j * 14, rx + (w - 24) // 3 - 11, y + 24 + j * 14],
                        fill=(90, 100, 115))
            d.ellipse([rx + (w - 24) // 3 - 14, y + 19 + j * 14, rx + (w - 24) // 3 - 10,
                       y + 23 + j * 14], fill=(120, 220, 130))
    d.ellipse([x + w - 30, y + 4, x + w - 8, y + 26], fill=(60, 140, 80))
    d.text((x + w - 25, y + 7), "$", font=font(F_SANS_B, 13), fill=(255, 255, 255))


def illu_flags(d, x, y, w, h):
    d.rectangle([x + 10, y + 12, x + w // 2 - 4, y + h - 14], fill=(200, 30, 30))
    for sx, sy in ((x + 22, y + 22), (x + 34, y + 20), (x + 30, y + 30)):
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 220, 60))
    d.rectangle([x + w // 2 + 4, y + 12, x + w - 10, y + h - 14], fill=(250, 250, 250),
                outline=LINE, width=1)
    d.ellipse([x + w // 2 + 18, y + h // 2 - 10, x + w // 2 + 38, y + h // 2 + 10],
              fill=(200, 30, 30))
    d.line([x + w // 2 - 4, y + 8, x + w // 2 + 4, y + 8], fill=INK, width=2)


def illu_plane(d, x, y, w, h):
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(70, 70, 75))
    for i in range(6):
        d.line([x + 10 + i * 16, y + h - 6, x + 18 + i * 16, y + h - 6],
               fill=(255, 220, 90), width=2)
    cx, cy = x + w // 2, y + h // 2 - 6
    d.polygon([(cx - 34, cy), (cx + 30, cy - 6), (cx + 42, cy), (cx + 30, cy + 4),
               (cx - 20, cy + 6)], fill=(240, 240, 240), outline=(120, 120, 125))
    d.polygon([(cx - 6, cy - 4), (cx + 6, cy - 16), (cx + 12, cy - 4)], fill=(200, 205, 210))
    d.ellipse([x + 12, y + 10, x + 30, y + 28], fill=GREEN)
    d.line([x + 16, y + 19, x + 20, y + 23], fill=(255, 255, 255), width=2)
    d.line([x + 20, y + 23, x + 27, y + 14], fill=(255, 255, 255), width=2)


def illu_chip(d, x, y, w, h):
    cx, cy = x + w // 2, y + h // 2
    d.rectangle([cx - 20, cy - 18, cx + 20, cy + 18], fill=(45, 50, 60))
    for i in range(5):
        px = cx - 16 + i * 8
        d.line([px, cy - 24, px, cy - 18], fill=(45, 50, 60), width=2)
        d.line([px, cy + 18, px, cy + 24], fill=(45, 50, 60), width=2)
    d.rectangle([cx - 10, cy - 8, cx + 10, cy + 8], fill=(90, 200, 140))
    d.rectangle([x + 10, y + 10, x + 30, y + 26], fill=(40, 90, 160))
    d.text((x + 14, y + 12), "AU", font=font(F_SANS_B, 9), fill=(255, 255, 255))
    d.rectangle([x + w - 30, y + 10, x + w - 10, y + 26], fill=(200, 30, 30))
    d.ellipse([x + w - 25, y + 14, x + w - 15, y + 22], fill=(255, 220, 60))


def illu_bitcoin(d, x, y, w, h):
    cx, cy, r = x + w // 2 - 8, y + h // 2, 24
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(230, 175, 60),
              outline=(170, 120, 30), width=2)
    d.text((cx - 8, cy - 15), "B", font=font(F_SERIF_B, 26), fill=(140, 95, 20))
    d.line([cx - 4, cy - 18, cx - 4, cy + 18], fill=(140, 95, 20), width=2)
    d.line([cx + 3, cy - 18, cx + 3, cy + 18], fill=(140, 95, 20), width=2)
    pts = [(x + w - 34, y + 12), (x + w - 26, y + 22), (x + w - 18, y + 16),
           (x + w - 10, y + 30)]
    d.line(pts, fill=RED, width=3, joint="curve")
    d.polygon([(x + w - 14, y + 26), (x + w - 6, y + 26), (x + w - 10, y + 34)], fill=RED)


def illu_f1(d, x, y, w, h):
    for i in range(4):
        for j in range(3):
            if (i + j) % 2 == 0:
                d.rectangle([x + 12 + i * 9, y + 8 + j * 9, x + 21 + i * 9, y + 17 + j * 9],
                            fill=INK)
            else:
                d.rectangle([x + 12 + i * 9, y + 8 + j * 9, x + 21 + i * 9, y + 17 + j * 9],
                            fill=(255, 255, 255), outline=LINE)
    cx, cy = x + w // 2 + 6, y + h // 2 + 8
    d.polygon([(cx - 34, cy + 4), (cx - 18, cy - 8), (cx + 14, cy - 8), (cx + 34, cy + 2),
               (cx + 30, cy + 8), (cx - 30, cy + 8)], fill=(200, 30, 30))
    d.ellipse([cx - 22, cy + 2, cx - 10, cy + 14], fill=INK)
    d.ellipse([cx + 14, cy + 2, cx + 26, cy + 14], fill=INK)
    d.text((x + w - 58, y + h - 18), "1:34.041", font=font(F_SANS_B, 9), fill=INK)


ILLU = {"riyadh": illu_riyadh, "cop31": illu_cop31, "peru": illu_peru,
        "kryvyi": illu_kryvyi, "bridge": illu_bridge, "drone": illu_drone,
        "atom": illu_atom, "servers": illu_servers, "flags": illu_flags,
        "plane": illu_plane, "chip": illu_chip, "bitcoin": illu_bitcoin,
        "f1": illu_f1}

# ---------------------------------------------------------------- panels
VERIFY_FILL = {"OFFICIAL": BLUE, "CONFIRMED": GREEN, "REPORTED": AMBER,
               "CLAIM": RED}


def chip(d, x, y, text, fill, fg=(255, 255, 255)):
    fnt = font(F_SANS_B, 8)
    tw = d.textlength(text, font=fnt)
    d.rounded_rectangle([x, y, x + tw + 10, y + 14], radius=3, fill=fill)
    d.text((x + 5, y + 2), text, font=fnt, fill=fg)
    return tw + 10


def draw_panel(d, x, y, w, h, num, title, deck, source, verify, key, bg, hero):
    d.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=PAPER,
                        outline=LINE, width=1)
    ih = 88 if hero else 58
    d.rounded_rectangle([x + 1, y + 1, x + w - 1, y + ih], radius=4, fill=bg)
    d.rectangle([x + 1, y + ih - 8, x + w - 1, y + ih], fill=bg)
    ILLU[key](d, x + 4, y + 4, w - 8, ih - 4)
    d.ellipse([x + 8, y + 8, x + 30, y + 30], fill=RED)
    nf = font(F_SANS_B, 12 if hero else 11)
    nt = str(num)
    d.text((x + 19 - d.textlength(nt, font=nf) / 2, y + 11 if hero else y + 10),
           nt, font=nf, fill=(255, 255, 255))
    tx = x + 8
    tw = w - 16
    tf = font(F_SERIF_B, 13 if hero else 10)
    tlines = wrap(d, title, tf, tw)
    assert len(tlines) <= 2, (num, tlines)
    ty = y + ih + 6
    block(d, tx, ty, tlines, tf, INK, 16 if hero else 13)
    df = font(F_SERIF, 10 if hero else 8)
    dlines = wrap(d, deck, df, tw)
    assert len(dlines) <= 3, (num, dlines)
    dy = ty + (16 if hero else 13) * len(tlines) + 2
    block(d, tx, dy, dlines, df, (60, 56, 50), 12 if hero else 10)
    cy = y + h - 19
    chip(d, tx, cy, source, (255, 255, 255), INK)
    d.rounded_rectangle([tx, cy, tx + d.textlength(source, font=font(F_SANS_B, 8)) + 10,
                         cy + 14], radius=3, outline=INK, width=1)
    vw = chip(d, tx + d.textlength(source, font=font(F_SANS_B, 8)) + 16, cy,
              verify, VERIFY_FILL[verify])
    assert tx + d.textlength(source, font=font(F_SANS_B, 8)) + 16 + vw <= x + w - 4


# ---------------------------------------------------------------- map
CONTINENTS = {
    "NA": [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60),
           (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
           (-105, 20), (-117, 33), (-125, 49), (-150, 60)],
    "SA": [(-80, 10), (-60, 8), (-50, 0), (-40, -5), (-35, -8), (-40, -20),
           (-48, -28), (-58, -35), (-65, -45), (-70, -55), (-73, -40),
           (-75, -20), (-80, -5)],
    "EU": [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59),
           (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (30, 70), (20, 70),
           (12, 65), (5, 60), (-5, 50)],
    "AF": [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
           (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (30, -30), (20, -35),
           (15, -27), (12, -18), (9, -2), (9, 4), (-8, 5)],
    "AS": [(30, 36), (35, 36), (43, 41), (48, 38), (54, 37), (60, 25), (66, 25),
           (72, 20), (77, 8), (80, 7), (85, 20), (89, 22), (92, 16), (95, 16),
           (100, 8), (103, 2), (105, 10), (108, 12), (109, 20), (114, 22),
           (120, 25), (122, 30), (127, 35), (130, 42), (135, 44), (140, 40),
           (142, 50), (150, 60), (160, 60), (170, 66), (178, 65), (170, 60),
           (160, 55), (142, 52), (135, 43), (127, 40), (122, 38), (115, 38),
           (110, 40), (105, 38), (100, 38), (95, 30), (90, 28), (85, 25),
           (80, 25), (75, 28), (70, 30), (65, 35), (60, 38), (55, 40),
           (50, 42), (45, 42), (40, 40), (35, 38)],
    "OC": [(114, -22), (114, -30), (120, -34), (129, -32), (137, -35), (142, -38),
           (147, -39), (150, -37), (153, -27), (146, -19), (142, -11), (136, -12),
           (132, -12), (126, -14), (122, -17)],
}
# (num, lon, lat, dx, dy) — dx/dy nudge pins out of the Riyadh/Kyiv clusters
PINS = [(1, 46.7, 24.7, -6, 18), (2, 30.7, 36.9, -4, 16), (3, -75.5, -11.2, 0, 0),
        (4, 33.4, 47.9, 26, -20), (5, 30.5, 50.5, -30, -22), (6, 56.5, 26.6, 24, 16),
        (7, 51.4, 35.7, 30, 2), (8, -77.0, 38.9, -14, 7), (9, 116.4, 39.9, 0, 0),
        (10, 125.6, 7.1, 0, 0), (11, 149.1, -35.3, 0, 0), (12, -74.0, 40.7, 14, -7),
        (13, -115.1, 36.2, 0, 0)]


def draw_map(d, mx, my, mw, mh):
    # latitude window -60..85 so continents are not squashed flat
    def proj(lon, lat):
        return (mx + (lon + 180) / 360 * mw, my + (85 - lat) / 145 * mh)
    for pts in CONTINENTS.values():
        d.polygon([proj(lon, lat) for lon, lat in pts], fill=(222, 210, 185),
                  outline=(150, 140, 120))
    nf = font(F_SANS_B, 8)
    for num, lon, lat, dx, dy in PINS:
        px, py = proj(lon, lat)
        qx, qy = px + dx, py + dy
        if dx or dy:
            d.line([px, py, qx, qy], fill=RED, width=1)
        d.ellipse([qx - 8, qy - 8, qx + 8, qy + 8], fill=RED, outline=(255, 255, 255))
        t = str(num)
        d.text((qx - d.textlength(t, font=nf) / 2, qy - 6), t, font=nf,
               fill=(255, 255, 255))


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    # top line + masthead
    center(d, 6, "ONE DAY  \u2022  ONE PAGE  \u2022  ALL THE WORLD\u2019S NEWS",
           font(F_SANS, 8), GRAY)
    center(d, 18, "THE WORLD IN ONE DAY", font(F_SERIF_B, 36), RED)
    d.line([10, 60, W - 10, 60], fill=RED, width=2)
    d.line([10, 63, W - 10, 63], fill=RED, width=1)
    # date + subheadline
    center(d, 68, "Saturday 21 November 2026", font(F_SERIF_B, 32), INK)
    center(d, 106,
           "Three missiles down over Riyadh  \u2022  COP31 into overtime  \u2022  Peru shaken by a 6.7 quake",
           font(F_SERIF_I, 13), (60, 56, 50))
    # stat strip
    stats = [("35", "STORIES IN ALL"), ("13", "PICTURED ABOVE"),
             ("3", "MISSILES DOWN OVER RIYADH"), ("6.7", "PERU QUAKE (MAGNITUDE)"),
             ("146", "SAFE AFTER DAVAO LANDING"), ("$58,983", "BITCOIN, DOWN 3.9%")]
    sw, gap = 162, 6
    for i, (val, lab) in enumerate(stats):
        x = 10 + i * (sw + gap)
        d.rounded_rectangle([x, 126, x + sw, 172], radius=4, fill=PAPER,
                            outline=LINE, width=1)
        center(d, 130, val, font(F_SERIF_B, 19), RED, x, x + sw)
        center(d, 154, lab, font(F_SANS_B, 8), INK, x, x + sw)
    # region bar
    center(d, 178, "STORIES BY REGION \u2014 35 IN ALL", font(F_SANS_B, 10), INK)
    bx, bw, bh = 10, W - 20, 16
    x = bx
    for name, cnt, col in REGIONS:
        seg = bw * cnt / 35
        d.rectangle([x, 192, x + seg, 192 + bh], fill=col)
        x += seg
    d.rectangle([bx, 192, bx + bw, 192 + bh], outline=INK, width=1)
    leg = "  \u00b7  ".join(f"{n} {c}" for n, c, _ in REGIONS) + "  \u2014  total 35"
    center(d, 212, leg, font(F_SANS, 10), INK)
    # hero row
    for i, p in enumerate(PANELS[:3]):
        draw_panel(d, 10 + i * 334, 228, 326, 184, *p, hero=True)
    # small rows
    for row in range(2):
        for j in range(5):
            p = PANELS[3 + row * 5 + j]
            draw_panel(d, 10 + j * 202, 418 + row * 162, 196, 156, *p, hero=False)
    # verdict strip
    d.rounded_rectangle([10, 742, W - 10, 774], radius=4, fill=(253, 243, 227),
                        outline=RED, width=2)
    vt = "THE VERDICT \u2014 A day of near-misses: three missiles stopped over Riyadh and all 146 saved in Davao \u2014 but no climate deal in Antalya and no let-up in Ukraine."
    d.text((20, 750), vt, font=font(F_SERIF_B, 11), fill=INK)
    assert d.textlength(vt, font=font(F_SERIF_B, 11)) <= W - 40
    # bottom: map + ALSO
    d.text((10, 780), "WHERE IT HAPPENED \u2014 13 PLACES", font=font(F_SANS_B, 10), fill=INK)
    draw_map(d, 10, 796, 480, 108)
    ax = 498
    d.text((ax, 780), "ALSO ON SATURDAY 21 NOVEMBER \u2014 22 MORE STORIES",
           font=font(F_SANS_B, 10), fill=INK)
    af = font(F_SANS, 9)
    for k, (num, text, _reg) in enumerate(ALSO):
        col = 0 if k < 11 else 1
        row = k % 11
        cx = ax + col * 258
        cy = 796 + row * 10
        item = f"{num}  {text}"
        assert d.textlength(item, font=af) <= 254, item
        d.text((cx, cy), item, font=af, fill=INK)
    # date check
    d.rounded_rectangle([10, 910, W - 10, 976], radius=4, fill=PAPER,
                        outline=RED, width=2)
    d.text((20, 916), "DATE CHECK \u2014 WHAT WE LEFT OUT, AND WHY",
           font=font(F_SANS_B, 11), fill=RED)
    bf = font(F_SERIF, 10)
    dc1 = ("Left out on purpose \u2014 all Friday 20 November, not today: the UK\u2013EU reset deal "
           "(100,000 visas); the Wall Street slide into correction; the strike on Kyiv\u2019s bridge; "
           "missiles landing in Poland; Cyclone Akvan\u2019s landfall.")
    dc2 = ("Not yet known when this page was drawn: whether BepiColombo has entered Mercury orbit; "
           "the final text of the COP31 deal.")
    for i, ln in enumerate(wrap(d, dc1, bf, W - 40)):
        d.text((20, 934 + i * 13), ln, font=bf, fill=INK)
    n1 = len(wrap(d, dc1, bf, W - 40))
    for i, ln in enumerate(wrap(d, dc2, bf, W - 40)):
        d.text((20, 934 + (n1 + i) * 13), ln, font=bf, fill=INK)
    assert 934 + (n1 + len(wrap(d, dc2, bf, W - 40))) * 13 <= 976
    # footer
    center(d, 982,
           "Every story here happened, or was first reported, on Saturday 21 November 2026.",
           font(F_SERIF_I, 10), INK)
    center(d, 998,
           "HOW WE CHECKED \u2014 OFFICIAL: named authority  \u00b7  CONFIRMED: two independent sources  \u00b7  REPORTED: a single wire report  \u00b7  CLAIM: one side only, unconfirmed",
           font(F_SANS, 8), GRAY)
    return img


if __name__ == "__main__":
    img = build()
    png_path = os.path.join(HERE, "entry.png")
    img.save(png_path, format="PNG", optimize=True)
    size = os.path.getsize(png_path)
    print("PNG bytes:", size)
    if size > 260000:
        img.save(png_path, format="JPEG", quality=88, optimize=True)
        print("JPEG bytes:", os.path.getsize(png_path))
    print("saved", png_path)
