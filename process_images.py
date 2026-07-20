#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量处理HTML知识卡片：
1. 嵌入16张知识点示意图
2. 增强所有HTML的响应式手机体验
3. 创建图形库总索引页面
4. 在根目录首页增加图形库入口
"""

import os
import re
import html

BASE_DIR = r"C:\Users\user\WPSDrive\203612604\WPS云盘\申悦文档\AI辅助\2028高考知识库"

# ============================================================
# 配置：16张图片的插入映射
# ============================================================
IMAGE_INSERTIONS = [
    # 物理（4张）
    {
        "html": "物理/核心知识网络/高一筑基_物理_核心知识网络_牛顿三定律与受力分析.html",
        "img_src": "../../图形库/物理/受力分析_斜面物体.png",
        "alt": "斜面物体受力分析图",
        "caption": "图：斜面物体受力分析（G=重力，N=支持力，f=摩擦力，Gx=下滑分力）",
        "insert_after": "<h3>记忆口诀/技巧</h3>",
        "insert_before": True,
    },
    {
        "html": "物理/核心知识网络/高一筑基_物理_核心知识网络_匀变速直线运动公式体系.html",
        "img_src": "../../图形库/物理/运动学_vt图像对比.png",
        "alt": "运动学v-t图像对比图",
        "caption": "图：匀变速直线运动v-t图像对比（斜率=加速度，面积=位移）",
        "insert_after": "<h3>核心公式/定理</h3>",
        "insert_before": True,
    },
    {
        "html": "物理/核心知识网络/高一筑基_物理_核心知识网络_曲线运动与万有引力.html",
        "img_src": "../../图形库/物理/万有引力圆周运动.png",
        "alt": "万有引力与圆周运动示意图",
        "caption": "图：万有引力提供圆周运动向心力（卫星轨道运动）",
        "insert_after": "<h4>万有引力定律与天体运动</h4>",
        "insert_before": False,
    },
    {
        "html": "物理/核心知识网络/高二深化_物理_核心知识网络_热学光学与原子物理.html",
        "img_src": "../../图形库/物理/电路串并联对比.png",
        "alt": "电路串并联对比图",
        "caption": "图：串联与并联电路对比（电流、电压、电阻关系）",
        "insert_after": "<hr>\n\n<h2>备注</h2>",
        "insert_before": True,
    },
    # 化学（4张）
    {
        "html": "化学/核心知识网络/高二深化_化学_核心知识网络_结构化学基础.html",
        "img_src": "../../图形库/化学/电子能级图.png",
        "alt": "电子能级图",
        "caption": "图：原子电子能级与排布示意图（1s→2s→2p→...）",
        "insert_after": "<h3>关键概念</h3>",
        "insert_before": True,
    },
    {
        "html": "化学/核心知识网络/高二深化_化学_核心知识网络_结构化学基础.html",
        "img_src": "../../图形库/化学/化学键类型对比.png",
        "alt": "化学键类型对比图",
        "caption": "图：离子键、共价键、金属键类型对比示意图",
        "insert_after": "<h3>核心公式/定理</h3>",
        "insert_before": True,
    },
    {
        "html": "化学/核心知识网络/高二深化_化学_核心知识网络_水溶液中的离子平衡.html",
        "img_src": "../../图形库/化学/化学平衡移动.png",
        "alt": "化学平衡移动示意图",
        "caption": "图：勒夏特列原理——化学平衡移动方向判断（浓度/温度/压强影响）",
        "insert_after": "<h3>方法步骤</h3>",
        "insert_before": True,
    },
    {
        "html": "化学/核心知识网络/高一筑基_化学_核心知识网络_化学反应与能量.html",
        "img_src": "../../图形库/化学/原电池示意图.png",
        "alt": "原电池工作原理示意图",
        "caption": "图：原电池工作原理（化学能→电能，电子流向与离子迁移）",
        "insert_after": "<h3>常见放热/吸热反应速记</h3>",
        "insert_before": True,
    },
    # 生物（4张）
    {
        "html": "生物/核心知识网络/高一筑基_生物_核心知识网络_有丝分裂与减数分裂.html",
        "img_src": "../../图形库/生物/有丝分裂时期.png",
        "alt": "有丝分裂各时期示意图",
        "caption": "图：有丝分裂前、中、后、末四个时期染色体行为变化",
        "insert_after": "<h4>二、有丝分裂各时期特征</h4>",
        "insert_before": False,
    },
    {
        "html": "生物/核心知识网络/高一筑基_生物_核心知识网络_有丝分裂与减数分裂.html",
        "img_src": "../../图形库/生物/DNA复制半保留.png",
        "alt": "DNA半保留复制示意图",
        "caption": "图：DNA半保留复制（S期：每个DNA复制为两个，各含一条母链）",
        "insert_after": "<h4>一、细胞周期</h4>",
        "insert_before": False,
    },
    {
        "html": "生物/核心知识网络/高一筑基_生物_核心知识网络_有丝分裂与减数分裂.html",
        "img_src": "../../图形库/生物/减数分裂染色体变化.png",
        "alt": "减数分裂染色体变化示意图",
        "caption": "图：减数分裂Ⅰ和Ⅱ染色体数目与行为变化（2n→n→2n→n）",
        "insert_after": "<h4>三、减数分裂过程（核心：染色体复制一次，细胞分裂两次）</h4>",
        "insert_before": False,
    },
    {
        "html": "生物/核心知识网络/高二深化_生物_核心知识网络_生态系统与环境保护.html",
        "img_src": "../../图形库/生物/光合作用过程.png",
        "alt": "光合作用过程示意图",
        "caption": "图：光合作用过程（光反应+暗反应，能量转化：光能→化学能→有机物）",
        "insert_after": "<h4>六、能量流动（核心考点）</h4>",
        "insert_before": False,
    },
    # 数学（4张）
    {
        "html": "数学/核心知识网络/高一筑基_数学_核心知识网络_三角恒等变换与yAsinwxφ.html",
        "img_src": "../../图形库/数学/三角函数变换.png",
        "alt": "三角函数图象变换示意图",
        "caption": "图：y=Asin(ωx+φ)图象变换（振幅A、周期2π/ω、相位φ）",
        "insert_after": "<h3>四、辅助角公式</h3>",
        "insert_before": False,
    },
    {
        "html": "数学/核心知识网络/高二深化_数学_核心知识网络_椭圆双曲线抛物线.html",
        "img_src": "../../图形库/数学/椭圆定义.png",
        "alt": "椭圆定义示意图",
        "caption": "图：椭圆定义——平面上到两定点F₁、F₂距离之和为常数2a的轨迹",
        "insert_after": "<h3>一、椭圆（以焦点在 $x$ 轴上为例）</h3>",
        "insert_before": False,
    },
    {
        "html": "数学/核心知识网络/高二深化_数学_核心知识网络_导数的运算与应用.html",
        "img_src": "../../图形库/数学/导数几何意义.png",
        "alt": "导数几何意义示意图",
        "caption": "图：导数的几何意义——切线斜率（f'(x₀)=切线在x₀处斜率）",
        "insert_after": "<h3>一、基本初等函数的导数公式</h3>",
        "insert_before": False,
    },
    {
        "html": "数学/核心知识网络/高一筑基_数学_核心知识网络_空间几何体表面积与体积.html",
        "img_src": "../../图形库/数学/三视图示意.png",
        "alt": "三视图与空间几何体示意图",
        "caption": "图：空间几何体三视图（主视图、俯视图、左视图）与直观图",
        "insert_after": "<h3>一、多面体（柱、锥）</h3>",
        "insert_before": False,
    },
]


# ============================================================
# 辅助函数
# ============================================================

def make_figure_html(img_src, alt, caption):
    return (
        f'\n<div class="figure">\n'
        f'  <img src="{img_src}" alt="{alt}">\n'
        f'  <div class="figure-caption">{caption}</div>\n'
        f'</div>\n'
    )


def add_responsive_css(content):
    """在<style>标签中添加响应式CSS和.figure/.table-wrap样式"""
    # 检查是否已有 .figure 样式
    if '.figure {' not in content:
        # 在 </style> 前插入 .figure 样式
        figure_css = (
            "\n  .figure { text-align: center; margin: 20px 0; }\n"
            "  .figure img { max-width: 100%; border: 1px solid #ddd; border-radius: 4px; }\n"
            "  .figure-caption { color: #666; font-size: 10pt; margin-top: 5px; }\n"
        )
        content = content.replace('</style>', figure_css + '</style>', 1)

    # 确保 img 样式存在
    if 'img { max-width: 100%; height: auto;' not in content:
        if 'img { max-width: 100%;' in content:
            # 已经有 max-width，但没有 height: auto，则添加
            content = content.replace(
                'img { max-width: 100%;',
                'img { max-width: 100%; height: auto;'
            )
        else:
            # 在 <style> 中添加 img 样式
            content = content.replace(
                '<style>',
                '<style>\n  img { max-width: 100%; height: auto; }'
            )

    # 添加响应式CSS
    responsive_css = """\n  /* 响应式增强 */
  @media (max-width: 600px) {
    body { padding: 12px; }
    h1 { font-size: 20pt; }
    h2 { font-size: 16pt; }
    .figure img { border-radius: 4px; }
    table { font-size: 10pt; }
  }
  .table-wrap { overflow-x: auto; }\n"""

    # 避免重复插入
    if '@media (max-width: 600px)' not in content:
        content = content.replace('</style>', responsive_css + '</style>', 1)

    return content


def wrap_tables(content):
    """将未包裹的 <table> 用 <div class="table-wrap"> 包裹"""
    # 找到所有 <table> 的位置，检查是否已被包裹
    idx = 0
    while True:
        idx = content.find('<table', idx)
        if idx == -1:
            break
        # 检查前面是否有 <div class="table-wrap">
        before = content[max(0, idx-30):idx]
        if 'table-wrap' in before:
            idx += 6
            continue
        # 找到对应的 </table>
        table_start = idx
        depth = 1
        pos = idx + 6
        while depth > 0 and pos < len(content):
            next_open = content.lower().find('<table', pos)
            next_close = content.lower().find('</table>', pos)
            if next_close == -1:
                break
            if next_open != -1 and next_open < next_close:
                depth += 1
                pos = next_open + 6
            else:
                depth -= 1
                pos = next_close + 8
        if depth == 0:
            end = pos
            original = content[table_start:end]
            wrapped = f'<div class="table-wrap">\n{original}\n</div>'
            content = content[:table_start] + wrapped + content[end:]
            idx = table_start + len(wrapped)
        else:
            idx += 6
    return content
    """将未包裹的 <table> 用 <div class="table-wrap"> 包裹"""
    # 用正则匹配没有被 <div class="table-wrap"> 包裹的 <table>
    # 策略：找到所有 <table> 标签，检查前面是否有 <div class="table-wrap">
    # 简单方法：替换所有 <table> 为 <div class="table-wrap">\n<table>
    # 但这样会重复包裹已经包裹过的

    # 更精确的方法：逐个匹配
    pattern = re.compile(r'(?<!<div class="table-wrap">\s*)<table>', re.IGNORECASE)
    # 使用循环，避免重复替换
    max_iter = 100
    for _ in range(max_iter):
        match = pattern.search(content)
        if not match:
            break
        # 找到对应的 </table>
        start = match.start()
        table_start = match.end()
        # 找闭合的 </table>
        depth = 1
        pos = table_start
        while depth > 0 and pos < len(content):
            next_open = content.find('<table', pos)
            next_close = content.find('</table>', pos)
            if next_close == -1:
                break
            if next_open != -1 and next_open < next_close:
                depth += 1
                pos = next_open + 6
            else:
                depth -= 1
                pos = next_close + 8
        if depth == 0:
            end = pos
            # 在 </table> 后面可能有换行
            # 包裹这一段
            original = content[start:end]
            wrapped = f'<div class="table-wrap">\n{original}\n</div>'
            content = content[:start] + wrapped + content[end:]
        else:
            break
    return content


def process_html_file(filepath, insertions):
    """处理单个HTML文件：插入图片 + 增强响应式"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # 插入图片
    for ins in insertions:
        figure_html = make_figure_html(ins['img_src'], ins['alt'], ins['caption'])
        marker = ins['insert_after']

        if marker in content:
            if ins.get('insert_before'):
                # 在 marker 之前插入
                if figure_html not in content:  # 避免重复插入
                    content = content.replace(marker, figure_html + marker, 1)
                    modified = True
            else:
                # 在 marker 之后插入
                if figure_html not in content:
                    content = content.replace(marker, marker + figure_html, 1)
                    modified = True
        else:
            print(f"  ⚠️ 警告：在 {filepath} 中未找到标记 '{marker[:50]}...'")

    # 响应式增强
    original_content = content
    content = add_responsive_css(content)
    content = wrap_tables(content)
    if content != original_content:
        modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


