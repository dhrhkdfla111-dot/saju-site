"""
Build the ADHD Digital Planner PDF from config + content.

    python src/build.py            # -> build/adhd-planner-light.pdf
    python src/build.py --dark     # -> build/adhd-planner-dark.pdf  (optional)

Layout is HTML/CSS rendered by WeasyPrint, which turns every
`<a href="#page-0X">` into a real internal PDF GoTo link that GoodNotes /
Notability / Xodo can follow. All visual + copy decisions live in
config.py and content.py; this file only assembles them.
"""
import argparse
from pathlib import Path

from weasyprint import HTML

import config as C
import content as T


# ---------------------------------------------------------------------------
# Active palette
# ---------------------------------------------------------------------------
# The single source of truth for colours in BOTH the CSS and every inline style /
# SVG helper. render_html() swaps this to the dark palette before rendering the
# dark file, so inline colours (table borders, battery outlines, etc.) follow the
# theme automatically instead of being baked to the light values.
DARK_OVERRIDES = {
    "bg": "#22262B", "bg_soft": "#2B3036", "ink": "#D9DEE3",
    "ink_soft": "#A6AEB6", "ink_faint": "#6C757E", "line": "#3A4046",
    "blue_bg": "#2C3A44", "green_bg": "#2E3A31", "nav_bg": "#2B3036",
    "nav_ink": "#B7C0C8",
    # softer, less-saturated accents so panels don't read as heavy blocks
    "blue": "#6E9DBE", "green": "#7FAE8B", "blue_deep": "#9CC4E0",
    "green_deep": "#96C7A2",
}


def palette(dark: bool) -> dict:
    c = dict(C.COLORS)
    if dark:
        c.update(DARK_OVERRIDES)
    return c


# module-level active palette (light by default; render_html swaps it per theme)
PAL = palette(False)


# ---------------------------------------------------------------------------
# Small inline-SVG icon set for the nav bar (stroke = currentColor)
# ---------------------------------------------------------------------------
def _svg(paths, fill=False):
    attr = 'fill="currentColor" stroke="none"' if fill else \
        'fill="none" stroke="currentColor" stroke-width="1.7" ' \
        'stroke-linecap="round" stroke-linejoin="round"'
    return (f'<svg viewBox="0 0 24 24" class="nav-icon" {attr}>{paths}</svg>')

ICONS = {
    "home":    _svg('<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/>'),
    "sun":     _svg('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2'
                    'M20 12h2M5 5l1.5 1.5M17.5 17.5L19 19M19 5l-1.5 1.5M6.5 17.5L5 19"/>'),
    "cloud":   _svg('<path d="M7 18a4 4 0 010-8 5 5 0 019.6-1.3A3.5 3.5 0 1117 18z"/>'),
    "battery": _svg('<rect x="3" y="8" width="15" height="8" rx="2"/>'
                    '<path d="M21 11v2"/>'),
    "check":   _svg('<path d="M4 12l5 5L20 6"/>'),
    "list":    _svg('<path d="M8 6h12M8 12h12M8 18h12"/><circle cx="4" cy="6" r="1.4" fill="currentColor" stroke="none"/><circle cx="4" cy="12" r="1.4" fill="currentColor" stroke="none"/><circle cx="4" cy="18" r="1.4" fill="currentColor" stroke="none"/>'),
    "target":  _svg('<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3.4"/>'),
    "help":    _svg('<circle cx="12" cy="12" r="9"/><path d="M9.2 9.2a2.8 2.8 0 015.4 1c0 1.9-2.6 2.3-2.6 4"/><circle cx="12" cy="17" r="1" fill="currentColor" stroke="none"/>'),
    "grid":    _svg('<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M9 9v11"/>'),
    "gift":    _svg('<path d="M4 11h16v9H4z"/><path d="M2 7h20v4H2zM12 7v13"/><path d="M12 7S9.5 2 7.5 4 12 7 12 7zM12 7s2.5-5 4.5-3S12 7 12 7z"/>'),
    "moon":    _svg('<path d="M20 14A8 8 0 019.5 3.5 8 8 0 1020 14z"/>'),
    "calendar": _svg('<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 9.5h18M8 3v4M16 3v4"/>'),
    "star":    _svg('<path d="M12 3.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8L3.5 9.7l5.9-.9z"/>'),
}


