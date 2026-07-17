"""
Etsy listing gallery assets (the 'YOUR JOB' images).

Generates, into ../etsy-assets/:
  03-hyperlink-flow.png      page-to-page hyperlink map (the centerpiece)
  04-guilt-free-tracker.png  generic red-X tracker vs GOOD/it's okay stamps
  05-light-vs-dark.png       Check-In page in both modes, side by side
  07-whats-included.png      icon summary of everything in the download

All match the planner brand: cream bg, soft blue/green, Lexend. Rendered with
WeasyPrint then rasterized (2x) by PyMuPDF, so fonts embed correctly.

    python src/etsy_assets.py [flow|tracker|modes|included|all]
"""
import sys
from pathlib import Path

import fitz
from weasyprint import HTML
from PIL import Image

import config as C
from build import ICONS, battery_svg

CW = C.COLORS
F = C.FONTS
OUT = C.ROOT / "etsy-assets"
OUT.mkdir(exist_ok=True)
(C.BUILD_DIR / "preview").mkdir(parents=True, exist_ok=True)

FONT_FACE = f"""
@font-face {{ font-family:Lexend; font-weight:400; src:url("file://{F['regular']}"); }}
@font-face {{ font-family:Lexend; font-weight:500; src:url("file://{F['medium']}"); }}
@font-face {{ font-family:Lexend; font-weight:600; src:url("file://{F['semibold']}"); }}
@font-face {{ font-family:Lexend; font-weight:700; src:url("file://{F['bold']}"); }}
* {{ margin:0; padding:0; box-sizing:border-box; font-family:Lexend; }}
"""


def render_png(html, out, w, h, scale=2.0):
    pdf = C.BUILD_DIR / "preview" / (out.stem + ".pdf")
    HTML(string=html, base_url=str(C.ROOT)).write_pdf(str(pdf))
    d = fitz.open(str(pdf))
    d[0].get_pixmap(matrix=fitz.Matrix(scale, scale)).save(str(out))
    pdf.unlink()
    print(f"  {out.name}  ({int(w*scale)}x{int(h*scale)})")


