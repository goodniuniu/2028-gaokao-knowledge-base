#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_site.py — 2028高考知识库 一键站点重建脚本
=================================================
功能：
  1. 卡片页【换肤保留内容】：解析既有卡片 HTML 的 <body> 主内容（含已嵌入图片/
     MathJax 公式/表格），套入新模板（吸顶导航 + 面包屑 + 徽章行 + 共享 CSS）。
     徽章数据从同名 .md 元信息表解析。内容区用 KB-CONTENT 标记包裹，可重复构建。
  2. 对无 HTML 的 .md（6 张方法卡片 + 根目录管理文档 + 各科索引 + 复盘状态表）
     做简单 Markdown → HTML 转换生成页面。
  3. 重新生成全部 index.html（根、六科、各维度、方法、图形库、复盘追踪、
     英语、英语/单词复习及其子目录）。
  4. 链接校验：扫描所有生成/既有 HTML 的内部 href/src，输出断链清单。

用法：  python build_site.py
说明：  本脚本取代旧 generate_index.py；不修改任何 .md 文件。
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

import html as html_mod
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent

SUBJECTS = ["语文", "数学", "英语", "物理", "化学", "生物"]
DIMS = ["核心知识网络", "典型题型与方法", "易错警示与辨析", "素材与拓展"]
METHOD_CATS = ["学习方法", "心理建设", "生理管理", "考试策略"]

SUBJECT_ICONS = {
    "语文": "📖", "数学": "📐", "英语": "🌍", "物理": "⚛️",
    "化学": "⚗️", "生物": "🧬", "方法": "🎯", "复盘追踪": "📊", "图形库": "🖼️",
}
DIM_ICONS = {
    "核心知识网络": "🧠", "典型题型与方法": "📝", "易错警示与辨析": "⚠️",
    "素材与拓展": "📚", "单词复习": "🔤", "学习方法": "💡", "心理建设": "🧘",
    "生理管理": "💪", "考试策略": "🎓", "通用方法": "🧭",
}
SUBJECT_COLORS = {
    "语文": "#b03a2e", "数学": "#2563eb", "英语": "#059669",
    "物理": "#4f46e5", "化学": "#ea580c", "生物": "#0d9488", "方法": "#7c3aed",
}

# 根目录管理文档（md → html，首页快速导航链接）
ROOT_DOCS = [
    "00_知识库总索引.md",
    "01_知识卡片模板.md",
    "02_使用规则与检索说明.md",
    "00_知识库完善计划（650分目标）.md",
    "00_当前状态记录.md",
]
ROOT_DOC_ICONS = {
    "00_知识库总索引.md": "📋",
    "01_知识卡片模板.md": "📝",
    "02_使用规则与检索说明.md": "📖",
    "00_知识库完善计划（650分目标）.md": "🎯",
    "00_当前状态记录.md": "📌",
}

MATHJAX_HEAD = """<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
    processEscapes: true,
    processEnvironments: true
  },
  options: { skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre'] }
};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>"""

SITE_NAME = "2028高考知识库"
GITHUB_URL = "https://github.com/goodniuniu/2028-gaokao-knowledge-base"
PAGES_URL = "https://goodniuniu.github.io/2028-gaokao-knowledge-base"

CONTENT_START = "<!-- KB-CONTENT-START -->"
CONTENT_END = "<!-- KB-CONTENT-END -->"


# ---------------------------------------------------------------- 工具函数

def esc(s):
    return html_mod.escape(s, quote=True)


def rel_prefix(path: Path) -> str:
    """从 path 所在目录回到站点根的相对前缀，如 '../../'"""
    depth = len(path.parent.relative_to(ROOT).parts)
    return "../" * depth


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def write_text(p: Path, s: str):
    p.write_text(s, encoding="utf-8")


def md_title(md_path: Path) -> str:
    """提取 md 第一行 # 标题"""
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("# "):
                    return line[2:].strip()
                if line:
                    break
    except Exception:
        pass
    return md_path.stem


def parse_md_meta(md_path: Path) -> dict:
    """解析卡片 md 元信息表：| **状态** | ⚠️待强化 | 形式"""
    meta = {}
    try:
        text = read_text(md_path)
    except Exception:
        return meta
    for m in re.finditer(r"^\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|\s*$", text, re.M):
        key = m.group(1).strip()
        val = m.group(2).strip()
        if key not in meta:
            meta[key] = val
    return meta


def status_badge_class(status: str) -> str:
    if "✅" in status:
        return "kb-badge--ok"
    if "⚠" in status:
        return "kb-badge--warn"
    if "❌" in status:
        return "kb-badge--bad"
    return "kb-badge--tag"


def badges_html(meta: dict) -> str:
    """元信息 → 徽章行（状态/难度/时间标签/试卷来源/来源）"""
    out = []
    if meta.get("状态"):
        out.append(f'<span class="kb-badge {status_badge_class(meta["状态"])}">{esc(meta["状态"])}</span>')
    if meta.get("难度"):
        out.append(f'<span class="kb-badge kb-badge--diff">{esc(meta["难度"])}</span>')
    if meta.get("时间标签"):
        out.append(f'<span class="kb-badge kb-badge--tag">{esc(meta["时间标签"])}</span>')
    if meta.get("试卷来源"):
        out.append(f'<span class="kb-badge kb-badge--tag">{esc(meta["试卷来源"])}</span>')
    if meta.get("来源"):
        out.append(f'<span class="kb-badge kb-badge--src">来源：{esc(meta["来源"])}</span>')
    if not out:
        return ""
    return '<div class="kb-badges">' + "".join(out) + "</div>"


def extra_meta_note(meta: dict) -> str:
    """广东考情等长文本元信息 → 备注条（避免换肤时丢失信息）"""
    notes = []
    for k, v in meta.items():
        if k in ("状态", "难度", "时间标签", "试卷来源", "来源"):
            continue
        notes.append(f"<strong>{esc(k)}</strong>：{esc(v)}")
    if not notes:
        return ""
    return '<div class="kb-note">' + "<br>".join(notes) + "</div>"


