"""
All page copy for the ADHD Digital Planner.

Text is taken verbatim from adhd-planner-text-draft.md (the source of truth).
Where the draft left placeholders — Page 2 mini-todo examples and Page 8
link/response targets — the chosen values are marked PROPOSED and are pending
sign-off; they are isolated here so they are trivial to change.

Page ids (used as hyperlink anchors):
  page-01 Mindset      page-05 High Energy Bank   page-09 Habit Tracker
  page-02 Check-In     page-06 Task Breakdown     page-10 Reward Chart
  page-03 Brain Dump   page-07 Focus Plan         page-11 Monthly Overview
  page-04 Low Energy   page-08 Why Putting Off
"""

# Ordered list of pages. Each has an id, a nav key (which tab is "active"),
# and a `kind` that build.py uses to pick the layout renderer.
PAGES = [
    {"id": "page-01", "kind": "mindset",   "nav": "mindset"},
    {"id": "page-02", "kind": "checkin",   "nav": "checkin"},
    {"id": "page-03", "kind": "braindump", "nav": "braindump"},
    {"id": "page-04", "kind": "bank_low",  "nav": "banks"},
    {"id": "page-05", "kind": "bank_high", "nav": "banks"},
    {"id": "page-06", "kind": "breakdown", "nav": "tasks"},
    {"id": "page-07", "kind": "focus",     "nav": "tasks"},
    {"id": "page-08", "kind": "putoff",    "nav": "tasks"},
    {"id": "page-09", "kind": "habit",     "nav": "tasks"},
    {"id": "page-10", "kind": "reward",    "nav": "tasks"},
    {"id": "page-11", "kind": "monthly",   "nav": "tasks"},
]

# --- Page 1 — Mindset -------------------------------------------------------
MINDSET = {
    "title": "A word for you.",
    "blocks": [
        ("p",      "Couldn't keep the promise to write every day?"),
        ("p",      "Hesitated even to open this planner again?"),
        ("strong", "That's okay."),
        ("p",      "Even beautiful flowers bloom through countless winds."),
        ("p",      "Your path will have hardships too, big and small."),
        ("p",      "What matters isn't walking perfectly —"),
        ("strong", "it's getting back up when you fall."),
        ("p",      "Heavy heart, fear, guilt today?"),
        ("p",      "That's okay too."),
        ("strong", "This planner just wants to be\na small guide that helps you rise, every time you fall."),
    ],
}

# --- Page 2 — Check-In ------------------------------------------------------
CHECKIN = {
    "back_note": "If a hard feeling catches you today, come back to page one.",
    "back_target": "page-01",
    "sleep": ["Bad", "Okay", "Good"],
    "mood": ["Happy", "Angry", "Sad", "Neutral"],
    # PROPOSED mini-todo examples (drawn from the banks below) — pending sign-off
    "low_examples": [
        "Open just 1 email (no reply needed)",
        "Put away 5 visible items",
        "Drink a glass of water",
    ],
    "high_examples": [
        "Clear out backed-up emails",
        "Fully organize one room",
        "30 min of exercise",
    ],
    "low_target": "page-04",
    "high_target": "page-05",
}

# --- Page 3 — Brain Dump ----------------------------------------------------
BRAINDUMP = {
    "categories": ["Work", "Home", "Relationships", "Other"],
    "sort_headers": ["Urgent", "Important", "Later"],
    "next_note": "Something to act on? Take it to Task Breakdown.",
    "next_target": "page-06",
}

# --- Page 4/5 — To-Do Banks -------------------------------------------------
LOW_BANK = {
    "title": "Low Energy Bank",
    "subtitle": "5 min or less, impossible to fail",
    "groups": {
        "Work": [
            "Open just 1 email (no need to reply)",
            "Jot down just 1 thing for tomorrow",
            "Check just 1 pending notification",
        ],
        "Home": [
            "Put away 5 visible items",
            "Drink a glass of water and wash the cup",
            "Just make the bed",
        ],
        "Relationships": [
            "Send one emoji to check in",
            "Read just 1 unanswered message",
        ],
        "Other": [
            "Open a window and take 3 deep breaths",
            "Listen to a favorite song",
            "Just lie down for 5 minutes (this counts too)",
        ],
    },
}