# ===========================================================================
# #3 — Hyperlink flow diagram
# ===========================================================================
def build_flow():
    W, H = 1200, 1580

    def node(x, y, label, icon, tint, w=250, h=104):
        return (f'<div class="node n-{tint}" style="left:{x}px;top:{y}px;'
                f'width:{w}px;height:{h}px">'
                f'<div class="ni ni-{tint}">{ICONS[icon]}</div>'
                f'<span>{label}</span></div>')

    EDGE = f'fill="none" stroke="{CW["ink_soft"]}" stroke-width="3.2" marker-end="url(#ah)"'
    LOOP = (f'fill="none" stroke="{CW["green_deep"]}" stroke-width="3.2" '
            f'stroke-dasharray="8 7" marker-end="url(#ahg)"')

    # node top-left positions
    N = {
        "mindset":  (150, 300, "Mindset", "moon", "blue"),
        "checkin":  (150, 452, "Check-In", "sun", "blue"),
        "low":      (770, 388, "Low Energy Bank", "battery", "green"),
        "high":     (770, 516, "High Energy Bank", "battery", "green"),
        "brain":    (150, 636, "Brain Dump", "cloud", "blue"),
        "task":     (150, 788, "Task Breakdown", "list", "green"),
        "focus":    (150, 940, "Focus Plan", "target", "blue"),
        "putoff":   (150, 1092, "Why Putting Off?", "help", "blue"),
        "habit":    (150, 1244, "Habit Tracker", "grid", "green"),
        "reward":   (150, 1396, "Reward Chart", "star", "green"),
    }
    nodes = "".join(node(*v) for v in N.values())

    HGT = 104
    ax = N["mindset"][0] + 125   # 275 column-A center x
    def varrow(a, b):
        y1 = N[a][1] + HGT
        y2 = N[b][1]
        return f'<path {EDGE} d="M{ax},{y1} L{ax},{y2-12}"/>'
    chain = [("mindset", "checkin"), ("brain", "task"), ("task", "focus"),
             ("focus", "putoff"), ("putoff", "habit"), ("habit", "reward")]
    checkin_bottom = N["checkin"][1] + HGT
    brain_top = N["brain"][1]
    varr = "".join(varrow(a, b) for a, b in chain)
    varr += f'<path {EDGE} d="M{ax},{checkin_bottom} L{ax},{brain_top-12}"/>'

    # check-in right edge -> banks (curved)
    cin_rx = N["checkin"][0] + 250
    cin_cy = N["checkin"][1] + HGT // 2
    low_lx = N["low"][0]
    low_cy = N["low"][1] + HGT // 2
    high_cy = N["high"][1] + HGT // 2
    branch = (
        f'<path {EDGE} d="M{cin_rx},{cin_cy-16} C620,{cin_cy-16} 640,{low_cy} {low_lx-12},{low_cy}"/>'
        f'<path {EDGE} d="M{cin_rx},{cin_cy+16} C620,{cin_cy+16} 640,{high_cy} {low_lx-12},{high_cy}"/>')

    # loop-back: Why Putting Off -> Task Breakdown (bows right, going up)
    put_rx = N["putoff"][0] + 250
    put_cy = N["putoff"][1] + HGT // 2
    task_rx = N["task"][0] + 250
    task_cy = N["task"][1] + HGT // 2
    loop = (f'<path {LOOP} d="M{put_rx},{put_cy} C580,{put_cy} 580,{task_cy} '
            f'{task_rx+12},{task_cy}"/>')
    loop_label = ('<div class="loop-label" style="left:470px;top:965px">loops back to<br>the right tool</div>')

    svg = (f'<svg class="wires" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
           f'<defs>'
           f'<marker id="ah" markerWidth="9" markerHeight="9" refX="6.5" refY="3" '
           f'orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="{CW["ink_soft"]}"/></marker>'
           f'<marker id="ahg" markerWidth="9" markerHeight="9" refX="6.5" refY="3" '
           f'orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="{CW["green_deep"]}"/></marker>'
           f'</defs>{varr}{branch}{loop}</svg>')

    html = f"""<!doctype html><html><head><meta charset=utf-8><style>{FONT_FACE}
      @page {{ size:{W}px {H}px; margin:0; }}
      body {{ width:{W}px; height:{H}px; background:{CW['bg']}; position:relative; }}
      .title {{ text-align:center; padding:70px 80px 0; }}
      .title h1 {{ font-size:56px; font-weight:700; color:{CW['ink']}; line-height:1.15; }}
      .title .sub {{ font-size:26px; color:{CW['blue_deep']}; margin-top:16px; font-weight:500; }}
      .title .accent {{ width:96px;height:6px;border-radius:3px;background:{CW['green']};margin:24px auto 0; }}
      .wires {{ position:absolute; left:0; top:0; }}
      .edge {{ fill:none; stroke:{CW['ink_soft']}; stroke-width:3; marker-end:url(#ah); }}
      .edge.loop {{ stroke:{CW['green_deep']}; stroke-dasharray:7 7; }}
      .node {{ position:absolute; border-radius:20px; display:flex; align-items:center;
        gap:16px; padding:0 22px; box-shadow:0 6px 18px rgba(60,74,84,0.10);
        font-size:23px; font-weight:600; color:{CW['ink']}; z-index:2; }}
      .n-blue {{ background:{CW['blue_bg']}; border:2px solid {CW['blue']}; }}
      .n-green {{ background:{CW['green_bg']}; border:2px solid {CW['green']}; }}
      .ni {{ width:48px;height:48px;border-radius:13px;flex:0 0 auto;
        display:flex;align-items:center;justify-content:center; }}
      .ni .nav-icon {{ width:26px;height:26px; }}
      .ni-blue {{ background:#fff;color:{CW['blue_deep']}; }}
      .ni-green {{ background:#fff;color:{CW['green_deep']}; }}
      .loop-label {{ position:absolute; font-size:17px; color:{CW['green_deep']};
        font-weight:600; text-align:center; z-index:2; line-height:1.3; }}
      .foot {{ position:absolute; bottom:34px; left:0; right:0; text-align:center;
        font-size:20px; color:{CW['ink_soft']}; }}
    </style></head><body>
      <div class="title"><h1>Tap once. Land exactly where you need.</h1>
        <div class="sub">Every link tested &mdash; no dead ends, no scrolling to find the page.</div>
        <div class="accent"></div></div>
      {svg}{nodes}{loop_label}
      <div class="foot">ADHD Reset Planner &nbsp;&middot;&nbsp; functional hyperlinks, not just page flips</div>
    </body></html>"""
    render_png(html, OUT / "03-hyperlink-flow.png", W, H)


