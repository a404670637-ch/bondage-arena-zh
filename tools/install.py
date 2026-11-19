# -*- coding: utf-8 -*-
"""Install (or restore) the Chinese text file into the game folder."""
import argparse
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as builder
import common

BACKUP_SUFFIX = ".official"


def main():
    ap = argparse.ArgumentParser(description="Install the Bondage Arena Chinese patch")
    ap.add_argument("--game", help="game folder (contains Bondage Arena_Data)")
    ap.add_argument("--restore", action="store_true", help="restore the original zh.csv")
    args = ap.parse_args()

    game = common.find_game_dir(args.game)
    target = os.path.join(common.loc_dir(game), common.CSV_NAME)
    backup = target + BACKUP_SUFFIX

    if args.restore:
        if not os.path.exists(backup):
            raise SystemExit("no backup found: " + backup)
        shutil.copy2(backup, target)
        print("restored", target)
        return

    if not os.path.exists(backup):
        shutil.copy2(target, backup)
        print("backed up original ->", backup)
    else:
        print("backup already exists, keeping it:", backup)

    src = os.path.join(common.repo_root(), "dist", common.CSV_NAME)
    if not os.path.exists(src):
        src = builder.build()
    shutil.copy2(src, target)
    print("installed", target)
    print("select 中文 / Chinese in the game language menu.")


if __name__ == "__main__":
    main()
