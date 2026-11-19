# -*- coding: utf-8 -*-
"""Compare the installed game version with our translation database."""
import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common


def main():
    ap = argparse.ArgumentParser(description="Report what a game update changed")
    ap.add_argument("--game", help="game folder")
    ap.add_argument("--out", default="out/untranslated.csv", help="where to write the work list")
    args = ap.parse_args()

    game = common.find_game_dir(args.game)
    ru_path = os.path.join(common.loc_dir(game), "ru.csv")
    if not os.path.exists(ru_path):
        raise SystemExit("ru.csv not found: " + ru_path)

    ru, order = common.parse_game_csv(ru_path)
    data = common.load_strings()

    new_cells = []      # row, idx, ru
    changed_cells = []  # row, idx, ru
    matched = 0
    known_rows = set(data["rows"])
    for row in order:
        if row not in data["rows"]:
            info = {"len": 0, "dash": [], "items": []}
            data["rows"][row] = info
        info = data["rows"][row]
        by_hash = {it["h"]: it for it in info["items"]}
        by_idx = {it["i"]: it for it in info["items"]}
        for i, text in enumerate(ru[row]):
            if text == "":
                continue
            h = common.sha1_16(text)
            if h in by_hash:
                matched += 1
            elif i in by_idx:
                changed_cells.append((row, i, text))
            else:
                new_cells.append((row, i, text))

    print("rows in game:", len(order))
    print("cells matched by source hash:", matched)
    print("changed cells (same slot, new Russian):", len(changed_cells))
    print("brand new cells:", len(new_cells))
    old_rows = known_rows - set(order)
    if old_rows:
        print("rows that disappeared:", ", ".join(sorted(old_rows)))

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["state", "row", "index", "russian"])
        for row, i, t in new_cells:
            w.writerow(["new", row, i, t])
        for row, i, t in changed_cells:
            w.writerow(["changed", row, i, t])
    print("work list written to", args.out)


if __name__ == "__main__":
    main()
