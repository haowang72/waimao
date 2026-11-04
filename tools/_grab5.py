# -*- coding: utf-8 -*-
"""Fifth grab: Embraco distributor product pages (FFI / EGZ / NEK)."""
import re, ssl, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "candidate_images" / "_raw"
_CTX = ssl.create_default_context(); _CTX.check_hostname = False; _CTX.verify_mode = ssl.CERT_NONE

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

TARGETS = {
    "embraco-ffi12hbk": [
        "http://m.rfjcompressor.com/hermetic-piston-compressor/hermetic-piston-compressor-for-embraco/r134a-refrigerator-embraco-compressor.html",
    ],
    "embraco-egz80hlp": [
        "http://m.rfjcompressor.com/",
        "https://frigopartners.com/cold/compressor/compressor-fully-hermetic/aspera-embraco-compressors/",
        "https://qishanr.com/products/compressor-embraco-nt6220z",
    ],
}


def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "text/html,image/*,*/*"})
    with urllib.request.urlopen(req, timeout=timeout, context=_CTX) as r:
        return r.read()


def extract(html, base):
    out = []
    for pat in [r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)',
                r'data-src=["\']([^"\']+)', r'data-original=["\']([^"\']+)',
                r'"image"\s*:\s*"(https?://[^"]+)"',
                r'"(https?://[^"]+?\.(?:jpg|jpeg|png|webp))"',
                r'src=["\']([^"\']+\.(?:jpg|jpeg|png|webp))']:
        for m in re.finditer(pat, html, re.I):
            out.append(m.group(1))
    seen, res = set(), []
    for u in out:
        u = u.strip()
        if u.startswith("//"):
            u = "https:" + u
        if u.lower().startswith("http") and u not in seen:
            seen.add(u); res.append(u)
    return res


def ext_of(u, d):
    ul = u.lower()
    for e in ("jpg", "jpeg", "png", "webp"):
        if "." + e in ul:
            return "jpg" if e == "jpeg" else e
    if d[:3] == b"\xff\xd8\xff":
        return "jpg"
    if d[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    return None


def main():
    for slug, urls in TARGETS.items():
        dd = RAW / slug
        dd.mkdir(parents=True, exist_ok=True)
        n = 200
        for page in urls:
            try:
                html = fetch(page).decode("utf-8", "ignore")
            except Exception as e:
                print(f"[fail] {slug} {page} -> {e}")
                continue
            cand = extract(html, page)
            print(f"[page] {slug} {page} -> {len(cand)} refs")
            for cu in cand:
                try:
                    d = fetch(cu)
                except Exception:
                    continue
                if len(d) < 14000:
                    continue
                e = ext_of(cu, d)
                if not e:
                    continue
                fp = dd / f"n{n}.{e}"
                while fp.exists():
                    n += 1; fp = dd / f"n{n}.{e}"
                fp.write_bytes(d)
                print(f"   saved {fp.name} {len(d)//1024}KB <- {cu[:110]}")
                n += 1
                if n > 260:
                    break


if __name__ == "__main__":
    main()
