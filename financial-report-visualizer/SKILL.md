---
name: financial-report-visualizer
description: |
  End-to-end workflow for batch financial data analysis of listed companies:
  search, verify, compute metrics (margins, YoY growth), classify into sectors,
  generate analysis reports, and produce publication-quality bubble charts
  with CJK font support and automatic label repulsion.
  Use when user provides a list of companies to analyze financial performance
  (revenue, net profit, margins, YoY trends) or asks for sector-level comparison
  with visualizations. Works for any listed company group (cross-border e-commerce,
  manufacturing, tech, etc.).
---

# Financial Report Analyzer & Visualizer

## Overview

This skill provides a systematic 6-phase workflow for analyzing and visualizing the financial data of multiple listed companies. It handles everything from data collection through to publication-quality bubble chart generation.

**Typical trigger phrases:**
- "对以下上市公司做财报统计..." (analyze financial data for these listed companies...)
- "统计XX行业的上市公司财报数据并做可视化" (stats + visualization for XX sector)
- "分析这些公司的营收和净利润趋势" (analyze revenue and profit trends)
- Any request involving batch financial data extraction + chart generation

## Workflow

### Phase 1: Data Collection

**Goal:** Search and extract financial data for each company from their latest annual reports.

1. **Split companies into batches** of 10-13 each. For large lists (30+ companies), use `sessions_spawn` with 3-4 parallel sub-agents (`agent_id="general"`).

2. **Search query template** (Chinese A-share market):
   ```
   "COMPANY_NAME 2025年年度报告 扣除非经常性损益 净利润 营业收入"
   ```
   Replace the year as needed.

3. **Required data fields per company:**
   - 营业收入 (Operating Revenue) — exact number (in 亿元)
   - 营收同比增长率 (Revenue YoY %)
   - 归属于上市公司股东的扣除非经常性损益的净利润 (Deducted NP) — exact
   - 扣非净利润同比增长率 (Deducted NP YoY %)

4. **Sub-agent task format:**
   ```
   Verify the 20XX full-year annual report data for these N Chinese listed companies.
   For EACH company, search for their official 20XX 年年度报告.
   For each company, run at least 2 separate web_search queries to cross-verify.
   Output: one markdown table with columns: 公司|营业收入(亿元)|营收同比|扣非归母净利(亿元)|扣非净利同比|数据来源
   ```

### Phase 2: Data Verification

**Goal:** Cross-check all data against official audited annual reports, correct any discrepancies.

1. **Key risk areas where errors commonly occur:**
   - Confusing 归母净利润 with 扣非归母净利润 (differ by non-recurring P&L)
   - Using preliminary 业绩快报 (earnings flash) instead of final audited 年报
   - Incorrect YoY calculation for companies with negative base values

2. **Verification process:**
   - For high-priority companies (largest by revenue, or user-specified), do targeted verification with specific search queries
   - For companies identified as "亏损" (loss-making), recalculate YoY manually:
     - If base year negative: report as "减亏" (loss narrowed) or "转亏" (turned to loss)
     - If base year positive → negative: report as "转亏" with exact %

3. **Common corrections to flag:**
   - Report both the original and corrected values in a discrepancy table
   - Note which companies have been renamed (e.g., 有棵树 → 行云科技)

### Phase 3: Derived Metrics Calculation

**Goal:** Compute secondary financial metrics.

For each company:
- **扣非净利润率** = 扣非归母净利润 / 营业收入 × 100%
- **扣非净利润率同比变化** = Current year margin − Previous year margin (percentage points)
  - Previous year margin = (Previous year NP / Previous year revenue) × 100%
  - Previous year NP = Current NP / (1 + NP_YoY)
  - Previous year revenue = Current revenue / (1 + Revenue_YoY)

### Phase 4: Sector Classification

**Goal:** Classify each company into a business sector for comparative analysis.

1. **Classification method:**
   - Spawn 3 parallel `general` sub-agents, each handling 13 companies
   - Search query: `"COMPANY_NAME 主营 业务 赛道 20XX"`
   - Classify into pre-defined sector categories that make sense for the analysis context

2. **Example sector categories (cross-border e-commerce context):**
   - 消费电子/智能硬件, 工具/五金, 家具/家居, 服饰/纺织
   - 跨境电商卖家, 运动健康/健身, 宠物用品, 安防/物联网
   - 包装/新材料, 小家电, 其他制造/代工

