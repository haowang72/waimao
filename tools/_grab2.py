import urllib.request, urllib.parse, re
from pathlib import Path

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
ROOT = Path("data/candidate_images/_raw")

TARGETS = {
    "embraco-ffi12hbk": [
        "https://www.hvacrcompressor.com/embraco-compressor",
        "https://www.slovklima.sk/en?p=17200",
        "https://product.11467.com/info/3022656.htm",
        "https://gzqszl.cn.china.cn/supply/5109388636.html",
        "https://www.china.cn/zhilengyasuoji/4040723003.html",
        "https://provide.biz72.com/apj01ewq.html",
    ],
    "embraco-egz80hlp": [
        "https://www.embracous.com/blog/embraco-egz-80hlp-compressor-what-a-buyer-learned-after-5-years-price-86.html",
        "https://www.hvacrcompressor.com/embraco-compressor",
        "https://www.slovklima.sk/en?p=17200",
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
                r'<img[^>]+data-original=["\']([^"\']+\.(?:jpg|jpeg|png|webp))',
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
    # start numbering after existing
    start = len([f for f in d.iterdir() if f.suffix.lower() in (".jpg",".png",".webp")])
    n = start
    for url in urls:
        try:
            html = fetch(url, url).decode("utf-8", "ignore")
        except Exception as e:
            print(f"[{slug}] PAGE ERR {url[:60]} -> {e}")
            continue
        cands = img_urls(html, url)
        print(f"[{slug}] {len(cands)} imgs from {url[:55]}")
        for u in cands[:10]:
            if n - start >= 10: break
            try:
                data = fetch(u, url)
            except Exception:
                continue
            if len(data) < 7000:
                continue
            if data[:3] == b"\xff\xd8\xff": ext = ".jpg"
            elif data[:8] == b"\x89PNG\r\n\x1a\n": ext = ".png"
            elif data[:4] == b"RIFF": ext = ".webp"
            else: continue
            p = d / f"{n+1}{ext}"
            p.write_bytes(data); n += 1
            print(f"   saved {p.name} {len(data)}B")
    print(f"== {slug}: {n-start} new ==")
print("DONE2")