def nav_html(prefix: str) -> str:
    return f'''<nav class="kb-nav">
  <a class="kb-nav__brand" href="{prefix}index.html"><span class="kb-nav__dot"></span>📚 {SITE_NAME}</a>
  <div class="kb-nav__links">
    <a href="{prefix}index.html">🏠 首页</a>
    <a href="{prefix}图形库/index.html">🖼️ 图形库</a>
    <a href="{prefix}复盘追踪/index.html">📊 复盘追踪</a>
  </div>
</nav>'''


def breadcrumb_html(items) -> str:
    """items: [(label, href|None), ...]"""
    lis = []
    for i, (label, href) in enumerate(items):
        if href and i < len(items) - 1:
            lis.append(f'<li><a href="{href}">{esc(label)}</a></li>')
        else:
            lis.append(f'<li><span aria-current="page">{esc(label)}</span></li>')
    return '<ol class="kb-breadcrumb">' + "".join(lis) + "</ol>"


def footer_html(extra="") -> str:
    mid = f"<br>{extra}" if extra else ""
    return f'''<footer class="kb-footer">📝 本知识库持续更新中，目标：2028 高考 650 分{mid}<br>
<a href="{GITHUB_URL}">GitHub 仓库</a> · <a href="{PAGES_URL}">GitHub Pages</a></footer>'''


