"""
Round 11 — layer captions + inline link callouts onto the shop owner's real
hand-filled screenshots (never altering the handwriting).

For each page: draw small soft-blue callout pills with a leader line pointing at
each tappable link, then place the annotated screenshot on a cream card with the
overall caption below — matching the existing gallery style.

    python src/annotate_gallery.py [checkin|braindump|low|high|breakdown|all]
"""
import sys
import fitz
from PIL import Image, ImageDraw, ImageFont

import config as C
from howto_images import compose, check_at  # cream-card composer + hand checkmark

SRC = C.ROOT / "etsy-assets"
SHOT_DIR = SRC / "screenshots"        # the owner's raw hand-filled screenshots
LIGHT = C.BUILD_DIR / "adhd-planner-light.pdf"

# uploaded screenshots (1080x1440), mapped to their page
SHOTS = {
    "checkin":   ("KakaoTalk_20260719_215111151.jpg", 1),
    "braindump": ("KakaoTalk_20260719_215141030.jpg", 2),
    "low":       ("KakaoTalk_20260719_215214835.jpg", 3),
    "high":      ("KakaoTalk_20260719_215236274.jpg", 4),
    "breakdown": ("KakaoTalk_20260719_215258576.jpg", 5),
    "focus":     ("KakaoTalk_20260719_215318627.jpg", 6),
    "whyputoff": ("KakaoTalk_20260719_215338152.jpg", 7),
    "reward":    ("KakaoTalk_20260719_215400800.jpg", 9),
    "thismonth": ("KakaoTalk_20260719_215418053.jpg", 10),
}

# screenshot px per PDF point
IMG_W, IMG_H = 1080, 1440
SX, SY = IMG_W / 768.0, IMG_H / 1024.5

BLUE_BG = (231, 240, 246)
BLUE = (143, 184, 214)
BLUE_INK = (74, 116, 150)
PILL_FONT = str(C.FONTS["medium"])


def link_rect(page, text, near_y=None):
    hits = page.search_for(text)
    if not hits:
        return None
    if near_y is not None:
        hits = [min(hits, key=lambda r: abs(r.y0 * SY - near_y))]
    r = hits[0]
    return (r.x0 * SX, r.y0 * SY, r.x1 * SX, r.y1 * SY)


def _wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def callout(img, target, pill_center, label, maxw=360, fs=30, leader=True):
    """Rounded blue pill with wrapped label. With `leader` (default) also draws a
    line + arrowhead to `target`; set leader=False for a standalone box."""
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(PILL_FONT, fs)
    lines = _wrap(d, label, font, maxw)
    tw = max(d.textlength(ln, font=font) for ln in lines)
    lh = fs + 8
    padx, pady = 22, 14
    pw, ph = tw + padx * 2, len(lines) * lh + pady * 2
    cx, cy = pill_center
    x0, y0 = cx - pw / 2, cy - ph / 2
    x1, y1 = x0 + pw, y0 + ph

    if leader:
        tx, ty = target
        # leader: from the pill edge nearest the target, to the target point
        ex = min(max(tx, x0), x1)
        ey = min(max(ty, y0), y1)
        d.line([(ex, ey), (tx, ty)], fill=BLUE_INK, width=3)
        # arrowhead at target
        import math
        ang = math.atan2(ty - ey, tx - ex)
        a = 12
        d.polygon([(tx, ty),
                   (tx - a * math.cos(ang - 0.5), ty - a * math.sin(ang - 0.5)),
                   (tx - a * math.cos(ang + 0.5), ty - a * math.sin(ang + 0.5))],
                  fill=BLUE_INK)
    # pill
    d.rounded_rectangle([x0, y0, x1, y1], radius=ph / 2 if len(lines) == 1 else 20,
                        fill=BLUE_BG, outline=BLUE, width=3)
    yy = y0 + pady
    for ln in lines:
        lw = d.textlength(ln, font=font)
        d.text((cx - lw / 2, yy), ln, font=font, fill=BLUE_INK)
        yy += lh


