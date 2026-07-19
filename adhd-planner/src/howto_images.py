"""
Round 10 — "how it works" Etsy gallery images.

For each key daily-flow page, render the REAL planner page, overlay a natural,
hand-written example fill (Caveat handwriting font + hand-drawn circles/checks +
real habit-sticker PNGs), and place it on a cream card with a caption below —
matching the existing gallery style.

These are marketing mockups only; the planner PDFs are never modified.

    python src/howto_images.py [checkin|braindump|bank|breakdown|habit|all]
"""
import sys
import fitz
from PIL import Image, ImageDraw, ImageFont
from weasyprint import HTML

import config as C

CW = C.COLORS
OUT = C.ROOT / "etsy-assets"
PREV = C.BUILD_DIR / "preview"
PREV.mkdir(parents=True, exist_ok=True)
PDF = C.BUILD_DIR / "adhd-planner-light.pdf"

S = 2.4                       # page raster scale (pt -> px)
PEN = (58, 78, 108, 255)      # ink-pen blue-grey for the "handwriting"
PEN2 = (72, 92, 120, 255)
HAND = str(C.FONT_DIR / "Caveat-600.ttf")
LEX_B = str(C.FONTS["bold"])
LEX_M = str(C.FONTS["medium"])
LEX_R = str(C.FONTS["regular"])


# ---------------------------------------------------------------------------
# page raster + text lookup
# ---------------------------------------------------------------------------
def load_page(idx):
    doc = fitz.open(str(PDF))
    page = doc[idx]
    pix = page.get_pixmap(matrix=fitz.Matrix(S, S))
    img = Image.frombytes("RGBA", (pix.width, pix.height),
                          pix.samples) if pix.alpha else \
        Image.frombytes("RGB", (pix.width, pix.height), pix.samples).convert("RGBA")
    return page, img


def find(page, text, nth=0, near_y=None):
    """Pixel rect (x0,y0,x1,y1) of a match of `text`. With `near_y` (pixels) pick
    the hit closest to that row — guards against substring hits (e.g. 'Day' inside
    'today')."""
    hits = page.search_for(text)
    if not hits:
        return None
    if near_y is not None:
        r = min(hits, key=lambda h: abs(h.y0 * S - near_y))
    else:
        if nth >= len(hits):
            return None
        r = hits[nth]
    return (r.x0 * S, r.y0 * S, r.x1 * S, r.y1 * S)