def page_template(*, title, prefix, body_inner, subject=None, head_extra="", body_attrs="") -> str:
    attr = f'data-subject="{subject}"' if subject else ""
    if body_attrs:
        attr = (attr + " " + body_attrs).strip()
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)} | {SITE_NAME}</title>
<link rel="stylesheet" href="{prefix}assets/kb.css">
{head_extra}
</head>
<body {attr}>
{nav_html(prefix)}
{body_inner}
</body>
</html>'''


# ---------------------------------------------------------------- Markdown 转换

def _extract_code_blocks(text: str):
    """提取 ``` 围栏代码块 → 占位符"""
    blocks = []

    def repl(m):
        blocks.append(m.group(1))
        return f"\x00CODE{len(blocks) - 1}\x00"

    text = re.sub(r"```[^\n]*\n(.*?)```", repl, text, flags=re.S)
    return text, blocks


def _extract_math(text: str):
    """提取 $$...$$ 与 $...$ → 占位符（不转义 LaTeX 内容）"""
    segs = []

    def repl(m):
        segs.append(m.group(0))
        return f"\x00MATH{len(segs) - 1}\x00"

    text = re.sub(r"\$\$.+?\$\$", repl, text, flags=re.S)
    text = re.sub(r"\$[^\$\n]+?\$", repl, text)
    return text, segs


def _restore(text: str, token: str, values: list) -> str:
    for i, v in enumerate(values):
        text = text.replace(f"\x00{token}{i}\x00", v)
    return text


def _inline(text: str) -> str:
    """行内格式：转义 + 粗体/行内代码/图片/链接（占位符已在更外层处理）"""
    spans = []

    def keep(m):
        spans.append(m.group(0))
        return f"\x00SPAN{len(spans) - 1}\x00"

    # 图片与链接先整体保护（内部不再处理）
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", keep, text)
    text = re.sub(r"\[[^\]]+\]\([^)]+\)", keep, text)
    text = re.sub(r"`[^`]+`", keep, text)

    text = esc(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)

    def unkeep(m):
        raw = spans[int(m.group(1))]
        if raw.startswith("!["):
            mm = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", raw)
            return f'<img src="{esc(mm.group(2))}" alt="{esc(mm.group(1))}">'
        if raw.startswith("["):
            mm = re.match(r"\[([^\]]*)\]\(([^)]+)\)", raw)
            return f'<a href="{esc(mm.group(2))}">{esc(mm.group(1))}</a>'
        return f"<code>{esc(raw[1:-1])}</code>"

    text = re.sub(r"\x00SPAN(\d+)\x00", unkeep, text)
    return text


def md_body_to_html(md_text: str):
    """Markdown 正文 → HTML。跳过首个 # 标题与 字段/内容 元信息表。
    返回 (content_html, meta_dict)"""
    lines = md_text.split("\n")
    # 去掉首个 # 标题行
    for i, ln in enumerate(lines):
        if ln.strip().startswith("# "):
            del lines[i]
            break
    text = "\n".join(lines)

    # 解析并移除元信息表（表头含 字段/内容）
    meta = {}
    tbl = re.search(
        r"^\|\s*字段\s*\|\s*内容\s*\|\s*\n^\|[\s:\-|]+\|\s*\n((?:^\|.*\|\s*\n?)+)",
        text, re.M)
    if tbl:
        for row in tbl.group(1).strip().split("\n"):
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            if len(cells) >= 2:
                k = re.sub(r"\*\*", "", cells[0]).strip()
                meta[k] = cells[1]
        text = text[:tbl.start()] + text[tbl.end():]

    text, code_blocks = _extract_code_blocks(text)
    text, math_segs = _extract_math(text)

    out = []
    lines = text.split("\n")
    i = 0
    list_stack = []  # [(indent, tag)]

    def close_lists(to_indent=-1):
        while list_stack and list_stack[-1][0] > to_indent:
            _, tag = list_stack.pop()
            out.append(f"</{tag}>")

    def flush_para(buf):
        if buf:
            out.append("<p>" + _inline(" ".join(buf).strip()) + "</p>")
            buf.clear()

    para = []
    while i < len(lines):
        ln = lines[i]
        stripped = ln.strip()

        # 代码块占位行
        mcode = re.fullmatch(r"\x00CODE(\d+)\x00", stripped)
        if mcode:
            flush_para(para); close_lists()
            out.append(f"<pre><code>{esc(code_blocks[int(mcode.group(1))])}</code></pre>")
            i += 1
            continue

        if not stripped:
            flush_para(para); close_lists()
            i += 1
            continue

        # 标题
        mh = re.match(r"^(#{2,6})\s+(.*)$", stripped)
        if mh:
            flush_para(para); close_lists()
            level = len(mh.group(1))
            out.append(f"<h{level}>{_inline(mh.group(2).strip())}</h{level}>")
            i += 1
            continue

        # 分隔线
        if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", stripped):
            flush_para(para); close_lists()
            out.append("<hr>")
            i += 1
            continue

        # 表格
        if stripped.startswith("|") and i + 1 < len(lines) and re.match(
                r"^\|[\s:\-|]+\|\s*$", lines[i + 1].strip()):
            flush_para(para); close_lists()
            header = [c.strip() for c in stripped.strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            th = "".join(f"<th>{_inline(c)}</th>" for c in header)
            trs = []
            for r in rows:
                tds = "".join(f"<td>{_inline(c)}</td>" for c in r)
                trs.append(f"<tr>{tds}</tr>")
            out.append('<div class="table-wrap"><table>'
                       f"<tr>{th}</tr>{''.join(trs)}</table></div>")
            continue

        # 引用块
        if stripped.startswith(">"):
            flush_para(para); close_lists()
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            inner = "<br>".join(_inline(b.strip()) for b in buf if b.strip())
            out.append(f"<blockquote><p>{inner}</p></blockquote>")
            continue

        # 列表（无序 / 有序，按缩进嵌套）
        ml = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", ln)
        if ml:
            flush_para(para)
            indent = len(ml.group(1).replace("\t", "    ")) // 2
            tag = "ul" if ml.group(2) in ("-", "*") else "ol"
            item = ml.group(3).strip()
            while list_stack and list_stack[-1][0] > indent:
                _, t = list_stack.pop()
                out.append(f"</{t}>")
            if not list_stack or list_stack[-1][0] < indent:
                out.append(f"<{tag}>")
                list_stack.append((indent, tag))
            elif list_stack[-1][1] != tag:
                _, t = list_stack.pop()
                out.append(f"</{t}>")
                out.append(f"<{tag}>")
                list_stack.append((indent, tag))
            out.append(f"<li>{_inline(item)}</li>")
            i += 1
            continue

        para.append(stripped)
        i += 1

    flush_para(para)
    close_lists()

    content = "\n".join(out)
    content = _restore(content, "MATH", math_segs)
    # 残留代码占位（理论上已处理）
    content = _restore(content, "CODE",
                       [f"<pre><code>{esc(b)}</code></pre>" for b in code_blocks])
    return content, meta


def rewrite_md_links(content: str, from_dir: Path) -> str:
    """将指向 .md 的链接重写为同名 .html（若目标 html 存在）"""
    def repl(m):
        href = unquote(m.group(1))
        if not href.lower().endswith(".md"):
            return m.group(0)
        target_html = (from_dir / href).with_suffix(".html")
        if target_html.exists():
            return m.group(0)[:-len('.md"')] + '.html"'
        return m.group(0)
    return re.sub(r'href="([^"]+\.md)"', repl, content)


# ---------------------------------------------------------------- 断链修复

_STAGE_RE = re.compile(r"^(高一筑基|高二深化|高三冲刺)_")


def build_file_index() -> dict:
    """全站文件索引：stem -> [Path]（md/html，排除 index.html 与 .git）"""
    idx = {}
    for p in ROOT.rglob("*"):
        if ".git" in p.parts or not p.is_file():
            continue
        if p.suffix.lower() in (".md", ".html") and p.name != "index.html":
            idx.setdefault(p.stem, []).append(p)
    return idx


def _norm_stem(stem: str) -> str:
    return _STAGE_RE.sub("", stem)


def _pick_candidate(cands, from_dir: Path):
    """候选文件择优：同科目优先、html 优先"""
    if not cands:
        return None
    try:
        first = from_dir.relative_to(ROOT).parts[0]
    except Exception:
        first = ""
    def score(p: Path):
        same_subj = p.relative_to(ROOT).parts[0] == first
        is_html = p.suffix.lower() == ".html"
        return (same_subj, is_html)
    return sorted(cands, key=score, reverse=True)[0]


def fix_content_links(content: str, from_dir: Path, idx: dict) -> str:
    """修复内容区内部链接：
    - 指向 .md 且同名 .html 存在 → 改写为 .html
    - 目标不存在 → 按文件名全站查找（含阶段前缀归一化），命中则改写为正确相对路径
    - 仍找不到 → 退化为普通文本（保留显示文字，标注未创建）
    - 修复遗留畸形锚点（href 内含未转义引号）
    """
    # 预修复：href 属性值中混入多余引号的畸形锚点 → 去链接化
    def repair(m):
        label_m = re.search(r">(.*?)</a>\s*$", m.group(0), re.S)
        label = label_m.group(1) if label_m else ""
        return (f'<span class="kb-deadlink" '
                f'title="关联内容尚未创建">{label}</span>')
    content = re.sub(r'<a href="[^"]*"[^>]*"[^>]*>.*?</a>',
                     repair, content, flags=re.S)

    def repl(m):
        href = m.group(1)
        label = m.group(2)
        if href.startswith(("http://", "https://", "#", "mailto:", "data:",
                            "javascript:")):
            return m.group(0)
        frag = ""
        base = href
        if "#" in base:
            base, frag = base.split("#", 1)
            frag = "#" + frag
        target = unquote(base)
        resolved = from_dir / target
        # 已存在：md → 若同名 html 存在则升级
        if resolved.exists():
            if resolved.suffix.lower() == ".md":
                h = resolved.with_suffix(".html")
                if h.exists():
                    new = os_rel(h, from_dir)
                    return f'<a href="{new}{frag}">{label}</a>'
            return m.group(0)
        # 全站按文件名查找
        stem = Path(target).stem
        cands = idx.get(stem, [])
        if not cands:
            norm = _norm_stem(stem)
            cands = [p for s, ps in idx.items() if _norm_stem(s) == norm for p in ps]
        pick = _pick_candidate(cands, from_dir)
        if pick is not None:
            if pick.suffix.lower() == ".md" and pick.with_suffix(".html").exists():
                pick = pick.with_suffix(".html")
            new = os_rel(pick, from_dir)
            return f'<a href="{new}{frag}">{label}</a>'
        # 找不到目标：去链接化（保留文字）
        return (f'<span class="kb-deadlink" '
                f'title="关联内容尚未创建">{label}</span>')
    return re.sub(r'<a href="([^"]+)">(.*?)</a>', repl, content, flags=re.S)


def os_rel(target: Path, from_dir: Path) -> str:
    import os
    return os.path.relpath(target, from_dir).replace("\\", "/")


# ---------------------------------------------------------------- 卡片页换肤

def extract_card_content(html_text: str) -> str:
    """从既有卡片 HTML 提取正文内容（幂等：优先取标记区，否则剥离旧模板）"""
    m = re.search(r"<!-- KB-CONTENT-START -->(.*?)<!-- KB-CONTENT-END -->",
                  html_text, re.S)
    if m:
        return m.group(1).strip()
    m = re.search(r"<body[^>]*>(.*)</body>", html_text, re.S)
    if not m:
        return html_text
    body = m.group(1)
    # 旧返回链接
    body = re.sub(r'<a class="back"[^>]*>.*?</a>', "", body, count=1, flags=re.S)
    # 旧页脚
    body = re.sub(r'<div class="footer">.*?</div>', "", body, flags=re.S)
    # 首个 h1（模板会重新渲染标题）
    body = re.sub(r"<h1>.*?</h1>", "", body, count=1, flags=re.S)
    # 元信息表（字段/内容）
    body = re.sub(
        r'<div class="table-wrap">\s*<table>\s*<tr>\s*<th>字段</th>\s*<th>内容</th>\s*</tr>.*?</table>\s*</div>',
        "", body, count=1, flags=re.S)
    # 紧随其后的第一条 hr
    body = re.sub(r"<hr\s*/?>", "", body, count=1)
    return body.strip()


def ensure_tables_wrapped(content: str) -> str:
    """保险：若存在未包裹的 table 则统一包裹"""
    if "<table" not in content:
        return content
    if content.count("<table") == content.count('class="table-wrap"'):
        return content
    if 'class="table-wrap"' not in content:
        content = content.replace("<table", '<div class="table-wrap"><table')
        content = content.replace("</table>", "</table></div>")
    return content


def card_page(html_path: Path, md_path: Path, crumbs, subject: str, back_label: str,
              idx: dict):
    """换肤保留内容：重写单个卡片 HTML"""
    old = read_text(html_path) if html_path.exists() else ""
    content = extract_card_content(old)
    content = ensure_tables_wrapped(content)
    content = fix_content_links(content, html_path.parent, idx)
    title = md_title(md_path)
    meta = parse_md_meta(md_path)
    prefix = rel_prefix(html_path)

    body = f'''<div class="kb-wrap kb-wrap--narrow">
{breadcrumb_html(crumbs)}
<h1 class="kb-title">{esc(title)}</h1>
{badges_html(meta)}
{extra_meta_note(meta)}
<article class="kb-content">
{CONTENT_START}
{content}
{CONTENT_END}
</article>
<div class="kb-cardnav">
  <a class="kb-btn" href="./">← 返回{esc(back_label)}</a>
  <a class="kb-btn kb-btn--ghost" href="{prefix}index.html">🏠 返回首页</a>
