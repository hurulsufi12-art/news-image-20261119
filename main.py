"""news-image-20261119 entry (Python 3.13, standard library only).

The image is the entry.png beside this file, drawn with code by draw.py
(Pillow, run at build time only -- the grader runs this file alone, with
no network and nothing installed). This program copies it to
/output/entry.png, the same pattern as the kit starter's main.ts.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main() -> None:
    if not SOURCE.is_file():
        raise FileNotFoundError(f"entry image missing beside main.py: {SOURCE}")
    # The gate gives an invalid image no rate and no prize, so refuse to
    # ship anything that is not a PNG at all.
    if SOURCE.read_bytes()[:8] != PNG_MAGIC:
        raise ValueError(f"entry image beside main.py is not a PNG: {SOURCE}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    target = OUTPUT_DIR / "entry.png"
    shutil.copyfile(SOURCE, target)
    # Fail loudly instead of shipping a bad copy: the gate gives an
    # invalid entry no rate and no prize.
    if target.stat().st_size != SOURCE.stat().st_size:
        raise OSError(f"copied entry.png is {target.stat().st_size} bytes, "
                      f"source is {SOURCE.stat().st_size} bytes")
    if target.read_bytes()[:8] != PNG_MAGIC:
        raise ValueError("copied entry.png is not a PNG")


if __name__ == "__main__":
    main()
