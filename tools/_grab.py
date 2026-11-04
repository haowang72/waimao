import urllib.request, urllib.parse, re, os
from pathlib import Path

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
ROOT = Path("data/candidate_images/_raw")
ROOT.mkdir(parents=True, exist_ok=True)

# (slug, [candidate page urls])
TARGETS = {
    "gmcc-ph135x1c-4p3": [
        "https://nbhicool.en.made-in-china.com/product/JEPRsLdGqVrg/China-New-Original-Gmcc-Brand-Rotary-Compressor-for-Air-Conditioner.html",
    ],
    "gmcc-ph150x1c-4p3": [
        "https://www.tradechina.com/Wholesale-electronic-components-Support-BOM-Quotation_240142528.html",
    ],
    "copeland-zp24k3e-pfj-522": [
        "https://www.hvacrworld.au/products/SEC-ZR24K3E-PFJ-522_item.html",
        "http://www.bjxydkj.com/a/products/cp1/gulunyasuoji/2021/1119/2051.html",
    ],
    "maneurop-mt64hm4": [
        "https://en.indotrading.com/tirisglobalindonesia/danfoss-maneurop-mt64-p124286.aspx",
    ],
    "embraco-ffi12hbk": [
        "https://m.made-in-china.com/product/Embraco-Aspera-Refrigerator-Compressor-R134A-Ffi12hbk-925436725.html",
        "https://www.refrigerationdevice.com/quality-9584167-1-3hp-embraco-aspera-compressor-ffi-12hbk",
    ],
    "embraco-egz80hlp": [
        "https://www.mbsm.pro/search/Compressor+rotary/page/3?print=print-search",
    ],
    "aspera-nek6213z": [
        "https://frigopartners.com/compressor-aspera-embraco-t6213z-hbp-r134a-220-240v-50hz-not-available-replaced-by-successor",
    ],
    "aspera-nek2134gk": [
        "https://elgracool.pl/product-eng-209-Compressor-ASPERA-NEK2134GK.html",
        "https://primasupply.com/parts/true/842513",
    ],
}

def fetch(url, ref=None, t=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en",
        "Accept": "text/html,image/*,*/*", **( {"Referer": ref} if ref else {})})
    return urllib.request.urlopen(req, timeout=t).read()

def img_urls(html, base):
    found = []
    for pat in [r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)',
                r'<img[^>]+src=["\']([^"\']+\.(?:jpg|jpeg|png|webp))',
                r'<img[^>]+data-src=["\']([^"\']+\.(?:jpg|jpeg|png|webp))',
                r'<img[^>]+data-lazy-src=["\']([^"\']+\.(?:jpg|jpeg|png|webp))',
                r'srcset=["\']([^"\']+)']:
        for m in re.findall(pat, html, re.I):
            if "srcset" in pat:
                for part in m.split(","):
                    u = part.strip().split()[0]
                    if u.endswith((".jpg", ".jpeg", ".png", ".webp")):
                        found.append(urllib.parse.urljoin(base, u))
            else:
                found.append(urllib.parse.urljoin(base, m))
    seen = set(); out = []
    for u in found:
        if u not in seen:
            seen.add(u); out.append(u)
    return out

for slug, urls in TARGETS.items():
    d = ROOT / slug
    d.mkdir(parents=True, exist_ok=True)
    n = 0
    for url in urls:
        try:
            html = fetch(url, url).decode("utf-8", "ignore")
        except Exception as e:
            print(f"[{slug}] PAGE ERR {url[:60]} -> {e}")
            continue
        cands = img_urls(html, url)
        print(f"[{slug}] {len(cands)} imgs from {url[:55]}")
        for u in cands[:12]:
            if n >= 8: break
            try:
                data = fetch(u, url)
            except Exception as e:
                continue
            if len(data) < 7000:
                continue
            if data[:3] == b"\xff\xd8\xff":
                ext = ".jpg"
            elif data[:8] == b"\x89PNG\r\n\x1a\n":
                ext = ".png"
            elif data[:4] in (b"RIFF",):
                ext = ".webp"
            else:
                continue
            p = d / f"{n+1}{ext}"
            p.write_bytes(data)
            n += 1
            print(f"   saved {p.name} {len(data)}B")
    print(f"== {slug}: {n} downloaded ==")
print("DONE")
