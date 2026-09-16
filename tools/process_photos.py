#!/usr/bin/env python3
"""Optimize gallery source photos for the web.

Drop your originals (any of .heic/.jpg/.jpeg/.png, any capitalization) into
    docs/images/gallery/_raw/
naming each file with the target STEM below (extension doesn't matter), e.g.
    01-taj-mahal.HEIC   ->   docs/images/gallery/01-taj-mahal.jpg

Then run:   python3 tools/process_photos.py

Each photo is auto-rotated (EXIF), resized, compressed, and saved WITHOUT any
metadata (EXIF/GPS is stripped for privacy). HEIC is converted via macOS `sips`.
"""
import os
import subprocess
import sys
import tempfile
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "docs", "images", "gallery", "_raw")
OUT = os.path.join(ROOT, "docs", "images", "gallery")

# target stem -> (max long edge px, jpeg quality)
# Sized for crisp 2x retina at the displayed dimensions; the panorama is
# full-bleed so it gets the largest ceiling.
TARGETS = {
    "panorama":        (3200, 82),
    "01-taj-mahal":    (2200, 82),
    "02-pangong":      (2000, 82),
    "03-sahara":       (2000, 82),
    "04-ghana":        (2000, 82),
    "05-miami":        (2000, 82),
    "06-jaipur":       (2200, 82),
    "07-aescher":      (2000, 82),
    "08-lucerne":      (2000, 82),
    "09-paris":        (2200, 82),
}
EXTS = (".heic", ".heif", ".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp")


def find_source(stem):
    if not os.path.isdir(RAW):
        return None
    for f in os.listdir(RAW):
        name, ext = os.path.splitext(f)
        if name.lower() == stem.lower() and ext.lower() in EXTS:
            return os.path.join(RAW, f)
    return None


def load_image(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".heic", ".heif"):
        tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False).name
        subprocess.run(["sips", "-s", "format", "jpeg", path, "--out", tmp],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        img = Image.open(tmp)
        img.load()
        os.unlink(tmp)
        return img
    return Image.open(path)


def process(stem, max_edge, quality):
    src = find_source(stem)
    if not src:
        return "missing"
    img = load_image(src)
    img = ImageOps.exif_transpose(img)          # honour orientation
    img = img.convert("RGB")                     # drop alpha/profiles
    w, h = img.size
    scale = min(1.0, max_edge / float(max(w, h)))
    if scale < 1.0:
        img = img.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
    out = os.path.join(OUT, stem + ".jpg")
    # No exif passed -> metadata (incl. GPS) is stripped.
    img.save(out, "JPEG", quality=quality, optimize=True, progressive=True)
    kb = os.path.getsize(out) // 1024
    return f"{img.size[0]}x{img.size[1]}  {kb} KB  <- {os.path.basename(src)}"


def main():
    print(f"Reading from: {RAW}\n")
    done = missing = 0
    for stem, (edge, q) in TARGETS.items():
        result = process(stem, edge, q)
        if result == "missing":
            missing += 1
            print(f"  [ ] {stem:18} — no source in _raw/ (still using placeholder)")
        else:
            done += 1
            print(f"  [x] {stem:18} — {result}")
    print(f"\n{done} processed, {missing} still placeholder.")
    if missing:
        print("Add the missing files to _raw/ (named by the stem) and re-run.")


if __name__ == "__main__":
    main()
