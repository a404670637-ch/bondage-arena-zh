# -*- coding: utf-8 -*-
"""Shared helpers for the Bondage Arena Chinese patch tools."""
import csv
import hashlib
import json
import os
import sys

LOC_SUBPATH = os.path.join("Bondage Arena_Data", "StreamingAssets", "Localizations")
CSV_NAME = "zh.csv"
BOM = "\ufeff"


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def strings_path():
    return os.path.join(repo_root(), "data", "strings.json")


def load_strings():
    with open(strings_path(), encoding="utf-8") as f:
        return json.load(f)


def sha1_16(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]


def find_game_dir(explicit=None):
    """Locate the game folder (the one that contains Bondage Arena_Data)."""
    if explicit:
        p = os.path.abspath(explicit)
        if os.path.isdir(os.path.join(p, "Bondage Arena_Data")):
            return p
        raise SystemExit("not a Bondage Arena folder: " + p)

    candidates = []
    for drive in "CDEFGHIJ":
        candidates.append(drive + ":\\Bondage Arena 24.0 premium")
    # Steam library folders
    for base in (
        r"C:\Program Files (x86)\Steam\steamapps\common",
        r"C:\Program Files\Steam\steamapps\common",
    ):
        candidates.append(os.path.join(base, "Bondage Arena"))
    for c in candidates:
        if os.path.isdir(os.path.join(c, "Bondage Arena_Data")):
            return c
    raise SystemExit("game folder not found; pass --game <path>")


def loc_dir(game_dir):
    return os.path.join(game_dir, LOC_SUBPATH)


def parse_game_csv(path):
    """Reproduce Txt.Load_text: split on ';', stop the row at the first empty cell,
    turn '-' into an empty string."""
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f, delimiter=";"))
    out = {}
    order = []
    for r in rows:
        if not r or len(r) <= 1 or not r[0].strip():
            continue
        vals = []
        for c in r[1:]:
            if c == "":
                break
            vals.append("" if c == "-" else c)
        out[r[0]] = vals
        order.append(r[0])
    return out, order
