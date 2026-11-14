"""food-picture-01 entry, v3: a brighter, glossier steaming ramen.

This program ships one photograph to the judge: a close-up bowl of ramen
with chopsticks lifting a tall tangle of glossy noodles, a halved
soft-boiled egg with a deep orange jammy yolk, charred chashu fanned
across golden broth, scallions and nori, steam curling in warm light
over a dark wooden table. The picture lives beside this file as
entry.png (a JPEG under that name, which the rules allow) and is copied
to /output/entry.png byte for byte, so the judge sees exactly the frame
we reviewed and chose.

Only the Python standard library is used. There is no network and no
randomness: every run writes the same bytes. Before writing, the program
refuses an empty file, checks the JPEG magic bytes, and checks the
SHA-256 of the picture against the digest recorded below, so a damaged
or swapped file fails loudly instead of reaching the judge.

Run it outside the grader's container with:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import sys
from pathlib import Path

# SHA-256 of the v3 ramen photograph. The guard below ships nothing else.
PICTURE_SHA256 = "87a7f2844f49571916914445875ac9c9df2a3a27d896dc530ef0b58e64f2802e"


def load_picture() -> bytes:
    """Read entry.png and prove it is the reviewed v3 photograph."""
    picture = (Path(__file__).resolve().parent / "entry.png").read_bytes()
    if not picture:
        raise ValueError("entry.png is empty, refusing a blank frame")
    if picture[:2] != b"\xff\xd8":
        raise ValueError("entry.png is not a JPEG (bad magic bytes)")
    if picture[-2:] != b"\xff\xd9":
        raise ValueError("entry.png is a truncated JPEG (no end marker)")
    if hashlib.sha256(picture).hexdigest() != PICTURE_SHA256:
        raise ValueError("entry.png digest mismatch, refusing a swapped picture")
    return picture


def main() -> int:
    try:
        picture = load_picture()
    except (OSError, ValueError) as exc:
        print(f"entry.png rejected: {exc}", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(picture)
    # Read the copy back: the judge sees exactly these bytes, so the
    # file we wrote must match the picture we verified above.
    written = target.read_bytes()
    if written != picture:
        print("written copy differs from entry.png", file=sys.stderr)
        return 1
    print(f"wrote {target} ({len(picture)} bytes, sha256 {PICTURE_SHA256[:12]}...)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
