"""News image entry for make.fun: news-image-20261124.

Sums up the world news of Tuesday 24 November 2026 in one image.

The image itself is entry.png beside this file. It was drawn for this
entry as a dense one-page newspaper front page: a masthead with the
date, a lead story on the UN probe after Ukraine sank a Russian
warship off Libya, four big headlines (Nvidia soaring 31% as Huang
returns, Russia's nuclear warning, the Iran war deepening, and
fourteen nations backing the Rohingya genocide ruling), and a dated
"day in brief" grid — 32 stories in total, every one reported on
24 November 2026, across eight regions.

This program only copies that image to the output path. It uses the
standard library only, makes no network call, and reads nothing
outside its own directory, so running it twice writes the same bytes.
The image was rendered at build time by render_image.py (Pillow),
which wraps every line by measured pixel width so no text overlaps.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def main() -> None:
    if not SOURCE.is_file():
        raise FileNotFoundError(f"entry image missing: {SOURCE}")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    if target.stat().st_size > 1_048_576:
        raise ValueError("entry image is over the 1 MiB limit")


if __name__ == "__main__":
    main()
