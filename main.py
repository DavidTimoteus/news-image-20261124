#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261124 (v2).

Copies the pre-rendered front page (entry.png, drawn in code by
render_image.py with Pillow) to the output directory. Standard
library only, no network, no randomness: two runs write identical
bytes.
"""
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", out_dir / "entry.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
