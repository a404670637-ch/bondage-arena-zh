# -*- coding: utf-8 -*-
"""Offline checks that do not need the game installed."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common

data = common.load_strings()
errors = []
cells = 0
for row, info in data["rows"].items():
    n = info["len"]
    dash = set(info["dash"])
    seen = set()
    for it in info["items"]:
        cells += 1
        i = it["i"]
        if i in seen:
            errors.append("duplicate index %s[%d]" % (row, i))
        seen.add(i)
        if i >= n:
            errors.append("index out of range %s[%d]" % (row, i))
        if i in dash:
            errors.append("translation on a placeholder slot %s[%d]" % (row, i))
        zh = it["zh"]
        if not zh:
            errors.append("empty translation %s[%d]" % (row, i))
        if ";" in zh or "\n" in zh or "\r" in zh:
            errors.append("illegal character %s[%d]" % (row, i))
        if len(it["h"]) != 16:
            errors.append("bad hash %s[%d]" % (row, i))
    if len(seen) + len(dash) != n:
        errors.append("coverage mismatch %s: %d items + %d placeholders != %d"
                      % (row, len(seen), len(dash), n))

print("rows: %d | cells: %d" % (len(data["rows"]), cells))
if errors:
    for e in errors[:20]:
        print("ERROR:", e)
    sys.exit(1)
print("OK")