# ===========================================================================
# #5 — Light vs Dark comparison (real Check-In pages)
# ===========================================================================
def build_modes():
    _H=1330
    prev = C.BUILD_DIR / "preview"
    shots = {}
    for mode, pdf in [("light", "adhd-planner-light.pdf"), ("dark", "adhd-planner-dark.pdf")]:
        d = fitz.open(str(C.BUILD_DIR / pdf))
        p = prev / f"checkin-{mode}.png"
        d[1].get_pixmap(matrix=fitz.Matrix(1.4, 1.4)).save(str(p))  # page 2 = Check-In
        shots[mode] = p

    W, H = 1680, 1330
    def card(mode, label, badge_tint):
        return f"""
          <div class="card">
            <img src="file://{shots[mode]}"/>
            <div class="cap"><span class="badge {badge_tint}">{label}</span></div>
          </div>"""
    html = f"""<!doctype html><html><head><meta charset=utf-8><style>{FONT_FACE}
      @page {{ size:{W}px {H}px; margin:0; }}
      body {{ width:{W}px; height:{H}px; background:{CW['bg']}; }}
      .head {{ text-align:center; padding:70px 80px 10px; }}
      .head h1 {{ font-size:56px; font-weight:700; color:{CW['ink']}; }}
      .head .sub {{ font-size:26px; color:{CW['blue_deep']}; margin-top:14px; font-weight:500; }}
      .head .accent {{ width:96px;height:6px;border-radius:3px;background:{CW['green']};margin:22px auto 0; }}
      .row {{ display:flex; gap:70px; justify-content:center; padding:40px 90px; }}
      .card {{ display:flex; flex-direction:column; align-items:center; gap:22px; }}
      .card img {{ width:640px; border-radius:22px; box-shadow:0 18px 46px rgba(60,74,84,0.24);
        border:1px solid {CW['line']}; }}
      .badge {{ font-size:26px; font-weight:600; padding:12px 34px; border-radius:999px; }}
      .b-light {{ background:{CW['blue_bg']}; color:{CW['blue_deep']}; }}
      .b-dark {{ background:#2B3036; color:#D9DEE3; }}
      .foot {{ text-align:center; font-size:22px; color:{CW['ink_soft']}; margin-top:6px; }}
    </style></head><body>
      <div class="head"><h1>Two moods. One gentle planner.</h1>
        <div class="sub">Same pages, same working links &mdash; pick the theme your eyes prefer.</div>
        <div class="accent"></div></div>
      <div class="row">
        {card("light", "Light  (recommended)", "b-light")}
        {card("dark", "Dark  (easy on night eyes)", "b-dark")}
      </div>
      <div class="foot">Both files included &mdash; use one, or switch by time of day.</div>
    </body></html>"""
    render_png(html, OUT / "05-light-vs-dark.png", W, H)


