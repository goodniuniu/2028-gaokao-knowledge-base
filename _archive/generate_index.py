#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ⚠️ 本脚本已被 build_site.py 取代（新设计系统 + 卡片换肤 + 链接校验），保留仅供参考。
"""
为2028高考知识库生成所有index.html
解决GitHub Pages中文路径404问题
"""
import os
import re
from pathlib import Path

# 项目根目录
ROOT = Path("C:/Users/user/WPSDrive/203612604/WPS云盘/申悦文档/AI辅助/2028高考知识库")

# 科目图标映射
SUBJECT_ICONS = {
    "数学": "📐",
    "语文": "📖",
    "英语": "🌍",
    "物理": "⚛️",
    "化学": "⚗️",
    "生物": "🧬",
    "方法": "🎯",
    "复盘追踪": "📊",
}

# 分类图标映射
CATEGORY_ICONS = {
    "核心知识网络": "🧠",
    "典型题型与方法": "📝",
    "易错警示与辨析": "⚠️",
    "素材与拓展": "📚",
    "单词复习": "🔤",
    "日期词表": "📅",
    "可打印小测卷": "📄",
    "分组词表": "📋",
    "小测卷": "📄",
    "进度追踪": "📈",
    "学习方法": "💡",
    "心理建设": "🧘",
    "生理管理": "💪",
    "考试策略": "🎓",
}


def get_icon(subject, category=""):
    """获取图标"""
    if category in CATEGORY_ICONS:
        return CATEGORY_ICONS[category]
    return SUBJECT_ICONS.get(subject, "📁")


def extract_title_from_md(filepath):
    """从markdown文件提取标题"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if first_line.startswith('# '):
                return first_line[2:].strip()
            elif first_line.startswith('## '):
                return first_line[3:].strip()
    except Exception:
        pass
    return None


def extract_tags_from_md(filepath):
    """从markdown文件提取标签信息"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(2000)
            # 尝试匹配标签行
            tag_match = re.search(r'\*\*标签\*\*[:：]\s*(.+)', content)
            if tag_match:
                return tag_match.group(1).strip()
            # 尝试匹配元数据
            meta_match = re.search(r'---\s*\n(.*?)\s*\n---', content, re.DOTALL)
            if meta_match:
                meta = meta_match.group(1)
                for line in meta.split('\n'):
                    if line.startswith('tags:') or line.startswith('category:'):
                        return line.split(':', 1)[1].strip()
    except Exception:
        pass
    return ""


def get_relative_path(from_dir, to_path):
    """计算从from_dir到to_path的相对路径"""
    from_dir = Path(from_dir)
    to_path = Path(to_path)
    try:
        rel = os.path.relpath(to_path, from_dir)
        # 统一使用正斜杠
        return rel.replace('\\', '/')
    except ValueError:
        return str(to_path).replace('\\', '/')


