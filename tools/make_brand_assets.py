# -*- coding: utf-8 -*-
"""
品牌素材生成器（一次性/可重跑）
输入： site/assets/img/logo-horizontal.png  （商小白 横版 国际 LOGO，透明底）
输出：
  site/assets/img/favicon.png         96x96   从 LOGO 图形标裁剪的方形图标（深色底专用见 white 版）
  site/assets/img/favicon-white.png   96x96   （备用：深色底）
  site/assets/img/apple-touch-icon.png 180x180 白底方形图标
  site/assets/img/og-cover.png        1200x630 站点分享封面（无任何水印）
用法： python tools/make_brand_assets.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "site" / "assets" / "img"
LOGO = IMG / "logo-horizontal.png"

BRAND_EN = "Baizly"
BRAND_DESC = "China Second-Hand Compressor Recycling"
SITE_URL = "accompressorhub.com"
LOCATION = "Beijing, China"

FONT_BD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_RG = r"C:\Windows\Fonts\arial.ttf"
FONT_CN = r"C:\Windows\Fonts\msyh.ttc"
FONT_CN_BD = r"C:\Windows\Fonts\msyhbd.ttc"

BRAND_BLUE = (13, 63, 120)
BRAND_BLUE_2 = (26, 99, 196)
ACCENT = (242, 140, 30)
INK = (16, 26, 43)
MUTED = (107, 123, 146)
LINE = (228, 233, 240)


def mark_bbox(im):
    """定位 LOGO 左侧彩色图形标的包围盒（按饱和度找彩色像素）。"""
    rgba = im.convert("RGBA")
    w, h = rgba.size
    px = rgba.load()
    xs, ys = [], []
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 40:
                continue
            mx, mn = max(r, g, b), min(r, g, b)
            if mx > 60 and (mx - mn) > 55:      # 明显彩色 → 属于图形标
                xs.append(x)
                ys.append(y)
    if not xs:
        return (0, 0, int(w * 0.28), h)
    # 图形标在左侧，取左侧 40% 范围的结果
    cut = int(w * 0.42)
    xs = [x for x in xs if x <= cut]
    ys = [y for y in ys if y <= cut]
    if not xs:
        return (0, 0, int(w * 0.28), h)
    return (min(xs), min(ys), max(xs) + 1, max(ys) + 1)


def square_icon(src, size, bg=None, pad_ratio=0.14, out=None):
    box = mark_bbox(src)
    m = src.crop(box)
    inner = int(size * (1 - 2 * pad_ratio))
    m.thumbnail((inner, inner), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), bg if bg else (0, 0, 0, 0))
    canvas.paste(m, ((size - m.width) // 2, (size - m.height) // 2), m)
    canvas.save(out)
    return out, box


def draw_tracked(draw, xy, text, font, fill, tracking=0):
    """逐字绘制，模拟 letter-spacing。返回总宽度。"""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return x - xy[0]


def make_og():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)

    # 顶部品牌色条
    d.rectangle([0, 0, W, 10], fill=BRAND_BLUE)
    d.rectangle([0, 0, 320, 10], fill=ACCENT)
    # 底部浅色带
    d.rectangle([0, H - 96, W, H], fill=(245, 247, 250))
    d.line([0, H - 96, W, H - 96], fill=LINE, width=1)

    # LOGO
    logo = Image.open(LOGO).convert("RGBA")
    lw = 360
    logo2 = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    img.paste(logo2, ((W - logo2.width) // 2, 118), logo2)

    f_en = ImageFont.truetype(FONT_BD, 46)
    f_desc = ImageFont.truetype(FONT_RG, 24)
    f_cn = ImageFont.truetype(FONT_CN, 25)
    f_sm = ImageFont.truetype(FONT_RG, 20)

    # 品牌名
    tw = d.textlength(BRAND_EN, font=f_en)
    d.text(((W - tw) / 2, 304), BRAND_EN, font=f_en, fill=INK)
    # 英文描述
    dw = d.textlength(BRAND_DESC, font=f_desc)
    d.text(((W - dw) / 2, 372), BRAND_DESC, font=f_desc, fill=MUTED)
    # 分隔线
    d.line([(W - 120) / 2, 432, (W + 120) / 2, 432], fill=LINE, width=2)
    # 底部信息
    foot = f"{LOCATION}  ·  {SITE_URL}"
    fw = d.textlength(foot, font=f_sm)
    d.text(((W - fw) / 2, H - 58), foot, font=f_sm, fill=MUTED)

    out = IMG / "og-cover.png"
    img.save(out, optimize=True)
    return out


def main():
    src = Image.open(LOGO).convert("RGBA")
    box = mark_bbox(src)
    print("logo size:", src.size, "| mark bbox:", box)

    p1, _ = square_icon(src, 96, bg=None, out=IMG / "favicon.png")
    p2, _ = square_icon(src, 96, bg=(255, 255, 255, 255), out=IMG / "favicon-white.png")
    p3, _ = square_icon(src, 180, bg=(255, 255, 255, 255), out=IMG / "apple-touch-icon.png")
    p4 = make_og()

    for p in (p1, p2, p3, p4):
        print(f"  {p.name:<24} {p.stat().st_size // 1024:>4} KB")


if __name__ == "__main__":
    main()