# ===========================================================================
# #4 — Guilt-free tracker: generic red-X vs GOOD / it's okay
# ===========================================================================
def build_tracker():
    W, H = 1680, 760
    RED = "#CF5F55"       # clear, generic red — not disparaging any brand
    GREYX = "#9BA0A6"     # neutral grey (no green cast) for the "done" checks
    days = ["M", "T", "W", "T", "F", "S", "S"]
    stick = C.ASSET_DIR / "stickers"

    # LEFT: the usual guilt tracker — neutral-grey checks, hard red X on misses,
    # and a faint red wash on the missed cells so "failure" pops at a glance.
    xmark = (f'<svg viewBox="0 0 24 24" width="36" height="36" fill="none" stroke="{RED}" '
             f'stroke-width="3.4" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>')
    checkg = (f'<svg viewBox="0 0 24 24" width="34" height="34" fill="none" stroke="{GREYX}" '
              f'stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12l5 5L20 6"/></svg>')
    # (mark, is_miss)
    left_marks = [(checkg, False), (checkg, False), (xmark, True), (xmark, True),
                  (checkg, False), (xmark, True), (xmark, True)]
    left_cells = "".join(
        f'<td class="{"miss" if miss else ""}">{m}</td>' for m, miss in left_marks)
    left_head = "".join(f'<th>{d}</th>' for d in days)

    # RIGHT: our stamps — SAME week, SAME pattern, so each day contrasts directly:
    #   a missed day (red X, left)  ->  lavender "it's okay" stamp (right)
    #   a done day  (grey check)    ->  green "GOOD" stamp (right)
    good = f'<img src="file://{stick}/good-dot.png"/>'
    okay = f'<img src="file://{stick}/okay-dot.png"/>'
    right_marks = [okay if miss else good for _, miss in left_marks]
    right_cells = "".join(f'<td>{m}</td>' for m in right_marks)
    right_head = "".join(f'<th>{d}</th>' for d in days)

    html = f"""<!doctype html><html><head><meta charset=utf-8><style>{FONT_FACE}
      @page {{ size:{W}px {H}px; margin:0; }}
      body {{ width:{W}px; height:{H}px; background:{CW['bg']}; }}
      .head {{ text-align:center; padding:66px 80px 6px; }}
      .head h1 {{ font-size:54px; font-weight:700; color:{CW['ink']}; }}
      .head .sub {{ font-size:25px; color:{CW['ink_soft']}; margin-top:14px; }}
      .head .accent {{ width:96px;height:6px;border-radius:3px;background:{CW['green']};margin:20px auto 0; }}
      .row {{ display:flex; gap:54px; justify-content:center; padding:44px 80px; align-items:stretch; }}
      .panel {{ flex:1; border-radius:26px; padding:40px 42px; }}
      .p-before {{ background:#FbF1F0; border:2px solid {RED}; }}
      .p-after {{ background:{CW['green_bg']}; border:2px solid {CW['green']}; }}
      .plabel {{ font-size:22px; font-weight:600; letter-spacing:1px; text-transform:uppercase; }}
      .l-before {{ color:{RED}; }} .l-after {{ color:{CW['green_deep']}; }}
      .ptitle {{ font-size:34px; font-weight:700; color:{CW['ink']}; margin:8px 0 8px; }}
      table {{ width:100%; border-collapse:collapse; margin:22px 0 10px; text-align:center; }}
      th {{ font-size:24px; font-weight:600; color:{CW['ink_soft']}; padding:10px 0; }}
      td {{ height:96px; border:1px solid {CW['line']}; }}
      td.miss {{ background:#F7DEDA; }}
      td img {{ width:56px; height:56px; vertical-align:middle; }}
      .banner {{ margin-top:20px; padding:16px 22px; border-radius:14px; font-size:24px;
        font-weight:600; text-align:center; }}
      .ban-bad {{ background:{RED}; color:#fff; }}
      .ban-good {{ background:#fff; color:{CW['green_deep']}; border:1.5px solid {CW['green']}; }}
      .feel {{ font-size:22px; margin-top:16px; color:{CW['ink_soft']}; text-align:center; }}
    </style></head><body>
      <div class="head"><h1>Same week. A completely different feeling.</h1>
        <div class="sub">No red X. No broken streaks. No day marked as a failure.</div>
        <div class="accent"></div></div>
      <div class="row">
        <div class="panel p-before">
          <div class="plabel l-before">The usual way</div>
          <div class="ptitle">Miss a day &rarr; you failed.</div>
          <table><tr>{left_head}</tr><tr>{left_cells}</tr></table>
          <div class="banner ban-bad">✗ Streak lost. Start over.</div>
          <div class="feel">…so you stop opening it.</div>
        </div>
        <div class="panel p-after">
          <div class="plabel l-after">This planner</div>
          <div class="ptitle">Miss a day &rarr; still okay.</div>
          <table><tr>{right_head}</tr><tr>{right_cells}</tr></table>
          <div class="banner ban-good">GOOD or it&rsquo;s okay — both count.</div>
          <div class="feel">Rest counts too. 🌿</div>
        </div>
      </div>
    </body></html>"""
    render_png(html, OUT / "04-guilt-free-tracker.png", W, H)


