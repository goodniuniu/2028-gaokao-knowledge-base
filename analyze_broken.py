#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""analyze_broken.py — 仅分析 64 条真断链的性质，不改动任何文件。
分类：
  TYPE_X_prefix : 目标 basename 是某张已有卡的「后缀」（链接漏写 时间标签_科目_维度_ 前缀）
  TYPE_X_topic  : 去掉 时间标签/科目/维度 前缀后，主题词与某张已有卡一致（疑似改名）
  TYPE_Y        : 库内无任何匹配 -> 目标卡真缺失（需建卡或删链）
"""
import os, re
from pathlib import Path

ROOT = Path(__file__).parent
SUBJECTS = ["语文", "数学", "英语", "物理", "化学", "生物", "方法"]
EXCLUDE_NAMES = {"index.md"}
EXCLUDE_PREFIX = ("索引_",)
LINK_RE = re.compile(r"-\s*\[([^\]]+)\]\(([^)]+)\)")
HEAD_RE = re.compile(r"^#\s+(.+)$", re.M)

STRIP = ["高一筑基_", "高二深化_", "高三冲刺_", "方法_",
         "语文_", "数学_", "英语_", "物理_", "化学_", "生物_",
         "核心知识网络_", "典型题型与方法_", "易错警示与辨析_", "素材与拓展_"]

def norm(name: str) -> str:
    n = name
    for p in STRIP:
        if n.startswith(p):
            n = n[len(p):]
    return n

def parse_card(path: Path):
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^##\s+关联卡片\s*$.*?(?=^##\s|\Z)", text, re.S | re.M)
    links = []
    if m:
        for name, target in LINK_RE.findall(m.group(0)):
            links.append((name.strip(), target.strip()))
    return links

def build_index():
    index, cards = {}, []
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
            index.setdefault(md.name, md.resolve())
            cards.append(md.resolve())
    return index, cards

def main():
    index, cards = build_index()
    # 反向：suffix -> [basename]，norm_topic -> [basename]
    suffix_map, topic_map = {}, {}
    for bn in index:
        topic_map.setdefault(norm(bn[:-3]), []).append(bn)
        # 也用去掉时间/科目/维度后剩余的全部作为模糊键
    # 直接遍历卡片找断链
    broken = []
    for md in cards:
        for name, target in parse_card(md):
            if target.startswith("http") or target.startswith("#"):
                continue
            t = target.replace("\\", "/")
            cand = (md.parent / t).resolve()
            if cand.exists() and cand.suffix == ".md":
                continue
            base = t.rsplit("/", 1)[-1]
            if base in index:
                continue
            broken.append((md, name, base))

    type_x_prefix, type_x_topic, type_y = [], [], []
    for md, name, base in broken:
        topic = norm(base[:-3]) if base.endswith(".md") else norm(base)
        # TYPE_X_prefix: 已有卡 basename 以 base 结尾（base 不含 .md 时补）
        bkey = base[:-3] if base.endswith(".md") else base
        pref_matches = [bn for bn in index if bn[:-3].endswith(bkey)]
        topic_matches = [bn for bn, tops in topic_map.items() if topic and topic == bn]
        # 排除 base 自身显然不等
        if pref_matches:
            type_x_prefix.append((md, name, base, pref_matches))
        elif topic_matches:
            type_x_topic.append((md, name, base, topic_matches))
        else:
            type_y.append((md, name, base))

    print(f"真断链总数: {len(broken)}")
    print(f"  TYPE_X_prefix (漏前缀,可改链): {len(type_x_prefix)}")
    print(f"  TYPE_X_topic  (疑似改名,可改链): {len(type_x_topic)}")
    print(f"  TYPE_Y        (真缺失,需建卡/删链): {len(type_y)}")
    print()
    print("=== TYPE_X_prefix (漏写时间标签_科目_维度_前缀) ===")
    for md, name, base, m in type_x_prefix:
        print(f"  {md.relative_to(ROOT)}")
        print(f"      [{name}]({base})  ->  候选: {m}")
    print()
    print("=== TYPE_X_topic (主题一致,疑似改名) ===")
    for md, name, base, m in type_x_topic:
        print(f"  {md.relative_to(ROOT)}")
        print(f"      [{name}]({base})  ->  候选: {m}")
    print()
    print("=== TYPE_Y (库内无匹配,目标真缺失) ===")
    for md, name, base in type_y:
        print(f"  {md.relative_to(ROOT)}  ->  [{name}]({base})")

if __name__ == "__main__":
    main()
