#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_reconcile_figures.py — 一次性内容归位：
把散落在卡片 HTML 的 <div class="figure"> 图片（含说明）回填进对应 .md，
确立 "MD 为唯一源"。幂等：若 MD 已含该图片引用则跳过。
"""
import sys, re
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path

import build_site as bs
ROOT = bs.ROOT
SUBJECTS = bs.SUBJECTS
DIMS = bs.DIMS
CS, CE = bs.CONTENT_START, bs.CONTENT_END


def html_figures(html_text: str):
    """提取 HTML 正文块中的所有 figure：(src, caption)"""
    m = re.search(rf"{CS}(.*?){CE}", html_text, re.S)
    body = m.group(1) if m else html_text
    figs = []
    for fm in re.finditer(
            r'<div class="figure">.*?<img[^>]*src="([^"]+)"[^>]*>\s*'
            r'<div class="figure-caption">(.*?)</div>\s*</div>', body, re.S):
        src = fm.group(1)
        cap = re.sub(r"<[^>]+>", "", fm.group(2) or "").strip()
        figs.append((src, cap))
    return figs


def md_has_img(md_text: str, src: str) -> bool:
    return src in md_text


def insert_into_md(md_text: str, refs: list) -> str:
    """在内容区开头（## 核心内容 之前，或首个 --- 之后）插入图片引用"""
    block = "\n\n" + "\n\n".join(refs) + "\n"
    # 优先插到 "## 核心内容" 之前
    m = re.search(r"\n## 核心内容\n", md_text)
    if m:
        return md_text[:m.start()] + block + md_text[m.start():]
    # 否则插到首个 "---" 之后
    lines = md_text.split("\n")
    for i, ln in enumerate(lines):
        if ln.strip() == "---":
            return "\n".join(lines[:i+1]) + block + "\n" + "\n".join(lines[i+1:])
    return md_text + block


def safe_alt(cap: str, src: str) -> str:
    """alt 不能含 ] 或 )，否则破坏 markdown 图片语法"""
    if cap and "]" not in cap and ")" not in cap:
        return cap
    return Path(src).stem


def main():
    added_total = 0
    touched = 0
    for subject in SUBJECTS:
        for dim in DIMS:
            dim_dir = ROOT / subject / dim
            if not dim_dir.exists():
                continue
            for md_path in sorted(dim_dir.glob("*.md")):
                if md_path.name.startswith("索引_"):
                    continue
                html_path = md_path.with_suffix(".html")
                if not html_path.exists():
                    continue
                figs = html_figures(html_path.read_text(encoding="utf-8"))
                if not figs:
                    continue
                md_text = md_path.read_text(encoding="utf-8")
                refs = []
                for src, cap in figs:
                    if md_has_img(md_text, src):
                        continue
                    alt = safe_alt(cap, src)
                    refs.append(f"![{alt}]({src})")
                if refs:
                    md_text = insert_into_md(md_text, refs)
                    md_path.write_text(md_text, encoding="utf-8")
                    touched += 1
                    added_total += len(refs)
                    print(f"[+] {md_path.relative_to(ROOT)}  +{len(refs)} 图引用")
    print(f"\n完成：处理 {touched} 张卡片，新增 {added_total} 条图片引用。")


if __name__ == "__main__":
    main()
