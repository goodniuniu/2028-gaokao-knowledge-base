#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_backlinks.py — 关联卡片引用完整性检测
============================================
扫描全库知识卡片的「关联卡片」链接，构建有向引用图，区分四类问题：
  1) 真断链：链接目标在库内无任何同名卡片文件
  2) 路径写法不规范：库内存在该文件，但链接写法不是"相对源卡目录"的正确路径
                       （如跨目录只写文件名、或写了从仓库根起算的路径）→ 可机械修正
  3) 单向引用：A→B（路径正确）但 B 的关联卡片中无指向 A 的链接
  4) 自引用：A→A

用法：
    python check_backlinks.py                # 仅检测，生成报告
    python check_backlinks.py --fix-paths    # 自动修正"路径写法不规范"的链接（可逆，git 可回溯）
详细报告写入 复盘追踪/_backlinks_report.txt；控制台仅打印汇总。
退出码：存在真断链返回 1；否则 0（路径不规范 / 单向引用仅作软提示，不卡 CI）。
"""
import os, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent
SUBJECTS = ["语文", "数学", "英语", "物理", "化学", "生物", "方法"]
EXCLUDE_NAMES = {"index.md"}
EXCLUDE_PREFIX = ("索引_",)
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
HEAD_RE = re.compile(r"^#\s+(.+)$", re.M)
REPORT = ROOT / "复盘追踪" / "_backlinks_report.txt"


def parse_card(path: Path):
    """返回 (标题, [(链接名, 原始target), ...]) —— 仅「关联卡片」段落内的链接。"""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")
    title_m = HEAD_RE.search(text)
    title = title_m.group(1).strip() if title_m else path.stem
    m = re.search(r"^##\s+关联卡片\s*$.*?(?=^##\s|\Z)", text, re.S | re.M)
    links = []
    if m:
        for name, target in LINK_RE.findall(m.group(0)):
            links.append((name.strip(), target.strip()))
    return title, links


def build_index():
    """basename -> 绝对路径（文件名全局唯一）；同时返回卡片绝对路径列表。"""
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
            abs_p = md.resolve()
            index.setdefault(md.name, abs_p)
            cards.append(abs_p)
    return index, cards


def correct_rel(src_md: Path, dst: Path) -> str:
    return os.path.relpath(str(dst), str(src_md.parent)).replace("\\", "/")


def main():
    index, cards = build_index()
    title_of = {p: parse_card(p)[0] for p in cards}

    edges = []          # (src_abs, dst_abs, src_md, dst_name, raw_target_or_"")
    broken, self_ref = [], []

    for md in cards:
        abs_p = md.resolve()
        _, links = parse_card(md)
        for name, target in links:
            if target.startswith("http") or target.startswith("#"):
                continue
            t = target.replace("\\", "/")
            candidate = (md.parent / t).resolve()
            style_issue = False
            if candidate.exists() and candidate.suffix == ".md":
                dst = candidate
            else:
                base = t.rsplit("/", 1)[-1]
                dst = index.get(base)          # 全库文件名回退匹配
                if dst is None:
                    broken.append((md, name, target))
                    continue
                style_issue = True
            if dst == abs_p:
                self_ref.append((md, name))
                continue
            edges.append((abs_p, dst, md, name, target if style_issue else ""))

    out_adj = {p: set() for p in cards}
    for s, d, _, _, _ in edges:
        out_adj[s].add(d)

    style_issues = [(s, d, md, name, raw) for (s, d, md, name, raw) in edges if raw]
    one_way = []
    for s, d, md, name, raw in edges:
        if not raw and s not in out_adj[d]:     # raw=="" 表示路径正确
            suggestion = correct_rel(d, s)
            one_way.append((md, name, d, suggestion))
    two_way = len(edges) - len(style_issues) - len(one_way)

    # ---------- 写详细报告 ----------
    L = []
    L.append("=" * 78)
    L.append("关联卡片引用完整性检测报告")
    L.append("=" * 78)
    L.append(f"扫描卡片: {len(cards)} | 有效链接: {len(edges)}")
    L.append(f"真断链: {len(broken)} | 路径写法不规范: {len(style_issues)} | "
             f"单向引用(路径正确): {len(one_way)} | 双向: {two_way} | 自引用: {len(self_ref)}")
    L.append("")
    L.append("一、真断链（库内无同名文件，需手动确认目标卡片是否存在）")
    L.append(f"共 {len(broken)} 条")
    for md, name, target in broken:
        L.append(f"  ❌ {md.relative_to(ROOT)}  →  [{name}]({target})")
    L.append("")
    L.append("二、路径写法不规范（库内存在目标文件，应改为相对源卡目录的正确路径）")
    L.append(f"共 {len(style_issues)} 条")
    for s, d, md, name, raw in style_issues:
        L.append(f"  ~ {md.relative_to(ROOT)}")
        L.append(f"      原: [{name}]({raw})")
        L.append(f"      改: [{name}]({correct_rel(md, d)})")
    L.append("")
    L.append("三、单向引用（路径正确，但目标卡未反向链回，建议补充反向链接）")
    L.append(f"共 {len(one_way)} 条")
    for md, name, d, sug in one_way:
        L.append(f"  → {md.relative_to(ROOT)}")
        L.append(f"      链到 [{name}]({d.relative_to(ROOT)})")
        L.append(f"      建议 B 补充: - [{title_of[md.resolve()]}]({sug})")
    L.append("")
    L.append("四、自引用（A→A，通常无意义）")
    L.append(f"共 {len(self_ref)} 条")
    for md, name in self_ref:
        L.append(f"  ⚠️ {md.relative_to(ROOT)}  →  [{name}]")
    REPORT.write_text("\n".join(L), encoding="utf-8")

    # ---------- 自动修复路径写法不规范 ----------
    if "--fix-paths" in sys.argv:
        fixed = 0
        for s, d, md, name, raw in style_issues:
            corr = correct_rel(md, d)
            text = md.read_text(encoding="utf-8")
            for cand in (raw, raw.replace("\\", "/")):
                old = f"]({cand})"
                if old in text:
                    md.write_text(text.replace(old, f"]({corr})"), encoding="utf-8")
                    fixed += 1
                    break
        print(f"[--fix-paths] 已自动修正路径写法不规范的链接 {fixed} 条（可逆，git 可回溯）。")
        print(f"详细报告: {REPORT.relative_to(ROOT)}")
        return 0

    # ---------- 控制台汇总 ----------
    print("=" * 64)
    print(f"关联卡片检测：扫描卡片 {len(cards)} 张，有效链接 {len(edges)} 条")
    print("=" * 64)
    print(f"  真断链（库内无文件）:        {len(broken)}")
    print(f"  路径写法不规范（可修正）:    {len(style_issues)}")
    print(f"  单向引用（路径正确）:        {len(one_way)}")
    print(f"  双向引用（健康）:            {two_way}")
    print(f"  自引用:                      {len(self_ref)}")
    print("=" * 64)
    print(f"详细报告已写入: {REPORT.relative_to(ROOT)}")
    if broken:
        print("结论：存在真断链，需修复。❌")
        return 1
    print("结论：无真断链（路径不规范/单向引用为软提示）。✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