def generate_leaf_index_html(directory, md_files):
    """为叶子目录生成index.html"""
    rel_parts = directory.relative_to(ROOT).parts
    
    if len(rel_parts) >= 1:
        subject = rel_parts[0]
    else:
        subject = ""
    
    if len(rel_parts) >= 2:
        category = rel_parts[1]
    else:
        category = ""
    
    icon = get_icon(subject, category)
    
    # 构建返回首页的相对路径
    depth = len(rel_parts)
    back_href = "../" * depth
    
    # 构建标题
    if subject and category:
        title = f"{subject} - {category}"
        page_title = f"{subject} - {category} | 2028高考知识库"
    elif subject:
        title = subject
        page_title = f"{subject} | 2028高考知识库"
    else:
        title = "2028高考知识库"
        page_title = "2028高考知识库"
    
    # 构建卡片列表
    cards_html = []
    for md_file in sorted(md_files):
        md_path = directory / md_file
        display_title = extract_title_from_md(md_path) or md_file.replace('.md', '')
        tags = extract_tags_from_md(md_path)
        
        # 提取文件名中的阶段信息
        stage = ""
        if "高一筑基" in md_file:
            stage = "高一筑基"
        elif "高二深化" in md_file:
            stage = "高二深化"
        elif "高三冲刺" in md_file:
            stage = "高三冲刺"
        
        meta_parts = []
        if stage:
            meta_parts.append(stage)
        if tags:
            meta_parts.append(tags)
        
        meta = " | ".join(meta_parts) if meta_parts else "知识卡片"
        
        cards_html.append(f'''  <div class="card">
    <a href="{md_file}">📄 {display_title}</a>
    <div class="meta">{meta}</div>
  </div>''')
    
    cards_html_str = "\n".join(cards_html)
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title}</title>
<style>
  body {{ font-family: "Microsoft YaHei", sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #f5f7fa; }}
  h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
  .card {{ background: white; border-radius: 8px; padding: 15px 20px; margin: 12px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
  .card a {{ text-decoration: none; color: #2980b9; font-size: 14pt; }}
  .card a:hover {{ color: #e74c3c; }}
  .card .meta {{ color: #888; font-size: 10pt; margin-top: 5px; }}
  .back {{ display: inline-block; margin-bottom: 20px; padding: 8px 16px; background: #3498db; color: white; text-decoration: none; border-radius: 4px; }}
  .back:hover {{ background: #2980b9; }}
  .count {{ color: #7f8c8d; font-size: 12pt; margin-bottom: 20px; }}
</style>
</head>
<body>
  <a class="back" href="{back_href}">← 返回首页</a>
  <h1>{icon} {title}</h1>
  <p class="count">共 {len(md_files)} 张知识卡片</p>
{cards_html_str}
</body>
</html>'''
    
    return html


def count_md_files(subject_dir):
    """统计某科目下的md文件数量"""
    count = 0
    if subject_dir.exists():
        for root, dirs, files in os.walk(subject_dir):
            count += len([f for f in files if f.endswith('.md')])
    return count


def generate_root_index_html():
    """生成根目录index.html"""
    subjects = ["数学", "语文", "英语", "物理", "化学", "生物"]
    categories = ["核心知识网络", "典型题型与方法", "易错警示与辨析", "素材与拓展"]
    
    # 统计各科目卡片数
    subject_counts = {}
    for subject in subjects:
        subject_counts[subject] = count_md_files(ROOT / subject)
    
    # 总卡片数
    total_cards = sum(subject_counts.values()) + count_md_files(ROOT / "方法") + count_md_files(ROOT / "复盘追踪")
    
    # 构建科目导航卡片
    subject_cards = []
    for subject in subjects:
        icon = SUBJECT_ICONS.get(subject, "📁")
        count = subject_counts[subject]
        
        # 构建子目录链接
        cat_links = []
        for cat in categories:
            cat_dir = ROOT / subject / cat
            if cat_dir.exists() and any(cat_dir.iterdir()):
                cat_count = len([f for f in cat_dir.iterdir() if f.suffix == '.md'])
                cat_links.append(f'<a href="{subject}/{cat}/index.html">{cat}</a> ({cat_count})')
        
        # 英语额外链接
        if subject == "英语":
            word_review_links = []
            for sub in ["单词复习/日期词表", "单词复习/分组词表", "单词复习/小测卷", "单词复习/进度追踪"]:
                sub_dir = ROOT / subject / sub
                if sub_dir.exists():
                    sub_count = len([f for f in sub_dir.iterdir() if f.suffix == '.md'])
                    word_review_links.append(f'<a href="{subject}/{sub}/index.html">{sub.split("/")[-1]}</a> ({sub_count})')
            if word_review_links:
                cat_links.append("<br><small>单词复习: " + " | ".join(word_review_links) + "</small>")
        
        cat_links_html = "<br>".join(cat_links) if cat_links else "暂无内容"
        
        subject_cards.append(f'''  <div class="subject-card">
    <div class="subject-icon">{icon}</div>
    <div class="subject-name">{subject}</div>
    <div class="subject-count">{count} 张卡片</div>
    <div class="subject-links">
      {cat_links_html}
    </div>
  </div>''')
    
    subject_cards_html = "\n".join(subject_cards)
    
    # 方法专区
    method_dir = ROOT / "方法"
    method_count = count_md_files(method_dir) if method_dir.exists() else 0
    method_subdirs = []
    if method_dir.exists():
        for sub in sorted(method_dir.iterdir()):
            if sub.is_dir() and any(sub.iterdir()):
                sub_count = len([f for f in sub.iterdir() if f.suffix == '.md'])
                method_subdirs.append(f'<a href="方法/{sub.name}/index.html">{sub.name}</a> ({sub_count})')
    
    # 复盘追踪
    review_dir = ROOT / "复盘追踪"
    review_count = count_md_files(review_dir) if review_dir.exists() else 0
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>📚 2028高考知识库</title>
<style>
  body {{ font-family: "Microsoft YaHei", "PingFang SC", sans-serif; max-width: 1100px; margin: 0 auto; padding: 20px; background: #f0f4f8; color: #333; }}
  h1 {{ color: #1a5276; text-align: center; font-size: 28pt; margin-bottom: 10px; }}
  .subtitle {{ text-align: center; color: #5d6d7e; font-size: 12pt; margin-bottom: 30px; }}
  .stats {{ text-align: center; background: white; border-radius: 10px; padding: 15px; margin-bottom: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
  .stats span {{ display: inline-block; margin: 0 15px; font-size: 11pt; color: #555; }}
  .stats .num {{ color: #e74c3c; font-weight: bold; font-size: 14pt; }}
  .section-title {{ color: #2c3e50; font-size: 16pt; border-left: 4px solid #3498db; padding-left: 12px; margin: 30px 0 15px 0; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }}
  .subject-card {{ background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: transform 0.2s; }}
  .subject-card:hover {{ transform: translateY(-3px); box-shadow: 0 4px 16px rgba(0,0,0,0.12); }}
  .subject-icon {{ font-size: 32pt; text-align: center; margin-bottom: 8px; }}
  .subject-name {{ text-align: center; font-size: 16pt; font-weight: bold; color: #2c3e50; margin-bottom: 5px; }}
  .subject-count {{ text-align: center; color: #e74c3c; font-size: 11pt; margin-bottom: 10px; }}
  .subject-links {{ font-size: 10pt; line-height: 1.8; }}
  .subject-links a {{ color: #2980b9; text-decoration: none; }}
  .subject-links a:hover {{ color: #e74c3c; text-decoration: underline; }}
  .special-zone {{ background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 20px; }}
  .special-zone a {{ display: inline-block; margin: 5px 10px 5px 0; padding: 6px 14px; background: #eaf2f8; color: #2980b9; text-decoration: none; border-radius: 20px; font-size: 10pt; }}
  .special-zone a:hover {{ background: #3498db; color: white; }}
  .footer {{ text-align: center; margin-top: 40px; padding: 20px; color: #7f8c8d; font-size: 10pt; }}
  .footer a {{ color: #3498db; }}
  .quick-links {{ background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 20px; }}
  .quick-links a {{ display: inline-block; margin: 5px 10px 5px 0; padding: 8px 16px; background: #eaf2f8; color: #2980b9; text-decoration: none; border-radius: 6px; font-size: 11pt; }}
  .quick-links a:hover {{ background: #3498db; color: white; }}
</style>
</head>
<body>
  <h1>📚 2028高考知识库</h1>
  <p class="subtitle">2028年广东新高考六科学习知识库 | 考生：女儿 | 选科：语文、数学、英语、物理、化学、生物</p>
  
  <div class="stats">
    <span>总卡片数：<span class="num">{total_cards}</span></span>
    <span>覆盖科目：<span class="num">6</span>科</span>
    <span>知识维度：<span class="num">4</span>大模块</span>
    <span>目标分数：<span class="num">650</span>分</span>
  </div>
  
  <div class="section-title">快速导航</div>
  <div class="quick-links">
    <a href="00_知识库总索引.md">📋 知识库总索引</a>
    <a href="01_知识卡片模板.md">📝 卡片模板</a>
    <a href="02_使用规则与检索说明.md">📖 使用规则</a>
    <a href="00_知识库完善计划（650分目标）.md">🎯 完善计划</a>
  </div>
  
  <div class="section-title">六科知识库</div>
  <div class="grid">
{subject_cards_html}
  </div>
  
  <div class="section-title">🎯 方法体系</div>
  <div class="special-zone">
    <p>学习方法、心理建设、生理管理、考试策略</p>
    <p>{" | ".join(method_subdirs) if method_subdirs else "暂无分类"}</p>
    <p style="margin-top:10px"><a href="方法/index.html">→ 进入方法体系</a> ({method_count} 篇)</p>
  </div>
  
  <div class="section-title">📊 复盘追踪</div>
  <div class="special-zone">
    <p>知识掌握状态表、学习进度追踪</p>
    <p style="margin-top:10px"><a href="复盘追踪/index.html">→ 进入复盘追踪</a> ({review_count} 篇)</p>
  </div>
  
  <div class="footer">
    <p>📝 本知识库持续更新中，目标：2028 高考 650 分</p>
    <p><a href="https://github.com/goodniuniu/2028-gaokao-knowledge-base">GitHub 仓库</a> | 
       <a href="https://goodniuniu.github.io/2028-gaokao-knowledge-base">GitHub Pages</a></p>
  </div>
</body>
</html>'''
    
    return html


def main():
    """主函数：遍历目录生成所有index.html"""
    generated_count = 0
    
    # 1. 遍历所有目录，为包含.md文件的叶子目录生成index.html
    for root, dirs, files in os.walk(ROOT):
        root_path = Path(root)
        
        # 跳过.git目录
        if '.git' in root_path.parts:
            continue
        
        # 获取该目录下的md文件
        md_files = [f for f in files if f.endswith('.md')]
        
        # 如果该目录有md文件，或者是需要生成index.html的目录
        if md_files:
            index_path = root_path / 'index.html'
            
            # 不覆盖根目录的index.html（后面单独生成）
            if root_path == ROOT:
                continue
            
            html = generate_leaf_index_html(root_path, md_files)
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(html)
            generated_count += 1
            print(f"生成: {index_path.relative_to(ROOT)}")
    
    # 2. 生成根目录index.html
    root_index = ROOT / 'index.html'
    root_html = generate_root_index_html()
    with open(root_index, 'w', encoding='utf-8') as f:
        f.write(root_html)
    generated_count += 1
    print(f"生成: {root_index.relative_to(ROOT)}")
    
    print(f"\n✅ 共生成 {generated_count} 个 index.html 文件")
    return generated_count


if __name__ == '__main__':
    main()
