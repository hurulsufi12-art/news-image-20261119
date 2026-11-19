#!/usr/bin/env python3
"""Draw the newspaper front page for Thursday, 19 November 2026.

Build-time provenance only: this script is NOT run by the grader.
It produces entry.png (1024x1024, deterministic) next to itself.
Run:  python3 draw.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- palette
W = H = 1024
MARGIN = 36
PAPER = (251, 246, 236)      # warm newsprint cream
NAVY = (27, 42, 74)          # headlines, rules
RED = (178, 34, 34)          # kickers, date, rules
INK = (38, 42, 56)           # body text
FAINT = (118, 112, 102)      # hairlines
GOLD = (238, 172, 60)        # lit windows, sun
PINK = (228, 64, 140)        # neon horizon strip
SKY_TOP = (56, 26, 92)
SKY_MID = (120, 48, 118)
WATER = (38, 48, 104)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default(size)


F = {
    "mast": load("DejaVuSans-Bold.ttf", 62),
    "date": load("DejaVuSans-Bold.ttf", 34),
    "kick": load("DejaVuSans-Bold.ttf", 19),
    "head": load("DejaVuSans-Bold.ttf", 56),
    "grid_head": load("DejaVuSans-Bold.ttf", 25),
    "body": load("DejaVuSans.ttf", 20),
    "lead_body": load("DejaVuSans.ttf", 23),
    "tick": load("DejaVuSans.ttf", 20),
    "tick_b": load("DejaVuSans-Bold.ttf", 20),
    "label": load("DejaVuSans-Bold.ttf", 20),
}


def wrap(d, text, font, max_w):
    """Greedy word wrap by measured pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, max_w, leading, color=INK):
    """Draw wrapped paragraph, return y just below the last line."""
    for line in wrap(d, text, font, max_w):
        d.text((x, y), line, font=font, fill=color)
        y += leading
    return y


def rule(d, y, color, weight):
    d.rectangle([MARGIN, y, W - MARGIN, y + weight - 1], fill=color)
    return y + weight


