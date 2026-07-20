# -*- coding: utf-8 -*-
"""
2028高考知识库 — 第二批知识点示意图绘制脚本
使用 LaTeX 数学模式处理上下标，确保字形正确
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Arc, Circle, Rectangle, Polygon, FancyBboxPatch
import numpy as np
import os

# ===================== 全局设置 =====================
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150

COLORS = {
    'red': '#C44E52', 'blue': '#4C72B0', 'green': '#55A868',
    'orange': '#DD8452', 'purple': '#8172B2', 'gray': '#7F7F7F',
    'light_gray': '#CCCCCC', 'bg': '#FAFAFA', 'text': '#333333'
}

OUTPUT_DIR = r"C:\Users\user\WPSDrive\203612604\WPS云盘\申悦文档\AI辅助\2028高考知识库\图形库"


def savefig(fig, subdir, filename):
    path = os.path.join(OUTPUT_DIR, subdir, filename)
    fig.savefig(path, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  已保存: {subdir}/{filename}")


# ============================================================
# 物理 (4张)
# ============================================================

def draw_physics_1():
    """平抛运动分解图"""
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(-1, 11); ax.set_ylim(-1, 7)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_facecolor(COLORS['bg']); fig.patch.set_facecolor('white')

    # 坐标轴
    ax.annotate('', xy=(10, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
    ax.annotate('', xy=(0, 6), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
    ax.text(10.2, -0.3, 'x', fontsize=14)
    ax.text(-0.4, 6.2, 'y', fontsize=14)
    ax.text(-0.6, -0.5, 'O', fontsize=14, fontweight='bold')

    # 抛物线轨迹
    v0 = 3.0
    g = 2.0
    t = np.linspace(0, 2.5, 200)
    x = v0 * t
    y = 0.5 * g * t ** 2
    ax.plot(x, y, color=COLORS['blue'], linewidth=2.5)

    # P点
    tp = 1.5
    px = v0 * tp
    py = 0.5 * g * tp ** 2
    ax.plot(px, py, 'o', color=COLORS['red'], markersize=10, zorder=5)
    ax.text(px + 0.2, py + 0.3, 'P', fontsize=14, color=COLORS['red'], fontweight='bold')

    # 水平速度 v0
    ax.annotate('', xy=(px + 2, py), xytext=(px, py),
                arrowprops=dict(arrowstyle='->', color=COLORS['green'], lw=2.5))
    ax.text(px + 1.0, py + 0.4, r'$v_0$ (水平匀速)', fontsize=12, color=COLORS['green'], fontweight='bold')

    # 竖直速度 v_y = gt
    ax.annotate('', xy=(px, py + 2.5), xytext=(px, py),
                arrowprops=dict(arrowstyle='->', color=COLORS['orange'], lw=2.5))
    ax.text(px + 0.3, py + 1.3, r'$v_y = gt$ (竖直向下)', fontsize=12, color=COLORS['orange'], fontweight='bold')

    # 合速度
    vx, vy = 2.0, 2.5
    ax.annotate('', xy=(px + vx, py + vy), xytext=(px, py),
                arrowprops=dict(arrowstyle='->', color=COLORS['purple'], lw=2))
    ax.text(px + vx + 0.2, py + vy + 0.2, 'v', fontsize=13, color=COLORS['purple'], fontweight='bold')

    # 位移虚线
    ax.plot([0, px], [0, py], '--', color=COLORS['gray'], linewidth=1.5, alpha=0.6)
    ax.plot([0, px], [0, 0], '--', color=COLORS['light_gray'], linewidth=1.5, alpha=0.6)
    ax.plot([px, px], [0, py], '--', color=COLORS['light_gray'], linewidth=1.5, alpha=0.6)

    # 标注公式
    ax.text(6, 5.5, r'水平方向: $x = v_0 t$ (匀速直线)', fontsize=13, color=COLORS['green'],
            bbox=dict(boxstyle='round', facecolor='#E8F8F5', edgecolor=COLORS['green'], alpha=0.8))
    ax.text(6, 4.5, r'竖直方向: $y = \frac{1}{2}gt^2$ (自由落体)', fontsize=13, color=COLORS['orange'],
            bbox=dict(boxstyle='round', facecolor='#FEF9E7', edgecolor=COLORS['orange'], alpha=0.8))

    ax.set_title('平抛运动分解图', fontsize=18, fontweight='bold', pad=15)
    savefig(fig, '物理', '平抛运动分解.png')


def draw_physics_2():
    """电场线分布图"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.patch.set_facecolor('white')

    # 左半：正点电荷
    ax = ax1
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_facecolor(COLORS['bg'])

    q = Circle((0, 0), 0.3, facecolor=COLORS['red'], edgecolor='darkred', linewidth=2)
    ax.add_patch(q)
    ax.text(0, 0, '+', ha='center', va='center', fontsize=18, fontweight='bold', color='white')
    ax.text(0, -0.7, r'$+Q$', ha='center', fontsize=14, color=COLORS['red'], fontweight='bold')

    for angle in np.linspace(0, 2*np.pi, 12, endpoint=False):
        r_start = 0.4
        r_end = 2.8
        x1, y1 = r_start * np.cos(angle), r_start * np.sin(angle)
        x2, y2 = r_end * np.cos(angle), r_end * np.sin(angle)
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=COLORS['blue'], lw=1.5))

    for r in [1.0, 1.8, 2.6]:
        circle = Circle((0, 0), r, fill=False, edgecolor=COLORS['gray'], linewidth=1, linestyle='--', alpha=0.6)
        ax.add_patch(circle)
    ax.text(2.4, 2.6, '等势面', fontsize=10, color=COLORS['gray'])
    ax.set_title('正点电荷电场', fontsize=14, fontweight='bold', pad=10)

    # 右半：等量异种电荷
    ax = ax2
    ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_facecolor(COLORS['bg'])

    q1 = Circle((-1.5, 0), 0.3, facecolor=COLORS['red'], edgecolor='darkred', linewidth=2)
    ax.add_patch(q1)
    ax.text(-1.5, 0, '+', ha='center', va='center', fontsize=18, fontweight='bold', color='white')
    ax.text(-1.5, -0.7, r'$+Q$', ha='center', fontsize=14, color=COLORS['red'], fontweight='bold')

    q2 = Circle((1.5, 0), 0.3, facecolor=COLORS['blue'], edgecolor='darkblue', linewidth=2)
    ax.add_patch(q2)
    ax.text(1.5, 0, r'$-$', ha='center', va='center', fontsize=18, fontweight='bold', color='white')
    ax.text(1.5, -0.7, r'$-Q$', ha='center', fontsize=14, color=COLORS['blue'], fontweight='bold')

    # 电场线从正到负
    for angle in np.linspace(-60, 60, 7):
        r = 2.5
        rad = np.radians(angle)
        x1 = -1.5 + 0.4 * np.cos(rad)
        y1 = 0.4 * np.sin(rad)
        x2 = 1.5 - 0.4 * np.cos(rad)
        y2 = -0.4 * np.sin(rad)
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=COLORS['green'], lw=1.5, connectionstyle='arc3,rad=0.15'))

    # 中间连线
    ax.plot([-1.2, 1.2], [0, 0], color=COLORS['green'], linewidth=1.5)
    ax.annotate('', xy=(0.1, 0), xytext=(-0.1, 0),
                arrowprops=dict(arrowstyle='->', color=COLORS['green'], lw=1.5))

    # 等势面
    for r in [0.8, 1.6]:
        c1 = Circle((-1.5, 0), r, fill=False, edgecolor=COLORS['gray'], linewidth=1, linestyle='--', alpha=0.5)
        c2 = Circle((1.5, 0), r, fill=False, edgecolor=COLORS['gray'], linewidth=1, linestyle='--', alpha=0.5)
        ax.add_patch(c1); ax.add_patch(c2)

    ax.set_title('等量异种电荷电场', fontsize=14, fontweight='bold', pad=10)
    fig.suptitle('电场线分布图', fontsize=18, fontweight='bold', y=0.98)
    savefig(fig, '物理', '电场线分布.png')