</div>
{footer_html()}
</div>'''
    write_text(html_path, page_template(
        title=title, prefix=prefix, body_inner=body,
        subject=subject, head_extra=MATHJAX_HEAD))


def generate_card_from_md(md_path: Path, html_path: Path, crumbs, subject: str,
                          back_label: str, idx: dict):
    """md → 新卡片页（无既有 HTML 的方法卡片 / 文档页）"""
    text = read_text(md_path)
    content, meta = md_body_to_html(text)
    content = fix_content_links(content, md_path.parent, idx)
    title = md_title(md_path)
    if not meta:  # 文档页：再试一次元信息（保险）
        meta = parse_md_meta(md_path)
    prefix = rel_prefix(html_path)

    body = f'''<div class="kb-wrap kb-wrap--narrow">
{breadcrumb_html(crumbs)}
<h1 class="kb-title">{esc(title)}</h1>
{badges_html(meta)}
{extra_meta_note(meta)}
<article class="kb-content">
{CONTENT_START}
{content}
{CONTENT_END}
</article>
<div class="kb-cardnav">
  <a class="kb-btn" href="./">← 返回{esc(back_label)}</a>
  <a class="kb-btn kb-btn--ghost" href="{prefix}index.html">🏠 返回首页</a>
</div>
{footer_html()}
</div>'''
    write_text(html_path, page_template(
        title=title, prefix=prefix, body_inner=body,
        subject=subject, head_extra=MATHJAX_HEAD))


# ---------------------------------------------------------------- 索引页构建

def list_cards(dim_dir: Path):
    """返回目录下卡片 md 列表（排除 索引_*.md 等非卡片文档）"""
    if not dim_dir.exists():
        return []
    return sorted([p for p in dim_dir.glob("*.md")
                   if not p.name.startswith("索引_")])


def item_html(md_path: Path, href: str, icon="📄", show_badges=True) -> str:
    title = md_title(md_path)
    meta = parse_md_meta(md_path)
    badges = ""
    if show_badges:
        b = []
        if meta.get("状态"):
            b.append(f'<span class="kb-badge {status_badge_class(meta["状态"])}">{esc(meta["状态"])}</span>')
        if meta.get("难度"):
            b.append(f'<span class="kb-badge kb-badge--diff">{esc(meta["难度"])}</span>')
        if meta.get("时间标签"):
            b.append(f'<span class="kb-badge kb-badge--tag">{esc(meta["时间标签"])}</span>')
        if b:
            badges = f'<div class="kb-item__badges">{"".join(b)}</div>'
    return f'''<a class="kb-item" href="{href}">
  <span class="kb-item__icon">{icon}</span>
  <span class="kb-item__main"><span class="kb-item__title">{esc(title)}</span></span>
  {badges}
