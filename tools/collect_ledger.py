#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图文采集台账工具（二手平台来源通道）

流程：
  1. 从闲鱼 / 转转 / 闲转等平台截图或保存图片，按型号命名丢进 data/candidate_images/
     命名建议：<slug>-1.jpg / <slug>-2.jpg（如 gmcc-ph150x1c-4p3-1.jpg）
     系列页可用 <slug>.jpg（如 gmcc-ph-series.jpg）
  2. 运行本脚本：自动登记新图到 ledger.csv（状态=待审），并识别型号
  3. 你在 ledger.csv 里把确认可用的行 review_status 改成「已核」，填上 source_url / caption_cn
  4. 再跑一次本脚本：已核且图片存在的行，自动复制到 site/assets/img/<slug>-1.jpg
     （生成器 figure() 会优先用这张真图，占位框自动失效）
  5. 跑 tools/build_site.py 重建整站

绝不会自动把未审核的图上线 —— 只有 review_status=已核 才会被推进 site/。
"""
import csv, json, pathlib, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CAND = DATA / "candidate_images"
SITE_IMG = ROOT / "site" / "assets" / "img"
LEDGER = CAND / "ledger.csv"
MODELS = json.loads((DATA / "models.json").read_text(encoding="utf-8"))["models"]
SLUGS = {m["slug"]: m for m in MODELS}
IMG_EXTS = (".jpg", ".jpeg", ".png", ".webp")

HEADER = ["slug","brand","model","source_platform","source_url","image_file",
          "caption_cn","collected_at","review_status","risk_note","target"]


def load_ledger():
    if not LEDGER.exists():
        return [], {}
    rows = list(csv.DictReader(LEDGER.read_text(encoding="utf-8").strip().splitlines()))
    return rows, {r["slug"]: r for r in rows}


def infer_slug(fname):
    low = fname.lower()
    for slug in SLUGS:
        if slug.lower() in low:
            return slug
    return None


def main():
    promote = "--promote" in sys.argv
    rows, by_slug = load_ledger()
    if not rows:
        rows = [dict(zip(HEADER, [s, SLUGS[s]["brand"], SLUGS[s]["model"], "", "", "",
                                  "", "2026-10-15", "待采集", "", "models/" + s + ".html"]))
                for s in SLUGS]
        by_slug = {r["slug"]: r for r in rows}

    # 1) 登记候选目录里的新图
    newly = []
    if CAND.exists():
        for f in sorted(CAND.iterdir()):
            if f.suffix.lower() not in IMG_EXTS:
                continue
            slug = infer_slug(f.name)
            if not slug:
                print("  [跳过] 无法识别型号:", f.name)
                continue
            row = by_slug.setdefault(slug, dict(zip(HEADER,
                [slug, SLUGS[slug]["brand"], SLUGS[slug]["model"], "", "", "",
                 "", "2026-10-15", "待审", "", "models/" + slug + ".html"])))
            if not row.get("image_file"):
                row["image_file"] = f.name
                row["review_status"] = row.get("review_status") or "待审"
                if row["review_status"] == "待采集":
                    row["review_status"] = "待审"
                newly.append(f.name)

    # 2) 推进已核图片到 site/
    promoted = []
    if promote:
        for r in rows:
            if r.get("review_status") == "已核" and r.get("image_file"):
                src = CAND / r["image_file"]
                if src.exists():
                    dst = SITE_IMG / (r["slug"] + "-1.jpg")
                    shutil.copy(src, dst)
                    promoted.append(r["slug"])

    # 写回 ledger
    LEDGER.write_text("", encoding="utf-8")
    with LEDGER.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=HEADER)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in HEADER})

    # 汇总
    stat = {}
    for r in rows:
        stat[r.get("review_status", "")] = stat.get(r.get("review_status", ""), 0) + 1
    print("台账总行:", len(rows), "| 状态:", stat)
    if newly:
        print("本次新登记图片:", newly)
    if promoted:
        print("已推进 site/ 的图片:", promoted)
    pending = [r["slug"] for r in rows if r.get("review_status") in ("待采集", "待审")]
    print("待处理型号数:", len(pending))
    if pending:
        print("  待处理:", ", ".join(pending))


if __name__ == "__main__":
    main()