def draw_physics_3():
    """磁场中带电粒子圆周运动"""
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(-5, 5); ax.set_ylim(-4, 4)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_facecolor(COLORS['bg']); fig.patch.set_facecolor('white')

    # 圆形磁场区域（虚线）
    R = 2.5
    mag_field = Circle((0, 0), R, fill=False, edgecolor=COLORS['gray'], linewidth=2, linestyle='--')
    ax.add_patch(mag_field)
    ax.text(0, 0, r'$\times$' + '\n' + r'$\times$' + '\n' + r'$\times$', ha='center', va='center',
            fontsize=20, color=COLORS['light_gray'], alpha=0.5)
    ax.text(2.7, 2.7, '匀强磁场 B', fontsize=12, color=COLORS['gray'], fontstyle='italic')

    # 粒子轨迹：半圆
    theta = np.linspace(0, np.pi, 200)
    r_orbit = 2.0
    ox, oy = 0, -0.5  # 圆心偏移
    x_traj = ox + r_orbit * np.cos(theta)
    y_traj = oy + r_orbit * np.sin(theta)
    ax.plot(x_traj, y_traj, color=COLORS['blue'], linewidth=2.5)

    # 入射点
    entry_x, entry_y = ox + r_orbit * np.cos(0), oy + r_orbit * np.sin(0)
    ax.plot(entry_x, entry_y, 'o', color=COLORS['green'], markersize=10, zorder=5)
    ax.text(entry_x + 0.3, entry_y - 0.5, '入射', fontsize=11, color=COLORS['green'])

    # 入射速度
    ax.annotate('', xy=(entry_x - 1.2, entry_y), xytext=(entry_x, entry_y),
                arrowprops=dict(arrowstyle='->', color=COLORS['green'], lw=2.5))
    ax.text(entry_x - 0.8, entry_y + 0.4, r'$v$', fontsize=14, color=COLORS['green'], fontweight='bold')

    # 出射点
    exit_x, exit_y = ox + r_orbit * np.cos(np.pi), oy + r_orbit * np.sin(np.pi)
    ax.plot(exit_x, exit_y, 'o', color=COLORS['orange'], markersize=10, zorder=5)
    ax.text(exit_x - 0.5, exit_y + 0.3, '出射', fontsize=11, color=COLORS['orange'])

    # 出射速度
    ax.annotate('', xy=(exit_x - 1.2, exit_y), xytext=(exit_x, exit_y),
                arrowprops=dict(arrowstyle='->', color=COLORS['orange'], lw=2.5))
    ax.text(exit_x - 0.8, exit_y - 0.5, r'$v$', fontsize=14, color=COLORS['orange'], fontweight='bold')

    # 圆心 O
    ax.plot(ox, oy, 'x', color=COLORS['red'], markersize=12, markeredgewidth=2)
    ax.text(ox + 0.2, oy - 0.4, 'O', fontsize=14, color=COLORS['red'], fontweight='bold')

    # 半径
    ax.plot([ox, entry_x], [oy, entry_y], '--', color=COLORS['purple'], linewidth=1.5, alpha=0.7)
    ax.text((ox + entry_x)/2 + 0.2, (oy + entry_y)/2, r'$r = \frac{mv}{qB}$', fontsize=13,
            color=COLORS['purple'], fontweight='bold')

    # 洛伦兹力（指向圆心）
    mid_theta = np.pi / 2
    mid_x = ox + r_orbit * np.cos(mid_theta)
    mid_y = oy + r_orbit * np.sin(mid_theta)
    ax.annotate('', xy=(ox, oy), xytext=(mid_x, mid_y),
                arrowprops=dict(arrowstyle='->', color=COLORS['red'], lw=2.5))
    mx = (mid_x + ox) / 2 + 0.2
    my = (mid_y + oy) / 2 + 0.3
    ax.text(mx, my, r'$F = qvB$', fontsize=13, color=COLORS['red'], fontweight='bold')

    ax.set_title('磁场中带电粒子圆周运动', fontsize=18, fontweight='bold', pad=15)
    savefig(fig, '物理', '磁场粒子圆周运动.png')


def draw_physics_4():
    """理想气体状态变化图 (P-V图)"""
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_facecolor(COLORS['bg']); fig.patch.set_facecolor('white')

    V = np.linspace(0.5, 8, 200)

    # 等温线（双曲线）PV = nRT = const
    T1, T2 = 5.0, 10.0
    ax.plot(V, T1 / V, color=COLORS['blue'], linewidth=2.5, label='等温线')
    ax.plot(V, T2 / V, color=COLORS['blue'], linewidth=2.5, linestyle='--', alpha=0.6)

    # 等压线（水平线）
    ax.axhline(y=2.0, xmin=0.05, xmax=0.95, color=COLORS['green'], linewidth=2.5, label='等压线')
    ax.annotate('', xy=(7, 2.0), xytext=(5, 2.0),
                arrowprops=dict(arrowstyle='->', color=COLORS['green'], lw=2))

    # 等容线（竖直线）
    ax.axvline(x=3.0, ymin=0.05, ymax=0.95, color=COLORS['red'], linewidth=2.5, label='等容线')
    ax.annotate('', xy=(3.0, 6), xytext=(3.0, 4),
                arrowprops=dict(arrowstyle='->', color=COLORS['red'], lw=2))

    # 等温线箭头
    ax.annotate('', xy=(6, T1/6), xytext=(4.5, T1/4.5),
                arrowprops=dict(arrowstyle='->', color=COLORS['blue'], lw=2))

    # 标注
    ax.text(5.5, 5.5, r'$PV = nRT = $常数', fontsize=13, color=COLORS['blue'],
            bbox=dict(boxstyle='round', facecolor='#EBF5FB', edgecolor=COLORS['blue'], alpha=0.8))
    ax.text(6.5, 2.3, '等压膨胀', fontsize=11, color=COLORS['green'])
    ax.text(3.2, 6.5, '等容升压', fontsize=11, color=COLORS['red'])

    ax.axhline(y=0, color='black', linewidth=0.8)
    ax.axvline(x=0, color='black', linewidth=0.8)
    ax.set_xlabel('体积 V', fontsize=14)
    ax.set_ylabel('压强 P', fontsize=14)
    ax.set_title('理想气体状态变化图 (P-V 图)', fontsize=18, fontweight='bold', pad=15)
    ax.legend(loc='upper right', fontsize=12, framealpha=0.9)
    ax.set_xlim(-0.3, 8.5); ax.set_ylim(-0.3, 8)
    ax.grid(True, alpha=0.3)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    savefig(fig, '物理', '理想气体PV图.png')


# ============================================================
# 化学 (4张)
# ============================================================