</a>'''


def build_dim_index(subject: str, dim: str):
    """科目/维度 索引页"""
    dim_dir = ROOT / subject / dim
    cards = list_cards(dim_dir)
    out_path = dim_dir / "index.html"
    prefix = rel_prefix(out_path)
    icon = DIM_ICONS.get(dim, "📁")
    if cards:
        items = "\n".join(
            item_html(m, m.with_suffix(".html").name) for m in cards)
        count_line = f"共 {len(cards)} 张知识卡片"
    else:
        items = ""
        count_line = "暂无卡片，待补充"
    body = f'''<div class="kb-wrap">
{breadcrumb_html([("首页", prefix + "index.html"), (subject, f"../index.html"), (dim, None)])}
<h1 class="kb-title">{SUBJECT_ICONS.get(subject, "📁")} {esc(subject)} · {icon} {esc(dim)}</h1>
<p style="color:var(--text-2);margin:0 0 20px">{count_line}</p>
<div class="kb-list">
{items}
</div>
{footer_html()}
</div>'''
    write_text(out_path, page_template(
        title=f"{subject} · {dim}", prefix=prefix, body_inner=body, subject=subject))


def build_subject_index(subject: str):
    """科目首页：维度分区 + 卡片网格"""
    subj_dir = ROOT / subject
    out_path = subj_dir / "index.html"
    prefix = rel_prefix(out_path)
    color = SUBJECT_COLORS.get(subject, "#2563eb")
    icon = SUBJECT_ICONS.get(subject, "📁")

    sections = []
    total = 0
    for dim in DIMS:
        cards = list_cards(subj_dir / dim)
        if not cards:
            continue
        total += len(cards)
        items = "\n".join(
            item_html(m, f"{dim}/{m.with_suffix('.html').name}") for m in cards)
        sections.append(f'''<h2 class="kb-section-title">{DIM_ICONS.get(dim, "📁")} {esc(dim)}（{len(cards)}）</h2>
<div class="kb-list">
{items}
</div>''')

    # 英语：单词复习专区
    if subject == "英语":
        wr = subj_dir / "单词复习"
        if wr.exists():
            chips = ['<a class="kb-chip" href="单词复习/假期复习总入口.html">🗓️ 假期复习总入口</a>']
            for sub in ["日期词表", "分组词表", "小测卷", "进度追踪"]:
                sd = wr / sub
                if (sd / "index.html").exists():
                    cnt = len(list(sd.glob("*.md")))
                    chips.append(f'<a class="kb-chip" href="单词复习/{sub}/index.html">{DIM_ICONS.get(sub, "📁")} {sub}（{cnt}）</a>')
            chips.append('<a class="kb-chip" href="单词复习/单词复习总计划.md">📋 复习总计划</a>')
            sections.append(f'''<h2 class="kb-section-title">🔤 单词复习专区</h2>
<div class="kb-chips">{"".join(chips)}</div>''')

    index_doc = ""
    if (subj_dir / f"索引_{subject}.md").exists():
        index_doc = f'<a class="kb-chip" href="索引_{subject}.html">📋 {esc(subject)}总索引</a>'

    body = f'''<div class="kb-wrap">
{breadcrumb_html([("首页", prefix + "index.html"), (subject, None)])}
<h1 class="kb-title">{icon} {esc(subject)}知识库</h1>
<p style="color:var(--text-2);margin:0 0 16px">共 {total} 张知识卡片 · 四大知识维度</p>
<div class="kb-chips" style="margin-bottom:8px">{index_doc}</div>
{"".join(sections)}
{footer_html()}
</div>'''
    write_text(out_path, page_template(
        title=f"{subject}知识库", prefix=prefix, body_inner=body, subject=subject))


def build_method_index():
    """方法体系首页"""
    mdir = ROOT / "方法"
    out_path = mdir / "index.html"
    prefix = rel_prefix(out_path)
    sections = []

    # 根级通用方法卡片
    root_cards = [p for p in mdir.glob("*.md") if not p.name.startswith("索引_")]
    if root_cards:
        items = "\n".join(
            item_html(m, m.with_suffix(".html").name, icon="🧭") for m in sorted(root_cards))
        sections.append(f'''<h2 class="kb-section-title">🧭 通用方法（{len(root_cards)}）</h2>
<div class="kb-list">
{items}
</div>''')

    for cat in METHOD_CATS:
        cards = list_cards(mdir / cat)
        if not cards:
            continue
        items = "\n".join(
            item_html(m, f"{cat}/{m.with_suffix('.html').name}") for m in cards)
        sections.append(f'''<h2 class="kb-section-title">{DIM_ICONS.get(cat, "📁")} {esc(cat)}（{len(cards)}）</h2>
<div class="kb-list">
{items}
</div>''')

    index_doc = ""
    if (mdir / "索引_方法.md").exists():
        index_doc = '<a class="kb-chip" href="索引_方法.html">📋 方法体系总索引</a>'

    body = f'''<div class="kb-wrap">
{breadcrumb_html([("首页", prefix + "index.html"), ("方法", None)])}
<h1 class="kb-title">🎯 方法体系</h1>
<p style="color:var(--text-2);margin:0 0 16px">学习方法 · 心理建设 · 生理管理 · 考试策略</p>
<div class="kb-chips" style="margin-bottom:8px">{index_doc}</div>
{"".join(sections)}
{footer_html()}
</div>'''
    write_text(out_path, page_template(
        title="方法体系", prefix=prefix, body_inner=body, subject="方法"))


def build_method_cat_index(cat: str):
    cat_dir = ROOT / "方法" / cat
    cards = list_cards(cat_dir)
    out_path = cat_dir / "index.html"
    prefix = rel_prefix(out_path)
    items = "\n".join(item_html(m, m.with_suffix(".html").name) for m in cards)
    body = f'''<div class="kb-wrap">
{breadcrumb_html([("首页", prefix + "index.html"), ("方法", "../index.html"), (cat, None)])}
<h1 class="kb-title">{DIM_ICONS.get(cat, "📁")} {esc(cat)}</h1>
<p style="color:var(--text-2);margin:0 0 20px">共 {len(cards)} 篇</p>
<div class="kb-list">
{items}
</div>
{footer_html()}
</div>'''
    write_text(out_path, page_template(
        title=f"方法 · {cat}", prefix=prefix, body_inner=body, subject="方法"))


def build_gallery_index():
    """图形库索引：按科目画廊展示 PNG"""
    gdir = ROOT / "图形库"
    out_path = gdir / "index.html"
    prefix = rel_prefix(out_path)
    sections = []
    total = 0
    for sub in ["物理", "化学", "生物", "数学"]:
        sd = gdir / sub
        if not sd.exists():
            continue
        pngs = sorted(sd.glob("*.png"))
        if not pngs:
            continue
        total += len(pngs)
        figs = "\n".join(f'''<div class="kb-fig">
  <a href="{sub}/{p.name}" target="_blank"><img src="{sub}/{p.name}" alt="{esc(p.stem)}" loading="lazy"></a>
  <div class="kb-fig__cap">{esc(p.stem)}</div>
  <div class="kb-fig__sub">{sub}</div>
