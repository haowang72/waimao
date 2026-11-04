# -*- coding: utf-8 -*-
"""Extract embedded images from product catalog PDFs into _raw/<slug>/ with a 'pdf' prefix."""
import sys, io, ssl, urllib.request
from pathlib import Path
import pymupdf

_CTX = ssl.create_default_context()
_CTX.check_hostname = False
_CTX.verify_mode = ssl.CERT_NONE

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "candidate_images" / "_raw"
TMP = ROOT / "data" / "candidate_images" / "_pdf"
TMP.mkdir(parents=True, exist_ok=True)

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

JOBS = [
    ("maneurop-mt64hm4", "https://www.saginomiya.co.jp/sanki/products/circuit/MT-MTZ.pdf"),
    ("maneurop-mt64hm4", "https://www.cantas.com/urunpdf/Danfoss_MT_MTZ_NTZ_Urun_Kilavuzu.pdf"),
    ("maneurop-mt64hm4", "https://inter-thermo.hu/storage/catalog/files/MTZ-katalogus.pdf"),
]


def dl(url):
    fn = TMP / (url.split("/")[-1] or "doc.pdf")
    if not fn.exists():
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60, context=_CTX) as r:
            fn.write_bytes(r.read())
    return fn


def main():
    for slug, url in JOBS:
        try:
            pdf = dl(url)
        except Exception as e:
            print(f"[dl-fail] {url} -> {e}")
            continue
        dd = RAW / slug
        dd.mkdir(parents=True, exist_ok=True)
        doc = pymupdf.open(pdf)
        cnt = 0
        for pno in range(len(doc)):
            for img in doc[pno].get_images(full=True):
                xref = img[0]
                try:
                    d = doc.extract_image(xref)
                except Exception:
                    continue
                data = d["image"]
                if len(data) < 45000:            # product photos are usually bigger
                    continue
                if min(d["width"], d["height"]) < 200:
                    continue
                fp = dd / f"pdf_p{pno+1}_{xref}.{d['ext']}"
                fp.write_bytes(data)
                print(f"{slug}: {fp.name}  {len(data)//1024}KB  {d['width']}x{d['height']}")
                cnt += 1
        print(f"[{slug}] from {pdf.name}: {cnt} images")


if __name__ == "__main__":
    main()
