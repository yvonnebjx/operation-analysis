#!/usr/bin/env python3
"""
FINANCIAL BUBBLE CHART — canonical generation script.
Produces a consistently styled publication-quality bubble chart for
listed-company financial data with sector color-coding, CJK font support,
and automatic label repulsion to prevent overlaps.

Usage:
  1. Replace the `data` list below with your company data.
  2. (Optional) Adjust `SECTOR_COLORS` for your sector categories.
  3. Run: MPLCONFIGDIR=/tmp/mpl_cjk /opt/anaconda3/bin/python3 this_script.py

Data format — each tuple:
  (company_name, revenue_亿, deducted_np_亿, deducted_np_margin_pct, sector_name)

Canvas: 80×56 inches @ 100dpi (8000×5600px), suitable for fullscreen / projection.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
import numpy as np
import math
import os

# ── CJK Font ──────────────────────────────────────────────────────
_CJK_PATHS = [
    '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
    '/System/Library/Fonts/STHeiti Medium.ttc',
    '/System/Library/Fonts/PingFang.ttc',
]
_font_path = None
for p in _CJK_PATHS:
    if os.path.exists(p):
        _font_path = p
        break
if _font_path is None:
    raise RuntimeError("No CJK font found. Tried: " + ", ".join(_CJK_PATHS))

fm.fontManager.addfont(_font_path)

# ── Font Properties ────────────────────────────────────────────────
FP_TITLE   = fm.FontProperties(fname=_font_path, size=120)
FP_AXIS    = fm.FontProperties(fname=_font_path, size=104)
FP_LABEL   = fm.FontProperties(fname=_font_path, size=76)
FP_LEGEND  = fm.FontProperties(fname=_font_path, size=60)
FP_ANNO    = fm.FontProperties(fname=_font_path, size=72)
FP_TICK    = fm.FontProperties(fname=_font_path, size=72)
FP_LEGTITLE = fm.FontProperties(fname=_font_path, size=68)

# ── Canvas ─────────────────────────────────────────────────────────
FIG_SIZE   = (80, 56)
DPI        = 100
BUBBLE_SCALE = 15000  # area scale factor
X_RANGE    = (-22, 22)
Y_PADDING  = 20  # top padding above max revenue

# ── Sector Colors ──────────────────────────────────────────────────
SECTOR_COLORS = {
    "消费电子":       "#1565C0",
    "工具/五金":       "#E65100",
    "服饰/纺织":       "#827717",
    "家具/家居":       "#2E7D32",
    "跨境电商卖家":    "#6A1B9A",
    "运动健康/健身":   "#00838F",
    "宠物用品":       "#AD1457",
    "其他制造":       "#795548",
    "安防/物联网":     "#4527A0",
    "包装/新材料":     "#C79100",
    "小家电":         "#D84315",
}

# ── Data (REPLACE THIS BLOCK) ──────────────────────────────────────
# Format: (公司名, 营收_亿, 扣非净利润_亿, 扣非净利润率_%, 赛道)
data = [
    # ("公司名", 营收, 扣非净利, 净利率, "赛道"),
]

# ── Repulsion Parameters ───────────────────────────────────────────
REPULSION_ITERATIONS = 200
LABEL_CHAR_WIDTH_RATIO = 0.7   # CJK char width ≈ 0.7 × font size
OVERLAP_TOLERANCE = 1.15       # > 1.0 = more aggressive separation
ANCHOR_PULL = 0.03             # pull toward bubble center
REPULSION_FORCE = 0.5          # force per overlap unit
MAX_DRIFT_MULTIPLIER = 4.0     # max label distance from bubble (× label height)

# ── Insight Annotations (REPLACE THIS BLOCK) ───────────────────────
# Format: (text, x, y, fontsize, color, bold, fontproperties)
INSIGHTS = [
    # ("文本", x, y, fontsize, "#color", True/False, FP_ANNO),
]


def main():
    if not data:
        print("ERROR: data list is empty. Populate it with company data.")
        return

    fig, ax = plt.subplots(figsize=FIG_SIZE)
    fig.patch.set_facecolor('#FCFCFC')
    ax.set_facecolor('#FCFCFC')

    # ── Bubble scale ────────────────────────────────────────────
    max_np_abs = max(abs(np_val) for _, _, np_val, _, _ in data) if data else 1
    scale = BUBBLE_SCALE / max_np_abs

    # ── Estimate pixels-per-data-unit for repulsion ──────────────
    x_pixels = FIG_SIZE[0] * DPI * 0.82
    y_range = max(rev for _, rev, _, _, _ in data) + Y_PADDING
    y_pixels = FIG_SIZE[1] * DPI * 0.82
    x_rng = X_RANGE[1] - X_RANGE[0]
    px_per_x = x_pixels / x_rng
    px_per_y = y_pixels / y_range

    label_h_data = FP_LABEL.get_size() / px_per_y
    label_w_data_map = {}
    for name, _, _, _, _ in data:
        label_w_data_map[name] = len(name) * FP_LABEL.get_size() * LABEL_CHAR_WIDTH_RATIO / px_per_x

    # ── Plot bubbles ────────────────────────────────────────────
    for name, rev, np_val, margin, sector in data:
        color = SECTOR_COLORS.get(sector, '#9E9E9E')
        size = abs(np_val) * scale
        alpha_val = 0.85 if np_val >= 0 else 0.68
        edge_color = '#222222' if np_val >= 0 else '#C62828'
        edge_w = 5 if np_val >= 0 else 7
        ax.scatter(margin, rev, s=size, c=color, edgecolors=edge_color,
                   linewidths=edge_w, alpha=alpha_val, zorder=4)

    # ── Initial label positions ─────────────────────────────────
    np.random.seed(42)
    label_positions = []
    for name, rev, np_val, margin, sector in data:
        size = abs(np_val) * scale
        bubble_radius = np.sqrt(size / np.pi)
        if np_val >= 0:
            dy = bubble_radius + label_h_data * 1.2 + np.random.uniform(-2, 2)
        else:
            dy = -(bubble_radius + label_h_data * 1.2 + np.random.uniform(1, 3))
        dx = np.random.uniform(-1.0, 1.0)
        label_positions.append([margin + dx, rev + dy])

    # ── Repulsion iteration ─────────────────────────────────────
    for iteration in range(REPULSION_ITERATIONS):
        moved = False
        forces = np.zeros((len(data), 2))
        for i in range(len(data)):
            xi, yi = label_positions[i]
            name_i = data[i][0]
            w_i = max(label_w_data_map.get(name_i, 2.5), 2.0)
            h_i = label_h_data * 1.1
            for j in range(i + 1, len(data)):
                xj, yj = label_positions[j]
                name_j = data[j][0]
                w_j = max(label_w_data_map.get(name_j, 2.5), 2.0)
                h_j = label_h_data * 1.1
                dx_ij = xi - xj
                dy_ij = yi - yj
                dist = math.sqrt(dx_ij**2 + dy_ij**2)
                min_dx = (w_i + w_j) / 2 * OVERLAP_TOLERANCE
                min_dy = (h_i + h_j) / 2 * OVERLAP_TOLERANCE
                if dist < max(min_dx, min_dy) and dist > 0.001:
                    overlap = max(min_dx, min_dy) - dist
                    nx = dx_ij / dist
                    ny = dy_ij / dist
                    f = overlap * REPULSION_FORCE
                    forces[i][0] += nx * f
                    forces[i][1] += ny * f
                    forces[j][0] -= nx * f
                    forces[j][1] -= ny * f
                    moved = True
            # Anchor pull
            ax_i = data[i][3]; ay_i = data[i][1]
            dax = ax_i - xi; day = ay_i - yi
            adist = math.sqrt(dax**2 + day**2)
            if adist > label_h_data * MAX_DRIFT_MULTIPLIER:
                forces[i][0] += dax * ANCHOR_PULL
                forces[i][1] += day * ANCHOR_PULL
        for i in range(len(data)):
            label_positions[i][0] += forces[i][0]
            label_positions[i][1] += forces[i][1]
            label_positions[i][0] = np.clip(label_positions[i][0], X_RANGE[0]-3, X_RANGE[1]+3)
            label_positions[i][1] = np.clip(label_positions[i][1], -10, y_range + 10)
        if not moved:
            break

    # ── Draw labels + leader lines ──────────────────────────────
    for i, (name, rev, np_val, margin, sector) in enumerate(data):
        lx, ly = label_positions[i]
        tc = '#111111' if np_val >= 0 else '#D32F2F'
        bdist = math.sqrt((lx - margin)**2 + (ly - rev)**2)
        if bdist > label_h_data * 1.5:
            ax.plot([margin, lx], [rev, ly], color='#888888', linewidth=1.8,
                    alpha=0.5, zorder=2)
        ax.annotate(name, (lx, ly), ha='center', va='center',
                    fontsize=FP_LABEL.get_size(), fontweight='bold',
                    color=tc, fontproperties=FP_LABEL, zorder=10)

    # ── Reference bubbles ───────────────────────────────────────
    for ref_val, ref_x, ref_y, label in [(5.0, 21.5, 20, '利润参考: 5亿'),
                                          (1.0, 21.5, 10, '利润参考: 1亿')]:
        rs = ref_val * scale
        ax.scatter(ref_x, ref_y, s=rs, c='none', edgecolors='#555555',
                   linewidths=8, linestyle='--', alpha=0.4, zorder=2)
        ax.annotate(label, (ref_x + 2, ref_y - 0.5), fontsize=72, color='#555555',
                    va='center', fontproperties=FP_ANNO)

    # ── Legend ──────────────────────────────────────────────────
    legend_elems = []
    seen_sectors = set()
    for _, _, _, _, sector in data:
        if sector not in seen_sectors:
            seen_sectors.add(sector)
            n = sum(1 for d in data if d[4] == sector)
            color = SECTOR_COLORS.get(sector, '#9E9E9E')
            legend_elems.append(mpatches.Patch(facecolor=color, alpha=0.88,
                                label=f'{sector}  ({n}家)'))
    leg = ax.legend(handles=legend_elems, loc='upper left',
              fontsize=FP_LEGEND.get_size(), framealpha=0.97,
              edgecolor='#AAAAAA', fancybox=True, prop=FP_LEGEND,
              title='赛道分组', title_fontproperties=FP_LEGTITLE,
              borderpad=1.2, handlelength=2, handleheight=1.5,
              borderaxespad=1.0, labelspacing=0.8)
    leg.get_title().set_fontsize(FP_LEGTITLE.get_size())

    # ── Axis ────────────────────────────────────────────────────
    ax.set_xlabel('扣非净利润率  (%)', fontsize=FP_AXIS.get_size(),
                  weight='bold', color='#222222', labelpad=30,
                  fontproperties=FP_AXIS)
    ax.set_ylabel('主营业务收入  (亿元)', fontsize=FP_AXIS.get_size(),
                  weight='bold', color='#222222', labelpad=30,
                  fontproperties=FP_AXIS)
    ax.set_title('上市公司财报气泡图\n颜色=赛道  |  纵轴=营收  |  气泡面积 ∝ |扣非净利润|  |  黑边=盈利  ·  红边=亏损',
                 fontsize=FP_TITLE.get_size(), weight='bold', pad=60,
                 color='#111111', fontproperties=FP_TITLE)

    ax.set_xlim(*X_RANGE)
    ax.set_ylim(0, y_range)
    ax.axhline(y=0, color='#BDBDBD', linewidth=3)
    ax.axvline(x=0, color='#BDBDBD', linewidth=5, linestyle='-', alpha=0.5)
    ax.grid(True, alpha=0.08, linestyle='--', linewidth=2)

    # ── Tick labels — explicit configuration ─────────────────────
    ax.tick_params(axis='both', which='major', labelsize=FP_TICK.get_size(),
                   width=3, length=10, pad=15, color='#333333')
    ax.tick_params(axis='both', which='minor', width=1.5, length=5, color='#888888')
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontproperties(FP_TICK)
        label.set_color('#222222')

    # ── Insight annotations ─────────────────────────────────────
    box_style = dict(boxstyle='round,pad=1.0', alpha=0.93)
    for ins in INSIGHTS:
        text, x, y, fs, color, bold, fp = ins
        kw = {'fontsize': fs, 'color': color, 'fontproperties': fp}
        if bold:
            kw['fontweight'] = 'bold'
        ax.annotate(text, (x, y), **kw,
                    bbox={**box_style, 'facecolor': '#F5F5F5',
                          'edgecolor': '#BDBDBD'})

    # ── Save ────────────────────────────────────────────────────
    plt.tight_layout(pad=12)
    # Ensure sufficient margin for tick labels
    plt.subplots_adjust(left=0.06, bottom=0.06, right=0.97, top=0.95)
    outpath = os.path.join(os.getcwd(), 'bubble_chart_output.png')
    plt.savefig(outpath, dpi=DPI, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    sz = os.path.getsize(outpath) / 1024 / 1024
    print(f"Chart saved: {outpath} ({sz:.1f}MB, "
          f"{FIG_SIZE[0]}×{FIG_SIZE[1]}in @ {DPI}dpi)")
    plt.close()


if __name__ == '__main__':
    main()
