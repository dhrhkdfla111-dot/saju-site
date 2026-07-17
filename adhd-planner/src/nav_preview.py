"""Render 3 nav-bar style options as a comparison image for sign-off."""
import fitz
from weasyprint import HTML
import config as C
from build import ICONS

CW = C.COLORS

def bar_tabs(active="checkin"):
    tabs = ""
    for t in C.NAV_TABS:
        a = "active" if t["key"] == active else ""
        tabs += (f'<a class="t {a}" href="#">{ICONS[t["icon"]]}<span>{t["label"]}</span></a>')
    return f'<nav class="tabs">{tabs}</nav>'

def bar_pills(active="checkin"):
    tabs = ""
    for t in C.NAV_TABS:
        a = "active" if t["key"] == active else ""
        tabs += (f'<a class="p {a}" href="#">{ICONS[t["icon"]]}<span>{t["label"]}</span></a>')
    return f'<nav class="pills">{tabs}</nav>'

def bar_min(active="checkin"):
    tabs = ""
    for t in C.NAV_TABS:
        a = "active" if t["key"] == active else ""
        lbl = f'<span>{t["label"]}</span>' if a else ""
        tabs += (f'<a class="m {a}" href="#">{ICONS[t["icon"]]}{lbl}</a>')
    return f'<nav class="min">{tabs}</nav>'

STYLES = f"""
@font-face {{ font-family:Lexend; font-weight:500; src:url("file://{C.FONTS['medium']}"); }}
@font-face {{ font-family:Lexend; font-weight:600; src:url("file://{C.FONTS['semibold']}"); }}
@font-face {{ font-family:Lexend; font-weight:700; src:url("file://{C.FONTS['bold']}"); }}
@page {{ size:{C.PAGE_W}px 300px; margin:0; }}
* {{ box-sizing:border-box; margin:0; padding:0; font-family:Lexend; }}
body {{ background:{CW['bg']}; }}
.frame {{ width:{C.PAGE_W}px; height:300px; background:{CW['bg']}; position:relative; }}
.cap {{ position:absolute; bottom:16px; left:40px; color:{CW['ink_soft']}; font-size:20px; font-weight:600; }}
.ghost {{ position:absolute; bottom:70px; left:40px; color:{CW['ink_faint']}; font-size:34px; font-weight:700; }}
.nav-icon {{ width:24px; height:24px; }}

/* option 1 — segmented tabs */
.tabs {{ display:flex; height:88px; background:{CW['nav_bg']}; border-bottom:1px solid {CW['line']}; }}
.tabs .t {{ flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center;
  gap:4px; text-decoration:none; color:{CW['nav_ink']}; font-size:15px; font-weight:500;
  border-right:1px solid {CW['line']}; }}
.tabs .t:last-child {{ border-right:none; }}
.tabs .t.active {{ color:#fff; background:{CW['nav_active']}; }}

/* option 2 — floating pills */
.pills {{ display:flex; gap:12px; padding:20px 28px; justify-content:center; }}
.pills .p {{ display:flex; align-items:center; gap:8px; padding:12px 20px; border-radius:999px;
  background:{CW['bg_soft']}; color:{CW['nav_ink']}; text-decoration:none; font-size:15px;
  font-weight:500; border:1px solid {CW['line']}; }}
.pills .p .nav-icon {{ width:20px; height:20px; }}
.pills .p.active {{ background:{CW['blue']}; color:#fff; border-color:{CW['blue']}; }}

/* option 3 — minimal icons, label on active only */
.min {{ display:flex; gap:34px; padding:24px 40px; align-items:center; }}
.min .m {{ display:flex; align-items:center; gap:8px; color:{CW['ink_faint']}; text-decoration:none;
  font-size:15px; font-weight:600; }}
.min .m.active {{ color:{CW['blue_deep']}; }}
.min .m.active .nav-icon {{ color:{CW['blue_deep']}; }}
"""

def frame(nav, cap):
    return (f'<div class="frame">{nav}<div class="ghost">Today’s Check-In</div>'
            f'<div class="cap">{cap}</div></div>')

html = (f'<!doctype html><html><head><meta charset=utf-8><style>{STYLES}</style></head><body>'
        f'{frame(bar_tabs(), "Option A — Segmented Tabs  (clear, obvious, always-visible)")}'
        f'{frame(bar_pills(), "Option B — Floating Pills  (soft, gentle, airier)")}'
        f'{frame(bar_min(), "Option C — Minimal Icons  (quiet, low visual weight, most whitespace)")}'
        f'</body></html>')

HTML(string=html, base_url=str(C.ROOT)).write_pdf(str(C.BUILD_DIR / "nav-options.pdf"))
d = fitz.open(str(C.BUILD_DIR / "nav-options.pdf"))
# stack the 3 pages vertically into one png
scale = 1.0
pw = int(C.PAGE_W*scale); ph = int(300*scale); pad = 16
out = fitz.open(); pg = out.new_page(width=pw+2*pad, height=len(d)*ph+(len(d)+1)*pad)
pg.draw_rect(pg.rect, color=(0.9,0.9,0.9), fill=(0.9,0.9,0.9))
for i, p in enumerate(d):
    pix = p.get_pixmap(matrix=fitz.Matrix(scale, scale))
    y = pad + i*(ph+pad)
    pg.insert_image(fitz.Rect(pad, y, pad+pw, y+ph), pixmap=pix)
pg.get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(str(C.BUILD_DIR / "nav-options.png"))
print("wrote nav-options.png")
