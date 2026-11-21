#!/usr/bin/env python3
"""Render the one-image summary of world news for Friday 20 November 2026.

Layout: a dark masthead carrying the date, a small hand-drawn world map
with a red dot per story, then a 5 x 6 grid of story cards (30 stories).
Each card has a numbered place tag, a one-to-two-line headline and a short
caption of at most three lines.

Every story below was verified by web research on Saturday 21 November
2026 as an event that happened or was first reported on Friday 20
November 2026. The research notes list the source for each one plus the
stories that were checked and rejected for being 19 November or earlier.

Run:  python3 draw_poster.py   (writes entry.png next to this script)
"""

from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 1024, 1024
OUTPUT = "entry.png"

BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

DARK = (15, 23, 42)
PAPER = (251, 249, 244)
ACCENT = (185, 28, 28)
GOLD = (202, 158, 45)
CARD = (255, 255, 255)
CARD_EDGE = (203, 213, 225)
GREY = (71, 85, 105)
LAND = (148, 163, 184)
SEA = (226, 232, 240)
LIGHT_GREY = (203, 213, 225)

# Tag colour per region.
TAG = {
    "ASIA": (30, 90, 160),
    "EUROPE": (107, 33, 168),
    "MIDEAST": (180, 83, 9),
    "AFRICA": (146, 64, 14),
    "AMERICAS": (21, 128, 61),
    "GLOBAL": (100, 116, 139),
    "SPORT": (190, 24, 93),
}

# (place, region, headline, caption). Headlines fit ~44 chars, captions ~64.
ITEMS = [
    ("ODISHA", "ASIA", "Cyclone Akvan hits Odisha coast",
     "Landfall near Gopalpur; 300,000 evacuated, no deaths yet."),
    ("KYIV", "EUROPE", "Russia strikes Kyiv bridges",
     "8 killed, 28 hurt across 9 regions; Lviv station hit."),
    ("POLAND", "EUROPE", "Russia violates Polish airspace",
     "2 missiles and a drone cross over as allied drills begin."),
    ("ESTONIA", "EUROPE", "Estonia shuts Russia border",
     "Border closed for at least six months."),
    ("IRAQ", "MIDEAST", "Iraqi forces move on Kataib Hezbollah",
     "Federal troops deploy in Jurf al-Sakhar over oil smuggling."),
    ("LONDON", "EUROPE", "RAF Fairford suspects face trial",
     "Two men to stand trial in Nov 2027; prosecutors allege Iran link."),
    ("BRUSSELS", "EUROPE", "UK-EU summit: youth mobility deal",
     "Scheme for up to 100,000 a year each way set to be agreed."),
    ("BERLIN", "EUROPE", "Merz rejects a new Yalta deal",
     "No settlement on Europe's future without Europeans."),
    ("RIYADH", "MIDEAST", "Saudis intercept Houthi missile",
     "Another missile and 5 drones downed on Friday."),
    ("HORMUZ", "MIDEAST", "Tanker catches fire after mine hit",
     "Iran steps up tanker attacks as war enters its 9th month."),
    ("GAZA", "MIDEAST", "Israeli troops cross Yellow Line",
     "First incursion since the truce; tunnel dismantled."),
    ("ANTALYA", "GLOBAL", "COP31 draft drops fossil-fuel exit",
     "Talks enter their final day without a phase-out call."),
    ("NEW YORK", "GLOBAL", "Stocks fall for fifth straight day",
     "S&P -2%; Nikkei -4.8% as Asian markets drop on Friday."),
    ("LONDON", "GLOBAL", "Gold falls 4.2% as dollar climbs",
     "US 10-year yield climbs above 5%."),
    ("EDINBURGH", "GLOBAL", "GTA 6 tops $2.3bn at launch",
     "Biggest entertainment launch ever, industry estimates say."),
]

