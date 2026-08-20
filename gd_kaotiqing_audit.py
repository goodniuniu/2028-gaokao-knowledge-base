#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gd_kaotiqing_audit.py — 广东考情标注现状审计
============================================
提取每张知识卡片的「广东考情」字段，按精确化程度分类：
  A 已锚定真题：同时含 年份(20xx) + 题号(Txx/第xx题/Qxx)
  B 含年份无题号：含 20xx 但无具体题号
  C 含频率无年份：含 高频/中频/低频/常考 等但无 20xx
  D 笼统/未填：其他（含模板占位、空）
输出整体与分维度分布，并列出各维度"需升级(B/C/D)"的卡片原文，供精确化参考。
"""
import re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).parent
SUBJECTS = ["语文", "数学", "英语", "物理", "化学", "生物", "方法"]
DIMS = ["核心知识网络", "典型题型与方法", "易错警示与辨析", "素材与拓展",
        "学习方法", "考试策略", "心理建设", "生理管理"]
EXCLUDE_NAMES = {"index.md"}
EXCLUDE_PREFIX = ("索引_",)
REPORT = ROOT / "复盘追踪" / "_gd_kaotiqing_audit.txt"

YEAR = re.compile(r"20\d{2}")
QNUM = re.compile(r"(T\d{1,2}|第\d+题|Q\d{1,2}|题号\s*\d*)")
FREQ = re.compile(r"高频|中频|低频|常考|未考|偶考|必考")


def field(text, name):
    m = re.search(r"\|\s*\*\*" + name + r"\*\*\s*\|\s*(.+?)\s*\|", text)
    return m.group(1).strip() if m else ""


def classify(v):
    has_y = bool(YEAR.search(v))
    has_q = bool(QNUM.search(v))
    if has_y and has_q:
        return "A"
    if has_y and not has_q:
        return "B"
    if not has_y and FREQ.search(v):
        return "C"
    return "D"


def main():
    rows = []
    for subject in SUBJECTS:
        sdir = ROOT / subject
        if not sdir.exists():
            continue
        for md in sorted(sdir.rglob("*.md")):
            rel = md.relative_to(ROOT)
            if "单词复习" in rel.parts:
                continue
            if md.name in EXCLUDE_NAMES or md.name.startswith(EXCLUDE_PREFIX):
                continue
            text = md.read_text(encoding="utf-8")
            v = field(text, "广东考情")
            dim = rel.parts[1] if len(rel.parts) > 2 else "(根)"
            rows.append((subject, dim, md, v, classify(v)))

    # 分布
    from collections import defaultdict
    by_dim = defaultdict(lambda: {"A": 0, "B": 0, "C": 0, "D": 0, "total": 0})
    for subject, dim, md, v, c in rows:
        if dim in DIMS:
            by_dim[dim][c] += 1
            by_dim[dim]["total"] += 1

    L = []
    L.append("=" * 78)
    L.append("广东考情标注现状审计")
    L.append("=" * 78)
    total = len(rows)
    a = sum(1 for *_ , c in rows if c == "A")
    b = sum(1 for *_ , c in rows if c == "B")
    cc = sum(1 for *_ , c in rows if c == "C")
    d = sum(1 for *_ , c in rows if c == "D")
    L.append(f"卡片总数: {total}  |  A已锚定:{a}  B年份无题号:{b}  C频率无年份:{cc}  D笼统/未填:{d}")
    L.append("")
    L.append("分维度分布（仅六科四维）：")
    for dim in DIMS[:4]:
        s = by_dim[dim]
        L.append(f"  {dim}: 总{s['total']}  A{s['A']} B{s['B']} C{s['C']} D{s['D']}")
    L.append("")
    L.append("典型题型与方法 维度 — 需升级(B/C/D)清单：")
    for subject, dim, md, v, c in rows:
        if dim == "典型题型与方法" and c != "A":
            L.append(f"  [{c}] {md.relative_to(ROOT)}")
            L.append(f"       现状: {v[:80]}")
    L.append("")
    L.append("核心知识网络 维度 — 需升级(B/C/D)清单（抽样前20）：")
    cnt = 0
    for subject, dim, md, v, c in rows:
        if dim == "核心知识网络" and c != "A":
            L.append(f"  [{c}] {md.relative_to(ROOT)}")
            L.append(f"       现状: {v[:80]}")
            cnt += 1
            if cnt >= 20:
                break
    REPORT.write_text("\n".join(L), encoding="utf-8")

    print("=" * 64)
    print(f"广东考情审计：卡片 {total} 张")
    print(f"  A 已锚定年份+题号: {a}")
    print(f"  B 含年份无题号:    {b}")
    print(f"  C 含频率无年份:    {cc}")
    print(f"  D 笼统/未填:       {d}")
    print("=" * 64)
    for dim in DIMS[:4]:
        s = by_dim[dim]
        print(f"  {dim}: 总{s['total']}  A{s['A']} B{s['B']} C{s['C']} D{s['D']}")
    print("=" * 64)
    print(f"详细清单: {REPORT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
