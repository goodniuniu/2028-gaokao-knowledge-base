# -*- coding: utf-8 -*-
"""
2028高考知识库 — 知识点示意图：基因表达载体模式图与双酶切定向插入
输出：图形库/生物/基因表达载体与双酶切.png  （嵌入卡片：基因工程基本操作）
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch, Arc
import numpy as np
import os

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150

C = {
    'red': '#C44E52', 'blue': '#4C72B0', 'green': '#55A868',
    'orange': '#DD8452', 'purple': '#8172B2', 'gray': '#7F7F7F',
    'text': '#333333', 'bg': '#FAFAFA', 'soft': '#E8E8F0',
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 5.2))
fig.patch.set_facecolor(C['bg'])

# ================= 左图：环状表达载体模式图 =================
ax1.set_xlim(-2.6, 2.6); ax1.set_ylim(-2.0, 2.0)
ax1.set_aspect('equal'); ax1.axis('off')
ax1.set_title('基因表达载体模式图（环状质粒）', fontsize=13, color=C['text'], pad=12)

# 质粒主环
ring = Circle((0, 0), 1.15, fill=False, lw=10,
             edgecolor=C['soft'], zorder=1)
ax1.add_patch(ring)

# 组件弧段（按角度布置）
def arc_component(start_deg, end_deg, color, radius=1.15, lw=10):
    a = Arc((0, 0), 2*radius, 2*radius, angle=0,
            theta1=start_deg, theta2=end_deg, lw=lw, edgecolor=color, zorder=2)
    ax1.add_patch(a)

arc_component(95, 155, C['green'])    # 启动子
arc_component(165, 255, C['red'])     # 目的基因
arc_component(262, 285, C['orange'])  # 终止子
arc_component(295, 60, C['purple'])   # 标记基因
# 复制原点：小圆点
ori_xy = (1.15*np.cos(np.radians(78)), 1.15*np.sin(np.radians(78)))
ax1.add_patch(Circle(ori_xy, 0.075, color=C['blue'], zorder=3))

# 标注（引线）
def label(xy_deg, name, color, dx, dy, ha):
    x = 1.15*np.cos(np.radians(xy_deg)); y = 1.15*np.sin(np.radians(xy_deg))
    ax1.annotate(name, xy=(x, y), xytext=(x+dx, y+dy),
                 fontsize=11, color=color, ha=ha, va='center', fontweight='bold',
                 arrowprops=dict(arrowstyle='-', color=color, lw=1.2))

label(125, '启动子\n（开转录）', C['green'], 0.25, 0.55, 'left')
label(210, '目的基因', C['red'], -0.35, -0.62, 'right')
label(273, '终止子\n（停转录）', C['orange'], 0.18, -0.72, 'left')
label(350, '标记基因\n（筛细胞）', C['purple'], 0.35, -0.28, 'left')
label(78, '复制原点', C['blue'], 0.22, 0.42, 'left')

ax1.text(0, 0.06, '质粒', ha='center', fontsize=12, color=C['gray'])
ax1.text(0, -0.12, '(可自主复制)', ha='center', fontsize=9, color=C['gray'])

# ================= 右图：双酶切 → 定向插入 =================
ax2.set_xlim(0, 10); ax2.set_ylim(0, 10)
ax2.axis('off')
ax2.set_title('双酶切：两种末端 = 一把钥匙一把锁', fontsize=13, color=C['text'], pad=12)

def gene_bar(y, x0, w, color, label_text, end_l='BamHⅠ', end_r='HindⅢ'):
    """带黏性末端凸出小段的水平条"""
    h = 0.52
    ax2.add_patch(Rectangle((x0, y-h/2), w, h, facecolor=color,
                            edgecolor='none', alpha=0.85, zorder=2))
    # 左右黏性末端凸出（错位小矩形）
    ax2.add_patch(Rectangle((x0-0.28, y-h/2-0.10), 0.30, h*0.42,
                            facecolor=color, edgecolor='none', alpha=0.55, zorder=2))
    ax2.add_patch(Rectangle((x0+w-0.02, y+h/2-0.32+0.10), 0.30, h*0.42,
                            facecolor=color, edgecolor='none', alpha=0.55, zorder=2))
    ax2.text(x0+w/2, y, label_text, ha='center', va='center',
             fontsize=11.5, color='white', fontweight='bold', zorder=3)
    ax2.text(x0-0.35, y+0.62, end_l, ha='right', fontsize=10.5, color=C['blue'])
    ax2.text(x0+w+0.35, y+0.62, end_r, ha='left', fontsize=10.5, color=C['orange'])

# ① 目的基因（两端不同末端）
gene_bar(7.6, 2.2, 5.2, C['red'], '目的基因')
ax2.text(0.35, 7.6, '①', fontsize=13, color=C['gray'], va='center')

# ② 线性化载体（两端互补末端 + 启动子方向）
y2 = 4.6
ax2.add_patch(Rectangle((1.6, y2-0.26), 6.4, 0.52, facecolor=C['blue'],
                        edgecolor='none', alpha=0.8, zorder=2))
ax2.add_patch(Rectangle((1.32, y2-0.26-0.10), 0.30, 0.22, facecolor=C['blue'],
                        edgecolor='none', alpha=0.55, zorder=2))
ax2.add_patch(Rectangle((8.0, y2+0.04+0.10), 0.30, 0.22, facecolor=C['blue'],
                        edgecolor='none', alpha=0.55, zorder=2))
ax2.text(4.8, y2, '线性化载体（MCS处切开）', ha='center', va='center',
         fontsize=11.5, color='white', fontweight='bold', zorder=3)
ax2.text(1.25, y2+0.58, 'BamHⅠ末端', ha='right', fontsize=10.5, color=C['blue'])
ax2.text(8.35, y2+0.58, 'HindⅢ末端', ha='left', fontsize=10.5, color=C['orange'])
ax2.text(0.35, y2, '②', fontsize=13, color=C['gray'], va='center')
# 启动子方向箭头（载体上）
arrow = FancyArrowPatch((1.7, y2-0.75), (3.6, y2-0.75),
                        arrowstyle='-|>', mutation_scale=16,
                        color=C['green'], lw=2)
ax2.add_patch(arrow)
ax2.text(2.6, y2-1.15, '启动子 → 转录方向', fontsize=9.5, color=C['green'], ha='center')

# ③ 连接产物
y3 = 1.7
ax2.add_patch(Rectangle((1.6, y3-0.26), 6.7, 0.52, facecolor=C['soft'],
                        edgecolor=C['gray'], lw=0.8, zorder=1))
ax2.add_patch(Rectangle((4.35, y3-0.26), 2.0, 0.52, facecolor=C['red'],
                        edgecolor='none', alpha=0.85, zorder=2))
ax2.text(3.0, y3, '载体', ha='center', va='center', fontsize=10.5, color=C['text'], zorder=3)
ax2.text(5.35, y3, '目的基因', ha='center', va='center', fontsize=10.5,
         color='white', fontweight='bold', zorder=3)
ax2.text(7.4, y3, '载体', ha='center', va='center', fontsize=10.5, color=C['text'], zorder=3)
ax2.text(0.35, y3, '③', fontsize=13, color=C['gray'], va='center')
ax2.text(5.35, y3-0.85, '两端不同 → 不能自身环化、不能插反（定向插入）',
         fontsize=10.5, color=C['text'], ha='center')

plt.tight_layout()
out = os.path.join(os.path.dirname(__file__), '生物', '基因表达载体与双酶切.png')
plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=C['bg'])
print('saved:', out)