ITEMS += [
    ("EUROPE", "GLOBAL", "Youth strike in 25+ countries",
     "Young people protest living costs and militarization."),
    ("SAN SALVADOR", "AMERICAS", "Bukele registers for third term",
     "Formal bid for a third straight six-year term."),
    ("SENEGAL", "AFRICA", "Migrant boat capsizes off Yenne",
     "50-100 aboard; 4 bodies found, dozens missing."),
    ("SUDAN", "AFRICA", "Drone strike kills 10 at gold mine",
     "Attack in South Kordofan; Amnesty urges a probe."),
    ("HAITI", "AMERICAS", "Haiti raid kills 34 gang suspects",
     "Forces retake a corridor out of Port-au-Prince."),
    ("TOKYO", "ASIA", "Japan inflation hits year's high",
     "Core inflation rises as energy subsidies expire."),
    ("BRASILIA", "AMERICAS", "Brazil sells $1bn to defend real",
     "Central bank intervenes as the currency falls ~18% in a month."),
    ("BRAZIL", "AMERICAS", "Lula recognises Raoni's land",
     "Ancestral Kayapo and Yudja land recognised; Awa emerge briefly."),
    ("NEW YORK", "GLOBAL", "UN chief race stalls after 8 votes",
     "No successor to Guterres agreed by the Security Council."),
    ("DHAKA", "ASIA", "Violence flares ahead of Hasina return",
     "Protests and arson in Gopalganj; passport bid rejected."),
    ("ISRAEL", "MIDEAST", "Mosque torched in al-Dahi",
     "Hebrew revenge graffiti; driver rams Palestinians in Kafr Qasim."),
    ("ETHIOPIA", "AFRICA", "Strikes reported near Badme",
     "Drone and artillery fire on the Ethiopia-Eritrea border."),
    ("SUVA", "ASIA", "Fiji declares national disaster",
     "El Nino drought worsens; Tonga declares an emergency too."),
    ("LOS ANGELES", "AMERICAS", "El Nino storm threatens LA",
     "Flooding and mudslides feared; evacuations possible."),
    ("WASHINGTON", "GLOBAL", "IMF: world debt nears 100% of GDP",
     "Georgieva warns debt is highest since the Second World War."),
]

# Map markers: (longitude, latitude, region), one per story.
MARKERS = [
    (84.9, 19.3, "ASIA"), (30.5, 50.4, "EUROPE"), (19.0, 52.0, "EUROPE"),
    (25.0, 59.0, "EUROPE"), (44.2, 32.9, "MIDEAST"), (-1.8, 51.7, "EUROPE"),
    (4.4, 50.8, "EUROPE"), (13.4, 52.5, "EUROPE"), (46.7, 24.7, "MIDEAST"),
    (56.5, 26.5, "MIDEAST"), (34.5, 31.5, "MIDEAST"), (30.7, 36.9, "GLOBAL"),
    (-74.0, 40.7, "GLOBAL"), (-0.1, 51.5, "GLOBAL"), (-3.2, 55.9, "GLOBAL"),
    (8.0, 47.0, "GLOBAL"), (-89.2, 13.7, "AMERICAS"), (-17.4, 14.7, "AFRICA"),
    (29.5, 11.5, "AFRICA"), (-72.3, 18.5, "AMERICAS"), (139.7, 35.7, "ASIA"),
    (-47.9, -15.8, "AMERICAS"), (-52.0, -9.0, "AMERICAS"), (-74.0, 40.7, "GLOBAL"),
    (90.4, 23.8, "ASIA"), (35.2, 32.7, "MIDEAST"), (37.9, 14.7, "AFRICA"),
    (178.4, -18.1, "ASIA"), (-118.2, 34.1, "AMERICAS"), (-77.0, 38.9, "GLOBAL"),
]

# Rough continent outlines as (lon, lat) polygons, equirectangular.
LAND_POLYS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-75, 62), (-60, 55), (-55, 47), (-70, 44), (-75, 39), (-80, 32),
     (-81, 26), (-90, 21), (-97, 16), (-105, 20), (-115, 28), (-125, 40),
     (-125, 49), (-140, 60), (-155, 58), (-168, 66)],
    # Greenland
    [(-58, 64), (-45, 60), (-30, 68), (-20, 70), (-40, 76), (-58, 76)],
    # South America
    [(-80, 9), (-75, 11), (-62, 10), (-52, 5), (-50, -2), (-40, -5),
     (-35, -9), (-40, -20), (-48, -28), (-55, -35), (-65, -41), (-70, -50),
     (-73, -53), (-73, -37), (-70, -20), (-80, -5), (-80, 9)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (25, 65), (20, 70),
     (15, 71), (10, 68), (5, 60), (-5, 58), (-10, 54), (-10, 36)],
    # Africa
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -18), (32, -26), (26, -34),
     (18, -35), (15, -27), (12, -18), (9, -1), (9, 4), (-8, 4), (-13, 8),
     (-17, 15)],
    # Asia
    [(30, 62), (40, 68), (60, 70), (80, 73), (100, 76), (120, 73),
     (140, 72), (160, 70), (178, 66), (170, 60), (162, 56), (158, 53),
     (142, 50), (140, 40), (135, 35), (130, 33), (127, 35), (122, 38),
     (120, 32), (115, 23), (108, 18), (105, 10), (100, 8), (97, 16),
     (92, 21), (88, 22), (80, 15), (77, 8), (75, 20), (72, 20), (66, 25),
     (60, 25), (56, 26), (52, 28), (48, 30), (44, 29), (40, 31), (36, 36),
     (30, 36), (30, 42), (35, 45), (40, 48), (45, 52), (50, 55), (55, 58),
     (60, 60), (30, 62)],
    # Australia
    [(114, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -11), (137, -12),
     (132, -12), (126, -14), (122, -17), (118, -20), (114, -22)],
]


