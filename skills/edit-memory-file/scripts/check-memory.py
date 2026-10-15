#!/usr/bin/env python3
"""Usage: check-memory.py FILE [MAX_LINES]

Checks a memory file against size limits, entry hygiene and link integrity.
Standard library only; runs the same on Linux, macOS and Windows.
Exit 0 when clean, 1 when problems were found, 2 on bad input.
"""
import datetime
import glob
import os
import re
import sys
from urllib.parse import unquote

MAX_BYTES = 25000


def main(argv):
    if len(argv) not in (2, 3):
        print(__doc__.strip().splitlines()[0])
        return 2
    path = argv[1]
    try:
        max_lines = int(argv[2]) if len(argv) == 3 else 100
    except ValueError:
        print("ERROR: MAX_LINES must be an integer")
        return 2
    if not os.path.isfile(path):
        print("ERROR: %s not found" % path)
        return 2
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")

    with open(path, encoding="utf-8-sig", newline="") as handle:
        text = handle.read()
    lines = text.splitlines()
    size = os.path.getsize(path)
    folder = os.path.dirname(os.path.abspath(path))
    today = datetime.date.today()
    today_s = today.isoformat()
    quarter = "%d-Q%d" % (today.year, (today.month - 1) // 3 + 1)
    problems = []

    print("lines=%d (max %d) bytes=%d (max %d)" % (len(lines), max_lines, size, MAX_BYTES))
    if len(lines) > max_lines:
        problems.append("OVER-LINES: %d > %d" % (len(lines), max_lines))
    if size > MAX_BYTES:
        problems.append("OVER-BYTES: %d > %d" % (size, MAX_BYTES))

    for num, line in enumerate(lines, 1):
        # Expired EXPIRES or REVIEW annotations (YYYY-QN, YYYY-MM or YYYY-MM-DD)
        for date in re.findall(r"\[(?:EXPIRES|REVIEW): ([^\]]+)\]", line):
            if re.fullmatch(r"\d{4}-Q[1-4]", date):
                expired = date < quarter
            elif re.fullmatch(r"\d{4}-\d{2}", date):
                expired = date < today_s[:7]
            elif re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
                expired = date < today_s
            else:
                expired = False
            if expired:
                problems.append("EXPIRED: line %d (%s)" % (num, date))
        # Top-level bullets must be index lines or start with a YYYY-MM date
        if line.startswith("- ") and not re.match(r"- (\[|\d{4}-\d{2})", line):
            problems.append("UNDATED: line %d: %s" % (num, line[:60]))

    # Relative links must resolve
    for target in sorted(set(re.findall(r"\]\(([^)#\s]+)", text))):
        if re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", target):
            continue
        if not os.path.exists(os.path.join(folder, unquote(target))):
            problems.append("BROKEN-LINK: %s" % target)

    # Topic files with frontmatter beside an index must be linked from it
    if os.path.basename(path) == "MEMORY.md":
        for other in sorted(glob.glob(os.path.join(folder, "*.md"))):
            base = os.path.basename(other)
            if base == "MEMORY.md":
                continue
            with open(other, encoding="utf-8-sig", errors="replace") as handle:
                head = handle.read().splitlines()
            if head[:1] == ["---"] and any(item.startswith("name:") for item in head[1:]):
                if "(%s)" % base not in text:
                    problems.append("ORPHAN: %s has no index line" % base)

    for item in problems:
        print(item)
    print("OK" if not problems else "problems=%d" % len(problems))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))