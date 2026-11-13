# "The Empty Chair" — news-image-01 entry (Python 3.13, standard library only).
#
# The program copies the repository-held image to /output/entry.png.
# It runs with no network, deterministically: the same bytes every run.
#
# Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
MAX_BYTES = 1048576  # gate limit: at most 1 MiB
# Magic bytes the gate accepts: PNG signature or JPEG SOI marker.
MAGIC = (b"\x89PNG\r\n\x1a\n", b"\xff\xd8\xff")

os.makedirs(DST_DIR, exist_ok=True)
dst = os.path.join(DST_DIR, "entry.png")
shutil.copyfile(SRC, dst)

# Fail loudly instead of handing the grader a broken file.
with open(dst, "rb") as f:
    head = f.read(8)
size = os.path.getsize(dst)
if not head.startswith(MAGIC):
    raise SystemExit("entry.png is neither PNG nor JPEG (bad magic bytes)")
if size > MAX_BYTES:
    raise SystemExit(f"entry.png is {size} bytes, over the 1 MiB limit")
print(f"wrote {dst} ({size} bytes)")
