#!/usr/bin/env python3
"""Write entry.png to the make.fun output directory.

Python 3.13, standard library only, no network, deterministic: the file
is copied byte for byte, and the copy is re-read and compared before we
report success. Two runs produce byte-identical output.

Usage:
    MAKEFUN_OUTPUT_DIR=out python3 main.py
    (without the variable, defaults to /output)
"""
import hashlib
import os
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024        # 1 MiB gate from the bounty rules
MAX_DIMENSION = 1024           # 1024x1024 gate from the bounty rules
SOURCE_NAME = "entry.png"


def fail(message):
    print(f"main.py: ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def read_png_dimensions(data):
    """Width/height from the IHDR chunk (bytes 16-23 of a PNG file)."""
    if len(data) < 24:
        fail("entry.png is shorter than a PNG header (24 bytes)")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)

    try:
        with open(source, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        fail(f"cannot read {source}: {exc}")

    if not data.startswith(PNG_MAGIC):
        fail("entry.png does not start with the PNG magic bytes")
    if len(data) > MAX_BYTES:
        fail(f"entry.png is {len(data)} bytes, over the 1 MiB limit")

    width, height = read_png_dimensions(data)
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        fail(f"entry.png is {width}x{height}, over the 1024x1024 limit")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        fail(f"cannot create output directory {out_dir}: {exc}")

    destination = os.path.join(out_dir, SOURCE_NAME)
    try:
        with open(destination, "wb") as handle:
            handle.write(data)
    except OSError as exc:
        fail(f"cannot write {destination}: {exc}")

    try:
        with open(destination, "rb") as handle:
            written = handle.read()
    except OSError as exc:
        fail(f"cannot re-read {destination} for verification: {exc}")
    if written != data:
        fail("verification failed: written file differs from entry.png")
    out_w, out_h = read_png_dimensions(written)
    if (out_w, out_h) != (width, height):
        fail("verification failed: written file dimensions changed")

    digest = hashlib.sha256(data).hexdigest()
    print(f"main.py: wrote {destination} ({len(data)} bytes, "
          f"{width}x{height} PNG, sha256 {digest})")


if __name__ == "__main__":
    main()