3. **Output format:** `公司名 | 赛道分类 | 一句话简述主营`

### Phase 5: Analysis Report Generation

**Goal:** Generate a structured markdown report with sector-level statistics and trend analysis.

**Statistics to compute per sector:**
| Metric | Formula |
| :--- | :--- |
| Company count | Count |
| Average revenue | Sum(revenue) / N |
| Average NP margin | Sum(margins) / N |
| Profit ratio | Count(NP ≥ 0) / N × 100% |
| Median revenue YoY | Median of revenue YoY values |
| Trend assessment | Qualitative (e.g., "稳健", "承压", "高增长") |

**Report structure:**
1. 赛道全景图 (sector overview table)
2. 核心赛道深度拆解 (deep dives per sector with layered analysis)
3. 趋势总判断 (overall trend summary)
4. 各公司赛道分类明细 (full classification listing)

### Phase 6: Bubble Chart Visualization

**CRITICAL — Always use the canonical script.** Do NOT write ad-hoc chart code. The canonical script at `scripts/generate_bubble_chart.py` ensures consistent styling across every invocation.

**How to use:**

1. Read `scripts/generate_bubble_chart.py` from the skill directory.
2. Replace the `data` list with your company data (format: `(name, revenue_亿, np_亿, margin_pct, sector)`).
3. Replace the `INSIGHTS` list with your analysis annotations.
4. Run via bash:
   ```
   cd workspace && MPLCONFIGDIR=/tmp/mpl_cjk /opt/anaconda3/bin/python3 << 'PYEOF'
   [script content with data block replaced]
   PYEOF
   ```
   The script outputs `bubble_chart_output.png` in the current directory.

**Script location:** `{skill_dir}/scripts/generate_bubble_chart.py`

The script handles:
- CJK font auto-detection (Arial Unicode → STHeiti → PingFang)
- 200-round force-directed label repulsion to prevent overlaps
- Leader lines connecting labels to their bubbles
- 11-color sector palette with legend
- Reference bubble scale indicators
- 80×56 inch canvas @ 100dpi (suitable for fullscreen/projection)

**Chart parameters:**
- **X-axis:** 扣非净利润率 (%)
- **Y-axis:** 主营业务收入 (亿元)
- **Bubble size:** Proportional to |扣非净利润| (area, not radius)
- **Color:** By sector
- **Border:** Black = profitable, Red = loss-making

### Tuning Parameters (edit in the script if needed)

| Parameter | Default | Effect |
| :--- | :---: | :--- |
| `BUBBLE_SCALE` | 15000 | Larger = bigger bubbles |
| `REPULSION_ITERATIONS` | 200 | More = cleaner label separation |
| `OVERLAP_TOLERANCE` | 1.15 | >1 = more space between labels |
| `FP_LABEL.size` | 76 | Company name font size (pt) |
| `FP_LEGEND.size` | 60 | Legend font size (pt) |
| `FIG_SIZE` | (80, 56) | Canvas dimensions (inches) |
| `DPI` | 100 | Output resolution |

### Color Palette

New sectors are auto-assigned default colors. To add sector-specific colors, edit `SECTOR_COLORS` in the script:
```python
SECTOR_COLORS = {
    "消费电子": "#1565C0", "工具/五金": "#E65100",
    "服饰/纺织": "#827717", "家具/家居": "#2E7D32",
    "跨境电商卖家": "#6A1B9A", "运动健康/健身": "#00838F",
    "宠物用品": "#AD1457", "其他制造": "#795548",
    "安防/物联网": "#4527A0", "包装/新材料": "#C79100",
    "小家电": "#D84315",
    # Add new sectors here
}
```

---

## Output Files

| File | Description |
| :--- | :--- |
| `20XX_sector_analysis_report.md` | Full analysis report with sector breakdown |
| `20XX_financial_report_v2.md` | Verified financial data table (all companies) |
| `bubble_chart_output.png` | Bubble chart from canonical script |

---

## Python Environment Notes

- Use system Python (`/opt/anaconda3/bin/python3` on macOS) — the bundled Python may have numpy code-signing issues
- Set `MPLCONFIGDIR=/tmp/mpl_cjk` to avoid font cache conflicts
- The canonical script auto-detects available CJK fonts — no manual font config needed