def draw_chemistry_1():
    """元素周期律趋势图"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    fig.patch.set_facecolor('white')

    Z = np.arange(1, 21)
    # 模拟原子半径：周期减小，族增大
    radius = np.array([
        3.0, 2.5,  # H, He
        2.8, 2.2, 1.8, 1.6, 1.5, 1.4, 1.35, 1.3,  # Li-Ne
        2.6, 2.0, 1.7, 1.5, 1.45, 1.4, 1.35, 1.3,  # Na-Ar
        2.5, 2.1  # K, Ca
    ])
    # 金属性
    metal = np.array([
        0.5, 0.3,
        3.0, 2.5, 2.2, 2.0, 1.8, 1.5, 1.2, 0.8,
        2.8, 2.3, 1.9, 1.7, 1.6, 1.5, 1.3, 1.0,
        2.7, 2.4
    ])
    nonmetal = 3.5 - metal

    elements = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
                'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca']

    # 上半：原子半径
    ax = ax1
    ax.set_facecolor(COLORS['bg'])
    ax.plot(Z, radius, 'o-', color=COLORS['blue'], linewidth=2, markersize=6, label='原子半径')
    ax.fill_between(Z, radius, alpha=0.1, color=COLORS['blue'])

    # 周期分界线
    for x in [2.5, 10.5, 18.5]:
        ax.axvline(x=x, color=COLORS['light_gray'], linestyle='--', linewidth=1)
    ax.text(1.5, 3.2, '第1周期', ha='center', fontsize=10, color=COLORS['gray'])
    ax.text(6.5, 3.2, '第2周期', ha='center', fontsize=10, color=COLORS['gray'])
    ax.text(14.5, 3.2, '第3周期', ha='center', fontsize=10, color=COLORS['gray'])

    # 箭头标注趋势
    ax.annotate('', xy=(10, 2.0), xytext=(3, 2.0),
                arrowprops=dict(arrowstyle='->', color=COLORS['red'], lw=2))
    ax.text(6.5, 2.2, '同周期从左到右递减', fontsize=11, color=COLORS['red'], ha='center')

    ax.set_xticks(Z)
    ax.set_xticklabels(elements, fontsize=9)
    ax.set_ylabel('相对原子半径', fontsize=12)
    ax.set_title('原子半径变化趋势', fontsize=14, fontweight='bold', pad=10)
    ax.set_ylim(0.8, 3.5)
    ax.grid(True, alpha=0.3)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

    # 下半：金属性/非金属性
    ax = ax2
    ax.set_facecolor(COLORS['bg'])
    ax.plot(Z, metal, 's-', color=COLORS['orange'], linewidth=2, markersize=5, label='金属性')
    ax.plot(Z, nonmetal, '^-', color=COLORS['green'], linewidth=2, markersize=5, label='非金属性')

    for x in [2.5, 10.5, 18.5]:
        ax.axvline(x=x, color=COLORS['light_gray'], linestyle='--', linewidth=1)

    ax.annotate('', xy=(10, 1.5), xytext=(3, 1.5),
                arrowprops=dict(arrowstyle='->', color=COLORS['orange'], lw=2))
    ax.text(6.5, 1.7, '金属性减弱', fontsize=11, color=COLORS['orange'], ha='center')
    ax.annotate('', xy=(3, 2.5), xytext=(10, 2.5),
                arrowprops=dict(arrowstyle='->', color=COLORS['green'], lw=2))
    ax.text(6.5, 2.7, '非金属性增强', fontsize=11, color=COLORS['green'], ha='center')

    ax.set_xticks(Z)
    ax.set_xticklabels(elements, fontsize=9)
    ax.set_ylabel('相对强弱', fontsize=12)
    ax.set_xlabel('原子序数', fontsize=12)
    ax.set_title('金属性/非金属性变化趋势', fontsize=14, fontweight='bold', pad=10)
    ax.legend(loc='upper right', fontsize=11)
    ax.set_ylim(0, 3.5)
    ax.grid(True, alpha=0.3)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

    fig.suptitle('元素周期律趋势图', fontsize=18, fontweight='bold', y=0.98)
    savefig(fig, '化学', '元素周期律趋势.png')


def draw_chemistry_2():
    """有机官能团结构对比"""
    fig, axes = plt.subplots(1, 4, figsize=(14, 5))
    fig.patch.set_facecolor('white')

    groups = [
        ('羟基', r'$-OH$', r'$CH_3CH_2OH$', '乙醇', COLORS['blue']),
        ('羧基', r'$-COOH$', r'$CH_3COOH$', '乙酸', COLORS['red']),
        ('醛基', r'$-CHO$', r'$CH_3CHO$', '乙醛', COLORS['green']),
        ('酯基', r'$-COO-$', r'$CH_3COOCH_2CH_3$', '乙酸乙酯', COLORS['purple']),
    ]

    for ax, (name, group, formula, compound, color) in zip(axes, groups):
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_facecolor('#F8F9FA')

        # 方框
        rect = FancyBboxPatch((0.05, 0.05), 0.9, 0.9,
                               boxstyle='round,pad=0.02', facecolor='white',
                               edgecolor=color, linewidth=2.5)
        ax.add_patch(rect)

        # 官能团名称
        ax.text(0.5, 0.85, name, ha='center', va='center', fontsize=15,
                fontweight='bold', color=color)

        # 官能团结构式（红色高亮）
        ax.text(0.5, 0.62, group, ha='center', va='center', fontsize=16,
                color=COLORS['red'], fontweight='bold')

        # 化合物结构式
        ax.text(0.5, 0.38, formula, ha='center', va='center', fontsize=14, color=COLORS['text'])

        # 化合物名称
        ax.text(0.5, 0.15, compound, ha='center', va='center', fontsize=13,
                color=COLORS['gray'], fontstyle='italic')

    fig.suptitle('有机官能团结构对比', fontsize=18, fontweight='bold', y=0.98)
    savefig(fig, '化学', '有机官能团对比.png')


def draw_chemistry_3():
    """化学实验装置（制取气体）"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.patch.set_facecolor('white')

    # 左：固固加热制气（制O₂）
    ax = ax1
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3.5)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_facecolor(COLORS['bg'])

    # 大试管（倾斜）
    tube = Polygon([[-1.8, -0.5], [1.2, 1.5], [1.4, 1.2], [-1.6, -0.8]],
                   closed=True, facecolor='#E8F8F5', edgecolor=COLORS['blue'], linewidth=2.5)
    ax.add_patch(tube)
    ax.text(-0.2, 0.6, r'$KMnO_4$', ha='center', fontsize=11, color=COLORS['blue'])

    # 棉花
    ax.plot([-1.4, 1.0], [1.35, 1.35], color='#D5DBDB', linewidth=4)

    # 酒精灯
    lamp_body = Rectangle((-2.2, -2.0), 0.8, 1.2, facecolor='#FADBD8', edgecolor=COLORS['red'], linewidth=1.5)
    ax.add_patch(lamp_body)
    ax.plot([-1.95, -1.55], [-0.8, -0.8], color=COLORS['gray'], linewidth=1.5)
    ax.plot([-1.75, -1.75], [-0.8, -0.4], color=COLORS['gray'], linewidth=1.5)
    # 火焰
    flame = Polygon([[-1.85, -0.4], [-1.75, -0.1], [-1.65, -0.4]],
                    facecolor='#F39C12', edgecolor='#E67E22', linewidth=1)
    ax.add_patch(flame)
    ax.text(-1.75, -2.3, '酒精灯', ha='center', fontsize=10, color=COLORS['red'])

    # 铁架台（简化）
    ax.plot([-2.5, -2.5], [-2.5, 2.5], color=COLORS['gray'], linewidth=2)
    ax.plot([-2.7, -2.3], [2.5, 2.5], color=COLORS['gray'], linewidth=2)
    ax.plot([-2.7, -2.3], [-2.5, -2.5], color=COLORS['gray'], linewidth=2)
    ax.plot([-2.5, -1.6], [0.8, 0.8], color=COLORS['gray'], linewidth=2)
    ax.text(-2.8, 0, '铁架台', ha='center', fontsize=10, color=COLORS['gray'], rotation=90)

    # 导管
    ax.plot([1.3, 2.2], [1.35, 1.35], color=COLORS['gray'], linewidth=2)
    ax.plot([2.2, 2.2], [1.35, 0.5], color=COLORS['gray'], linewidth=2)

    # 集气瓶（排水法）
    jar = Rectangle((1.8, -1.5), 1.0, 2.0, facecolor='#D4E6F1', edgecolor=COLORS['blue'],
                    linewidth=2, alpha=0.4)
    ax.add_patch(jar)
    ax.plot([1.8, 2.8], [0.3, 0.3], color=COLORS['blue'], linewidth=1.5)
    ax.text(2.3, -0.3, '水', ha='center', fontsize=10, color=COLORS['blue'])
    ax.plot([2.2, 2.2], [0.5, -0.2], color=COLORS['gray'], linewidth=2)
    ax.text(2.3, -1.8, '集气瓶', ha='center', fontsize=10, color=COLORS['blue'])

    ax.set_title('固固加热制气\n(如制 $O_2$)', fontsize=13, fontweight='bold', pad=10)

    # 右：固液不加热制气（制CO₂）
    ax = ax2
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3.5)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_facecolor(COLORS['bg'])

    # 锥形瓶
    flask = Polygon([[-1.0, -1.5], [1.0, -1.5], [1.3, 0.5], [0.3, 1.0], [-0.3, 1.0], [-1.3, 0.5]],
                    closed=True, facecolor='#E8F8F5', edgecolor=COLORS['green'], linewidth=2.5)
    ax.add_patch(flask)
    ax.text(0, -0.3, r'$CaCO_3$' + '\n+稀HCl', ha='center', fontsize=10, color=COLORS['green'])

    # 长颈漏斗
    ax.plot([0.5, 0.5], [1.0, 2.0], color=COLORS['gray'], linewidth=2)
    ax.plot([0.3, 0.7], [2.0, 2.0], color=COLORS['gray'], linewidth=2)
    ax.plot([0.3, 0.7], [2.0, 1.8], color=COLORS['gray'], linewidth=1)
    ax.text(0.9, 1.5, '长颈漏斗', fontsize=10, color=COLORS['gray'])

    # 导管
    ax.plot([0.0, 1.5], [1.0, 1.0], color=COLORS['gray'], linewidth=2)
    ax.plot([1.5, 1.5], [1.0, 0.2], color=COLORS['gray'], linewidth=2)

    # 集气瓶（向上排空气法）
    jar2 = Rectangle((1.3, -1.5), 1.0, 1.7, facecolor='white', edgecolor=COLORS['blue'], linewidth=2)
    ax.add_patch(jar2)
    ax.plot([1.3, 2.3], [-1.5, -1.5], color=COLORS['blue'], linewidth=2)
    ax.plot([1.3, 2.3], [0.2, 0.2], color=COLORS['blue'], linewidth=2)
    ax.plot([1.3, 1.3], [-1.5, 0.2], color=COLORS['blue'], linewidth=2)
    ax.plot([2.3, 2.3], [-1.5, 0.2], color=COLORS['blue'], linewidth=2)
    ax.plot([1.5, 1.5], [0.2, -0.2], color=COLORS['gray'], linewidth=2)
    ax.text(1.8, -0.6, r'$CO_2$', ha='center', fontsize=11, color=COLORS['gray'])
    ax.text(1.8, -1.8, '集气瓶', ha='center', fontsize=10, color=COLORS['blue'])

    # 向上排空气箭头
    ax.annotate('', xy=(2.5, 0.0), xytext=(2.5, -0.8),
                arrowprops=dict(arrowstyle='->', color=COLORS['gray'], lw=1.5))
    ax.text(2.7, -0.4, '空气', fontsize=9, color=COLORS['gray'])

    ax.set_title('固液不加热制气\n(如制 $CO_2$)', fontsize=13, fontweight='bold', pad=10)

    fig.suptitle('化学实验装置：气体制取', fontsize=18, fontweight='bold', y=0.98)
    savefig(fig, '化学', '气体制取装置.png')


