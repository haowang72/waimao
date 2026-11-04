# -*- coding: utf-8 -*-
"""Third focused grab: exact-model B2B product pages for the models still missing images.
   Extracts og:image first, then gallery images. Saves to data/candidate_images/_raw/<slug>/."""
import os, re, sys, urllib.request, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "candidate_images" / "_raw"
RAW.mkdir(parents=True, exist_ok=True)

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

TARGETS = {
    "gmcc-ph150x1c-4p3": [
        "https://www.tradechina.com/Wholesale-electronic-components-Support-BOM-Quotation_240142528.html",
    ],
    "maneurop-mt64hm4": [
        "https://m.11467.com/product/d4633351.htm",
        "https://mip.biz72.com/provide/elv11blm0.html",
    ],
    "embraco-egz80hlp": [
        "https://www.hvacrcompressor.com/search?type=product&q=EGZ80HLP",
        "https://www.embracous.com/blog/embraco-egz-80hlp-compressor-what-a-buyer-learned-after-5-years-price-86.html",
        "https://www.embracous.com/",
    ],
}

IMG_RE = re.compile(r'(?:og:image[^>]*?content=["\']|["\'](https?://[^"\']+?\.(?:jpg|jpeg|png|webp)))', re.I)


def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,image/*,*/*",
        "Accept-Language": "en-US,en;q=0.9",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def extract_images(html, base):
    out = []
    # og:image / twitter:image first
    for pat in [r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)',
                r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)',
                r'"image"\s*:\s*"(https?://[^"]+)"',
                r'data-src=["\']([^"\']+)',
                r'data-lazy-src=["\']([^"\']+)',
                r'src=["\']([^"\']+\.(?:jpg|jpeg|png|webp))',
                r'srcset=["\']([^"\',]+)']:
        for m in re.finditer(pat, html, re.I):
            out.append(m.group(1))
    # normalise
    res, seen = [], set()
    for u in out:
        u = u.strip()
        if u.startswith("//"):
            u = "https:" + u
        elif u.startswith("/"):
            u = urllib.parse.urljoin(base, u)
        if not u.lower().startswith("http"):
            continue
        if u in seen:
            continue
        seen.add(u)
        res.append(u)
    return res


def guess_ext(url, data):
    u = url.lower()
    for e in ("jpg", "jpeg", "png", "webp"):
        if "." + e in u:
            return "jpg" if e == "jpeg" else e
    if data[:3] == b"\xff\xd8\xff":
        return "jpg"
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    if data[:4] == b"RIFF":
        return "webp"
    return None


def main():
    for slug, urls in TARGETS.items():
        destdir = RAW / slug
        destdir.mkdir(parents=True, exist_ok=True)
        n = 1
        for page in urls:
            try:
                html = fetch(page).decode("utf-8", "ignore")
            except Exception as e:
                print(f"[page-fail] {slug} {page} -> {e}")
                continue
            cand = extract_images(html, page)
            print(f"[page] {slug} {page} -> {len(cand)} img refs")
            for cu in cand:
                try:
                    data = fetch(cu)
                except Exception as e:
                    continue
                if len(data) < 9000:      # skip tiny icons/logos
                    continue
                ext = guess_ext(cu, data)
                if not ext:
                    continue
                while (destdir / f"{n}.{ext}").exists():
                    n += 1
                fp = destdir / f"g{n}.{ext}"
                fp.write_bytes(data)
                print(f"   saved {fp.name}  {len(data)//1024}KB  <- {cu[:110]}")
                n += 1
                if n > 30:
                    break
    print("done")


if __name__ == "__main__":
    main()
