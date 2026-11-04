# -*- coding: utf-8 -*-
"""
图库初始化器
用法：
    python tools/build_placeholders.py          # 生成占位图 + 刷新配图计划表
    python tools/build_placeholders.py --check  # 只检查哪些型号还缺实物图

设计原则：占位图是**图纸风格的占位卡**，一眼看得出不是照片 ——
绝不生成"看起来像产品照片"的假图，那是在对外承诺你并不拥有的东西。
"""
import csv
import json
import pathlib
import sys
from PIL import Image, ImageDraw, ImageFont

BASE = pathlib.Path(__file__).resolve().parent.parent
DATA = BASE / "data"
IMGDIR = BASE / "site" / "assets" / "img" / "products"
W, H = 1200, 900

BG = (244, 247, 251)
GRID = (225, 233, 243)
FRAME = (180, 196, 216)
LINE = (88, 108, 134)
ACCENT = (13, 63, 120)
MUTED = (128, 145, 166)

FONT_DIR = pathlib.Path("C:/Windows/Fonts")


def font(name, size, bold_name=None):
    try:
        return ImageFont.truetype(str(FONT_DIR / name), size)
    except Exception:
        return ImageFont.truetype(str(FONT_DIR / (bold_name or "arial.ttf")), size)


def draw_body(d, cx, cy, category):
    """画一个极简示意轮廓：rotary/scroll 立式，reciprocating 卧式"""
    if category == "reciprocating":
        r = (cx - 190, cy - 110, cx + 190, cy + 110)
        d.rounded_rectangle(r, radius=105, outline=LINE, width=4)
        d.line((cx - 190, cy, cx + 190, cy), fill=GRID, width=2)
        # 管口
        d.ellipse((cx - 30, cy - 150, cx + 30, cy - 90), outline=LINE, width=4)
        d.rectangle((cx + 120, cy - 95, cx + 165, cy - 50), outline=LINE, width=4)
        # 底座
        d.rectangle((cx - 210, cy + 110, cx - 150, cy + 140), outline=LINE, width=3)
        d.rectangle((cx + 150, cy + 110, cx + 210, cy + 140), outline=LINE, width=3)
    else:
        top = cy - 210
        bot = cy + 190
        d.ellipse((cx - 150, top - 34, cx + 150, top + 34), outline=LINE, width=4)
        d.rectangle((cx - 150, top, cx + 150, bot), outline=LINE, width=4)
        d.arc((cx - 150, bot - 60, cx + 150, bot + 60), start=0, end=180, fill=LINE, width=4)
        # 端子盒
        d.rounded_rectangle((cx - 55, top - 120, cx + 55, top - 40), radius=10, outline=LINE, width=4)
        # 管路
        d.ellipse((cx + 90, top - 130, cx + 150, top - 70), outline=LINE, width=4)
        d.ellipse((cx - 30, bot - 130, cx + 30, bot - 70), outline=LINE, width=4)


def placeholder(m):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    for x in range(0, W, 40):
        d.line((x, 0, x, H), fill=GRID, width=1)
    for y in range(0, H, 40):
        d.line((0, y, W, y), fill=GRID, width=1)
    d.rectangle((24, 24, W - 24, H - 24), outline=FRAME, width=3)

    f_cat = font("arialbd.ttf", 26)
    f_brand = font("arialbd.ttf", 58)
    f_model = font("arial.ttf", 44)
    f_small = font("arial.ttf", 24)

    cat_label = {
        "rotary": "ROTARY COMPRESSOR",
        "scroll": "SCROLL COMPRESSOR",
        "reciprocating": "HERMETIC RECIPROCATING COMPRESSOR",
    }.get(m["category"], "COMPRESSOR")

    d.text((64, 62), cat_label, font=f_cat, fill=MUTED)
    draw_body(d, W // 2, H // 2 - 10, m["category"])
    d.text((64, H - 210), m["brand"].upper(), font=f_brand, fill=ACCENT)
    d.text((64, H - 145), m["model"], font=f_model, fill=LINE)
    d.text((64, H - 96), f"{m['hp']}  |  {m['refrigerant']}  |  {m['type']}", font=f_small, fill=MUTED)
    d.line((64, H - 74, W - 64, H - 74), fill=FRAME, width=2)
    d.text((64, H - 62), "Product photo pending — replace with real unit photo before launch",
           font=f_small, fill=(176, 92, 30))
    return img


def alt_text(m):
    kind = {
        "rotary": "rotary compressor",
        "scroll": "scroll compressor",
        "reciprocating": "hermetic reciprocating compressor",
    }.get(m["category"], "compressor")
    return f"{m['brand']} {m['model']} {kind}, {m['hp']} {m['refrigerant']} — wholesale supply"


def pipeline_rows():
    rows = []
    with (DATA / "pipeline.csv").open(encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows


def main():
    check_only = "--check" in sys.argv
    model_meta = json.loads((DATA / "models.json").read_text(encoding="utf-8"))
    models = model_meta["models"]
    IMGDIR.mkdir(parents=True, exist_ok=True)

    if check_only:
        missing = []
        for m in models:
            real = IMGDIR / (m["slug"] + "-1.jpg")
            if not real.exists():
                missing.append((m["brand"], m["model"]))
        print(f"型号总数 {len(models)}｜缺实物图 {len(missing)} 个（当前页面显示占位卡）")
        for b, mo in missing[:40]:
            print(f"  [pending]  {b} {mo}")
        return

    made = 0
    for m in models:
        # 占位图独立文件名，实拍图用 <slug>-1.jpg 同名覆盖即可自动接管，不会误判、也不需要删除占位图
        target = IMGDIR / (m["slug"] + "-placeholder.jpg")
        placeholder(m).save(target, quality=86, optimize=True)
        made += 1
    print(f"占位卡已生成 {made} 张 -> site/assets/img/products/  (实拍图命名规则：<slug>-1.jpg)")

    plan_path = DATA / "image_plan.csv"
    rows = pipeline_rows()
    done_slugs = {m["slug"]: m for m in models}
    with plan_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["priority", "brand", "model", "category", "file_front", "file_side",
                    "file_nameplate", "alt_text", "source_plan", "status"])
        for r in rows:
            slug = r["model_or_range"].lower().replace(" ", "-").replace("/", "-")
            slug = "".join(ch for ch in slug if ch.isalnum() or ch == "-").strip("-") or "unsorted"
            alt = f"{r['brand']} {r['model_or_range']} compressor, {r['hp']} {r['refrigerant']} — wholesale supply"
            if slug in done_slugs:
                status = "page_live / photo pending"
                source = "self-shot batch (recommended)"
            elif r["params_status"] == "hold":
                status = "on hold"
                source = "not started"
            else:
                status = "queued"
                source = "self-shot batch (recommended)"
            w.writerow([r["priority"], r["brand"], r["model_or_range"], r["category"],
                        f"{slug}-1.jpg", f"{slug}-2.jpg", f"{slug}-3.jpg",
                        alt, source, status])
    print(f"配图计划表已刷新 -> {plan_path} ({len(rows)} 行)")
    print()
    print("下一步：把实拍图按同名覆盖放进 site/assets/img/products/，再跑 python tools/build_site.py 即可自动挂上")


if __name__ == "__main__":
    main()
