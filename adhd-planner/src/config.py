"""
Design tokens & build configuration for the ADHD Digital Planner.

Everything visual and structural that you might want to tweak later lives here,
so edits ("make the green softer", "bump the font size", "swap the nav style")
never require touching the layout logic in build.py.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "fonts"
ASSET_DIR = ROOT / "assets"
BUILD_DIR = ROOT / "build"

# ---------------------------------------------------------------------------
# Page geometry
# ---------------------------------------------------------------------------
# iPad Pro 12.9" portrait point size — a clean, common canvas for GoodNotes /
# Notability planners. Links map neatly onto full-screen taps at this size.
PAGE_W = 1024          # px @ 96dpi
PAGE_H = 1366          # px @ 96dpi
MARGIN = 64            # outer content margin

# ---------------------------------------------------------------------------
# Color palette  (Visual Design Spec — pastel / light)
# ---------------------------------------------------------------------------
COLORS = {
    # base
    "bg":            "#FBF7EF",   # cream / off-white
    "bg_soft":       "#F4EEE1",   # slightly deeper cream for panels
    "ink":           "#3E4A54",   # soft charcoal (never pure black)
    "ink_soft":      "#6B7680",   # muted secondary text
    "ink_faint":     "#A7AEB4",   # hints / placeholders
    "line":          "#E4DCCB",   # hairline dividers on cream

    # accents
    "blue":          "#8FB8D6",   # soft blue  ("It's okay")
    "blue_deep":     "#5E8FB3",   # readable blue for links/labels
    "blue_bg":       "#E7F0F6",   # blue tint panel
    "green":         "#9CCBA6",   # soft green ("GOOD")
    "green_deep":    "#5FA06E",   # readable green
    "green_bg":      "#E8F3EA",   # green tint panel
    "lavender":      "#C3C1E6",   # light blue-lavender (habit "It's okay" stamp)

    # nav
    "nav_bg":        "#F1EADD",
    "nav_active":    "#8FB8D6",
    "nav_ink":       "#5B6670",
}

# ---------------------------------------------------------------------------
# Typography
# ---------------------------------------------------------------------------
FONTS = {
    "family": "Lexend",
    "regular": FONT_DIR / "Lexend-400.ttf",
    "medium":  FONT_DIR / "Lexend-500.ttf",
    "semibold": FONT_DIR / "Lexend-600.ttf",
    "bold":    FONT_DIR / "Lexend-700.ttf",
}

TYPE = {
    "base_px":     20,     # >= 14-16pt spec; 20px reads comfortably at this canvas
    "line_height": 1.5,    # 1.5x spacing per spec
    "h1_px":       46,
    "h2_px":       30,
    "h3_px":       23,
    "small_px":    16,
    "nav_px":      15,
}

# ---------------------------------------------------------------------------
# Navigation bar
# ---------------------------------------------------------------------------
# Tabs shown on every page. `target` is the page id the tab jumps to.
# "Tasks" points at the Task Breakdown sheet as the entry to the task tools.
NAV_TABS = [
    {"key": "mindset",   "label": "Home",       "icon": "home",   "target": "page-01"},
    {"key": "checkin",   "label": "Check-In",   "icon": "sun",    "target": "page-02"},
    {"key": "braindump", "label": "Brain Dump", "icon": "cloud",  "target": "page-03"},
    {"key": "banks",     "label": "To-Do",      "icon": "battery","target": "page-04"},
    {"key": "tasks",     "label": "Tasks",      "icon": "check",  "target": "page-06"},
]

# Which nav style to render: "tabs" | "pills" | "sidebar"
# (Options are previewed for sign-off before the full build is finalized.)
NAV_STYLE = "tabs"

# ---------------------------------------------------------------------------
# Build metadata
# ---------------------------------------------------------------------------
TITLE = "The Gentle Planner — ADHD Digital Planner"
DARK_MODE = False   # primary build is light; dark is a separate optional file
