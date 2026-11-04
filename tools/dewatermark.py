#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""去水印工具 (watermark remover)

背景：本站产品图一部分来自网络/二手平台，凡带水印的图**必须去水印后才能上线**（用户硬规则）。

用法：
  # 自动模式（识别"低饱和度的异常亮/暗细线"型文字/网址水印，再 inpaint 修补）
  python tools/dewatermark.py in.jpg out.jpg --mode auto

  # 指定水印偏亮 / 偏暗，调阈值
  python tools/dewatermark.py in.jpg out.jpg --mode bright --thresh 20 --strength 2

  # 手动蒙版（最可靠）：白色=要去掉的水印区域，黑色=保留。用画图/PS 涂一下即可
  python tools/dewatermark.py in.jpg out.jpg --mask mask.png

  # 只裁掉四周水印带（不修补）
  python tools/dewatermark.py in.jpg out.jpg --crop 60 60 60 60

局限：对"大面积、不透明贴片/大 Logo"水印效果一般，这种请用 --mask 或直接换图。
"""
import argparse
import sys

import cv2
import numpy as np


def build_auto_mask(img, mode="auto", thresh=18, sat_max=55, dilate=3):
    """自动估计水印蒙版：低饱和度 + 与局部背景差异明显的细线结构。"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    sat = hsv[:, :, 1].astype(np.int16)

    # 局部背景（中值滤波近似），diff>0 表示比周围亮，diff<0 表示比周围暗
    bg = cv2.medianBlur(gray, 31).astype(np.int16)
    diff = gray.astype(np.int16) - bg

    if mode == "bright":
        cand = (diff > thresh)
    elif mode == "dark":
        cand = (diff < -thresh)
    else:  # auto：亮暗都算
        cand = (np.abs(diff) > thresh)

    # 水印通常是中性灰/白（低饱和），借这个特征排除彩色产品细节
    cand &= (sat < sat_max)
    m = (cand.astype(np.uint8)) * 255

    # 去掉"大块"结构（产品本体/大色块），只保留细线（水印笔画）
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
    big = cv2.morphologyEx(m, cv2.MORPH_OPEN, k)
    big = cv2.dilate(big, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    thin = cv2.bitwise_and(m, cv2.bitwise_not(big))

    # 补回笔画宽度，避免留下残影
    if dilate > 0:
        thin = cv2.dilate(thin, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilate, dilate)))
    return thin


def main():
    ap = argparse.ArgumentParser(description="去水印（inpaint 修补）")
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--mode", choices=["auto", "bright", "dark"], default="auto")
    ap.add_argument("--thresh", type=int, default=18, help="与局部背景的灰度差阈值，越大去掉的越少")
    ap.add_argument("--sat-max", type=int, default=55, help="饱和度上限，越低越只认中性灰")
    ap.add_argument("--strength", type=int, default=2, help="膨胀强度 1-4，越大覆盖越狠")
    ap.add_argument("--mask", default=None, help="手动蒙版 png（白=去除）")
    ap.add_argument("--protect", nargs=4, type=int, action="append", metavar=("X0", "Y0", "X1", "Y1"),
                    help="保护区域，可重复。该矩形内不做去水印（如铭牌/标签区），避免误伤")
    ap.add_argument("--crop", nargs=4, type=int, metavar=("T", "B", "L", "R"),
                    help="先裁掉 上 下 左 右 边距（像素），再做后续处理")
    ap.add_argument("--debug-mask", default=None, help="把蒙版另存一份，方便检查")
    args = ap.parse_args()

    img = cv2.imread(args.src, cv2.IMREAD_COLOR)
    if img is None:
        print("ERROR: 读不到图片", args.src, file=sys.stderr)
        return 2

    if args.crop:
        t, b, l, r = args.crop
        h, w = img.shape[:2]
        img = img[t:h - b, l:w - r]

    if args.mask:
        mask = cv2.imread(args.mask, cv2.IMREAD_GRAYSCALE)
        if mask is None:
            print("ERROR: 读不到蒙版", args.mask, file=sys.stderr)
            return 2
        if mask.shape[:2] != img.shape[:2]:
            mask = cv2.resize(mask, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_NEAREST)
    else:
        dilate = {1: 1, 2: 3, 3: 5, 4: 7}.get(args.strength, 3)
        mask = build_auto_mask(img, args.mode, args.thresh, args.sat_max, dilate)

    # 保护区域：铭牌/标签这类关键区域不要去水印，避免误伤
    if args.protect:
        for x0, y0, x1, y1 in args.protect:
            mask[y0:y1, x0:x1] = 0

    if args.debug_mask:
        cv2.imwrite(args.debug_mask, mask)

    out = cv2.inpaint(img, mask, 4, cv2.INPAINT_TELEA)
    cv2.imwrite(args.dst, out, [cv2.IMWRITE_JPEG_QUALITY, 90])

    covered = float((mask > 0).mean()) * 100
    print(f"OK -> {args.dst}  (蒙版覆盖 {covered:.2f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
