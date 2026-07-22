#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_html_md_consistency.py — HTML 与 MD 内容一致性校验
========================================================
用于"MD 是唯一源"架构下，确认每张卡片的 HTML 正文确实由对应 MD 生成，
没有遗漏（图片缺失 / 正文段落缺失 / 标题缺失）。

原理：
  expected = md_body_to_html(md)[0]   # 用构建脚本同款转换器，从 MD 生成 HTML
  actual   = extract_card_content(html)  # 取当前 HTML 的 KB-CONTENT 正文块
对照两者：图片集合、标题集合、可见文本，逐项报告差异。

用法：  python check_html_md_consistency.py
退出码：发现不一致返回 1，否则 0（可接入 CI）。
"""
import sys, re, html as html_mod
sys.stdout.reconfigure(encoding="utf-8")

import build_site as bs
from pathlib import Path

ROOT = bs.ROOT
SUBJECTS = bs.SUBJECTS
DIMS = bs.DIMS
CS, CE = bs.CONTENT_START, bs.CONTENT_END


def extract_content(text: str) -> str:
    m = re.search(rf"{CS}(.*?){CE}", text, re.S)
    return m.group(1).strip() if m else text


def norm_text(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    s = html_mod.unescape(s)          # 反转义 &quot; &amp; &lt; 等，避免与MD字面字符误判为不一致
    s = re.sub(r"\s+", " ", s).strip()
    return s


def imgs(s: str):
    return re.findall(r'<img[^>]+src="([^"]+)"', s)


def headings(s: str):
    return re.findall(r"<h([2-6])>(.*?)</h\1>", s)


def analyze(md_path: Path):
    html_path = md_path.with_suffix(".html")
    if not html_path.exists():
        return None
    md_text = md_path.read_text(encoding="utf-8")
    expected_html, _ = bs.md_body_to_html(md_text)   # 期望（由MD生成）
    actual_html = extract_content(html_path.read_text(encoding="utf-8"))  # 实际

    e_imgs, a_imgs = imgs(expected_html), imgs(actual_html)
    e_head, a_head = headings(expected_html), headings(actual_html)
    e_txt, a_txt = norm_text(expected_html), norm_text(actual_html)

    issues = []
    # 1) 图片：MD生成应包含所有HTML图片
    missing_imgs = [i for i in a_imgs if i not in e_imgs]
    if missing_imgs:
        issues.append(("图片缺失", missing_imgs))
    # 2) 标题：MD生成应包含所有HTML标题（防止正文段落丢失）
    a_head_set = {(l, norm_text(h)) for l, h in a_head}
    e_head_set = {(l, norm_text(h)) for l, h in e_head}
    missing_heads = [h for h in a_head_set if h not in e_head_set]
    if missing_heads:
        issues.append(("标题缺失", [f"H{h[0]}: {h[1][:40]}" for h in missing_heads]))
    # 3) 文本长度差异（显著）
    if len(a_txt) > len(e_txt) + 200:
        issues.append(("HTML正文偏长", [f"HTML={len(a_txt)} > MD生成={len(e_txt)}"]))

    return issues


def main():
    problems = []
    checked = 0
    for subject in SUBJECTS:
        for dim in DIMS:
            dim_dir = ROOT / subject / dim
            if not dim_dir.exists():
                continue
            for md_path in sorted(dim_dir.glob("*.md")):
                if md_path.name.startswith("索引_"):
                    continue
                checked += 1
                issues = analyze(md_path)
                if issues:
                    problems.append((md_path.relative_to(ROOT), issues))

    print("=" * 64)
    print(f"一致性校验：检查卡片 {checked} 张，发现不一致 {len(problems)} 张")
    print("=" * 64)
    for rel, issues in problems:
        print(f"\n[{rel}]")
        for kind, items in issues:
            print(f"  ⚠️ {kind}（{len(items)}）:")
            for it in items:
                print(f"     - {it}")
    print("\n" + "=" * 64)
    if problems:
        print("结论：存在 HTML 有而 MD 没有的内容 → MD 不是完整源，需回填后修复构建。")
        return 1
    print("结论：全部卡片 HTML 正文均可由 MD 生成（MD 为完整源）。✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
