"""
Resolve every internal link in the built PDF to (source page -> target page)
and label it with the text sitting under the link rectangle.

This confirms the link *structure* GoodNotes / Notability / Xodo actually read:
standard PDF GoTo actions to named destinations. It is not a substitute for a
physical on-device tap test, but it verifies exactly what those apps consume.
"""
import sys
import fitz

PDF = sys.argv[1] if len(sys.argv) > 1 else "build/adhd-planner-light.pdf"
doc = fitz.open(PDF)

PAGE_NAMES = {
    0: "Mindset", 1: "Check-In", 2: "Brain Dump", 3: "Low Energy Bank",
    4: "High Energy Bank", 5: "Task Breakdown", 6: "Focus Plan",
    7: "Why Putting Off", 8: "Habit Tracker", 9: "Reward Chart", 10: "Monthly",
}


def label_for(page, rect):
    r = fitz.Rect(rect)
    txt = page.get_textbox(r).strip().replace("\n", " ")
    if not txt:  # icon-only area — widen a little to catch the label under it
        txt = page.get_textbox(fitz.Rect(r.x0 - 6, r.y0 - 4, r.x1 + 6, r.y1 + 22)).strip()
    return " ".join(txt.split())[:42] or "(icon)"


# Dedup: nav links produce several rects per tab; collapse by (label, target).
print(f"PDF: {PDF}  ({doc.page_count} pages)\n")
ok = bad = 0
for i, page in enumerate(doc):
    links = [l for l in page.get_links()
             if l["kind"] in (fitz.LINK_GOTO, fitz.LINK_NAMED) and l.get("page", -1) >= 0]
    seen = {}
    for l in links:
        tgt = l["page"]
        lbl = label_for(page, l["from"])
        key = (lbl, tgt)
        seen[key] = seen.get(key, 0) + 1
    if not seen:
        print(f"p{i+1:02d} {PAGE_NAMES[i]:<18} — no links (entry page)")
        continue
    print(f"p{i+1:02d} {PAGE_NAMES[i]}")
    for (lbl, tgt), n in seen.items():
        arrow = "OK " if 0 <= tgt < doc.page_count else "BAD"
        if arrow == "OK ":
            ok += 1
        else:
            bad += 1
        dest = f"p{tgt+1:02d} {PAGE_NAMES.get(tgt,'?')}" if tgt >= 0 else "UNRESOLVED"
        print(f"    [{arrow}] '{lbl}'  ->  {dest}")
    print()

print(f"resolved GoTo links: {ok} valid, {bad} broken")

# --- targeted checks from the revision request ---------------------------
def _internal(l):
    # WeasyPrint emits internal links as named destinations (kind=NAMED);
    # pymupdf still resolves the target into l["page"]. Accept both.
    return l["kind"] in (fitz.LINK_GOTO, fitz.LINK_NAMED) and l.get("page", -1) >= 0


def find(page_idx, needle):
    page = doc[page_idx]
    for l in page.get_links():
        if not _internal(l):
            continue
        if needle.lower() in label_for(page, l["from"]).lower():
            return l["page"]
    return None

print("\n--- targeted checks ---")
checks = [
    ("Page 2 back-note -> Page 1", find(1, "come back") == 0 or find(1, "hard feeling") == 0),
    ("Page 2 'full Low Energy Bank' -> Page 4", find(1, "Low Energy Bank") == 3),
    ("Page 2 'full High Energy Bank' -> Page 5", find(1, "High Energy Bank") == 4),
    ("Page 3 'act on ... Task Breakdown' -> Page 6", find(2, "act on") == 5 or find(2, "Task Breakdown") == 5),
]
# nav bar targets, checked on Check-In page (index 1)
nav_targets = {"Home": 0, "Check-In": 1, "Brain Dump": 2, "To-Do": 3, "Tasks": 5}
for lbl, want in nav_targets.items():
    checks.append((f"Nav '{lbl}' -> p{want+1:02d}", find(1, lbl) == want))

for name, passed in checks:
    print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
