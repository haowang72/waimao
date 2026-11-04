# -*- coding: utf-8 -*-
"""
型号排队表进度看板
用法： python tools/pipeline_report.py
读 data/pipeline.csv，输出「已完成 / 待补参数 / 下一批该做谁」的统计。
"""
import csv
import pathlib

BASE = pathlib.Path(__file__).resolve().parent.parent
CSV = BASE / "data" / "pipeline.csv"

CAT_NAME = {
    "rotary": "Rotary 旋转式",
    "scroll": "Scroll 涡旋式",
    "reciprocating": "Hermetic 往复式",
    "other": "其他 / 候选池",
}


def load():
    with CSV.open(encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def main():
    rows = load()
    total = len(rows)
    done = [r for r in rows if r["params_status"] == "done"]
    pending = [r for r in rows if r["params_status"] == "pending"]
    hold = [r for r in rows if r["params_status"] == "hold"]

    print(f"排队总数：{total} 条 | 已入库 {len(done)} | 待补参数 {len(pending)} | 暂缓 {len(hold)}")
    print("完成度：%.1f%%" % (len(done) / total * 100))
    print()

    print("按品类：")
    for key, name in CAT_NAME.items():
        sub = [r for r in rows if r["category"] == key]
        d = len([r for r in sub if r["params_status"] == "done"])
        stars = sum(1 for r in sub if r["demand"] == "5")
        print(f"  {name:<18} 总 {len(sub):>2} 条｜已入库 {d:>2}｜高热度(demand=5) {stars:>2} 条")
    print()

    nxt = [r for r in pending if r["priority"] == "P0"]
    nxt.sort(key=lambda r: -int(r["demand"]))
    print("下一批建议（P0 未完成，按热度降序，前 12）：")
    for i, r in enumerate(nxt[:12], 1):
        print(f"  {i:>2}. [{r['brand']}] {r['model_or_range']:<28} {r['hp']:<8} {r['refrigerant']:<14} 需求{r['demand']} 确认度{r['confidence']}")
    print()

    noparam = [r for r in pending if r["confidence"] == "C"]
    print(f"确认度 C（需要先从实货/平台捞型号编号）的条数：{len(noparam)}")


if __name__ == "__main__":
    main()
