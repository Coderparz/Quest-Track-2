# Step 1: cut the 4 poses out of art/sheet.png and shrink them to about 250 px.
# Uses only tkinter (comes with Python), no installs.
# Run once:  python cut_poses.py

import struct
import tkinter as tk
from pathlib import Path


def clean_png_bytes(path):
    """Read a PNG but keep only the picture parts.
    sheet.png has a hidden 'content credentials' section (caBX) with a small
    logo inside, and tkinter wrongly shows that logo instead of the dog."""
    data = Path(path).read_bytes()
    out = [data[:8]]  # PNG signature
    pos = 8
    while pos < len(data):
        length, kind = struct.unpack(">I4s", data[pos:pos + 8])
        chunk = data[pos:pos + 12 + length]
        if kind in (b"IHDR", b"PLTE", b"tRNS", b"IDAT", b"IEND"):
            out.append(chunk)
        pos += 12 + length
        if kind == b"IEND":
            break
    return b"".join(out)

ART = Path(__file__).parent / "art"

# Which spot in the 2x2 sheet is which pose: (column, row)
POSES = {
    "ready": (0, 0),   # top-left: both paws up
    "left":  (1, 0),   # top-right: left paw hits
    "right": (0, 1),   # bottom-left: right paw hits
    "sleep": (1, 1),   # bottom-right: sleeping zZ
}

# Shrink: keep 1 of every 5 pixels, then make 2x bigger  ->  2/5 = 0.4 size
# (each pose is 627 px, so 627 x 0.4 = about 250 px)
ZOOM, SUBSAMPLE = 2, 5

root = tk.Tk()
root.withdraw()  # we don't need a window, only the picture tools

sheet = tk.PhotoImage(data=clean_png_bytes(ART / "sheet.png"))
w, h = sheet.width(), sheet.height()
cell_w, cell_h = w // 2, h // 2
print(f"sheet: {w}x{h}, each pose: {cell_w}x{cell_h}")
print("corner is see-through:", sheet.transparency_get(0, 0))

for name, (col, row) in POSES.items():
    x, y = col * cell_w, row * cell_h
    cell = sheet.copy(from_coords=(x, y, x + cell_w, y + cell_h))
    small = cell.subsample(SUBSAMPLE).zoom(ZOOM)
    out = ART / f"{name}.png"
    small.write(out, format="png")
    print(f"saved {out.name}: {small.width()}x{small.height()}")

root.destroy()
