#!/usr/bin/env python3
"""Publish the 24 November 2026 front page for the make.fun harness.

The entry image lives next to this file as entry.png. All this program
does is place an exact copy of it where the harness expects it, then
confirm the copy is complete by comparing file sizes. Nothing here
touches the network, and nothing is random, so repeated runs produce
identical output bytes.
"""

import os
import sys

CHUNK = 1 << 20


def output_directory():
    """Directory the harness reads, from the environment or the default."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def publish(source, destination):
    """Copy source to destination in 1 MiB chunks; return bytes written."""
    written = 0
    with open(source, "rb") as src, open(destination, "wb") as dst:
        while True:
            block = src.read(CHUNK)
            if not block:
                break
            dst.write(block)
            written += len(block)
    return written


def main(argv=None):
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        print(f"entry image not found: {source}", file=sys.stderr)
        return 1
    out_dir = output_directory()
    os.makedirs(out_dir, exist_ok=True)
    destination = os.path.join(out_dir, "entry.png")
    copied = publish(source, destination)
    if copied != os.path.getsize(source):
        print("copy incomplete", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
