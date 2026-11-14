"""food-picture-01 entry (Python 3.13, standard library only).

Copies the picture held in entry.png beside this file to /output/entry.png,
byte for byte. The picture is a steaming bowl of ramen photographed close up:
glossy noodles lifted high on wooden chopsticks, a halved soft-boiled egg
with a jammy orange yolk, charred chashu, scallions and nori in golden broth,
steam rising in warm light. It is made to make the mouth water at one glance
and to read clearly even at about 300 pixels across.

The file is a JPEG (told apart by its first bytes) kept under the name
entry.png, as the rules allow. The program does no network access and no
computation that could vary between runs, so two runs write identical bytes.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import sys
from pathlib import Path  # standard library only; nothing is installed before the run


def main() -> int:
    here = Path(__file__).resolve().parent
    picture = (here / "entry.png").read_bytes()
    # The picture is a JPEG under the name entry.png; the gate tells the
    # format from the first bytes, so nothing here needs to know or care.
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(picture)
    # Fail loudly rather than silently shipping a partial copy: the judge
    # sees exactly these bytes, so the written file must match the source.
    if target.read_bytes() != picture:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