def draw_chemistry_4():
    """沉淀溶解平衡曲线"""
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_facecolor(COLORS['bg']); fig.patch.set_facecolor('white')

    # 坐标轴
    x = np.linspace(-1, 6, 200)
    y = 4 - x  # Ksp 直线

    ax.fill_between(x, y, 6, where=(y <= 6), alpha=0.15, color=COLORS['red'], label='过饱和区（有沉淀）')
    ax.fill_between(x, -1, y, where=(y >= -1), alpha=0.15, color=COLORS['green'], label='不饱和区（溶解）')

    ax.plot(x, y, color=COLORS['blue'], linewidth=2.5, label=r'$K_{sp}$ 曲线')

    # 标注点
    ax.plot(2, 2, 'o', color=COLORS['blue'], markersize=10, zorder=5)
    ax.text(2.2, 2.2, r'$Q = K_{sp}$', fontsize=12, color=COLORS['blue'], fontweight='bold')

    ax.plot(1, 1, 's', color=COLORS['green'], markersize=8)
    ax.text(1.2, 0.7, r'$Q < K_{sp}$', fontsize=11, color=COLORS['green'])

    ax.plot(3.5, 1.5, '^', color=COLORS['red'], markersize=8)
    ax.text(3.7, 1.8, r'$Q > K_{sp}$', fontsize=11, color=COLORS['red'])

    # 区域标注
    ax.text(4.5, 5, '过饱和区', fontsize=13, color=COLORS['red'], fontweight='bold')
    ax.text(0.5, 0.5, '不饱和区', fontsize=13, color=COLORS['green'], fontweight='bold')

    # Ksp值标注
    ax.text(4, 3.5, r'$K_{sp} = [Ag^+][Cl^-]$', fontsize=14, color=COLORS['blue'],
            bbox=dict(boxstyle='round', facecolor='#EBF5FB', edgecolor=COLORS['blue'], alpha=0.9))
    ax.text(4, 2.5, r'$K_{sp}(AgCl) = 1.8 \times 10^{-10}$', fontsize=12, color=COLORS['gray'])

    ax.axhline(y=0, color='black', linewidth=0.8)
    ax.axvline(x=0, color='black', linewidth=0.8)
    ax.set_xlabel(r'$-\log[c($阳离子$)]$', fontsize=14)
    ax.set_ylabel(r'$-\log[c($阴离子$)]$', fontsize=14)
    ax.set_title('沉淀溶解平衡曲线', fontsize=18, fontweight='bold', pad=15)
    ax.legend(loc='upper right', fontsize=11, framealpha=0.9)
    ax.set_xlim(-0.5, 6); ax.set_ylim(-0.5, 6)
    ax.grid(True, alpha=0.3)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    savefig(fig, '化学', '沉淀溶解平衡曲线.png')


# ============================================================
# 生物 (4张)
# ============================================================