# ============================================================
# 主逻辑
# ============================================================

def main():
    # 1. 处理16个目标HTML文件的图片插入和响应式增强
    print("=" * 60)
    print("步骤1：在16个目标HTML中插入图片并增强响应式")
    print("=" * 60)

    # 按文件分组insertions
    file_insertions = {}
    for ins in IMAGE_INSERTIONS:
        html_path = os.path.join(BASE_DIR, ins['html'])
        if html_path not in file_insertions:
            file_insertions[html_path] = []
        file_insertions[html_path].append(ins)

    modified_count = 0
    for html_path, insertions in file_insertions.items():
        if os.path.exists(html_path):
            if process_html_file(html_path, insertions):
                print(f"  ✓ 已修改: {os.path.relpath(html_path, BASE_DIR)}")
                modified_count += 1
            else:
                print(f"  ○ 无变化: {os.path.relpath(html_path, BASE_DIR)}")
        else:
            print(f"  ✗ 文件不存在: {html_path}")

    print(f"\n  共修改 {modified_count} 个目标HTML文件")

    # 2. 对所有HTML文件进行响应式增强（确保所有文件都有table-wrap和响应式CSS）
    print("\n" + "=" * 60)
    print("步骤2：对所有HTML文件进行响应式增强")
    print("=" * 60)

    all_html_files = []
    for root, dirs, files in os.walk(BASE_DIR):
        # 跳过 .git 目录
        dirs[:] = [d for d in dirs if d != '.git']
        for fname in files:
            if fname.endswith('.html'):
                all_html_files.append(os.path.join(root, fname))

    responsive_modified = 0
    for html_path in all_html_files:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        content = add_responsive_css(content)
        content = wrap_tables(content)

        if content != original:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(content)
            responsive_modified += 1

    print(f"  共增强 {responsive_modified} 个HTML文件（含 table-wrap + 响应式CSS）")

    # 3. 创建图形库总索引页面
    print("\n" + "=" * 60)
    print("步骤3：创建图形库总索引页面")
    print("=" * 60)
    create_gallery_index()

    # 4. 在根目录首页增加图形库入口
    print("\n" + "=" * 60)
    print("步骤4：在根目录首页增加图形库入口")
    print("=" * 60)
    add_gallery_to_home()

    print("\n" + "=" * 60)
    print("全部任务完成！")
    print("=" * 60)


