# -*- coding: utf-8 -*-
"""
2028高考知识库 — 知识点示意图绘制脚本
物理4张 + 化学4张 + 生物4张 + 数学4张 = 16张
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from matplotlib.patches import FancyArrowPatch, Arc, Circle, Rectangle, Polygon
import numpy as np
import os

# ===================== 全局设置 =====================
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150

# 配色方案（淡雅专业）
COLORS = {
    'red': '#C44E52',
    'blue': '#4C72B0',
    'green': '#55A868',
    'orange': '#DD8452',
    'purple': '#8172B2',
    'gray': '#7F7F7F',
    'light_gray': '#CCCCCC',
    'bg': '#FAFAFA',
    'text': '#333333'
}

OUTPUT_DIR = r"C:\Users\user\WPSDrive\203612604\WPS云盘\申悦文档\AI辅助\2028高考知识库\图形库"


def savefig(fig, subdir, filename):
    path = os.path.join(OUTPUT_DIR, subdir, filename)
    fig.savefig(path, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  ✓ 已保存: {subdir}/{filename}")


# ============================================================
# 物理
# ============================================================

def draw_physics_1():
    """斜面物体受力分析图"""
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor(COLORS['bg'])
    fig.patch.set_facecolor('white')

    # 画斜面（30度角）
    theta = np.radians(30)
    slope_base = [2, 8.5]
    slope_height = 3.5
    slope_top = [slope_base[0] + slope_height / np.tan(theta), slope_base[1] + slope_height]
    slope_bottom = [slope_base[0], slope_base[1]]

    # 斜面三角形
    triangle = Polygon([
        [slope_bottom[0], slope_bottom[1]],
        [slope_top[0], slope_top[1]],
        [slope_top[0], slope_bottom[1]]
    ], closed=True, facecolor='#E8DCC8', edgecolor='#B8A88C', linewidth=1.5)
    ax.add_patch(triangle)

    # 斜面线
    ax.plot([slope_bottom[0], slope_top[0]], [slope_bottom[1], slope_top[1]],
            'k-', linewidth=2)
    ax.plot([slope_bottom[0], slope_top[0]], [slope_bottom[1], slope_bottom[1]],
            'k-', linewidth=1.5)
    ax.plot([slope_top[0], slope_top[0]], [slope_bottom[1], slope_top[1]],
            'k-', linewidth=1.5)

    # 画方块（在斜面上，约中间位置）
    s = 0.8  # 方块半长
    # 方块中心在斜面上
    cx = 5.5
    cy = slope_bottom[1] + (cx - slope_bottom[0]) * np.tan(theta)
    # 方块的四个角（旋转theta角）
    corners = np.array([[-s, -s], [s, -s], [s, s], [-s, s]])
    rot = np.array([[np.cos(theta), -np.sin(theta)],
                    [np.sin(theta), np.cos(theta)]])
    box = corners @ rot.T + [cx, cy]
    box_patch = Polygon(box, closed=True, facecolor='#A0C4E8',
                        edgecolor=COLORS['blue'], linewidth=2)
    ax.add_patch(box_patch)

    # 力的起点（方块中心）
    ox, oy = cx, cy

    # 重力G（竖直向下）
    g_len = 2.0
    ax.annotate('', xy=(ox, oy - g_len), xytext=(ox, oy),
                arrowprops=dict(arrowstyle='->', color=COLORS['red'], lw=2.5))
    ax.text(ox + 0.3, oy - g_len / 2, 'G (重力)', fontsize=14, color=COLORS['red'],
            fontweight='bold')

    # 支持力N（垂直斜面向上）
    n_len = 1.6
    nx = ox + n_len * np.sin(theta)
    ny = oy + n_len * np.cos(theta)
    ax.annotate('', xy=(nx, ny), xytext=(ox, oy),
                arrowprops=dict(arrowstyle='->', color=COLORS['blue'], lw=2.5))
    ax.text(nx + 0.2, ny + 0.2, 'N (支持力)', fontsize=14, color=COLORS['blue'],
            fontweight='bold')

    # 摩擦力f（沿斜面向上）
    f_len = 1.2
    fx = ox - f_len * np.cos(theta)
    fy = oy - f_len * np.sin(theta)
    ax.annotate('', xy=(fx, fy), xytext=(ox, oy),
                arrowprops=dict(arrowstyle='->', color=COLORS['green'], lw=2.5))
    ax.text(fx - 0.8, fy - 0.3, 'f (摩擦力)', fontsize=14, color=COLORS['green'],
            fontweight='bold')

    # 重力沿斜面向下的分力Gx
    gx_len = 1.6
    gxx = ox - gx_len * np.cos(theta)
    gxy = oy - gx_len * np.sin(theta)
    ax.annotate('', xy=(gxx, gxy), xytext=(ox, oy),
                arrowprops=dict(arrowstyle='->', color=COLORS['orange'], lw=2,
                               linestyle='--'))
    ax.text(gxx - 0.5, gxy - 0.5, r"$G_x$ (下滑分力)", fontsize=13,
            color=COLORS['orange'], fontweight='bold')

    # 标注斜面角θ
    arc_x = slope_bottom[0] + 1.0
    arc_y = slope_bottom[1]
    arc = Arc((arc_x, arc_y), 1.2, 1.2, angle=0, theta1=0, theta2=30,
              color=COLORS['gray'], lw=1.5)
    ax.add_patch(arc)
    ax.text(arc_x + 0.7, arc_y + 0.35, r'$\theta = 30°$', fontsize=12,
            color=COLORS['gray'])

    # 标注垂直符号（N与斜面垂直）
    # 在斜面上画一个小直角符号
    perp_len = 0.3
    px = ox + perp_len * np.cos(theta)
    py = oy + perp_len * np.sin(theta)
    p2x = px + perp_len * np.sin(theta)
    p2y = py + perp_len * np.cos(theta)
    p3x = ox + perp_len * np.sin(theta)
    p3y = oy + perp_len * np.cos(theta)
    ax.plot([px, p2x, p3x], [py, p2y, p3y], 'k-', linewidth=1)

    ax.set_title('斜面物体受力分析图', fontsize=18, fontweight='bold', pad=15)
    savefig(fig, '物理', '受力分析_斜面物体.png')


def draw_physics_2():
    """运动学v-t图像对比"""
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_facecolor(COLORS['bg'])
    fig.patch.set_facecolor('white')

    t = np.linspace(0, 10, 200)
    v_uniform = np.full_like(t, 5)
    v_accel = 2 + 0.8 * t
    v_decel = 10 - 0.6 * t

    ax.plot(t, v_uniform, color=COLORS['blue'], linewidth=2.5,
            label='匀速直线运动 (v = 5 m/s)')
    ax.plot(t, v_accel, color=COLORS['green'], linewidth=2.5,
            label='匀加速直线运动 (v = 2 + 0.8t)')
    ax.plot(t, v_decel, color=COLORS['red'], linewidth=2.5,
            label='匀减速直线运动 (v = 10 - 0.6t)')

    # 标注关键点
    ax.plot([0, 10], [5, 5], 'o', color=COLORS['blue'], markersize=6)
    ax.plot(0, 2, 'o', color=COLORS['green'], markersize=6)
    ax.plot(0, 10, 'o', color=COLORS['red'], markersize=6)

    # 填充面积示意
    ax.fill_between(t, 0, v_uniform, where=(t >= 2) & (t <= 7), alpha=0.12,
                    color=COLORS['blue'])

    ax.axhline(y=0, color='black', linewidth=0.8)
    ax.axvline(x=0, color='black', linewidth=0.8)
    ax.set_xlabel('时间 t (s)', fontsize=14)
    ax.set_ylabel('速度 v (m/s)', fontsize=14)
    ax.set_title('运动学 v-t 图像对比', fontsize=18, fontweight='bold', pad=15)
    ax.legend(loc='upper right', fontsize=12, framealpha=0.9)
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-1, 12)
    ax.grid(True, alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    savefig(fig, '物理', '运动学_vt图像对比.png')


def draw_physics_3():
    """万有引力与圆周运动"""
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(-6, 6)
    ax.set_ylim(-5, 5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor(COLORS['bg'])
    fig.patch.set_facecolor('white')

    # 中心天体
    sun = Circle((0, 0), 1.2, facecolor='#F4D03F', edgecolor='#D4AC0D',
                 linewidth=2.5)
    ax.add_patch(sun)
    ax.text(0, 0, 'M', ha='center', va='center', fontsize=16,
            fontweight='bold', color='#8B7508')
    ax.text(0, -1.8, '中心天体', ha='center', va='top', fontsize=13,
            color=COLORS['text'])

    # 轨道圆
    orbit_r = 3.5
    orbit = Circle((0, 0), orbit_r, fill=False, edgecolor=COLORS['light_gray'],
                   linewidth=1.5, linestyle='--')
    ax.add_patch(orbit)

    # 卫星位置（右上）
    sat_angle = np.radians(45)
    sx = orbit_r * np.cos(sat_angle)
    sy = orbit_r * np.sin(sat_angle)
    satellite = Circle((sx, sy), 0.35, facecolor='#85C1E9',
                       edgecolor=COLORS['blue'], linewidth=2)
    ax.add_patch(satellite)
    ax.text(sx, sy, 'm', ha='center', va='center', fontsize=12,
            fontweight='bold', color=COLORS['blue'])
    ax.text(sx + 0.6, sy + 0.6, '卫星', fontsize=12, color=COLORS['text'])

    # 万有引力箭头（指向圆心）
    ax.annotate('', xy=(0, 0), xytext=(sx, sy),
                arrowprops=dict(arrowstyle='->', color=COLORS['red'], lw=3))
    mx = (sx + 0) / 2 - 0.5
    my = (sy + 0) / 2 + 0.3
    ax.text(mx, my, 'F (万有引力)', fontsize=14, color=COLORS['red'],
            fontweight='bold')

    # 速度方向（切线）
    vx = -np.sin(sat_angle) * 1.5
    vy = np.cos(sat_angle) * 1.5
    ax.annotate('', xy=(sx + vx, sy + vy), xytext=(sx, sy),
                arrowprops=dict(arrowstyle='->', color=COLORS['green'], lw=2.5))
    ax.text(sx + vx * 1.2, sy + vy * 1.2, 'v', fontsize=14,
            color=COLORS['green'], fontweight='bold')

    # 轨道运动方向箭头（圆弧箭头）
    arc_arrow = Arc((0, 0), 6.8, 6.8, angle=0, theta1=30, theta2=60,
                    color=COLORS['gray'], lw=2)
    ax.add_patch(arc_arrow)
    # 在60度位置画小箭头
    aax = 3.4 * np.cos(np.radians(60))
    aay = 3.4 * np.sin(np.radians(60))
    ax.annotate('', xy=(aax - 0.3, aay + 0.2), xytext=(aax, aay),
                arrowprops=dict(arrowstyle='->', color=COLORS['gray'], lw=1.5))

    # 公式
    ax.text(0, -4.2,
            r'$F = G\frac{Mm}{r^2} = m\frac{v^2}{r} = m\omega^2 r$',
            ha='center', fontsize=16, color=COLORS['text'])

    ax.set_title('万有引力与圆周运动', fontsize=18, fontweight='bold', pad=15)
    savefig(fig, '物理', '万有引力圆周运动.png')


def draw_physics_4():
    """电路图（串并联对比）"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.patch.set_facecolor('white')

    def draw_resistor(ax, x, y, orient='h', label='R'):
        if orient == 'h':
            # 水平电阻: 锯齿形
            xs = [x - 0.6, x - 0.4, x - 0.2, x, x + 0.2, x + 0.4, x + 0.6]
            ys = [y, y + 0.2, y - 0.2, y + 0.2, y - 0.2, y + 0.2, y]
            ax.plot(xs, ys, 'b-', linewidth=2)
            ax.plot([x - 0.6, x - 0.8], [y, y], 'b-', linewidth=2)
            ax.plot([x + 0.6, x + 0.8], [y, y], 'b-', linewidth=2)
            ax.text(x, y + 0.45, label, ha='center', fontsize=12,
                    color=COLORS['blue'], fontweight='bold')
        else:
            # 垂直电阻
            ys = [y - 0.6, y - 0.4, y - 0.2, y, y + 0.2, y + 0.4, y + 0.6]
            xs = [x, x + 0.2, x - 0.2, x + 0.2, x - 0.2, x + 0.2, x]
            ax.plot(xs, ys, 'b-', linewidth=2)
            ax.plot([x, x], [y - 0.6, y - 0.8], 'b-', linewidth=2)
            ax.plot([x, x], [y + 0.6, y + 0.8], 'b-', linewidth=2)
            ax.text(x + 0.4, y, label, ha='left', fontsize=12,
                    color=COLORS['blue'], fontweight='bold')

    # ========== 左：串联电路 ==========
    ax = ax1
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor(COLORS['bg'])

    # 电源
    ax.plot([-1.5, -1.5], [1.2, 0.4], 'k-', linewidth=2)
    ax.plot([-1.7, -1.3], [0.4, 0.4], 'k-', linewidth=2)
    ax.plot([-1.6, -1.4], [0.1, 0.1], 'k-', linewidth=2)
    ax.text(-1.5, -0.1, '电源', ha='center', fontsize=11)

    # 串联回路
    wire = [
        [-1.5, 1.2], [0, 1.2], [0, 0.7],
        [0, 0.3], [0, -0.2], [0, -0.7],
        [0, -1.2], [-1.5, -1.2], [-1.5, -0.4]
    ]
    xs, ys = zip(*wire)
    ax.plot(xs, ys, 'k-', linewidth=2)

    draw_resistor(ax, 0, 0.5, 'h', 'R₁')
    draw_resistor(ax, 0, -0.45, 'h', 'R₂')

    # 电流方向箭头
    ax.annotate('', xy=(0.6, 1.2), xytext=(0.1, 1.2),
                arrowprops=dict(arrowstyle='->', color=COLORS['red'], lw=2))
    ax.text(0.35, 1.45, 'I', fontsize=13, color=COLORS['red'], fontweight='bold')

    ax.text(0, -1.7, '串联电路', ha='center', fontsize=14, fontweight='bold')
    ax.text(0, -1.95, r'$R_{总} = R_1 + R_2$', ha='center', fontsize=12,
            color=COLORS['gray'])

    # ========== 右：并联电路 ==========
    ax = ax2
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor(COLORS['bg'])

    # 电源
    ax.plot([-1.5, -1.5], [1.2, 0.4], 'k-', linewidth=2)
    ax.plot([-1.7, -1.3], [0.4, 0.4], 'k-', linewidth=2)
    ax.plot([-1.6, -1.4], [0.1, 0.1], 'k-', linewidth=2)
    ax.text(-1.5, -0.1, '电源', ha='center', fontsize=11)

    # 主干线
    ax.plot([-1.5, 1.5], [1.2, 1.2], 'k-', linewidth=2)
    ax.plot([-1.5, 1.5], [-1.2, -1.2], 'k-', linewidth=2)
    ax.plot([-1.5, -1.5], [-1.2, -0.4], 'k-', linewidth=2)

    # 分支点
    ax.plot([0, 0], [1.2, 0.6], 'k-', linewidth=2)
    ax.plot([0, 0], [-0.6, -1.2], 'k-', linewidth=2)

    draw_resistor(ax, 0, 0, 'v', 'R₁')

    ax.plot([0.8, 0.8], [1.2, 0.6], 'k-', linewidth=2)
    ax.plot([0.8, 0.8], [-0.6, -1.2], 'k-', linewidth=2)
    draw_resistor(ax, 0.8, 0, 'v', 'R₂')

    # 电流方向
    ax.annotate('', xy=(-0.6, 1.2), xytext=(-1.1, 1.2),
                arrowprops=dict(arrowstyle='->', color=COLORS['red'], lw=2))
    ax.text(-0.85, 1.45, 'I', fontsize=13, color=COLORS['red'],
            fontweight='bold')
    ax.annotate('', xy=(0, 0.9), xytext=(0, 1.15),
                arrowprops=dict(arrowstyle='->', color=COLORS['orange'], lw=1.8))
    ax.text(0.2, 1.0, r'$I_1$', fontsize=12, color=COLORS['orange'])
    ax.annotate('', xy=(0.8, 0.9), xytext=(0.8, 1.15),
                arrowprops=dict(arrowstyle='->', color=COLORS['green'], lw=1.8))
    ax.text(1.0, 1.0, r'$I_2$', fontsize=12, color=COLORS['green'])

    ax.text(0.4, -1.7, '并联电路', ha='center', fontsize=14, fontweight='bold')
    ax.text(0.4, -1.95, r'$\frac{1}{R_{总}} = \frac{1}{R_1} + \frac{1}{R_2}$',
            ha='center', fontsize=12, color=COLORS['gray'])

    fig.suptitle('电路图：串联与并联对比', fontsize=18, fontweight='bold',
                 y=0.98)
    savefig(fig, '物理', '电路串并联对比.png')