def draw_biology_1():
    """细胞结构模式图"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 7))
    fig.patch.set_facecolor('white')

    def draw_organelle(ax, x, y, name, color, shape='circle', size=0.25):
        if shape == 'circle':
            c = Circle((x, y), size, facecolor=color, edgecolor='white', linewidth=1.5, alpha=0.8)
            ax.add_patch(c)
        elif shape == 'ellipse':
            e = mpatches.Ellipse((x, y), size*2, size, facecolor=color, edgecolor='white', linewidth=1.5, alpha=0.8)
            ax.add_patch(e)
        elif shape == 'rect':
            r = Rectangle((x-size, y-size/2), size*2, size, facecolor=color, edgecolor='white', linewidth=1.5, alpha=0.8)
            ax.add_patch(r)
        ax.text(x, y - size - 0.15, name, ha='center', fontsize=8, color=COLORS['text'])

    # 左：动物细胞
    ax = ax1
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_facecolor(COLORS['bg'])

    cell = Circle((0, 0), 2.5, facecolor='#FCE4EC', edgecolor=COLORS['red'], linewidth=2.5)
    ax.add_patch(cell)
    ax.text(0, 2.8, '动物细胞', ha='center', fontsize=14, fontweight='bold', color=COLORS['red'])

    # 细胞核
    nucleus = Circle((0, 0.3), 0.7, facecolor='#D7BDE2', edgecolor='white', linewidth=1.5)
    ax.add_patch(nucleus)
    ax.text(0, 0.3, '细胞核', ha='center', va='center', fontsize=9, color=COLORS['text'])

    # 中心体
    centriole = Circle((0.8, -1.2), 0.15, facecolor='#F9E79F', edgecolor='white', linewidth=1.5)
    ax.add_patch(centriole)
    ax.text(0.8, -1.55, '中心体', ha='center', fontsize=8, color=COLORS['text'])

    # 线粒体
    mito = mpatches.Ellipse((-1.0, 1.0), 0.6, 0.3, angle=30, facecolor='#AED6F1', edgecolor='white', linewidth=1.5)
    ax.add_patch(mito)
    ax.text(-1.0, 0.7, '线粒体', ha='center', fontsize=8, color=COLORS['text'])

    # 其他细胞器
    draw_organelle(ax, -0.8, -0.8, '核糖体', '#F5B7B1', 'circle', 0.12)
    draw_organelle(ax, 1.2, 0.8, '高尔基体', '#A9DFBF', 'rect', 0.2)
    draw_organelle(ax, -1.3, -0.3, '内质网', '#D5A6BD', 'ellipse', 0.2)

    ax.text(0, -2.8, '无细胞壁、叶绿体、液泡', ha='center', fontsize=10, color=COLORS['gray'], fontstyle='italic')

    # 右：植物细胞
    ax = ax2
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_facecolor(COLORS['bg'])

    cell_wall = Rectangle((-2.5, -2.5), 5, 5, facecolor='#E8F8F5', edgecolor=COLORS['green'], linewidth=3)
    ax.add_patch(cell_wall)
    cell_mem = Rectangle((-2.2, -2.2), 4.4, 4.4, facecolor='#D5F5E3', edgecolor=COLORS['green'],
                         linewidth=1.5, linestyle='--')
    ax.add_patch(cell_mem)
    ax.text(0, 2.8, '植物细胞', ha='center', fontsize=14, fontweight='bold', color=COLORS['green'])

    # 细胞核
    nucleus2 = Circle((0, 0.3), 0.7, facecolor='#D7BDE2', edgecolor='white', linewidth=1.5)
    ax.add_patch(nucleus2)
    ax.text(0, 0.3, '细胞核', ha='center', va='center', fontsize=9, color=COLORS['text'])

    # 叶绿体
    chloro = mpatches.Ellipse((1.3, 1.2), 0.5, 0.8, angle=45, facecolor='#58D68D', edgecolor='white', linewidth=1.5)
    ax.add_patch(chloro)
    ax.text(1.6, 1.0, '叶绿体', ha='center', fontsize=8, color=COLORS['text'])

    # 大液泡
    vacuole = Circle((-0.5, -0.8), 1.0, facecolor='#AED6F1', edgecolor='white', linewidth=1.5, alpha=0.5)
    ax.add_patch(vacuole)
    ax.text(-0.5, -0.8, '大液泡', ha='center', va='center', fontsize=9, color=COLORS['text'])

    # 线粒体
    mito2 = mpatches.Ellipse((-1.3, 1.3), 0.6, 0.3, angle=-30, facecolor='#AED6F1', edgecolor='white', linewidth=1.5)
    ax.add_patch(mito2)
    ax.text(-1.3, 1.0, '线粒体', ha='center', fontsize=8, color=COLORS['text'])

    draw_organelle(ax, 1.0, -1.3, '核糖体', '#F5B7B1', 'circle', 0.12)
    draw_organelle(ax, 1.6, -0.3, '高尔基体', '#A9DFBF', 'rect', 0.2)
    draw_organelle(ax, -1.5, -0.3, '内质网', '#D5A6BD', 'ellipse', 0.2)

    ax.text(0, -2.8, '有细胞壁、叶绿体、大液泡', ha='center', fontsize=10, color=COLORS['gray'], fontstyle='italic')

    fig.suptitle('细胞结构模式图', fontsize=18, fontweight='bold', y=0.98)
    savefig(fig, '生物', '细胞结构模式图.png')


def draw_biology_2():
    """神经反射弧"""
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.set_xlim(-1, 14); ax.set_ylim(-2, 3)
    ax.axis('off')
    ax.set_facecolor(COLORS['bg']); fig.patch.set_facecolor('white')

    # 5个部分的位置
    positions = [
        (1.5, 0.5, '感受器\n(皮肤)'),
        (4.0, 0.5, '传入神经'),
        (7.0, 0.5, '神经中枢\n(脊髓)'),
        (9.5, 0.5, '传出神经'),
        (12.0, 0.5, '效应器\n(肌肉)'),
    ]

    colors = [COLORS['blue'], COLORS['green'], COLORS['purple'], COLORS['orange'], COLORS['red']]

    for i, ((x, y, label), color) in enumerate(zip(positions, colors)):
        if i == 0 or i == 4:
            # 感受器和效应器用椭圆
            shape = mpatches.Ellipse((x, y), 1.2, 1.0, facecolor=color, edgecolor='white', linewidth=2, alpha=0.8)
        else:
            shape = FancyBboxPatch((x - 0.6, y - 0.4), 1.2, 0.8,
                                   boxstyle='round,pad=0.05', facecolor=color, edgecolor='white', linewidth=2)
        ax.add_patch(shape)
        ax.text(x, y, label, ha='center', va='center', fontsize=11, fontweight='bold', color='white')

    # 连接箭头
    arrow_y = 0.5
    for i in range(4):
        x1 = positions[i][0] + 0.7
        x2 = positions[i+1][0] - 0.7
        ax.annotate('', xy=(x2, arrow_y), xytext=(x1, arrow_y),
                    arrowprops=dict(arrowstyle='->', color=COLORS['gray'], lw=2.5))

    # 传入神经上的神经节
    ganglion = Circle((5.2, 0.5), 0.25, facecolor='#F4D03F', edgecolor='#D4AC0D', linewidth=2)
    ax.add_patch(ganglion)
    ax.text(5.2, 0.5, '节', ha='center', va='center', fontsize=9, color='#8B7508', fontweight='bold')
    ax.text(5.2, 0.0, '神经节', ha='center', fontsize=9, color=COLORS['gray'])

    # 兴奋传导方向标注
    ax.annotate('', xy=(13.5, 0.5), xytext=(0.5, 0.5),
                arrowprops=dict(arrowstyle='->', color=COLORS['red'], lw=3))
    ax.text(7, 1.3, '兴奋传导方向', ha='center', fontsize=13, color=COLORS['red'], fontweight='bold')

    # 反射弧文字说明
    ax.text(7, -1.0, '反射弧 = 感受器 → 传入神经 → 神经中枢 → 传出神经 → 效应器',
            ha='center', fontsize=13, color=COLORS['text'],
            bbox=dict(boxstyle='round', facecolor='#FFF9E6', edgecolor=COLORS['orange'], alpha=0.9))

    ax.set_title('神经反射弧', fontsize=18, fontweight='bold', pad=15)
    savefig(fig, '生物', '神经反射弧.png')


def draw_biology_3():
    """遗传定律分离比"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9))
    fig.patch.set_facecolor('white')

    # 上半：分离定律 3:1
    ax = ax1
    ax.set_xlim(0, 10); ax.set_ylim(0, 5)
    ax.axis('off')
    ax.set_facecolor(COLORS['bg'])

    ax.text(5, 4.5, '分离定律：一对等位基因', ha='center', fontsize=15, fontweight='bold', color=COLORS['text'])

    # P代
    ax.text(1, 3.5, 'P:', fontsize=13, fontweight='bold')
    rect_p1 = FancyBboxPatch((1.5, 3.2), 0.8, 0.5, boxstyle='round', facecolor=COLORS['blue'], edgecolor='white')
    ax.add_patch(rect_p1)
    ax.text(1.9, 3.45, 'AA', ha='center', va='center', fontsize=12, color='white', fontweight='bold')
    ax.text(2.5, 3.45, r'$\times$', ha='center', va='center', fontsize=14)
    rect_p2 = FancyBboxPatch((2.8, 3.2), 0.8, 0.5, boxstyle='round', facecolor=COLORS['green'], edgecolor='white')
    ax.add_patch(rect_p2)
    ax.text(3.2, 3.45, 'aa', ha='center', va='center', fontsize=12, color='white', fontweight='bold')

    # F1
    ax.annotate('', xy=(5, 3.0), xytext=(2.5, 3.2),
                arrowprops=dict(arrowstyle='->', color=COLORS['gray'], lw=1.5))
    ax.text(4.5, 3.5, 'F1:', fontsize=13, fontweight='bold')
    rect_f1 = FancyBboxPatch((5, 3.0), 0.8, 0.5, boxstyle='round', facecolor=COLORS['purple'], edgecolor='white')
    ax.add_patch(rect_f1)
    ax.text(5.4, 3.25, 'Aa', ha='center', va='center', fontsize=12, color='white', fontweight='bold')

    # F2 棋盘格
    ax.text(1.5, 1.8, 'F2:', fontsize=13, fontweight='bold')
    ax.annotate('', xy=(5, 1.5), xytext=(5, 3.0),
                arrowprops=dict(arrowstyle='->', color=COLORS['gray'], lw=1.5))

    # 4格棋盘
    genotypes = [('AA', COLORS['blue']), ('Aa', COLORS['purple']),
                 ('Aa', COLORS['purple']), ('aa', COLORS['green'])]
    for idx, (geno, color) in enumerate(genotypes):
        row = idx // 2
        col = idx % 2
        x = 2.5 + col * 1.2
        y = 1.0 - row * 1.0
        rect = Rectangle((x, y), 1.0, 0.8, facecolor=color, edgecolor='white', linewidth=2, alpha=0.8)
        ax.add_patch(rect)
        ax.text(x + 0.5, y + 0.4, geno, ha='center', va='center', fontsize=12, color='white', fontweight='bold')

    # 3:1 柱状图
    bar_x = [6.5, 7.8]
    bar_h = [3, 1]
    bar_c = [COLORS['purple'], COLORS['green']]
    labels = ['A_ (3/4)', 'aa (1/4)']
    for bx, bh, bc, lbl in zip(bar_x, bar_h, bar_c, labels):
        rect = Rectangle((bx, 0), 0.8, bh * 0.5, facecolor=bc, edgecolor='white', linewidth=2, alpha=0.8)
        ax.add_patch(rect)
        ax.text(bx + 0.4, bh * 0.5 + 0.1, lbl, ha='center', fontsize=11, color=COLORS['text'])
    ax.text(7.1, 2.0, '3 : 1', ha='center', fontsize=16, fontweight='bold', color=COLORS['red'])

    ax.set_title('分离定律', fontsize=14, fontweight='bold', pad=10)

    # 下半：自由组合 9:3:3:1
    ax = ax2
    ax.set_xlim(0, 10); ax.set_ylim(0, 5)
    ax.axis('off')
    ax.set_facecolor(COLORS['bg'])

    ax.text(5, 4.5, '自由组合定律：两对基因', ha='center', fontsize=15, fontweight='bold', color=COLORS['text'])

    # 柱状图表示 9:3:3:1
    phenotypes = [
        ('A_B_\n(9/16)', 9, COLORS['blue']),
        ('A_bb\n(3/16)', 3, COLORS['green']),
        ('aaB_\n(3/16)', 3, COLORS['orange']),
        ('aabb\n(1/16)', 1, COLORS['red']),
    ]
    max_h = 9
    start_x = 1.5
    bar_w = 1.2
    gap = 0.5
    for i, (label, h, color) in enumerate(phenotypes):
        x = start_x + i * (bar_w + gap)
        bh = h / max_h * 3.0
        rect = Rectangle((x, 0), bar_w, bh, facecolor=color, edgecolor='white', linewidth=2, alpha=0.8)
        ax.add_patch(rect)
        ax.text(x + bar_w/2, bh + 0.15, label, ha='center', fontsize=10, color=COLORS['text'])
        ax.text(x + bar_w/2, -0.4, str(h), ha='center', fontsize=12, fontweight='bold', color=COLORS['text'])

    ax.text(6.5, 2.5, '9  :  3  :  3  :  1', ha='left', fontsize=18,
            fontweight='bold', color=COLORS['red'],
            bbox=dict(boxstyle='round', facecolor='#FFF9E6', edgecolor=COLORS['red'], alpha=0.9))

    ax.set_title('自由组合定律', fontsize=14, fontweight='bold', pad=10)

    fig.suptitle('遗传定律分离比', fontsize=18, fontweight='bold', y=0.98)
    savefig(fig, '生物', '遗传定律分离比.png')


