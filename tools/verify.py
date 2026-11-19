# -*- coding: utf-8 -*-
"""Validate dist/zh.csv with the game's own loader rules."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common


def main():
    game = common.find_game_dir(None)
    loc = common.loc_dir(game)
    ru, order = common.parse_game_csv(os.path.join(loc, "ru.csv"))
    en, _ = common.parse_game_csv(os.path.join(loc, "en.csv"))
    zh_path = os.path.join(common.repo_root(), "dist", common.CSV_NAME)
    zh, _ = common.parse_game_csv(zh_path)

    print("rows:", len(order))
    bad = 0
    for row in order:
        if len(ru[row]) != len(zh.get(row, [])):
            bad += 1
            print("length mismatch:", row, len(ru[row]), len(zh.get(row, [])))
    print("length problems:", bad)

    cur = {}
    for layer in (ru, en, zh):
        for k, v in layer.items():
            old = cur.get(k)
            if old is None or len(v) >= len(old):
                cur[k] = list(v)
            else:
                old = list(old)
                for i, x in enumerate(v):
                    old[i] = x
                cur[k] = old

    empty = 0
    for row in order:
        arr = cur.get(row, [])
        for i, v in enumerate(arr):
            if v == "":
                empty += 1
    print("empty slots after merge:", empty)
    print("OK" if not bad else "PROBLEMS FOUND")


if __name__ == "__main__":
    main()
