#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""诊断：HTML 与 MD 内容漂移检测。
对每张卡片：提取 HTML 正文文本 + 图片src，与 MD 正文文本 + 图片做对比，
报告 HTML 独有的内容（防止改建构脚本后丢失）。
"""
import sys, re
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SUBJECTS = ["语文", "数学", "英语", "物理", "化学", "生物"]
DIMS = ["核心知识网络", "典型题型与方法", "易错警示与辨析", "素材与拓展"]

CONTENT_START = "<!-- KB-CONTENT-START -->"
CONTENT_END = "<!-- KB-CONTENT-END -->"

def extract_html_content(text: str) -> str:
    m = re.search(rf"{CONTENT_START}(.*?){CONTENT_END}", text, re.S)
    if m:
        return m.group(1)
    return text

def strip_tags(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def html_imgs(text: str):
    return re.findall(r'<img[^>]+src="([^"]+)"', text)

def md_imgs(text: str):
    return re.findall(r'!\[[^\]]*\]\(([^)]+)\)', text)

def md_text_body(md_text: str) -> str:
    lines = md_text.split("\n")
    for i, ln in enumerate(lines):
        if ln.strip().startswith("# "):
            del lines[i]; break
    text = "\n".join(lines)
    # 去元信息表
    tbl = re.search(r"^\|\s*字段\s*\|\s*内容\s*\|\s*\n", text, re.M)
    if tbl:
        # 找到表结束
        lines2 = text.split("\n")
        out = []
        skip = False
        for ln in lines2:
            if ln.strip().startswith("| 字段 | 内容 |"):
                skip = True; continue
            if skip and re.match(r"^\|[\s:\-|]+\|\s*$", ln.strip()):
                skip = False; continue
            if skip:
                continue
            out.append(ln)
        text = "\n".join(out)
    return strip_tags(text)

total_html_only_imgs = 0
total_html_longer = 0
problems = []

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
            html_text = html_path.read_text(encoding="utf-8")
            md_text = md_path.read_text(encoding="utf-8")
            hc = extract_html_content(html_text)
            hc_stripped = strip_tags(hc)
            md_stripped = md_text_body(md_text)

            h_imgs = html_imgs(hc)
            m_imgs = md_imgs(md_text)
            # HTML 图片不在 MD 中
            html_only_imgs = [img for img in h_imgs if img not in m_imgs]

            # HTML 正文是否比 MD 多（显著）
            h_len = len(hc_stripped)
            m_len = len(md_stripped)
            longer = h_len > m_len + 200  # 文本多 200 字以上视为有额外内容

            if html_only_imgs or longer:
                total_html_only_imgs += len(html_only_imgs)
                if longer: total_html_longer += 1
                problems.append((md_path.relative_to(ROOT), html_only_imgs,
                                 h_len, m_len, longer))

print("="*70)
print(f"漂移卡片数（HTML 有而 MD 没有的内容）：{len(problems)}")
print(f"  - 含 HTML 独有图片的卡片：{sum(1 for p in problems if p[1])}")
print(f"  - 含 HTML 文本多于 MD 的卡片：{total_html_longer}")
print("="*70)
for rel, imgs, hl, ml, longer in problems:
    print(f"\n[{rel}]")
    print(f"  文本长度 HTML={hl}  MD={ml}  {'⚠️HTML更长' if longer else '✅'}")
    if imgs:
        print(f"  HTML独有图片({len(imgs)}):")
        for img in imgs:
            print(f"    - {img}")
