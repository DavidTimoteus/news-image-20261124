#!/usr/bin/env python3
"""Entry point: copy the pre-rendered front page to /output/entry.png.

Stdlib only. Deterministic: a plain byte-for-byte copy, no timestamps,
no randomness, no network. Running it twice writes identical bytes.
"""

import os

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DST = "/output/entry.png"


def main():
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    with open(SRC, "rb") as fin, open(DST, "wb") as fout:
        while True:
            block = fin.read(8192)
            if not block:
                break
            fout.write(block)


if __name__ == "__main__":
    main()