def create_gallery_index():
    """创建图形库 index.html"""
    gallery_dir = os.path.join(BASE_DIR, '图形库')
    index_path = os.path.join(gallery_dir, 'index.html')

    # 收集所有图片
    images = []
    subjects = ['物理', '化学', '生物', '数学']
    for subject in subjects:
        subj_dir = os.path.join(gallery_dir, subject)
        if os.path.isdir(subj_dir):
            for fname in sorted(os.listdir(subj_dir)):
                if fname.lower().endswith('.png'):
                    images.append({
                        'subject': subject,
                        'filename': fname,
                        'path': f'{subject}/{fname}',
                    })

    # 生成图片卡片HTML
    cards_html = ""
    for img in images:
        cards_html += f"""    <div class="card">
      <a href="{img['path']}" target="_blank">
        <img src="{img['path']}" alt="{img['filename']}">
      </a>
      <div class="card-title">{os.path.splitext(img['filename'])[0]}</div>
      <div class="card-subject">{img['subject']}</div>
    </div>
"""

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>2028高考知识库 | 图形索引</title>
<style>
  body {{
    font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    background: #f5f7fa;
    line-height: 1.8;
    color: #333;
  }}
  h1 {{
    color: #1a5276;
    text-align: center;
    font-size: 26pt;
    margin-bottom: 10px;
  }}
  .subtitle {{
    text-align: center;
    color: #5d6d7e;
    font-size: 12pt;
    margin-bottom: 30px;
  }}
  .back {{
    display: inline-block;
    margin-bottom: 20px;
    padding: 8px 16px;
    background: #3498db;
    color: white;
    text-decoration: none;
    border-radius: 4px;
  }}
  .back:hover {{ background: #2980b9; }}
  .gallery {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 20px;
    margin-bottom: 40px;
  }}
  .card {{
    background: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    transition: transform 0.2s, box-shadow 0.2s;
  }}
  .card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.12);
  }}
  .card img {{
    width: 100%;
    height: 180px;
    object-fit: cover;
    display: block;
    border-bottom: 1px solid #eee;
  }}
  .card-title {{
    padding: 12px 15px 4px;
    font-size: 12pt;
    font-weight: bold;
    color: #2c3e50;
    word-break: break-all;
  }}
  .card-subject {{
    padding: 0 15px 12px;
    font-size: 10pt;
    color: #e74c3c;
  }}
  .footer {{
    text-align: center;
    margin-top: 40px;
    padding: 20px;
    color: #7f8c8d;
    font-size: 10pt;
  }}
  /* 响应式 */
  @media (max-width: 600px) {{
    body {{ padding: 12px; }}
    h1 {{ font-size: 20pt; }}
    .gallery {{ grid-template-columns: 1fr; }}
    .card img {{ height: 220px; }}
  }}
  @media (min-width: 601px) and (max-width: 900px) {{
    .gallery {{ grid-template-columns: repeat(2, 1fr); }}
  }}
  @media (min-width: 901px) {{
    .gallery {{ grid-template-columns: repeat(4, 1fr); }}
  }}