def draw_biology_4():
    """中心法则"""
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(-5, 5); ax.set_ylim(-4, 4)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_facecolor(COLORS['bg']); fig.patch.set_facecolor('white')

    # 中心圆：DNA
    dna = Circle((0, 0), 1.0, facecolor=COLORS['blue'], edgecolor='white', linewidth=3)
    ax.add_patch(dna)
    ax.text(0, 0, 'DNA', ha='center', va='center', fontsize=16, fontweight='bold', color='white')

    # 箭头1: DNA -> DNA (复制)
    arrow1 = Arc((0, 0), 3.5, 3.5, angle=0, theta1=30, theta2=80, color=COLORS['green'], lw=2.5)
    ax.add_patch(arrow1)
    # 箭头头
    a1x = 1.75 * np.cos(np.radians(80))
    a1y = 1.75 * np.sin(np.radians(80))
    ax.annotate('', xy=(a1x - 0.1, a1y + 0.15), xytext=(a1x, a1y),
                arrowprops=dict(arrowstyle='->', color=COLORS['green'], lw=2))
    ax.text(1.2, 2.2, 'DNA复制', fontsize=12, color=COLORS['green'], fontweight='bold')

    # 箭头2: DNA -> RNA (转录)
    arrow2 = Arc((0, 0), 3.5, 3.5, angle=0, theta1=100, theta2=150, color=COLORS['orange'], lw=2.5)
    ax.add_patch(arrow2)
    a2x = 1.75 * np.cos(np.radians(100))
    a2y = 1.75 * np.sin(np.radians(100))
    ax.annotate('', xy=(a2x - 0.15, a2y + 0.1), xytext=(a2x, a2y),
                arrowprops=dict(arrowstyle='->', color=COLORS['orange'], lw=2))
    ax.text(-1.6, 2.0, '转录', fontsize=12, color=COLORS['orange'], fontweight='bold')

    # RNA 圆
    rna = Circle((-2.5, 0), 0.7, facecolor=COLORS['orange'], edgecolor='white', linewidth=2.5)
    ax.add_patch(rna)
    ax.text(-2.5, 0, 'RNA', ha='center', va='center', fontsize=13, fontweight='bold', color='white')

    # 箭头3: RNA -> 蛋白质 (翻译)
    ax.annotate('', xy=(-0.8, -0.3), xytext=(-1.8, -0.1),
                arrowprops=dict(arrowstyle='->', color=COLORS['purple'], lw=2.5))
    ax.text(-1.5, -0.6, '翻译', fontsize=12, color=COLORS['purple'], fontweight='bold')

    # 蛋白质
    protein = Circle((0, -2.2), 0.8, facecolor=COLORS['purple'], edgecolor='white', linewidth=2.5)
    ax.add_patch(protein)
    ax.text(0, -2.2, '蛋白质', ha='center', va='center', fontsize=11, fontweight='bold', color='white')

    # 箭头4: RNA -> RNA (RNA复制，虚线，病毒)
    arrow4 = Arc((-2.5, 0), 2.5, 2.5, angle=0, theta1=160, theta2=200, color=COLORS['gray'], lw=2, linestyle='--')
    ax.add_patch(arrow4)
    a4x = -2.5 + 1.25 * np.cos(np.radians(200))
    a4y = 1.25 * np.sin(np.radians(200))
    ax.annotate('', xy=(a4x - 0.1, a4y - 0.1), xytext=(a4x, a4y),
                arrowprops=dict(arrowstyle='->', color=COLORS['gray'], lw=1.5))
    ax.text(-3.8, -0.3, 'RNA复制', fontsize=10, color=COLORS['gray'], fontstyle='italic')

    # 箭头5: RNA -> DNA (逆转录，虚线，病毒)
    ax.annotate('', xy=(-0.8, 0.3), xytext=(-1.8, 0.1),
                arrowprops=dict(arrowstyle='->', color=COLORS['gray'], lw=2, linestyle='--'))
    ax.text(-1.5, 0.6, '逆转录', fontsize=10, color=COLORS['gray'], fontstyle='italic')

    # 病毒特有标注
    ax.text(-3.8, -1.0, '病毒特有', fontsize=9, color=COLORS['gray'])
    ax.text(-3.8, -1.3, '(虚线)', fontsize=9, color=COLORS['gray'])

    # 中心法则公式
    ax.text(0, -3.5, r'$DNA \to DNA \to RNA \to$ 蛋白质',
            ha='center', fontsize=14, color=COLORS['text'],
            bbox=dict(boxstyle='round', facecolor='#EBF5FB', edgecolor=COLORS['blue'], alpha=0.9))

    ax.set_title('中心法则', fontsize=18, fontweight='bold', pad=15)
    savefig(fig, '生物', '中心法则.png')


# ============================================================
# 数学 (4张)
# ============================================================

