"""Audit: find all bi() calls NOT in unsafe_allow_html contexts."""
import re

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Track which bi() calls are inside unsafe_allow_html blocks
# vs used as variables that feed into unsafe_allow_html blocks
for i, line in enumerate(lines, 1):
    if "bi(" not in line:
        continue
    s = line.strip()
    # Skip definition
    if s.startswith("def bi("):
        continue
    if "Return an" in s:
        continue
    # Skip variable assignments (used in HTML contexts)
    if any(s.startswith(x) for x in [
        "emoji =", "em =", "icon =", "flags_html", "sig_html",
        "STATUS_", "nav_icons", "tier_map", "tier_icon", "tier_label",
        "icon_name", "contact +=",
    ]):
        continue
    # Skip lines with unsafe_allow_html=True
    if "unsafe_allow_html" in s:
        continue
    # Skip lines that are part of multi-line unsafe_allow_html blocks
    # Check if they are inside an f-string that ends with unsafe_allow_html
    # These are variable definitions that will be used in HTML
    if s.startswith("for icon,val") or s.startswith("for col,label"):
        continue
    # These are items in lists that will be used in HTML via unsafe_allow_html
    if s.startswith("(bi(") or s.startswith('(f"') or s.startswith('"'):
        # Check if part of tips/rows/items/cats list
        # Look at nearby context
        context = "".join(lines[max(0,i-5):i+5])
        if "unsafe_allow_html" in context:
            continue
    
    print(f"L{i}: {s[:150]}")
