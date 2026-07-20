#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
draw_batch2.py — 第二批16张知识点示意图嵌入HTML知识卡片
并更新图形库索引页面
"""

import os
import re

BASE_DIR = r"C:\Users\user\WPSDrive\203612604\WPS云盘\申悦文档\AI辅助\2028高考知识库"


def figure_html(subject, filename, caption):
    """生成统一的 .figure 容器 HTML"""
    return (
        f'\n<div class="figure">\n'
        f'  <img src="../../图形库/{subject}/{filename}" alt="{caption}">\n'
        f'  <div class="figure-caption">图：{caption}</div>\n'
        f'</div>\n'
    )


# ============================================================
# 插入任务列表：每个任务包含 (目标文件相对路径, old_string, new_string)
# ============================================================
insertions = []

# ── 物理（4张） ──
insertions.append((
    "物理/核心知识网络/高一筑基_物理_核心知识网络_曲线运动与万有引力.html",
    "</blockquote>\n\n<h4>圆周运动公式体系</h4>",
    "</blockquote>\n" + figure_html("物理", "平抛运动分解.png", "平抛运动分解示意图（水平匀速+竖直自由落体）") + "\n<h4>圆周运动公式体系</h4>"
))

insertions.append((
    "物理/核心知识网络/高二深化_物理_核心知识网络_电场公式体系.html",
    "</table>\n</div>\n\n<h3>方法步骤</h3>",
    "</table>\n</div>\n" + figure_html("物理", "电场线分布.png", "常见电场线分布示意图（点电荷、等量异种/同种电荷、匀强电场）") + "\n<h3>方法步骤</h3>"
))

insertions.append((
    "物理/核心知识网络/高二深化_物理_核心知识网络_磁场公式体系.html",
    "</blockquote>\n\n<h4>4. 磁通量</h4>",
    "</blockquote>\n" + figure_html("物理", "磁场粒子圆周运动.png", "带电粒子在匀强磁场中做匀速圆周运动（洛伦兹力提供向心力）") + "\n<h4>4. 磁通量</h4>"
))

insertions.append((
    "物理/核心知识网络/高二深化_物理_核心知识网络_热学光学与原子物理.html",
    "</blockquote>\n\n<h4>热力学定律</h4>",
    "</blockquote>\n" + figure_html("物理", "理想气体PV图.png", "理想气体状态变化p-V图、V-T图、p-T图示意图") + "\n<h4>热力学定律</h4>"
))

# ── 化学（4张） ──
insertions.append((
    "化学/核心知识网络/高二深化_化学_核心知识网络_结构化学基础.html",
    "</table>\n</div>\n\n<h3>记忆口诀/技巧</h3>",
    "</table>\n</div>\n" + figure_html("化学", "元素周期律趋势.png", "元素周期律趋势图（原子半径、电离能、电负性、金属性/非金属性变化规律）") + "\n<h3>记忆口诀/技巧</h3>"
))

insertions.append((
    "化学/核心知识网络/高二深化_化学_核心知识网络_有机化学推断与合成.html",
    "</table>\n</div>\n\n<h3>合成路线设计常用策略</h3>",
    "</table>\n</div>\n" + figure_html("化学", "有机官能团对比.png", "常见有机官能团结构与性质对比") + "\n<h3>合成路线设计常用策略</h3>"
))

insertions.append((
    "化学/核心知识网络/高一筑基_化学_核心知识网络_化学计量与物质的量.html",
    "</ol>\n  <div class=\"footer\">",
    "</ol>\n\n<h2>配套图形</h2>\n\n" + figure_html("化学", "气体制取装置.png", "实验室常见气体制取装置图（固固加热/固液不加热/固液加热型）") + "\n  <div class=\"footer\">"
))

insertions.append((
    "化学/核心知识网络/高二深化_化学_核心知识网络_水溶液中的离子平衡.html",
    "</code></pre>\n\n<h3>记忆口诀/技巧</h3>",
    "</code></pre>\n" + figure_html("化学", "沉淀溶解平衡曲线.png", "沉淀溶解平衡曲线与溶度积Ksp示意图") + "\n<h3>记忆口诀/技巧</h3>"
))

# ── 生物（4张） ──
insertions.append((
    "生物/核心知识网络/高一筑基_生物_核心知识网络_细胞结构与功能.html",
    "</table>\n</div>\n\n<h4>3. 分泌蛋白合成与分泌途径（蛋白质分选）</h4>",
    "</table>\n</div>\n" + figure_html("生物", "细胞结构模式图.png", "动物细胞与植物细胞结构模式图对比") + "\n<h4>3. 分泌蛋白合成与分泌途径（蛋白质分选）</h4>"
))

insertions.append((
    "生物/核心知识网络/高一筑基_生物_核心知识网络_神经体液免疫调节.html",
    "效应器：传出神经末梢 + 所支配的肌肉或腺体</code></pre>\n\n<p>##### 兴奋在神经纤维上的传导</p>",
    "效应器：传出神经末梢 + 所支配的肌肉或腺体</code></pre>\n" + figure_html("生物", "神经反射弧.png", "神经反射弧结构示意图（感受器→传入神经→神经中枢→传出神经→效应器）") + "\n<p>##### 兴奋在神经纤维上的传导</p>"
))

insertions.append((
    "生物/核心知识网络/高一筑基_生物_核心知识网络_遗传定律体系.html",
    "适用条件：一对等位基因，细胞核遗传，有性生殖，子代数量足够多</code></pre>\n\n<p>##### 自由组合定律（两对及以上相对性状）</p>",
    "适用条件：一对等位基因，细胞核遗传，有性生殖，子代数量足够多</code></pre>\n" + figure_html("生物", "遗传定律分离比.png", "孟德尔分离定律与自由组合定律分离比示意图（3:1与9:3:3:1）") + "\n<p>##### 自由组合定律（两对及以上相对性状）</p>"
))

insertions.append((
    "生物/核心知识网络/高二深化_生物_核心知识网络_基因工程与生物技术.html",
    "</ul>\n\n<h4>四、基因工程应用</h4>",
    "</ul>\n" + figure_html("生物", "中心法则.png", "中心法则示意图（DNA复制→转录→翻译→蛋白质，以及逆转录和RNA复制）") + "\n<h4>四、基因工程应用</h4>"
))

# ── 数学（4张） ──
insertions.append((
    "数学/核心知识网络/高一筑基_数学_核心知识网络_函数零点与函数模型.html",
    "<h3>三、二分法求近似解</h3>\n<p><strong>步骤口诀</strong>：定区间，找中点，中值计算两边看；同号去，异号算，零点落在异号间；周而复始怎么办，精确度上来判断。</p>\n\n<h3>四、常见函数模型</h3>",
    "<h3>三、二分法求近似解</h3>\n<p><strong>步骤口诀</strong>：定区间，找中点，中值计算两边看；同号去，异号算，零点落在异号间；周而复始怎么办，精确度上来判断。</p>\n" + figure_html("数学", "函数零点二分法.png", "函数零点二分法求近似解示意图") + "\n<h3>四、常见函数模型</h3>"
))

insertions.append((
    "数学/典型题型与方法/高一筑基_数学_典型题型与方法_解三角形通法.html",
    "<strong>适用场景</strong>：已知三边、两边夹一角、两边一对角（求第三边）。\n</blockquote>\n\n<p>#### 3. 面积公式（多版本，灵活选择）</p>",
    "<strong>适用场景</strong>：已知三边、两边夹一角、两边一对角（求第三边）。\n</blockquote>\n" + figure_html("数学", "正余弦定理.png", "正弦定理与余弦定理解三角形示意图") + "\n<p>#### 3. 面积公式（多版本，灵活选择）</p>"
))

insertions.append((
    "数学/核心知识网络/高一筑基_数学_核心知识网络_空间几何体表面积与体积.html",
    "</blockquote>\n\n<hr>\n\n<h3>三、组合体与等积法</h3>",
    "</blockquote>\n" + figure_html("数学", "外接球示意图.png", "空间几何体外接球与内切球示意图（长方体、正方体、三棱锥外接球）") + "\n<hr>\n\n<h3>三、组合体与等积法</h3>"
))

insertions.append((
    "数学/核心知识网络/高二深化_数学_核心知识网络_二项分布超几何分布与正态分布.html",
    "</table>\n</div>\n\n<hr>",
    "</table>\n</div>\n" + figure_html("数学", "概率分布对比.png", "二项分布、超几何分布与正态分布概率密度对比示意图") + "\n<hr>"
))


# ============================================================
# 执行插入
# ============================================================

def do_insert(rel_path, old, new):
    full_path = os.path.join(BASE_DIR, rel_path)
    if not os.path.exists(full_path):
        print(f"  ⚠️ 文件不存在，跳过: {rel_path}")
        return False

    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if old not in content:
        print(f"  ⚠️ 未找到插入锚点，跳过: {rel_path}")
        return False

    if new in content:
        print(f"  ⚠️ 已包含插入内容，跳过: {rel_path}")
        return False

    new_content = content.replace(old, new, 1)

    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  ✅ 已插入: {rel_path}")
    return True


print("=" * 60)
print("开始第二批16张图片嵌入…")
print("=" * 60)

success_count = 0
failed = []

for rel_path, old, new in insertions:
    print(f"\n处理: {rel_path}")
    if do_insert(rel_path, old, new):
        success_count += 1
    else:
        failed.append(rel_path)

print("\n" + "=" * 60)
print(f"嵌入完成：成功 {success_count} / 总计 {len(insertions)}")
if failed:
    print(f"失败/跳过: {len(failed)}")
    for f in failed:
        print(f"  - {f}")
print("=" * 60)

# ============================================================
# 更新图形库 index.html
# ============================================================

INDEX_PATH = os.path.join(BASE_DIR, "图形库", "index.html")

print("\n更新图形库 index.html …")

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    idx_content = f.read()

# 第一批已有的16张（保持不动）
batch1_cards = [
    ("物理", "万有引力圆周运动.png"),
    ("物理", "受力分析_斜面物体.png"),
    ("物理", "电路串并联对比.png"),
    ("物理", "运动学_vt图像对比.png"),
    ("化学", "化学平衡移动.png"),
    ("化学", "化学键类型对比.png"),
    ("化学", "原电池示意图.png"),
    ("化学", "电子能级图.png"),
    ("生物", "DNA复制半保留.png"),
    ("生物", "光合作用过程.png"),
    ("生物", "减数分裂染色体变化.png"),
    ("生物", "有丝分裂时期.png"),
    ("数学", "三视图示意.png"),
    ("数学", "三角函数变换.png"),
    ("数学", "导数几何意义.png"),
    ("数学", "椭圆定义.png"),
]

batch2_cards = [
    ("物理", "平抛运动分解.png"),
    ("物理", "电场线分布.png"),
    ("物理", "磁场粒子圆周运动.png"),
    ("物理", "理想气体PV图.png"),
    ("化学", "元素周期律趋势.png"),
    ("化学", "有机官能团对比.png"),
    ("化学", "气体制取装置.png"),
    ("化学", "沉淀溶解平衡曲线.png"),
    ("生物", "细胞结构模式图.png"),
    ("生物", "神经反射弧.png"),
    ("生物", "遗传定律分离比.png"),
    ("生物", "中心法则.png"),
    ("数学", "函数零点二分法.png"),
    ("数学", "正余弦定理.png"),
    ("数学", "外接球示意图.png"),
    ("数学", "概率分布对比.png"),
]

def make_card(subject, filename):
    name = filename.replace('.png', '')
    return (
        f'    <div class="card">\n'
        f'      <a href="{subject}/{filename}" target="_blank">\n'
        f'        <img src="{subject}/{filename}" alt="{filename}">\n'
        f'      </a>\n'
        f'      <div class="card-title">{name}</div>\n'
        f'      <div class="card-subject">{subject}</div>\n'
        f'    </div>\n'
    )

def make_section(subject, cards):
    section_html = f'  <h2 style="color:#1a5276;margin-top:40px;border-left:4px solid #3498db;padding-left:12px;">{subject}</h2>\n'
    section_html += '  <div class="gallery">\n'
    for c in cards:
        section_html += make_card(subject, c)
    section_html += '  </div>\n'
    return section_html

# 按学科分组
physics = [c[1] for c in batch1_cards if c[0] == "物理"] + [c[1] for c in batch2_cards if c[0] == "物理"]
chemistry = [c[1] for c in batch1_cards if c[0] == "化学"] + [c[1] for c in batch2_cards if c[0] == "化学"]
biology = [c[1] for c in batch1_cards if c[0] == "生物"] + [c[1] for c in batch2_cards if c[0] == "生物"]
math = [c[1] for c in batch1_cards if c[0] == "数学"] + [c[1] for c in batch2_cards if c[0] == "数学"]

new_index = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>2028高考知识库 | 图形索引</title>
<style>
  body {
    font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    background: #f5f7fa;
    line-height: 1.8;
    color: #333;
  }
  h1 {
    color: #1a5276;
    text-align: center;
    font-size: 26pt;
    margin-bottom: 10px;
  }
  .subtitle {
    text-align: center;
    color: #5d6d7e;
    font-size: 12pt;
    margin-bottom: 30px;
  }
  .back {
    display: inline-block;
    margin-bottom: 20px;
    padding: 8px 16px;
    background: #3498db;
    color: white;
    text-decoration: none;
    border-radius: 4px;
  }
  .back:hover { background: #2980b9; }
  .gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 20px;
    margin-bottom: 40px;
  }
  .card {
    background: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    transition: transform 0.2s, box-shadow 0.2s;
  }
  .card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.12);
  }
  .card img {
    width: 100%;
    height: 180px;
    object-fit: cover;
    display: block;
    border-bottom: 1px solid #eee;
  }
  .card-title {
    padding: 12px 15px 4px;
    font-size: 12pt;
    font-weight: bold;
    color: #2c3e50;
    word-break: break-all;
  }
  .card-subject {
    padding: 0 15px 12px;
    font-size: 10pt;
    color: #e74c3c;
  }
  .footer {
    text-align: center;
    margin-top: 40px;
    padding: 20px;
    color: #7f8c8d;
    font-size: 10pt;
  }
  /* 响应式 */
  @media (max-width: 600px) {
    body { padding: 12px; }
    h1 { font-size: 20pt; }
    .gallery { grid-template-columns: 1fr; }
    .card img { height: 220px; }
  }
  @media (min-width: 601px) and (max-width: 900px) {
    .gallery { grid-template-columns: repeat(2, 1fr); }
  }
  @media (min-width: 901px) {
    .gallery { grid-template-columns: repeat(4, 1fr); }
  }
</style>
</head>
<body>
  <a class="back" href="../index.html">← 返回首页</a>
  <h1>🖼️ 图形索引</h1>
  <p class="subtitle">2028高考知识库 · 知识点示意图汇总（共 32 张）</p>

'''

new_index += make_section("物理", physics)
new_index += make_section("化学", chemistry)
new_index += make_section("生物", biology)
new_index += make_section("数学", math)

new_index += '''
  <div class="footer">
    <p>2028高考知识库 | 广东新高考六科 | 点击图片可查看大图</p>
  </div>
</body>
</html>
'''

with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write(new_index)

print(f"  ✅ 图形库 index.html 已更新为 32 张（按学科分组）")
print(f"\n脚本执行完毕。")