def draw_math_1():
    """函数零点与二分法"""
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_facecolor(COLORS['bg']); fig.patch.set_facecolor('white')

    x = np.linspace(0.5, 5, 300)
    y = x ** 3 - 6 * x ** 2 + 9 * x - 2  # 三次函数，有零点
    ax.plot(x, y, color=COLORS['blue'], linewidth=2.5, label=r'$y = f(x)$')

    # 零点位置
    ax.axhline(y=0, color='black', linewidth=0.8)
    ax.axvline(x=0, color='black', linewidth=0.8)

    # 初始区间 [a, b]
    a, b = 0.5, 3.5
    fa = a ** 3 - 6 * a ** 2 + 9 * a - 2
    fb = b ** 3 - 6 * b ** 2 + 9 * b - 2

    ax.plot(a, fa, 'o', color=COLORS['green'], markersize=10, zorder=5)
    ax.plot(b, fb, 'o', color=COLORS['red'], markersize=10, zorder=5)
    ax.text(a, fa + 0.8, r'$f(a) > 0$', fontsize=12, color=COLORS['green'], fontweight='bold')
    ax.text(b, fb - 0.8, r'$f(b) < 0$', fontsize=12, color=COLORS['red'], fontweight='bold')

    # 迭代1
    c1 = (a + b) / 2
    fc1 = c1 ** 3 - 6 * c1 ** 2 + 9 * c1 - 2
    ax.plot(c1, fc1, 's', color=COLORS['orange'], markersize=10, zorder=5)
    ax.axvline(x=c1, color=COLORS['orange'], linestyle='--', linewidth=1.5, alpha=0.6)
    ax.text(c1, fc1 + 0.8, r"$c_1 = \frac{a+b}{2}$" + '\n' + r'$f(c_1) < 0$', fontsize=10,
            color=COLORS['orange'], ha='center', fontweight='bold')

    # 迭代2
    a2, b2 = a, c1
    c2 = (a2 + b2) / 2
    fc2 = c2 ** 3 - 6 * c2 ** 2 + 9 * c2 - 2
    ax.plot(c2, fc2, 'D', color=COLORS['purple'], markersize=9, zorder=5)
    ax.axvline(x=c2, color=COLORS['purple'], linestyle='-.', linewidth=1.5, alpha=0.6)
    ax.text(c2, fc2 + 1.0, r"$c_2 = \frac{a+c_1}{2}$", fontsize=10,
            color=COLORS['purple'], ha='center', fontweight='bold')

    # 区间标注
    ax.plot([a, b], [-3.5, -3.5], color=COLORS['green'], linewidth=3)
    ax.text((a+b)/2, -3.2, r'$[a, b]$', ha='center', fontsize=11, color=COLORS['green'])
    ax.plot([a, c1], [-4.2, -4.2], color=COLORS['orange'], linewidth=3)
    ax.text((a+c1)/2, -3.9, r'$[a, c_1]$', ha='center', fontsize=11, color=COLORS['orange'])

    ax.set_xlabel('x', fontsize=14)
    ax.set_ylabel('y', fontsize=14)
    ax.set_title('函数零点与二分法', fontsize=18, fontweight='bold', pad=15)
    ax.legend(loc='upper right', fontsize=12)
    ax.set_xlim(-0.2, 5.5); ax.set_ylim(-5, 5)
    ax.grid(True, alpha=0.3)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    savefig(fig, '数学', '函数零点二分法.png')


def draw_math_2():
    """正余弦定理几何意义"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))
    fig.patch.set_facecolor('white')

    # 左：正弦定理 + 外接圆
    ax = ax1
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_facecolor(COLORS['bg'])

    # 外接圆
    R = 2.2
    circle = Circle((0, 0), R, fill=False, edgecolor=COLORS['gray'], linewidth=1.5, linestyle='--')
    ax.add_patch(circle)
    ax.plot(0, 0, 'x', color=COLORS['gray'], markersize=8)
    ax.text(0.2, -0.3, 'O', fontsize=12, color=COLORS['gray'])

    # 三角形ABC
    angles = [np.radians(70), np.radians(190), np.radians(310)]
    A = (R * np.cos(angles[0]), R * np.sin(angles[0]))
    B = (R * np.cos(angles[1]), R * np.sin(angles[1]))
    C = (R * np.cos(angles[2]), R * np.sin(angles[2]))

    tri = Polygon([A, B, C], closed=True, fill=False, edgecolor=COLORS['blue'], linewidth=2.5)
    ax.add_patch(tri)

    ax.plot(*A, 'o', color=COLORS['red'], markersize=8)
    ax.plot(*B, 'o', color=COLORS['red'], markersize=8)
    ax.plot(*C, 'o', color=COLORS['red'], markersize=8)

    ax.text(A[0] + 0.15, A[1] + 0.2, 'A', fontsize=14, color=COLORS['red'], fontweight='bold')
    ax.text(B[0] - 0.3, B[1] - 0.1, 'B', fontsize=14, color=COLORS['red'], fontweight='bold')
    ax.text(C[0] + 0.15, C[1] - 0.3, 'C', fontsize=14, color=COLORS['red'], fontweight='bold')

    # 边标注
    ax.text((B[0]+C[0])/2 - 0.2, (B[1]+C[1])/2 - 0.3, 'a', fontsize=13, color=COLORS['blue'])
    ax.text((A[0]+C[0])/2 + 0.2, (A[1]+C[1])/2 + 0.1, 'b', fontsize=13, color=COLORS['blue'])
    ax.text((A[0]+B[0])/2 + 0.1, (A[1]+B[1])/2 + 0.2, 'c', fontsize=13, color=COLORS['blue'])

    # 正弦定理公式
    ax.text(0, -2.7, r'$\frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C} = 2R$',
            ha='center', fontsize=14, color=COLORS['text'],
            bbox=dict(boxstyle='round', facecolor='#EBF5FB', edgecolor=COLORS['blue'], alpha=0.9))
    ax.set_title('正弦定理', fontsize=14, fontweight='bold', pad=10)

    # 右：余弦定理 + 投影
    ax = ax2
    ax.set_xlim(-1, 6); ax.set_ylim(-1, 5)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_facecolor(COLORS['bg'])

    # 三角形ABC（直角坐标系中）
    Ax, Ay = 0.5, 0.5
    Bx, By = 4.5, 0.5
    Cx, Cy = 1.5, 3.0

    ax.plot([Ax, Bx, Cx, Ax], [Ay, By, Cy, Ay], color=COLORS['blue'], linewidth=2.5)
    ax.plot(Ax, Ay, 'o', color=COLORS['red'], markersize=8)
    ax.plot(Bx, By, 'o', color=COLORS['red'], markersize=8)
    ax.plot(Cx, Cy, 'o', color=COLORS['red'], markersize=8)

    ax.text(Ax - 0.3, Ay - 0.3, 'A', fontsize=14, color=COLORS['red'], fontweight='bold')
    ax.text(Bx + 0.2, By - 0.3, 'B', fontsize=14, color=COLORS['red'], fontweight='bold')
    ax.text(Cx + 0.1, Cy + 0.3, 'C', fontsize=14, color=COLORS['red'], fontweight='bold')

    # 高线（投影）
    foot_x = Cx
    foot_y = Ay
    ax.plot([Cx, foot_x], [Cy, foot_y], '--', color=COLORS['green'], linewidth=1.5, alpha=0.7)
    ax.plot(foot_x, foot_y, 's', color=COLORS['green'], markersize=6)
    ax.text(foot_x + 0.15, foot_y - 0.3, 'D', fontsize=11, color=COLORS['green'])

    # 边标注
    ax.text((Ax + Bx)/2, Ay - 0.4, 'c', fontsize=13, color=COLORS['blue'])
    ax.text((Bx + Cx)/2 + 0.2, (By + Cy)/2, 'a', fontsize=13, color=COLORS['blue'])
    ax.text((Ax + Cx)/2 - 0.3, (Ay + Cy)/2, 'b', fontsize=13, color=COLORS['blue'])

    # 角C标注
    ax.text(Cx - 0.3, Cy - 0.5, r'$\angle C$', fontsize=12, color=COLORS['orange'])

    # 投影线段
    ax.plot([Ax, foot_x], [Ay - 0.15, Ay - 0.15], color=COLORS['gray'], linewidth=1)
    ax.text((Ax + foot_x)/2, Ay - 0.4, r'$b\cos C$', ha='center', fontsize=10, color=COLORS['gray'])
    ax.text((foot_x + Bx)/2, Ay - 0.4, r'$a\cos B$', ha='center', fontsize=10, color=COLORS['gray'])

    # 余弦定理公式
    ax.text(2.5, -0.7, r'$c^2 = a^2 + b^2 - 2ab\cos C$',
            ha='center', fontsize=14, color=COLORS['text'],
            bbox=dict(boxstyle='round', facecolor='#FFF9E6', edgecolor=COLORS['orange'], alpha=0.9))
    ax.set_title('余弦定理', fontsize=14, fontweight='bold', pad=10)

    fig.suptitle('正余弦定理几何意义', fontsize=18, fontweight='bold', y=0.98)
    savefig(fig, '数学', '正余弦定理.png')


def draw_math_3():
    """立体几何外接球"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))
    fig.patch.set_facecolor('white')

    # 上半：长方体外接球
    ax = ax1
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_facecolor(COLORS['bg'])

    # 外接球（虚线圆）
    sphere = Circle((0, 0), 2.5, fill=False, edgecolor=COLORS['gray'], linewidth=2, linestyle='--')
    ax.add_patch(sphere)
    ax.text(2.7, 2.5, '外接球', fontsize=11, color=COLORS['gray'], fontstyle='italic')

    # 长方体（简化2D示意）
    w, h = 3.0, 2.0
    rect = Rectangle((-w/2, -h/2), w, h, fill=False, edgecolor=COLORS['blue'], linewidth=2.5)
    ax.add_patch(rect)

    # 对角线（直径）
    ax.plot([-w/2, w/2], [-h/2, h/2], '--', color=COLORS['red'], linewidth=2)
    ax.annotate('', xy=(w/2, h/2), xytext=(-w/2, -h/2),
                arrowprops=dict(arrowstyle='<->', color=COLORS['red'], lw=2))
    ax.text(0.3, 0.3, r'$2R = \sqrt{a^2+b^2+c^2}$', fontsize=12, color=COLORS['red'], fontweight='bold')

    ax.plot(0, 0, 'x', color=COLORS['gray'], markersize=10)
    ax.text(0.15, -0.25, '球心', fontsize=11, color=COLORS['gray'])

    # 顶点
    for px, py in [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)]:
        ax.plot(px, py, 'o', color=COLORS['blue'], markersize=6)

    ax.set_title('长方体外接球', fontsize=14, fontweight='bold', pad=10)

    # 下半：正四面体外接球
    ax = ax2
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_facecolor(COLORS['bg'])

    # 外接球
    sphere2 = Circle((0, 0), 2.5, fill=False, edgecolor=COLORS['gray'], linewidth=2, linestyle='--')
    ax.add_patch(sphere2)

    # 正四面体（2D投影）
    tetra = np.array([
        [0, 2.0],
        [-1.8, -1.0],
        [1.8, -1.0],
    ])
    tri = Polygon(tetra, closed=True, fill=False, edgecolor=COLORS['green'], linewidth=2.5)
    ax.add_patch(tri)

    # 第四条边（虚线表示在后方）
    ax.plot([tetra[0,0], 0], [tetra[0,1], -1.8], '--', color=COLORS['green'], linewidth=1.5, alpha=0.6)
    ax.plot([tetra[1,0], 0], [tetra[1,1], -1.8], color=COLORS['green'], linewidth=2.5)
    ax.plot([tetra[2,0], 0], [tetra[2,1], -1.8], color=COLORS['green'], linewidth=2.5)
    ax.plot(0, -1.8, 'o', color=COLORS['green'], markersize=6)

    # 高线和球心
    ax.plot([0, 0], [2.0, -1.8], '--', color=COLORS['red'], linewidth=1.5, alpha=0.7)
    ax.plot(0, 0, 'x', color=COLORS['gray'], markersize=10)
    ax.text(0.2, 0.2, '球心', fontsize=11, color=COLORS['gray'])

    # 公式
    ax.text(0, -2.7, r'$R = \frac{\sqrt{6}}{4}a$', ha='center', fontsize=14, color=COLORS['text'],
            bbox=dict(boxstyle='round', facecolor='#E8F8F5', edgecolor=COLORS['green'], alpha=0.9))

    ax.set_title('正四面体外接球', fontsize=14, fontweight='bold', pad=10)

    fig.suptitle('立体几何外接球', fontsize=18, fontweight='bold', y=0.98)
    savefig(fig, '数学', '外接球示意图.png')


