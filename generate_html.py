# -*- coding: utf-8 -*-
"""
Batch Markdown to HTML converter for 2028 Gaokao Knowledge Base.
Handles: 语文, 英语(excluding 单词复习), 物理, 化学, 生物
"""
import os
import re
import glob

# Base directory
BASE = r"C:\Users\user\WPSDrive\203612604\WPS云盘\申悦文档\AI辅助\2028高考知识库"

# Subjects to process
SUBJECTS = ["语文", "英语", "物理", "化学", "生物"]

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | 2028高考{subject}</title>
<!-- MathJax 3 -->
<script>
MathJax = {{
  tex: {{
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    processEscapes: true,
    processEnvironments: true
  }},
  options: {{ skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre'] }}
}};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>
  body {{ font-family: "Microsoft YaHei", "PingFang SC", sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #f5f7fa; line-height: 1.8; color: #333; }}
  h1 {{ color: #1a5276; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
  h2 {{ color: #2874a6; border-left: 4px solid #3498db; padding-left: 12px; margin-top: 30px; }}
  h3 {{ color: #2e86c1; }}
  h4 {{ color: #3498db; }}
  table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
  th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
  th {{ background: #eaf2f8; }}
  code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: Consolas, monospace; }}
  pre {{ background: #f4f4f4; padding: 12px; border-radius: 4px; overflow-x: auto; }}
  pre code {{ background: transparent; padding: 0; }}
  blockquote {{ border-left: 4px solid #3498db; margin: 15px 0; padding: 10px 20px; background: #eaf2f8; }}
  .back {{ display: inline-block; margin-bottom: 20px; padding: 8px 16px; background: #3498db; color: white; text-decoration: none; border-radius: 4px; }}
  .back:hover {{ background: #2980b9; }}
  .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #888; font-size: 10pt; }}
  ul, ol {{ margin: 10px 0; padding-left: 25px; }}
  li {{ margin: 5px 0; }}
  a {{ color: #2980b9; }}
  a:hover {{ color: #e74c3c; }}
  hr {{ border: none; border-top: 1px solid #ddd; margin: 25px 0; }}
  img {{ max-width: 100%; height: auto; border-radius: 4px; }}
  .figure {{ text-align: center; margin: 20px 0; }}
  .figure img {{ max-width: 100%; border: 1px solid #ddd; border-radius: 4px; }}
  .figure-caption {{ color: #666; font-size: 10pt; margin-top: 5px; }}
</style>
</head>
<body>
  <a class="back" href="./">← 返回目录</a>
{content}
  <div class="footer">2028高考知识库 | 广东新高考{subject}</div>
</body>
</html>
'''


def escape_html(text):
    """Escape HTML special characters."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text


def unescape_in_math(text):
    """Unescape HTML entities inside math delimiters."""
    # Pattern to match $...$ and $$...$$
    def unescape_match(m):
        s = m.group(0)
        s = s.replace('&lt;', '<')
        s = s.replace('&gt;', '>')
        s = s.replace('&amp;', '&')
        return s
    
    # $$...$$
    text = re.sub(r'\$\$[^$]*\$\$', unescape_match, text)
    # $...$ (but not $$)
    text = re.sub(r'(?<!\$)\$[^$\n]+\$(?!\$)', unescape_match, text)
    return text


def md_to_html(md_text):
    """Convert markdown text to HTML using regex-based parser (like math subject)."""
    lines = md_text.split('\n')
    result = []
    i = 0
    in_code_block = False
    code_lang = ''
    code_lines = []
    in_table = False
    table_lines = []
    in_list = False
    list_type = None  # 'ul' or 'ol'
    list_items = []
    
    def flush_table():
        nonlocal table_lines
        if not table_lines:
            return
        html_parts = ['<table>']
        for idx, row in enumerate(table_lines):
            row = row.strip()
            if row.startswith('|'):
                row = row[1:]
            if row.endswith('|'):
                row = row[:-1]
            cells = [c.strip() for c in row.split('|')]
            cells = [c for c in cells if c or c == '']
            # Skip separator rows (---)
            if all(re.match(r'^[-:]+$', c.strip()) for c in cells if c.strip()):
                continue
            tag = 'th' if idx == 0 else 'td'
            html_parts.append('<tr>' + ''.join(f'<{tag}>{inline_md_to_html(c)}</{tag}>' for c in cells) + '</tr>')
        html_parts.append('</table>')
        table_lines = []
        result.append('\n'.join(html_parts))
    
    def flush_list():
        nonlocal list_items, list_type, in_list
        if not list_items:
            return
        tag = 'ul' if list_type == 'ul' else 'ol'
        items_html = '\n'.join(f'<li>{inline_md_to_html(item)}</li>' for item in list_items)
        result.append(f'<{tag}>\n{items_html}\n</{tag}>')
        list_items = []
        in_list = False
        list_type = None
    
    def flush_code():
        nonlocal code_lines, in_code_block, code_lang
        if not code_lines:
            return
        code_content = '\n'.join(code_lines)
        code_content = escape_html(code_content)
        lang_attr = f' class="language-{code_lang}"' if code_lang else ''
        result.append(f'<pre><code{lang_attr}>{code_content}</code></pre>')
        code_lines = []
        in_code_block = False
        code_lang = ''
    
    while i < len(lines):
        line = lines[i]
        
        # Code block
        if line.strip().startswith('```'):
            if in_code_block:
                flush_code()
            else:
                flush_table()
                flush_list()
                in_code_block = True
                code_lang = line.strip()[3:].strip()
            i += 1
            continue
        
        if in_code_block:
            code_lines.append(line)
            i += 1
            continue
        
        # Table
        if line.strip().startswith('|'):
            flush_list()
            in_table = True
            table_lines.append(line)
            i += 1
            continue
        elif in_table:
            flush_table()
            in_table = False
        
        # Empty line
        if line.strip() == '':
            flush_list()
            i += 1
            continue
        
        # Horizontal rule
        if re.match(r'^\s*---\s*$', line) or re.match(r'^\s*\*\*\*\s*$', line):
            flush_list()
            result.append('<hr>')
            i += 1
            continue
        
        # Headers
        m = re.match(r'^(#{1,4})\s+(.*)$', line)
        if m:
            flush_list()
            level = len(m.group(1))
            content = inline_md_to_html(m.group(2))
            result.append(f'<h{level}>{content}</h{level}>')
            i += 1
            continue
        
        # Unordered list
        m = re.match(r'^(\s*)[-*+]\s+(.*)$', line)
        if m:
            if not in_list or list_type != 'ul':
                flush_list()
                in_list = True
                list_type = 'ul'
            list_items.append(m.group(2))
            i += 1
            continue
        
        # Ordered list
        m = re.match(r'^(\s*)\d+\.\s+(.*)$', line)
        if m:
            if not in_list or list_type != 'ol':
                flush_list()
                in_list = True
                list_type = 'ol'
            list_items.append(m.group(2))
            i += 1
            continue
        
        # Blockquote
        if line.strip().startswith('>'):
            flush_list()
            bq_lines = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                bq_line = lines[i].strip()
                if bq_line.startswith('>'):
                    bq_line = bq_line[1:].strip()
                bq_lines.append(bq_line)
                i += 1
            bq_content = '\n'.join(bq_lines)
            # Process blockquote content recursively
            bq_html = md_to_html(bq_content)
            # Remove outer <p> tags if present
            bq_html = re.sub(r'^<p>|</p>$', '', bq_html.strip())
            result.append(f'<blockquote>\n{bq_html}\n</blockquote>')
            continue
        
        # Regular paragraph
        flush_list()
        para = inline_md_to_html(line)
        result.append(f'<p>{para}</p>')
        i += 1
    
    # Flush remaining
    if in_table:
        flush_table()
    if in_list:
        flush_list()
    if in_code_block:
        flush_code()
    
    return '\n\n'.join(result)


def inline_md_to_html(text):
    """Convert inline markdown to HTML."""
    # Code inline
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    # Images -> figure
    def img_repl(m):
        alt = m.group(1)
        src = m.group(2)
        return f'<div class="figure"><img src="{src}" alt="{alt}"><div class="figure-caption">{alt}</div></div>'
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', img_repl, text)
    # Links (but not images)
    text = re.sub(r'(?<!!)\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return text


def extract_h1(md_text):
    """Extract first h1 title from markdown."""
    for line in md_text.split('\n'):
        if line.startswith('# '):
            return line[2:].strip()
    return ""


def convert_file(md_path, subject):
    """Convert a single markdown file to HTML."""
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
    
    title = extract_h1(md_text) or os.path.splitext(os.path.basename(md_path))[0]
    
    # Convert markdown to HTML
    html_content = md_to_html(md_text)
    
    # Unescape math
    html_content = unescape_in_math(html_content)
    
    # Wrap in template
    full_html = HTML_TEMPLATE.format(title=title, subject=subject, content=html_content)
    
    # Write HTML
    html_path = os.path.splitext(md_path)[0] + '.html'
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    return html_path


def update_index_html(index_path):
    """Update index.html to change .md links to .html links."""
    if not os.path.exists(index_path):
        return False
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace .md links with .html, but be careful not to break things
    # Only replace href="... .md" patterns
    new_content = re.sub(r'href="([^"]+)\.md"', r'href="\1.html"', content)
    
    if new_content != content:
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False


def main():
    stats = {}
    
    for subject in SUBJECTS:
        subject_dir = os.path.join(BASE, subject)
        if not os.path.exists(subject_dir):
            continue
        
        count = 0
        
        # Find all .md files excluding index files and 单词复习 for 英语
        for root, dirs, files in os.walk(subject_dir):
            # Skip 单词复习 directory for 英语
            if subject == '英语' and '单词复习' in root:
                continue
            
            for fname in files:
                if not fname.endswith('.md'):
                    continue
                if fname.startswith('索引_'):
                    continue
                
                md_path = os.path.join(root, fname)
                try:
                    convert_file(md_path, subject)
                    count += 1
                except Exception as e:
                    print(f"Error converting {md_path}: {e}")
        
        stats[subject] = count
        print(f"{subject}: generated {count} HTML files")
    
    # Update index.html files
    index_files = [
        # 语文
        os.path.join(BASE, '语文', '核心知识网络', 'index.html'),
        os.path.join(BASE, '语文', '典型题型与方法', 'index.html'),
        os.path.join(BASE, '语文', '易错警示与辨析', 'index.html'),
        os.path.join(BASE, '语文', '素材与拓展', 'index.html'),
        # 英语
        os.path.join(BASE, '英语', '核心知识网络', 'index.html'),
        os.path.join(BASE, '英语', '典型题型与方法', 'index.html'),
        os.path.join(BASE, '英语', '易错警示与辨析', 'index.html'),
        os.path.join(BASE, '英语', '素材与拓展', 'index.html'),
        # 物理
        os.path.join(BASE, '物理', '核心知识网络', 'index.html'),
        os.path.join(BASE, '物理', '典型题型与方法', 'index.html'),
        os.path.join(BASE, '物理', '易错警示与辨析', 'index.html'),
        os.path.join(BASE, '物理', '素材与拓展', 'index.html'),
        # 化学
        os.path.join(BASE, '化学', '核心知识网络', 'index.html'),
        os.path.join(BASE, '化学', '典型题型与方法', 'index.html'),
        os.path.join(BASE, '化学', '易错警示与辨析', 'index.html'),
        os.path.join(BASE, '化学', '素材与拓展', 'index.html'),
        # 生物
        os.path.join(BASE, '生物', '核心知识网络', 'index.html'),
        os.path.join(BASE, '生物', '典型题型与方法', 'index.html'),
        os.path.join(BASE, '生物', '易错警示与辨析', 'index.html'),
        os.path.join(BASE, '生物', '素材与拓展', 'index.html'),
        # 其他
        os.path.join(BASE, '方法', 'index.html'),
        os.path.join(BASE, '复盘追踪', 'index.html'),
    ]
    
    updated = 0
    for idx_path in index_files:
        if update_index_html(idx_path):
            updated += 1
            print(f"Updated: {idx_path}")
        else:
            if os.path.exists(idx_path):
                print(f"No change needed: {idx_path}")
            else:
                print(f"Missing: {idx_path}")
    
    print(f"\nTotal index.html updated: {updated}")
    print(f"\nHTML generation stats:")
    for subject, count in stats.items():
        print(f"  {subject}: {count} files")


if __name__ == '__main__':
    main()