# ============================================================
# 化学
# ============================================================

def draw_chemistry_1():
    """原子电子排布能级图"""
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_facecolor(COLORS['bg'])
    fig.patch.set_facecolor('white')

    levels = [
        ('1s', 1, 1, 2),
        ('2s', 2, 2, 2),
        ('2p', 2, 3, 6),
        ('3s', 3, 4, 2),
        ('3p', 3, 5, 6),
        ('4s', 4, 6, 2),
        ('3d', 3, 7, 10),
        ('4p', 4, 8, 6),
    ]

    # 画能级阶梯
    bar_w = 1.2
    for i, (name, n, y, max_e) in enumerate(levels):
        x = 2 + i * 1.15
        color = COLORS['blue'] if 's' in name else (
            COLORS['green'] if 'p' in name else COLORS['orange'])
        rect = Rectangle((x - bar_w / 2, y - 0.25), bar_w, 0.5,
                         facecolor=color, edgecolor='white', alpha=0.7,
                         linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x, y, name, ha='center', va='center', fontsize=12,
                fontweight='bold', color='white')
        ax.text(x, y - 0.55, f'最多{max_e}e⁻', ha='center', va='top',
                fontsize=10, color=COLORS['text'])

    # 能级分组标注
    groups = [
        (1, 1.5, '第1能层 (K)'),
        (2, 2.5, '第2能层 (L)'),
        (3, 4.5, '第3能层 (M)'),
        (4, 7, '第4能层 (N)'),
    ]
    for n, y_avg, label in groups:
        ax.annotate('', xy=(11.5, y_avg), xytext=(1.5, y_avg),
                    arrowprops=dict(arrowstyle='->', color=COLORS['gray'],
                                    lw=1.5))
        ax.text(11.7, y_avg, label, ha='left', va='center', fontsize=12,
                color=COLORS['gray'], fontstyle='italic')

    # 能量方向箭头
    ax.annotate('', xy=(0.8, 7.5), xytext=(0.8, 1),
                arrowprops=dict(arrowstyle='->', color=COLORS['red'], lw=2))
    ax.text(0.3, 4, '能\n量\n升\n高', ha='center', va='center', fontsize=12,
            color=COLORS['red'], fontweight='bold')

    ax.set_title('原子电子排布能级图', fontsize=18, fontweight='bold', pad=15)
    savefig(fig, '化学', '电子能级图.png')