def annotate(kind):
    """Return (annotated_page_img, title, caption) for one page."""
    fname, idx = SHOTS[kind]
    img = Image.open(str(SHOT_DIR / fname)).convert("RGBA")
    doc = fitz.open(str(LIGHT))
    page = doc[idx]

    if kind == "checkin":
        callout(img, None, (792, 236),
                "tap to return to the Mindset page anytime", maxw=344, leader=False)
        r = link_rect(page, "tap for full Low Energy Bank")
        callout(img, ((r[0] + r[2]) / 2, r[3] + 2), (230, 1330),
                "tap for more options", maxw=340, fs=28)
        r = link_rect(page, "tap for full High Energy Bank")
        callout(img, ((r[0] + r[2]) / 2, r[3] + 2), (710, 1330),
                "tap for more options", maxw=340, fs=28)
        title = "Daily Check-In"
        cap = ("Write today's date, then circle how you slept and how you're feeling. "
               "Circle the battery icon that matches your energy — low or high, so "
               "there's no number to guess. Right below, a few small tasks are already "
               "waiting that match that energy. Pick one, or write your own.")

    elif kind == "braindump":
        r = link_rect(page, "Take it to Task Breakdown")
        callout(img, ((r[0] + r[2]) / 2, r[3] + 2), (392, 1356),
                "tap to start breaking it into steps", maxw=560, fs=28)
        title = "Brain Dump"
        cap = ("Whatever's stuck in your head — write it down, no need to sort it yet. "
               "If something needs sorting, drop it into Urgent / Important / Later. "
               "If something needs action, tap through to Task Breakdown.")

    elif kind in ("low", "high"):
        r = link_rect(page, "Back to Check-In")
        callout(img, ((r[0] + r[2]) / 2, r[3]), (792, 220),
                "tap to go back and note down what you picked", maxw=300)
        title = "Low Energy Bank" if kind == "low" else "High Energy Bank"
        cap = ("Browse the full list, sorted by Work, Home, Relationships, and Other. "
               "Pick one that fits, then head back to your Check-In page to note it "
               "down. Nothing here feels right? That's okay too — write your own.")

    elif kind == "breakdown":
        title = "Task Breakdown"
        cap = ("Write the big task at the top. Then ignore everything else and just "
               "write the very first tiny step. That's the only one you do right now — "
               "the rest can wait.")

    elif kind == "focus":
        title = "Focus Plan"
        cap = ("Name what's pulling your attention right now — up to 3 things. If you "
               "can remove one, do. If not, that's fine too. Then try 25 minutes. No "
               "pressure, just try.")

    elif kind == "whyputoff":
        callout(img, None, (842, 286),
                "the blue text jumps straight to that tool", maxw=316, leader=False)
        title = "Why Am I Putting This Off?"
        cap = ("Pick whichever reason fits today — no need to figure out the “real” "
               "one. Each reason links straight to the tool that actually helps, so "
               "you're never stuck wondering what to do next.")

    elif kind == "reward":
        # per request: check one 'Can't think of one' box so the opt-out feature shows.
        # Use the Big row (3rd) — empty, so 'save it for later' reads naturally.
        boxes = page.search_for("Can't think of one")
        b = boxes[2]                      # Big row
        cy = (b.y0 + b.y1) / 2 * SY
        cx = b.x0 * SX - 30               # checkbox sits just left of the text
        check_at(img, cx, cy, color=(44, 49, 62), size=24, width=6)
        title = "Reward Chart"
        cap = ("Decide what you'll give yourself before you even start — small, medium, "
               "or big. Can't think of anything? Check that box and decide later. "
               "Rewards aren't something you have to earn.")

    elif kind == "thismonth":
        title = "This Month"
        cap = ("Write in the month and year, then just three things you want from it — "
               "no more. The calendar and note below are yours to use or skip completely.")

    return img, title, cap


NAMES = {"checkin": "howto-1-checkin.png", "braindump": "howto-2-braindump.png",
         "low": "howto-3-low-energy.png", "high": "howto-4-high-energy.png",
         "breakdown": "howto-5-task-breakdown.png", "focus": "howto-6-focus.png",
         "whyputoff": "howto-7-why-putting-off.png", "reward": "howto-8-reward.png",
         "thismonth": "howto-9-this-month.png"}