def battery_svg(fill: float, size: int = 44, fill_color: str | None = None) -> str:
    """Reusable battery icon. `fill` is 0.0-1.0 (empty -> full).

    The outline/frame and overall size are IDENTICAL for every fill level —
    only the inner bar width changes — so any row of these stays perfectly
    consistent automatically. Vector, not emoji (emoji batteries render
    inconsistently across PDF viewers).
    """
    fill_color = fill_color or PAL["green_deep"]
    fill = max(0.0, min(1.0, fill))
    inner_max = 12.5
    w = inner_max * fill
    bar = (f'<rect x="4.2" y="10" width="{w:.2f}" height="4" rx="1" '
           f'fill="{fill_color}" stroke="none"/>' if w > 0.1 else "")
    return (f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" style="display:block" '
            f'fill="none" stroke="{PAL["ink"]}" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round">'
            f'<rect x="2.5" y="8" width="16.5" height="8" rx="2.2"/>'
            f'<path d="M21 10.6v2.8"/>{bar}</svg>')


def energy_selector(steps: int = 5, size: int = 52) -> str:
    """The 5-step energy picker: equal-width columns so the batteries sit on one
    baseline with even spacing; only each battery's fill differs. (low)/(high)
    labels align under the first/last column."""
    cells = "".join(
        f'<div style="flex:1;display:flex;justify-content:center">'
        f'{battery_svg(i / (steps - 1), size=size)}</div>'
        for i in range(steps))
    mids = '<span style="flex:1"></span>' * (steps - 2)
    labels = (f'<span style="flex:1;text-align:center">(low)</span>{mids}'
              f'<span style="flex:1;text-align:center">(high)</span>')
    return (f'<div style="max-width:600px">'
            f'<div style="display:flex;align-items:center">{cells}</div>'
            f'<div class="small" style="display:flex;margin-top:10px">{labels}</div>'
            f'</div>')


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
def build_css(dark: bool) -> str:
    c = palette(dark)
    ty = C.TYPE
    F = C.FONTS
    return f"""
@font-face {{ font-family:Lexend; font-weight:400; src:url("file://{F['regular']}"); }}
@font-face {{ font-family:Lexend; font-weight:500; src:url("file://{F['medium']}"); }}
@font-face {{ font-family:Lexend; font-weight:600; src:url("file://{F['semibold']}"); }}
@font-face {{ font-family:Lexend; font-weight:700; src:url("file://{F['bold']}"); }}

@page {{ size:{C.PAGE_W}px {C.PAGE_H}px; margin:0; }}

* {{ box-sizing:border-box; margin:0; padding:0; }}
html {{ font-family:Lexend, Verdana, sans-serif; }}
body {{ color:{c['ink']}; }}

.page {{
  position:relative; width:{C.PAGE_W}px; height:{C.PAGE_H}px;
  background:{c['bg']}; overflow:hidden; page-break-after:always;
  font-size:{ty['base_px']}px; line-height:{ty['line_height']};
}}
.page:last-child {{ page-break-after:auto; }}
.body {{ padding:{C.MARGIN}px; padding-top:{C.MARGIN + 96}px; height:100%; }}

/* ---- nav bar (tabs style) ---- */
.nav {{
  position:absolute; top:0; left:0; right:0; height:88px;
  background:{c['nav_bg']}; display:flex; align-items:stretch;
  border-bottom:1px solid {c['line']};
}}
.nav a {{
  flex:1; display:flex; flex-direction:column; align-items:center;
  justify-content:center; gap:4px; text-decoration:none;
  color:{c['nav_ink']}; font-size:{ty['nav_px']}px; font-weight:500;
  border-right:1px solid {c['line']};
}}
.nav a:last-child {{ border-right:none; }}
.nav a.active {{ color:#fff; background:{c['nav_active']}; }}
.nav-icon {{ width:24px; height:24px; }}

/* ---- typography ---- */
h1 {{ font-size:{ty['h1_px']}px; font-weight:700; line-height:1.25; }}
h2 {{ font-size:{ty['h2_px']}px; font-weight:600; line-height:1.3; }}
h3 {{ font-size:{ty['h3_px']}px; font-weight:600; color:{c['ink']}; }}
p  {{ margin:0 0 6px; }}
.small {{ font-size:{ty['small_px']}px; color:{c['ink_soft']}; }}
.faint {{ color:{c['ink_faint']}; }}
.strong {{ font-weight:600; }}
a.link {{ color:{c['blue_deep']}; text-decoration:none; font-weight:500; }}

/* ---- reusable pieces ---- */
.panel {{ background:{c['bg_soft']}; border:1px solid {c['line']};
          border-radius:20px; padding:28px 32px; }}
.panel-blue {{ background:{c['blue_bg']}; border-color:{c['blue']}; }}
.panel-green {{ background:{c['green_bg']}; border-color:{c['green']}; }}
.row {{ display:flex; align-items:center; }}
.gap {{ gap:16px; }}
.divider {{ height:1px; background:{c['line']}; margin:26px 0; }}

.checkbox {{ width:26px; height:26px; border:2px solid {c['ink_faint']};
             border-radius:7px; display:inline-block; flex:0 0 auto; }}
.writeline {{ border-bottom:1.5px solid {c['line']}; height:0; }}

.chip {{ display:inline-flex; align-items:center; justify-content:center;
         height:46px; padding:0 24px; line-height:1; border-radius:999px;
         border:1.5px solid {c['line']}; color:{c['ink_soft']};
         font-size:{ty['small_px']}px; background:{c['bg']}; text-align:center; }}

.pill-link {{ display:inline-flex; align-items:center; gap:8px;
              padding:10px 20px; border-radius:999px;
              background:{c['blue_bg']}; color:{c['blue_deep']};
              text-decoration:none; font-weight:500; font-size:{ty['small_px']}px; }}

/* plain-text "tap for full ... Bank" links; margin-top:auto pins them to the
   bottom of their box so the pair lines up regardless of checklist wrapping.
   Colour is theme-aware (uses the active palette, not a hardcoded light value). */
.bank-link {{ display:inline-block; margin-top:auto; padding-top:16px;
              text-decoration:none; font-weight:500; font-size:{ty['small_px']}px; }}
.bank-link-blue {{ color:{c['blue_deep']}; }}
.bank-link-green {{ color:{c['green_deep']}; }}

.back-note {{ position:absolute; top:104px; right:{C.MARGIN}px;
             max-width:360px; text-align:right; font-size:{ty['small_px']}px;
             color:{c['blue_deep']}; text-decoration:none; }}

.page-label {{ position:absolute; bottom:26px; right:32px;
               font-size:13px; color:{c['ink_faint']}; }}
.page-foot {{ position:absolute; bottom:24px; left:{C.MARGIN}px;
              font-size:13px; color:{c['ink_faint']}; letter-spacing:1px; }}

/* ---- standard page header ---- */
.phead {{ display:flex; align-items:center; gap:18px; }}
.phead h1 {{ line-height:1.15; }}
.badge {{ width:62px; height:62px; border-radius:17px; flex:0 0 auto;
          display:flex; align-items:center; justify-content:center; }}
.badge .nav-icon {{ width:30px; height:30px; }}
.badge-blue {{ background:{c['blue_bg']}; color:{c['blue_deep']}; }}
.badge-green {{ background:{c['green_bg']}; color:{c['green_deep']}; }}
.accent {{ height:5px; width:84px; border-radius:3px; margin:20px 0 30px; }}
.accent-blue {{ background:{c['blue']}; }}
.accent-green {{ background:{c['green']}; }}
"""