# ===========================================================================
# #7 — What's included infographic
# ===========================================================================
def build_included():
    W, H = 1680, 910
    doc = ('<svg viewBox="0 0 24 24" width="40" height="40" fill="none" stroke="currentColor" '
           'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
           '<path d="M6 2h8l4 4v16H6z"/><path d="M14 2v4h4M9 13h6M9 17h6"/></svg>')
    stick = C.ASSET_DIR / "stickers"

    def card(icon_html, title, cap, tint):
        return f"""
          <div class="card">
            <div class="ic ic-{tint}">{icon_html}</div>
            <div class="ct">{title}</div>
            <div class="cc">{cap}</div>
          </div>"""

    moon = ICONS["moon"]; sun = ICONS["sun"]; grid = ICONS["grid"]; help_i = ICONS["help"]
    stamp_img = (f'<img src="file://{stick}/good-dot.png"/><img src="file://{stick}/okay-dot.png" '
                 f'style="margin-left:-10px"/>')
    cards = "".join([
        card(f'<span class="ico">{sun}</span>' + doc, "Light PDF", "the main planner, 11 pages", "blue"),
        card(f'<span class="ico">{moon}</span>' + doc, "Dark PDF", "same planner, night theme", "blue"),
        card(f'<div class="stamps">{stamp_img}</div>', "4 Habit Stickers", "GOOD + it's okay, drag & drop", "green"),
        card(grid, "Sticker Sheet", "lasso-copy inside any app", "green"),
        card(doc, "Start-Here Guide", "60-second setup, illustrated", "blue"),
        card(help_i, "README + FAQ", "per-app help & troubleshooting", "green"),
    ])
    html = f"""<!doctype html><html><head><meta charset=utf-8><style>{FONT_FACE}
      @page {{ size:{W}px {H}px; margin:0; }}
      body {{ width:{W}px; height:{H}px; background:{CW['bg']}; }}
      .head {{ text-align:center; padding:70px 80px 6px; }}
      .head h1 {{ font-size:56px; font-weight:700; color:{CW['ink']}; }}
      .head .sub {{ font-size:26px; color:{CW['blue_deep']}; margin-top:14px; font-weight:500; }}
      .head .accent {{ width:96px;height:6px;border-radius:3px;background:{CW['green']};margin:22px auto 0; }}
      .grid {{ display:flex; flex-wrap:wrap; gap:44px; padding:56px 110px; justify-content:center; }}
      .card {{ width:400px; background:#fff; border:1px solid {CW['line']}; border-radius:24px;
        padding:38px 34px; box-shadow:0 8px 22px rgba(60,74,84,0.08);
        display:flex; flex-direction:column; align-items:flex-start; gap:12px; }}
      .ic {{ width:84px; height:84px; border-radius:20px; display:flex; align-items:center;
        justify-content:center; gap:2px; }}
      .ic-blue {{ background:{CW['blue_bg']}; color:{CW['blue_deep']}; }}
      .ic-green {{ background:{CW['green_bg']}; color:{CW['green_deep']}; }}
      .ic .ico .nav-icon {{ width:30px; height:30px; margin-right:-4px; }}
      .stamps img {{ width:52px; height:52px; }}
      .ct {{ font-size:30px; font-weight:700; color:{CW['ink']}; }}
      .cc {{ font-size:21px; color:{CW['ink_soft']}; }}
      .foot {{ text-align:center; font-size:23px; color:{CW['ink_soft']}; }}
    </style></head><body>
      <div class="head"><h1>Everything in your instant download</h1>
        <div class="sub">One zip. No account, no add-ons, no waiting.</div>
        <div class="accent"></div></div>
      <div class="grid">{cards}</div>
      <div class="foot">Works with GoodNotes &amp; Notability on iPad &middot; Xodo on Android</div>
    </body></html>"""
    render_png(html, OUT / "07-whats-included.png", W, H)


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    print("etsy assets ->", OUT)
    if which in ("flow", "all"):
        build_flow()
    if which in ("modes", "all"):
        build_modes()
    if which in ("tracker", "all"):
        build_tracker()
    if which in ("included", "all"):
        build_included()