</div>''' for p in pngs)
        sections.append(f'''<h2 class="kb-section-title">{SUBJECT_ICONS.get(sub, "🖼️")} {sub}（{len(pngs)}）</h2>
<div class="kb-gallery">
{figs}
</div>''')

    body = f'''<div class="kb-wrap">
{breadcrumb_html([("首页", prefix + "index.html"), ("图形库", None)])}
<h1 class="kb-title">🖼️ 图形索引</h1>
<p style="color:var(--text-2);margin:0 0 20px">知识点示意图汇总 · 共 {total} 张（点击看大图）</p>
{"".join(sections)}
{footer_html()}
</div>'''
    write_text(out_path, page_template(
        title="图形索引", prefix=prefix, body_inner=body, subject="图形库"))


def build_review_index():
    """复盘追踪索引"""
    rdir = ROOT / "复盘追踪"
    out_path = rdir / "index.html"
    prefix = rel_prefix(out_path)
    items = []
    state_md = rdir / "知识掌握状态表.md"
    if state_md.exists():
        items.append(item_html(state_md, "知识掌握状态表.html", icon="📊"))
    body = f'''<div class="kb-wrap">
{breadcrumb_html([("首页", prefix + "index.html"), ("复盘追踪", None)])}
<h1 class="kb-title">📊 复盘追踪</h1>
<p style="color:var(--text-2);margin:0 0 20px">知识掌握状态表 · 学习进度追踪</p>
<div class="kb-list">
{"".join(items)}
</div>
{footer_html()}
</div>'''
    write_text(out_path, page_template(
        title="复盘追踪", prefix=prefix, body_inner=body, subject="复盘追踪"))


def build_english_index():
    """英语首页已由 build_subject_index 处理（含单词复习专区）。
    此函数生成 英语/单词复习/index.html"""
    wr = ROOT / "英语" / "单词复习"
    out_path = wr / "index.html"
    prefix = rel_prefix(out_path)

    cards = []
    if (wr / "假期复习总入口.html").exists():
        cards.append('''<a class="kb-card" href="假期复习总入口.html" style="--card-accent:#059669">
  <div class="kb-card__icon">🗓️</div>
  <div class="kb-card__title">假期复习总入口</div>
  <div class="kb-card__meta">49 天日历视图 · 打卡进度追踪 · 每日词表与小测直达</div>
</a>''')
    if (wr / "单词复习总计划.md").exists():
        cards.append('''<a class="kb-card" href="单词复习总计划.md">
  <div class="kb-card__icon">📋</div>
  <div class="kb-card__title">单词复习总计划</div>
  <div class="kb-card__meta">6008 词整体规划（Markdown 原文）</div>
</a>''')
    for sub, desc in [("日期词表", "按日期组织的每日词表"),
                      ("分组词表", "按分组组织的词表"),
                      ("小测卷", "每日小测与答案"),
                      ("进度追踪", "打卡表与错题本")]:
        sd = wr / sub
        if (sd / "index.html").exists():
            cnt = len(list(sd.glob("*.md")))
            cards.append(f'''<a class="kb-card" href="{sub}/index.html">
  <div class="kb-card__icon">{DIM_ICONS.get(sub, "📁")}</div>
  <div class="kb-card__title">{esc(sub)}（{cnt}）</div>
  <div class="kb-card__meta">{esc(desc)}</div>
</a>''')
    pq = wr / "可打印小测卷"
    if pq.exists():
        cnt = len(list(pq.glob("*.html")))
        cards.append(f'''<a class="kb-card" href="假期复习总入口.html">
  <div class="kb-card__icon">🖨️</div>
  <div class="kb-card__title">可打印小测卷（{cnt}）</div>
  <div class="kb-card__meta">A4 打印版小测 · 从假期复习总入口按日进入</div>
</a>''')

    body = f'''<div class="kb-wrap">
{breadcrumb_html([("首页", prefix + "index.html"), ("英语", "../index.html"), ("单词复习", None)])}
<h1 class="kb-title">🔤 英语 · 单词复习</h1>
<p style="color:var(--text-2);margin:0 0 20px">假期：2025年7月13日 ~ 8月30日 · 共 49 天 · 6008 词</p>
<div class="kb-grid">
{"".join(cards)}
</div>
{footer_html()}
</div>'''
    write_text(out_path, page_template(
        title="英语 · 单词复习", prefix=prefix, body_inner=body, subject="英语"))


def build_vocab_sub_index(sub: str):
    """单词复习子目录索引（日期词表/分组词表/小测卷/进度追踪）→ 链接 .md 原文"""
    sd = ROOT / "英语" / "单词复习" / sub
    if not sd.exists():
        return
    out_path = sd / "index.html"
    prefix = rel_prefix(out_path)
    mds = sorted(sd.glob("*.md"))
    items = "\n".join(
        item_html(m, m.name, icon="📄", show_badges=False) for m in mds)
    body = f'''<div class="kb-wrap">
{breadcrumb_html([("首页", prefix + "index.html"), ("英语", "../../index.html"), ("单词复习", "../index.html"), (sub, None)])}
<h1 class="kb-title">{DIM_ICONS.get(sub, "📁")} {esc(sub)}</h1>
<p style="color:var(--text-2);margin:0 0 20px">共 {len(mds)} 个文件（Markdown 原文）</p>
<div class="kb-list">
{items}
</div>
{footer_html()}
</div>'''
    write_text(out_path, page_template(
        title=f"单词复习 · {sub}", prefix=prefix, body_inner=body, subject="英语"))


def build_root_index():
    """站点根首页：hero + 统计 + 快速导航 + 六科卡片网格 + 专区"""
    out_path = ROOT / "index.html"
    prefix = ""

    total_cards = 0
    subject_cards = []
    for subject in SUBJECTS:
        icon = SUBJECT_ICONS[subject]
        color = SUBJECT_COLORS[subject]
        count = 0
        links = []
        for dim in DIMS:
            cards = list_cards(ROOT / subject / dim)
            if cards:
                count += len(cards)
                links.append(
                    f'<a href="{subject}/{dim}/index.html">{dim}</a> <span class="cnt">({len(cards)})</span>')
        total_cards += count
        extra = ""
        if subject == "英语":
            extra = ('<br><a href="英语/单词复习/index.html">🔤 单词复习专区</a> '
                     '<span class="cnt">(假期49天)</span>')
        subject_cards.append(f'''<a class="kb-card" href="{subject}/index.html" style="--card-accent:{color}">
  <div class="kb-card__icon">{icon}</div>
  <div class="kb-card__title">{subject}</div>
  <div class="kb-card__meta">{count} 张卡片</div>
  <div class="kb-card__links">{"<br>".join(links)}{extra}</div>
