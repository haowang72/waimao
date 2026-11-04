# -*- coding: utf-8 -*-
"""Sixth grab: hunt an exact Embraco EGZ80HLP product photo."""
import re, ssl, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "candidate_images" / "_raw"
_CTX = ssl.create_default_context(); _CTX.check_hostname = False; _CTX.verify_mode = ssl.CERT_NONE
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

PAGES = [
    "https://frigopartners.com/search?search=EGZ80HLP",
    "https://frigopartners.com/search?search=EGZ",
    "https://frigopartners.com/cold/compressor/compressor-fully-hermetic/aspera-embraco-compressors/?p=2",
]


def fetch(u, t=25):
    req = urllib.request.Request(u, headers={"User-Agent": UA, "Accept": "text/html,image/*,*/*"})
    with urllib.request.urlopen(req, timeout=t, context=_CTX) as r:
        return r.read()


def main():
    dd = RAW / "embraco-egz80hlp"
    dd.mkdir(parents=True, exist_ok=True)
    n = 300
    for page in PAGES:
        try:
            html = fetch(page).decode("utf-8", "ignore")
        except Exception as e:
            print(f"[fail] {page} -> {e}")
            continue
        urls = set()
        for pat in [r'"(https?://[^"]+?\.(?:jpg|jpeg|png|webp))"',
                    r'data-src=["\']([^"\']+)',
                    r'src=["\']([^"\']+\.(?:jpg|jpeg|png|webp))']:
            for m in re.finditer(pat, html, re.I):
                urls.add(m.group(1))
        # also pick product-code filenames mentioning egz / embraco / aspesa
        print(f"[page] {page} -> {len(urls)} urls")
        for u in sorted(urls):
            low = u.lower()
            if not any(k in low for k in ("egz", "embraco", "aspera", "verdichter", "/media/")):
                continue
            try:
                d = fetch(u)
            except Exception:
                continue
            if len(d) < 14000:
                continue
            ext = "png" if d[:8] == b"\x89PNG\r\n\x1a\n" else "jpg"
            fp = dd / f"e{n}.{ext}"
            while fp.exists():
                n += 1; fp = dd / f"e{n}.{ext}"
            fp.write_bytes(d)
            print(f"   saved {fp.name} {len(d)//1024}KB <- {u[:120]}")
            n += 1
            if n > 340:
                return


if __name__ == "__main__":
    main()
