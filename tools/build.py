# -*- coding: utf-8 -*-
"""Rebuild dist/zh.csv from data/strings.json (no game files required)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common


def fix_quotes(s):
    """ASCII double quotes would confuse CSV editors; use full-width ones."""
    if '"' not in s or s.count('"') % 2:
        return s
    out = []
    opening = True
    for ch in s:
        if ch == '"':
            out.append("\u201c" if opening else "\u201d")
            opening = not opening
        else:
            out.append(ch)
    return "".join(out)


def build():
    data = common.load_strings()
    lines = []
    total = 0
    for row, info in data["rows"].items():
        n = info["len"]
        cells = ["-"] * n
        for it in info["items"]:
            zh = it["zh"]
            if not zh:
                raise SystemExit("empty translation: %s[%d]" % (row, it["i"]))
            if ";" in zh or "\n" in zh or "\r" in zh:
                raise SystemExit("illegal character in %s[%d]" % (row, it["i"]))
            cells[it["i"]] = fix_quotes(zh)
        lines.append(row + ";" + ";".join(cells))
        total += n
    out = os.path.join(common.repo_root(), "dist", common.CSV_NAME)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8-sig", newline="") as f:
        f.write("\r\n".join(lines) + "\r\n")
    print("wrote %s (%d rows, %d cells)" % (out, len(lines), total))
    return out


if __name__ == "__main__":
    build()