</a>''')

    # 方法卡片数
    method_count = len([p for p in (ROOT / "方法").glob("*.md")
                        if not p.name.startswith("索引_")])
    for cat in METHOD_CATS:
        method_count += len(list_cards(ROOT / "方法" / cat))
    total_cards += method_count

    quick = "".join(
        f'<a class="kb-chip" href="{Path(d).with_suffix(".html").name}">{ROOT_DOC_ICONS[d]} {esc(md_title(ROOT / d))}</a>'
        for d in ROOT_DOCS if (ROOT / d).exists())
    quick += '<a class="kb-chip" href="图形库/index.html">🖼️ 图形索引</a>'

    method_links = " ".join(
        f'<a class="kb-chip" href="方法/{cat}/index.html">{DIM_ICONS[cat]} {cat}</a>'
        for cat in METHOD_CATS if list_cards(ROOT / "方法" / cat))

    body = f'''<div class="kb-wrap">
<div class="kb-hero">
  <h1>📚 {SITE_NAME}</h1>
  <p>2028年广东新高考六科学习知识库 · 选科：语文 / 数学 / 英语 / 物理 / 化学 / 生物</p>
  <div class="kb-stats">
    <div class="kb-stat"><span class="num">{total_cards}</span><span class="label">知识卡片</span></div>
    <div class="kb-stat"><span class="num">6</span><span class="label">覆盖科目</span></div>
    <div class="kb-stat"><span class="num">4</span><span class="label">知识维度</span></div>
    <div class="kb-stat"><span class="num">650</span><span class="label">目标分数</span></div>
  </div>
</div>

<h2 class="kb-section-title">快速导航</h2>
<div class="kb-chips">{quick}</div>

<h2 class="kb-section-title">六科知识库</h2>
<div class="kb-grid kb-grid--wide">
{"".join(subject_cards)}
</div>

<h2 class="kb-section-title">🎯 方法体系</h2>
<div class="kb-card" style="--card-accent:{SUBJECT_COLORS["方法"]}">
  <div class="kb-card__title">学习方法 · 心理建设 · 生理管理 · 考试策略（{method_count} 篇）</div>
  <div class="kb-chips" style="margin-top:12px">{method_links}
  <a class="kb-chip" href="方法/index.html">→ 进入方法体系</a></div>
</div>

<h2 class="kb-section-title">📌 学习管理</h2>
<div class="kb-grid">
  <a class="kb-card" href="复盘追踪/index.html" style="--card-accent:#475569">
    <div class="kb-card__icon">📊</div>
    <div class="kb-card__title">复盘追踪</div>
    <div class="kb-card__meta">知识掌握状态表 · 学习进度追踪</div>
  </a>
  <a class="kb-card" href="图形库/index.html" style="--card-accent:#0891b2">
    <div class="kb-card__icon">🖼️</div>
    <div class="kb-card__title">图形库</div>
    <div class="kb-card__meta">32 张知识点示意图（物理 / 化学 / 生物 / 数学）</div>
  </a>
</div>

{footer_html()}
</div>'''
    write_text(out_path, page_template(
        title="首页", prefix=prefix, body_inner=body))


# ---------------------------------------------------------------- 假期复习总入口换肤

def reskin_holiday_entry():
    """英语/单词复习/假期复习总入口.html：保留日历/进度功能，套新导航与共享CSS"""
    p = ROOT / "英语" / "单词复习" / "假期复习总入口.html"
    if not p.exists():
        return
    old = read_text(p)

    m = re.search(r"<!-- KB-STYLE-START -->(.*?)<!-- KB-STYLE-END -->", old, re.S)
    if m:
        style_inner = m.group(1)
    else:
        ms = re.search(r"<style>(.*?)</style>", old, re.S)
        style_inner = ms.group(1) if ms else ""

    m = re.search(r"<!-- KB-CONTENT-START -->(.*?)<!-- KB-CONTENT-END -->", old, re.S)
    if m:
        body_inner = m.group(1)
    else:
        mb = re.search(r"<body[^>]*>(.*?)<script>", old, re.S)
        body_inner = mb.group(1) if mb else ""

    m = re.search(r"<!-- KB-SCRIPT-START -->(.*?)<!-- KB-SCRIPT-END -->", old, re.S)
    if m:
        script_inner = m.group(1)
    else:
        mj = re.search(r"<script>(.*?)</script>\s*</body>", old, re.S)
        script_inner = mj.group(1) if mj else ""

    prefix = rel_prefix(p)
    crumbs = breadcrumb_html([
        ("首页", prefix + "index.html"),
        ("英语", "../index.html"),
        ("单词复习", "./index.html"),
        ("假期复习总入口", None)])
    # 原页面 .container 自带 max-width；导航/面包屑用 kb-wrap 对齐宽度
    new = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>2028高考英语词汇假期复习总入口 | {SITE_NAME}</title>
<link rel="stylesheet" href="{prefix}assets/kb.css">
<style>
<!-- KB-STYLE-START -->{style_inner}<!-- KB-STYLE-END -->
</style>
</head>
<body data-subject="英语">
{nav_html(prefix)}
<div class="kb-wrap" style="max-width:1200px;padding-bottom:0">
{crumbs}
</div>
{CONTENT_START}{body_inner}{CONTENT_END}
<script>
<!-- KB-SCRIPT-START -->{script_inner}<!-- KB-SCRIPT-END -->
</script>
</body>
</html>'''
    write_text(p, new)


# ---------------------------------------------------------------- 链接校验

