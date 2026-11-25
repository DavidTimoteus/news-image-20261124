#!/usr/bin/env python3
"""Entrypoint: emit the pre-rendered front page as /output/entry.png.

The image is rendered at build time by render_image.py (Pillow, code-drawn);
this program only places the exact bytes at the harness output path, so two
runs always produce identical output.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST_DIR = "/output"
DST = os.path.join(DST_DIR, "entry.png")


def main():
    os.makedirs(DST_DIR, exist_ok=True)
    with open(SRC, "rb") as src, open(DST, "wb") as dst:
        while True:
            block = src.read(1 << 16)
            if not block:
                break
            dst.write(block)


if __name__ == "__main__":
    main()
