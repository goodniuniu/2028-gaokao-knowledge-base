#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""提取 HTML比MD长的卡片中，HTML独有正文文本（去标签后），供回填判断。"""
import sys, re
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path

ROOT = Path(__file__).resolve().parent
targets = [
    r"数学\核心知识网络\高二深化_数学_核心知识网络_等差数列与等比数列.md",
    r"物理\核心知识网络\高二深化_物理_核心知识网络_物理实验体系.md",
    r"物理\典型题型与方法\高二深化_物理_典型题型与方法_力学三大模型通法.md",
    r"物理\易错警示与辨析\高一筑基_物理_易错警示与辨析_动能定理错题分析.md",
    r"物理\素材与拓展\高一筑基_物理_素材与拓展_广东科技素材（华为5G与比亚迪）.md",
]

def strip_tags(s):
    s = re.sub(r"<[^>]+>", "\n", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s.strip()

for t in targets:
    md = ROOT / t
    html = md.with_suffix(".html")
    ht = html.read_text(encoding="utf-8")
    m = re.search(r"<!-- KB-CONTENT-START -->(.*?)<!-- KB-CONTENT-END -->", ht, re.S)
    body = m.group(1) if m else ht
    # 去掉图片/表格标签，只看文本块
    text = strip_tags(body)
    print("\n" + "="*60)
    print(t)
    print("="*60)
    print(text[:1500])
