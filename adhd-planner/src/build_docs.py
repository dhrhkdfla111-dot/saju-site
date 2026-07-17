"""
Render a branded, in-app 'Start Here' quick-start PDF that matches the planner's
look. This is the pretty version buyers open on their iPad; README.md is the
full text reference. Content is kept in sync with dist/README.md.
"""
import fitz
from weasyprint import HTML
import config as C

CW = C.COLORS
F = C.FONTS

CSS = f"""
@font-face {{ font-family:Lexend; font-weight:400; src:url("file://{F['regular']}"); }}
@font-face {{ font-family:Lexend; font-weight:500; src:url("file://{F['medium']}"); }}
@font-face {{ font-family:Lexend; font-weight:600; src:url("file://{F['semibold']}"); }}
@font-face {{ font-family:Lexend; font-weight:700; src:url("file://{F['bold']}"); }}
@page {{ size:{C.PAGE_W}px {C.PAGE_H}px; margin:0; }}
* {{ margin:0; padding:0; box-sizing:border-box; font-family:Lexend; }}
.page {{ width:{C.PAGE_W}px; height:{C.PAGE_H}px; background:{CW['bg']};
  padding:80px 88px; color:{CW['ink']}; font-size:19px; line-height:1.5;
  page-break-after:always; position:relative; }}
.page:last-child {{ page-break-after:auto; }}
h1 {{ font-size:44px; font-weight:700; color:{CW['blue_deep']}; }}
.tag {{ font-size:16px; letter-spacing:2px; text-transform:uppercase;
  color:{CW['ink_soft']}; margin-top:8px; }}
.accent {{ height:5px; width:84px; border-radius:3px; background:{CW['green']}; margin:20px 0 30px; }}
h2 {{ font-size:24px; font-weight:600; margin:26px 0 12px;
  display:flex; align-items:center; gap:12px; }}
h2 .dot {{ width:14px; height:14px; border-radius:50%; background:{CW['blue']}; flex:0 0 auto; }}
p {{ margin:0 0 10px; }}
.small {{ font-size:16px; color:{CW['ink_soft']}; }}
ol, ul {{ margin:6px 0 12px 26px; }}
li {{ margin:7px 0; }}
.panel {{ background:{CW['bg_soft']}; border:1px solid {CW['line']};
  border-radius:18px; padding:22px 26px; margin:14px 0; }}
.panel-blue {{ background:{CW['blue_bg']}; border-color:{CW['blue']}; }}
.panel-green {{ background:{CW['green_bg']}; border-color:{CW['green']}; }}
strong {{ font-weight:600; }}
.q {{ font-weight:600; margin-top:16px; }}
.foot {{ position:absolute; bottom:30px; left:88px; right:88px;
  font-size:14px; color:{CW['ink_faint']}; letter-spacing:1px;
  display:flex; justify-content:space-between; }}
table {{ width:100%; border-collapse:collapse; margin:12px 0; font-size:16px; }}
td, th {{ border:1px solid {CW['line']}; padding:10px 14px; text-align:left; }}
th {{ font-weight:600; background:{CW['bg_soft']}; }}
"""

PAGE1 = f"""
<div class="page">
  <h1>Start Here</h1>
  <div class="tag">ADHD Reset Planner — a gentle, guilt-free planner</div>
  <div class="accent"></div>

  <p>Working hyperlinks, energy-based task suggestions, and draggable habit
  stamps — with <strong>no streaks, no red X, no guilt</strong>. Use it on the
  days you can. Rest counts too.</p>

  <h2><span class="dot"></span>60-second setup</h2>
  <ol>
    <li><strong>Unzip</strong> this folder on your iPad (Files app → tap the .zip).</li>
    <li>Open <strong>GoodNotes</strong> (or Notability / Xodo).</li>
    <li><strong>Import</strong> the planner PDF as a <strong>document</strong> (not "as image").</li>
    <li>Tap the <strong>top navigation bar</strong> — it should jump between pages.
      That means everything works.</li>
  </ol>
  <div class="panel panel-blue small">Pick <strong>one</strong> planner file —
    <strong>Light</strong> (recommended) or <strong>Dark</strong>. You don't need both.</div>

  <h2><span class="dot"></span>How to navigate</h2>
  <ul>
    <li><strong>Top nav bar</strong> (every page): Home · Check-In · Brain Dump ·
      To-Do · Tasks. Tap to jump from anywhere.</li>
    <li><strong>Energy → tasks:</strong> on Check-In, tap "full Low / High Energy
      Bank" to get tasks that match today's energy.</li>
    <li><strong>Gentle loop:</strong> the note on Check-In links back to the
      Mindset page for the hard days.</li>
  </ul>

  <h2><span class="dot"></span>Habit stamps</h2>
  <p class="small">Drag <strong>good-stamp.png</strong> / <strong>okay-stamp.png</strong>
  from Files onto a tracker cell, or lasso-copy from <strong>sticker-sheet.pdf</strong>.
  GOOD (green) = did it. it's okay (lavender) = didn't, and that's fine.</p>

  <div class="foot"><span>ADHD RESET PLANNER</span><span>1 / 2</span></div>
</div>
"""

