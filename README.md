# Operation Analysis — Accio Skills

Custom agent skills for business operations analysis, built for [Accio Work](https://www.accio.com/work/doc) AI agents.

A collection of custom skills built for [Accio Work](https://www.accio.com/work/doc) AI agents.

## Skills

### financial-report-visualizer

End-to-end workflow for batch financial data analysis of listed companies: search, verify, compute metrics (margins, YoY growth), classify into sectors, generate analysis reports, and produce publication-quality bubble charts with CJK font support and automatic label repulsion.

- **SKILL.md** — Workflow instructions for the agent
- **scripts/generate_bubble_chart.py** — Canonical bubble chart generation script

### category-management-matrix

Analyze e-commerce management reports (Excel) to perform YTD YoY analysis and categorize product categories into a 4-quadrant management matrix (Stars, Cash Cows, Volume/Question Marks, Dogs).

- **SKILL.md** — Workflow instructions for the agent
- **scripts/analyze_mgmt_report.py** — Excel analysis and chart generation script

### cbec-operating-analysis

Cross-border e-commerce operating diagnosis tool. Performs budget-vs-actual and YoY analysis across Amazon, Walmart, TikTok Shop, DTC, and similar channels. Maps user-specific fields, generates reusable evidence slices, detects abnormal conditions, attributes root causes, and produces meeting-ready reports with charts.

- **SKILL.md** — Workflow instructions for the agent
- **scripts/** — Python scripts for report generation (`generate_operating_report.py`, `generate_charts.py`, `generate_evidence.py`, `ensure_environment.py`, `run_paths.py`)
- **references/** — Domain knowledge files (analysis methodology, channel knowledge, field mapping, seasonal knowledge, prompt templates, etc.)

## Usage

These skills are designed to be loaded into an Accio Work agent. See [Accio Work documentation](https://www.accio.com/work/doc) for how to install skills.

## Development

When updating a skill, edit the files in this repo directly and push:

```bash
git add -A
git commit -m "description of changes"
git push
```

A `sync.sh` script is also provided to sync the latest versions from an Accio agent-core installation into this repo.

## Feedback

If you encounter any issues or have suggestions, scan the QR code below to contact the author:

![contact](https://sc01.alicdn.com/kf/A5ea0ea4d06f54c7c90f9d094ef241b7ds.jpg)
