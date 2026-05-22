[![English](https://img.shields.io/badge/lang-English-blue.svg)](README.md)

# 经营分析 — 自定义 Agent 技能

面向企业经营分析场景的自定义 AI Agent 技能，兼容 [Accio Work](https://www.accio.com/work/doc) 和 [Codex](https://codex.alibaba-inc.com/) 两个平台。

## 技能列表

### financial-report-visualizer

上市公司财务数据的批量分析工具：搜索、验证、计算指标（利润率、同比增长率）、赛道分类、生成分析报告，以及制作出版级质量的 CJK 气泡图（带标签自动避让）。

- **SKILL.md** — Agent 工作流程指令
- **scripts/generate_bubble_chart.py** — 气泡图生成脚本

### category-management-matrix

电商经营管报（Excel）分析工具：自动进行 YTD 同比分析，将产品类目划分到四象限管理矩阵（明星、现金牛、规模、瘦狗）。

- **SKILL.md** — Agent 工作流程指令
- **scripts/analyze_mgmt_report.py** — Excel 分析及图表生成脚本

### cbec-operating-analysis

跨境电商经营诊断工具。对 Amazon、Walmart、TikTok Shop、DTC 等渠道进行预实对比和同比分析。自动映射用户字段、生成可复用的分析切片、检测异常指标、归因分析，并输出会议级报告及图表。

- **SKILL.md** — Agent 工作流程指令
- **scripts/** — 报告生成 Python 脚本（`generate_operating_report.py`、`generate_charts.py`、`generate_evidence.py`、`ensure_environment.py`、`run_paths.py`）
- **references/** — 领域知识文件（分析方法论、渠道知识、字段映射、季节知识、提示词模板等）

## 使用方法

将这些技能加载到 [Accio Work](https://www.accio.com/work/doc) 或 [Codex](https://codex.alibaba-inc.com/) Agent 中即可使用。具体安装方式请参见各平台文档。

## 开发

修改技能后直接推送：

```bash
git add -A
git commit -m "描述修改内容"
git push
```

仓库中还提供了 `sync.sh` 脚本，用于从 Accio agent-core 安装目录同步最新版本到本仓库。

## 反馈

如有问题或建议，扫描下方二维码联系作者或加入社群：

<p align="left">
  <img src="https://sc01.alicdn.com/kf/A5ea0ea4d06f54c7c90f9d094ef241b7ds.jpg" width="160" alt="作者二维码">
  &nbsp;&nbsp;&nbsp;
  <img src="https://sc01.alicdn.com/kf/Ae07fe088ff2a492999115376e4716ae7f.jpg" width="160" alt="社群二维码">
</p>