# ---------------------------------------------------------------------------
# Nav bar
# ---------------------------------------------------------------------------
def render_nav(active_key: str) -> str:
    tabs = []
    for tab in C.NAV_TABS:
        cls = "active" if tab["key"] == active_key else ""
        icon = ICONS.get(tab["icon"], "")
        tabs.append(
            f'<a class="{cls}" href="#{tab["target"]}">{icon}'
            f'<span>{tab["label"]}</span></a>')
    return f'<nav class="nav">{"".join(tabs)}</nav>'


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def checkbox(label="", link=None, cls=""):
    inner = f'<span class="checkbox"></span>'
    text = ""
    if label:
        if link:
            text = f'&nbsp;&nbsp;<a class="link" href="#{link}">{label}</a>'
        else:
            text = f'&nbsp;&nbsp;{label}'
    return f'<div class="row gap {cls}" style="margin:12px 0">{inner}<span>{text}</span></div>'


def writelines(n, width="100%", gap=54):
    return "".join(
        f'<div class="writeline" style="width:{width};margin-top:{gap}px"></div>'
        for _ in range(n))


def escape_hatch(compact=False):
    """A gentle 'none of these fit' opt-out for the To-Do banks — a blank
    write-in line + a quiet reassurance, matching the guilt-free tone used on the
    Reward Chart / procrastination pages. `compact` = the tight Page-2 mini boxes
    (smaller type, 2 short lines); otherwise = the roomier full bank pages."""
    fs = "font-size:15px;" if compact else ""
    top = "10px" if compact else "20px"
    write = (f'<div class="row gap" style="margin-top:{top}"><span class="checkbox"></span>'
             f'<span style="{fs}white-space:nowrap">Or write your own:</span>'
             f'<span class="writeline" style="flex:1;margin-left:10px"></span></div>')
    opt = (f'<div class="faint" style="{fs or "font-size:16px;"}margin-top:8px">'
           f'None of these feel right? <span class="strong">That&rsquo;s okay too.</span></div>')
    return write + opt