# ---------------------------------------------------------------------------
# hand-drawn overlays (rendered on a temp layer + rotated for a natural feel)
# ---------------------------------------------------------------------------
def hand(img, xy, text, size, color=PEN, angle=0.0, anchor="lm"):
    font = ImageFont.truetype(HAND, size)
    tmp = Image.new("RGBA", (int(len(text) * size * 0.8) + 40, int(size * 1.8) + 20),
                    (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    d.text((10, 10), text, font=font, fill=color)
    bb = tmp.getbbox()
    tmp = tmp.crop(bb)
    if angle:
        tmp = tmp.rotate(angle, expand=True, resample=Image.BICUBIC)
    x, y = xy
    ax, ay = anchor
    px = x if ax == "l" else x - tmp.width // 2 if ax == "c" else x - tmp.width
    py = y - tmp.height // 2 if ay == "m" else y if ay == "t" else y - tmp.height
    img.alpha_composite(tmp, (int(px), int(py)))


def circle_rect(img, rect, color=PEN, pad=10, angle=-3, width=5):
    """Hand-drawn ellipse around a text rect."""
    x0, y0, x1, y1 = rect
    w = int(x1 - x0 + pad * 2) + 40
    h = int(y1 - y0 + pad * 2) + 40
    tmp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    d.ellipse([20, 20, w - 20, h - 20], outline=color, width=width)
    tmp = tmp.rotate(angle, expand=True, resample=Image.BICUBIC)
    cx = (x0 + x1) / 2 - tmp.width / 2
    cy = (y0 + y1) / 2 - tmp.height / 2
    img.alpha_composite(tmp, (int(cx), int(cy)))


def check_at(img, cx, cy, color=PEN, size=26, width=6):
    """A hand-drawn checkmark centred on (cx, cy)."""
    tmp = Image.new("RGBA", (size * 2, size * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    s = size
    d.line([(s * 0.55, s * 1.0), (s * 0.9, s * 1.35), (s * 1.5, s * 0.6)],
           fill=color, width=width, joint="curve")
    tmp = tmp.rotate(-4, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(tmp, (int(cx - tmp.width / 2), int(cy - tmp.height / 2)))


# ---------------------------------------------------------------------------
# compose: filled page card + caption, on a cream canvas
# ---------------------------------------------------------------------------
def compose(page_img, title, caption, out_name, page_w=940):
    scale = page_w / page_img.width
    pg = page_img.convert("RGB").resize(
        (page_w, int(page_img.height * scale)), Image.LANCZOS)

    pad = 70
    title_h = 96
    # wrap caption
    cap_font = ImageFont.truetype(LEX_M, 27)
    words = caption.split()
    lines, cur = [], ""
    maxw = page_w
    dummy = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    for w in words:
        t = (cur + " " + w).strip()
        if dummy.textlength(t, font=cap_font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    cap_h = int(len(lines) * 40 + 40)

    W = page_w + pad * 2
    H = title_h + pg.height + cap_h + pad * 2
    canvas = Image.new("RGB", (W, H), (251, 247, 239))  # cream
    dr = ImageDraw.Draw(canvas)

    # title
    tfont = ImageFont.truetype(LEX_B, 40)
    tw = dr.textlength(title, font=tfont)
    dr.text(((W - tw) / 2, pad), title, font=tfont, fill=(62, 74, 84))
    # accent bar
    dr.rounded_rectangle([(W / 2 - 42, pad + 62), (W / 2 + 42, pad + 68)],
                         radius=3, fill=(156, 203, 166))

    # page card with soft border
    px, py = pad, pad + title_h
    canvas.paste(pg, (px, py))
    dr.rectangle([px, py, px + pg.width - 1, py + pg.height - 1],
                 outline=(228, 220, 203), width=2)

    # caption
    cy = py + pg.height + 30
    for ln in lines:
        lw = dr.textlength(ln, font=cap_font)
        dr.text(((W - lw) / 2, cy), ln, font=cap_font, fill=(94, 143, 179))
        cy += 40

    canvas.save(str(OUT / out_name))
    canvas.resize((int(W * 0.42), int(H * 0.42))).save(str(PREV / ("hw-" + out_name)))
    print(f"  {out_name}  ({W}x{H})")


# ---------------------------------------------------------------------------
# 1 — Check-In
# ---------------------------------------------------------------------------
def build_checkin():
    page, img = load_page(1)
    # date fills (anchor Day/Year to the Month row to dodge substring hits)
    rm = find(page, "Month")
    row_y = rm[1] if rm else None
    for label, val, ang in [("Month", "July", -2), ("Day", "21", 1), ("Year", "'26", -2)]:
        r = find(page, label, near_y=row_y) if row_y else find(page, label)
        if r:
            hand(img, (r[2] + 14, (r[1] + r[3]) / 2 - 4), val, 44, angle=ang)
    # sleep: circle "Okay"
    r = find(page, "Okay")
    if r:
        circle_rect(img, r, pad=14, angle=-4)
    # energy: 2nd battery from left — interpolate between (low) and (high)
    lo, hi = find(page, "(low)"), find(page, "(high)")
    if lo and hi:
        lo_cx = (lo[0] + lo[2]) / 2
        hi_cx = (hi[0] + hi[2]) / 2
        b2x = lo_cx + (hi_cx - lo_cx) * (1 / 4)
        b_y = lo[1] - 42 * S / 2.4 - 20  # a touch above the (low) label row
        b_y = lo[1] - 44
        circle_rect(img, (b2x - 34, b_y - 24, b2x + 34, b_y + 24), pad=8, angle=-3)
    # mood: circle "Neutral"
    r = find(page, "Neutral")
    if r:
        circle_rect(img, r, pad=14, angle=3)
    # low box: check "Drink a glass of water"
    r = find(page, "Drink a glass of water")
    if r:
        check_at(img, r[0] - 30, (r[1] + r[3]) / 2)
    cap = ("Write today's date, then circle how you slept and how you're feeling. "
           "Circle the battery that matches your energy — low or high, so there's no "
           "number to guess. Right below, small tasks are already waiting that match "
           "that energy. Pick one, or write your own.")
    compose(img, "Daily Check-In", cap, "howto-1-checkin.png")


def pt(v):
    return v * S


# ---------------------------------------------------------------------------
# 2 — Brain Dump
# ---------------------------------------------------------------------------
def build_braindump():
    page, img = load_page(2)
    # scattered thoughts inside the big box (positions in pt, jittered angles)
    notes = [
        ("email landlord about the leak", 92, 300, -3, 42),
        ("call mom back!!", 452, 335, 2, 44),
        ("return boots — too small :(", 120, 432, -1, 42),
        ("Jenny's bday — the 22nd", 430, 470, 3, 42),
        ("renew library books", 150, 560, -2, 42),
    ]
    for txt, x, y, ang, sz in notes:
        hand(img, (pt(x), pt(y)), txt, sz, angle=ang, anchor="lt")
    # sort a couple into the table (Urgent / Later)
    u = find(page, "Urgent")
    if u:
        hand(img, (u[0], u[3] + pt(40)), "landlord", 40, angle=-1, anchor="lt")
    lt = find(page, "Later")
    if lt:
        hand(img, (lt[0], lt[3] + pt(40)), "return boots", 40, angle=1, anchor="lt")
    cap = ("Whatever's stuck in your head — write it down, no need to sort it yet. "
           "If something needs sorting, drop it into Urgent / Important / Later. "
           "If something needs action, tap through to Task Breakdown.")
    compose(img, "Brain Dump", cap, "howto-2-braindump.png")


# ---------------------------------------------------------------------------
# 3 — Low Energy Bank
# ---------------------------------------------------------------------------
def build_bank():
    page, img = load_page(3)
    # circle one browsed Work item (the pages are bullet menus, so "picking" =
    # a hand circle, not a checkbox)
    r = find(page, "Jot down just 1 thing for tomorrow")
    if r:
        circle_rect(img, r, pad=12, angle=-2, width=5)
    cap = ("Browse the full list, sorted by Work, Home, Relationships, and Other. "
           "Pick one that fits, then head back to your Check-In page to note it down. "
           "Nothing here feels right? That's okay too — write your own.")
    compose(img, "Energy Task Bank", cap, "howto-3-bank.png")


# ---------------------------------------------------------------------------
# 4 — Task Breakdown
# ---------------------------------------------------------------------------
def build_breakdown():
    page, img = load_page(5)
    r = find(page, "Big task:")
    if r:
        hand(img, (r[0] + pt(14), r[3] + pt(20)), "clean out the closet explosion",
             46, angle=-1, anchor="lm")
    r = find(page, "First, just this one")
    if r:
        hand(img, (r[0] + pt(6), r[3] + pt(14)), "put 5 things in the donate bag",
             44, angle=-1, anchor="lm")
    cap = ("Write the big task at the top. Then ignore everything else and just write "
           "the very first tiny step. That's the only one you do right now — the rest "
           "can wait.")
    compose(img, "Task Breakdown", cap, "howto-4-breakdown.png")


# ---------------------------------------------------------------------------
# 5 — Habit Tracker
# ---------------------------------------------------------------------------
def build_habit():
    page, img = load_page(8)
    # month / week meta
    r = find(page, "Month:")
    if r:
        hand(img, (r[2] + pt(12), (r[1] + r[3]) / 2), "July", 40, angle=-1)
    r = find(page, "Week of:")
    if r:
        hand(img, (r[2] + pt(12), (r[1] + r[3]) / 2), "the 7th", 40, angle=-1)
    # grid geometry (pt): content-left 48, name col 165 wide, 7 day cols of 72.43
    cl, name_w, day_w = 48.0, 165.0, (672.0 - 165.0) / 7
    header = [h for h in page.search_for("Habit") if 250 < h.y0 < 320]
    row1_y = (header[0].y1 + 50) if header else 334.0    # pt
    # habit name
    hand(img, (pt(cl + name_w / 2), pt(row1_y)), "drink water", 40, angle=-1, anchor="cm")
    # week of stamps: mixed GOOD / okay, with one blank day
    dots = {
        "g": Image.open(str(C.ASSET_DIR / "stickers/good-dot.png")).convert("RGBA"),
        "o": Image.open(str(C.ASSET_DIR / "stickers/okay-dot.png")).convert("RGBA"),
    }
    pattern = ["g", "g", "o", "", "g", "o", "g"]
    ds = 122
    for i, k in enumerate(pattern):
        if not k:
            continue
        cx = pt(cl + name_w + (i + 0.5) * day_w)
        cy = pt(row1_y)
        st = dots[k].resize((ds, ds), Image.LANCZOS)
        img.alpha_composite(st, (int(cx - ds / 2), int(cy - ds / 2)))
    cap = ("Write in the month and week. Each day, drag a stamp onto that day's cell — "
           "GOOD if you did it, it's okay if you didn't. A blank square doesn't mean "
           "failure here. It just means you'll try again tomorrow.")
    compose(img, "Habit Tracker", cap, "howto-5-habit.png")


BUILDERS = {"checkin": build_checkin, "braindump": build_braindump,
            "bank": build_bank, "breakdown": build_breakdown, "habit": build_habit}

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    print("how-to images ->", OUT)
    for k, fn in BUILDERS.items():
        if which in (k, "all"):
            fn()