def draw_chemistry_2():
    """化学键类型对比"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.patch.set_facecolor('white')

    # ===== 左：NaCl 离子键 =====
    ax = ax1
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor(COLORS['bg'])

    # Na+ 大球
    na = Circle((-1.2, 0), 1.0, facecolor='#FADBD8', edgecolor=COLORS['red'],
                linewidth=2.5)
    ax.add_patch(na)
    ax.text(-1.2, 0, 'Na⁺', ha='center', va='center', fontsize=18,
            fontweight='bold', color=COLORS['red'])

    # Cl- 大球
    cl = Circle((1.2, 0), 1.3, facecolor='#D4E6F1', edgecolor=COLORS['blue'],
                linewidth=2.5)
    ax.add_patch(cl)
    ax.text(1.2, 0, 'Cl⁻', ha='center', va='center', fontsize=18,
            fontweight='bold', color=COLORS['blue'])

    # 静电引力
    ax.annotate('', xy=(-0.1, 0), xytext=(0.1, 0),
                arrowprops=dict(arrowstyle='<->', color=COLORS['purple'], lw=3))
    ax.text(0, 0.5, '静电引力', ha='center', fontsize=12,
            color=COLORS['purple'], fontweight='bold')

    ax.text(0, -2.5, 'NaCl 离子键', ha='center', fontsize=14, fontweight='bold')
    ax.text(0, -2.9, '电子转移形成阴阳离子', ha='center', fontsize=11,
            color=COLORS['gray'])

    # ===== 右：HCl 共价键 =====
    ax = ax2
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor(COLORS['bg'])

    # H 小球
    h = Circle((-0.9, 0), 0.5, facecolor='#FCF3CF', edgecolor=COLORS['orange'],
               linewidth=2)
    ax.add_patch(h)
    ax.text(-0.9, 0, 'H', ha='center', va='center', fontsize=14,
            fontweight='bold', color=COLORS['orange'])

    # Cl 大球
    cl2 = Circle((0.9, 0), 1.0, facecolor='#D4E6F1', edgecolor=COLORS['blue'],
                 linewidth=2.5)
    ax.add_patch(cl2)
    ax.text(0.9, 0, 'Cl', ha='center', va='center', fontsize=16,
            fontweight='bold', color=COLORS['blue'])

    # 共用电子对（在中间）
    ep = Circle((0, 0), 0.25, facecolor=COLORS['green'],
                edgecolor=COLORS['green'], alpha=0.8)
    ax.add_patch(ep)
    ax.text(0, -0.55, '共用电子对', ha='center', fontsize=11,
            color=COLORS['green'], fontweight='bold')

    # 电子云示意
    for offset in [-0.15, 0.15]:
        tiny = Circle((offset, 0), 0.08, facecolor='white',
                      edgecolor=COLORS['green'], linewidth=1)
        ax.add_patch(tiny)

    ax.text(0, -2.5, 'HCl 共价键', ha='center', fontsize=14, fontweight='bold')
    ax.text(0, -2.9, '共用电子对（偏向Cl）', ha='center', fontsize=11,
            color=COLORS['gray'])

    fig.suptitle('化学键类型对比：离子键 vs 共价键', fontsize=18,
                 fontweight='bold', y=0.98)
    savefig(fig, '化学', '化学键类型对比.png')


def draw_chemistry_3():
    """化学平衡移动（勒夏特列原理）"""
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_facecolor(COLORS['bg'])
    fig.patch.set_facecolor('white')

    t = np.linspace(0, 12, 300)

    # 三段平衡过程
    # 0-3: 初始平衡
    # 3-4: 突变（增加反应物浓度）
    # 4-8: 重新建立平衡
    # 8-9: 突变（升温）
    # 9-12: 再次平衡

    c = np.zeros_like(t)
    v_f = np.zeros_like(t)  # 正反应速率
    v_r = np.zeros_like(t)  # 逆反应速率

    for i, ti in enumerate(t):
        if ti < 3:
            c[i] = 2.0
            v_f[i] = 1.0
            v_r[i] = 1.0
        elif ti < 3.5:
            c[i] = 2.0 + (ti - 3) * 4
            v_f[i] = 1.0 + (ti - 3) * 6
            v_r[i] = 1.0 + (ti - 3) * 0.5
        elif ti < 8:
            prog = (ti - 3.5) / 4.5
            c[i] = 4.0 - prog * 1.5
            v_f[i] = 4.0 - prog * 2.0
            v_r[i] = 1.25 + prog * 0.75
        elif ti < 8.5:
            c[i] = 2.5 + (ti - 8) * 3
            v_f[i] = 2.0 + (ti - 8) * 4
            v_r[i] = 2.0 + (ti - 8) * 5
        else:
            prog = (ti - 8.5) / 3.5
            c[i] = 4.0 - prog * 1.0
            v_f[i] = 4.0 - prog * 1.5
            v_r[i] = 4.5 - prog * 1.5

    ax.plot(t, c, color=COLORS['blue'], linewidth=2.5,
            label='反应物浓度 c')
    ax.plot(t, v_f, color=COLORS['green'], linewidth=2.5, linestyle='-',
            label='正反应速率 v₊')
    ax.plot(t, v_r, color=COLORS['red'], linewidth=2.5, linestyle='-',
            label='逆反应速率 v₋')

    # 平衡状态区域标注
    ax.axvspan(0, 3, alpha=0.08, color=COLORS['blue'])
    ax.axvspan(4, 8, alpha=0.08, color=COLORS['green'])
    ax.axvspan(9.5, 12, alpha=0.08, color=COLORS['orange'])

    ax.text(1.5, 4.5, '平衡状态 I', ha='center', fontsize=11,
            color=COLORS['blue'])
    ax.text(6, 4.5, '平衡状态 II', ha='center', fontsize=11,
            color=COLORS['green'])
    ax.text(10.75, 4.5, '平衡状态 III', ha='center', fontsize=11,
            color=COLORS['orange'])

    # 突变标注
    ax.annotate('增加反应物\n浓度', xy=(3, 2), xytext=(4.5, 3.8),
                arrowprops=dict(arrowstyle='->', color=COLORS['gray'], lw=1.5),
                fontsize=10, color=COLORS['gray'], ha='center')
    ax.annotate('升温', xy=(8, 2.5), xytext=(9.5, 4.0),
                arrowprops=dict(arrowstyle='->', color=COLORS['gray'], lw=1.5),
                fontsize=10, color=COLORS['gray'], ha='center')

    ax.axhline(y=0, color='black', linewidth=0.8)
    ax.axvline(x=0, color='black', linewidth=0.8)
    ax.set_xlabel('时间 t', fontsize=14)
    ax.set_ylabel('浓度 / 速率', fontsize=14)
    ax.set_title('化学平衡移动（勒夏特列原理）', fontsize=18, fontweight='bold',
                 pad=15)
    ax.legend(loc='upper right', fontsize=11, framealpha=0.9)
    ax.set_xlim(-0.5, 12.5)
    ax.set_ylim(0, 5)
    ax.grid(True, alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    savefig(fig, '化学', '化学平衡移动.png')


def draw_chemistry_4():
    """原电池示意图 (Zn-Cu)"""
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(-6, 6)
    ax.set_ylim(-4, 4)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor(COLORS['bg'])
    fig.patch.set_facecolor('white')

    # 左烧杯（ZnSO4）
    left_beaker = Rectangle((-4.5, -2.5), 3, 4.5, fill=False,
                            edgecolor=COLORS['gray'], linewidth=2)
    ax.add_patch(left_beaker)
    left_fill = Rectangle((-4.5, -2.5), 3, 4.5, facecolor='#D4E6F1',
                          edgecolor='none', alpha=0.3)
    ax.add_patch(left_fill)
    ax.text(-3, 2.3, 'ZnSO₄ 溶液', ha='center', fontsize=11,
            color=COLORS['blue'])

    # Zn 电极
    zn = Rectangle((-3.3, -2.2), 0.6, 3.5, facecolor='#B0B0B0',
                   edgecolor='#666666', linewidth=2)
    ax.add_patch(zn)
    ax.text(-3.0, 1.6, 'Zn', ha='center', fontsize=12, fontweight='bold')
    ax.text(-3.0, -2.8, '负极 (阳极)', ha='center', fontsize=11,
            color=COLORS['red'])

    # 右烧杯（CuSO4）
    right_beaker = Rectangle((1.5, -2.5), 3, 4.5, fill=False,
                             edgecolor=COLORS['gray'], linewidth=2)
    ax.add_patch(right_beaker)
    right_fill = Rectangle((1.5, -2.5), 3, 4.5, facecolor='#FADBD8',
                           edgecolor='none', alpha=0.3)
    ax.add_patch(right_fill)
    ax.text(3, 2.3, 'CuSO₄ 溶液', ha='center', fontsize=11,
            color=COLORS['red'])

    # Cu 电极
    cu = Rectangle((2.7, -2.2), 0.6, 3.5, facecolor='#D4AC0D',
                   edgecolor='#B7950B', linewidth=2)
    ax.add_patch(cu)
    ax.text(3.0, 1.6, 'Cu', ha='center', fontsize=12, fontweight='bold',
            color='#7D6608')
    ax.text(3.0, -2.8, '正极 (阴极)', ha='center', fontsize=11,
            color=COLORS['green'])

    # 盐桥（U形管）
    bridge_x = np.linspace(-1.0, 1.0, 50)
    bridge_top_y = 2.0 + 0.3 * np.sin(bridge_x * np.pi)
    ax.fill_between(bridge_x, bridge_top_y, 2.0, color='#E8DAEF',
                    edgecolor=COLORS['purple'], alpha=0.7, linewidth=2)
    ax.plot(bridge_x, bridge_top_y, color=COLORS['purple'], linewidth=2)
    ax.text(0, 2.6, '盐桥', ha='center', fontsize=11,
            color=COLORS['purple'], fontweight='bold')

    # 导线
    ax.plot([-3.0, -3.0, 3.0, 3.0], [1.6, 3.0, 3.0, 1.6], 'k-',
            linewidth=2.5)

    # 电流计
    meter = Circle((0, 3.0), 0.4, facecolor='white',
                   edgecolor=COLORS['gray'], linewidth=2)
    ax.add_patch(meter)
    ax.text(0, 3.0, 'G', ha='center', va='center', fontsize=14,
            fontweight='bold', color=COLORS['gray'])

    # 电子流向（导线中，从Zn到Cu）
    ax.annotate('', xy=(0, 3.45), xytext=(-2, 3.45),
                arrowprops=dict(arrowstyle='->', color=COLORS['orange'], lw=2.5))
    ax.text(-1, 3.7, 'e⁻ 流向', fontsize=11, color=COLORS['orange'],
            fontweight='bold')

    # 离子流向
    ax.annotate('', xy=(-2.5, 0), xytext=(-3.8, 0),
                arrowprops=dict(arrowstyle='->', color=COLORS['blue'], lw=2))
    ax.text(-3.15, 0.4, 'SO₄²⁻', fontsize=10, color=COLORS['blue'])

    ax.annotate('', xy=(3.8, 0), xytext=(2.5, 0),
                arrowprops=dict(arrowstyle='->', color=COLORS['red'], lw=2))
    ax.text(3.15, 0.4, 'Cu²⁺', fontsize=10, color=COLORS['red'])

    # 电极反应
    ax.text(-3.0, -3.5, r'Zn $-$ 2e⁻ → Zn²⁺', ha='center', fontsize=12,
            color=COLORS['red'])
    ax.text(3.0, -3.5, r'Cu²⁺ + 2e⁻ → Cu', ha='center', fontsize=12,
            color=COLORS['green'])

    ax.set_title('原电池示意图（Zn-Cu 原电池）', fontsize=18, fontweight='bold',
                 pad=15)
    savefig(fig, '化学', '原电池示意图.png')


# ============================================================
# 生物
# ============================================================

def draw_biology_1():
    """光合作用过程"""
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_facecolor(COLORS['bg'])
    fig.patch.set_facecolor('white')

    # 叶绿体外形
    chloroplast = mpatches.Ellipse((6, 4), 10, 6.5, facecolor='#D5F5E3',
                                    edgecolor='#27AE60', linewidth=3)
    ax.add_patch(chloroplast)
    ax.text(6, 7.3, '叶绿体', ha='center', fontsize=14,
            fontweight='bold', color='#27AE60')

    # 上半：类囊体薄膜（光反应）
    thylakoid = Rectangle((1.5, 4.2), 9, 2.5, facecolor='#FCF3CF',
                          edgecolor='#D4AC0D', linewidth=2, alpha=0.8)
    ax.add_patch(thylakoid)
    ax.text(6, 6.3, '光反应（类囊体薄膜）', ha='center', fontsize=13,
            fontweight='bold', color='#B7950B')

    # 光反应内容
    ax.text(2.5, 5.5, r'$H_2O$', fontsize=14, color=COLORS['blue'])
    ax.annotate('', xy=(3.5, 5.5), xytext=(2.8, 5.5),
                arrowprops=dict(arrowstyle='->', color=COLORS['blue'], lw=2))
    ax.text(3.8, 5.5, '光解', fontsize=11, color=COLORS['text'])

    ax.text(5.0, 5.5, '光', fontsize=14, color=COLORS['orange'],
            fontweight='bold')
    ax.annotate('', xy=(5.5, 5.5), xytext=(5.2, 5.5),
                arrowprops=dict(arrowstyle='->', color=COLORS['orange'], lw=2))

    ax.text(6.5, 5.5, 'ATP', fontsize=13, color=COLORS['green'],
            fontweight='bold')
    ax.text(8.0, 5.5, 'NADPH', fontsize=13, color=COLORS['purple'],
            fontweight='bold')
    ax.text(9.5, 5.5, r'$O_2$', fontsize=14, color=COLORS['red'])

    # 下半：叶绿体基质（暗反应）
    stroma = Rectangle((1.5, 1.3), 9, 2.5, facecolor='#EBDEF0',
                       edgecolor='#8E44AD', linewidth=2, alpha=0.8)
    ax.add_patch(stroma)
    ax.text(6, 1.7, '暗反应（叶绿体基质）', ha='center', fontsize=13,
            fontweight='bold', color='#8E44AD')

    ax.text(2.5, 3.0, r'$CO_2$', fontsize=14, color=COLORS['gray'])
    ax.annotate('', xy=(3.5, 3.0), xytext=(2.8, 3.0),
                arrowprops=dict(arrowstyle='->', color=COLORS['gray'], lw=2))
    ax.text(3.8, 3.0, '固定', fontsize=11, color=COLORS['text'])

    ax.text(5.0, 3.0, 'C₃', fontsize=13, color=COLORS['blue'])
    ax.annotate('', xy=(6.0, 3.0), xytext=(5.4, 3.0),
                arrowprops=dict(arrowstyle='->', color=COLORS['blue'], lw=2))
    ax.text(6.3, 3.0, '还原', fontsize=11, color=COLORS['text'])

    ax.text(7.5, 3.0, r'$(CH_2O)_n$', fontsize=13, color=COLORS['green'],
            fontweight='bold')
    ax.text(9.2, 3.0, '+ C₅', fontsize=12, color=COLORS['text'])

    # 箭头连接光反应和暗反应
    ax.annotate('', xy=(6.5, 3.8), xytext=(6.5, 4.2),
                arrowprops=dict(arrowstyle='->', color=COLORS['green'], lw=2.5))
    ax.text(6.8, 4.0, 'ATP\nNADPH', fontsize=10, color=COLORS['green'])

    ax.annotate('', xy=(5.5, 4.2), xytext=(5.5, 3.8),
                arrowprops=dict(arrowstyle='->', color=COLORS['orange'], lw=2))
    ax.text(5.0, 4.0, 'ADP+Pi\nNADP⁺', fontsize=10, color=COLORS['orange'])

    ax.set_title('光合作用过程示意图', fontsize=18, fontweight='bold', pad=15)
    savefig(fig, '生物', '光合作用过程.png')


def draw_biology_2():
    """有丝分裂时期对比"""
    fig, axes = plt.subplots(1, 5, figsize=(16, 5))
    fig.patch.set_facecolor('white')

    stages = ['间期', '前期', '中期', '后期', '末期']
    descriptions = [
        'DNA复制\n蛋白质合成',
        '染色质螺旋化\n核膜核仁消失',
        '染色体排列在\n赤道板上',
        '着丝点分裂\n染色体移向两极',
        '染色体解螺旋\n核膜核仁重建'
    ]

    for idx, (ax, stage, desc) in enumerate(zip(axes, stages, descriptions)):
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_facecolor(COLORS['bg'])

        # 细胞轮廓
        cell = Circle((0, 0), 1.2, fill=False, edgecolor=COLORS['gray'],
                      linewidth=2)
        ax.add_patch(cell)

        if idx == 0:  # 间期
            # 染色质（散乱小点）
            np.random.seed(42)
            for _ in range(12):
                x, y = np.random.randn(2) * 0.4
                if x ** 2 + y ** 2 < 0.8:
                    ax.plot(x, y, 'o', color=COLORS['blue'], markersize=4)
            # 核膜核仁
            nucleus = Circle((0, 0), 0.5, fill=False, edgecolor=COLORS['gray'],
                             linewidth=1.5, linestyle='--')
            ax.add_patch(nucleus)
            ax.plot(0, 0, 'o', color=COLORS['red'], markersize=6)

        elif idx == 1:  # 前期
            # 染色体（X形）
            for pos in [(-0.3, 0.3), (0.3, -0.3)]:
                x, y = pos
                ax.plot([x - 0.15, x + 0.15], [y + 0.15, y - 0.15],
                        color=COLORS['blue'], linewidth=4)
                ax.plot([x - 0.15, x + 0.15], [y - 0.15, y + 0.15],
                        color=COLORS['blue'], linewidth=4)

        elif idx == 2:  # 中期
            # 染色体排在赤道板
            for pos in [(-0.35, 0), (0, 0), (0.35, 0)]:
                x, y = pos
                ax.plot([x, x], [y + 0.2, y - 0.2], color=COLORS['blue'],
                        linewidth=4)
            ax.axhline(y=0, color=COLORS['orange'], linewidth=1.5, linestyle='--')
            ax.text(0.8, 0, '赤道板', fontsize=9, color=COLORS['orange'])

        elif idx == 3:  # 后期
            # 染色体分开
            for pos in [(-0.6, 0.3), (-0.6, -0.3)]:
                ax.plot([pos[0], pos[0]], [pos[1] + 0.15, pos[1] - 0.15],
                        color=COLORS['blue'], linewidth=4)
            for pos in [(0.6, 0.3), (0.6, -0.3)]:
                ax.plot([pos[0], pos[0]], [pos[1] + 0.15, pos[1] - 0.15],
                        color=COLORS['blue'], linewidth=4)
            # 纺锤丝
            ax.plot([-0.6, 0], [0.3, 0.8], color=COLORS['green'],
                    linewidth=1, alpha=0.6)
            ax.plot([0.6, 0], [0.3, 0.8], color=COLORS['green'],
                    linewidth=1, alpha=0.6)

        elif idx == 4:  # 末期
            # 两个子细胞
            cell1 = Circle((-0.5, 0), 0.55, fill=False,
                           edgecolor=COLORS['gray'], linewidth=2)
            cell2 = Circle((0.5, 0), 0.55, fill=False,
                           edgecolor=COLORS['gray'], linewidth=2)
            ax.add_patch(cell1)
            ax.add_patch(cell2)
            ax.plot([-0.5, 0.5], [0, 0], 'k-', linewidth=2)
            for cx in [-0.5, 0.5]:
                ax.plot(cx, 0, 'o', color=COLORS['red'], markersize=5)
                for _ in range(4):
                    x, y = cx + np.random.randn() * 0.15, np.random.randn() * 0.15
                    ax.plot(x, y, 'o', color=COLORS['blue'], markersize=3)

        ax.set_title(stage, fontsize=14, fontweight='bold', pad=5)
        ax.text(0, -1.45, desc, ha='center', va='top', fontsize=9,
                color=COLORS['text'])

    fig.suptitle('有丝分裂时期对比', fontsize=18, fontweight='bold', y=1.02)
    savefig(fig, '生物', '有丝分裂时期.png')


def draw_biology_3():
    """DNA复制示意图（半保留复制）"""
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_facecolor(COLORS['bg'])
    fig.patch.set_facecolor('white')

    def draw_dna_strand(ax, x0, y0, length, color, label=None, dashed=False):
        style = '--' if dashed else '-'
        lw = 3 if not dashed else 2.5
        ax.plot([x0, x0 + length], [y0, y0], color=color, linewidth=lw,
                linestyle=style)
        if label:
            ax.text(x0 + length / 2, y0 + 0.25, label, ha='center',
                    fontsize=11, color=color, fontweight='bold')

    # ===== 第一步：亲代DNA双螺旋（解开前） =====
    ax.text(1.5, 7.3, '① 亲代DNA', fontsize=12, fontweight='bold',
            color=COLORS['text'])
    draw_dna_strand(ax, 1, 6.8, 2.5, COLORS['blue'], '亲代链')
    draw_dna_strand(ax, 1, 6.2, 2.5, COLORS['red'], '亲代链')
    # 双螺旋示意
    for i in range(6):
        x = 1.2 + i * 0.4
        ax.plot([x, x], [6.2, 6.8], color=COLORS['purple'], linewidth=1.5,
                alpha=0.5)

    # ===== 第二步：解旋 =====
    ax.text(5.5, 7.3, '② 解旋酶解开双链', fontsize=12, fontweight='bold',
            color=COLORS['text'])
    draw_dna_strand(ax, 4.5, 6.8, 1.0, COLORS['blue'])
    draw_dna_strand(ax, 4.5, 6.2, 1.0, COLORS['red'])
    # 叉口
    ax.plot([5.5, 5.8], [6.8, 6.5], color=COLORS['blue'], linewidth=3)
    ax.plot([5.5, 5.8], [6.2, 6.5], color=COLORS['red'], linewidth=3)
    draw_dna_strand(ax, 5.8, 6.5, 1.2, COLORS['blue'])
    draw_dna_strand(ax, 5.8, 6.5, 1.2, COLORS['red'])
    ax.text(5.8, 7.0, '解旋酶', fontsize=10, color=COLORS['green'],
            fontweight='bold')

    # ===== 第三步：半保留复制 =====
    ax.text(8.5, 7.3, '③ 半保留复制', fontsize=12, fontweight='bold',
            color=COLORS['text'])
    draw_dna_strand(ax, 8, 6.8, 1.5, COLORS['blue'])
    draw_dna_strand(ax, 8, 6.2, 1.5, COLORS['red'])
    draw_dna_strand(ax, 8, 6.8, 1.5, COLORS['red'], None, dashed=True)
    draw_dna_strand(ax, 8, 6.2, 1.5, COLORS['blue'], None, dashed=True)
    ax.text(9.8, 7.0, 'DNA聚合酶', fontsize=10, color=COLORS['orange'],
            fontweight='bold')

    # ===== 结果：两个子代DNA =====
    ax.text(3, 4.5, '结果：两个子代DNA分子', fontsize=13, fontweight='bold',
            color=COLORS['text'])

    # 子代1
    draw_dna_strand(ax, 1.5, 3.5, 3.0, COLORS['blue'], '亲代链')
    draw_dna_strand(ax, 1.5, 2.9, 3.0, COLORS['red'], '新合成链', dashed=True)
    for i in range(8):
        x = 1.7 + i * 0.35
        ax.plot([x, x], [2.9, 3.5], color=COLORS['purple'], linewidth=1.5,
                alpha=0.4)
    ax.text(3.0, 2.4, '子代DNA ①', ha='center', fontsize=11,
            color=COLORS['text'])

    # 子代2
    draw_dna_strand(ax, 7, 3.5, 3.0, COLORS['red'], '亲代链')
    draw_dna_strand(ax, 7, 2.9, 3.0, COLORS['blue'], '新合成链', dashed=True)
    for i in range(8):
        x = 7.2 + i * 0.35
        ax.plot([x, x], [2.9, 3.5], color=COLORS['purple'], linewidth=1.5,
                alpha=0.4)
    ax.text(8.5, 2.4, '子代DNA ②', ha='center', fontsize=11,
            color=COLORS['text'])

    # 图例
    ax.plot([1, 1.5], [1.2, 1.2], color=COLORS['blue'], linewidth=3)
    ax.text(1.7, 1.2, '亲代链', va='center', fontsize=10)
    ax.plot([1, 1.5], [0.8, 0.8], color=COLORS['red'], linewidth=3,
            linestyle='--')
    ax.text(1.7, 0.8, '新合成链', va='center', fontsize=10)

    ax.set_title('DNA复制：半保留复制', fontsize=18, fontweight='bold', pad=15)
    savefig(fig, '生物', 'DNA复制半保留.png')


def draw_biology_4():
    """减数分裂染色体变化（2n=4）"""
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    fig.patch.set_facecolor('white')

    stages = [
        '间期', '减I前期', '减I中期', '减I后期',
        '减II前期', '减II中期', '减II后期', '末期'
    ]
    descriptions = [
        'DNA复制\n2n=4',
        '同源染色体\n联会配对',
        '同源染色体\n排列赤道板',
        '同源染色体\n分离',
        '染色体\n散乱分布',
        '染色体排列\n赤道板',
        '着丝点分裂\n染色单体分离',
        '形成4个\n配子 n=2'
    ]

    colors_homo = [COLORS['blue'], COLORS['red']]

    for idx, (ax, stage, desc) in enumerate(
            zip(axes.flat, stages, descriptions)):
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_facecolor(COLORS['bg'])

        if idx < 7:
            cell = Circle((0, 0), 1.2, fill=False, edgecolor=COLORS['gray'],
                          linewidth=2)
            ax.add_patch(cell)

        if idx == 0:  # 间期
            for pos in [(-0.4, 0.3), (0.4, -0.3)]:
                ax.plot([pos[0] - 0.15, pos[0] + 0.15],
                        [pos[1] + 0.1, pos[1] - 0.1],
                        color=COLORS['blue'], linewidth=3, alpha=0.6)
                ax.plot([pos[0] - 0.15, pos[0] + 0.15],
                        [pos[1] - 0.1, pos[1] + 0.1],
                        color=COLORS['red'], linewidth=3, alpha=0.6)

        elif idx == 1:  # 减I前期（联会）
            # 两对同源染色体联会（X形配对）
            for dy, c1, c2 in [(0.4, COLORS['blue'], COLORS['light_gray']),
                                 (-0.4, COLORS['red'], COLORS['light_gray'])]:
                ax.plot([-0.3, 0.3], [dy + 0.15, dy - 0.15], color=c1,
                        linewidth=4)
                ax.plot([-0.3, 0.3], [dy - 0.15, dy + 0.15], color=c2,
                        linewidth=4)
            # 交叉互换示意
            ax.plot([-0.05, 0.05], [0.35, 0.45], color=COLORS['orange'],
                    linewidth=2)
            ax.text(0, 0.7, '交叉互换', fontsize=9, color=COLORS['orange'],
                    ha='center')

        elif idx == 2:  # 减I中期
            for c, dx in [(COLORS['blue'], -0.3), (COLORS['red'], 0.3)]:
                ax.plot([dx, dx], [0.4, -0.4], color=c, linewidth=4)
            ax.axhline(y=0, color=COLORS['orange'], linewidth=1, linestyle='--')

        elif idx == 3:  # 减I后期
            for c, dx in [(COLORS['blue'], -0.6), (COLORS['red'], 0.6)]:
                ax.plot([dx, dx], [0.3, -0.3], color=c, linewidth=4)
            ax.annotate('', xy=(-0.9, 0), xytext=(-0.5, 0),
                        arrowprops=dict(arrowstyle='->', color=COLORS['blue'],
                                        lw=1.5))
            ax.annotate('', xy=(0.9, 0), xytext=(0.5, 0),
                        arrowprops=dict(arrowstyle='->', color=COLORS['red'],
                                        lw=1.5))

        elif idx == 4:  # 减II前期
            for pos in [(-0.4, 0.3), (0.4, -0.3)]:
                ax.plot([pos[0], pos[0]], [pos[1] + 0.2, pos[1] - 0.2],
                        color=COLORS['blue'], linewidth=4)

        elif idx == 5:  # 减II中期
            for dx in [-0.3, 0.3]:
                ax.plot([dx, dx], [0.3, -0.3], color=COLORS['blue'],
                        linewidth=4)
            ax.axhline(y=0, color=COLORS['orange'], linewidth=1, linestyle='--')

        elif idx == 6:  # 减II后期
            for dx in [-0.7, 0.7]:
                ax.plot([dx, dx], [0.2, -0.2], color=COLORS['blue'],
                        linewidth=4)
            ax.annotate('', xy=(-1.0, 0), xytext=(-0.6, 0),
                        arrowprops=dict(arrowstyle='->', color=COLORS['blue'],
                                        lw=1.5))
            ax.annotate('', xy=(1.0, 0), xytext=(0.6, 0),
                        arrowprops=dict(arrowstyle='->', color=COLORS['blue'],
                                        lw=1.5))

        elif idx == 7:  # 末期（4个配子）
            positions = [(-0.7, 0.5), (0.7, 0.5), (-0.7, -0.5), (0.7, -0.5)]
            for px, py in positions:
                cell = Circle((px, py), 0.35, fill=False,
                              edgecolor=COLORS['gray'], linewidth=1.5)
                ax.add_patch(cell)
                ax.plot([px - 0.08, px + 0.08], [py, py], color=COLORS['blue'],
                        linewidth=2)

        ax.set_title(stage, fontsize=12, fontweight='bold', pad=5)
        ax.text(0, -1.45, desc, ha='center', va='top', fontsize=9,
                color=COLORS['text'])

    fig.suptitle('减数分裂染色体变化（2n=4）', fontsize=18, fontweight='bold',
                 y=0.98)
    savefig(fig, '生物', '减数分裂染色体变化.png')


# ============================================================
# 数学
# ============================================================

def draw_math_1():
    """三角函数 y=Asin(ωx+φ) 变换"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    fig.patch.set_facecolor('white')

    x = np.linspace(0, 4 * np.pi, 500)

    plots = [
        (r'$y = \sin(x)$', np.sin(x), '基准正弦波', COLORS['blue']),
        (r'$y = \sin(2x)$', np.sin(2 * x), '周期压缩 (ω=2)', COLORS['green']),
        (r'$y = 2\sin(x)$', 2 * np.sin(x), '振幅放大 (A=2)', COLORS['red']),
        (r'$y = \sin(x + \frac{\pi}{4})$', np.sin(x + np.pi / 4),
         '相位左移 (φ=π/4)', COLORS['orange']),
    ]

    for ax, (label, y, title, color) in zip(axes.flat, plots):
        ax.set_facecolor(COLORS['bg'])
        ax.plot(x, y, color=color, linewidth=2.5, label=label)
        ax.axhline(y=0, color='black', linewidth=0.8)
        ax.axvline(x=0, color='black', linewidth=0.8)
        ax.set_xlim(-0.5, 4 * np.pi + 0.5)
        ax.set_ylim(-2.5, 2.5)
        ax.set_title(title, fontsize=13, fontweight='bold', pad=8)
        ax.set_xlabel('x', fontsize=11)
        ax.set_ylabel('y', fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right', fontsize=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # 标出关键周期点
        if '2x' in label:
            ax.axvline(x=np.pi, color=color, linestyle='--', alpha=0.4)
            ax.text(np.pi, -2.2, r'$\pi$', ha='center', fontsize=10, color=color)
        elif '基准' in title or '放大' in title or '相位' in title:
            ax.axvline(x=2 * np.pi, color=color, linestyle='--', alpha=0.4)
            ax.text(2 * np.pi, -2.2, r'$2\pi$', ha='center', fontsize=10,
                    color=color)

    fig.suptitle(r'三角函数变换：$y = A\sin(\omega x + \varphi)$',
                 fontsize=18, fontweight='bold', y=0.98)
    savefig(fig, '数学', '三角函数变换.png')


def draw_math_2():
    """椭圆定义示意图"""
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(-5, 5)
    ax.set_ylim(-4, 4)
    ax.set_aspect('equal')
    ax.set_facecolor(COLORS['bg'])
    fig.patch.set_facecolor('white')

    # 椭圆参数
    a, b = 3.5, 2.5
    c = np.sqrt(a ** 2 - b ** 2)

    # 画椭圆
    theta = np.linspace(0, 2 * np.pi, 300)
    x = a * np.cos(theta)
    y = b * np.sin(theta)
    ax.plot(x, y, color=COLORS['blue'], linewidth=2.5)

    # 焦点
    f1, f2 = (-c, 0), (c, 0)
    ax.plot(*f1, 'o', color=COLORS['red'], markersize=10)
    ax.plot(*f2, 'o', color=COLORS['red'], markersize=10)
    ax.text(f1[0] - 0.3, f1[1] - 0.4, r'$F_1$', fontsize=14,
            color=COLORS['red'], fontweight='bold')
    ax.text(f2[0] + 0.1, f2[1] - 0.4, r'$F_2$', fontsize=14,
            color=COLORS['red'], fontweight='bold')

    # 椭圆上一点P
    p_angle = np.radians(50)
    px, py = a * np.cos(p_angle), b * np.sin(p_angle)
    ax.plot(px, py, 'o', color=COLORS['green'], markersize=10)
    ax.text(px + 0.2, py + 0.3, 'P', fontsize=14, color=COLORS['green'],
            fontweight='bold')

    # 连线 PF1, PF2
    ax.plot([px, f1[0]], [py, f1[1]], color=COLORS['orange'],
            linewidth=2, linestyle='--')
    ax.plot([px, f2[0]], [py, f2[1]], color=COLORS['orange'],
            linewidth=2, linestyle='--')

    # 标注距离
    mid1 = ((px + f1[0]) / 2, (py + f1[1]) / 2)
    mid2 = ((px + f2[0]) / 2, (py + f2[1]) / 2)
    ax.text(mid1[0] - 0.3, mid1[1] + 0.3, r'$|PF_1|$', fontsize=12,
            color=COLORS['orange'])
    ax.text(mid2[0] + 0.1, mid2[1] + 0.3, r'$|PF_2|$', fontsize=12,
            color=COLORS['orange'])

    # 长轴、短轴
    ax.plot([-a, a], [0, 0], color=COLORS['gray'], linewidth=1.5,
            linestyle='-.', alpha=0.7)
    ax.plot([0, 0], [-b, b], color=COLORS['gray'], linewidth=1.5,
            linestyle='-.', alpha=0.7)
    ax.text(a + 0.2, 0, 'A', fontsize=12, color=COLORS['gray'])
    ax.text(-a - 0.4, 0, "A'", fontsize=12, color=COLORS['gray'])
    ax.text(0.2, b + 0.2, 'B', fontsize=12, color=COLORS['gray'])
    ax.text(0.2, -b - 0.4, "B'", fontsize=12, color=COLORS['gray'])

    # 定义公式
    ax.text(0, -3.5,
            r'定义：$|PF_1| + |PF_2| = 2a$（常数）',
            ha='center', fontsize=15, color=COLORS['text'],
            bbox=dict(boxstyle='round', facecolor='#FFF9E6',
                      edgecolor=COLORS['orange'], alpha=0.9))

    ax.set_title('椭圆定义示意图', fontsize=18, fontweight='bold', pad=15)
    ax.axis('off')
    savefig(fig, '数学', '椭圆定义.png')


def draw_math_3():
    """导数几何意义"""
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_facecolor(COLORS['bg'])
    fig.patch.set_facecolor('white')

    # 曲线 y = f(x) = x^2 / 4 + 1
    x = np.linspace(-1, 6, 300)
    y = x ** 2 / 4 + 0.5
    ax.plot(x, y, color=COLORS['blue'], linewidth=2.5, label=r'$y = f(x)$')

    # 切点 x0
    x0 = 3
    y0 = x0 ** 2 / 4 + 0.5
    ax.plot(x0, y0, 'o', color=COLORS['red'], markersize=12, zorder=5)
    ax.text(x0 + 0.15, y0 + 0.25, r'$P(x_0, f(x_0))$', fontsize=13,
            color=COLORS['red'], fontweight='bold')

    # 切线 y = f'(x0)(x-x0) + f(x0) = (x0/2)(x-x0) + y0
    slope = x0 / 2
    tangent_x = np.linspace(1, 5, 100)
    tangent_y = slope * (tangent_x - x0) + y0
    ax.plot(tangent_x, tangent_y, color=COLORS['green'], linewidth=2.5,
            linestyle='--', label='切线')

    # 割线（取另一点 x1=4）
    x1 = 4.5
    y1 = x1 ** 2 / 4 + 0.5
    secant_x = np.linspace(2.5, 5, 100)
    secant_slope = (y1 - y0) / (x1 - x0)
    secant_y = secant_slope * (secant_x - x0) + y0
    ax.plot(secant_x, secant_y, color=COLORS['orange'], linewidth=2,
            linestyle='-.', label='割线')
    ax.plot(x1, y1, 's', color=COLORS['orange'], markersize=8)
    ax.text(x1 + 0.1, y1 + 0.2, 'Q', fontsize=12, color=COLORS['orange'])

    # 标注斜率
    ax.annotate('', xy=(x0 + 1.2, y0 + slope * 1.2),
                xytext=(x0, y0),
                arrowprops=dict(arrowstyle='->', color=COLORS['green'], lw=2))
    ax.text(x0 + 0.8, y0 + slope * 0.6 + 0.15,
            r"斜率 $k = f'(x_0)$", fontsize=13, color=COLORS['green'],
            fontweight='bold')

    # Δx, Δy 示意
    dx = 1.5
    dy = secant_slope * dx
    ax.plot([x0, x0 + dx, x0 + dx], [y0, y0, y0 + dy], 'k-',
            linewidth=1, alpha=0.5)
    ax.text(x0 + dx / 2, y0 - 0.25, r'$\Delta x$', ha='center', fontsize=11)
    ax.text(x0 + dx + 0.15, y0 + dy / 2, r'$\Delta y$', ha='left',
            fontsize=11)

    # 极限过程示意
    ax.annotate('当 Q→P 时，割线→切线', xy=(4.5, 5.5), xytext=(5.5, 6.5),
                arrowprops=dict(arrowstyle='->', color=COLORS['gray'], lw=1.5),
                fontsize=11, color=COLORS['gray'])

    ax.axhline(y=0, color='black', linewidth=0.8)
    ax.axvline(x=0, color='black', linewidth=0.8)
    ax.set_xlabel('x', fontsize=14)
    ax.set_ylabel('y', fontsize=14)
    ax.set_title('导数的几何意义', fontsize=18, fontweight='bold', pad=15)
    ax.legend(loc='upper left', fontsize=12)
    ax.set_xlim(-1, 6.5)
    ax.set_ylim(-0.5, 7)
    ax.grid(True, alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    savefig(fig, '数学', '导数几何意义.png')


def draw_math_4():
    """立体几何三视图"""
    fig = plt.figure(figsize=(14, 7))

    # 左：长方体直观图（3D）
    ax1 = fig.add_subplot(121, projection='3d')

    # 长方体顶点 (3x2x1.5)
    w, h, d = 3, 2, 1.5
    vertices = np.array([
        [0, 0, 0], [w, 0, 0], [w, h, 0], [0, h, 0],
        [0, 0, d], [w, 0, d], [w, h, d], [0, h, d]
    ])

    edges = [
        [0, 1], [1, 2], [2, 3], [3, 0],  # 底面
        [4, 5], [5, 6], [6, 7], [7, 4],  # 顶面
        [0, 4], [1, 5], [2, 6], [3, 7]   # 侧棱
    ]

    for edge in edges:
        points = vertices[edge]
        ax1.plot3D(*points.T, color=COLORS['blue'], linewidth=2)

    # 虚线表示隐藏棱
    hidden = [[0, 1], [0, 3], [0, 4]]
    for edge in hidden:
        points = vertices[edge]
        ax1.plot3D(*points.T, color=COLORS['blue'], linewidth=1.5,
                   linestyle='--', alpha=0.5)

    # 标注尺寸
    ax1.text(w / 2, -0.3, 0, '3', ha='center', fontsize=11, color=COLORS['text'])
    ax1.text(w + 0.2, h / 2, 0, '2', ha='left', fontsize=11, color=COLORS['text'])
    ax1.text(w + 0.2, h, d / 2, '1.5', ha='left', fontsize=11,
             color=COLORS['text'])

    ax1.set_title('长方体直观图', fontsize=14, fontweight='bold', pad=10)
    ax1.set_xlim(-0.5, 4)
    ax1.set_ylim(-0.5, 3)
    ax1.set_zlim(-0.5, 2.5)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')

    # 右：三视图
    ax2 = fig.add_subplot(122)
    ax2.set_xlim(-1, 10)
    ax2.set_ylim(-1, 8)
    ax2.set_aspect('equal')
    ax2.axis('off')
    ax2.set_facecolor(COLORS['bg'])

    # 主视图（前视，3x1.5）
    rect1 = Rectangle((0.5, 5.5), 3, 1.5, facecolor='#D6EAF8',
                      edgecolor=COLORS['blue'], linewidth=2)
    ax2.add_patch(rect1)
    ax2.text(2, 6.25, '3', ha='center', fontsize=11, color=COLORS['text'])
    ax2.text(0.3, 6.25, '1.5', ha='right', fontsize=11, color=COLORS['text'])
    ax2.text(2, 7.3, '主视图', ha='center', fontsize=13,
             fontweight='bold', color=COLORS['blue'])

    # 俯视图（上视，3x2）
    rect2 = Rectangle((0.5, 2.5), 3, 2, facecolor='#D5F5E3',
                      edgecolor=COLORS['green'], linewidth=2)
    ax2.add_patch(rect2)
    ax2.text(2, 3.5, '3', ha='center', fontsize=11, color=COLORS['text'])
    ax2.text(0.3, 3.5, '2', ha='right', fontsize=11, color=COLORS['text'])
    ax2.text(2, 4.8, '俯视图', ha='center', fontsize=13,
             fontweight='bold', color=COLORS['green'])

    # 左视图（左视，2x1.5）
    rect3 = Rectangle((5.5, 3.5), 2, 1.5, facecolor='#FCF3CF',
                      edgecolor=COLORS['orange'], linewidth=2)
    ax2.add_patch(rect3)
    ax2.text(6.5, 4.25, '2', ha='center', fontsize=11, color=COLORS['text'])
    ax2.text(5.3, 4.25, '1.5', ha='right', fontsize=11, color=COLORS['text'])
    ax2.text(6.5, 5.3, '左视图', ha='center', fontsize=13,
             fontweight='bold', color=COLORS['orange'])

    # 对齐线（虚线）
    ax2.plot([0.5, 0.5], [4.5, 5.5], 'k--', linewidth=1, alpha=0.4)
    ax2.plot([3.5, 3.5], [4.5, 5.5], 'k--', linewidth=1, alpha=0.4)
    ax2.plot([5.5, 5.5], [3.5, 5.5], 'k--', linewidth=1, alpha=0.4)
    ax2.plot([7.5, 7.5], [3.5, 5.5], 'k--', linewidth=1, alpha=0.4)

    ax2.text(5, -0.3, '长对正、高平齐、宽相等', ha='center', fontsize=13,
             color=COLORS['gray'], fontstyle='italic')

    fig.suptitle('立体几何三视图', fontsize=18, fontweight='bold', y=0.98)
    savefig(fig, '数学', '三视图示意.png')


# ============================================================
# 主程序
# ============================================================
if __name__ == '__main__':
    print("=" * 50)
    print("开始绘制 2028高考知识库 知识点示意图")
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
            print(f"  ✗ 失败: {fn.__name__} - {e}")

    print("=" * 50)
    print(f"绘制完成：{success} / {len(functions)} 张")
    print("=" * 50)