def page_header(title, icon_key, subtitle=None, tint="blue", size=None):
    """Standard page title block: soft icon badge + title (+ subtitle) + accent bar.
    Gives every content page a consistent, 'designed' identity tied to its section."""
    icon = ICONS.get(icon_key, "")
    sub = f'<p class="small" style="margin-top:2px">{subtitle}</p>' if subtitle else ""
    style = f' style="font-size:{size}px"' if size else ""
    return (f'<div class="phead"><div class="badge badge-{tint}">{icon}</div>'
            f'<div><h1{style}>{title}</h1>{sub}</div></div>'
            f'<div class="accent accent-{tint}"></div>')


# ---------------------------------------------------------------------------
# Page renderers
# ---------------------------------------------------------------------------
def page_mindset(_):
    m = T.MINDSET
    blocks = []
    for kind, text in m["blocks"]:
        html = text.replace("\n", "<br>")
        if kind == "strong":
            blocks.append(f'<p class="strong" style="font-size:26px;margin:22px 0">{html}</p>')
        else:
            blocks.append(f'<p style="margin:14px 0;color:{PAL["ink_soft"]}">{html}</p>')
    return f"""
      <div class="body" style="display:flex;flex-direction:column;
           text-align:center;padding-left:120px;padding-right:120px;padding-top:96px">
        <div style="margin-bottom:56px">
          <div style="font-size:56px;font-weight:700;color:{PAL['blue_deep']};
               letter-spacing:0.5px">{C.PLANNER_TITLE}</div>
          <div class="small" style="margin-top:10px;letter-spacing:2px;
               text-transform:uppercase">{C.PLANNER_TAGLINE}</div>
          <div style="width:120px;height:3px;background:{PAL['green']};
               border-radius:2px;margin:26px auto 0"></div>
        </div>
        <div style="flex:1;display:flex;flex-direction:column;justify-content:center">
          <h1 style="margin-bottom:36px">{m['title']}</h1>
          {''.join(blocks)}
        </div>
      </div>"""


