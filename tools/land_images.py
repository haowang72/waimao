# -*- coding: utf-8 -*-
"""Land verified candidate product photos into site/assets/img/products/<slug>-1.jpg.

Rules enforced here:
  * only visually verified, watermark-free, people-free photos are mapped
  * the two GMCC photos carrying a blue 'HICOOL' logo on white are auto-cropped
  * oversized photos are downscaled for web
"""
import sys
from pathlib import Path
import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "candidate_images" / "_raw"
OUT = ROOT / "site" / "assets" / "img" / "products"
OUT.mkdir(parents=True, exist_ok=True)

MAXSIDE = 1100


def imread_u(path):
    """cv2.imread fails on non-ASCII Windows paths; decode from bytes instead."""
    p = Path(path)
    if not p.exists():
        return None
    data = np.fromfile(str(p), dtype=np.uint8)
    if data.size == 0:
        return None
    return cv2.imdecode(data, cv2.IMREAD_COLOR)


def imwrite_u(path, img):
    ok, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 90])
    if ok:
        buf.tofile(str(path))
    return ok


# slug-file  ->  source path under _raw/
COPIES = {
    "copeland-zp24k3e-pfj-522-1.jpg": "copeland-zp24k3e-pfj-522/3.jpg",
    "aspera-nek6213z-1.jpg":          "aspera-nek6213z/1.jpg",
    "aspera-nek2134gk-1.jpg":         "embraco-egz80hlp/e318.jpg",
    "aspera-nek-series-1.jpg":        "aspera-nek2134gk/7.jpg",
    "embraco-ffi12hbk-1.jpg":         "embraco-egz80hlp/n216.jpg",
    "embraco-egz80hlp-1.jpg":         "embraco-egz80hlp/e311.jpg",
    "gmcc-ph150x1c-4p3-1.jpg":        "gmcc-ph150x1c-4p3/1.jpg",
    "maneurop-mt64hm4-1.jpg":         "maneurop-mt64hm4/d405.jpg",
    "copeland-zr-series-1.jpg":       "site:copeland-zr34k3-pfj-522-1.jpg",
}

# dest -> source, with HICOOL blue-logo auto-crop
CROPS = {
    "gmcc-ph135x1c-4p3-1.jpg": "gmcc-ph135x1c-4p3/8.jpg",
    "gmcc-ph-series-1.jpg":    "gmcc-ph135x1c-4p3/1.jpg",
}


def trim_blue_logo(img, guard=0.28):
    """Crop the top band that holds a blue brand logo (HICOOL) sitting on white."""
    h, w = img.shape[:2]
    band = img[:int(h * guard)]
    b = band[:, :, 0].astype(int); r = band[:, :, 2].astype(int)
    blue = (b > 90) & (r < 120) & ((b - r) > 35)
    ys, xs = np.where(blue)
    if len(ys) == 0:
        return img, 0
    cut = min(int(ys.max()) + int(h * 0.02) + 12, int(h * guard))
    return img[cut:, :], cut


def save(img, name):
    h, w = img.shape[:2]
    s = MAXSIDE / max(h, w)
    if s < 1:
        img = cv2.resize(img, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA)
    fp = OUT / name
    imwrite_u(fp, img)
    return fp, f"{img.shape[1]}x{img.shape[0]}"


def main():
    ok, miss = 0, []
    print("== straight copies ==")
    for dest, src in COPIES.items():
        if src.startswith("site:"):
            p = ROOT / "site" / "assets" / "img" / "products" / src.split(":", 1)[1]
        else:
            p = RAW / src
        img = imread_u(p)
        if img is None:
            miss.append((dest, str(p))); print(f"  MISS {dest} <- {p}"); continue
        fp, dim = save(img, dest)
        print(f"  ok  {dest:<34} {dim:>9}  <- {p.name}"); ok += 1

    print("== HICOOL crop ==")
    for dest, src in CROPS.items():
        p = RAW / src
        img = imread_u(p)
        if img is None:
            miss.append((dest, str(p))); print(f"  MISS {dest} <- {p}"); continue
        img2, cut = trim_blue_logo(img)
        fp, dim = save(img2, dest)
        print(f"  ok  {dest:<34} {dim:>9}  cropped {cut}px top  <- {p.name}"); ok += 1

    print(f"\nlanded {ok}, missing {len(miss)}")
    for d, s in miss:
        print("  missing:", d, s)


if __name__ == "__main__":
    main()