def typeface(size, bold=False):
    return ImageFont.truetype(BOLD_PATH if bold else REG_PATH, size)


def fit_text(draw, text, fnt, max_w):
    """Greedy word wrap of one string into lines no wider than max_w."""
    out = []
    for chunk in text.split("\n"):
        words = chunk.split()
        current = ""
        for word in words:
            trial = (current + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                current = trial
            else:
                if current:
                    out.append(current)
                current = word
        if current:
            out.append(current)
    return out


def draw_masthead(draw):
    draw.rectangle([0, 0, CANVAS_W, 96], fill=DARK)
    draw.rectangle([0, 96, CANVAS_W, 101], fill=ACCENT)
    draw.text((24, 14), "FRIDAY 20 NOVEMBER 2026",
              font=typeface(34, bold=True), fill=(255, 255, 255))
    draw.text((1000, 14), "THE WORLD IN ONE DAY",
              font=typeface(22, bold=True), fill=GOLD, anchor="ra")
    draw.text((24, 58), "30 STORIES  ·  SIX CONTINENTS  ·  ONE DAY",
              font=typeface(20, bold=True), fill=LIGHT_GREY)
    draw.text((1000, 58), "20 NOV 2026",
              font=typeface(20, bold=True), fill=LIGHT_GREY, anchor="ra")


def draw_map(draw):
    x0, y0, x1, y1 = 16, 114, 1008, 258
    draw.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=SEA,
                           outline=CARD_EDGE, width=1)
    draw.text((x0 + 10, y0 + 6), "WHERE THE NEWS HAPPENED",
              font=typeface(13, bold=True), fill=GREY)

    def project_xy(lon, lat):
        px = x0 + 8 + (lon + 170) / 360.0 * (x1 - x0 - 16)
        py = y0 + 22 + (75 - lat) / 130.0 * (y1 - y0 - 30)
        return (px, py)

    for poly in LAND_POLYS:
        draw.polygon([project_xy(lon, lat) for lon, lat in poly], fill=LAND)
    for lon, lat, _region in MARKERS:
        px, py = project_xy(lon, lat)
        draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=ACCENT,
                     outline=(255, 255, 255), width=1)


def draw_card(draw, index, place, region, headline, caption,
              cell_x, cell_y, cell_w, cell_h):
    colour = TAG[region]
    draw.rounded_rectangle([cell_x, cell_y, cell_x + cell_w, cell_y + cell_h],
                           radius=6, fill=CARD, outline=CARD_EDGE, width=1)
    draw.rectangle([cell_x, cell_y + 4, cell_x + 4, cell_y + cell_h - 4],
                   fill=colour)
    text_x = cell_x + 10
    draw.text((text_x, cell_y + 6), f"{index + 1:02d}  {place}",
              font=typeface(12, bold=True), fill=colour)
    y = cell_y + 24
    for line in fit_text(draw, headline, typeface(15, bold=True),
                         cell_w - 20)[:2]:
        draw.text((text_x, y), line, font=typeface(15, bold=True), fill=DARK)
        y += 18
    for line in fit_text(draw, caption, typeface(11), cell_w - 20)[:3]:
        draw.text((text_x, y), line, font=typeface(11), fill=GREY)
        y += 14


def render():
    assert len(ITEMS) == 30, f"expected 30 stories, got {len(ITEMS)}"
    assert len(MARKERS) == 30, f"expected 30 map markers, got {len(MARKERS)}"
    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
    draw = ImageDraw.Draw(canvas)

    draw_masthead(draw)
    draw_map(draw)

    margin, gap = 16, 8
    columns, rows = 5, 6
    grid_top = 270
    grid_h = CANVAS_H - grid_top - 30
    cell_w = (CANVAS_W - 2 * margin - (columns - 1) * gap) // columns
    cell_h = (grid_h - (rows - 1) * gap) // rows
    for i, (place, region, headline, caption) in enumerate(ITEMS):
        col, row = i % columns, i // columns
        draw_card(draw, i, place, region, headline, caption,
                  margin + col * (cell_w + gap),
                  grid_top + row * (cell_h + gap),
                  cell_w, cell_h)

    draw.text((512, CANVAS_H - 16),
              "All 30 stories happened or were first reported on Friday 20 November 2026.",
              font=typeface(14), fill=GREY, anchor="mm")

    canvas.save(OUTPUT, optimize=True)
    print(f"wrote {OUTPUT}: {canvas.size[0]}x{canvas.size[1]}")


if __name__ == "__main__":
    render()