def page_checkin(_):
    ck = T.CHECKIN
    sleep = "".join(f'<span class="chip" style="margin-right:14px">{s}</span>'
                    for s in ck["sleep"])
    mood = "".join(f'<span class="chip" style="margin-right:14px">{m}</span>'
                   for m in ck["mood"])
    # Energy: reusable 5-step selector (one baseline, even spacing, identical frames)
    energy = energy_selector(5, size=52)
    # Box headers: the SAME battery component as a matched pair — 1 empty / 1 full.
    low_batt = battery_svg(0.0, size=28)
    high_batt = battery_svg(1.0, size=28)
    low = "".join(checkbox(x) for x in ck["low_examples"])
    high = "".join(checkbox(x) for x in ck["high_examples"])
    return f"""
      <a class="back-note" href="#{ck['back_target']}">&#8627; {ck['back_note']}</a>
      <div class="body">
        {page_header("Today's Check-In", "sun", tint="blue")}
        <h3>Sleep</h3>
        <div class="row" style="margin:14px 0 26px">{sleep}</div>
        <h3>Energy</h3>
        <div style="margin:16px 0 8px">{energy}</div>
        <h3 style="margin-top:26px">Mood <span class="small">(circle one)</span></h3>
        <div class="row" style="margin:14px 0">{mood}</div>
        <div class="divider"></div>
        <div class="row gap" style="align-items:stretch;gap:24px">
          <div class="panel panel-blue" style="flex:1;display:flex;flex-direction:column">
            <div class="row" style="justify-content:space-between;align-items:baseline">
              <h3 style="white-space:nowrap"><span style="display:inline-flex;
                align-items:center;gap:8px">{low_batt} Low Energy</span></h3>
              <span class="small">pick one</span>
            </div>
            {low}
            {escape_hatch(compact=True)}
            <a class="bank-link bank-link-blue" href="#{ck['low_target']}">
              tap for full Low Energy Bank &#8594;</a>
          </div>
          <div class="panel panel-green" style="flex:1;display:flex;flex-direction:column">
            <div class="row" style="justify-content:space-between;align-items:baseline">
              <h3 style="white-space:nowrap"><span style="display:inline-flex;
                align-items:center;gap:8px">{high_batt} High Energy</span></h3>
              <span class="small">pick one</span>
            </div>
            {high}
            {escape_hatch(compact=True)}
            <a class="bank-link bank-link-green" href="#{ck['high_target']}">
              tap for full High Energy Bank &#8594;</a>
          </div>
        </div>
      </div>"""


def page_braindump(_):
    bd = T.BRAINDUMP
    cats = " &middot; ".join(bd["categories"])
    heads = "".join(f'<th style="padding:16px;text-align:left;font-weight:600;'
                    f'border:1px solid {PAL["line"]}">{h}</th>'
                    for h in bd["sort_headers"])
    cells = "".join(f'<td style="height:220px;border:1px solid {PAL["line"]};'
                    'vertical-align:top"></td>' for _ in bd["sort_headers"])
    return f"""
      <div class="body">
        {page_header("Brain Dump", "cloud", tint="blue")}
        <p class="faint" style="margin-top:-14px">{cats}
          <span class="small">&nbsp;— faint hints, free writing still welcome</span></p>
        <div class="panel" style="height:520px;margin:22px 0">
          <span class="faint small">everything on your mind — just get it out</span>
        </div>
        <h3>Sort it <span class="small">(optional, no pressure to sort everything)</span></h3>
        <table style="width:100%;border-collapse:collapse;margin-top:14px">
          <tr>{heads}</tr><tr>{cells}</tr>
        </table>
        <a class="pill-link" href="#{bd['next_target']}" style="margin-top:26px">
          {bd['next_note']} &#8594;</a>
      </div>"""


def _bank(bank, tint):
    cols = []
    for group, items in bank["groups"].items():
        lis = "".join(f'<div class="row gap" style="margin:10px 0">'
                      f'<span class="checkbox"></span><span>{i}</span></div>'
                      for i in items)
        cols.append(f'<div class="panel panel-{tint}" style="margin-bottom:22px">'
                    f'<h3 style="margin-bottom:8px">{group}</h3>{lis}</div>')
    half1 = "".join(cols[:2])
    half2 = "".join(cols[2:])
    return f"""
      <div class="body">
        {page_header(bank['title'], "battery", subtitle=bank['subtitle'], tint=tint)}
        <div class="row" style="align-items:flex-start;gap:24px">
          <div style="flex:1">{half1}</div>
          <div style="flex:1">{half2}</div>
        </div>
        <div style="max-width:760px;margin-top:4px">{escape_hatch(compact=False)}</div>
      </div>"""


