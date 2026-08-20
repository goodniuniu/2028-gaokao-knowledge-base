#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_backlinks_phase2.py — 2.3 余量修复（安全机械部分）
1) TYPE_X 真断链改链：目标卡实际存在，仅链接名（前缀/时间标签）写法不对 -> 改为正确全名+正确相对路径
2) 461 条单向引用 -> 双向：在目标卡「关联卡片」段补一条反向链接
TYPE_Y（目标卡真缺失）不动，留给用户决策。
全程可逆（git 可回溯）。运行前建议 git status 干净。
"""
import os, re, sys
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

sys.stdout.reconfigure(encoding="utf-8")

def norm(name: str) -> str:
    n = name
    for p in STRIP:
        if n.startswith(p):
            n = n[len(p):]
    return n

def parse_card(path: Path):
    text = path.read_text(encoding="utf-8")
    title_m = HEAD_RE.search(text)
    title = title_m.group(1).strip() if title_m else path.stem
    m = re.search(r"^##\s+关联卡片\s*$.*?(?=^##\s|\Z)", text, re.S | re.M)
    links = []
    if m:
        for name, target in LINK_RE.findall(m.group(0)):
            links.append((name.strip(), target.strip()))
    return title, links

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

def correct_rel(src_md: Path, dst: Path) -> str:
    return os.path.relpath(str(dst), str(src_md.parent)).replace("\\", "/")

def title_of_path(p, cache):
    if p not in cache:
        cache[p] = parse_card(p)[0]
    return cache[p]

def append_reverse_link(dst_md: Path, src_md: Path, src_title: str, cache):
    """在 dst_md 的「关联卡片」段末尾追加一条指向 src_md 的反向链接；无该段则新建。"""
    rel = correct_rel(dst_md, src_md)
    new_line = f"- [{src_title}]({rel})"
    text = dst_md.read_text(encoding="utf-8")
    # 精确去重：仅当"该反向链接本身"已存在时才跳过（避免误判正文提及源卡名）
    if f"]({rel})" in text:
        return False
    sec = re.search(r"(^##\s+关联卡片\s*$.*?)(?=^##\s|\Z)", text, re.S | re.M)
    if sec:
        body = sec.group(1)
        insert_at = sec.end()
        # 段内末尾（去掉尾部空白）后追加
        prefix = "" if body.rstrip().endswith("\n") else "\n"
        text = text[:insert_at] + prefix + new_line + "\n" + text[insert_at:]
    else:
        sep = "\n\n" if text.rstrip() else ""
        text = text.rstrip() + sep + "\n## 关联卡片\n\n" + new_line + "\n"
    dst_md.write_text(text, encoding="utf-8")
    return True

def main():
    index, cards = build_index()
    title_cache = {}
    # norm_topic -> [basename]
    topic_map = {}
    for bn in index:
        topic_map.setdefault(norm(bn[:-3]), []).append(bn)

    edges = []          # (src_abs, dst_abs, src_md, dst_name, raw_or_"")
    broken = []
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
                dst = index.get(base)
                if dst is None:
                    broken.append((md, name, target))
                    continue
                style_issue = True
            if dst == abs_p:
                continue
            edges.append((abs_p, dst, md, name, target if style_issue else ""))

    # out_adj
    out_adj = {p: set() for p in cards}
    for s, d, _, _, _ in edges:
        out_adj[s].add(d)

    # ---- 1) TYPE_X 真断链改链 ----
    fixed_x = 0
    report_x = []
    for md, name, target in broken:
        t = target.replace("\\", "/")
        base = t.rsplit("/", 1)[-1]
        bkey = base[:-3] if base.endswith(".md") else base
        topic = norm(bkey)
        # 候选：basename 以 bkey 结尾（漏前缀）
        pref = [bn for bn in index if bn[:-3].endswith(bkey) and bn != base]
        # 候选：归一化主题一致（疑似改名/时间标签错）
        topic_cands = topic_map.get(topic, [])
        cand_bn = None
        if pref:
            cand_bn = pref[0]
        elif topic_cands:
            # 选首个匹配（如有多个取时间标签最匹配的）
            cand_bn = topic_cands[0]
        if not cand_bn:
            continue
        dst = index[cand_bn]
        corr = correct_rel(md, dst)
        # 只替换 target 部分（保留原链接文字）
        text = md.read_text(encoding="utf-8")
        old = f"]({target})"
        if old in text:
            md.write_text(text.replace(old, f"]({corr})"), encoding="utf-8")
            fixed_x += 1
            report_x.append(f"  ✅ {md.relative_to(ROOT)}\n      [{name}]({target}) -> ({corr})")

    # ---- 2) 单向 -> 双向 ----
    added = 0
    for s, d, md, name, raw in edges:
        if raw:
            continue  # 路径不规范（已在上轮 --fix-paths 处理，这里不再动）
        if s in out_adj[d]:
            continue
        if append_reverse_link(d, s, title_of_path(s, title_cache), title_cache):
            added += 1

    print(f"TYPE_X 改链: {fixed_x} 条")
    for r in report_x:
        print(r)
    print(f"单向->双向 补反向链接: {added} 条")
    print("TYPE_Y（目标真缺失，未处理）: {} 条".format(len(broken) - fixed_x))
    print("提示: 改完请运行 check_backlinks.py 复核，再 build_site.py。")

if __name__ == "__main__":
    main()
