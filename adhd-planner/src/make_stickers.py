"""
Generate draggable digital sticker assets (transparent PNG) for GoodNotes /
Notability — the GOOD / It's okay habit stamps from Page 9.

Rendered via WeasyPrint (so Lexend embeds/rasterizes correctly) to a
transparent-background PDF, then rasterized with alpha by PyMuPDF.

Outputs (assets/stickers/):
  good-stamp.png   green labeled stamp   ("GOOD" + check)
  okay-stamp.png   lavender labeled stamp ("it's okay" + heart)
  good-dot.png     small solid green circle   (fits tracker cells)
  okay-dot.png     small solid lavender circle
  sticker-sheet.png / .pdf   all stamps on one sheet (lasso-copy in-app)
"""
import fitz
from weasyprint import HTML
import config as C

CW = C.COLORS
OUT = C.ASSET_DIR / "stickers"
OUT.mkdir(parents=True, exist_ok=True)

GREEN = "#7CB98A"      # GOOD  (did it)
LAV = "#B9B6E4"        # It's okay (didn't)

FONT_FACE = f"""
@font-face {{ font-family:Lexend; font-weight:600; src:url("file://{C.FONTS['semibold']}"); }}
@font-face {{ font-family:Lexend; font-weight:700; src:url("file://{C.FONTS['bold']}"); }}
* {{ margin:0; padding:0; box-sizing:border-box; font-family:Lexend; }}
"""

CHECK = ('<svg viewBox="0 0 24 24" width="{s}" height="{s}" fill="none" '
         'stroke="#ffffff" stroke-width="3.2" stroke-linecap="round" '
         'stroke-linejoin="round"><path d="M4 12l5 5L20 6"/></svg>')
HEART = ('<svg viewBox="0 0 24 24" width="{s}" height="{s}" fill="{c}" '
         'stroke="none"><path d="M12 21s-7-4.6-9.3-9C1 8.5 2.6 5 6 5c2 0 3.2 1.2 '
         '4 2.3C10.8 6.2 12 5 14 5c3.4 0 5 3.5 3.3 7C19 16.4 12 21 12 21z"/></svg>')


def stamp_html(size, fill, label, glyph, label_color, fs):
    """A round stamp: filled circle + soft inner ring + glyph + label."""
    return f"""<!doctype html><html><head><meta charset=utf-8><style>{FONT_FACE}
      @page {{ size:{size}px {size}px; margin:0; }}
      .wrap {{ width:{size}px; height:{size}px; display:flex; }}
      .circle {{ width:{size-40}px; height:{size-40}px; margin:auto;
        border-radius:50%; background:{fill};
        display:flex; flex-direction:column; align-items:center;
        justify-content:center; gap:{int(size*0.02)}px;
        box-shadow:0 10px 26px rgba(60,74,84,0.22);
        border:{max(4,int(size*0.018))}px solid rgba(255,255,255,0.55); }}
      .label {{ color:{label_color}; font-weight:700;
        font-size:{fs}px; letter-spacing:0.5px; }}
    </style></head><body><div class="wrap"><div class="circle">
      {glyph}<div class="label">{label}</div>
    </div></div></body></html>"""


def dot_html(size, fill):
    return f"""<!doctype html><html><head><meta charset=utf-8><style>{FONT_FACE}
      @page {{ size:{size}px {size}px; margin:0; }}
      .wrap {{ width:{size}px; height:{size}px; display:flex; }}
      .circle {{ width:{size-24}px; height:{size-24}px; margin:auto; border-radius:50%;
        background:{fill}; box-shadow:0 6px 16px rgba(60,74,84,0.20);
        border:{max(3,int(size*0.03))}px solid rgba(255,255,255,0.6); }}
    </style></head><body><div class="wrap"><div class="circle"></div></div></body></html>"""