PAGE2 = f"""
<div class="page">
  <h1>Tips & FAQ</h1>
  <div class="accent"></div>

  <h2><span class="dot"></span>Reusing pages (daily/weekly)</h2>
  <p class="small">This is a one-of-each template set. To reuse a page,
  <strong>duplicate</strong> it in your app:</p>
  <ul class="small">
    <li><strong>GoodNotes:</strong> thumbnail grid (top-left) → ⋯ on a page → Duplicate Page.</li>
    <li><strong>Notability:</strong> page thumbnails → ⋯ / long-press → Duplicate.</li>
    <li><strong>Xodo:</strong> page thumbnail panel → long-press → Duplicate.</li>
  </ul>

  <h2><span class="dot"></span>Links won't jump? Try this</h2>
  <div class="panel panel-green small">
    <ol style="margin-left:22px">
      <li><strong>Import as a document, not an image</strong> ("as image" flattens links).</li>
      <li><strong>Update your app</strong> (Notability needs v11+ for internal links).</li>
      <li><strong>Turn off the pen/eraser first</strong> — switch to the Hand/Pointer
        tool, then tap the link.</li>
      <li><strong>Tap right on the tab/label</strong> — zoom in a little and tap it directly.</li>
      <li><strong>Don't "flatten" or "print to PDF"</strong> — it can strip the links.</li>
    </ol>
  </div>

  <h2><span class="dot"></span>Compatibility</h2>
  <table>
    <tr><th>App</th><th>Hyperlinks</th><th>Stickers</th></tr>
    <tr><td>GoodNotes 5 / 6</td><td>✓ Yes</td><td>✓ Drag PNG or lasso-copy</td></tr>
    <tr><td>Notability (v11+)</td><td>✓ Yes</td><td>✓ Lasso-copy from sheet</td></tr>
    <tr><td>Xodo (view mode)</td><td>✓ Yes</td><td>✓ Lasso-copy from sheet</td></tr>
  </table>
  <p class="small">Any PDF app with internal-link support works — the links are
  standard PDF "go-to page" links, nothing proprietary.</p>

  <div class="panel panel-blue">
    <p class="q" style="margin-top:0">A note on using this</p>
    <p class="small">You don't have to use every page, every day. Skip what
    doesn't help. This is a small guide for getting back up — not another thing
    to be perfect at. <strong>Rest counts too.</strong></p>
  </div>
  <p class="small" style="margin-top:14px">Personal-use digital download —
  please don't resell or redistribute. Thank you for supporting a tiny shop. 🌿</p>

  <div class="foot"><span>ADHD RESET PLANNER</span><span>2 / 2</span></div>
</div>
"""

html = f'<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>{PAGE1}{PAGE2}</body></html>'
out = C.ROOT / "dist" / "Start-Here.pdf"
out.parent.mkdir(exist_ok=True)
HTML(string=html, base_url=str(C.ROOT)).write_pdf(str(out))
# preview
d = fitz.open(str(out))
for i, p in enumerate(d):
    p.get_pixmap(matrix=fitz.Matrix(0.7, 0.7)).save(str(C.BUILD_DIR / f"preview/startguide-{i+1}.png"))
print(f"wrote {out}")