def build(kind):
    img, title, cap = annotate(kind)
    compose(img, title, cap, NAMES[kind])


# ---------------------------------------------------------------------------
# Combined Low + High Energy Bank (side-by-side, "Two moods" style)
# ---------------------------------------------------------------------------
def _rounded(im, rad):
    from PIL import ImageDraw as _D
    mask = Image.new("L", im.size, 0)
    _D.Draw(mask).rounded_rectangle([0, 0, im.size[0] - 1, im.size[1] - 1], rad, fill=255)
    out = im.convert("RGBA")
    out.putalpha(mask)
    return out


def build_combined():
    from PIL import ImageFilter
    CREAM = (251, 247, 239)
    INK = (62, 74, 84)
    BLUEDEEP = (94, 143, 179)
    GREEN = (156, 203, 166)
    LINE = (228, 220, 203)

    low = annotate("low")[0]
    high = annotate("high")[0]
    PW = 626
    ph = int(low.height * PW / low.width)
    low = low.convert("RGB").resize((PW, ph), Image.LANCZOS)
    high = high.convert("RGB").resize((PW, ph), Image.LANCZOS)

    pad, gap, title_h = 80, 60, 210
    caption = ("Browse the full list, sorted by Work, Home, Relationships, and Other. "
               "Pick one that fits, then head back to your Check-In page to note it "
               "down. Nothing here feels right? That's okay too — write your own.")
    W = pad * 2 + PW * 2 + gap
    cap_font = ImageFont.truetype(str(C.FONTS["medium"]), 27)
    tmp_d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    cap_lines = _wrap(tmp_d, caption, cap_font, W - pad * 2)
    cap_h = len(cap_lines) * 40 + 50
    H = title_h + ph + cap_h + pad

    canvas = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(canvas)

    # title + subtitle + accent
    tfont = ImageFont.truetype(str(C.FONTS["bold"]), 54)
    sfont = ImageFont.truetype(str(C.FONTS["medium"]), 27)
    title = "Match your energy, not the clock."
    sub = "Same planner, two lists — pick what matches how you feel today."
    d.text(((W - d.textlength(title, font=tfont)) / 2, 66), title, font=tfont, fill=INK)
    d.text(((W - d.textlength(sub, font=sfont)) / 2, 132), sub, font=sfont, fill=BLUEDEEP)
    d.rounded_rectangle([(W / 2 - 48, 182), (W / 2 + 48, 188)], radius=3, fill=GREEN)

    # two page cards with rounded corners + soft shadow
    def paste_card(card, x, y, rad=22):
        shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        sb = Image.new("RGBA", (card.width, card.height), (0, 0, 0, 0))
        ImageDraw.Draw(sb).rounded_rectangle([0, 0, card.width - 1, card.height - 1],
                                             rad, fill=(60, 74, 84, 80))
        shadow.paste(sb, (x, y + 16), sb)
        shadow = shadow.filter(ImageFilter.GaussianBlur(20))
        canvas.alpha_composite(shadow)
        rc = _rounded(card, rad)
        canvas.alpha_composite(rc, (x, y))
        d.rounded_rectangle([x, y, x + card.width - 1, y + card.height - 1],
                            rad, outline=LINE, width=2)

    y0 = title_h
    paste_card(low, pad, y0)
    paste_card(high, pad + PW + gap, y0)

    # caption
    cy = y0 + ph + 34
    for ln in cap_lines:
        d.text(((W - d.textlength(ln, font=cap_font)) / 2, cy), ln, font=cap_font, fill=BLUEDEEP)
        cy += 40

    out = SRC / "howto-energy-banks-combined.png"
    canvas.convert("RGB").save(str(out))
    canvas.convert("RGB").resize((int(W * 0.4), int(H * 0.4))).save(
        str(C.BUILD_DIR / "preview" / "hw-combined.png"))
    print(f"  {out.name}  ({W}x{H})")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    print("annotating gallery ->", SRC)
    if which in ("combined", "all"):
        build_combined()
    for k in SHOTS:
        if which in (k, "all"):
            build(k)
