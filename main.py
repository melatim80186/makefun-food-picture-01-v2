"""food-picture-01 entry: steaming ramen, ready for the judge.

The entry program for make.fun's "Make the best-looking food picture"
bounty. It writes the picture stored beside it (entry.png) to
/output/entry.png, byte for byte, so the image judge sees exactly the
photograph we made: a close-up bowl of ramen, chopsticks lifting glossy
noodles, a halved soft-boiled egg with a jammy orange yolk, charred
chashu, scallions and nori floating in golden broth, steam curling up
in warm light over a dark wooden table.

The picture file is a JPEG that keeps the name entry.png, which the
rules allow. The program uses only the Python standard library, touches
no network, and has no randomness, so every run produces the same
bytes. It also checks the picture against its expected SHA-256 before
writing, so a damaged or swapped file fails loudly instead of reaching
the judge.

Run it outside the grader's container with:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import sys
from pathlib import Path

# SHA-256 of the ramen photograph as built for this entry. The check
# below refuses to ship anything else.
EXPECTED_SHA256 = "f189b5d9ec9fbc82ea8f7cc4f72bcae14272ba959bbab5351a951612493701ce"


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    picture = source.read_bytes()
    if not picture:
        print("entry.png is empty, refusing to write a blank frame", file=sys.stderr)
        return 1
    if picture[:2] != b"\xff\xd8":
        print("entry.png is not a JPEG (bad magic bytes)", file=sys.stderr)
        return 1
    digest = hashlib.sha256(picture).hexdigest()
    if digest != EXPECTED_SHA256:
        print(f"entry.png digest mismatch: got {digest}", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(picture)
    # Read the copy back: the judge sees exactly these bytes, so the
    # written file must match the picture we verified above.
    written = target.read_bytes()
    if written != picture:
        print("written copy differs from entry.png", file=sys.stderr)
        return 1
    print(f"wrote {target} ({len(written)} bytes, sha256 {digest[:12]}...)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