</style>
</head>
<body>
  <a class="back" href="../index.html">← 返回首页</a>
  <h1>🖼️ 图形索引</h1>
  <p class="subtitle">2028高考知识库 · 知识点示意图汇总（共 {len(images)} 张）</p>

  <div class="gallery">
{cards_html}  </div>

  <div class="footer">
    <p>2028高考知识库 | 广东新高考六科 | 点击图片可查看大图</p>
  </div>
</body>
</html>
"""

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"  ✓ 已创建: {os.path.relpath(index_path, BASE_DIR)}")


def add_gallery_to_home():
    """在根目录 index.html 增加图形库入口"""
    home_path = os.path.join(BASE_DIR, 'index.html')
    with open(home_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 在"快速导航"区域增加图形库入口
    marker = '<a href="00_知识库完善计划（650分目标）.html">🎯 完善计划</a>'
    gallery_link = '\n    <a href="图形库/index.html">🖼️ 图形索引</a>'

    if '图形库/index.html' not in content:
        if marker in content:
            content = content.replace(marker, marker + gallery_link)
            with open(home_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ 已在首页快速导航添加图形库入口")
        else:
            print(f"  ⚠️ 未找到标记，无法添加图形库入口")
    else:
        print(f"  ○ 图形库入口已存在")


if __name__ == '__main__':
    main()