def page_bank_low(_):
    return _bank(T.LOW_BANK, "blue")


def page_bank_high(_):
    return _bank(T.HIGH_BANK, "green")


def page_breakdown(_):
    b = T.BREAKDOWN
    steps = "".join(
        f'<div class="row gap" style="margin:20px 0"><span class="checkbox"></span>'
        f'<span class="faint">Step {i+1}</span>'
        f'<span class="writeline" style="flex:1;margin-left:12px"></span></div>'
        for i in range(b["steps"]))
    return f"""
      <div class="body">
        {page_header("Task Breakdown Sheet", "list", tint="green")}
        <h3>{b['big_label']}</h3>
        <div class="writeline" style="margin:18px 0 34px"></div>
        <div class="panel panel-green">
          <h3>&#8594; {b['first_label']}</h3>
          <div class="writeline" style="margin-top:22px;border-color:{PAL['green_deep']}"></div>
          <p class="small" style="margin-top:14px">({b['first_hint']})</p>
        </div>
        <div style="margin-top:30px">{steps}</div>
        <p class="small faint" style="margin-top:20px">({b['footer']})</p>
      </div>"""


def page_focus(_):
    f = T.FOCUS
    slots = "".join(
        f'<div class="row gap" style="margin:18px 0"><span class="faint">{i+1}.</span>'
        f'<span class="writeline" style="flex:1"></span></div>' for i in range(3))
    return f"""
      <div class="body">
        {page_header("Focus Plan", "target", tint="blue")}
        <h3>{f['distract_prompt']}</h3>
        <div style="margin:20px 0 34px">{slots}</div>
        <h3>{f['remove_prompt']}</h3>
        {checkbox(f['yes'])}{checkbox(f['no'])}
        <div class="panel panel-blue" style="margin-top:34px;text-align:center">
          <h2>&#9201; {f['timer']}</h2>
          <p class="small" style="margin-top:8px">({f['timer_note']})</p>
        </div>
      </div>"""


def page_putoff(_):
    p = T.PUTOFF
    rows = []
    for it in p["items"]:
        arrow = f'&#8594; {it["response"]}'
        if it.get("target"):
            resp = f'<a class="link" href="#{it["target"]}">{arrow}</a>'
        else:
            resp = f'<span class="small">{arrow}</span>'
        strong = ' class="strong"' if it.get("emphasis") else ''
        rows.append(
            f'<div class="row gap" style="margin:16px 0;align-items:flex-start">'
            f'<span class="checkbox"></span>'
            f'<span><span{strong}>{it["text"]}</span> &nbsp;{resp}</span></div>')
    return f"""
      <div class="body">
        {page_header(p['title'], "help", subtitle=p['subtitle'], tint="blue")}
        {''.join(rows)}
      </div>"""


def page_habit(_):
    h = T.HABIT
    day_head = "".join(f'<th style="padding:14px;font-weight:600">{d}</th>' for d in h["days"])
    rows = ""
    for _ in range(h["habit_rows"]):
        cells = "".join(f'<td style="border:1px solid {PAL["line"]};height:96px"></td>'
                        for _ in h["days"])
        rows += (f'<tr><td style="border:1px solid {PAL["line"]};width:220px;'
                 'height:96px"></td>' + cells + '</tr>')
    legend = "".join(
        f'<div class="row gap" style="margin-right:36px">'
        f'<span style="width:30px;height:30px;border-radius:50%;'
        f'background:{PAL[color]}"></span><span>{label}</span></div>'
        for label, color in h["legend"])
    return f"""
      <div class="body">
        {page_header(h['title'], "grid", subtitle=h['subtitle'], tint="green")}
        <table style="width:100%;border-collapse:collapse;text-align:center">
          <tr><th style="padding:14px">Habit</th>{day_head}</tr>{rows}
        </table>
        <div class="row" style="margin-top:30px">{legend}</div>
        <p class="small faint" style="margin-top:14px">({h['note']})</p>
        <p class="small" style="margin-top:8px">{h['sticker_note']}</p>
        <div class="panel panel-green" style="margin-top:26px;text-align:center">
          <h3>{h['footer']}</h3>
        </div>
      </div>"""


