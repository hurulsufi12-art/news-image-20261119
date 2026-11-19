#!/usr/bin/env python3
"""Draw entry.png for news-image-20261119: a newspaper front page summing up
Thursday 19 November 2026. Deterministic: fixed fonts, fixed geometry, no
randomness, no timestamps, no network. Run: python3 draw.py -> entry.png
(1024x1024, well under 1 MiB). Everything is drawn with code (Pillow
primitives); no photos, no AI-generated images."""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 36                      # side margin
CW = W - 2 * M              # content width = 952

PAPER = (251, 249, 242)     # warm newsprint white
INK = (20, 36, 62)          # navy
RED = (176, 30, 36)         # masthead red
GREY = (90, 100, 112)
LIGHT_GREY = (214, 214, 206)
SKY_TOP = (38, 32, 86)      # Vice City dusk sky, top
SKY_MID = (120, 52, 110)    # dusk sky, middle
SKY_LOW = (238, 120, 90)    # sunset band
NEON = (255, 64, 150)       # neon pink
NEON_CYAN = (64, 224, 224)  # neon cyan
SUN = (255, 190, 90)
BUILD = (24, 20, 52)        # skyline silhouette
BUILD2 = (44, 34, 74)
SEA = (40, 52, 110)
GOLD = (212, 160, 38)
ORANGE = (224, 122, 31)

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    """Greedy word wrap to lines no wider than max_w."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_one_line(draw, s, f_path, size, max_w):
    """Shrink font until the string fits on one line; return (font, size)."""
    while size > 12:
        f = font(f_path, size)
        if text_w(draw, s, f) <= max_w:
            return f, size
        size -= 1
    return font(f_path, 12), 12


def para(draw, x, y, s, f, color, max_w, leading):
    """Draw wrapped paragraph, return y after last line."""
    for line in wrap(draw, s, f, max_w):
        draw.text((x, y), line, font=f, fill=color)
        y += leading
    return y


# ---------------------------------------------------------------- icons
def icon_ballot(d, x, y, s, color):
    """Ballot box with a check mark."""
    d.rectangle([x + s * 0.14, y + s * 0.34, x + s * 0.86, y + s * 0.92],
                outline=color, width=max(3, s // 16))
    d.rectangle([x + s * 0.08, y + s * 0.24, x + s * 0.92, y + s * 0.34],
                fill=color)
    d.rectangle([x + s * 0.36, y + s * 0.27, x + s * 0.64, y + s * 0.31],
                fill=PAPER)
    d.line([x + s * 0.28, y + s * 0.62, x + s * 0.44, y + s * 0.78,
            x + s * 0.74, y + s * 0.44], fill=RED,
           width=max(4, s // 12), joint="curve")


def icon_jet(d, x, y, s, color):
    """Fighter jet, top view, climbing."""
    d.polygon([(x + s * 0.50, y + s * 0.04), (x + s * 0.60, y + s * 0.62),
               (x + s * 0.50, y + s * 0.78), (x + s * 0.40, y + s * 0.62)], fill=color)
    d.polygon([(x + s * 0.42, y + s * 0.48), (x + s * 0.06, y + s * 0.86),
               (x + s * 0.24, y + s * 0.86), (x + s * 0.46, y + s * 0.62)], fill=color)
    d.polygon([(x + s * 0.58, y + s * 0.48), (x + s * 0.94, y + s * 0.86),
               (x + s * 0.76, y + s * 0.86), (x + s * 0.54, y + s * 0.62)], fill=color)
    d.polygon([(x + s * 0.42, y + s * 0.66), (x + s * 0.30, y + s * 0.94),
               (x + s * 0.44, y + s * 0.94)], fill=color)
    d.polygon([(x + s * 0.58, y + s * 0.66), (x + s * 0.70, y + s * 0.94),
               (x + s * 0.56, y + s * 0.94)], fill=color)
    d.ellipse([x + s * 0.46, y + s * 0.18, x + s * 0.54, y + s * 0.34], fill=PAPER)


def icon_summit(d, x, y, s, color):
    """Three leaders at a table: three heads above a table line."""
    for cx in (0.24, 0.50, 0.76):
        hx = x + s * cx
        d.ellipse([hx - s * 0.09, y + s * 0.10, hx + s * 0.09, y + s * 0.28],
                  fill=color)
        d.pieslice([hx - s * 0.14, y + s * 0.28, hx + s * 0.14, y + s * 0.62],
                   start=180, end=360, fill=color)
    d.rectangle([x + s * 0.06, y + s * 0.62, x + s * 0.94, y + s * 0.70],
                fill=color)
    d.rectangle([x + s * 0.14, y + s * 0.70, x + s * 0.20, y + s * 0.92],
                fill=color)
    d.rectangle([x + s * 0.80, y + s * 0.70, x + s * 0.86, y + s * 0.92],
                fill=color)
    # three small flags on the table
    for i, fc in enumerate((RED, GOLD, NEON_CYAN)):
        fx = x + s * (0.30 + 0.20 * i)
        d.line([fx, y + s * 0.62, fx, y + s * 0.44], fill=fc, width=3)
        d.polygon([(fx, y + s * 0.44), (fx + s * 0.10, y + s * 0.48),
                   (fx, y + s * 0.52)], fill=fc)


def icon_cyclone(d, x, y, s, color):
    """Spiral storm: concentric arcs winding inward."""
    cx, cy = x + s * 0.50, y + s * 0.52
    for k in range(4):
        r = s * (0.42 - 0.09 * k)
        d.arc([cx - r, cy - r, cx + r, cy + r], start=20 + k * 55,
              end=300 + k * 55, fill=color, width=max(3, s // 18))
    d.ellipse([cx - s * 0.07, cy - s * 0.07, cx + s * 0.07, cy + s * 0.07],
              fill=RED)
    # rain streaks below
    for i in range(3):
        rx = x + s * (0.20 + 0.28 * i)
        d.line([rx, y + s * 0.86, rx - s * 0.06, y + s * 0.98], fill=color,
               width=max(3, s // 20))


def icon_bank(d, x, y, s, color):
    """Bank building: pediment roof, columns, steps."""
    d.polygon([(x + s * 0.06, y + s * 0.34), (x + s * 0.50, y + s * 0.08),
               (x + s * 0.94, y + s * 0.34)], fill=color)
    for i in range(4):
        cx = x + s * (0.18 + 0.21 * i)
        d.rectangle([cx - s * 0.045, y + s * 0.40, cx + s * 0.045,
                     y + s * 0.78], fill=color)
    d.rectangle([x + s * 0.08, y + s * 0.78, x + s * 0.92, y + s * 0.86],
                fill=color)
    d.rectangle([x + s * 0.04, y + s * 0.86, x + s * 0.96, y + s * 0.94],
                fill=color)
    d.ellipse([x + s * 0.40, y + s * 0.14, x + s * 0.60, y + s * 0.32],
              fill=PAPER)


def draw_vice_city(d, x, y, w, h):
    """Stylised Vice City at dusk: gradient sky, big sun, skyline with lit
    windows, two palm trees, neon strip, water with reflections."""
    # sky: horizontal gradient bands, top dusk navy to sunset orange
    bands = 48
    for i in range(bands):
        t = i / (bands - 1)
        if t < 0.55:
            u = t / 0.55
            c = tuple(int(SKY_TOP[k] + (SKY_MID[k] - SKY_TOP[k]) * u)
                      for k in range(3))
        else:
            u = (t - 0.55) / 0.45
            c = tuple(int(SKY_MID[k] + (SKY_LOW[k] - SKY_MID[k]) * u)
                      for k in range(3))
        yy = y + int(h * 0.62 * i / bands)
        d.rectangle([x, yy, x + w, y + int(h * 0.62 * (i + 1) / bands) + 1],
                    fill=c)
    horizon = y + int(h * 0.62)
    # sun, low over the skyline
    sun_cx, sun_cy, sun_r = x + int(w * 0.68), horizon - 52, 34
    d.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
              fill=SUN)
    # skyline: fixed building silhouettes with lit windows
    buildings = [
        (0.00, 0.30, 0.13, BUILD), (0.13, 0.22, 0.11, BUILD2),
        (0.24, 0.36, 0.12, BUILD), (0.36, 0.26, 0.10, BUILD2),
        (0.46, 0.42, 0.13, BUILD), (0.59, 0.24, 0.11, BUILD2),
        (0.70, 0.34, 0.12, BUILD), (0.82, 0.28, 0.18, BUILD2),
    ]
    for bx, bh, bw, col in buildings:
        bx0 = x + int(w * bx)
        bw_px = int(w * bw)
        bh_px = int(h * bh)
        d.rectangle([bx0, horizon - bh_px, bx0 + bw_px, horizon], fill=col)
        # lit windows, fixed grid
        for wy in range(2, bh_px - 6, 14):
            for wx in range(5, bw_px - 5, 12):
                if (wx // 12 + wy // 14) % 3 == 0:
                    d.rectangle([bx0 + wx, horizon - bh_px + wy,
                                 bx0 + wx + 4, horizon - bh_px + wy + 5],
                                fill=GOLD)
    # palm trees, silhouetted against the sunset: leaning trunk plus
    # drooping fronds drawn as short curved polylines
    for px, ph in ((0.10, 58), (0.88, 66)):
        tx0 = x + int(w * px)
        ty0 = horizon
        d.line([tx0, ty0, tx0 + 6, ty0 - ph], fill=BUILD, width=5)
        top_x, top_y = tx0 + 6, ty0 - ph
        for ang in (-160, -125, -90, -55, -20):
            rad = math.radians(ang)
            ex = top_x + int(28 * math.cos(rad))
            ey = top_y + int(14 * math.sin(rad)) + 8
            mx = top_x + int(15 * math.cos(rad))
            my = top_y + int(7 * math.sin(rad)) - 6
            d.line([(top_x, top_y), (mx, my), (ex, ey)], fill=BUILD,
                   width=4, joint="curve")
    # neon strip along the waterfront
    d.rectangle([x, horizon - 4, x + w, horizon + 2], fill=NEON)
    # water with sun reflection
    d.rectangle([x, horizon + 2, x + w, y + h], fill=SEA)
    for i, rw in enumerate((120, 84, 56, 34)):
        ry = horizon + 14 + i * 14
        d.rectangle([sun_cx - rw // 2, ry, sun_cx + rw // 2, ry + 4],
                    fill=SUN)
    d.text((x + 10, y + h - 26), "VICE CITY", font=font(FONT_B, 15),
           fill=(255, 255, 255))


# ---------------------------------------------------------------- layout
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    y = 30
    # --- masthead ---
    f_mast = font(FONT_B, 62)
    mast = "THE WORLD IN ONE DAY"
    d.text(((W - text_w(d, mast, f_mast)) / 2, y), mast, font=f_mast, fill=INK)
    y += 78
    d.rectangle([M, y, W - M, y + 4], fill=RED)
    y += 14
    f_date = font(FONT_B, 36)
    date = "THURSDAY, 19 NOVEMBER 2026"
    d.text(((W - text_w(d, date, f_date)) / 2, y), date, font=f_date, fill=RED)
    y += 52
    d.rectangle([M, y, W - M, y + 2], fill=INK)
    y += 12

    # --- lead story: GTA VI launches today ---
    f_kick = font(FONT_B, 18)
    d.text((M, y), "LEAD  •  GAMING", font=f_kick, fill=RED)
    y += 26
    ill_w, ill_h = 360, 240
    ill_x, ill_y = W - M - ill_w, y
    draw_vice_city(d, ill_x, ill_y, ill_w, ill_h)
    tx = M
    tw = ill_x - 18 - M
    f_head = font(FONT_B, 42)
    head_lines = wrap(d, "GTA VI LAUNCHES TODAY", f_head, tw)
    for line in head_lines:
        d.text((tx, y), line, font=f_head, fill=INK)
        y += 50
    y += 6
    f_body = font(FONT_R, 22)
    lead_sum = ("Grand Theft Auto VI begins its global rollout today. "
                "Gamers enter Vice City after a 13-year wait since "
                "GTA V.")
    y = para(d, tx, y, lead_sum, f_body, INK, tw, 29)
    lead_bottom = max(y, ill_y + ill_h) + 12
    d.rectangle([M, lead_bottom, W - M, lead_bottom + 2], fill=INK)
    y = lead_bottom + 14

    # --- grid of 4 stories, 2 columns ---
    stories = [
        ("ASIA", "TRUMP-XI-PUTIN SUMMIT TODAY",
         "The three leaders meet in Shenzhen during APEC, their first "
         "trilateral summit.",
         icon_summit),
        ("AMERICAS", "JEFFRIES FOR SPEAKER",
         "Democrats nominate Hakeem Jeffries. He would be the first "
         "African-American Speaker.",
         icon_ballot),
        ("MIDDLE EAST", "US-IRAN FIRE CONTINUES",
         "Iran widens attacks to Kuwait and Bahrain after the US struck "
         "a missile site on Qeshm Island.",
         icon_jet),
        ("ASIA", "CYCLONE AKVAN NEARS INDIA",
         "Cyclone Akvan nears India's east coast. Landfall is expected "
         "between Machilipatnam and Puri.",
         icon_cyclone),
    ]
    col_w = (CW - 20) // 2
    row_h = 132
    for i, (kick, head, summ, icon) in enumerate(stories):
        col = i % 2
        row = i // 2
        cx = M + col * (col_w + 20)
        cy = y + row * (row_h + 12)
        d.text((cx + 74, cy), kick, font=font(FONT_B, 16), fill=RED)
        f_h, _ = fit_one_line(d, head, FONT_B, 24, col_w - 74)
        d.text((cx + 74, cy + 20), head, font=f_h, fill=INK)
        para(d, cx + 74, cy + 50, summ, font(FONT_R, 19), INK,
             col_w - 74, 24)
        icon(d, cx, cy + 6, 62, INK)
        if col == 0:
            d.line([cx + col_w + 10, cy + 4, cx + col_w + 10, cy + row_h - 8],
                   fill=LIGHT_GREY, width=2)
    y = y + 2 * (row_h + 12) + 2

    # --- fifth story, full width ---
    d.rectangle([M, y, W - M, y + 2], fill=LIGHT_GREY)
    y += 10
    d.text((M + 74, y), "EUROPE", font=font(FONT_B, 16), fill=RED)
    f_h, _ = fit_one_line(d, "EU PROPOSES €45 BILLION UKRAINE LOAN",
                          FONT_B, 24, CW - 74)
    d.text((M + 74, y + 20), "EU PROPOSES €45 BILLION UKRAINE LOAN",
           font=f_h, fill=INK)
    para(d, M + 74, y + 50,
         "The EU proposes a €45 billion loan to Ukraine, to be repaid "
         "after Russia pays reparations.",
         font(FONT_R, 19), INK, CW - 74, 24)
    icon_bank(d, M, y + 6, 62, INK)
    y += 100
    d.rectangle([M, y, W - M, y + 2], fill=INK)
    y += 12

    # --- ticker ---
    f_tick_b = font(FONT_B, 19)
    f_tick = font(FONT_R, 19)
    tick = ("NASA: Voyager 1 passes one-light-day mark today  •  "
            "Fed minutes: most officials expect further rate hikes  •  "
            "Moldova summons Russian envoy over drone incursions  •  "
            "Australia sanctions Israeli settlers  •  "
            "Pew: Islam on track to be world's largest religion by 2035")
    d.text((M, y), "ALSO:", font=f_tick_b, fill=RED)
    tx = M + text_w(d, "ALSO:  ", f_tick_b)
    y = para(d, tx, y, tick, f_tick, INK, W - M - tx, 25)
    y += 8
    d.rectangle([M, y, W - M, y + 4], fill=RED)

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