def draw_math_4():
    """概率分布对比"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))
    fig.patch.set_facecolor('white')

    # 左：二项分布 B(n=10, p=0.5)
    ax = ax1
    ax.set_facecolor(COLORS['bg'])

    n, p = 10, 0.5
    # 手动计算二项分布 PMF
    def binom_pmf(k, n, p):
        from math import comb
        return comb(n, k) * (p ** k) * ((1 - p) ** (n - k))

    x = np.arange(0, n + 1)
    pmf = np.array([binom_pmf(k, n, p) for k in x])

    bars = ax.bar(x, pmf, color=COLORS['blue'], edgecolor='white', linewidth=1.5, alpha=0.8, width=0.7)
    ax.axvline(x=n*p, color=COLORS['red'], linestyle='--', linewidth=2, label=r'$\mu = np = 5$')

    ax.set_xlabel('k', fontsize=13)
    ax.set_ylabel('P(X=k)', fontsize=13)
    ax.set_title(r'二项分布 $B(n=10, p=0.5)$', fontsize=14, fontweight='bold', pad=10)
    ax.legend(loc='upper right', fontsize=11)
    ax.set_xlim(-0.5, 10.5); ax.set_ylim(0, 0.3)
    ax.grid(True, alpha=0.3, axis='y')
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

    # 右：正态分布 N(mu, sigma^2)
    ax = ax2
    ax.set_facecolor(COLORS['bg'])

    mu, sigma = 0, 1
    # 手动计算正态分布 PDF
    x2 = np.linspace(-4, 4, 300)
    pdf = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x2 - mu) / sigma) ** 2)

    ax.plot(x2, pdf, color=COLORS['green'], linewidth=2.5, label=r'$N(\mu, \sigma^2)$')
    ax.fill_between(x2, pdf, alpha=0.2, color=COLORS['green'])

    # mu标注
    ax.axvline(x=mu, color=COLORS['red'], linestyle='--', linewidth=2, label=r'$\mu = 0$')
    y_at_mu = (1 / (sigma * np.sqrt(2 * np.pi)))
    ax.plot(mu, y_at_mu, 'o', color=COLORS['red'], markersize=10, zorder=5)
    ax.text(mu, y_at_mu + 0.03, r'$\mu$', ha='center', fontsize=14,
            color=COLORS['red'], fontweight='bold')

    # sigma标注
    y_at_sigma = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5)
    ax.annotate('', xy=(mu + sigma, y_at_sigma),
                xytext=(mu, y_at_mu * 0.6),
                arrowprops=dict(arrowstyle='->', color=COLORS['orange'], lw=2))
    ax.text(mu + 0.5, 0.25, r'$\sigma$', fontsize=13, color=COLORS['orange'], fontweight='bold')

    # 对称轴
    ax.axvline(x=mu, color=COLORS['gray'], linestyle=':', linewidth=1, alpha=0.5)
    ax.text(mu, -0.02, '对称轴', ha='center', fontsize=10, color=COLORS['gray'])

    # 68-95-99.7 规则示意
    ax.fill_between(x2, pdf, where=(x2 >= mu - sigma) & (x2 <= mu + sigma),
                    alpha=0.15, color=COLORS['blue'])
    ax.text(mu, 0.15, r'$\approx 68\%$', ha='center', fontsize=10, color=COLORS['blue'])

    ax.set_xlabel('x', fontsize=13)
    ax.set_ylabel(r'$\varphi(x)$', fontsize=13)
    ax.set_title(r'正态分布 $N(0, 1)$', fontsize=14, fontweight='bold', pad=10)
    ax.legend(loc='upper right', fontsize=11)
    ax.set_xlim(-4.5, 4.5); ax.set_ylim(-0.02, 0.45)
    ax.grid(True, alpha=0.3)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

    fig.suptitle('概率分布对比', fontsize=18, fontweight='bold', y=0.98)
    savefig(fig, '数学', '概率分布对比.png')


# ============================================================
# 主程序
# ============================================================
if __name__ == '__main__':
    print("=" * 50)
    print("开始绘制 2028高考知识库 第二批知识点示意图")
    print("=" * 50)

    functions = [
        draw_physics_1, draw_physics_2, draw_physics_3, draw_physics_4,
        draw_chemistry_1, draw_chemistry_2, draw_chemistry_3, draw_chemistry_4,
        draw_biology_1, draw_biology_2, draw_biology_3, draw_biology_4,
        draw_math_1, draw_math_2, draw_math_3, draw_math_4,
    ]

    success = 0
    for fn in functions:
        try:
            fn()
            success += 1
        except Exception as e:
            print(f"  失败: {fn.__name__} - {e}")

    print("=" * 50)
    print(f"绘制完成：{success} / {len(functions)} 张")
    print("=" * 50)