def render_png(html, out, size, scale=2.0):
    pdf = OUT / (out.stem + ".pdf")
    HTML(string=html, base_url=str(C.ROOT)).write_pdf(str(pdf))
    d = fitz.open(str(pdf))
    pix = d[0].get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=True)
    pix.save(str(out))
    pdf.unlink()
    print(f"  {out.name}  ({pix.width}x{pix.height})")


print("stickers ->", OUT)
render_png(stamp_html(560, GREEN, "GOOD", CHECK.format(s=118), "#ffffff", 84),
           OUT / "good-stamp.png", 560)
render_png(stamp_html(560, LAV, "it&rsquo;s okay", HEART.format(s=104, c="#ffffff"),
                      "#4A4770", 66), OUT / "okay-stamp.png", 560)
render_png(dot_html(240, GREEN), OUT / "good-dot.png", 240)
render_png(dot_html(240, LAV), OUT / "okay-dot.png", 240)


# --- sticker sheet (all stamps, for in-app lasso copy) ----------------------
def cell(fill, label, glyph, lc, fs):
    return f"""<div class="cell"><div class="circle" style="background:{fill};
        border:5px solid rgba(255,255,255,0.55)">{glyph}
        <div class="label" style="color:{lc};font-size:{fs}px">{label}</div></div></div>"""

sheet = f"""<!doctype html><html><head><meta charset=utf-8><style>{FONT_FACE}
  @page {{ size:{C.PAGE_W}px {C.PAGE_H}px; margin:0; }}
  body {{ background:{CW['bg']}; }}
  .head {{ padding:80px 80px 0; }}
  h1 {{ font-size:44px; font-weight:700; color:{CW['ink']}; }}
  .sub {{ font-size:20px; color:{CW['ink_soft']}; margin-top:10px; line-height:1.5; }}
  .grid {{ display:flex; flex-wrap:wrap; gap:60px; padding:70px 90px; justify-content:center; }}
  .cell {{ width:300px; height:300px; display:flex; }}
  .circle {{ width:260px; height:260px; margin:auto; border-radius:50%;
    display:flex; flex-direction:column; align-items:center; justify-content:center;
    gap:8px; box-shadow:0 10px 26px rgba(60,74,84,0.22); }}
  .label {{ font-weight:700; letter-spacing:0.5px; white-space:nowrap; }}
  .dotrow {{ display:flex; gap:70px; justify-content:center; align-items:center; padding:10px; }}
  .dot {{ width:120px; height:120px; border-radius:50%; box-shadow:0 6px 16px rgba(60,74,84,0.2);
    border:4px solid rgba(255,255,255,0.6); }}
  .foot {{ text-align:center; color:{CW['ink_soft']}; font-size:18px; margin-top:26px; }}
</style></head><body>
  <div class="head"><h1>Habit Stamps</h1>
    <div class="sub">Drag a stamp onto your Habit Tracker. Two feelings, both fine —
      no red marks, no streak-shaming.<br>Best used as the separate PNG files;
      you can also lasso-copy straight from this sheet.</div></div>
  <div class="grid">
    {cell(GREEN, "GOOD", CHECK.format(s=64), "#ffffff", 40)}
    {cell(LAV, "it&rsquo;s okay", HEART.format(s=56, c="#ffffff"), "#4A4770", 31)}
  </div>
  <div class="dotrow">
    <div class="dot" style="background:{GREEN}"></div>
    <div class="dot" style="background:{LAV}"></div>
  </div>
  <div class="foot">GOOD (did it) &nbsp;&middot;&nbsp; it&rsquo;s okay (didn&rsquo;t) &nbsp;&middot;&nbsp; Rest counts too.</div>
</body></html>"""

sheet_pdf = OUT / "sticker-sheet.pdf"
HTML(string=sheet, base_url=str(C.ROOT)).write_pdf(str(sheet_pdf))
fitz.open(str(sheet_pdf))[0].get_pixmap(matrix=fitz.Matrix(1.4, 1.4)).save(str(OUT / "sticker-sheet.png"))
print(f"  sticker-sheet.pdf / .png")