def check_links():
    """扫描全部 HTML 的内部 href/src，返回断链清单 [(file, link)]"""
    broken = []
    html_files = [p for p in ROOT.rglob("*.html") if ".git" not in p.parts]
    for f in html_files:
        text = read_text(f)
        for m in re.finditer(r'(?:href|src)="([^"]+)"', text):
            link = m.group(1).strip()
            if not link or link.startswith(("http://", "https://", "#", "mailto:",
                                            "data:", "javascript:")):
                continue
            target = unquote(link.split("#")[0].split("?")[0])
            if not target:
                continue
            resolved = (f.parent / target)
            if link.endswith("/") or target.endswith("/"):
                if not (resolved / "index.html").exists() and not resolved.is_dir():
                    broken.append((f, link))
                continue
            if resolved.is_dir():
                if not (resolved / "index.html").exists():
                    broken.append((f, link))
                continue
            if not resolved.exists():
                broken.append((f, link))
    return broken


# ---------------------------------------------------------------- 主流程

def main():
    rebuilt_cards = 0
    generated_cards = 0
    generated_docs = 0
    idx = build_file_index()

    # ---- 1. 六科卡片：换肤保留内容 ----
    for subject in SUBJECTS:
        for dim in DIMS:
            dim_dir = ROOT / subject / dim
            for md_path in list_cards(dim_dir):
                html_path = md_path.with_suffix(".html")
                crumbs = [("首页", rel_prefix(html_path) + "index.html"),
                          (subject, "../index.html"),
                          (dim, "./index.html"),
                          (md_title(md_path), None)]
                if html_path.exists():
                    card_page(html_path, md_path, crumbs, subject, dim, idx)
                    rebuilt_cards += 1
                else:
                    generate_card_from_md(md_path, html_path, crumbs, subject, dim, idx)
                    generated_cards += 1

    # ---- 2. 方法卡片（含 6 张无 HTML 的） ----
    mdir = ROOT / "方法"
    for md_path in sorted(mdir.glob("*.md")):
        if md_path.name.startswith("索引_"):
            continue
        html_path = md_path.with_suffix(".html")
        crumbs = [("首页", rel_prefix(html_path) + "index.html"),
                  ("方法", "./index.html"),
                  (md_title(md_path), None)]
        if html_path.exists():
            card_page(html_path, md_path, crumbs, "方法", "方法体系", idx)
            rebuilt_cards += 1
        else:
            generate_card_from_md(md_path, html_path, crumbs, "方法", "方法体系", idx)
            generated_cards += 1
    for cat in METHOD_CATS:
        for md_path in list_cards(mdir / cat):
            html_path = md_path.with_suffix(".html")
            crumbs = [("首页", rel_prefix(html_path) + "index.html"),
                      ("方法", "../index.html"),
                      (cat, "./index.html"),
                      (md_title(md_path), None)]
            if html_path.exists():
                card_page(html_path, md_path, crumbs, "方法", cat, idx)
                rebuilt_cards += 1
            else:
                generate_card_from_md(md_path, html_path, crumbs, "方法", cat, idx)
                generated_cards += 1

    # ---- 3. 文档页：根目录管理文档 / 各科索引 / 复盘状态表 ----
    for d in ROOT_DOCS:
        md_path = ROOT / d
        if md_path.exists():
            html_path = md_path.with_suffix(".html")
            crumbs = [("首页", "index.html"), (md_title(md_path), None)]
            generate_card_from_md(md_path, html_path, crumbs, None, "首页", idx)
            generated_docs += 1
    for subject in SUBJECTS:
        md_path = ROOT / subject / f"索引_{subject}.md"
        if md_path.exists():
            html_path = md_path.with_suffix(".html")
            crumbs = [("首页", rel_prefix(html_path) + "index.html"),
                      (subject, "./index.html"),
                      (md_title(md_path), None)]
            generate_card_from_md(md_path, html_path, crumbs, subject, subject, idx)
            generated_docs += 1
    md_path = ROOT / "方法" / "索引_方法.md"
    if md_path.exists():
        html_path = md_path.with_suffix(".html")
        crumbs = [("首页", rel_prefix(html_path) + "index.html"),
                  ("方法", "./index.html"), (md_title(md_path), None)]
        generate_card_from_md(md_path, html_path, crumbs, "方法", "方法体系", idx)
        generated_docs += 1
    md_path = ROOT / "复盘追踪" / "知识掌握状态表.md"
    if md_path.exists():
        html_path = md_path.with_suffix(".html")
        crumbs = [("首页", rel_prefix(html_path) + "index.html"),
                  ("复盘追踪", "./index.html"), (md_title(md_path), None)]
        generate_card_from_md(md_path, html_path, crumbs, "复盘追踪", "复盘追踪", idx)
        generated_docs += 1

    # ---- 4. 索引页 ----
    index_count = 0
    for subject in SUBJECTS:
        build_subject_index(subject); index_count += 1
        for dim in DIMS:
            # 目录存在即生成（含空维度："暂无卡片"占位页，保证链接可达）
            if (ROOT / subject / dim).is_dir():
                build_dim_index(subject, dim); index_count += 1
    build_method_index(); index_count += 1
    for cat in METHOD_CATS:
        if list_cards(ROOT / "方法" / cat):
            build_method_cat_index(cat); index_count += 1
    build_gallery_index(); index_count += 1
    build_review_index(); index_count += 1
    build_english_index(); index_count += 1
    for sub in ["日期词表", "分组词表", "小测卷", "进度追踪"]:
        if (ROOT / "英语" / "单词复习" / sub).exists():
            build_vocab_sub_index(sub); index_count += 1
    build_root_index(); index_count += 1

    # ---- 5. 假期复习总入口换肤 ----
    reskin_holiday_entry()

    # ---- 6. 链接校验 ----
    broken = check_links()

    print("=" * 60)
    print(f"✅ 卡片页换肤重建：{rebuilt_cards} 张")
    print(f"✅ 新卡片页生成（原无 HTML）：{generated_cards} 张")
    print(f"✅ 文档页生成：{generated_docs} 个")
    print(f"✅ 索引页生成：{index_count} 个")
    print(f"✅ 假期复习总入口：已换肤（功能保留）")
    print("-" * 60)
    if broken:
        print(f"⚠️ 发现断链 {len(broken)} 处：")
        for f, link in broken:
            print(f"  [{f.relative_to(ROOT)}] -> {link}")
    else:
        print("✅ 链接校验通过：无断链")
    print("=" * 60)
    return len(broken)


if __name__ == "__main__":
    sys.exit(0 if main() == 0 else 1)
