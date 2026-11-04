#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
海外压缩机站 — 全站一致性体检脚本
每次改完 tools/build_site.py 或 data/models.json 并重建后跑一遍：
    python tools/qa_check.py
脚本只报告，不改动任何文件。
"""
import os, re, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
DATA = os.path.join(ROOT, "data", "models.json")

CJK = re.compile(r"[\u4e00-\u9fff]")
FORBIDDEN = re.compile(
    r"before (ordering|installation|wiring|replacement|swapping|selecting)"
    r"|always confirm|confirm against the nameplate|check before ordering",
    re.I,
)
WARRANTY = re.compile(r"warranty|12 months", re.I)
LABEL = re.compile(r"private label|oem private label|one source|export-ready packing|cross-reference before shipping", re.I)

# 这些属于"待回填占位"，不是错误，只给 WARNING
PLACEHOLDER = {
    "accompressorhub.com": "占位域名（上线前换成真实域名）",
    "+861000000000": "占位电话（tel 链接）",
    "+8613800000000": "占位 WhatsApp 号",
    "sales@accompressorhub.com": "占位邮箱",
    "WeChat: accompressorhub": "占位微信号",
}

problems, warnings = [], []

def add(kind, where, detail):
    (problems if kind == "FAIL" else warnings).append(f"[{kind}] {where}: {detail}")

def check_html():
    htmls = glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True)
    if not htmls:
        add("FAIL", "site/", "没有任何生成的 HTML 页面，先跑 build_site.py")
        return
    for h in htmls:
        rel = os.path.relpath(h, SITE)
        t = open(h, encoding="utf-8").read()
        if CJK.search(t):
            add("FAIL", rel, "正文含中文字符（英文站零中文规则）")
        if FORBIDDEN.search(t):
            add("FAIL", rel, "残留'教买家确认'类提醒文案")
        if WARRANTY.search(t):
            add("FAIL", rel, "残留 warranty / 12 months（应改用 Quality check 口径）")
        if LABEL.search(t):
            add("FAIL", rel, "残留 private label / one source / export-ready packing 等已弃表述")
        if "<title>" in t and "Baizly" not in t:
            add("FAIL", rel, "title 未带 Baizly 品牌词")
        if rel == "index.html" and "hero-plate" in t:
            add("FAIL", rel, "hero 仍重复放置 LOGO（应只在页头）")
        for pat, msg in PLACEHOLDER.items():
            if pat in t:
                add("WARN", rel, f"占位数据：{pat}（{msg}）")
    # 死链检查
    for h in htmls:
        rel = os.path.relpath(h, SITE)
        base = os.path.dirname(h)
        t = open(h, encoding="utf-8").read()
        for m in re.findall(r'src="([^"]+)"', t):
            if m.startswith(("http://", "https://", "data:", "tel:", "mailto:", "wa.me", "t.me")):
                continue
            p = os.path.normpath(os.path.join(base, m))
            if not os.path.exists(p):
                add("FAIL", rel, f"图片缺失：{m}")
        for m in re.findall(r'href="([^"]+)"', t):
            if m.startswith(("http://", "https://", "mailto:", "tel:", "wa.me", "t.me", "#")):
                continue
            if m.endswith("/"):
                m += "index.html"
            p = os.path.normpath(os.path.join(base, m))
            if not os.path.exists(p):
                add("FAIL", rel, f"内链缺失：{m}")

def check_src():
    if not os.path.exists(DATA):
        return
    t = open(DATA, encoding="utf-8").read()
    if LABEL.search(t):
        add("FAIL", "data/models.json", "数据源残留已弃表述（private label / one source / export-ready packing）")
    if WARRANTY.search(t) and "Tested & inspected before dispatch" not in t:
        add("FAIL", "data/models.json", "数据源残留 warranty / 12 months")

def coverage():
    # 关键一致性计数（信息，不判 FAIL）
    htmls = glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True)
    ally = sum("most reliable ally in China" in open(h, encoding="utf-8").read() for h in htmls
               if "/models/" in h)
    qc = sum("Quality check" in open(h, encoding="utf-8").read() for h in htmls)
    lt = sum("Lead time (dispatch)" in open(h, encoding="utf-8").read() for h in htmls)
    print(f"  型号页 CTA(ally): {ally}/12 | Quality check 面板: {qc} 页 | Lead time(dispatch): {lt} 页")

def main():
    print("=== Baizly 全站体检 ===")
    check_html()
    check_src()
    coverage()
    print(f"\nFAIL: {len(problems)}  |  WARN(占位): {len(warnings)}")
    for p in problems:
        print("  " + p)
    for w in warnings:
        print("  " + w)
    if problems:
        print("\n结论：存在需修复的问题，修复后重跑。")
        sys.exit(1)
    else:
        print("\n结论：PASS —— 一致性规则全部通过（占位数据待你回填）。")
        sys.exit(0)

if __name__ == "__main__":
    main()