def page_reward(_):
    r = T.REWARD
    tiers = ""
    for t in r["tiers"]:
        tiers += f"""
          <div class="panel" style="margin-bottom:22px">
            <div class="row" style="justify-content:space-between;align-items:baseline">
              <h3>{t['label']}</h3><span class="small faint">{t['eg']}</span>
            </div>
            <div class="writeline" style="margin:18px 0 14px"></div>
            {checkbox(r['cant_think'])}
          </div>"""
    return f"""
      <div class="body">
        {page_header(r['title'], "star", tint="green", size=32)}
        {tiers}
        <div class="panel panel-blue" style="text-align:center;margin-top:8px">
          <h3>{r['footer']}</h3>
        </div>
      </div>"""


def page_monthly(_):
    m = T.MONTHLY
    goals = "".join(
        f'<div class="row gap" style="margin:16px 0"><span class="faint">{i+1}.</span>'
        f'<span class="writeline" style="flex:1"></span></div>' for i in range(3))
    # plain mini calendar 7x5
    cal = ""
    day = 1
    for _ in range(5):
        cells = ""
        for _ in range(7):
            cells += (f'<td style="border:1px solid {PAL["line"]};height:104px;'
                      'vertical-align:top;padding:8px" class="small faint">'
                      f'{day if day <= 31 else ""}</td>')
            day += 1
        cal += f"<tr>{cells}</tr>"
    return f"""
      <div class="body">
        {page_header(m['title'], "calendar", tint="blue")}
        <h3>{m['goals_label']}</h3>
        <div style="margin:16px 0 8px">{goals}</div>
        <p class="small faint">({m['goals_note']})</p>
        <h3 style="margin-top:26px">{m['calendar_label']}
          <span class="small">— {m['calendar_note']}</span></h3>
        <table style="width:100%;border-collapse:collapse;margin-top:14px">{cal}</table>
        <h3 style="margin-top:26px">{m['note_label']}</h3>
        {writelines(2, gap=48)}
      </div>"""


RENDERERS = {
    "mindset": page_mindset, "checkin": page_checkin, "braindump": page_braindump,
    "bank_low": page_bank_low, "bank_high": page_bank_high, "breakdown": page_breakdown,
    "focus": page_focus, "putoff": page_putoff, "habit": page_habit,
    "reward": page_reward, "monthly": page_monthly,
}


# ---------------------------------------------------------------------------
# Assemble
# ---------------------------------------------------------------------------
def render_html(dark: bool) -> str:
    global PAL
    PAL = palette(dark)   # inline styles & SVG helpers read this; must match theme
    pages = []
    for pg in T.PAGES:
        body = RENDERERS[pg["kind"]](pg)
        is_cover = pg["kind"] == "mindset"
        nav = "" if is_cover else render_nav(pg["nav"])
        num = pg["id"].replace("page-0", "").replace("page-", "")
        label = f'<div class="page-label">{num}</div>'
        foot = "" if is_cover else f'<div class="page-foot">{C.PLANNER_TITLE.upper()}</div>'
        pages.append(f'<section class="page" id="{pg["id"]}">{nav}{body}{foot}{label}</section>')
    css = build_css(dark)
    return (f'<!doctype html><html><head><meta charset="utf-8">'
            f'<style>{css}</style></head><body>{"".join(pages)}</body></html>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dark", action="store_true")
    args = ap.parse_args()
    dark = args.dark or C.DARK_MODE
    html = render_html(dark)
    C.BUILD_DIR.mkdir(exist_ok=True)
    name = "adhd-planner-dark.pdf" if dark else "adhd-planner-light.pdf"
    out = C.BUILD_DIR / name
    HTML(string=html, base_url=str(C.ROOT)).write_pdf(str(out))
    print(f"wrote {out}  ({out.stat().st_size//1024} KB)")


if __name__ == "__main__":
    main()