HIGH_BANK = {
    "title": "High Energy Bank",
    "subtitle": "batch mode, multiple at once",
    "groups": {
        "Work": [
            "Clear out backed-up emails",
            "Plan out next week",
            "30 min deep focus on a stalled project",
        ],
        "Home": [
            "Fully organize one room",
            "Grocery shop and plan meals for the week",
            "Catch up on laundry/dishes in one go",
        ],
        "Relationships": [
            "Reach out to someone you haven't talked to in a while",
            "Set up a meetup",
        ],
        "Other": [
            "30 min of exercise",
            "Learn or try something new",
            "Make one decision you've been putting off",
        ],
    },
}

# --- Page 6 — Task Breakdown ------------------------------------------------
BREAKDOWN = {
    "big_label": "Big task:",
    "first_label": "First, just this one:",
    "first_hint": "everything else can wait — do this one first",
    "steps": 5,
    "footer": "max 5 steps — no infinite breakdown, no progress bar",
}

# --- Page 7 — Focus Plan ----------------------------------------------------
FOCUS = {
    "distract_prompt": "What's distracting you right now? (pick up to 3)",
    "remove_prompt": "Can you remove it right now?",
    "yes": "Yes -> remove it",
    "no": "No -> that's fine, leave it for today",
    "timer": "Try 25 minutes",
    "timer_note": "no pressure — just try",
}

# --- Page 8 — Why Am I Putting This Off? ------------------------------------
# PROPOSED responses/targets for the draft's unspecified items — pending sign-off.
PUTOFF = {
    "title": "Why Am I Putting This Off?",
    "subtitle": "pick what fits — no need to solve all of it",
    "items": [
        {"text": "It feels too big",
         "response": "go to the Task Breakdown Sheet", "target": "page-06"},
        {"text": "I don't know where to start",
         "response": "just name the very first step", "target": "page-06"},
        {"text": "I'm bored",
         "response": "make it shorter, or pair it with a reward", "target": "page-10"},
        {"text": "I want to do it perfectly",
         "response": "done is kinder than perfect — aim for good enough today",
         "target": None},
        {"text": "I have no energy",
         "response": "pick one tiny thing from the Low Energy Bank", "target": "page-04"},
        {"text": "Just because",
         "response": "Rest and enjoy your time, then come back", "target": None,
         "emphasis": True},
    ],
}

# --- Page 9 — Habit Tracker -------------------------------------------------
HABIT = {
    "title": "Habit Tracker",
    "subtitle": "weekly grid, up to 3 habits at a time",
    "days": ["M", "T", "W", "T", "F", "S", "S"],
    "habit_rows": 3,
    "legend": [
        ("GOOD (did it)", "green"),
        ("It's okay (didn't)", "lavender"),
    ],
    "note": "no red marks, no X, no streak-break emphasis — blank days simply aren't shown as \"failed\"",
    "footer": "Rest counts too.",
    "sticker_note": "Habit stamps are draggable stickers — see the sticker sheet.",
}

# --- Page 10 — Reward Chart -------------------------------------------------
REWARD = {
    "title": "Finish this one thing — what will you give yourself?",
    "tiers": [
        {"label": "Small", "eg": "e.g. favorite snack, 5-min walk"},
        {"label": "Medium", "eg": "e.g. an episode of your show, coffee run"},
        {"label": "Big", "eg": "e.g. something you've wanted, a full day off"},
    ],
    "cant_think": "Can't think of one — save it for later",
    "footer": "Rewards aren't earned. They're just nice to have.",
}

# --- Page 11 — Monthly Overview ---------------------------------------------
MONTHLY = {
    "title": "This Month",
    "goals_label": "Just 3 things this month",
    "goals_note": "more than 3? save the rest for next month — no guilt",
    "calendar_label": "Mini Calendar",
    "calendar_note": "plain numbers only — write in it if you want, leave it blank if you don't",
    "note_label": "A note to myself this month:",
}
