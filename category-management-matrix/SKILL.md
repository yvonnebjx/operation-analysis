---
name: category-management-matrix
description: Analyze e-commerce management reports (Excel) to perform YTD YoY analysis and categorize product categories into a 4-quadrant management matrix (Stars, Cash Cows, Volume/Question Marks, Dogs). Use this skill whenever the user provides a management report (管报) and asks for performance analysis, category growth, margin analysis, or a "matrix" (矩阵) view. It excels at identifying which categories are driving growth vs. which are losing money.
---

# Category Management Matrix Analysis

This skill automates the process of analyzing product category performance using GMV and Gross Profit data. It compares Year-To-Date (YTD) performance against the previous year and classifies categories into four quadrants based on their Growth and Margin.

## Quadrant Definitions
- **明星 (Stars)**: High Growth, High Margin (GP% ≥ 8%, YoY ≥ 0%). Focus on continued investment.
- **规模 (Volume)**: High Growth, Low Margin (GP% < 8%, YoY ≥ 0%). Focus on scale and cost optimization.
- **现金牛 (Cash Cows)**: Low Growth, High Margin (GP% ≥ 8%, YoY < 0%). Focus on harvesting profit.
- **瘦狗 (Dogs)**: Low Growth, Low Margin (GP% < 8%, YoY < 0%). Focus on elimination or replacement.

## Environment Requirement

The script requires **openpyxl==3.1.3**. Versions 3.1.4+ have a known chart layout regression bug causing axes to disappear or render incorrectly in both Excel and WPS.

```bash
pip install openpyxl==3.1.3
```

## Input Data Columns

The tool expects an Excel file (usually `实际数据` sheet) with columns for:
- **日期 (Date)**: To filter YTD data (Jan-Nov both years).
- **三级分类 (Level 3 Category)**: The dimension for aggregation.
- **GMV**: Total sales value.
- **销售毛利 (Gross Profit)**: Total profit.

## Usage

```bash
python scripts/analyze_mgmt_report.py --input "path/to/report.xlsx" --output "output.xlsx" [--month 11]
```

`--month` defaults to 11 (YTD through November). The script handles files with 200k+ rows efficiently.

## Output Workbook Structure

The generated Excel file contains 4 sheets:

### 1. 结论汇总 (Summary)

Four-column quadrant layout with color coding:

| Column | Quadrant | Color |
|--------|----------|-------|
| 第【1】区 | 盈利&GMV下滑 (Cash Cows) | Orange |
| 第【2】区 | 盈利&GMV增长 (Stars) | Green |
| 第【3】区 | 亏损&GMV增长 (Volume) | Gold |
| 第【4】区 | 亏损&GMV下滑 (Dogs) | Red |

Each category is labeled with two symbols: `品类名+符号1+符号2`
- **符号1**: GP% trend — `+` if 2024 GP% > 2023 GP%, `-` otherwise
- **符号2**: Gross Profit amount trend — `+` if 2024 profit > 2023 profit, `-` otherwise

Example: `电视挂架++` = both GP% and profit amount increased YoY.

### 2. 明细数据 (Details)

Full YTD comparison table with columns:
三级分类, 2024 YTD GMV, 2023 YTD GMV, GMV YoY, 2024 YTD 毛利, 2023 YTD 毛利, 2024 GP%, 四象限分类

### 3. 经营情况矩阵图 (Scatter Chart)

A professionally styled scatter chart with:

**Axis Configuration**:
- **X-axis**: `GMV YoY增长率`, range [-100%, 200%], interval 50%
- **Y-axis**: `24年YTD-GP%`, range [-32%, 40%], interval 8%
- Quadrant dividing lines: blue dashed lines at X=0% and Y=8%

**Visual Style**:
- Dark blue circle markers (size 8) with white borders
- No connecting lines between data points
- Chart size: 32cm × 16cm (large format for clarity)
- Horizontal axis titles
- Y-axis title at top, X-axis title at bottom-right

**Value Clipping** (for plotting only — raw data in Details sheet unchanged):
- GP% values clipped to [-40%, 40%]
- YoY values clipped to [-100%, 200%]

### 4. 图表数据 (Chart Source Data)

Raw data feeding the scatter chart: Category, GP%, GMV YoY. Hidden by default.

## WPS Compatibility Notes

The script includes two workarounds for WPS Office rendering quirks:

1. **openpyxl 3.1.3 downgrade**: Required. See Environment Requirement above.
2. **X/Y axis mapping swap** (lines 184, 193 in the script): WPS sometimes flips axis property assignment. The code maps GMV YoY settings to `x_axis` and GP% settings to `y_axis` to compensate.
3. **Explicit axes retention**: `chart.x_axis.delete = False` / `chart.y_axis.delete = False` prevents axes from being hidden.
4. **Manual plot area layout**: Prevents title/label overlap in WPS by setting explicit `plotArea` bounds.

## How to Use This Skill

When the user provides a management report and asks for analysis:

1. Read this SKILL.md for context.
2. Ensure `openpyxl==3.1.3` is installed.
3. Run the script:
   ```bash
   python /path/to/skill/scripts/analyze_mgmt_report.py --input "<user's file>" --output "analysis_result.xlsx"
   ```
4. Present a summary in chat covering:
   - Top 5 categories by GMV with YoY performance.
   - Key outliers (high growth but negative margin, sharp declines, etc.).
   - Quadrant distribution overview.