# ---------------------------------------------------------------- skyline
def draw_skyline(d, x, y, w, h):
    """Vice City at dusk: gradient sky, low sun, tower blocks with lit
    windows, a neon strip, and gold reflections on dark water."""
    horizon = y + int(h * 0.62)
    # sky gradient, one horizontal band per pixel row
    for row in range(horizon - y):
        t = row / max(1, horizon - y - 1)
        r = int(SKY_TOP[0] + (SKY_MID[0] - SKY_TOP[0]) * t)
        g = int(SKY_TOP[1] + (SKY_MID[1] - SKY_TOP[1]) * t)
        b = int(SKY_TOP[2] + (SKY_MID[2] - SKY_TOP[2]) * t)
        d.line([(x, y + row), (x + w, y + row)], fill=(r, g, b))
    # low sun, left to peek through a gap in the tower line
    sun_cx, sun_cy, sun_r = x + 172, horizon - 36, 32
    d.ellipse([sun_cx - sun_r, sun_cy - sun_r,
               sun_cx + sun_r, sun_cy + sun_r], fill=GOLD)
    # tower blocks, each (left offset, width, height above horizon);
    # a gap around x+150..x+195 leaves the sun visible
    towers = [(0, 52, 96), (56, 44, 128), (104, 40, 88), (196, 44, 138),
              (244, 52, 100), (300, 44, 126), (348, 28, 88)]
    for off, tw, th in towers:
        bx = x + off
        d.rectangle([bx, horizon - th, bx + tw, horizon], fill=(24, 22, 44))
        # lit windows on a fixed checker so the render is deterministic
        cols = max(1, (tw - 16) // 15)
        for col in range(cols):
            for row in range(th // 26):
                if (col + row * 2 + off // 8) % 3:
                    wx = bx + 8 + col * 15
                    wy = horizon - th + 10 + row * 26
                    d.rectangle([wx, wy, wx + 7, wy + 9], fill=GOLD)
    # palm silhouette on the right edge
    px, py = x + w - 26, horizon - 84
    d.line([(px, py + 84), (px, py)], fill=(24, 22, 44), width=5)
    for dx, dy in [(-26, -14), (-14, -24), (0, -28), (16, -22), (28, -10)]:
        d.line([(px, py), (px + dx, py + dy)], fill=(24, 22, 44), width=4)
    # neon strip on the horizon, then water with gold reflections
    d.rectangle([x, horizon, x + w, horizon + 5], fill=PINK)
    d.rectangle([x, horizon + 6, x + w, y + h], fill=WATER)
    # label sits just under the neon strip; reflections start below it
    d.text((x + 14, horizon + 8), "VICE CITY", font=F["label"],
           fill=(255, 255, 255))
    for i, ln in enumerate((150, 110, 170, 90, 130)):
        ry = horizon + 34 + i * 10
        rx = x + 30 + (i % 2) * 60
        d.line([(rx, ry), (rx + ln, ry)], fill=GOLD, width=4)


# ---------------------------------------------------------------- icons
def icon_summit(d, x, y, s):
    """Three leaders seated at a table."""
    for i, c in enumerate((NAVY, RED, GOLD)):
        cx = x + 12 + i * (s // 3)
        d.ellipse([cx - 8, y + 4, cx + 8, y + 20], fill=c)
        d.rectangle([cx - 9, y + 24, cx + 9, y + 38], fill=c)
    d.rectangle([x, y + 40, x + s, y + 46], fill=NAVY)
    d.line([(x + 4, y + 46), (x + 4, y + s)], fill=NAVY, width=4)
    d.line([(x + s - 4, y + 46), (x + s - 4, y + s)], fill=NAVY, width=4)


def icon_ballot(d, x, y, s):
    """Ballot box with a red check."""
    d.rectangle([x + 4, y + 18, x + s - 4, y + s - 2], outline=NAVY, width=4)
    d.rectangle([x, y + 12, x + s, y + 20], fill=NAVY)
    d.line([(x + 12, y + 38), (x + 24, y + 50), (x + s - 10, y + 22)],
           fill=RED, width=6)


def icon_missile(d, x, y, s):
    """Missile rising with a flame trail."""
    d.polygon([(x + s // 2, y + 2), (x + s - 12, y + 34),
               (x + 12, y + 34)], fill=NAVY)
    d.rectangle([x + s // 2 - 6, y + 34, x + s // 2 + 6, y + 48], fill=NAVY)
    d.polygon([(x + s // 2, y + s - 2), (x + s // 2 - 8, y + 48),
               (x + s // 2 + 8, y + 48)], fill=RED)


def icon_cyclone(d, x, y, s):
    """Spiral storm: concentric arcs around a red eye."""
    cx, cy = x + s // 2, y + s // 2
    for r in (26, 19, 12):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
              fill=NAVY, width=4)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)


def icon_bank(d, x, y, s):
    """Classical bank front: pediment, columns, steps."""
    d.polygon([(x + 2, y + 20), (x + s // 2, y + 2), (x + s - 2, y + 20)],
              fill=NAVY)
    d.ellipse([x + s // 2 - 6, y + 10, x + s // 2 + 6, y + 22], fill=PAPER)
    for i in range(4):
        cx = x + 10 + i * (s - 20) // 3
        d.rectangle([cx - 4, y + 26, cx + 4, y + 50], fill=NAVY)
    d.rectangle([x, y + 52, x + s, y + 56], fill=NAVY)
    d.rectangle([x + 4, y + 58, x + s - 4, y + 62], fill=NAVY)


ICONS = {
    "summit": icon_summit,
    "ballot": icon_ballot,
    "missile": icon_missile,
    "cyclone": icon_cyclone,
    "bank": icon_bank,
}


def story_cell(d, x, y, w, icon, kicker, headline, body):
    """One grid story: icon at left, kicker + headline + body at right."""
    ICONS[icon](d, x, y + 4, 56)
    tx = x + 70
    d.text((tx, y), kicker, font=F["kick"], fill=RED)
    hy = y + 26
    for line in wrap(d, headline, F["grid_head"], w - 70):
        d.text((tx, hy), line, font=F["grid_head"], fill=NAVY)
        hy += 30
    return para(d, tx, hy + 4, body, F["body"], w - 70, 24)


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    right = W - MARGIN

    # masthead
    title = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(title, font=F["mast"])) / 2, 24),
           title, font=F["mast"], fill=NAVY)
    rule(d, 104, RED, 4)
    date = "THURSDAY, 19 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=F["date"])) / 2, 116),
           date, font=F["date"], fill=RED)
    rule(d, 164, NAVY, 3)

    # ---- lead story -----------------------------------------------------
    lead_x, lead_y = MARGIN, 182
    lead_w = 540
    d.text((lead_x, lead_y), "LEAD  \u2022  GAMING", font=F["kick"], fill=RED)
    hy = lead_y + 28
    for line in ("GTA VI LAUNCHES", "TODAY"):
        d.text((lead_x, hy), line, font=F["head"], fill=NAVY)
        hy += 62
    para(d, lead_x, hy + 6,
         "Grand Theft Auto VI begins its global rollout today. "
         "Gamers enter Vice City after a 13-year wait since GTA V.",
         F["lead_body"], lead_w, 29)

    panel_x, panel_w = 612, 376
    draw_skyline(d, panel_x, 186, panel_w, 218)

    rule(d, 424, NAVY, 3)

    # ---- 2 x 2 grid -----------------------------------------------------
    col_w = (right - MARGIN - 24) // 2
    col2_x = MARGIN + col_w + 24
    grid = [
        (MARGIN, "summit", "ASIA", "TRUMP\u2013XI\u2013PUTIN SUMMIT TODAY",
         "First trilateral summit of the three leaders, in Shenzhen "
         "during APEC."),
        (col2_x, "ballot", "AMERICAS", "JEFFRIES FOR SPEAKER",
         "Democrats nominate Hakeem Jeffries \u2014 the first "
         "African-American Speaker."),
        (MARGIN, "missile", "MIDDLE EAST", "US\u2013IRAN FIRE CONTINUES",
         "Iran widens attacks to Kuwait and Bahrain after a US strike "
         "on Qeshm Island."),
        (col2_x, "cyclone", "ASIA", "CYCLONE AKVAN NEARS INDIA",
         "Landfall is expected between Machilipatnam and Puri on "
         "India's east coast."),
    ]
    # Rows are placed from measured heights so wrapped text can never
    # spill into the row below (the first draft overlapped here).
    row1_y = 442
    row1_bottom = max(
        story_cell(d, gx, row1_y, col_w, icon, kick, head, body)
        for gx, icon, kick, head, body in grid[:2])
    row2_y = row1_bottom + 16
    row2_bottom = max(
        story_cell(d, gx, row2_y, col_w, icon, kick, head, body)
        for gx, icon, kick, head, body in grid[2:])
    # vertical divider between the two columns, per row
    for y0, y1 in ((row1_y, row1_bottom), (row2_y, row2_bottom)):
        d.line([(512, y0 + 4), (512, y1 - 4)], fill=FAINT, width=2)

    rule(d, row2_bottom + 14, FAINT, 2)

    # ---- EU loan, full width --------------------------------------------
    eu_y = row2_bottom + 32
    icon_bank(d, MARGIN, eu_y, 56)
    tx = MARGIN + 70
    d.text((tx, eu_y - 2), "EUROPE", font=F["kick"], fill=RED)
    d.text((tx, eu_y + 24), "EU PROPOSES \u20ac45 BILLION UKRAINE LOAN",
           font=F["grid_head"], fill=NAVY)
    eu_bottom = para(d, tx, eu_y + 58,
                     "The EU proposes a \u20ac45 billion loan to Ukraine, to "
                     "be repaid after Russia pays reparations.",
                     F["body"], right - tx, 26)

    rule(d, eu_bottom + 14, NAVY, 3)

    # ---- ticker ----------------------------------------------------------
    ty = eu_bottom + 30
    d.text((MARGIN, ty), "ALSO:", font=F["tick_b"], fill=RED)
    tick = ("NASA: Voyager 1 passes one-light-day mark today  \u2022  "
            "Fed minutes: most officials expect further rate hikes  \u2022  "
            "Moldova summons Russian envoy over drone incursions  \u2022  "
            "Australia sanctions Israeli settlers  \u2022  "
            "Pew: Islam on track to be world's largest religion by 2035")
    tick_bottom = para(d, MARGIN + 70, ty, tick, F["tick"],
                       right - MARGIN - 70, 25)
    rule(d, tick_bottom + 12, RED, 4)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG")
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
